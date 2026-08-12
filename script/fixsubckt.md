# fixsubckt

Removes the `**` that xschem puts in front of the top level subcircuit. Reads
stdin, writes stdout; run by `make xsch` on every schematic netlist.

Xschem comments out the top `.subckt`, presumably to emulate a testbench top.
This flow wants the opposite: the top cell must be a real subcircuit so it can
be instantiated as a DUT inside a testbench.

So `**.subckt` becomes `.subckt`, `**.ends` becomes `.ends`, and the `*+`
continuation lines that follow a commented subcircuit line become plain `+`
continuations. Commas are replaced with spaces, which strips the bus notation
xschem emits in a port list.
