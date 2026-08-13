# cicconf

Project templates for [cicconf](https://github.com/wulffern/cicconf), the tool
that clones an IP's dependencies and scaffolds a new IP repository.

```bash
cicconf --config config.yaml clone --https      # fetch dependencies
cicconf newip bias                              # make a new IP
```

`newip` does not take the template path. It reads it from the `options` block
of the *monorepo* `config.yaml` you run it in:

```yaml
options:
  project: JNW
  technology: SKY130A
  template:
    ip: ../tech_sky130A/cicconf/jnw.yaml
```

so `cicconf newip bias` creates `JNW_BIAS_SKY130A` in a directory named
`jnw_bias_sky130a`. `--project`, `--technology` and `--ip` override the three
values for one invocation, which is how you use a template that is not the
project default:

```bash
cicconf newip bias --ip ../tech_sky130A/cicconf/lelo.yaml
```

A template is one yaml file describing a whole repository. cicconf substitutes
into it before parsing it as yaml, then runs the keys it recognises in order:

| Key | What it does |
|:-|:-|
| `dirs` | Directories to create |
| `create` | `filename: contents` pairs to write |
| `do` | Shell commands to run in the new directory |
| `echo` | A message to print at the end |
| `copy` | Files to copy from a source IP; only does anything with `--src`, which `newip` does not pass |

The substitutions are `${IP}`, `${CELL}` and their lowercase forms `${ip}` and
`${cell}`, followed by environment variables. `${CELL}` is not something you
choose: it is the IP name with its last underscore-separated segment removed,
so `JNW_BIAS_SKY130A` gives `JNW_BIAS`.

All four templates here build the same shape of repository and differ only in
the details.

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
