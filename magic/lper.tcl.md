# lper.tcl

Parasitic extraction with resistance *and* capacitance, run by `make lper`.
The slowest and most complete of the three.

```tcl
flatten {CELL}_flat
load {CELL}_flat
cellname delete {CELL}
extract do resistance
extract do capacitance
extract do coupling
extract all
ext2sim labels on
ext2sim -p lpe/extr
extresist tolerance 10
extresist all
ext2spice extresist on
ext2spice cthresh 0.01
```

Resistance extraction in magic is a two step affair: `extresist` needs the
`.sim` file that `ext2sim` writes, and only then can `ext2spice extresist on`
merge the resistor network into the spice netlist. `tolerance 10` is the
percentage below which a resistance is not worth splitting a node for.

`cellname delete {CELL}` drops the unflattened original so the flattened copy
is unambiguously the top cell.

Output is `lpe/{CELL}_lper.spi`, a different name from the capacitance-only
flow, so both can exist side by side. `make lper` then LVS's it against the CDL
with the parasitic R and C filtered out.
