#set VDD AVDD
#set GND AVSS
#set SUB 0

load {PATH}/{CELL}.mag
#writeall force

#flatten {CELL}_flat
#load {CELL}_flat

select top cell

extract path extfiles
extract all

ext2sim labels on
ext2sim -p extfiles

ext2spice lvs
ext2spice format ngspice
ext2spice resistor off
#ext2spice hierarchy off
#ext2spice subcircuits off
#ext2spice merge conservative
ext2spice cthresh 0.1
ext2spice -p extfiles -o lpe/{CELL}_lpe.spi
quit
