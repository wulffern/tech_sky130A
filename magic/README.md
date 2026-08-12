# magic

Everything [magic](http://opencircuitdesign.com/magic/) needs: the startup
file, the batch scripts behind `make drc`, `make lvs`, `make lpe`, `make ant`
and `make gds`, the interactive helpers, and the colour scheme.

## How the batch scripts are run

The `.tcl` files here are templates, not runnable scripts. `make/core.make`
substitutes two placeholders and writes the result into the IP's work area
before magic sees it:

```make
cat ../tech/magic/drc.tcl | perl -pe 's#{PATH}#${LMAG}#ig;s#{CELL}#${PRCELL}#ig;' \
    > drc/${PRCELL}_drc.tcl
magic -noconsole -dnull drc/${PRCELL}_drc.tcl > drc/${PRCELL}_drc.log 2>&1
```

`{PATH}` becomes `../design/<LIB>`, `{CELL}` becomes `<PREFIX><CELL>`. Every
script ends in `quit` because it runs without a console.

`-dnull` means no graphics, so these run in CI.

## The extraction scripts

Five of them, and the differences matter:

| Script | Hierarchy | Resistance | Used by |
|:-|:-|:-|:-|
| [lvs.tcl](lvs.tcl.md) | hierarchical | no | `make lvs` (default) |
| [lvsflat.tcl](lvsflat.tcl.md) | flat netlist, `hierarchy off` | no | `make lvs` with `LVSTCL=lvsflat.tcl` |
| [lvsf.tcl](lvsf.tcl.md) | flattened cell | no | `make xflvs` |
| [lpe.tcl](lpe.tcl.md) | flattened cell | no, caps only | `make lpe` |
| [lpeh.tcl](lpeh.tcl.md) | hierarchical | no, caps only | `make lpeh` |
| [lper.tcl](lper.tcl.md) | flattened cell | yes | `make lper` |
