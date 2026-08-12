# render_gds.py

Renders a GDS to SVG, coloured with the layer map from
[cic/sky130A.tech](../cic/sky130A.tech.md). Run by `make lplot`:

```bash
python3 ../tech/magic/render_gds.py gds/<CELL>.gds lplot/<CELL>.svg [tech.json]
```

The tech file is optional; without it the script looks for
`../cic/sky130A.tech` relative to its own location.

## Why gdstk and not KLayout

The output has to be a real vector SVG so it scales without loss when it is
embedded in the documentation PDF. KLayout's Python API has no SVG export, so
[gdstk](https://heitzmann.github.io/gdstk/) does the writing.

## What it does with the tech file

For every layer with a `number`, a `datatype` and a `color`, it builds an SVG
style keyed on the `(number, datatype)` pair. The first definition wins, which
matters because several ciccreator layer names share one GDS purpose.

- `fill: nofill` in the tech file becomes an outline: no fill, 1 px stroke.
- Anything else becomes a translucent fill at 55% opacity with a 0.5 px stroke,
  so overlapping layers stay readable.
- Colour names are resolved through a small table (`red`, `goldenrod`, `aqua`,
  ...); an unknown name falls back to grey, and a `#rrggbb` value is used
  as is.

Layers `(235, 0)`, `(235, 4)` and `(235, 5)`, the prBoundary and area-ID
layers, are filtered out of every cell before rendering. They are usually the
largest shapes in the file, and leaving them in would inflate the SVG viewBox
so the actual layout is drawn small.

The top cell is written at `scaling=20` with a 2% pad on a white background.
Requires `gdstk`; the script has no other dependency.
