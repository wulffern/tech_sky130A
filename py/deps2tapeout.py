#!/usr/bin/env python3
"""Pin the exact dependency versions used for a tapeout delivery.

An IP block references its dependencies as symlinks:

    tech               -> ../tech_sky130A
    design/<DEP>       -> ../../<repo>/design/<DEP>

Each link target lives in its own git repository (managed by cicconf). For a
reproducible delivery we want to know the *exact* commit of every dependency
that went into the shipped GDS -- not just the branch name cicconf tracks.

This script walks the ``tech`` symlink and every symlink under ``design/`` (plus
any ``--extra`` repos such as ``cpdk`` that are not reachable through a symlink),
resolves each to its git repository, and writes a cicconf-style ``config.yaml``
into the tapeout folder. The output is a dependency *lock*: ``name: {remote,
revision}`` entries with ``#-`` description comments, where ``revision`` is
pinned to the exact commit SHA instead of a branch name, so ``cicconf clone``
can reconstruct the exact environment. The monorepo ``options`` block (template/
project/technology) is intentionally omitted -- this is a lock file, not a full
cicconf project config. Repositories with uncommitted changes are listed as a
warning (the pinned SHA does not capture a dirty tree); pass ``--fail-on-dirty``
to turn that into a hard error for a strictly reproducible delivery.
"""

import os
import re

import subprocess

import click
import yaml


def git(repo, *args):
    """Run a git command in *repo*; return stripped stdout or None on failure."""
    try:
        return subprocess.check_output(
            ["git", "-C", repo, *args],
            stderr=subprocess.DEVNULL, text=True).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def repo_info(path):
    """Return git metadata for the repository containing *path*, or None."""
    top = git(path, "rev-parse", "--show-toplevel")
    if not top:
        return None
    # Note: git() strips the whole output, which would eat the leading status
    # column of the first porcelain line -- read it raw so every line keeps its
    # "XY PATH" columns intact. --untracked-files=no ignores new/untracked (??)
    # files: only tracked changes count towards "dirty".
    try:
        raw = subprocess.run(["git", "-C", top, "status", "--porcelain",
                              "--untracked-files=no"],
                             stderr=subprocess.DEVNULL, text=True,
                             stdout=subprocess.PIPE).stdout
    except FileNotFoundError:
        raw = ""
    changes = [ln[:2].strip() + " " + ln[3:] for ln in raw.splitlines() if ln.strip()]
    return {
        "name": os.path.basename(top),
        "remote": git(top, "remote", "get-url", "origin"),
        "revision": git(top, "rev-parse", "HEAD"),
        "dirty": bool(changes),
        "changes": changes,
    }


def iter_links(ip_root):
    """Yield (relpath, target) for the tech symlink and every design/ symlink."""
    tech = os.path.join(ip_root, "tech")
    if os.path.islink(tech):
        yield "tech", tech

    design = os.path.join(ip_root, "design")
    if os.path.isdir(design):
        for entry in sorted(os.listdir(design)):
            p = os.path.join(design, entry)
            if os.path.islink(p):
                yield os.path.join("design", entry), p


def read_cicconf(path):
    """Return (options, {name: description}) parsed from a cicconf config.yaml.

    Descriptions come from either a ``#- ...`` comment preceding the key or a
    ``description:`` field on the entry.
    """
    if not path or not os.path.isfile(path):
        return None, {}

    with open(path, encoding="utf-8") as f:
        text = f.read()

    # Comment-based descriptions: a "#- desc" line immediately above a top-level key.
    descs = {}
    pending = None
    for line in text.splitlines():
        m = re.match(r"^#-\s*(.+?)\s*$", line)
        if m:
            pending = m.group(1)
            continue
        key = re.match(r"^([A-Za-z0-9_]+):\s*$", line)
        if key:
            if pending and key.group(1) != "options":
                descs[key.group(1)] = pending
            pending = None
        elif line.strip():
            pending = None

    # Field-based descriptions + the options block.
    try:
        data = yaml.safe_load(text) or {}
    except yaml.YAMLError:
        data = {}
    for name, entry in data.items():
        if isinstance(entry, dict) and entry.get("description"):
            descs.setdefault(name, entry["description"])

    return data.get("options"), descs


