


cell:
	cicsim simcell  ${LIB} ${CELL} ../tech/cicsim/cell_spice/template.yaml

cellsv:
	cicsim simcell  ${LIB} ${CELL} ../tech/cicsim/cell_sv/template.yaml

netlist_cell:
	test -d ../../work/xsch || mkdir ../../work/xsch
	cd ../../work/ && make xsch LIB=${LIB} CELL=${CELL}
ifeq ($(VIEW),Lay)
	cd ../../work && make cdl lpe LIB=${LIB} CELL=${CELL}
#- THE LPE NETLIST NEVER MEETS fixsubckt, so a sky130 diode reaches
#- the simulator with magic's extraction units: area in square
#- picometres read as square METRES, whose junction capacitance is
#- farads. Measured on tt_um_lelo_temp_wulffern: the solver died at
#- the first input edge (timestep 1e-21), every temperature. Same
#- charter as fixsubckt: LVS keeps magic's units, the SIMULATION
#- netlist is the side that gets patched. Converts only values > 1,
#- so re-running never scales twice.
	perl -pi -e 'if (/sky130_fd_pr__diode/) { s/\barea=([0-9.eE+]+)/"area=".($$1>1?sprintf("%.6g",$$1*1e-24):$$1)/e; s/\bperim=([0-9.eE+]+)/"perim=".($$1>1?sprintf("%.6g",$$1*1e-12):$$1)/e; }' ../../work/lpe/${CELL}_lpe.spi
endif

ver:
	test -d ../../work/xsch && cd ../../work/ && make ver LIB=${LIB} CELL=${CELL}

netlist: netlist_cell
#- I've seen port ordering change between xschem version, so I also
# generate a xdut.spi file that always has the right port ordering.
#- TODO: Should I add the view here? Either xsch or lpe??
	perl ../../tech/script/genxdut ../../work/xsch/${CELL}.spice ${CELL}


netlist_sv:
	perl ../../tech/script/netlist_mdl ../../rtl/${CELL}.ys ${LIB}
	cd ../../rtl; yosys ${CELL}.ys
	perl ../../tech/script/genxdut ../../rtl/${CELL}.spice ${CELL}
