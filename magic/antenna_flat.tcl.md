# antenna_flat.tcl

Flat antenna check, run by `make antf`.

Same as [antenna.tcl](antenna.tcl.md), except the cell is flattened into
`{CELL}_flat` first and the extraction goes to `ant/extf`:

```tcl
flatten {CELL}_flat
load {CELL}_flat
```

This is the check that matters for a net that runs through several cells. A
hierarchical antenna check only sees the metal inside one cell, so a long route
assembled at the top level looks harmless in every child and is only caught
here.
