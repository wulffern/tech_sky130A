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

## Reproducible parasitics

The script also sorts the extracted parasitics and renumbers them, so that
extracting an unchanged layout twice produces a byte identical netlist.

magic does not emit the parasitic list in a stable order. The same layout
extracted twice gives the same parasitics — same nodes, same values, same
count — in a different sequence and under different `C<n>` names. Measured on
`LELOTEMP_CMP`: three extractions, 181 capacitors and 55 other lines every
time, every non-parasitic line byte identical, only the ordering moving.

That matters because the file hash is what the flow keys off. `cicsim` records
a sha per dependency per corner and re-simulates when one stops matching, so a
re-extraction marked every `Lay` run stale and invited hours of resimulating an
unchanged circuit. It also made `lpe/*.spi` useless to diff when a layout
change really *did* alter the parasitics, because the signal drowned in
reordering.

Lines of the form

```
C<n> node node value [$ comment]
R<n> node node value [$ comment]
```

are collected, sorted on the unordered node pair and the value, renumbered from
zero per type, and written back where the block started. The nodes are emitted
in the order magic wrote them; the pair is only ordered to build the sort key.
Anything mentioning `sky130` is left alone, so device resistors — which come
out as `R<n>` lines carrying a model name — keep their place.

Reordering is safe: a spice netlist is a set of elements, and the element names
are labels nothing reads. `make lvs` strips every `^C` line before netgen sees
it. No device, node or value is touched.
