#!/usr/bin/env python3
"""Renumber a Magic cell's port indices so the extracted netlist port order
matches a reference SPICE/CDL netlist.

Magic's ``ext2spice`` emits a ``.subckt`` pin list ordered by the ``port N``
index numbers stored in the ``.mag`` file -- *not* by label position or name.
When a layout is built (or its ports are relabelled) the indices often end up in
a different order than the schematic ``.subckt``. That doesn't break LVS (netgen
matches pins by name), but it makes the layout and schematic netlists awkward to
diff and can confuse tools that assume a fixed pin order.

This tool reads the port order from a reference netlist's ``.subckt`` line and
rewrites the ``port N`` indices in the ``.mag`` so the two orders agree. Only the
index numbers change -- geometry, layers, labels and net names are untouched.
Ports present in the layout but not in the reference are kept and pushed to the
end (in their original order).

Example (from an IP ``work/`` dir):

    python3 ../tech/py/matchports.py \\
        --mag ../design/<LIB>/<CELL>.mag \\
        --ref cdl/<CELL>.spice --apply

Then re-extract (``make lvs`` / ``make lvs_tt``) to pick up the new order.
"""

import os
import re

import click


def read_ref_ports(path, cell):
    """Return the ordered pin list of ``.subckt <cell> ...`` from a netlist."""
    with open(path, encoding="utf-8") as f:
        text = f.read()
    # .subckt line, possibly continued with leading '+'. Match up to the first
    # line that is not a continuation.
    m = re.search(rf"^\.subckt\s+{re.escape(cell)}\s+(.*?)\n(?=[^+])",
                  text, re.S | re.M | re.I)
    if not m:
        return None
    body = m.group(1).replace("\n+", " ")
    return body.split()


def iter_mag_ports(lines):
    """Yield (flabel_idx, port_idx, name, cur_index) for each port in <<labels>>.

    A port is a ``flabel`` line immediately followed by a ``port N ...`` line.
    """
    in_labels = False
    for i, ln in enumerate(lines):
        if ln.strip() == "<< labels >>":
            in_labels = True
            continue
        if ln.startswith("<<"):
            in_labels = False
            continue
        if not in_labels:
            continue
        fm = re.match(r"flabel\s+\S+\s+.*\s(\S+)\s*$", ln)
        if fm and i + 1 < len(lines):
            pm = re.match(r"(port\s+)(\d+)(\s+.*)$", lines[i + 1])
            if pm:
                yield i, i + 1, fm.group(1), int(pm.group(2))


@click.command()
@click.option("--mag", required=True, help="Layout .mag file to renumber.")
@click.option("--ref", required=True,
              help="Reference netlist (.spice/.cdl) whose .subckt order to match.")
@click.option("--cell", default="", show_default=False,
              help="Top cell / subckt name (default: .mag basename without ext).")
@click.option("--apply/--dry-run", default=False, show_default=True,
              help="Write the file. Off by default (prints the mapping only).")
def main(mag, ref, cell, apply):
    """Renumber .mag port indices to match a reference netlist's pin order."""
    if not os.path.isfile(mag):
        raise click.ClickException(f"no such .mag: {mag}")
    if not os.path.isfile(ref):
        raise click.ClickException(f"no such reference netlist: {ref}")

    cell = cell or os.path.splitext(os.path.basename(mag))[0]

    ref_ports = read_ref_ports(ref, cell)
    if not ref_ports:
        raise click.ClickException(
            f"could not find '.subckt {cell}' in {ref}")
    ref_pos = {name: i for i, name in enumerate(ref_ports)}

    lines = open(mag, encoding="utf-8").read().splitlines()
    ports = list(iter_mag_ports(lines))
    if not ports:
        raise click.ClickException(f"no <<labels>> ports found in {mag}")

    # Order: ports found in the reference first (in reference order), then any
    # extra layout-only ports after, keeping their original file order.
    BIG = len(ref_pos) + len(ports)
    order = sorted(
        range(len(ports)),
        key=lambda k: (ref_pos.get(ports[k][2], BIG + k),))

    new_index = {}          # position-in-ports -> new port index
    for new_idx, k in enumerate(order):
        new_index[k] = new_idx

    # Report + apply.
    changed = 0
    click.echo(f"cell {cell}: {len(ports)} ports  (ref has {len(ref_ports)})")
    for k in order:
        _, port_line_idx, prefix, old = ports[k]
        name = ports[k][2]
        new = new_index[k]
        extra = "" if name in ref_pos else "  [not in ref -> end]"
        if old != new:
            changed += 1
        click.echo(f"  idx {new:3d}  <- was {old:3d}   {name}{extra}")
        if apply:
            m = re.match(r"(port\s+)\d+(\s+.*)$", lines[port_line_idx])
            lines[port_line_idx] = f"{m.group(1)}{new}{m.group(2)}"

    # Warn about names present only on one side.
    mag_names = {p[2] for p in ports}
    for name in ref_ports:
        if name not in mag_names:
            click.secho(f"  warn: '{name}' in ref but not in layout", fg="yellow")

    click.echo(f"\n{changed}/{len(ports)} indices renumbered")
    if apply:
        open(mag, "w", encoding="utf-8").write("\n".join(lines) + "\n")
        click.echo(f"WROTE {mag}  (reload in magic, then re-extract)")
    else:
        click.echo("(dry run; pass --apply to write)")


if __name__ == "__main__":
    main()
