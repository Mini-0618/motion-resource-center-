#!/usr/bin/env node
// Render single frames only (no video) — used by scripts/stillcheck.py.
// Usage: node still.mjs --tokens t.json --script s.json --times 3.1,9.4,15.2 --outdir dir
import {bundle} from '@remotion/bundler';
import {renderStill, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {prepare} from './prepare.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(process.argv.slice(2).reduce((acc, a, i, arr) => (a.startsWith('--') ? [...acc, [a.slice(2), arr[i + 1]]] : acc), []));
if (!args.tokens || !args.script || !args.times || !args.outdir) {
  console.error('usage: node still.mjs --tokens <t.json> --script <s.json> --times 1.0,2.0 --outdir <dir>');
  process.exit(2);
}
const {tokens, script, browserExecutable, pub} = prepare(args);
const inputProps = {tokens, script};
fs.mkdirSync(args.outdir, {recursive: true});
const serveUrl = await bundle({entryPoint: path.join(here, 'src/index.ts'), publicDir: pub});
const composition = await selectComposition({serveUrl, id: 'Main', inputProps, browserExecutable});
const times = args.times.split(',').map(Number);
for (let i = 0; i < times.length; i++) {
  const frame = Math.min(composition.durationInFrames - 1, Math.max(0, Math.round(times[i] * composition.fps)));
  const out = path.resolve(args.outdir, `still_${i}.png`);
  await renderStill({composition, serveUrl, output: out, frame, inputProps, browserExecutable, chromiumOptions: {gl: 'swangle'}});
  console.log(`[still] t=${times[i]}s frame=${frame} -> ${out}`);
}
