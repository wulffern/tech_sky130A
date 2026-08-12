# lvsf.tcl

Extraction from a flattened *cell*, run by `make xflvs`.

The difference from [lvsflat.tcl](lvsflat.tcl.md) is where the flattening
happens. Here magic flattens the layout itself before extracting:

```tcl
flatten {CELL}_flat
load {CELL}_flat
extract all
ext2spice lvs
ext2spice format ngspice
```

so the extractor sees one cell with no children at all. `lvsflat.tcl` keeps the
layout hierarchy and only flattens when writing the netlist.

Flattening the layout is the bigger hammer: it resolves everything, but it also
loses the cell names, so a mismatch points at a device rather than at a block.
Reach for it when `lvsflat.tcl` still reports something that looks like a
hierarchy artefact.
