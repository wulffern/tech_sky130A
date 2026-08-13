# cicsim.yaml

The shared cicsim configuration: simulator, one variable, and 41 corners. An
IP symlinks it into `sim/`:

```bash
cd sim && ln -s ../tech/cicsim/cicsim.yaml
```

## simulator

`ngspice`.

## variable

`CPDK_NGPICE: ../../../`.

Note that cicsim 0.2.7 does not read this key. The only top-level keys it
looks at are `ngspice`, `spectre`, `cadence`, `corner` and `options`, so
whatever consumes `variable` is either older, newer, or somewhere else
entirely. Do not assume changing it does anything.

## corner

Each key is a corner name, each value is the spice text cicsim writes into the
netlist when that corner is selected. Pick one from each group.

| Group | Names | Defined in |
|:-|:-|:-|
| General | `Gt` | nothing, it is a placeholder |
| Temperature | `Tt` `Tl` `Tm` `Th` | [ngspice/temperature.spi](../ngspice/temperature.spi.md) |
| Supply | `Vt` `Vl` `Vh` | [ngspice/supply.spi](../ngspice/supply.spi.md) |
| Process | `Ktt` `Kss` `Kff` `Ksf` `Kfs` `Khh` `Khl` `Klh` `Kll` | the PDK model files, spelled out |
| Process, Monte Carlo | the same with an `mm` suffix, plus `Kmc` | the PDK, with the mc switches on |
| Process, short form | `Att` `Ass` `Aff` `Asf` `Afs` `Ahh` `Ahl` `Alh` `All` and `Amc...` | one `.lib` into the PDK's `sky130.lib.spice` |

## What the two letters mean

They are one sky130 corner name, not a device choice and an RC choice picked
independently. Two families:

| Corner | FET models | Resistance | Capacitance |
|:-|:-|:-|:-|
| `Ktt` | tt | typical | typical |
| `Kss` | ss | high | high |
| `Kff` | ff | low | low |
| `Ksf` | sf | typical | typical |
| `Kfs` | fs | typical | typical |
| `Khh` | tt | high | high |
| `Khl` | tt | high | low |
| `Klh` | tt | low | high |
| `Kll` | tt | low | low |

In the first family the letters are the device corner, nfet then pfet, and
the `r+c` set follows it: `Kss` pulls in `res_high__cap_high`, `Kff` pulls in
`res_low__cap_low`, and the skewed corners stay on typical RC. In the second
family the devices are typical and the letters are the parasitic corner
instead, resistance then capacitance. `Khh` is `Kss`'s parasitics without
`Kss`'s devices.

The `mm` variants set `mc_mm_switch=1` on the same includes, for mismatch.
`Kmc` is not a corner in that sense at all: it includes only
`parameters/critical.spice` and `parameters/montecarlo.spice` with
`mc_pr_switch=1`.

The `A...` names are the identical corners as a single
`.lib "$PDK_ROOT/.../sky130.lib.spice" <xy>` line, and `Amc...` maps to the
PDK's `<xy>_mm` sections. `K...` exists because
[py/genyaml](../py/genyaml.md) expanded those sections into explicit
includes, which is what makes each corner's real content visible here.

The temperature and supply corners are one-line `.lib` references, so the
actual values live in one place and are edited there.

## Keeping it in sync

The process corners are generated, not written: [py/genyaml](../py/genyaml.md)
walks the PDK's `sky130.lib.spice` and prints these blocks, and
[ngspice/corners.py](../ngspice/corners.py.md) expands this file into
`ngspice/corners.spi` for the case where a netlist is run without cicsim.
Regenerate both after a PDK update.
