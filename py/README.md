# py

Python tools that are too large to live in [script/](../script/README.md), all
using [click](https://click.palletsprojects.com) for their command line.

| Tool | Run by | What it does |
|:-|:-|:-|
| [genyaml](genyaml.md) | this folder's [Makefile](Makefile.md) | Turns the PDK's spice library tree into the corner definitions |
| [fixmag.py](fixmag.py.md) | `make fixmag` | Repairs the library paths in a `.mag` hierarchy |
| [matchports.py](matchports.py.md) | `make matchports` | Renumbers layout ports to match the schematic pin order |
| [deps2tapeout.py](deps2tapeout.py.md) | `make preflight` | Pins every dependency to an exact commit for a delivery |
| [readme2tapeout.py](readme2tapeout.py.md) | `make deliver` | Converts an IP README into a Tiny Tapeout `info.md` |
| [mkdocsite.py](mkdocsite.py.md) | the DOCS workflow | Builds the site you are reading |
