# checklvs

Reads a netgen LVS log on stdin and prints whether the circuits matched.

```bash
cat lvs/<CELL>_lvs.log | ../tech/script/checklvs <CELL> [--short] [--noprop]
```

| Option | Effect |
|:-|:-|
| none | Echoes the whole log, then a large ASCII smiley or frowny |
| `--short` | One line: `<CELL>  [ LVS OK ]` in green, or `[ LVS FAIL ]` in red |
| `--noprop` | Ignore property errors when deciding |

Exit status is 0 on a match, 1 otherwise, so it gates `make lvs`.

A run counts as passing when netgen says `Circuits match uniquely` and there
were no property errors, no `failed pin matching` and no
`Final result: Netlists do not match`.

`--noprop` exists for the flat flow. Flat LVS resolves symmetric gates by their
properties, and netgen flags that as a property error even when every itemized
property matches, so the flat run passes `--noprop` and property checking is
left to the hierarchical per-cell runs.

Perl, uses `Term::ANSIColor`.
