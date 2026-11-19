#!/usr/bin/env python3
"""Writes malformed variants of a PNG into a directory, for negative tests.

Usage: python3 -I tests/make_bad_headers.py <valid.png> <out_dir>
"""
import os
import struct
import sys
import zlib


def chunk(ctype, body):
    return struct.pack(">I", len(body)) + ctype + body + struct.pack(">I", zlib.crc32(ctype + body) & 0xFFFFFFFF)


def main(src, out):
    os.makedirs(out, exist_ok=True)
    data = open(src, "rb").read()
    ihdr = data[8:33]  # full valid IHDR chunk
    body = bytearray(ihdr[8:21])  # 13 bytes of IHDR data

    def write(name, blob):
        with open(os.path.join(out, name + ".png"), "wb") as f:
            f.write(blob)

    write("signature_only", data[:8])
    write("truncated_header", data[:20])
    write("first_chunk_not_ihdr", data[:12] + b"IDAT" + data[16:])
    bad_len = bytearray(data); bad_len[8:12] = struct.pack(">I", 12)
    write("ihdr_length_12", bytes(bad_len))
    write("width_zero", data[:8] + chunk(b"IHDR", struct.pack(">II", 0, 1024) + bytes(body[8:])) + data[33:])
    write("width_1025", data[:8] + chunk(b"IHDR", struct.pack(">II", 1025, 1024) + bytes(body[8:])) + data[33:])
    write("height_2048", data[:8] + chunk(b"IHDR", struct.pack(">II", 1024, 2048) + bytes(body[8:])) + data[33:])
    crc_bad = bytearray(data); crc_bad[16] ^= 0x01
    write("ihdr_crc_mismatch", bytes(crc_bad))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
