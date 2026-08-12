# cicsim.yaml

The shared cicsim configuration: simulator, one variable, and 41 corners. An
IP symlinks it into `sim/`:

```bash
cd sim && ln -s ../tech/cicsim/cicsim.yaml
```

## simulator

`ngspice`.

## variable

`CPDK_NGPICE: ../../../`, the path a testbench uses to reach the cpdk spice
models from inside `sim/<CELL>/`.

## corner

Each key is a corner name, each value is the spice text cicsim writes into the
netlist when that corner is selected. Pick one from each group.

| Group | Names | Defined in |
|:-|:-|:-|
| General | `Gt` | nothing, it is a placeholder |
| Temperature | `Tt` `Tl` `Tm` `Th` | [ngspice/temperature.spi](../ngspice/temperature.spi.md) |
| Supply | `Vt` `Vl` `Vh` | [ngspice/supply.spi](../ngspice/supply.spi.md) |
| Process | `Ktt` `Kss` `Kff` `Ksf` `Kfs` `Khh` `Khl` `Klh` `Kll` | the PDK model files |
| Process, Monte Carlo | the same with an `mm` suffix, plus `Kmc` | the PDK, with the mc switches on |
| Analog model set | `Att` `Ass` `Aff` `Asf` `Afs` `All` `Ahh` `Ahl` `Alh` and `Amc...` | the PDK |

The two letters in a process corner name are the device corner and the
parasitic corner: `Kss` is slow devices with the typical RC set, `Khl` is high
resistance with low capacitance, and so on. The `mm` variants set
`mc_mm_switch=1` for mismatch, `Kmc` sets `mc_pr_switch=1` for process
variation.

The temperature and supply corners are one-line `.lib` references, so the
actual values live in one place and are edited there.

## Keeping it in sync

The process corners are generated, not written: [py/genyaml](../py/genyaml.md)
walks the PDK's `sky130.lib.spice` and prints these blocks, and
[ngspice/corners.py](../ngspice/corners.py.md) expands this file into
`ngspice/corners.spi` for the case where a netlist is run without cicsim.
Regenerate both after a PDK update.
