# lvsflat.tcl

Flat extraction for LVS. Selected per IP with `LVSTCL=lvsflat.tcl` in the
`work/Makefile`.

Same extraction as [lvs.tcl](lvs.tcl.md), but the netlist is resolved by
geometry across the whole tree:

```tcl
ext2spice lvs
ext2spice hierarchy off
ext2spice subcircuit top on
```

The comment at the top of the file explains why this exists. Hierarchical
extraction promotes every dangling net in a cell to a subcircuit port: the
dummy poly strips of a transistor pattern and the unrouted bulk straps of
tap-less leaf cells all become pins, and netgen then drowns the real comparison
in port errors. Worse, it cannot see a connection that only exists between
cells, so an assembly where a strap shorts two rails can be DRC clean and still
pass LVS.

With `hierarchy off`, dangling nets stay internal node names instead of ports,
wells and substrate resolve against the taps that are actually there, and
netgen flattens the schematic side itself. `subcircuit top on` keeps the top
cell's own port list, so pin matching still means something.

The cost is that a mismatch is reported against one big flat netlist. Keep
running the hierarchical flow per cell for readable errors and for property
checking; [script/checklvs](../script/checklvs.md) is passed `--noprop` in the
flat flow because symmetric gates resolved by property look like property
errors there.
