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
