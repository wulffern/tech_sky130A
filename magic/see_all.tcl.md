# see_all.tcl

Makes every layer visible in an interactive magic session.

```tcl
source ../tech/magic/see_all.tcl
```

The file defines four layer lists, `all`, `frontend`, `backend` and `metal`,
and then runs `see` over `all`. The lists are the useful part: they are the
complete sky130A layer set split into front end of line (wells, implants,
diffusion, poly, devices, resistors), back end of line (`li` through `met5`,
vias, MiM caps, RDL, passivation) and just the routing metals.

Use it to recover from a session where layers have been hidden one at a time.
Its counterpart is [see_metal.tcl](see_metal.tcl.md).
