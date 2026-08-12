# checkant

Turns a magic `antennacheck` log into a CSV.

```bash
../tech/script/checkant ant/<CELL>_ant.log
```

Run by `make ant` and `make antf`. Writes `ant/<CELL>_ant.csv` beside the log
and prints how many violations it found.

The log is parsed from `Running antenna checks` onwards, in blocks of five
lines starting at each `Cell:`. Each block gives one row:

| Column | From |
|:-|:-|
| `name` | the cell |
| `layer` | the plane the violation is on, e.g. `locali` |
| `ratio` | the effective antenna ratio |
| `limit` | the process limit it exceeded |
| `gaterect` | gate rectangle, as `(x1 y1),(x2 y2)` |
| `antrect` | antenna rectangle |
| `gwidth`, `gheight` | gate size, derived from `gaterect` |

Sorting the CSV by `ratio` is the quickest way to find which net to break up
first; the gate size columns tell you whether a diode is worth adding or
whether the gate is simply too small for the metal attached to it.

Requires `pandas`.
