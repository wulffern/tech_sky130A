#!/usr/bin/env python3
"""Render a GDS to SVG using layer colors from ``tech/cic/sky130A.tech``.

Usage:
    render_gds.py <in.gds> <out.svg> [tech.json]

We use gdstk so the output is a real vector SVG that scales without quality
loss when embedded in the LaTeX PDF. KLayout's Python API has no SVG export.
"""
import json
import os
import sys

import gdstk


# ---------- args ----------
if len(sys.argv) < 3:
    print("usage: render_gds.py <in.gds> <out.svg> [tech.json]", file=sys.stderr)
    sys.exit(2)

gds_path = sys.argv[1]
out_path = sys.argv[2]
tech_path = sys.argv[3] if len(sys.argv) > 3 else None
if not tech_path:
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.normpath(os.path.join(here, "..", "cic", "sky130A.tech"))
    if os.path.exists(candidate):
        tech_path = candidate


# ---------- color helpers ----------
NAMED_COLORS = {
    "red": "#cc2222", "green": "#22aa22", "blue": "#3355cc",
    "yellow": "#ddcc22", "cyan": "#33ccdd", "aqua": "#33ccdd",
    "pink": "#dd88aa", "brown": "#8b5a2b", "darkgreen": "#006400",
    "goldenrod": "#daa520", "purple": "#8844aa", "orange": "#dd7722",
    "magenta": "#cc33cc", "white": "#ffffff", "black": "#000000",
    "gray": "#888888", "grey": "#888888",
}


def to_hex(name):
    if not name:
        return "#888888"
    if name.startswith("#") and len(name) == 7:
        return name
    return NAMED_COLORS.get(name.lower(), "#888888")


# ---------- parse tech file -> per-(layer,datatype) SVG style ----------
HIDDEN = {(235, 4), (235, 0), (235, 5)}  # prBoundary / area-ID

style = {}
if tech_path and os.path.exists(tech_path):
    with open(tech_path) as f:
        tech = json.load(f)
    for _, props in (tech.get("layers") or {}).items():
        num = props.get("number")
        dt = props.get("datatype", -1)
        color = props.get("color")
        fill = props.get("fill", "fill")
        if num is None or dt is None or dt < 0 or not color:
            continue
        key = (num, dt)
        if key in style:
            continue  # first definition wins
        hex_color = to_hex(color)
        if fill == "nofill":
            style[key] = {"fill": "none", "stroke": hex_color, "stroke-width": "1"}
        else:
            style[key] = {
                "fill": hex_color, "stroke": hex_color,
                "fill-opacity": "0.55", "stroke-width": "0.5",
            }

# ---------- render ----------
lib = gdstk.read_gds(gds_path)
tops = lib.top_level()
if not tops:
    raise SystemExit(f"ERROR: no top cell in {gds_path}")

# Strip hidden layers from every cell so they don't inflate the SVG viewBox.
hidden_spec = list(HIDDEN)
for cell in lib.cells:
    cell.filter(hidden_spec, remove=True)

tops[0].write_svg(
    out_path,
    scaling=20,
    precision=6,
    shape_style=style,
    background="#ffffff",
    pad="2%",
)
print(f"INFO: wrote {out_path}")
