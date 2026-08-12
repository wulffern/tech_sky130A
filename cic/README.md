# cic

The sky130A technology description for
[ciccreator](https://github.com/wulffern/ciccreator) and
[cicpy](https://github.com/wulffern/cicpy), the tools that generate transistor
level layout from a `.cic` description.

Where the PDK tells magic and KLayout how to check a layout, this file tells
ciccreator how to *draw* one: which GDS purpose each abstract layer maps to,
how wide a metal may be, how much enclosure a via needs, and which layers the
router may use in which direction.

Two names, one file: [sky130.tech](sky130.tech.md) is a symlink to
[sky130A.tech](sky130A.tech.md), because some flows ask for the variant letter
and some do not.
