# tran.meas

Measurements to run on the raw file after the simulation, as an ngspice
`.control` block.

```spice
.control
load {cicname}.raw
echo "MEAS_START"
echo "MEAS_END"
.endc
```

`{cicname}` is substituted by cicsim with the name of the run.

The template is empty on purpose: everything printed between `MEAS_START` and
`MEAS_END` is parsed by cicsim into the result yaml, keyed by name. Add
measurements between the two echoes:

```spice
meas tran vout_final FIND v(OUT) AT=9n
print vout_final
```

The names that appear here are the ones [tran.yaml](tran.yaml.md) gives
specification limits to.
