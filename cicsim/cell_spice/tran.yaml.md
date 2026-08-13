# tran.yaml

Specification limits for the measurements, one block per measured name. The
template is all comments, showing the fields:

```yaml
#<name>:
#  src:
#    - <paramters>
#  typ: <typical spec value>
#  name: <long name>
#  min: <minimum spec value>
#  max: <maximum spec value>
#  scale: <scale, multiply result by scale>
#  digits: <significant digits>
#  unit: Unit
```

cicsim uses this when it builds the summary table: `min` and `max` decide
whether a result passes, `scale`, `digits` and `unit` decide how it is
displayed, and `name` is the human readable label. `desc` is accepted too,
though the template does not mention it.

`src` is the selector, not a formula: it names the measurement column, or a
list of columns, that this entry covers, and the summary keeps only the
columns some spec names. So a measurement with no entry here is not merely
unjudged — it is dropped from the table. Defaults if you omit a field are
`unit: V`, `scale: 1`, `typ: 0`, `digits: 2`.
