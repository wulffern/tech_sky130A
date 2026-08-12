# drc.tcl

Magic DRC, run by `make drc`.

```tcl
load {PATH}/{CELL}.mag
logcommands drc/{CELL}_drc.log
set b [view bbox]
box values ...
expand
expand
drc style drc(full)
drc catchup
drc why
drc count total
```

The box is set to the full cell view and expanded twice so that every child
cell is loaded and checked, not just the top level outline. `drc style
drc(full)` selects the complete rule deck rather than the fast subset.
`drc catchup` forces the check to finish before anything is printed, `drc why`
lists each violation, and `drc count total` prints the total on the last line.

That last line is all `make drc` looks at: it greps for `: 0` and prints
`DRC OK` or `DRC FAIL`. On failure the last ten lines of the log are shown.

For the KLayout deck instead, use `make kdrc` and
[script/checkkdrc](../script/checkkdrc.md).
