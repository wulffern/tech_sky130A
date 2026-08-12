# template.yaml

What `cicsim simcell` reads to create a new simulation directory.

```bash
make cell LIB=<LIB> CELL=<CELL>     # from sim/
```

## create

Writes a local `cicsim.yaml` that adds two view corners on top of the shared
[cicsim/cicsim.yaml](../cicsim.yaml.md):

```yaml
options:
  useTmpDir: False
  sha: True
corner:
  Lay: ''
  Sch: ''
ngspice:
  library: ${IP}
  cell: ${CELL}
```

`Sch` and `Lay` are empty corners: they add nothing to the netlist, and exist
so the view can be named on the command line and end up in the result
directory name. [tran.spi](tran.spi.md) then switches on `Lay` with `#ifdef` to
include the extracted netlist instead of the schematic one.

`sha: True` records the netlist hash with the results, so a stale result is
recognisable. `useTmpDir: False` keeps the run in place, which makes debugging
a failed simulation much easier.

## copy

`tran.spi`, `tran.py`, `tran.meas`, `tran.yaml`, `Makefile`, `summary.yaml`.

## do

Runs `make netlist`, then `git add`s the seven files, so a new testbench is
staged and nothing is forgotten.
