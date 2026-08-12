# bitpattern.py

The inverse of [bit2hex.py](bit2hex.py.md): reads the `stipples` section of
[mos.24bit.dstyle](mos.24bit.dstyle.md) in the current directory and prints
each pattern as an 8×8 grid of ones and zeros, so you can see what a style
actually looks like without starting magic.

```bash
cd magic && python3 bitpattern.py
```

The filename is hard coded, so run it from this folder.
