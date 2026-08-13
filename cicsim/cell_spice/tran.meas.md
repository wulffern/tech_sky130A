# tran.meas

Measurements to run on the raw file after the simulation, as an ngspice
`.control` block.

This is a **second ngspice invocation**, not part of the first: cicsim runs
`ngspice -b <run>.meas` once the simulation is done and captures the output in
`<run>.logm`. That is why the file starts by loading the raw file the
simulation left behind, and why an expensive measurement costs you nothing on
the simulation itself.

```spice
.control
load {cicname}.raw
echo "MEAS_START"
echo "MEAS_END"
.endc
```

`{cicname}` is substituted by cicsim with the name of the run.

The template is empty on purpose: the two echoes mark the region of
`<run>.logm` that cicsim parses, as `key = value` pairs and as tables. Add
measurements between them:

```spice
meas tran vout_final FIND v(OUT) AT=9n
print vout_final
```

The names that appear here are the ones [tran.yaml](tran.yaml.md) gives
specification limits to.
