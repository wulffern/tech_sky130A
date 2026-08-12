# bit2hex.py

A throwaway helper for writing stipple patterns into
[mos.24bit.dstyle](mos.24bit.dstyle.md).

Magic's display styles describe a fill pattern as eight hex bytes, one per
row of an 8×8 bitmap. Writing that by hand is unpleasant, so the two patterns
here are drawn as strings of ones and zeros

```python
stipple = [
"11111111",
"10000011",
...
]
```

and printed as hex:

```bash
python3 bit2hex.py
```

The two patterns are diagonal hatches leaning in opposite directions. Edit the
lists and rerun to make a new one; there is no command line interface.

[bitpattern.py](bitpattern.py.md) does the inverse.
