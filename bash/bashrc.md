# bashrc

The two environment variables every tool in this repository assumes.

```bash
export PDK_ROOT=/opt/pdk/share/pdk
export PDK=sky130A
```

`PDK_ROOT` is the open_pdks install prefix, the directory that holds the
`sky130A/` tree with `libs.tech` and `libs.ref`. `PDK` names the process
variant inside it.

Source it from your own `~/.bashrc`, or copy the two lines:

```bash
source ~/path/to/tech_sky130A/bash/bashrc
```

The paths match the aicex container, where the PDK is installed under
`/opt/pdk`. On a hand built toolchain the prefix is whatever was passed to
`open_pdks` as `--prefix` (see [tools_install.make](../make/tools_install.make.md),
which suggests `/usr/local/eda`), so change `PDK_ROOT` to match.

Everything downstream depends on these:

- `magic/.magicrc` sources `$PDK_ROOT/sky130A/libs.tech/magic/sky130A.magicrc`
- `xschem/xschemrc` sources `$PDK_ROOT/sky130A/libs.tech/xschem/xschemrc` and
  uses `$PDK` to find the start window
- `make/core.make` builds `PDKPATH=${PDK_ROOT}/sky130A` for the netgen setup
  and the KLayout DRC deck
