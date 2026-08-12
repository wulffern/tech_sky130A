# cicconf

Project templates for [cicconf](https://github.com/wulffern/cicconf), the tool
that clones an IP's dependencies and scaffolds a new IP repository.

```bash
cicconf --config config.yaml clone --https      # fetch dependencies
cicconf template ../tech/cicconf/jnw.yaml       # make a new IP
```

A template is one yaml file describing a whole repository: the directories to
create, the files to write with `${IP}` and `${CELL}` substituted, and the
commands to run afterwards. All four here build the same shape of repository
and differ only in the details.

| Template | Standard cells | Extras |
|:-|:-|:-|
| [ip_template.yaml](ip_template.yaml.md) | `jnw_tr`, `jnw_atr` | an `rtl/` directory for mixed signal work |
| [jnw.yaml](jnw.yaml.md) | `jnw_tr`, `jnw_atr` | a SIM workflow, so simulations run in CI |
| [lelo.yaml](lelo.yaml.md) | `jnw_tr`, `jnw_atr` | a root `Makefile` for the documentation targets |
| [rey.yaml](rey.yaml.md) | `rey_tr`, `rey_atr` | a root `Makefile`, and a wider `.gitignore` |

Every one of them pins `tech_sky130A` as a dependency and symlinks it in as
`tech`, which is how an IP ends up with the layout all the make targets and tcl
templates in this repository are written against:

```
my_ip/
├── tech -> ../tech_sky130A
├── design/MY_IP_SKY130A/
├── work/          make drc, lvs, gds, ...
├── sim/           cicsim testbenches
└── .github/workflows/
```
