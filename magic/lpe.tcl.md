# lpe.tcl

Parasitic extraction with capacitance, run by `make lpe`. This is the netlist
used for a post-layout simulation (`VIEW=Lay`).

The cell is flattened first, so coupling between cells is captured:

```tcl
flatten {CELL}_flat
load {CELL}_flat
extract path lpe/ext
extract all
ext2spice lvs
ext2spice cthresh 0.01
ext2spice -p lpe/ext -o lpe/{CELL}_lpe.spi
```

`cthresh 0.01` is magic's capacitance threshold: capacitors below it are
dropped. Lower it to catch more, raise it for a netlist that simulates in
reasonable time. Check magic's own documentation for the units before reading
much into the number; what is certain here is that this flow keeps far more
capacitance than [lpeh.tcl](lpeh.tcl.md), which uses `0.1`.

Resistance is *not* extracted; use [lper.tcl](lper.tcl.md) for that.

`make lpe` does three things afterwards: strips the `_flat` suffix from the
netlist, runs [script/fixlpe](../script/fixlpe.md) to put the schematic's port
list back, and then LVS's the extracted netlist against the CDL with the
capacitors removed, to prove the parasitic netlist is still the same circuit.
