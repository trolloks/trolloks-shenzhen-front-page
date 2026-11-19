#!/usr/bin/env python3
"""Checks entry.png against the competition gate: PNG type, <=1024 px, <=1 MiB, whole file.

Usage: python3 -I tests/check_entry.py <file.png>
"""
import struct
import sys
import zlib

from PIL import Image

MAX_SIDE = 1024
MAX_BYTES = 1024 * 1024
SIG = b"\x89PNG\r\n\x1a\n"


def check_chunks(data):
    """Walk every chunk, verify each CRC, and require IEND as the last chunk."""
    pos = 8
    seen = []
    while pos < len(data):
        (length,) = struct.unpack(">I", data[pos:pos + 4])
        ctype = data[pos + 4:pos + 8]
        body = data[pos + 8:pos + 8 + length]
        crc = struct.unpack(">I", data[pos + 8 + length:pos + 12 + length])[0]
        if zlib.crc32(ctype + body) & 0xFFFFFFFF != crc:
            raise AssertionError(f"bad CRC in chunk {ctype!r}")
        seen.append(ctype)
        pos += 12 + length
        if ctype == b"IEND":
            break
    if not seen or seen[0] != b"IHDR" or seen[-1] != b"IEND" or pos != len(data):
        raise AssertionError("PNG is not a whole file (missing IHDR/IEND or trailing bytes)")
    return seen


def main(path):
    with open(path, "rb") as f:
        data = f.read()
    assert data[:8] == SIG, "not a PNG (signature mismatch)"
    chunks = check_chunks(data)
    with Image.open(path) as im:
        assert im.format == "PNG", f"format is {im.format}"
        im.load()
        w, h = im.size
    assert w <= MAX_SIDE and h <= MAX_SIDE, f"dimensions {w}x{h} exceed {MAX_SIDE}"
    assert len(data) <= MAX_BYTES, f"{len(data)} bytes exceeds 1 MiB"
    print(f"OK {path}: PNG, {w}x{h}, {len(data)} bytes ({len(data) / MAX_BYTES:.1%} of 1 MiB), chunks={len(chunks)}")


if __name__ == "__main__":
    main(sys.argv[1])
