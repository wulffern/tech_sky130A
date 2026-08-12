# tran.spi

The testbench netlist template. A transient run of the DUT with a ramped
supply, and the starting point for anything more interesting.

## Includes

```spice
#ifdef Lay
.include ../../../work/lpe/${CELL}_lpe.spi
#else
.include ../../../work/xsch/${CELL}.spice
#endif
```

The `Lay` corner from [template.yaml](template.yaml.md) is what flips this, so
`make typical VIEW=Lay` simulates the extracted netlist with no edit to the
testbench.

The DUT itself comes from `.include ../xdut.spi`, regenerated on every netlist
by [script/genxdut](../../script/genxdut.md) so the port order is always
right.

## Stimulus

```spice
.param AVDD = {vdda}
VSS  VSS  0     dc 0
VDD  VDD_1V8  VSS  pwl 0 0 10n {AVDD}
```

`vdda` comes from the supply corner, see
[ngspice/supply.spi](../../ngspice/supply.spi.md), so `Vl`, `Vt` and `Vh`
change the supply without touching this file. The supply ramps over 10 ns
rather than stepping, which avoids an impossible initial transient.

`.option TNOM=27 GMIN=1e-15 reltol=1e-3` and `.param TRF = 10p` set the
tolerances and a default edge rate.

## Control

`.save all` probes everything, which is right for a template and worth
narrowing once a testbench is real. The `.control` block runs `optran` to find
an operating point, then `tran 1n 10n 1p`, writes the raw file and quits.
`num_threads=8`; `color0`/`color1` are set so an interactive plot is readable.
