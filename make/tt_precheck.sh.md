# tt_precheck.sh

Runs the Tiny Tapeout precheck locally, so a submission is not first rejected
by CI.

```bash
make precheck CELL=<CELL>            # from work/
bash tt_precheck.sh <CELL> [TAPEOUT_DIR]
```

`TAPEOUT_DIR` defaults to `../tapeout`.

It reproduces what the `TinyTapeout/tt-gds-action/precheck` action does, which
is to clone `tt-support-tools` and run

```bash
precheck/precheck.py --gds <top>.gds --tech sky130A
```

with klayout, magic and the sky130A PDK on the path. That covers magic DRC,
KLayout DRC, forbidden layers, pin labels, the pin and boundary checks, the
power and analog pin checks and verilog syntax.

## Environment

| Variable | Default |
|:-|:-|
| `TT_TOOLS` | `~/github/tt-support-tools` |
| `PDK_ROOT` | `/opt/pdk/share/pdk` |
| `EDA_BIN` | `/opt/eda/bin` |
| `KLAYOUT` | auto-detected |
| `PYTHON` | first python ≥ 3.10 found |
| `TT_TECH` | `sky130A` |

If `tt-support-tools` is missing the script says exactly what to clone.

## What it does

1. Finds klayout, including inside a macOS `.app` bundle, and a python new
   enough for the precheck.
2. Creates `tt-support-tools/precheck/.venv` on first run and installs the
   requirements. On arm64 macOS `gdstk` is built from source, so
   `CMAKE_PREFIX_PATH` is pointed at Homebrew's qhull.
3. Symlinks the klayout it found into the venv, since `precheck.py` calls
   `klayout` by name. On macOS it also drops in an `nproc` shim, because some
   KLayout DRC decks call it to pick a thread count.
4. Stages `<TAPEOUT>/precheck_run/` with `<CELL>.gds`, `<CELL>.lef`,
   `<CELL>.v` (copied from `src/project.v`) and `info.yaml`, the layout
   `precheck.py` expects.
5. Runs the precheck from inside `tt-support-tools/precheck`, which its own
   relative paths require.

`set -euo pipefail`, so the first failure stops it.
