# jnw.yaml

The template for the JNW flow. Identical to
[ip_template.yaml](ip_template.yaml.md) except for three things.

**No `rtl/` directory.** JNW blocks are analog, so there is no gate level
verilog to keep.

**A SIM workflow.** `.github/workflows/sim.yaml` calls
`analogicus/jnw-actions/.github/workflows/sim.yaml@main` on any push that
touches `design/**.sch`, `design/**.mag`, `design/**.sym`, `sim/**`,
`info.yaml` or `config.yaml`, and the README gets the matching badge. This is
the flow where simulations are expected to run on every commit, not just
locally.

**No `addpath` lines** for `JNW_ATR_SKY130A` and `JNW_TR_SKY130A` in
`work/.magicrc`; the libraries are reached through the `design/` symlinks
instead.

Dependencies are the same: `cpdk`, `tech_sky130A`, `jnw_tr_sky130a`,
`jnw_atr_sky130a`.
