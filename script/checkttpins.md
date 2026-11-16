# checkttpins

Checks the ports of a Tiny Tapeout top level layout against the tile DEF.

```bash
make ttpins CELL=tt_um_<name>                         # from work/
../tech/script/checkttpins ../design/<LIB>/tt_um_<name>.mag
../tech/script/checkttpins <mag> --def <other.def>
```

For every pin in the DEF (default [tt/tt_block_1x1_pg.def](../tt/README.md))
it requires an `flabel` in the `.mag` with

- the same name,
- exactly the same rectangle, in magic's 5 nm units, and
- the same `port` direction (`input`/`output`).

It prints one line per problem (`MISSING`, `POSITION` or `DIR`) and then a
`PINS OK`/`PINS FAIL` verdict, and exits 1 on any problem.

The power stripes (`VDPWR`, `VGND`) are not DEF pins, so they are not checked
here. The full [tt_precheck.sh](../make/tt_precheck.sh.md) covers those.

## Why

The LELO template had its 43 met4 signal pins mirrored in X: each net sat
at `177.56 µm − x_def`. Every pad was on the DEF grid, so it looked right, and
the problem only came out at tapeout. This check takes a fraction of a second
and runs before an IP is pushed, see `makegroups.py` and
[rey.yaml](../cicconf/rey.yaml.md).

Requires `click`.
