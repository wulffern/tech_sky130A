# genxdut

Writes `xdut.spi`, a single line that instantiates the DUT with the port order
of the netlist that was just generated.

```bash
perl ../../tech/script/genxdut ../../work/xsch/<CELL>.spice <CELL>
```

Run by the `netlist` target of [sim.make](../make/sim.make.md).

```spice
*Automatic generated instance fron ../../tech/scripts/genxdut MY_CELL
XDUT VDD VSS IN OUT MY_CELL
```

Port ordering has changed between xschem versions, so a testbench that spells
out its own DUT instance silently connects the wrong nets after a tool upgrade.
Testbenches therefore `.include ../xdut.spi` and this file is regenerated from
the current netlist every time.

It reads the `.subckt <name>` line and its `+` continuations, flattens them
onto one line, and writes the instance. The header comment names an older path
for the script.
