# fixspi

Sorts the instances inside every `.subckt` by group and number. Reads stdin,
writes stdout; used by `make spi`.

```
xbber223a D G S B PMOS          xaber123a D G S B NMOS
xaber223a D G S B NMOS    ->    xaber223a D G S B NMOS
xaber123a D G S B NMOS          xbber223a D G S B PMOS
```

An instance name is split into a leading group (everything before the first
digit or bracket) and a trailing number, and the lines are emitted grouped and
then numerically ordered. A netlist that comes out in a stable order diffs
cleanly against the previous run, which is the whole point.

On the way through it also:

- joins `+` continuation lines into one line
- uncomments `**.subckt` and `**.ends`, the same xschem quirk
  [fixsubckt](fixsubckt.md) deals with
- rewrites bus brackets `<7>` as `_7`

Comment lines inside a subcircuit are passed through in place. A line that does
not parse raises an exception rather than being silently dropped.
