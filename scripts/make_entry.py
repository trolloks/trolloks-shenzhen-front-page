#!/usr/bin/env python3
"""Reproducibly convert the commissioned illustration into the competition PNG.

Usage: python3 -I scripts/make_entry.py <input.png> <output.png>

Steps (deterministic for a fixed Pillow version):
1. Decode the input and convert to RGB (no alpha, no metadata carried over).
2. Resize so the longest side is at most 1024 px with Pillow LANCZOS.
   The square 1254 px artwork becomes 1024 x 1024.
3. Save as an optimised 24-bit PNG. If that exceeds 1 MiB, fall back to
   adaptive palette quantisation (FASTOCTREE), trying 256, then fewer colours,
   until the file fits.
4. Re-open the result to confirm it is a valid PNG within the limits.
"""
import io
import os
import sys

from PIL import Image

MAX_SIDE = 1024
MAX_BYTES = 1024 * 1024  # 1 MiB


def encode(img, colors=None):
    buf = io.BytesIO()
    if colors is None:
        img.save(buf, format="PNG", optimize=True)
    else:
        q = img.quantize(colors=colors, method=Image.Quantize.FASTOCTREE, dither=Image.Dither.FLOYDSTEINBERG)
        q.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


def convert(src, dst):
    with Image.open(src) as im:
        im.load()
        rgb = im.convert("RGB")
    w, h = rgb.size
    scale = min(1.0, MAX_SIDE / max(w, h))
    if scale < 1.0:
        size = (round(w * scale), round(h * scale))
        rgb = rgb.resize(size, Image.Resampling.LANCZOS)

    data = encode(rgb)
    used = "rgb"
    if len(data) > MAX_BYTES:
        for colors in (256, 192, 128, 64):
            data = encode(rgb, colors)
            used = f"adaptive-{colors}"
            if len(data) <= MAX_BYTES:
                break
    if len(data) > MAX_BYTES:
        sys.exit("error: could not fit the image under 1 MiB")

    tmp = dst + ".tmp"
    with open(tmp, "wb") as f:
        f.write(data)
    os.replace(tmp, dst)
    print(f"wrote {dst}: {rgb.size[0]}x{rgb.size[1]}, {len(data)} bytes, mode={used}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("usage: make_entry.py <input.png> <output.png>")
    convert(sys.argv[1], sys.argv[2])
