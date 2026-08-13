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

The key under `simulations` is the testbench name, and it is load bearing:
cicsim reads the specification from `<key>.yaml`, so `tran:` here is what
makes [tran.yaml](tran.yaml.md) the spec file. Rename the testbench and this
key has to follow, or the table comes out empty.

Under `data`, one entry per column of the table. `src` is the result directory
a corner run wrote, and `method` says how to reduce the runs in it:

| Method | Typical column | Min / max columns |
|:-|:-|:-|
| contains `typ` | median | none |
| contains `3std` | mean | mean ± 3σ |
| contains `std` | mean | mean ± 1σ |
| anything else | median | the actual min and max of the set |

The match is a substring test in the order above, so `typical` selects the
first row and `minmax` falls through to the last. Two consequences worth
knowing: `typical` reports the **median** of whatever runs are in that
directory, not "the one typical run" — it only looks like a single value
because the set usually holds one — and `minmax` reports a real minimum and
maximum, so it is the honest worst case rather than a σ estimate.

The three defaults line up with the `typical`, `etc` and `mc` targets of the
[Makefile](Makefile.md), which is why plain `make` runs exactly those before
`summary`. Add a `Lay_typ` entry pointing at `results/tran_Lay_typical` to get
the post-layout column beside the schematic one.
