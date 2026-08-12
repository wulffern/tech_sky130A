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

`cthresh 0.01` keeps every capacitor down to 0.01 fF. Lower it to catch more,
raise it for a netlist that simulates in reasonable time.

Resistance is *not* extracted; use [lper.tcl](lper.tcl.md) for that.

`make lpe` does three things afterwards: strips the `_flat` suffix from the
netlist, runs [script/fixlpe](../script/fixlpe.md) to put the schematic's port
list back, and then LVS's the extracted netlist against the CDL with the
capacitors removed, to prove the parasitic netlist is still the same circuit.
