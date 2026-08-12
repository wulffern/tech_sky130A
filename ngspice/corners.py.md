# corners.py

Expands the `corner:` dictionary of
[cicsim/cicsim.yaml](../cicsim/cicsim.yaml.md) into a plain ngspice library
file, [corners.spi](corners.spi.md).

Every key becomes a `.lib` block holding that corner's spice text:

```spice
.lib Kss
.param mc_mm_switch=0
.param mc_pr_switch=0
    .include "$PDK_ROOT/sky130A/libs.tech/ngspice/r+c/res_typical__cap_typical.spice"
    ...
.endl
```

cicsim itself reads the yaml directly, so `corners.spi` exists for the case
where a netlist is simulated by hand, without cicsim, and wants the same corner
definitions. Run it through `make corners`, not directly, so it picks up the
relative path to the yaml.
