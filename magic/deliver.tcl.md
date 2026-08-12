# deliver.tcl

Writes the abstract view for a tapeout. Used by `make deliver`, which
substitutes `{LIB}` and `{CELL}` before running it:

```tcl
load ../design/{LIB}/{CELL}.mag
lef write ../tapeout/lef/{CELL}.lef -pinonly
exit
```

`-pinonly` writes the pins and the cell outline but no obstruction geometry, so
the LEF describes where a top level router may connect without also describing
the whole cell.

Note that this is one of the few scripts here that takes `{LIB}` as well as
`{CELL}`, and that it ends in `exit` rather than `quit`.
