# bash

Shell environment for the sky130A tools.

The EDA tools find the PDK through environment variables rather than through
any file in this repository, so the variables have to be set before magic,
xschem, netgen or ngspice start. This folder holds the snippet that sets them.
