// Copies the packaged final image, entry.png beside this file, to <output dir>/entry.png.
// Node 22 standard library only. Run with Node's type stripping, for example:
//   node --experimental-strip-types main.ts            (Node 22.6+)
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node --experimental-strip-types main.ts
//
// Safety: the output directory is created only if missing and is never removed or
// replaced, so a mounted /output keeps its mount point and anything else in it.
// The PNG is written to a temporary file in the same directory and renamed into
// place, so the judge never sees a half-written entry.png.

import { copyFileSync, existsSync, mkdirSync, readFileSync, renameSync, rmSync, statSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024;
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const source = new URL('./entry.png', import.meta.url);
const outDir: string = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const target = join(outDir, 'entry.png');
const temp = join(outDir, `.entry.png.${process.pid}.tmp`);

const bytes = readFileSync(source);
if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
}
if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
  throw new Error('entry.png is not a PNG file');
}

// Create the directory only when it is missing; an existing or mounted one is used as is.
if (!existsSync(outDir)) {
  mkdirSync(outDir, { recursive: true });
}

try {
  copyFileSync(source, temp);
  if (statSync(temp).size !== bytes.length) {
    throw new Error('copy size mismatch');
  }
  renameSync(temp, target);
} catch (err) {
  if (existsSync(temp)) rmSync(temp, { force: true });
  throw err;
}

console.log(`wrote ${target} (${bytes.length} bytes)`);
