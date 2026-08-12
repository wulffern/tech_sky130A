# The design flow

The loop, from an empty schematic to a layout that passes everything. Every
command here is run from the IP's `work/` directory, which is where
[make/core.make](../make/core.make.md) expects to be.

Two variables control everything: `LIB`, the directory under `../design/`, and
`CELL`. Set them once in `work/Makefile` and leave them out of the commands, or
pass them per invocation:

```bash
make drc LIB=MY_IP_SKY130A CELL=MY_CELL
```

`PREFIX` is prepended to `CELL` if set, giving `PRCELL`, which is the name
actually used everywhere.

## The picture

```
     schematic                                 layout
  design/<LIB>/<CELL>.sch                design/<LIB>/<CELL>.mag
         │                                        │
    make xsch │ make cdl                          │ make gds / make drc
         ▼                                        ▼
  xsch/<CELL>.spice     ── make lvs ──▶   lvs/<CELL>.spi
  cdl/<CELL>.spice                        gds/<CELL>.gds
         │                                        │
         │                                   make lpe
         ▼                                        ▼
    simulation  ◀───────────────────  lpe/<CELL>_lpe.spi
```

## 1. Draw the schematic

```bash
make xview
```

Opens xschem with the setup from [xschem/xschemrc](../xschem/xschemrc.md): the
cpdk borders and symbols are on the library path, buses netlist as `<7>` rather
than `[7]`, and netlists land in `xsch/`.

## 2. Netlist it

```bash
make xsch      # xsch/<CELL>.spice, for simulation
make cdl       # cdl/<CELL>.spice, for LVS
```

Two netlists, because they need to be different. The simulation netlist has the
top cell as a real `.subckt` so a testbench can instantiate it, which is what
[script/fixsubckt](../script/fixsubckt.md) fixes up after xschem writes it. The
CDL uses `[]` bus characters, matching what magic's extraction produces.

## 3. Simulate the schematic

Covered in [Simulation](03-simulation.md). Do this before drawing any layout:
finding out the circuit does not work after a week of layout is an expensive
way to learn it.

## 4. Draw the layout

By hand in magic:

```bash
make lview
```

or generated from a ciccreator description:

```bash
make ip        # ../cic/ip.json -> ../design/<LIB>
make view      # inspect it in cic-gui
```

`make ip` runs ciccreator and then cicpy to transpile the result into spice,
verilog, xschem and magic views, using
[cic/sky130A.tech](../cic/sky130A.tech.md) for the layer map and rules. If
`../cic/ip.py` or `../cic/post.py` exist they run before and after.

Magic starts with [magic/.magicrc](../magic/.magicrc.md), which loads the
placement helpers in [magic/cic.tcl](../magic/cic.tcl.md) and turns on the full
DRC style.

## 5. Check the layout

```bash
make drc       # magic, full rule deck
make kdrc      # KLayout, the sign-off deck
make lvs       # magic extraction + netgen
make ant       # antenna check
```

Each prints one line per cell, green or red. Details are in
[Verification](04-verification.md).

Run them over a whole library with the `all` variants, once `CELLS` is set in
`work/Makefile`:

```bash
make drcall
make xlvsall
```

## 6. Extract and simulate again

```bash
make lpe       # lpe/<CELL>_lpe.spi, with capacitance
```

Then rerun the testbench with `VIEW=Lay`, which switches the include in the
testbench from the schematic netlist to the extracted one. Nothing else in the
testbench changes.

`make lpe` also LVSs the extracted netlist against the CDL with the capacitors
stripped out, so a netlist that silently lost a connection during extraction
does not quietly become your simulation result.

There are three extraction flows and the difference matters:
[lpe](../magic/lpe.tcl.md) flattens and extracts capacitance,
[lpeh](../magic/lpeh.tcl.md) keeps the hierarchy and is much faster on a large
block, [lper](../magic/lper.tcl.md) adds resistance and is the slowest.

## 7. Render it

```bash
make gds       # gds/<CELL>.gds
make lplot     # lplot/<CELL>.svg, coloured from the tech file
```

The SVG is a real vector image, which is why
[render_gds.py](../magic/render_gds.py.md) uses gdstk rather than KLayout. Drop
it in the README and it ends up in the documentation.

## 8. Deliver

See [Tapeout](05-tapeout.md).

## Cleaning up

```bash
make clean     # removes lvs drc lpe cdl gds and the extraction leftovers
```

Everything under `work/` is generated. If a result looks impossible, delete it
and run again before believing it.
