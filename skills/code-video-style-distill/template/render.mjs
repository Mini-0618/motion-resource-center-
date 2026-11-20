#!/usr/bin/env node
// Usage: node render.mjs --tokens style-tokens.json --script script.json --out out.mp4 [--concurrency 4] [--browser /usr/bin/google-chrome]
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
import {prepare} from './prepare.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, arr) => (a.startsWith('--') ? [...acc, [a.slice(2), arr[i + 1]]] : acc), []),
);
if (!args.tokens || !args.script || !args.out) {
  console.error('usage: node render.mjs --tokens <style-tokens.json> --script <script.json> --out <out.mp4>');
  process.exit(2);
}
const {tokens, script, browserExecutable, pub} = prepare(args);

const inputProps = {tokens, script};
console.log('[render] bundling…');
const serveUrl = await bundle({entryPoint: path.join(here, 'src/index.ts'), publicDir: pub});
const composition = await selectComposition({serveUrl, id: 'Main', inputProps, browserExecutable});
console.log(`[render] ${composition.width}x${composition.height}@${composition.fps} frames=${composition.durationInFrames} browser=${browserExecutable || 'remotion-default'}`);
let last = -1;
await renderMedia({
  composition,
  serveUrl,
  codec: 'h264',
  outputLocation: path.resolve(args.out),
  inputProps,
  browserExecutable,
  concurrency: Number(args.concurrency || 4),
  chromiumOptions: {gl: 'swangle'},
  // fresh timestamp in the container metadata: every render is a distinct file (compare.py ledger dedups by sha256)
  metadata: {comment: `code-video-style-distill render ${new Date().toISOString()}`},
  onProgress: ({progress}) => {
    const p = Math.floor(progress * 10);
    if (p !== last) { last = p; process.stdout.write(`[render] ${p * 10}%\n`); }
  },
});
console.log(`[render] done -> ${path.resolve(args.out)}`);
