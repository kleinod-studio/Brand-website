#!/usr/bin/env python3
"""Builds the kleinod.studio brand assets (design direction "Fassung": a gem drawn as a line).

Run:  python3 build.py
Writes SVG files next to this script and PNG previews into preview/.
The wordmark text is converted to outlines (via Pango/Cairo), so the SVGs look the same
everywhere, without the font installed. Font: Adwaita Sans (SIL OFL), GNOME's UI font.
"""

import subprocess
from pathlib import Path

import gi

gi.require_version("Pango", "1.0")
gi.require_version("PangoCairo", "1.0")
import cairo  # noqa: E402
from gi.repository import Pango, PangoCairo  # noqa: E402

HERE = Path(__file__).resolve().parent
FONT = "Adwaita Sans"

# Palette: one violet as the signature, an ink for text, a lavender for quiet surfaces.
COLORS = {
    "light": {"mark": "#4B3F9E", "text": "#2A2550", "muted": "#6A6590"},
    "dark": {"mark": "#A99CF5", "text": "#F1EFFA", "muted": "#B9B4D8"},
}

# The gem, in a 64×64 grid: crown outline, girdle and facet lines. Stroke 4.5, round joins.
GEM_OUTLINE = [(8, 24), (20, 10), (44, 10), (56, 24), (32, 56)]
GEM_FACETS = [(20, 10), (26, 24), (32, 56), (38, 24), (44, 10)]
GEM_STROKE = 4.5


def text_path(text: str, size: float, weight: str = "Medium", letter_spacing: float = 0.0) -> tuple[str, float, float]:
    """SVG path data for a line of text, plus its width and its baseline offset (ascent)."""
    surface = cairo.RecordingSurface(cairo.CONTENT_COLOR_ALPHA, None)
    cr = cairo.Context(surface)
    layout = PangoCairo.create_layout(cr)
    layout.set_font_description(Pango.FontDescription.from_string(f"{FONT} {weight} {size}px"))
    if letter_spacing:
        attributes = Pango.AttrList()
        attributes.insert(Pango.attr_letter_spacing_new(int(letter_spacing * Pango.SCALE)))
        layout.set_attributes(attributes)
    layout.set_text(text, -1)
    PangoCairo.layout_path(cr, layout)
    parts = []
    for kind, points in cr.copy_path():
        if kind == cairo.PATH_MOVE_TO:
            parts.append("M%.2f %.2f" % points)
        elif kind == cairo.PATH_LINE_TO:
            parts.append("L%.2f %.2f" % points)
        elif kind == cairo.PATH_CURVE_TO:
            parts.append("C%.2f %.2f %.2f %.2f %.2f %.2f" % points)
        elif kind == cairo.PATH_CLOSE_PATH:
            parts.append("Z")
    ink, logical = layout.get_pixel_extents()
    baseline = layout.get_baseline() / Pango.SCALE
    # Remember the visible (ink) box: lockups centre on what you see, not on the line box.
    text_path.ink = (ink.y, ink.height)
    return " ".join(parts), logical.width - letter_spacing, baseline


def gem(x: float, y: float, scale: float, color: str) -> str:
    pts = lambda seq: " ".join(f"{x + px * scale:.2f},{y + py * scale:.2f}" for px, py in seq)  # noqa: E731
    sw = GEM_STROKE * scale
    return (
        f'<g fill="none" stroke="{color}" stroke-width="{sw:.2f}" stroke-linejoin="round" stroke-linecap="round">'
        f'<polygon points="{pts(GEM_OUTLINE)}"/>'
        f'<polyline points="{pts([(8, 24), (56, 24)])}"/>'
        f'<polyline points="{pts(GEM_FACETS)}"/></g>'
    )


def svg(width: float, height: float, body: str, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width:.0f}" height="{height:.0f}" '
        f'viewBox="0 0 {width:.0f} {height:.0f}" role="img" aria-label="{title}">\n{body}\n</svg>\n'
    )


def build_brand(mode: str) -> dict[str, str]:
    c = COLORS[mode]
    files = {}
    files["mark"] = svg(64, 64, gem(0, 0, 1, c["mark"]), "kleinod.studio")

    # Horizontal lockup: gem | kleinod.studio  (".studio" quieter)
    name, name_w, base = text_path("kleinod", 40)
    ink_top, ink_height = text_path.ink  # "kleinod" has the tallest letters (k, l, d)
    dot, dot_w, _ = text_path(".studio", 40, "Regular")
    height = 64
    # Optical centre of the gem, including the stroke: outline from y 10 to 56.
    gem_centre = (10 + 56) / 2
    text_top = gem_centre - (ink_top + ink_height / 2)
    body = gem(0, 0, 1, c["mark"])
    body += f'<path transform="translate(80 {text_top:.2f})" fill="{c["text"]}" d="{name}"/>'
    body += f'<path transform="translate({80 + name_w:.2f} {text_top:.2f})" fill="{c["muted"]}" d="{dot}"/>'
    files["logo-horizontal"] = svg(80 + name_w + dot_w + 4, height, body, "kleinod.studio")

    # Stacked lockup: gem above "kleinod", "STUDIO" letter-spaced below
    big, big_w, big_base = text_path("kleinod", 44)
    small, small_w, small_base = text_path("STUDIO", 15, "Medium", letter_spacing=5)
    width = max(big_w, small_w, 96) + 16
    body = gem((width - 96) / 2, 0, 1.5, c["mark"])
    body += f'<path transform="translate({(width - big_w) / 2:.2f} 96)" fill="{c["text"]}" d="{big}"/>'
    body += f'<path transform="translate({(width - small_w) / 2:.2f} {96 + big_base + 10:.2f})" fill="{c["muted"]}" d="{small}"/>'
    files["logo-stacked"] = svg(width, 96 + big_base + 10 + small_base + 8, body, "kleinod.studio")
    return files


