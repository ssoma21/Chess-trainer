#!/usr/bin/env python3
"""Generate app icons into dist/icons/ (needs Pillow and the DejaVu Sans font)."""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "dist", "icons"); os.makedirs(OUT, exist_ok=True)
FONT = next(p for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", "C:/Windows/Fonts/seguisym.ttf"] if os.path.exists(p))
def draw(size, pad, rounded):
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0) if rounded else (38, 37, 34, 255)); d = ImageDraw.Draw(im)
    if rounded: d.rounded_rectangle((0, 0, size - 1, size - 1), radius=size * .21, fill=(38, 37, 34, 255))
    d.rounded_rectangle((size * pad, size * pad, size - size * pad - 1, size - size * pad - 1), radius=size * .16, fill=(119, 149, 86, 255))
    f = ImageFont.truetype(FONT, int(size * .62)); t = "\u265e"; b = d.textbbox((0, 0), t, font=f)
    d.text(((size - (b[2] - b[0])) / 2 - b[0], (size - (b[3] - b[1])) / 2 - b[1]), t, font=f, fill=(255, 255, 255, 255))
    return im
draw(192, .06, True).save(os.path.join(OUT, "icon-192-rounded.png"))
draw(180, 0, False).convert("RGB").save(os.path.join(OUT, "icon-180.png"))
draw(192, .08, False).convert("RGB").save(os.path.join(OUT, "icon-192.png"))
draw(512, .08, False).convert("RGB").save(os.path.join(OUT, "icon-512.png"))
draw(256, .06, True).save(os.path.join(OUT, "icon.ico"), sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])
print("icons written to", OUT)
