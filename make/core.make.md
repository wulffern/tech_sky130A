# core.make

The verification flow. Included from an IP's `work/Makefile`, which sets `LIB`
and `CELL`; every target below is then run from `work/`.

## Variables

| Variable | Default | Meaning |
|:-|:-|:-|
| `LIB` | — | Library name, the directory under `../design/` |
| `CELL` | — | Cell name |
| `PREFIX` | empty | Prepended to `CELL` to give `PRCELL`, the name actually used |
| `PDKPATH` | `${PDK_ROOT}/sky130A` | Where the netgen setup and KLayout deck are found |
| `LVSTCL` | `lvs.tcl` | Extraction recipe, set to `lvsflat.tcl` for a flat comparison |
| `NETGENSETUP` | the PDK setup | Override to layer project specific tolerances on top |
| `VERILOG_FILE` | unset | Gate level verilog to read into the LVS source netlist |
| `CELLS` | unset | Cell list for the `...all` targets |
| `OPT` | empty | Passed to `checklvs`, e.g. `--short` |
| `CICEXCLUDE` | `""` | Cells for cicpy to skip |

`ECHO` is picked per platform, because Ubuntu's `echo` does not want `-e`.

## Netlists

| Target | Result |
|:-|:-|
| `xsch` | `xsch/<CELL>.spice` from the schematic, post-processed by [fixsubckt](../script/fixsubckt.md) |
| `cdl` | `cdl/<CELL>.spice`, the LVS netlist, bus characters forced back to `[]` |
| `ver` | `<CELL>.v`, an empty verilog module with the right ports, via [genver](../script/genver.md) |
| `spi` | Netlist rewritten into `../cic/<CELL>.spi` with instances sorted by [fixspi](../script/fixspi.md) |
| `gds` | `gds/<CELL>.gds` written by magic |
| `lplot` | `lplot/<CELL>.svg` via [render_gds.py](../magic/render_gds.py.md) |

## Layout generation

`ip` runs ciccreator and cicpy over `../cic/ip.json` to generate
`../design/<LIB>`, optionally bracketed by `../cic/ip.py` and `../cic/post.py`.
`view` opens the same description in `cic-gui`. If a `../../ciccreator`
checkout exists it is used in preference to the installed `cic`.

## Checks

| Target | Tool | Summary written by |
|:-|:-|:-|
| `drc` | magic, [drc.tcl](../magic/drc.tcl.md) | inline perl, `DRC OK` / `DRC FAIL` |
| `kdrc` | KLayout, the PDK's `sky130A_mr.drc` | [checkkdrc](../script/checkkdrc.md) |
| `lvs` (= `xlvs`) | magic + netgen | [checklvs](../script/checklvs.md) |
| `xflvs` | magic ([lvsf.tcl](../magic/lvsf.tcl.md)) + netgen | [checklvs](../script/checklvs.md) |
| `ant` / `antf` | magic `antennacheck` | [checkant](../script/checkant.md) |

Each of these substitutes `{PATH}` and `{CELL}` into the matching template from
[magic/](../magic/README.md), runs magic with `-noconsole -dnull`, and keeps
both the generated tcl and the log in the target's directory so a failure can
be re-run by hand.

`kdrc` runs the KLayout deck with `feol`, `beol` and `offgrid` enabled on 8
threads, and never fails the build (`|| true`) because it is a second opinion
alongside magic.

The `VERILOG_FILE` case is worth knowing: for a mixed signal design the digital
block only exists in gate level verilog, so netgen must read that verilog *and*
the sky130 standard cell spice into the source netlist. Otherwise it invents an
empty placeholder subcircuit and the top cell fails pin matching on the
resulting port symmetry. Setting `VERILOG_FILE` switches `xlvs` from the one
line netgen invocation to the `LVS_NETGEN_TCL` script that does this.

`lvsall`, `xlvsall`, `xflvsall`, `drcall` and `lpeall` loop the matching target
over `${CELLS}`.

## Extraction

`lpe`, `lpeh` and `lper` map onto [lpe.tcl](../magic/lpe.tcl.md),
[lpeh.tcl](../magic/lpeh.tcl.md) and [lper.tcl](../magic/lper.tcl.md). All
three depend on `xsch`, strip the `_flat` suffix magic leaves behind, repair the
port list with [fixlpe](../script/fixlpe.md), and then LVS the extracted
netlist against the CDL to prove the parasitics did not change the circuit. The
capacitors (and for `lper` the resistors) are filtered out before that
comparison.

## Repair helpers

| Target | Runs | Default |
|:-|:-|:-|
| `matchports` | [matchports.py](../py/matchports.py.md) | dry run, apply with `MPOPT=--apply` |
| `fixbbox` | [fixbbox](../script/fixbbox.md) | dry run, apply with `BBOPT=--apply` |
| `fixmag` | [fixmag.py](../py/fixmag.py.md) | writes |

`readonly` and `writable` chmod the library's `.mag`, `.sch` and `.sym` files,
which is the cheapest way to stop a session from editing a frozen block.

## Delivery

`preflight` is deliberately first and deliberately fast: it aborts if there is
no `../tapeout` directory, before the multi-minute checks run, and calls
[deps2tapeout.py](../py/deps2tapeout.py.md) to pin the exact dependency SHAs
into `../tapeout/ip/config.yaml`.

`deliver` then runs `cdl gds lvs drc ant`, tries `lpe`, and copies the results
into `../tapeout`: GDS (also under a dated name), LEF written by
[deliver.tcl](../magic/deliver.tcl.md), the schematic and extracted spice, the
DRC/LVS/antenna logs into `reports/`, and a Tiny Tapeout `docs/info.md`
converted from the IP README by
[readme2tapeout.py](../py/readme2tapeout.py.md) plus a self contained
`info.html`.

`precheck` runs [tt_precheck.sh](tt_precheck.sh.md) against that staged
delivery.

`clean` removes `lvs drc lpe cdl gds` and the extraction leftovers.
