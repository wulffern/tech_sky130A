# Technology PDK layer for tech_sky130A

This is not a full PDK, it's a small layer of customization on top of the
existing PDK.

An IP repository clones this one as `tech`, and every relative path here is
written against that layout:

```
my_ip/
├── tech -> ../tech_sky130A
├── design/MY_IP_SKY130A/
├── work/          make drc, lvs, gds, lpe, deliver
├── sim/           cicsim testbenches
└── .github/workflows/
```

[cicconf](cicconf/README.md) is what creates that structure.

## Guides

Start here if you have not used this before.

| Guide | |
|:-|:-|
| [Getting started](guide/01-getting-started.md) | Tools, environment, and making your first IP |
| [The design flow](guide/02-design-flow.md) | Schematic → netlist → layout → checks → extraction |
| [Simulation](guide/03-simulation.md) | Corner names, testbenches, specs and summaries |
| [Verification](guide/04-verification.md) | DRC, LVS (and when to go flat), antenna, repairs |
| [Tapeout](guide/05-tapeout.md) | Pinning dependencies, delivering, precheck |
| [When something breaks](guide/06-troubleshooting.md) | The failures you will actually hit |

## Reference

| Folder | Description |
|:-|:-|
| [bash](bash/README.md) | `PDK_ROOT` and `PDK`, which every tool here assumes |
| [cic](cic/README.md) | Layer map, device map and design rules for [ciccreator](https://github.com/wulffern/ciccreator) |
| [cicconf](cicconf/README.md) | Templates for [cicconf](https://github.com/wulffern/cicconf) |
| [cicsim](cicsim/README.md) | Templates for [cicsim](https://github.com/wulffern/cicsim) and default simulation files |
| [magic](magic/README.md) | Color maps for magic, a .magicrc, and the batch scripts behind DRC/LVS/LPE |
| [make](make/README.md) | Makefiles for running DRC/LVS/LPE etc |
| [ngspice](ngspice/README.md) | Definition of temperature and supply corners |
| [py](py/README.md) | Larger python tools: dependency pinning, port matching, corner generation |
| [script](script/README.md) | Any scripts |
| [xschem](xschem/README.md) | xschem setup files |

## Documentation

The guides above live in [guide/](guide/01-getting-started.md). The reference
is the repository itself: every file has a markdown file beside it saying what
it is and who runs it, and every folder has a `README.md`. Both halves are
published as a site at <https://wulffern.github.io/tech_sky130A>, built by
[py/mkdocsite.py](py/mkdocsite.py.md) and the DOCS workflow.

```bash
python3 py/mkdocsite.py --check    # is anything undocumented?
python3 py/mkdocsite.py            # build docs/
cd docs && bundle install && bundle exec jekyll serve
```

When you add a file, add its `.md` beside it. CI fails otherwise.
