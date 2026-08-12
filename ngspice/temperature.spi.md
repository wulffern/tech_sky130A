# temperature.spi

The temperature corners, one `.option TEMP` per `.lib`.

| Corner | Temperature |
|:-|:-|
| `Tt` | 27 °C, typical |
| `Tm` | 42.4 °C |
| `Tl` | −40 °C |
| `Tnh` | 85 °C |
| `Tah` | 105 °C |
| `Th` | 125 °C |

`Tl` and `Th` are the pair used by the `slow`, `fast` and `etc` targets of the
[cell_spice Makefile](../cicsim/cell_spice/Makefile.md). `Tnh` and `Tah` are
there for parts qualified to a narrower range than 125 °C.

Note that `Tm` is not in the middle of anything: it is the temperature a die
tends to sit at, useful when a measurement is being matched.