# --- App icons ---------------------------------------------------------------------
# Every kleinod.studio app icon: its own object, drawn in the GNOME style (front face plus a
# slightly darker base), and the gem as a filled seal at the bottom right. The seal is the
# family signature; size, position and colours stay the same across apps.

SEAL = """<g transform="translate({x} {y}) scale({s})">
  <polygon points="8,24 20,10 44,10 56,24 32,56" fill="#4B3F9E" stroke="#FFFFFF" stroke-width="5" stroke-linejoin="round"/>
  <polygon points="20,10 44,10 38,24 26,24" fill="#6D60C7"/>
  <polygon points="8,24 20,10 26,24" fill="#5A4DB3"/>
  <polygon points="56,24 44,10 38,24" fill="#5A4DB3"/>
  <polygon points="26,24 38,24 32,56" fill="#3B3083"/>
</g>"""


def typecase_icon() -> str:
    """Typecase: a sheet of text, a second sheet behind it (the library), and the seal."""
    body = """
  <!-- back sheet -->
  <rect x="34" y="12" width="70" height="92" rx="7" fill="#C9C4E6"/>
  <rect x="35" y="11" width="68" height="88" rx="6" fill="#E6E3F5" stroke="#C9C4E6" stroke-width="2"/>
  <!-- front sheet: base, then face -->
  <rect x="22" y="22" width="72" height="94" rx="7" fill="#B6B0DA"/>
  <rect x="23" y="19" width="70" height="92" rx="6" fill="#FFFFFF" stroke="#CFCAE8" stroke-width="2"/>
  <!-- heading and lines of text -->
  <rect x="33" y="32" width="40" height="7" rx="3.5" fill="#2A2550"/>
  <rect x="33" y="48" width="50" height="4" rx="2" fill="#9A95BF"/>
  <rect x="33" y="58" width="46" height="4" rx="2" fill="#9A95BF"/>
  <rect x="33" y="68" width="50" height="4" rx="2" fill="#9A95BF"/>
  <rect x="33" y="78" width="30" height="4" rx="2" fill="#9A95BF"/>
  <!-- caret -->
  <rect x="66" y="75" width="3" height="10" rx="1.5" fill="#4B3F9E"/>
""" + SEAL.format(x=72, y=78, s=0.75)
    return svg(128, 128, body, "Typecase")


def typecase_symbolic() -> str:
    """16×16 single-colour variant (GNOME symbolic icons: filled shapes, one colour)."""
    body = """<g fill="#2e3436">
  <path d="M4 1h8a2 2 0 0 1 2 2v6.5h-1.5V3a.5.5 0 0 0-.5-.5H4a.5.5 0 0 0-.5.5v10c0 .28.22.5.5.5h4.5V15H4a2 2 0 0 1-2-2V3a2 2 0 0 1 2-2z"/>
  <rect x="5" y="4.5" width="5" height="1.5" rx=".75"/>
  <rect x="5" y="7.5" width="6" height="1.2" rx=".6"/>
  <rect x="5" y="10" width="3.5" height="1.2" rx=".6"/>
  <path d="M10.6 11h3.8l1.1 1.3-3 3.7-3-3.7z"/>
</g>"""
    return svg(16, 16, body, "Typecase")


def main():
    out = {}
    for mode in ("light", "dark"):
        for name, content in build_brand(mode).items():
            out[f"kleinod-studio-{name}{'' if mode == 'light' else '-dark'}.svg"] = content
    out["apps/studio.kleinod.Typecase.svg"] = typecase_icon()
    out["apps/studio.kleinod.Typecase-symbolic.svg"] = typecase_symbolic()
    for name, content in out.items():
        path = HERE / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    preview = HERE / "preview"
    preview.mkdir(exist_ok=True)
    for name in out:
        target = preview / (Path(name).stem + ".png")
        size = ["-w", "512"] if "symbolic" not in name else ["-w", "128"]
        subprocess.run(["rsvg-convert", *size, "-o", str(target), str(HERE / name)], check=True)
    print("\n".join(sorted(out)))


if __name__ == "__main__":
    main()
