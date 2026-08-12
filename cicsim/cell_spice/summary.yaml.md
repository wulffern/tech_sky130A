# summary.yaml

Tells `cicsim summary` which result sets go into the README table.

```yaml
description: TB_NCM
simulations:
   tran:
    name: Transient analysis
    description: |
      Check transient operation
    data:
      - name: Sch_typ
        src: results/tran_Sch_typical
        method: typical
      - name: Sch_etc
        src: results/tran_Sch_etc
        method: minmax
      - name: Sch_3std
        src: results/tran_Sch_mc
        method: 3std
```

One entry per column of the table. `src` is the result directory a corner run
wrote, and `method` says how to reduce the runs in it to a single number:

| Method | Reduction |
|:-|:-|
| `typical` | The single typical run |
| `minmax` | Worst case over every run in the set |
| `3std` | Mean ± 3 standard deviations, for the Monte Carlo set |

The three defaults line up with the `typical`, `etc` and `mc` targets of the
[Makefile](Makefile.md), which is why plain `make` runs exactly those before
`summary`. Add a `Lay_typ` entry pointing at `results/tran_Lay_typical` to get
the post-layout column beside the schematic one.
