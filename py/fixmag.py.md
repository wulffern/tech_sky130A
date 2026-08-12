# fixmag.py

Repairs the library path on every `use` line in a magic cell hierarchy.

```bash
python3 ../tech/py/fixmag.py ../design/<LIB>/<CELL>.mag      # make fixmag
```

A `.mag` file references a child cell as

```
use MY_CHILD  MY_CHILD_0 ../SOME_LIB
```

and the third field is a path that magic has to resolve. When a cell is moved
between libraries, or a layout is assembled from cells that came from several
places, those paths go stale and magic silently loads the wrong cell or none
at all.

The script reads the cell, and for every `use` looks for `<cellname>.mag` in
any sibling directory (`../*/`). Exactly one hit rewrites the library field to
that directory. More than one hit is an error, reported and left alone, since
guessing between two cells with the same name would be worse than leaving it
broken. It then recurses into every child it resolved and rewrites those too.

Changed lines are printed as `Old:` / `New:` pairs, and only files that
actually contain `use` lines are rewritten.

`JNW_TR_SKY130A` and `JNW_ATR_SKY130A` are in an exclude list: those are shared
standard cell libraries reached through a symlink, and must not be rewritten
from inside an IP.

Note that this writes in place with no dry run, so commit before running it.
