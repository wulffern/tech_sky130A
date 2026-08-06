#- Flat extraction for LVS.
#-
#- The hierarchical extraction promotes every dangling net in a cell to
#- a subcircuit port: the dummy poly strips of the transistor pattern
#- and the unrouted bulk straps of tap-less leaf cells all become pins,
#- and netgen drowns the real comparison in port errors. Worse, it
#- cannot see a connection that only exists between cells, so an
#- assembly where a strap shorts two rails DRC-clean can still pass.
#-
#- ext2spice hierarchy off resolves connectivity by geometry across the
#- whole tree and writes one flat netlist. Dangling nets stay internal
#- node names instead of ports, wells and substrate resolve against the
#- taps that are actually there, and netgen flattens the schematic side
#- itself. subcircuit top on keeps the cell's own port list so pin
#- matching still means something.
set SUB 0
set OPATH lvs/ext
load {PATH}/{CELL}.mag
extract path ${OPATH}
extract all
ext2spice lvs
ext2spice hierarchy off
ext2spice subcircuit top on
ext2spice -p ${OPATH} -o lvs/{CELL}.spi
quit
