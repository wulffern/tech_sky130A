# ip_template.yaml

The generic IP template, and the one to copy when starting a new flow.

```bash
cicconf template ../tech/cicconf/ip_template.yaml
```

## dirs

`design/`, `design/${IP}/`, `.github/workflows/`, `media/`, `sim/`, `work/`
and `rtl/`. The `rtl/` directory is what distinguishes this template from the
others: it is where the gate level verilog of a mixed signal block lives, the
`VERILOG_FILE` that [core.make](../make/core.make.md) reads into the LVS source
netlist.

## create

| File | Contents |
|:-|:-|
| `info.yaml` | Library, cell, author, github user, tagline, and the `doc:` and `sim:` sections the documentation action reads |
| `config.yaml` | The cicconf dependency list: `cpdk`, `tech_sky130A`, `jnw_tr_sky130a`, `jnw_atr_sky130a` |
| `.github/workflows/{lvs,drc,gds,docs}.yaml` | Thin callers of the reusable workflows in `analogicus/jnw-actions` |
| `.gitignore` | Tool output: `*.ext`, `*.gds`, `output_*/`, `work/lvs`, `work/gds`, ... |
| `design/${IP}/${CELL}.md` | The cell's documentation stub |
| `design/${IP}/${CELL}.sch` | An empty schematic with a border and `VDD_1V8`, `VSS`, `PWRUP_1V8` pins |
| `work/Makefile` | `include ../tech/make/core.make`, plus the commented list of useful targets |
| `work/.magicrc`, `work/xschemrc` | Two liners that source [magic/.magicrc](../magic/.magicrc.md) and [xschem/xschemrc](../xschem/xschemrc.md), with `addpath` lines for the standard cell libraries |
| `sim/Makefile` | Loops the cicsim targets over the simulation directories |
| `README.md` | Title, tagline, workflow badges, and a cell table |

## do

The symlinks are the important part, since every relative path in this
repository assumes them:

```bash
ln -s ../tech_sky130A tech
cd work && ln -s ../tech/magic/mos.24bit.dstyle
cd work && ln -s ../tech/magic/mos.24bit.std.cmap
cd sim  && ln -s ../tech/cicsim/cicsim.yaml
cd design && ln -s ../../jnw_tr_sky130a/design/JNW_TR_SKY130A
cd design && ln -s ../../jnw_atr_sky130a/design/JNW_ATR_SKY130A
```

Then `git init`, and a first commit. Note the `git add -f` lines: `work/` is
in the `.gitignore`, so the rc files, the Makefile and the two colour files
have to be forced in.
