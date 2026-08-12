# Tapeout

Delivering a block means two things: the files themselves, and enough
information to rebuild them a year later. Both come out of `make deliver`.

## Prerequisites

A `../tapeout` directory, normally a submodule of the tapeout repository. If it
is not there, `make preflight` stops immediately, which is deliberate: finding
out after the multi-minute DRC and LVS runs is a waste of an afternoon.

## Pin the dependencies first

```bash
make preflight
make preflight DEPS_OPT=--fail-on-dirty
```

[py/deps2tapeout.py](../py/deps2tapeout.py.md) walks the `tech` symlink and
every symlink under `design/`, resolves each to its git repository, and writes
`../tapeout/ip/config.yaml` as a cicconf-style *lock file*: same `name:
{remote, revision}` shape, but `revision` is the exact commit SHA rather than
the branch cicconf tracks.

That distinction is the whole point. `main` will have moved by the time anyone
asks what was taped out; a SHA will not. `cicconf clone` on that lock
reconstructs the exact environment that produced the GDS.

Repositories with uncommitted changes are listed as a warning, because a
pinned SHA does not capture a dirty tree. Dirty trees are normal while
iterating, which is why it is only a warning by default. For a delivery you
actually intend to be reproducible, use `--fail-on-dirty` and commit
everything first.

## Deliver

```bash
make deliver
```

runs `preflight cdl gds lvs drc ant`, then `lpe`, then copies into
`../tapeout/`:

| Destination | What |
|:-|:-|
| `gds/<CELL>.gds` | The layout, plus a `<date>_<CELL>.gds` copy |
| `lef/<CELL>.lef` | Pins and outline only, via [deliver.tcl](../magic/deliver.tcl.md) |
| `spi/` | The schematic netlist and the extracted one |
| `reports/` | The DRC, LVS and antenna logs |
| `docs/info.md`, `docs/info.html` | The documentation |
| `ip/config.yaml` | The dependency lock |

Note the order: the checks run *before* anything is copied, so a failing block
cannot be delivered by accident.

The LEF is written `-pinonly`: it says where a top level router may connect,
without also describing the whole cell.

## The documentation

[py/readme2tapeout.py](../py/readme2tapeout.py.md) converts the IP `README.md`
into a Tiny Tapeout `docs/info.md`. The `docs` folder is flat, so every locally
resolvable image is copied next to `info.md` with its path flattened and the
markdown reference rewritten. CI badges are stripped and replaced with links to
the repository and its documentation site, derived from the git remote. PNGs
over the Tiny Tapeout limits are re-encoded and scaled down until they fit.

Then pandoc renders a self contained `info.html`.

So: whatever is in the IP README is what gets submitted. Run `make summary` in
the simulation directories first, so the measured results are in it.

## Precheck

```bash
make precheck
```

[make/tt_precheck.sh](../make/tt_precheck.sh.md) runs the same checks the
`TinyTapeout/tt-gds-action/precheck` action runs in CI: magic DRC, KLayout DRC,
forbidden layers, pin labels, the pin and boundary checks, power and analog pin
checks, and verilog syntax.

It needs a `tt-support-tools` checkout, and tells you what to clone if it is
missing:

```bash
git clone https://github.com/TinyTapeout/tt-support-tools ~/github/tt-support-tools
```

The venv is created on first run. Everything else is auto-detected, including
klayout inside a macOS app bundle. Override with `TT_TOOLS`, `PDK_ROOT`,
`EDA_BIN`, `KLAYOUT`, `PYTHON` or `TT_TECH`.

## A sensible order

```bash
cd work
make readonly            # freeze the design
make deliver             # checks, then copy
make precheck            # what CI will run
cd ../../tapeout && git add . && git commit
```

Then commit the IP too, so the SHA in the lock file exists on a remote.
