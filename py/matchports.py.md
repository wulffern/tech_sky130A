# matchports.py

Renumbers a magic cell's port indices so the extracted netlist's pin order
matches a reference netlist.

```bash
make matchports                      # dry run, from work/
make matchports MPOPT=--apply        # write

python3 ../tech/py/matchports.py --mag ../design/<LIB>/<CELL>.mag \
                                 --ref cdl/<CELL>.spice --apply
```

| Option | Default | Meaning |
|:-|:-|:-|
| `--mag` | required | Layout `.mag` to renumber |
| `--ref` | required | Netlist whose `.subckt` order to match |
| `--cell` | `.mag` basename | Subcircuit name to look for |
| `--apply` / `--dry-run` | dry run | Write the file |

## Why

`ext2spice` orders the `.subckt` pin list by the `port N` indices stored in the
`.mag`, not by label position or name. When a layout is built, or its ports are
relabelled, those indices often end up in a different order than the schematic.
LVS still passes, because netgen matches pins by name, but the two netlists are
then awkward to diff and any tool that assumes a fixed pin order gets it wrong.

## What it changes

Only the numbers on `port N` lines inside `<< labels >>`. Geometry, layers,
labels and net names are untouched. Ports are ordered as they appear in the
reference; ports that exist in the layout but not in the reference keep their
relative order and are pushed to the end, marked `[not in ref -> end]` in the
report. Names in the reference that are missing from the layout are warned
about in yellow.

Re-extract afterwards (`make lvs`) to pick up the new order, and reload the
cell if magic has it open.
