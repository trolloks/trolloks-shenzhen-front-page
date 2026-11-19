// Copies the packaged final image, entry.png beside this file, to <output dir>/entry.png.
// Node 22 standard library only. Run with Node's type stripping, for example:
//   node --experimental-strip-types main.ts            (Node 22.6+)
// Outside the grader's container, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node --experimental-strip-types main.ts
//
// Validation: the file is read once. Its PNG signature, the first chunk (IHDR, length 13,
// with a correct CRC) and both canvas dimensions (1 to 1024 pixels) are checked before
// anything is written. The validated bytes are then written, not the path, so a change
// to the source after validation cannot reach the output.
//
// Safety: the output directory is created only if missing and is never removed or
// replaced, so a mounted /output keeps its mount point and anything else in it.
// The bytes go to a temporary file in the same directory and are renamed into place,
// so the judge never sees a half-written entry.png.

import { existsSync, mkdirSync, readFileSync, renameSync, rmSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';
import { crc32 } from 'node:zlib';

const MAX_BYTES = 1024 * 1024;
const MAX_SIDE = 1024;
const PNG_SIGNATURE = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
// Signature (8) + IHDR length (4) + type (4) + IHDR data (13) + CRC (4).
const IHDR_END = 8 + 4 + 4 + 13 + 4;

export function validatePngHeader(bytes: Buffer): { width: number; height: number } {
  if (bytes.length > MAX_BYTES) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB limit`);
  }
  if (bytes.length < IHDR_END) {
    throw new Error(`entry.png is truncated: ${bytes.length} bytes, header needs ${IHDR_END}`);
  }
  if (!bytes.subarray(0, 8).equals(PNG_SIGNATURE)) {
    throw new Error('entry.png is not a PNG file (signature mismatch)');
  }
  const chunkLength = bytes.readUInt32BE(8);
  if (chunkLength !== 13) {
    throw new Error(`first chunk length is ${chunkLength}, expected 13`);
  }
  if (bytes.subarray(12, 16).toString('latin1') !== 'IHDR') {
    throw new Error('first chunk is not IHDR');
  }
  const storedCrc = bytes.readUInt32BE(29);
  if (crc32(bytes.subarray(12, 29)) !== storedCrc) {
    throw new Error('IHDR CRC mismatch');
  }
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  if (width === 0 || height === 0) {
    throw new Error(`zero dimension: ${width}x${height}`);
  }
  if (width > MAX_SIDE || height > MAX_SIDE) {
    throw new Error(`dimensions ${width}x${height} exceed ${MAX_SIDE}x${MAX_SIDE}`);
  }
  return { width, height };
}

function main(): void {
  const source = new URL('./entry.png', import.meta.url);
  const outDir: string = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
  const target = join(outDir, 'entry.png');
  const temp = join(outDir, `.entry.png.${process.pid}.tmp`);

  // Read and validate once, before the output directory is touched.
  const bytes = readFileSync(source);
  const { width, height } = validatePngHeader(bytes);

  // Create the directory only when it is missing; an existing or mounted one is used as is.
  if (!existsSync(outDir)) {
    mkdirSync(outDir, { recursive: true });
  }

  try {
    // Write the validated buffer itself; 'wx' refuses to overwrite a leftover temp file.
    writeFileSync(temp, bytes, { flag: 'wx' });
    renameSync(temp, target);
  } catch (err) {
    if (existsSync(temp)) rmSync(temp, { force: true });
    throw err;
  }

  console.log(`wrote ${target} (${bytes.length} bytes, ${width}x${height})`);
}

main();
