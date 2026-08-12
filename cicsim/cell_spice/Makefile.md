# Makefile

The corner runs for one testbench. Copied into `sim/<CELL>/`.

Set at the top: `TB=tran` (the testbench name), `VIEW=Sch` (switch to `Lay` for
post-layout), `CELL`, `LIB` and `OPT`. It includes
[make/sim.make](../../make/sim.make.md) for the netlist targets.

`make` alone runs `typical etc mc summary`.

| Target | Corners |
|:-|:-|
| `typical` | `Gt Ktt Tt Vt` |
| `slow` | `Gt Kss "Th,Tl" Vl` |
| `fast` | `Gt Kff "Th,Tl" Vh` |
| `tfs` | all three process, temperature and supply corners: 27 runs |
| `etc` | `Gt "Kss,Kff,Ksf,Kfs" "Th,Tl" "Vl,Vh"`: the 16 extreme combinations |
| `ntc` | `Gt "Ktt,Kss,Kff" Tt Vt`, process only |
| `temp` | `Gt Ktt "Tt,Th,Tl" Vt`, temperature only |
| `mc` | 30 Monte Carlo runs at `Kttmm Tt Vt` |
| `test` | `typical` with `OPT="Debug"` |

Every one of them depends on `netlist`, so the netlist is always current.
Results land in `output_${VIEW}_<target>/`.

Then:

- `summary` runs `cicsim summary --output README.md`, which builds the result
  table from [summary.yaml](summary.yaml.md) and
  [tran.yaml](tran.yaml.md)
- `slide` turns that README into a slidy HTML deck with pandoc
- `clean` removes the output directories, `*.run`, `*.pdf` and `*.csv`
