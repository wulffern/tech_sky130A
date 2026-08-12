# cic.tcl

Interactive tcl procedures, loaded by [.magicrc](.magicrc.md) into every magic
session. They work on the *fixed bounding box* of a cell, the `FIXED_BBOX`
property that ciccreator writes and that
[script/fixbbox](../script/fixbbox.md) repairs, so cells abut exactly instead
of by eye.

## `cicarray <x> <y>`

Arrays the selected cell `x` by `y`. Reads `FIXED_BBOX`, scales it by the
technology lambda, resizes the box to exactly one cell pitch and then calls
magic's `array`. Without the resize the array step would be the drawn extent of
the cell, which is usually a little smaller or larger than the pitch it should
be placed on.

## `cicPlaceVertical`

Stacks every instance in the cell vertically, starting at the current box
position. Instances are sorted bottom-to-top by their current y position
(`cicYSort`, alphabetically on a tie), then each is moved so its fixed bounding
box sits directly on top of the previous one. Useful after a generated layout
has the right cells but the wrong arrangement.

## `cicYSort a b`

The comparison used by `cicPlaceVertical`. Not meant to be called directly.
