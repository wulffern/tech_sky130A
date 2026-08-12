# Makefile

Two targets, both wrapping [genyaml](genyaml.md), for regenerating the process
corners after a PDK update.

```bash
cd py
make parse                      # walk the PDK spice library into spice.yaml
make process > corners.yaml     # turn spice.yaml into cicsim corner blocks
```

`parse` reads `$PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice`.

`process` prints the corner definitions with `--prefix K`, and excludes the
device families this flow does not use:

```
rf_(n|p)fet | fet_g5v0 | fet_03v3 | fet_20v0 | fet_05v0 | esd_nfet | _(h)vt
```

The output is pasted into the `corner:` section of
[cicsim/cicsim.yaml](../cicsim/cicsim.yaml.md), and
[ngspice/corners.py](../ngspice/corners.py.md) then expands that into
`corners.spi`.
