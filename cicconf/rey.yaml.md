# rey.yaml

The template for the REY flow. Like [lelo.yaml](lelo.yaml.md), with its own
standard cell libraries.

- **`rey_tr_sky130a` and `rey_atr_sky130a`** replace the `jnw_` libraries, both
  in `config.yaml` and in the `design/` symlinks.
- **A wider `.gitignore`**: on top of the usual tool output it also ignores
  `*.logm`, `*.sha`, `*.raw`, `*.out`, `*.vcd`, `simulation/`, `results/`,
  `docs/`, `*.html`, `/cdl/`, the `*_svg/` directories and `*_obj_dir/`. That
  last one is verilator's build directory.
- **A root `Makefile`** including [main.make](../make/main.make.md), same as
  the LELO template.

Note that this template ignores `docs/`, so a REY IP keeps its generated
documentation out of git and rebuilds it in CI.

## TinyTapeout top level

Every REY IP is a Tiny Tapeout 1x1 tile. After the `design/` symlinks the
template runs [rey_tt.sh](rey_tt.sh), which copies the files in `rey_tt/` into
`design/${IP}/`, replacing `@IP@`, `@CELL@` and `@cell@` in names and contents:

| File | What |
|:-|:-|
| `tt_um_<cell>_analogicus.mag/.sch` | The top level. `uio_oe[7:0]` tied low through `res_generic_m4` from a `REYTR_TIEL_CV`, `ui_in[0]` → `PWRUP_1V8` with an antenna diode, `OSC_TEMP_1V8` → `uo_out[0]` |
| `<CELL>.mag/.sch/.sym` | The default block: the two signals looped through two dummy metal resistors, so LVS has something to compare |
| `sky130_fd_pr__diode_pw2nd_05v5_lc.mag` | The 0.45 × 0.45 µm antenna diode |

`work/Makefile` defaults `CELL` to the top level, and `CELLS` lists both.

The top level came from `lelo_gr02_sky130a`, with these fixes:

- Its 43 signal ports match `tt/tt_block_1x1_pg.def` in name, rectangle and
  direction. The original LELO template had them mirrored in X. Run
  `make ttpins` ([checkttpins](../script/checkttpins.md)) after editing.
- The dummy `rmetal4` in the default block sits at y 18200–18280, below where
  the top level met4 drops end (block y ≈ 18496). Under the drops it gave
  "Can't overlap those layers" and shorted `ui_in[0]` to `uo_out[0]`.
- The diode sets `pj=1.8e6`. The `diode.sym` format reads `@pj`, so the
  `perim=` used in LELO was ignored and LVS failed on the property.

Generated IPs are DRC and LVS clean for both the block and the top level.
`makegroups.py` in the workspace root uses this template to make student groups.
