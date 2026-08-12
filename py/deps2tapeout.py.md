# deps2tapeout.py

Pins the exact dependency versions that went into a tapeout delivery.

```bash
make preflight                                  # from work/
make preflight DEPS_OPT=--fail-on-dirty

python3 ../tech/py/deps2tapeout.py --ip-root .. --out ../tapeout/ip/config.yaml
```

## Why

An IP references its dependencies as symlinks:

```
tech          -> ../tech_sky130A
design/<DEP>  -> ../../<repo>/design/<DEP>
```

Each target is its own git repository, tracked by cicconf at a *branch*. That
is fine while working, and useless for a delivery: the branch will have moved
by the time anyone asks what was actually taped out.

## What it writes

A cicconf style `config.yaml`, but as a lock file: `name: {remote, revision}`
with `#-` description comments, where `revision` is the exact commit SHA
instead of a branch name. `cicconf clone` on that file reconstructs the
environment that produced the GDS.

The descriptions are inherited from the surrounding cicconf configs so the lock
reads like the original: the monorepo `config.yaml` first, then the IP's own,
which wins on a conflict. The `options` block (template, project, technology) is
deliberately left out, because this is a lock file and not a project config.

Repositories are discovered by walking the `tech` symlink and every symlink
under `design/`, in that order, plus anything given with `--extra`.

| Option | Default | Meaning |
|:-|:-|:-|
| `--ip-root` | `..` | The IP directory holding `tech` and `design/` |
| `--out` | `../tapeout/ip/config.yaml` | Destination |
| `--source-config` | `<ip-root>/../config.yaml` | Where to inherit descriptions from |
| `--include-self` / `--no-include-self` | include | Also pin the IP repository itself |
| `--extra` | `../cpdk` | Repos not reachable through a symlink; repeatable |
| `--fail-on-dirty` | off | Abort instead of warning when a dependency has uncommitted changes |

Dirty trees are common while iterating, so by default the modified files are
listed as a warning; a pinned SHA does not capture them. Turn `--fail-on-dirty`
on for a delivery that has to be strictly reproducible.

One detail worth keeping: `git status --porcelain` output is read raw rather
than stripped, because stripping would eat the leading status column of the
first line. `--untracked-files=no` means new files do not count as dirty.
