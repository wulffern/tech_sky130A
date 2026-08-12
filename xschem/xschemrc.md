# xschemrc

The xschem startup file for an IP repository. Start xschem from the IP's
`work/` directory and it picks this up through the IP's own `xschemrc`, which
sources this one.

It begins by sourcing the PDK setup,
`$PDK_ROOT/sky130A/libs.tech/xschem/xschemrc`, then overrides what this flow
needs differently.

## Symbol libraries

`XSCHEM_LIBRARY_PATH` is flushed and rebuilt so the search order is known:
the xschem share dir, the user's `~/.xschem/xschem_library`, the PDK's
`libs.tech/xschem`, and finally `../../cpdk/design` for the shared borders and
symbols from [cpdk](https://github.com/wulffern/cpdk).

`dircolor` tints the library browser: PDK libraries blue, the personal and
device libraries red.

## Netlisting

| Setting | Value | Why |
|:-|:-|:-|
| `netlist_dir` | `$PWD/xsch` | `make xsch` expects `xsch/<CELL>.spice` |
| `bus_replacement_char` | `<>` | `DATA[7]` netlists as `DATA<7>`, which is what magic's extracted netlist uses |
| `netlist_type` | `spice` | |
| `ngspice_netlist` | 1 | |

`make cdl` overrides `bus_replacement_char` back to `[]` on the command line,
because the CDL that goes to netgen is compared against a layout netlist that
uses brackets.

## Editing

- `to_pdf` is `ps2pdf -dAutoRotatePages=/None`, so exported schematics keep
  their orientation
- `editor` opens an xterm with emacs
- toolbar and tabbed interface are both on
- `XSCHEM_START_WINDOW` is the PDK's `sky130_tests/top.sch`

## Things left commented out

`local_netlist_dir`, `top_subckt`, `lvs_netlist`, `replace_key` and
`xschem_libs`/`noprint_libs` are all present but disabled. `lvs_netlist` in
particular is set from the command line by `make cdl` instead of here, so that
the same rc file serves both the simulation netlist and the LVS netlist.
