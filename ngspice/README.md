# ngspice

Corner definitions for ngspice.

A simulation is run as a set of orthogonal corners: process (`K...`),
temperature (`T...`), supply (`V...`) and a general corner (`Gt`).
[cicsim](https://github.com/wulffern/cicsim) is told which combinations to run,
for example

```bash
cicsim run --name Sch_etc tran Sch Gt "Kss,Kff,Ksf,Kfs" "Th,Tl" "Vl,Vh"
```

and each name resolves to a `.lib` in one of the files here.

`temperature.spi` and `supply.spi` are written by hand. `corners.spi` is
generated from the corner dictionary in
[cicsim/cicsim.yaml](../cicsim/cicsim.yaml.md) by `make corners`, so the
process corners never drift between the two.
