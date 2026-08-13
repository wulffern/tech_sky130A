# corners.spi

Generated file. Do not edit: run `make corners` in this folder, which runs
[corners.py](corners.py.md) over the `corner:` section of
[cicsim/cicsim.yaml](../cicsim/cicsim.yaml.md).

It holds one `.lib` per corner name, 41 of them. Three kinds:

- **Wrappers.** `Tt`, `Tl`, `Tm`, `Th`, `Vt`, `Vl`, `Vh` and `Gt` just pull in
  the matching block of [temperature.spi](temperature.spi.md) or
  [supply.spi](supply.spi.md).
- **Process corners.** `Ktt`, `Kss`, `Kff`, `Ksf`, `Kfs`, `Khh`, `Khl`, `Klh`,
  `Kll` include the sky130 nfet, pfet, non-FET and `r+c` model files for one
  named PDK corner, with `mc_mm_switch` and `mc_pr_switch` both 0. The two
  letters are that corner's name: for `ss`/`ff`/`sf`/`fs` they are the device
  corner and the parasitics follow it, for `hh`/`hl`/`lh`/`ll` the devices are
  typical and the letters are resistance and capacitance. See
  [cicsim.yaml](../cicsim/cicsim.yaml.md) for the full table.
- **Monte Carlo variants.** The same names with an `mm` suffix (`Kttmm`,
  `Kssmm`, ...) set `mc_mm_switch=1` for mismatch, and `Kmc` sets
  `mc_pr_switch=1` for process variation.

The `A...` names (`Att`, `Ass`, `Amctt`, ...) are the same corners as a single
`.lib` line into the PDK's `sky130.lib.spice`, rather than the expanded
include list.

Paths into the PDK are written with `$PDK_ROOT` rather than the absolute
`/opt/pdk/share/pdk` they were parsed from, which is the `--replace` option of
[py/genyaml](../py/genyaml.md).
