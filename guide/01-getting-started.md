# Getting started

This repository is not a PDK. It is the thin layer of customization that sits
between the sky130A PDK and a design: the corner definitions, the make targets,
the magic and xschem setup, and the scripts that hold the flow together.

You never work *in* this repository. You clone it beside an IP repository,
which symlinks it as `tech`, and everything here is reached through that
symlink.

## 1. Get the tools

Two ways.

**The container.** `wulffern/aicex` has magic, xschem, netgen, ngspice,
KLayout and the PDK already installed, at the paths everything here assumes
(`/opt/pdk/share/pdk`, `/opt/eda/bin`). This is what CI uses, so a local run
matches CI exactly.

**From source.** [make/tools_install.make](../make/tools_install.make.md)
builds the lot on Ubuntu 20.04:

```bash
make -f tech_sky130A/make/tools_install.make
```

Either way, set the two environment variables everything depends on, see
[bash/bashrc](../bash/bashrc.md):

```bash
export PDK_ROOT=/opt/pdk/share/pdk    # or /usr/local/eda/share/pdk
export PDK=sky130A
```

Check it worked:

```bash
ls $PDK_ROOT/$PDK/libs.tech/magic/sky130A.magicrc
```

If that file is not there, nothing below will run.

## 2. Get the python tools

```bash
python3 -m pip install cicconf cicsim cicpy
```

[cicconf](https://github.com/wulffern/cicconf) clones dependencies and creates
IP repositories, [cicsim](https://github.com/wulffern/cicsim) runs
simulations, and cicpy transpiles generated layout. `pandas` and `click` are
needed by some of the [scripts](../script/README.md), and `gdstk` by
[render_gds.py](../magic/render_gds.py.md).

## 3. Make an IP

Pick a template from [cicconf/](../cicconf/README.md) and run it in the
directory that will hold your repositories:

```bash
mkdir ~/work && cd ~/work
cicconf template ../tech/cicconf/jnw.yaml
```

That creates the repository, writes the CI workflows, makes the first commit,
and lays down the symlinks the flow depends on:

```
~/work/
├── tech_sky130A/           this repository
├── cpdk/                   borders and shared symbols
├── jnw_tr_sky130A/         standard cells
├── jnw_atr_sky130A/        analog transistor library
└── my_ip/
    ├── tech -> ../tech_sky130A
    ├── config.yaml         what to clone
    ├── info.yaml           who you are, what the docs say
    ├── design/MY_IP_SKY130A/
    │   ├── MY_CELL.sch
    │   └── JNW_TR_SKY130A -> ../../../jnw_tr_sky130A/design/JNW_TR_SKY130A
    ├── work/               where you run make
    ├── sim/                where you run cicsim
    └── media/
```

On an IP that already exists, clone its dependencies instead:

```bash
cd my_ip
cicconf --rundir ../ --config config.yaml clone --https
```

## 4. Check the flow works

Everything in [make/core.make](../make/core.make.md) is run from `work/`:

```bash
cd my_ip/work
make help          # the built-in summary
make xview         # open the schematic in xschem
make xsch          # netlist it
```

`make help` prints the target list. Adding `-n` to any target shows the
commands it would run without running them, which is the fastest way to
understand what a target actually does:

```bash
make xsch LIB=MY_IP_SKY130A CELL=MY_CELL -n
```

## Where to go next

- [The design flow](02-design-flow.md) — the loop from schematic to signed-off layout
- [Simulation](03-simulation.md) — corners, testbenches and specs
- [Verification](04-verification.md) — DRC, LVS, antenna, and the repair tools
- [Tapeout](05-tapeout.md) — pinning dependencies and delivering
- [When something breaks](06-troubleshooting.md) — the failures you will actually hit
