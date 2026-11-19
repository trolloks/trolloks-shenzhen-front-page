#!/usr/bin/env bash
# Runs the full local test set: conversion (twice), gate checks, and main.ts repeat runs.
# No network access is used. Usage: bash tests/run_tests.sh
set -euo pipefail
cd "$(dirname "$0")/.."
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "== 1. Conversion is reproducible (two runs, byte-identical)"
python3 -I scripts/make_entry.py /artwork/illustration.png "$TMP/a.png"
python3 -I scripts/make_entry.py /artwork/illustration.png "$TMP/b.png"
cmp "$TMP/a.png" "$TMP/b.png"
cmp "$TMP/a.png" entry.png && echo "committed entry.png matches conversion output"

echo "== 2. Gate checks on entry.png"
python3 -I tests/check_entry.py entry.png
file --mime-type entry.png | grep -q 'image/png'

echo "== 3. main.ts repeat runs into an existing output directory"
OUT="$TMP/output"
mkdir -p "$OUT"
echo keep > "$OUT/other.txt"
for i in 1 2 3; do
  MAKEFUN_OUTPUT_DIR="$OUT" node main.ts
  cmp "$OUT/entry.png" entry.png
done
test -f "$OUT/other.txt" && echo "unrelated files in output dir preserved"
python3 -I tests/check_entry.py "$OUT/entry.png"
ls -A "$OUT" | grep -q '\.tmp$' && { echo "leftover temp file"; exit 1; } || echo "no temp files left behind"

echo "== 4. main.ts creates a missing output directory"
MAKEFUN_OUTPUT_DIR="$TMP/new/nested" node main.ts
cmp "$TMP/new/nested/entry.png" entry.png

echo "ALL TESTS PASSED"
