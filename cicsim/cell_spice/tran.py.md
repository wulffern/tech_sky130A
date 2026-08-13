# tran.py

Optional python post-processing, run by cicsim after the measurements.

The template returns immediately:

```python
def main(name):
  # Delete next line if you want to use python post processing
  return
```

Delete that `return` and the rest of the function reads `<name>.yaml`, the
measurement results, lets you compute anything ngspice could not, and writes
the yaml back. Whatever ends up in the file is what the summary table reports.

This is where a derived figure of merit belongs: an ENOB from a measured SNR,
a gain from two measured voltages, a yield from a Monte Carlo set.

## When it runs, and what it is handed

After every simulation in the invocation has succeeded, and before cicsim
collects the results. One failed simulation and the whole post-processing step
is skipped, so a missing derived number usually means a failed corner rather
than a broken script.

cicsim imports the module once and calls `main` for each run, inspecting the
signature first:

```python
def main(name):                 # name of the run, e.g. tran_Sch_typical_Ktt...
def main(name, corner):         # also gets the corner, if you declare it
```

Declaring the second parameter is how a script behaves differently per corner
without parsing the run name.
