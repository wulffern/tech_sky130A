# checkkdrc

Summarises a KLayout DRC report in the same one line style as the magic DRC
post-processing, so `make kdrc` reads like `make drc`.

```bash
python3 ../tech/script/checkkdrc drc/<CELL>_drc.xml <CELL>
```

Output on a clean run:

```
MY_CELL                                  [ KDRC OK   ]
```

and otherwise the violations, most common first:

```
MY_CELL                                  [ KDRC FAIL ]
    psdm.1 .................... 16
    li.3 ......................  4
    total                        20
```

It counts `<category>` elements in the XML report `make kdrc` produced, and
exits 0 only when the total is zero, so it can gate a build the way `make drc`
and `make lvs` do. `make kdrc` currently appends `|| true`, so the KLayout
result is advisory. A missing or malformed report prints `KDRC ERR` with the
exception and also exits 1.

Standard library only.
