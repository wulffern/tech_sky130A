# Simulation

Simulations are run by [cicsim](https://github.com/wulffern/cicsim) from the
IP's `sim/<CELL>/` directory. This repository supplies the corner definitions
every IP shares and the template a new testbench is scaffolded from.

## Corner names

A run picks one value from each of four groups. The names are terse, so:

| Group | Names | Means |
|:-|:-|:-|
| General | `Gt` | Nothing; a placeholder so the position is always filled |
| Process | `Ktt` `Kss` `Kff` `Ksf` `Kfs` `Khh` `Khl` `Klh` `Kll` | Two letters: device corner, then RC corner |
| Temperature | `Tt` 27 °C, `Tl` −40 °C, `Th` 125 °C, `Tm` 42.4 °C | [ngspice/temperature.spi](../ngspice/temperature.spi.md) |
| Supply | `Vt` 1.8 V, `Vl` 1.7 V, `Vh` 1.9 V | [ngspice/supply.spi](../ngspice/supply.spi.md) |

So `Kss` is slow devices with typical parasitics, `Ksf` is slow n and fast p,
`Khl` is high resistance with low capacitance. Add `mm` for mismatch
(`Kttmm`), and `Kmc` turns on process variation.

Two more, from the local `cicsim.yaml` the testbench template writes: `Sch`
and `Lay`. Both are empty corners. They add nothing to the netlist and exist so
the view ends up in the result directory name, and so
[tran.spi](../cicsim/cell_spice/tran.spi.md) can switch its include on `Lay`.

Run one directly:

```bash
cicsim run --name Sch_typical tran Sch Gt Ktt Tt Vt
```

Give a comma separated list in any position and cicsim runs the cross product:

```bash
cicsim run --name Sch_etc tran Sch Gt "Kss,Kff,Ksf,Kfs" "Th,Tl" "Vl,Vh"
```

That is 16 runs. You will not normally type this; the Makefile does.

## Make a testbench

From `sim/`:

```bash
make cell LIB=MY_IP_SKY130A CELL=MY_CELL
```

which runs `cicsim simcell` over
[cicsim/cell_spice/template.yaml](../cicsim/cell_spice/template.yaml.md) and
creates `sim/MY_CELL/` with seven files, already `git add`ed:

| File | Yours to edit |
|:-|:-|
| [tran.spi](../cicsim/cell_spice/tran.spi.md) | The testbench. Stimulus, probes, analysis |
| [tran.meas](../cicsim/cell_spice/tran.meas.md) | What to measure from the raw file |
| [tran.py](../cicsim/cell_spice/tran.py.md) | Optional python post-processing |
| [tran.yaml](../cicsim/cell_spice/tran.yaml.md) | Specification limits per measurement |
| [summary.yaml](../cicsim/cell_spice/summary.yaml.md) | Which result sets go in the table |
| [Makefile](../cicsim/cell_spice/Makefile.md) | `TB`, `VIEW`, and the corner targets |
| `cicsim.yaml` | Local options; usually left alone |

`tran` is just the testbench name. Copy the five `tran.*` files to `ac.*` and
set `TB=ac` for a second one.

## Run it

From `sim/<CELL>/`:

```bash
make            # typical, etc, mc, then summary
make typical    # one corner, quickest feedback
make tfs        # all 27 process/temperature/supply combinations
make mc         # 30 Monte Carlo runs
make temp       # temperature sweep only
```

Every target depends on `netlist`, so the netlist is regenerated first and
cannot go stale.

Post-layout is the same command with a different view:

```bash
make typical VIEW=Lay
```

which requires `make lpe` to have run in `work/` first.

## Get a table out

Measurements are printed between `MEAS_START` and `MEAS_END` in
[tran.meas](../cicsim/cell_spice/tran.meas.md):

```spice
meas tran vout_final FIND v(OUT) AT=9n
print vout_final
```

cicsim parses those into the result yaml. Give a measurement limits in
`tran.yaml` and it gets judged:

```yaml
vout_final:
  name: Output voltage at 9 ns
  min: 0.8
  max: 1.0
  unit: V
  digits: 3
```

Then:

```bash
make summary    # writes README.md with the table
```

`summary.yaml` decides the columns: the typical run, worst case over the `etc`
set, and mean ± 3σ over the Monte Carlo set. Add a `Lay_typ` entry pointing at
`results/tran_Lay_typical` to get the post-layout column beside the schematic
one.

The README that comes out is what the documentation action publishes, so a
simulation that is worth keeping should end with `make summary`.

## Where a derived number belongs

If a figure of merit needs more than ngspice can do, an ENOB from a measured
SNR or a yield from a Monte Carlo set, compute it in
[tran.py](../cicsim/cell_spice/tran.py.md). Delete the early `return`, read the
result yaml, add your key, write it back. It then behaves like any other
measurement, including its specification limits.

## Keeping corners in sync after a PDK update

The process corners are generated, not hand written:

```bash
cd py     && make parse && make process > /tmp/corners.yaml   # regenerate
cd ngspice && make corners                                    # expand to spice
```

[py/genyaml](../py/genyaml.md) walks the PDK's `sky130.lib.spice` and prints the
`corner:` blocks for [cicsim/cicsim.yaml](../cicsim/cicsim.yaml.md);
[ngspice/corners.py](../ngspice/corners.py.md) expands that yaml into
`ngspice/corners.spi` for anyone simulating without cicsim. Commit both.
