# lelo.yaml

The template for the LELO flow, a trimmed version of
[ip_template.yaml](ip_template.yaml.md).

Differences:

- **A root `Makefile`** holding `LIB`, `CELL` and
  `include tech/make/main.make`, so `make docs` works from the IP root. See
  [main.make](../make/main.make.md).
- **No `rtl/` directory** and no `sim:` section in `info.yaml`.
- **A smaller starting schematic**: the `border_xs` symbol instead of
  `border_s`, with the pins placed for a small block.
- The `work/Makefile` comment block documents `xsch` and `lvs` rather than
  `ip` and `xlvs`.

Dependencies and workflows are otherwise the same as the generic template:
`cpdk`, `tech_sky130A`, `jnw_tr_sky130a`, `jnw_atr_sky130a`, with GDS, DRC, LVS
and DOCS running in CI.
