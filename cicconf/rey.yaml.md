# rey.yaml

The template for the REY flow. Like [lelo.yaml](lelo.yaml.md), with its own
standard cell libraries.

- **`rey_tr_sky130a` and `rey_atr_sky130a`** replace the `jnw_` libraries, both
  in `config.yaml` and in the `design/` symlinks.
- **A wider `.gitignore`**: on top of the usual tool output it also ignores
  `*.logm`, `*.sha`, `*.raw`, `*.out`, `*.vcd`, `simulation/`, `results/`,
  `docs/`, `*.html`, `/cdl/`, the `*_svg/` directories and `*_obj_dir/`. That
  last one is verilator's build directory.
- **A root `Makefile`** including [main.make](../make/main.make.md), same as
  the LELO template.

Note that this template ignores `docs/`, so a REY IP keeps its generated
documentation out of git and rebuilds it in CI.
