# antenna.tcl

Hierarchical antenna check, run by `make ant`.

Extracts the cell into `ant/ext` and runs magic's `antennacheck`, which
compares the area of metal attached to a gate against the gate area and
reports every net over the process limit.

```tcl
extract path ant/ext
extract all
antennacheck debug
antennacheck -p ant/ext
```

`crashbackups stop` and `drc off` keep the batch run quiet and fast;
`snap internal` avoids moving anything onto the display grid.

The log goes to `ant/<CELL>_ant.log` and is summarised by
[script/checkant](../script/checkant.md), which turns it into a CSV.

Use [antenna_flat.tcl](antenna_flat.tcl.md) instead when the violation only
appears once the hierarchy is flattened, which is the usual case for a net
that is routed across several cells.
