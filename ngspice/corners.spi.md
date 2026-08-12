# corners.spi

Generated file. Do not edit: run `make corners` in this folder, which runs
[corners.py](corners.py.md) over the `corner:` section of
[cicsim/cicsim.yaml](../cicsim/cicsim.yaml.md).

It holds one `.lib` per corner name, 41 of them. Three kinds:

- **Wrappers.** `Tt`, `Tl`, `Tm`, `Th`, `Vt`, `Vl`, `Vh` and `Gt` just pull in
  the matching block of [temperature.spi](temperature.spi.md) or
  [supply.spi](supply.spi.md).
- **Process corners.** `Ktt`, `Kss`, `Kff`, `Ksf`, `Kfs`, `Khh`, `Khl`, `Klh`,
  `Kll` include the sky130 model files for that combination of device and
  parasitic corner, with `mc_mm_switch` and `mc_pr_switch` both 0.
- **Monte Carlo variants.** The same names with an `mm` suffix (`Kttmm`,
  `Kssmm`, ...) set `mc_mm_switch=1` for mismatch, and `Kmc` sets
  `mc_pr_switch=1` for process variation.

The `A...` names (`Att`, `Ass`, `Amctt`, ...) are the same idea for the analog
model set.

Paths into the PDK are written with `$PDK_ROOT` rather than the absolute
`/opt/pdk/share/pdk` they were parsed from, which is the `--replace` option of
[py/genyaml](../py/genyaml.md).
