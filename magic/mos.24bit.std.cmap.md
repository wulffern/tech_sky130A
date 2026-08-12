# mos.24bit.std.cmap

The colour map that [mos.24bit.dstyle](mos.24bit.dstyle.md) indexes into. One
line per colour:

```
# R  G   B  idx color-name
255 255 255 0   background_gray
220 95  95  1   poly_red
66  213 66  2   diff_green
```

RGB is 0–255, `idx` is the number a display style refers to, and the name is a
comment for humans.

Change a colour here and every layer drawn in that style changes; change a
style in the `.dstyle` file to move one layer onto a different colour.
