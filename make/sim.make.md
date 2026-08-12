# sim.make

Netlist targets for a simulation directory. Included from
`sim/<CELL>/Makefile`, two levels below the IP root, which is why the paths
here start with `../../`.

| Target | What it does |
|:-|:-|
| `netlist` | `netlist_cell`, then writes `xdut.spi` with [genxdut](../script/genxdut.md) |
| `netlist_cell` | Makes `../../work/xsch/<CELL>.spice`, and for `VIEW=Lay` also the CDL and the extracted netlist |
| `netlist_sv` | The mixed signal path: yosys synthesis, then `xdut.spi` |
| `cell` | Scaffolds a new spice testbench from [cicsim/cell_spice/template.yaml](../cicsim/cell_spice/template.yaml.md) |
| `cellsv` | The same from `cicsim/cell_sv/template.yaml` |
| `ver` | Regenerates the verilog stub for the cell |

The `xdut.spi` indirection exists because port ordering has changed between
xschem versions. A testbench includes `../xdut.spi` rather than instantiating
the DUT itself, so the instance line is regenerated from the netlist that was
just written and the order is always right.

`netlist_sv` runs [netlist_mdl](../script/netlist_mdl.md) over the cell's
`.ys` script to netlist each verilog cell it mentions, then runs yosys, then
builds the DUT instance from the synthesised netlist.

Note `cellsv` refers to a `cicsim/cell_sv/` template directory that this
repository does not currently ship; only
[cell_spice](../cicsim/cell_spice/README.md) is here.
