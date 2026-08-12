# supply.spi

The supply corners, as parameters rather than sources. A testbench writes

```spice
.param AVDD = {vdda}
VDD  VDD_1V8  VSS  pwl 0 0 10n {AVDD}
```

and the corner decides the value.

| Corner | vdda | vdde | vddh |
|:-|:-|:-|:-|
| `Vt` typical | 1.8 | 3.0 | 12 |
| `Vl` low | 1.7 | 2.4 | 10.8 |
| `Vh` high | 1.9 | 3.6 | 13.2 |

`vdda` is the 1.8 V core supply at ±5%. `vdde` is the 3.0 V IO supply, spread
much wider (−20% / +20%) because that is what the IO devices have to survive.
`vddh` is the 12 V high voltage domain at ±10%.
