# genver

Writes an empty verilog module with the right ports, from a spice netlist.

```bash
cd xsch && ../../tech/script/genver <CELL>.spice <CELL>
```

Run by `make ver`. Writes `<CELL>.v` in the current directory.

The point is to give a digital tool a black box with the correct pin list: the
module has ports and nothing else, no logic.

Port names come from the `.subckt` line and its `+` continuations. Direction
comes from the xschem `*.ipin`, `*.opin` and `*.iopin` comment lines that
xschem writes above the subcircuit: `.ipin` becomes `input wire`, `.opin` and
`.iopin` become `output wire`. Repeated bus bits such as `D<3> D<2> D<1> D<0>`
collapse into a single `[3:0] D`.

Ports are emitted in the order they appear in the `.subckt`, not the order the
direction comments appear, so the verilog pin order matches the spice one.
