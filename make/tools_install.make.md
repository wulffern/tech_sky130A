# tools_install.make

Builds the whole open source toolchain from source. Written for Ubuntu 20.04
LTS, and used when there is no aicex container to hand.

```bash
make -f tools_install.make          # everything
make -f tools_install.make cmagic   # just magic
```

`all` is `apt tcl tk cmagic cxschem cnetgen cngspice copen_pdks end`.

Each tool has two targets: a bare one that clones or downloads the source
(`magic`, `xschem`, `netgen`, `ngspice`, `open_pdks`, `tcl8.6.10`, `tk8.6.10`)
and a `c`-prefixed one that configures, builds and installs it.

| Target | Installs |
|:-|:-|
| `apt` | Build dependencies: flex, bison, tk8.6, cairo, X11 and readline headers |
| `tcl` / `tk` | Tcl/Tk 8.6.10 into `/usr/local/opt2/tcl-tk` |
| `cmagic` | [magic](https://github.com/RTimothyEdwards/magic) |
| `cxschem` | [xschem](https://github.com/StefanSchippers/xschem) |
| `cnetgen` | [netgen](https://github.com/RTimothyEdwards/netgen) |
| `cngspice` | ngspice with xspice, pss, openmp and cider enabled |
| `copen_pdks` | sky130 only; gf180mcu, klayout, irsim, openlane and qflow are all disabled |

`INSTALL_PATH` is `/usr/local/eda` and `end` reminds you to add it to your
shell:

```bash
export PDK_ROOT=/usr/local/eda/share/pdk
export PATH=/usr/local/eda/bin:$PATH
```

Two workarounds worth knowing. Magic and netgen are patched with `perl -pe` to
add `-Wno-error=implicit-function-declaration`, because newer compilers reject
what their configure scripts emit. Xschem's `Makefile.conf` has its `CFLAGS`
and `LDFLAGS` commented out and replaced with explicit include and library
paths, since the generated ones do not find the Tcl/Tk built above.

Note the X11 paths (`/opt/X11`) are the macOS XQuartz ones, so on a plain
Ubuntu box those `--x-includes`/`--x-libraries` arguments need changing.
