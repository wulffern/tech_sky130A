# sky130A.tech

The ciccreator technology file: layer map, device map and design rules for
sky130A, as JSON.

Four top level keys.

## version

Format version of the file, currently `2`.

## layers

58 named layers. A layer entry maps a ciccreator layer name onto a GDS
`number`/`datatype` pair, a magic `alias`, and the `material` ciccreator uses
to decide what a shape means:

```json
"M1" : { "alias" : "locali", "number" : 67, "datatype": 20,
         "material" : "metal", "previous" : "", "next" : "VIA1",
         "pin" : "M1_pin", "res" : "M1_res", "color" : "blue" }
```

`previous` and `next` chain the routing stack together (`M1` → `VIA1` → `M2`
→ ...) so ciccreator can build a via stack between any two layers. `pin` and
`res` point at the pin-purpose and resistor-purpose variants of the same
metal. `color` and `fill` are used when a layout is rendered, including by
[render_gds.py](../magic/render_gds.py.md), which reads this file to colour
its SVG.

Note the naming: the ciccreator stack is `M1..M5`, but sky130's local
interconnect is the bottom of that stack, so `M1` is `li`/`locali`, `M2` is
`met1`, and so on up to `M5` = `met4`. The magic `alias` column is where that
translation is written down.

Beyond the routing layers there are the diffusion, poly and implant layers
(`OD`, `PDIFF`, `NDIFF`, `PTAP`, `NTAP`, `PO`, `NW`, `PP`, `NP`, ...), the
threshold implants (`NLVT`, `PLVT`), the poly resistor layers (`POR`, `POXR`,
`CPOR`), the MiM cap layers (`MIM`, `MIMC`) and the `PR` boundary.

Some layers are duplicates that exist only so a shape can be tagged
differently in the source while landing on the same mask, for example `DMYPO`
(a dummy poly strip that is not a transistor gate) and `DMYPOR` (a resistor
dummy that must not be counted as a finger).

## technology

Global constants:

| Key | Value | Meaning |
|:-|:-|:-|
| `gamma` | 100 | Ångström per rule unit, so every rule below is in units of 100 Å = 10 nm |
| `grid` | 5 | Snap grid for ciccreator |
| `spiceunit` | 1 | Scale for device properties in the netlist |
| `techlib` | `sky130A` | PDK library name |
| `symbol_lib` | `cpdk` | Default xschem symbol library |
| `symbol_libs` | list | Where to look for symbols: `cpdk` design dirs and the PDK's `sky130_fd_pr` |

### Units

The internal coordinate system is **ångström**. In cicpy, `Cell.toMicron` is
`(angstrom/10)/1000.0` and a layout cell carries `um = 10000`, so there are
10 000 internal units in a micron.

`gamma` is what gets a rule into that system: `Rules.get()` returns
`rule_value * gamma`. With `gamma = 100`, a rule of `30` is 3000 Å, which is
0.3 µm. So the numbers in the `rules` section are in steps of 10 nm, not in
nanometres and not in internal units.

A worked example from the history of this file: `VIA4` (magic's via3) was
changed from `28` to `32` in a commit titled "legal VIA4 size", which is
0.28 µm → 0.32 µm, sky130's exact via3 size.

Magic output is a third scale again. `MagicPrinter.toMicron` is
`round(angstrom/50)`, snapping to the 50 Å = 5 nm sky130 grid; that 50 is
hard coded in cicpy and does not come from `grid`.

`grid` and `spiceunit` are read into cicpy's `Rules` object and then never
used by it, so whatever they do, they do it on the ciccreator side.

`devices` maps a ciccreator device name to the PDK subcircuit it netlists as,
its `devicetype` prefix and its port order:

| ciccreator | sky130 device | Type |
|:-|:-|:-|
| `nch` / `pch` | `sky130_fd_pr__nfet_01v8` / `pfet_01v8` | `XM` |
| `nch_lvt` / `pch_lvt` | `..._nfet_01v8_lvt` / `pfet_01v8_lvt` | `XM` |
| `rppo` | `sky130_fd_pr__res_high_po` | `XR` |
| `mresM1..M4` | `sky130_fd_pr__res_generic_l1/m1/m2/m3` | `R` |
| `mim` | `sky130_fd_pr__cap_mim_m3_1` | `XC` |

`propertymap` renames ciccreator properties onto the model parameters, so
`l`/`w`/`nf` become `length`/`width`/`nf`.

## rules

34 rule groups, all in units of 10 nm (see [Units](#units) above: the value
is multiplied by `gamma` to give ångström). A rule is either a plain minimum
(`width`, `space`, `minwidth`, `minlength`) or a relationship between two
layers, written as `<OTHER>enclosure` and `<OTHER>encOpposite` (enclosure
along and across the shape):

```json
"M1" : { "minlength": 30, "space": 30, "width": 30, "minwidth": 30,
         "ana_width": 30, "cap_width": 40, "capspace": 32,
         "VIA1enclosure": 3, "VIA1encOpposite": 6, "PTAPCenclosure": 0 }
```

Read that as: 0.30 µm minimum width and spacing, 0.40 µm when the metal is a
capacitor plate, and 0.03 µm of enclosure along a VIA1 with 0.06 µm across it.

`ROUTE` is the router's view of the stack rather than a DRC rule:

```json
"ROUTE" : { "horizontalgrid": 30, "verticalgrid": 40,
            "pinlayer": "M1", "pintravel": "v",
            "costs": { "M1": 1, "M2": 2, "M3": 2, "M4": 2, "M5": 4 },
            "directions": { "M2": "v", "M3": "h", "M4": "v", "M5": "h" } }
```

The two grids are on the same 10 nm scale as everything else, so routing is on
a 0.30 µm horizontal and 0.40 µm vertical pitch. `costs` biases the router
towards the cheap layers, `directions` fixes the preferred direction per
layer, and `pinlayer`/`pintravel` say that pins are on `M1` and that the
router may travel vertically on the pin layer, which is the cheapest thing it
can do.

`CELL` holds the placement pitch (`space` 20 = 0.20 µm, `digitalspace` 18 =
0.18 µm) rather than a geometric rule.
