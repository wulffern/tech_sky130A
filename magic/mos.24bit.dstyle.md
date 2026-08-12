# mos.24bit.dstyle

Magic display styles for a 24-bit X11 display: what colour and fill pattern
each layer is drawn with, which stipples exist, and how the layers stack in the
window.

It is the MOSIS distribution version 8.2 file, originally for three metal two
poly SCMOS, kept here so a layout looks the same on every machine regardless of
what the local magic install ships.

Sections, in file order:

- **`display_styles`** — one line per style: colour index into
  [mos.24bit.std.cmap](mos.24bit.std.cmap.md), stipple number, outline mask and
  the character used when the style is written to a `.mag` file.
- **`stipples`** — the fill patterns, eight hex bytes each, one per row of an
  8×8 bitmap. [bitpattern.py](bitpattern.py.md) prints these as ones and zeros,
  [bit2hex.py](bit2hex.py.md) goes the other way.

Magic finds it through the PDK's magicrc, not through
[.magicrc](.magicrc.md) directly.
