# genyaml

Reads the PDK's spice library tree and writes cicsim corner definitions.

```bash
./genyaml parse $PDK_ROOT/sky130A/libs.tech/ngspice/sky130.lib.spice
./genyaml process spice.yaml --prefix K --exclude "rf_(n|p)fet|..."
```

Normally run through the [Makefile](Makefile.md) in this folder.

## parse

Walks `.lib` and `.include` recursively from the given file and dumps the tree
to `spice.yaml` as `!Spice` objects. Each node records its filename, how many
non-comment lines it has, how many of those are includes, and its children
grouped by the `.lib` section they appeared in. A file whose every line is an
include is marked `includeOnly`, which is how the walker knows to descend
rather than emit it.

## process

Prints one cicsim corner per `.lib` name found, with underscores stripped:

```yaml
  Kss: |
    .param mc_mm_switch=0
    .param mc_pr_switch=0
    .include "$PDK_ROOT/sky130A/libs.tech/ngspice/..."
```

The two Monte Carlo switches are set from the corner name: `mm` in the name
turns on mismatch, `mc` turns on process variation, anything else turns both
off.

| Option | Default | Meaning |
|:-|:-|:-|
| `--prefix` | `K` | Prepended to every corner name |
| `--exclude` | none | Regex; matching include files are dropped |
| `--replace` | `/opt/pdk/share/pdk\|PDK_ROOT` | `find\|var`, rewrites the absolute PDK path as `$PDK_ROOT` |

The `--replace` default is what keeps the generated corners portable: the paths
are parsed as absolute and written back with the environment variable.
