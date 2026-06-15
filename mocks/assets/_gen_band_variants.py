#!/usr/bin/env python3
"""Recolor the creature's BAND (the tan/beige sash wrap) into per-agent band colors.
Body stays GREEN for every variant; only the band hue changes.
Source: creature-sprite-px.png (48x48 RGBA). Outputs creature-band-<name>.png."""
import colorsys
from PIL import Image

SRC = "creature-sprite-px.png"
im = Image.open(SRC).convert("RGBA")
W, H = im.size
px = im.load()

def is_band(r, g, b):
    # The band is warm tan/beige: R>=G>B, low saturation-ish, mid-high lightness,
    # and NOT green (green body has G clearly > R). Exclude the pale cream face
    # (very light, near-white) and dark eyes.
    if g > r + 8:            # green body
        return False
    mx, mn = max(r, g, b), min(r, g, b)
    if mx < 70:              # dark (eyes / outline)
        return False
    # tan band: r>=g>=b, reddish-warm, and not extremely pale (face is ~ (213,242,196) greenish-cream)
    if r >= g - 4 and g >= b and (r - b) >= 12 and b < 200:
        # face cream tends to be greenish (g>=r); band is r>=g. Already excluded g>r above.
        return True
    return False

# Per-agent band target hues (H in degrees) + sat/val multipliers for a crafted look.
VARIANTS = {
    "blue":   210,
    "pink":   330,
    "amber":   38,
    "teal":   175,
    "violet": 268,
}

# Precompute the band's average luminance so we can map shading consistently.
band_pixels = [(x, y) for y in range(H) for x in range(W)
               if px[x, y][3] > 30 and is_band(*px[x, y][:3])]
print("band pixels:", len(band_pixels))

for name, hue in VARIANTS.items():
    out = im.copy()
    o = out.load()
    for (x, y) in band_pixels:
        r, g, b, a = px[x, y]
        # use source luminance as value, give the band a rich but readable sat
        _, l, _ = colorsys.rgb_to_hls(r/255, g/255, b/255)
        # lift contrast a touch so the band ramps read as crafted shading
        l = min(1.0, max(0.0, (l - 0.5) * 1.18 + 0.5))
        sat = 0.62
        # amber a bit warmer/less saturated to stay cozy; teal/blue slightly deeper
        if name == "amber":
            sat = 0.72; l = min(1.0, l*0.98 + 0.04)
        nr, ng, nb = colorsys.hls_to_rgb(hue/360.0, l, sat)
        o[x, y] = (int(nr*255), int(ng*255), int(nb*255), a)
    out.save(f"creature-band-{name}.png")
    print("wrote", f"creature-band-{name}.png")
