# cicsim

Setup for [cicsim](https://github.com/wulffern/cicsim), the simulation runner.

Two things live here:

- [cicsim.yaml](cicsim.yaml.md), the corner definitions every IP shares. A new
  IP symlinks it into its `sim/` directory, so all designs run the same
  corners.
- [cell_spice/](cell_spice/README.md), the template for a new spice testbench.

A simulation is named by picking one value from each corner group:

```bash
cicsim run --name Sch_typical tran Sch Gt Ktt Tt Vt
```

`Gt` general, `Ktt` process, `Tt` temperature, `Vt` supply. Give a comma
separated list and cicsim runs the cross product, which is what the `etc`,
`tfs` and `temp` targets of the [cell_spice Makefile](cell_spice/Makefile.md)
do.
