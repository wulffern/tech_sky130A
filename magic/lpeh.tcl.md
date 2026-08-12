# lpeh.tcl

Hierarchical parasitic extraction, run by `make lpeh`.

Same as [lpe.tcl](lpe.tcl.md) without the `flatten`, extracting into
`lpe/exth`, and with two extra options:

```tcl
ext2spice format ngspice
ext2spice resistor off
ext2spice cthresh 0.1
```

The threshold is ten times looser than the flat flow (0.1 fF) and resistors are
off, because a hierarchical extraction is used when the flat one is too big to
finish. The netlist keeps the cell hierarchy, which makes it much smaller and
much faster to simulate, at the cost of missing every coupling capacitance
between cells.
