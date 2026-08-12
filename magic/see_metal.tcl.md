# see_metal.tcl

Hides everything, then shows only `li`, `m1`, `m2`, `m3` and `m4`.

```tcl
foreach x $all    { see no $x }
foreach x $metal  { see $x }
```

The layer lists are the same as in [see_all.tcl](see_all.tcl.md). Handy when
tracing a route through a dense cell, where the implants and diffusion make it
impossible to see which metal goes where.

`see_all.tcl` puts everything back.
