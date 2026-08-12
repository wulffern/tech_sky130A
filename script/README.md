# script

Small standalone programs, in whatever language suited the job, called from
the make targets in [make/](../make/README.md). Python where there is data to
structure, perl where there is a text stream to rewrite.

They fall into three groups.

**Check** — turn a tool log into a verdict:
[checkant](checkant.md), [checkkdrc](checkkdrc.md), [checklvs](checklvs.md).

**Fix** — repair a netlist or a layout the tools got wrong:
[fixbbox](fixbbox.md), [fixlpe](fixlpe.md), [fixspi](fixspi.md),
[fixsubckt](fixsubckt.md).

**Generate** — write a file from another file:
[gensvinst](gensvinst.md), [genver](genver.md), [genxdut](genxdut.md),
[netlist_mdl](netlist_mdl.md).
