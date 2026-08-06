#!/usr/bin/env bash
#
# Run the Tiny Tapeout precheck locally, reproducing the checks that the
# "TinyTapeout/tt-gds-action/precheck" GitHub action runs in CI (Magic DRC,
# KLayout DRC/forbidden-layer/pin-label, pin check, boundary check, power/analog
# pin checks, verilog syntax, ...).
#
# The action really just clones tt-support-tools and runs
#   precheck/precheck.py --gds <top>.gds --tech sky130A
# with klayout, magic and the sky130A PDK available. We do exactly the same
# thing against a locally-staged copy of the tapeout submission.
#
# Usage:
#   tt_precheck.sh <CELL> [TAPEOUT_DIR]
#
# Environment overrides (sensible macOS/aicex defaults):
#   TT_TOOLS   tt-support-tools checkout      (default: ~/github/tt-support-tools)
#   PDK_ROOT   PDK root holding sky130A       (default: /opt/pdk/share/pdk)
#   EDA_BIN    dir with magic/netgen          (default: /opt/eda/bin)
#   KLAYOUT    klayout executable             (default: auto-detected)
#   PYTHON     python >=3.10 for the venv     (default: auto-detected)
#   TT_TECH    precheck tech name             (default: sky130A)
#
set -euo pipefail

CELL="${1:?usage: tt_precheck.sh <CELL> [TAPEOUT_DIR]}"
TAPEOUT="${2:-../tapeout}"

TT_TOOLS="${TT_TOOLS:-$HOME/github/tt-support-tools}"
PDK_ROOT="${PDK_ROOT:-/opt/pdk/share/pdk}"
EDA_BIN="${EDA_BIN:-/opt/eda/bin}"
TT_TECH="${TT_TECH:-sky130A}"

# --- locate a klayout executable (CLI or macOS app bundle) ----------------
if [ -z "${KLAYOUT:-}" ]; then
    if command -v klayout >/dev/null 2>&1; then
        KLAYOUT="$(command -v klayout)"
    elif [ -x /Applications/KLayout/klayout.app/Contents/MacOS/klayout ]; then
        KLAYOUT=/Applications/KLayout/klayout.app/Contents/MacOS/klayout
    else
        echo "error: klayout not found (set KLAYOUT=/path/to/klayout)" >&2
        exit 1
    fi
fi

# --- locate a python >=3.10 for the precheck venv -------------------------
if [ -z "${PYTHON:-}" ]; then
    for p in python3.13 python3.12 python3.11 python3.10 python3; do
        if command -v "$p" >/dev/null 2>&1 && \
           "$p" -c 'import sys; sys.exit(0 if sys.version_info>=(3,10) else 1)' 2>/dev/null; then
            PYTHON="$p"; break
        fi
    done
    [ -z "${PYTHON:-}" ] && { echo "error: need python>=3.10 (set PYTHON=...)" >&2; exit 1; }
fi

[ -f "$TT_TOOLS/precheck/precheck.py" ] || {
    echo "error: tt-support-tools not at $TT_TOOLS (set TT_TOOLS=...)" >&2
    echo "       git clone https://github.com/TinyTapeout/tt-support-tools $TT_TOOLS" >&2
    exit 1
}
[ -d "$PDK_ROOT/$TT_TECH" ] || {
    echo "error: $TT_TECH not found under PDK_ROOT=$PDK_ROOT (set PDK_ROOT=...)" >&2
    exit 1
}

# --- bootstrap the precheck venv on first run -----------------------------
VENV="$TT_TOOLS/precheck/.venv"
if [ ! -x "$VENV/bin/python" ]; then
    echo ">> creating precheck venv ($PYTHON)"
    "$PYTHON" -m venv "$VENV"
    "$VENV/bin/pip" install -q --upgrade pip
    # gdstk builds from source on arm64 macOS and needs qhull headers.
    if command -v brew >/dev/null 2>&1 && brew --prefix qhull >/dev/null 2>&1; then
        export CMAKE_PREFIX_PATH="$(brew --prefix qhull)${CMAKE_PREFIX_PATH:+:$CMAKE_PREFIX_PATH}"
    fi
    "$VENV/bin/pip" install -q -r "$TT_TOOLS/precheck/requirements.txt"
fi
# Expose the found klayout to precheck.py (it calls "klayout" via subprocess).
ln -sf "$KLAYOUT" "$VENV/bin/klayout"

# Some klayout DRC decks call `nproc` (Linux-only) to pick a thread count;
# provide a shim on macOS so those checks can run.
if ! command -v nproc >/dev/null 2>&1 && [ ! -x "$VENV/bin/nproc" ]; then
    printf '#!/bin/sh\nsysctl -n hw.ncpu 2>/dev/null || echo 1\n' > "$VENV/bin/nproc"
    chmod +x "$VENV/bin/nproc"
fi

# --- stage the submission the way precheck.py expects ---------------------
#   <dir>/<CELL>.gds, <CELL>.lef, <CELL>.v, and a discoverable info.yaml
STAGE="$TAPEOUT/precheck_run"
rm -rf "$STAGE"; mkdir -p "$STAGE"
cp "$TAPEOUT/gds/$CELL.gds"  "$STAGE/$CELL.gds"
cp "$TAPEOUT/lef/$CELL.lef"  "$STAGE/$CELL.lef"
cp "$TAPEOUT/src/project.v"  "$STAGE/$CELL.v"
cp "$TAPEOUT/info.yaml"      "$STAGE/info.yaml"

# --- run precheck (cwd must be tt-support-tools/precheck for its rel paths) -
STAGE_ABS="$(cd "$STAGE" && pwd)"
echo ">> running precheck on $CELL ($TT_TECH)"
cd "$TT_TOOLS/precheck"
PDK_ROOT="$PDK_ROOT" PDK="$TT_TECH" \
PATH="$EDA_BIN:$VENV/bin:$PATH" \
    "$VENV/bin/python" precheck.py --gds "$STAGE_ABS/$CELL.gds" --tech "$TT_TECH"
