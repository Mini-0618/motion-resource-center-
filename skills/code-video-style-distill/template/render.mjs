#!/usr/bin/env node
// Usage: node render.mjs --tokens style-tokens.json --script script.json --out out.mp4 [--concurrency 4] [--browser /usr/bin/google-chrome]
import {bundle} from '@remotion/bundler';
import {renderMedia, selectComposition} from '@remotion/renderer';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, arr) => (a.startsWith('--') ? [...acc, [a.slice(2), arr[i + 1]]] : acc), []),
);
if (!args.tokens || !args.script || !args.out) {
  console.error('usage: node render.mjs --tokens <style-tokens.json> --script <script.json> --out <out.mp4>');
  process.exit(2);
}
const tokens = JSON.parse(fs.readFileSync(args.tokens, 'utf8'));
const script = JSON.parse(fs.readFileSync(args.script, 'utf8'));

// Content / style decoupling (recipe discipline idea: JuneYaooo/capsule-cinema, Apache-2.0 — idea only):
// style-tokens.json = reusable METHOD (no topic text); script.json = this episode's CONTENT (no colours/fonts/motion).
const STYLE_KEYS = ['palette', 'typography', 'layout', 'motion', 'canvas', 'components_style'];
const leaked = STYLE_KEYS.filter((k) => k in script);
if (leaked.length) {
  console.error(`[render] script.json must not carry style keys (${leaked.join(', ')}). Put them in style-tokens.json or an overrides file.`);
  process.exit(2);
}
if ('segments' in tokens) {
  console.error('[render] style-tokens.json must not carry content (segments). Put topic content in script.json.');
  process.exit(2);
}

// optional audio: copy into public/ so staticFile() can serve it
const pub = path.join(here, 'public');
fs.mkdirSync(pub, {recursive: true});
if (script.audio?.src) {
  const src = path.resolve(path.dirname(args.script), script.audio.src);
  const name = 'audio_' + path.basename(src);
  fs.copyFileSync(src, path.join(pub, name));
  script.audio.public_name = name;
}

const browserCandidates = [args.browser, process.env.REMOTION_BROWSER, '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'];
const browserExecutable = browserCandidates.find((p) => p && fs.existsSync(p)) || null;

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
  onProgress: ({progress}) => {
    const p = Math.floor(progress * 10);
    if (p !== last) { last = p; process.stdout.write(`[render] ${p * 10}%\n`); }
  },
});
console.log(`[render] done -> ${path.resolve(args.out)}`);
