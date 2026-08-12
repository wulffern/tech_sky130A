# netlist_mdl

Netlists every verilog cell that a yosys script reads.

```bash
perl ../../tech/script/netlist_mdl ../../rtl/<CELL>.ys <LIB>
```

Run by the `netlist_sv` target of [sim.make](../make/sim.make.md), before yosys
itself.

It scans the `.ys` script for `work/xsch/<name>.v` paths and, for each one,
runs

```bash
make netlist_cell ver LIB=<LIB> CELL=<name>
```

which regenerates that cell's spice netlist from its schematic and then its
verilog stub via [genver](genver.md). By the time yosys runs, every module it
is told to read exists and matches the current schematics.
