"""Render a sky130A GDS to PNG via KLayout (headless), using layer colors
from ``tech/cic/sky130A.tech``.

Invoked as:
    klayout -b -r render_gds.py -rd gds=path/in.gds -rd png=path/out.png \
            [-rd tech=path/sky130A.tech] [-rd w=1600] [-rd h=900]

Magic's ``plot pnm`` cannot render layer geometry in ``-dnull`` mode, and the
X11 ``-d XR`` driver fails on this macOS build, so we use KLayout for the
rendering. Colors are pulled from the same tech file ciccreator uses, to keep
schematic/layout/preview visuals consistent.
"""
import json
import os
import pya  # type: ignore  # provided by KLayout

# ---------- script args ----------
gds = globals().get("gds")
png = globals().get("png")
if not gds or not png:
    raise SystemExit("ERROR: -rd gds=... and -rd png=... are required")

tech_path = globals().get("tech")
if not tech_path:
    # Default: ../cic/sky130A.tech relative to this script.
    here = os.path.dirname(os.path.abspath(__file__))
    candidate = os.path.normpath(os.path.join(here, "..", "cic", "sky130A.tech"))
    if os.path.exists(candidate):
        tech_path = candidate

width = int(globals().get("w", 1600))
height = int(globals().get("h", 900))

# ---------- color helpers ----------
# Named colors used in sky130A.tech, mapped to 0xRRGGBB.
NAMED_COLORS = {
    "red": 0xCC2222, "green": 0x22AA22, "blue": 0x3355CC,
    "yellow": 0xDDCC22, "cyan": 0x33CCDD, "aqua": 0x33CCDD,
    "pink": 0xDD88AA, "brown": 0x8B5A2B, "darkgreen": 0x006400,
    "goldenrod": 0xDAA520, "purple": 0x8844AA, "orange": 0xDD7722,
    "magenta": 0xCC33CC, "white": 0xFFFFFF, "black": 0x000000,
    "gray": 0x888888, "grey": 0x888888,
}


def to_rgb(name):
    if not name:
        return 0x888888
    if name.startswith("#") and len(name) == 7:
        return int(name[1:], 16)
    return NAMED_COLORS.get(name.lower(), 0x888888)


# ---------- sky130A alias -> (GDS layer, datatype) ----------
# The `number` field in sky130A.tech is the Magic internal layer number, not
# the GDS pair. We translate the tech file's `alias` to the canonical sky130A
# GDS coordinates. Source: SkyWater 130nm PDK layer table.
ALIAS_TO_GDS = {
    "nwell":   (64, 20),
    "pwell":   (64, 44),
    "diff":    (65, 20),
    "ndiff":   (65, 20),
    "pdiff":   (65, 20),
    "ntap":    (65, 44),
    "ptap":    (65, 44),
    "ndcontact": (66, 44),
    "pdcontact": (66, 44),
    "ptapc":   (66, 44),
    "ntapc":   (66, 44),
    "polycontact": (66, 44),
    "pcontact":(66, 44),
    "xpolycontact": (66, 44),
    "xpolyres":(66, 13),
    "ppolyres":(66, 13),
    "poly":    (66, 20),
    "licon1":  (66, 44),
    "locali":  (67, 20),
    "li":      (67, 20),
    "li1":     (67, 20),
    "viali":   (67, 44),
    "metal1":  (68, 20),
    "met1":    (68, 20),
    "via1":    (68, 44),
    "metal2":  (69, 20),
    "met2":    (69, 20),
    "via2":    (69, 44),
    "metal3":  (70, 20),
    "met3":    (70, 20),
    "via3":    (70, 44),
    "metal4":  (71, 20),
    "met4":    (71, 20),
    "via4":    (71, 44),
    "metal5":  (72, 20),
    "met5":    (72, 20),
    "mimcap":  (89, 44),
    "nmoslvt": (125, 44),
    "pmoslvt": (125, 44),
}


# ---------- parse tech file ----------
gds_color = {}     # (layer, datatype) -> (rgb, filled)
hidden = {(235, 4), (235, 0), (235, 5), (0, 20)}  # PR / area-ID

if tech_path and os.path.exists(tech_path):
    with open(tech_path) as f:
        tech = json.load(f)
    for _, props in (tech.get("layers") or {}).items():
        alias = (props.get("alias") or "").strip().lower()
        color = props.get("color")
        fill = props.get("fill", "fill")
        if not alias or not color:
            continue
        pair = ALIAS_TO_GDS.get(alias)
        if pair is None:
            continue
        # Don't overwrite a more-specific datatype entry with a -1 default.
        if pair not in gds_color:
            gds_color[pair] = (to_rgb(color), fill != "nofill")

# ---------- read layout ----------
layout = pya.Layout()
layout.read(gds)
top = layout.top_cell()

# ---------- build layer view from tech colors ----------
view = pya.LayoutView()
view.show_layout(layout, False)

# White background, no grid.
view.set_config("background-color", "#ffffff")
view.set_config("grid-visible", "false")
view.set_config("grid-show-axes", "false")
view.set_config("grid-show-ruler", "false")

# Replace the auto-built layer list with one driven by sky130A.tech.
view.clear_layers()

for li in layout.layer_indexes():
    info = layout.get_info(li)
    num, dt = info.layer, info.datatype
    if (num, dt) in hidden:
        continue
    color_fill = gds_color.get((num, dt))
    if color_fill is None:
        continue  # layer not in tech file; omit from rendering
    rgb, filled = color_fill

    node = pya.LayerPropertiesNode()
    node.source_layer = num
    node.source_datatype = dt
    node.source_cellview = 0
    node.name = info.name or f"{num}/{dt}"
    node.frame_color = rgb
    node.fill_color = rgb
    node.dither_pattern = 0 if filled else 1   # 0=solid, 1=hollow
    node.transparent = not filled
    node.visible = True
    view.insert_layer(view.end_layers(), node)

# ---------- frame to the visible geometry ----------
view.max_hier()

visible_bbox = pya.Box()
it = view.begin_layers()
while not it.at_end():
    node = it.current()
    if node.visible:
        li = layout.layer(node.source_layer, node.source_datatype)
        if li is not None and li >= 0:
            try:
                visible_bbox += top.bbox_per_layer(li)
            except Exception:
                pass
    it.next()

if not visible_bbox.empty():
    pad_x = max(1, visible_bbox.width() // 20)
    pad_y = max(1, visible_bbox.height() // 20)
    visible_bbox = visible_bbox.enlarged(pad_x, pad_y)
    dbu = layout.dbu
    view.zoom_box(pya.DBox(
        visible_bbox.left * dbu, visible_bbox.bottom * dbu,
        visible_bbox.right * dbu, visible_bbox.top * dbu,
    ))
else:
    view.zoom_fit()

view.save_image(png, width, height)
print(f"INFO: wrote {png}")
