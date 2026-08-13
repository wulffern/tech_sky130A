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

`sha: True` is a caching switch, not a bookkeeping one. cicsim hashes every
input file it references, saves them as `<run>.sha`, and on the next run
compares. If nothing has changed it prints "No spice files have changed" and
**skips the simulation entirely**; the `.meas` file is hashed separately, so
an unchanged measurement file on top of a skipped simulation skips the
measurement run too. That is what makes a repeated `make typical` cheap, and
also why a run that "did nothing" is usually correct rather than broken. Pass
`--no-sha` to force it.

`useTmpDir: False` keeps the run directory where it is. With it on, cicsim
puts the run under `/tmp/cicsim/$USER/<lib>/<cell>/<rundir>`, symlinks it into
place, and rewrites `../` in every `.include` and `.lib` to an absolute path
so the relocated netlist still resolves. Off is the easier thing to debug,
since the files are simply there.

## copy

`tran.spi`, `tran.py`, `tran.meas`, `tran.yaml`, `Makefile`, `summary.yaml`.

## do

Runs `make netlist`, then `git add`s the seven files, so a new testbench is
staged and nothing is forgotten.
