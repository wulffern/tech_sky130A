# Verification

DRC, LVS, antenna, and the tools that repair what they find. All from `work/`.

Every check follows the same shape: a template from
[magic/](../magic/README.md) has `{PATH}` and `{CELL}` substituted into it, the
result is written into the check's own directory, magic runs it headless
(`-noconsole -dnull`), and a script in [script/](../script/README.md) turns the
log into one line. Both the generated tcl and the full log stay on disk, so any
failure can be reproduced by hand.

## DRC

```bash
make drc        # magic, drc(full)
make kdrc       # KLayout, the sign-off deck
make drcall     # magic over every cell in ${CELLS}
```

`make drc` uses [magic/drc.tcl](../magic/drc.tcl.md). The box is expanded twice
so child cells are checked too, not just the top outline, and `drc style
drc(full)` selects the complete deck rather than the fast subset the PDK
defaults to. Output:

```
MY_CELL                                  [ DRC OK   ]
```

On failure the last ten lines of `drc/<CELL>_drc.log` are printed; the whole
list of violations with coordinates is in that file.

`make kdrc` runs the PDK's `sky130A_mr.drc` with feol, beol and offgrid
enabled, and [script/checkkdrc](../script/checkkdrc.md) summarises the XML by
rule:

```
MY_CELL                                  [ KDRC FAIL ]
    psdm.1 .................... 16
    li.3 ......................  4
    total                        20
```

It never fails the build, because it is a second opinion. Magic and KLayout
disagree at the margins; KLayout is closer to what the foundry runs, so treat a
KLayout-only violation as real and a magic-only violation as worth
understanding.

## LVS

```bash
make lvs        # extract + netgen + verdict
make xlvsall    # every cell in ${CELLS}, one line each
```

The interesting decision is *how* the layout is extracted, and it is set per IP
in `work/Makefile`:

| `LVSTCL` | Extraction | When |
|:-|:-|:-|
| `lvs.tcl` (default) | [Hierarchical](../magic/lvs.tcl.md) | Leaf cells, and anything that passes |
| `lvsflat.tcl` | [Flat netlist, layout hierarchy kept](../magic/lvsflat.tcl.md) | Assemblies, tap-less cells, cross-cell connectivity |

Start hierarchical. Its errors name the cell that is wrong, which is worth a
lot. Switch to flat when you see the failure mode it cannot handle: hierarchical
extraction promotes every dangling net inside a cell to a subcircuit port, so
the dummy poly of a transistor pattern and the unrouted bulk straps of a
tap-less leaf cell all become pins, and netgen buries the real mismatch under
port errors. Worse, it cannot see a connection that only exists *between*
cells, so an assembly where a strap shorts two rails can be DRC clean and still
pass LVS.

```make
LVSTCL=lvsflat.tcl
```

The flat run passes `--noprop` to [script/checklvs](../script/checklvs.md),
because symmetric gates resolved by property look like property errors when
everything is flattened. That is why you keep running the hierarchical flow per
cell: it is what actually checks properties.

`make xflvs` is the bigger hammer again: it flattens the *layout*
([lvsf.tcl](../magic/lvsf.tcl.md)) rather than only the netlist. Everything
resolves, but a mismatch then points at a device instead of a block.

### Mixed signal

If the digital part of the block only exists as gate level verilog, netgen
needs to read it, or it invents an empty placeholder subcircuit and the top
cell fails pin matching on the resulting port symmetry. Set in `work/Makefile`:

```make
VERILOG_FILE=../rtl/foo.pnl.v
```

and `make lvs` switches to a netgen script that reads the verilog plus the
sky130 standard cell spice into the source netlist.

### Tolerances

`NETGENSETUP` defaults to the PDK's `sky130A_setup.tcl`. Override it to layer
project specific tolerances on top, rather than editing the PDK.

## Antenna

```bash
make ant        # hierarchical
make antf       # flattened
```

[script/checkant](../script/checkant.md) writes `ant/<CELL>_ant.csv` beside the
log with a row per violation: the ratio, the limit, and the gate and antenna
rectangles. Sort by ratio to find what to fix first; the gate size columns tell
you whether a protection diode is worth adding or whether the gate is simply
too small for the metal hanging off it.

Use `antf` for anything above leaf level. A hierarchical check only sees the
metal inside one cell, so a long route assembled at the top looks harmless in
every child.

## Repairing what you find

| Symptom | Tool |
|:-|:-|
| Cell overhangs its parent, arrays step wrong | `make fixbbox` → [fixbbox](../script/fixbbox.md) |
| Extracted pin order differs from the schematic | `make matchports` → [matchports.py](../py/matchports.py.md) |
| Magic loads the wrong child cell after a move | `make fixmag` → [fixmag.py](../py/fixmag.py.md) |

`fixbbox` and `matchports` are dry runs by default:

```bash
make fixbbox                 # report
make fixbbox BBOPT=--apply   # write
make matchports MPOPT=--apply
```

`fixmag` writes immediately, so commit first.

All three change files under `design/`, not `work/`. Re-extract afterwards.

## Freezing a block

When a cell is signed off and you want to be sure a stray session does not
edit it:

```bash
make readonly     # chmod a-w on the library's .mag and .sch
make writable     # undo
```
