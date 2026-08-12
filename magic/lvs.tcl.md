# lvs.tcl

Hierarchical extraction for LVS, the default recipe behind `make lvs`.

```tcl
set SUB 0
set OPATH lvs/ext
load {PATH}/{CELL}.mag
extract path lvs/ext
extract all
ext2spice lvs
ext2spice -p lvs/ext -o lvs/{CELL}.spi
```

`ext2spice lvs` selects the option set meant for comparison rather than
simulation: no parasitic capacitance, subcircuit ports kept, device names
preserved. The netlist it writes is handed to netgen together with the
schematic CDL.

The hierarchy is kept, so each child cell appears as its own `.subckt`. That
gives readable errors when a leaf cell is wrong, but it also means every
dangling net inside a cell is promoted to a port, and connectivity that only
exists between cells is invisible. When that becomes a problem, switch the IP's
`work/Makefile` to `LVSTCL=lvsflat.tcl`, see [lvsflat.tcl](lvsflat.tcl.md).

`SUB 0` names the substrate node `0`.
