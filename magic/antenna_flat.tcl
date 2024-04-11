

crashbackups stop
drc off
snap internal
load {PATH}/{CELL}.mag -dereference

flatten {CELL}_flat
load {CELL}_flat

select top cell
extract path extfiles
extract do local
extract no all
extract all
antennacheck debug
antennacheck -p extfiles
quit