@click.command()
@click.option("--ip-root", default="..", show_default=True,
              help="IP directory containing the 'tech' symlink and 'design/'.")
@click.option("--out", default="../tapeout/ip/config.yaml", show_default=True,
              help="Destination config.yaml.")
@click.option("--source-config", default="", show_default=False,
              help="cicconf config.yaml to inherit the 'options' block from "
                   "(default: <ip-root>/../config.yaml).")
@click.option("--include-self/--no-include-self", default=True, show_default=True,
              help="Also pin the IP repository that owns this design.")
@click.option("--extra", multiple=True, default=["../cpdk"], show_default=True,
              help="Extra repo paths (relative to --ip-root) to pin that are not "
                   "reachable via the tech/design symlinks, e.g. cpdk. Repeatable.")
@click.option("--fail-on-dirty/--no-fail-on-dirty", default=False, show_default=True,
              help="Abort if any dependency has uncommitted changes. Off by "
                   "default (dirty trees are common while iterating); the "
                   "modified files are listed as a warning instead. Turn on for "
                   "a strictly reproducible delivery.")
def main(ip_root, out, source_config, include_self, extra, fail_on_dirty):
    """Write a cicconf config.yaml pinning exact dependency commit SHAs."""
    ip_root = os.path.abspath(ip_root)
    monorepo_cfg = source_config or os.path.join(ip_root, "..", "config.yaml")
    ip_cfg = os.path.join(ip_root, "config.yaml")

    _, descs = read_cicconf(monorepo_cfg)
    _, ip_descs = read_cicconf(ip_cfg)
    descs.update(ip_descs)   # IP-level descriptions win

    # Collect one entry per repository, preserving discovery order.
    order = []
    seen = set()

    def add(info):
        if info and info["name"] not in seen:
            seen.add(info["name"])
            order.append(info)

    if include_self:
        add(repo_info(ip_root))
    for e in extra:
        p = os.path.join(ip_root, e)
        if os.path.exists(p):
            add(repo_info(os.path.realpath(p)))
        else:
            click.secho(f"  note: extra dep '{e}' not found at {p}, skipping",
                        fg="yellow")
    for _, target in iter_links(ip_root):
        add(repo_info(os.path.realpath(target)))

    if not order:
        raise click.ClickException(f"No dependency links found under {ip_root}")

    # Report status and detect dirty / remote-less repositories.
    dirty = []
    for info in order:
        if info["dirty"]:
            dirty.append(info["name"])
        state = "DIRTY" if info["dirty"] else "clean"
        click.secho(f"  {info['name']:24s} {str(info['revision'])[:12]}  [{state}]",
                    fg="yellow" if info["dirty"] else "green")
        for change in info.get("changes", []):
            click.secho(f"      {change}", fg="yellow")
        if info["remote"] is None:
            click.secho(f"  warn: {info['name']} has no 'origin' remote", fg="yellow")

    if dirty and fail_on_dirty:
        raise click.ClickException(
            "uncommitted changes in: " + ", ".join(dirty) + "\n"
            "Commit (and push) these before delivery so the pinned SHAs are "
            "reproducible, or drop --fail-on-dirty to pin the current HEAD "
            "anyway.")

    # Build the file text in cicconf style (comment + entries). The 'options'
    # block from the monorepo config is intentionally omitted: this file is a
    # dependency lock, not a full cicconf project config.
    chunks = []
    for info in order:
        block = ""
        if info["name"] in descs:
            block += f"#- {descs[info['name']]}\n"
        block += yaml.safe_dump(
            {info["name"]: {"remote": info["remote"], "revision": info["revision"]}},
            sort_keys=False, default_flow_style=False).rstrip()
        chunks.append(block)

    header = ("# Dependency lock for tapeout delivery -- AUTO-GENERATED.\n"
              "# 'revision' is the exact commit SHA that produced the delivered "
              "GDS.\n# Regenerate with tech/py/deps2tapeout.py (make deliver).\n\n")

    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(header + "\n\n".join(chunks) + "\n")

    click.echo(f"Wrote {out} ({len(order)} dependencies)")
    if dirty:
        click.secho("warn: pinned SHAs do not capture uncommitted changes in: " +
                    ", ".join(dirty) + " (commit for a reproducible delivery)",
                    fg="yellow")


if __name__ == "__main__":
    main()
