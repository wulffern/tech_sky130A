# make

The make system. An IP repository has a one line `Makefile` in its `work/`
directory:

```make
LIB=MY_IP_SKY130A
CELL=MY_CELL
include ../tech/make/core.make
```

and from then on every verification step is a make target run from `work/`.

| File | Included from | What it gives you |
|:-|:-|:-|
| [core.make](core.make.md) | `work/Makefile` | `gds`, `xsch`, `cdl`, `drc`, `kdrc`, `lvs`, `lpe`, `ant`, `deliver`, ... |
| [sim.make](sim.make.md) | a simulation directory's `Makefile` | `netlist`, `cell`, `ver` |
| [main.make](main.make.md) | the IP root `Makefile` | `docs` |
| [tools_install.make](tools_install.make.md) | nothing, run directly | builds magic, xschem, netgen, ngspice and the PDK from source |
| [tt_precheck.sh](tt_precheck.sh.md) | `make precheck` | runs the Tiny Tapeout precheck locally |

`make help` prints the built-in summary from `core.make`, and `-n` shows what a
target would run without running it:

```bash
make xsch LIB=RPLY_EX0_SKY130NM CELL=RPLY_EX0 -n
```
