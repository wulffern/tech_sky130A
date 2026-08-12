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

Every file in this repository has a markdown file beside it saying what it is
and who runs it, and every folder has a `README.md`. Those are published as a
site at <https://wulffern.github.io/tech_sky130A>, built by
[py/mkdocsite.py](py/mkdocsite.py.md) and the DOCS workflow.

```bash
python3 py/mkdocsite.py --check    # is anything undocumented?
python3 py/mkdocsite.py            # build docs/
cd docs && bundle install && bundle exec jekyll serve
```

When you add a file, add its `.md` beside it. CI fails otherwise.
