# gensvinst

Builds an ngspice `d_cosim` instance for a verilog module, so a compiled RTL
block can be co-simulated inside an analog testbench.

```bash
../tech/script/gensvinst <file.v> <module>
```

Writes `svinst.spi` in the current directory.

Ports are parsed from the `module <name> (...)` header: `parameter` lines are
collected first and substituted into bus ranges, so `[NBITS-1:0]` resolves.
Each bus bit becomes a separate node named `<port>.<index>`, counting down from
the msb, which is the naming the `d_cosim` bridge expects.

The generated file holds:

- the `adut_<name>` instance, with the input node list and then the output node
  list
- `.model dut_<name> d_cosim simulation="../<name>.so" delay=10p`, pointing at
  the compiled shared object
- a 1 GΩ resistor from every input and output node to ground, so ngspice does
  not complain about floating nodes
- for every output bus, a behavioural source `dec_<port>` that sums the bits
  weighted by 2^i and divided by `AVDD`, then `.save`s it

That last part is the useful one: it gives you the decimal value of a bus as a
single waveform, so a counter or an ADC output can be plotted directly instead
of as N separate digital traces. Scalar outputs are just `.save`d.

Perl. Note the generated header comment names an older path for this script.
