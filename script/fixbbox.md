# fixbbox

Repairs the `FIXED_BBOX` property of magic cells so it matches the cell's true
geometric bounding box.

```bash
make fixbbox                    # dry run, from work/
make fixbbox BBOPT=--apply      # write

fixbbox <lib_mag_dir> [exclude_cell] [--apply]
```

A stale or oversized `FIXED_BBOX` makes magic report the wrong cell extent, and
the cell then overhangs its parent or its tile. It also breaks the placement
helpers in [magic/cic.tcl](../magic/cic.tcl.md), which step by exactly that
property.

## How it gets the right answer

Magic computes the bounding box, not the script: `select top cell; box values`
handles magscale, hierarchy and arrays correctly, and no reimplementation of
that would stay correct for long.

The awkward part is getting the value back out without letting magic rewrite
the file. Magic is run on the real file so child cells resolve, it writes the
property and saves, the new value is read back in the file's own units, and
then the original bytes are restored. Only the `string FIXED_BBOX` line of the
original is patched. A full magic re-serialization would otherwise upgrade the
file format, renaming layers and regenerating the checkpaint layer, which turns
a one line fix into an unreviewable diff.

The property is added under `<< properties >>` if the cell has none, and a
properties section is created before `<< end >>` if that is missing too.

## Safety

- Dry run by default; `--apply` is required to write.
- `exclude_cell`, normally the top tile, keeps its fixed tile size.
- Symlinked `.mag` files are always skipped: they point at shared library
  sources outside the IP and must not be modified.

Output is one line per cell, in colour: `ok`, `would fix`, `fixed`, `symlink,
skipped` or `could not compute bbox`.
