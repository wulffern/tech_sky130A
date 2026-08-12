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
displayed, and `name` is the human readable label. `src` names the measurements
a derived entry is computed from.

A measurement with no entry here still appears in the results; it just has no
specification to be judged against.
