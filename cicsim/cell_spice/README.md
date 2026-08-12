# cell_spice

The template for a new spice testbench. Scaffolded by the `cell` target of
[sim.make](../../make/sim.make.md):

```bash
cicsim simcell <LIB> <CELL> ../tech/cicsim/cell_spice/template.yaml
```

which creates `sim/<CELL>/` holding a copy of every file here, with `${IP}` and
`${CELL}` substituted.

| File | What it is |
|:-|:-|
| [template.yaml](template.yaml.md) | The scaffold description cicsim reads |
| [Makefile](Makefile.md) | The corner runs: `typical`, `slow`, `fast`, `etc`, `mc`, ... |
| [tran.spi](tran.spi.md) | The testbench netlist |
| [tran.meas](tran.meas.md) | Measurements to extract from the raw file |
| [tran.py](tran.py.md) | Optional python post-processing |
| [tran.yaml](tran.yaml.md) | Specification limits for the summary table |
| [summary.yaml](summary.yaml.md) | Which results the README summary is built from |

The `tran` prefix is the testbench name. Copy the five `tran.*` files to
`<name>.*` and set `TB=<name>` in the Makefile to add a second testbench, an
`ac` or a `noise` one.
