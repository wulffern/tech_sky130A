# fixlpe

Replaces the port list of a flat extracted netlist with the one from the
schematic netlist.

```bash
../tech/script/fixlpe lpe/<CELL>_lpe.spi xsch/<CELL>.spice <CELL>
```

Run by `make lpe`, `make lper` and `make lpeh`, in place.

Flat extraction gets the *devices* right and the *ports* wrong: magic derives
the `.subckt` line from what happens to be labelled in the flattened layout, so
the order differs from the schematic and dangling internal nets appear as pins.
A testbench that includes the extracted netlist then connects the wrong things.

The fix is blunt and works: take the `.subckt` line (with its `+`
continuations) from the schematic netlist, and swap it in. The original
extracted port list is not deleted but commented out with a leading `*`,
prefixed by

```
* Replacing the lpe port list (../tech/scripts/fixlpe)
```

so the diff is visible in the netlist itself. Square brackets are converted to
angle brackets on the way through, matching the bus convention the rest of the
flow uses.

Both replacement and original are echoed to the terminal.
