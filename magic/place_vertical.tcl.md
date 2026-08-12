# place_vertical.tcl

Prints the name of every cell in memory.

```tcl
set values [ cellname list all ]
foreach x $values { echo $x }
```

Despite the name it does not place anything. The working vertical placer is the
`cicPlaceVertical` procedure in [cic.tcl](cic.tcl.md), which is loaded into
every session by [.magicrc](.magicrc.md); this file is what is left of an
earlier attempt and is useful now only as a quick listing of what is loaded.
