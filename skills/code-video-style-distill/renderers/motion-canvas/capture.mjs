#!/usr/bin/env node
// Headless capture for the Motion Canvas backend (own code, MIT).
//   node capture.mjs video  --tokens t.json --script s.json --out out.mp4 [--workers 2]
//   node capture.mjs stills --tokens t.json --script s.json --times 1.0,2.5 --outdir dir   -> still_<i>.png
// Builds the scene with Vite once (dist/), serves it on 127.0.0.1, loads it in headless Chrome (playwright-core),
// seeks frame by frame through window.render(t) and pipes JPEG screenshots into ffmpeg (same frame-seek recording
// idea as Lemo-Opuscar core/render/video.mjs, MIT — rewritten here). Audio is muxed by scripts/renderers.py.
import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import {spawn, execFileSync} from 'node:child_process';
import {fileURLToPath} from 'node:url';
import {chromium} from 'playwright-core';

const here = path.dirname(fileURLToPath(import.meta.url));
const [kind, ...rest] = process.argv.slice(2);
const opt = (k, d) => { const i = rest.indexOf(k); return i >= 0 ? rest[i + 1] : d; };
if (!['video', 'stills'].includes(kind) || !opt('--tokens') || !opt('--script')) {
  console.error('usage: node capture.mjs video|stills --tokens t.json --script s.json (--out out.mp4 | --times a,b --outdir dir)'); process.exit(2);
}
const tokens = JSON.parse(fs.readFileSync(opt('--tokens'), 'utf8'));
const script = JSON.parse(fs.readFileSync(opt('--script'), 'utf8'));
for (const k of ['palette', 'typography', 'layout', 'motion', 'canvas', 'components_style']) if (k in script) { console.error(`[mc] script.json must not carry style key ${k}`); process.exit(2); }
if ('segments' in tokens) { console.error('[mc] style-tokens.json must not carry content (segments)'); process.exit(2); }
delete script.audio;

// build once (rebuild when sources are newer than dist)
const dist = path.join(here, 'dist');
const newest = (d) => fs.readdirSync(d, {withFileTypes: true}).reduce((m, e) => Math.max(m, e.isDirectory() ? newest(path.join(d, e.name)) : fs.statSync(path.join(d, e.name)).mtimeMs), 0);
if (!fs.existsSync(path.join(dist, 'index.html')) || newest(path.join(here, 'src')) > fs.statSync(path.join(dist, 'index.html')).mtimeMs) {
  console.log('[mc] vite build…');
  execFileSync(process.execPath, [path.join(here, 'node_modules', 'vite', 'bin', 'vite.js'), 'build'], {cwd: here, stdio: 'inherit'});
}
const TYPES = {'.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css', '.png': 'image/png', '.json': 'application/json'};
const server = http.createServer((req, res) => {
  const p = path.join(dist, decodeURIComponent(new URL(req.url, 'http://x').pathname));
  if (!p.startsWith(dist) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); res.end(); return; }
  res.writeHead(200, {'Content-Type': TYPES[path.extname(p)] || 'application/octet-stream'}); fs.createReadStream(p).pipe(res);
});
await new Promise((r) => server.listen(0, '127.0.0.1', r));
const url = `http://127.0.0.1:${server.address().port}/index.html`;
const exe = [process.env.PLAYWRIGHT_CHROME, '/usr/bin/google-chrome', '/usr/bin/chromium', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'].find((p) => p && fs.existsSync(p));
const W = tokens.canvas?.width || 1920, H = tokens.canvas?.height || 1080;

async function open() {
  const browser = await chromium.launch({executablePath: exe, args: ['--force-color-profile=srgb', '--font-render-hinting=none', '--disable-gpu-vsync']});
  const page = await browser.newPage({viewport: {width: W, height: H}, deviceScaleFactor: 1});
  page.on('pageerror', (e) => console.error('[mc] page error:', e.message));
  await page.addInitScript((cfg) => { window.CVSD = cfg; }, {tokens, script});
  await page.goto(url);
  await page.waitForFunction(() => window.READY === true || window.ERROR, null, {timeout: 180000});
  const err = await page.evaluate(() => window.ERROR || null);
  if (err) { console.error('[mc] ' + err.split('\n')[0]); await browser.close(); server.close(); process.exit(3); }
  return {browser, page};
}

if (kind === 'stills') {
  const times = opt('--times').split(',').map(Number), outdir = opt('--outdir');
  fs.mkdirSync(outdir, {recursive: true});
  const {browser, page} = await open();
  const frames = await page.evaluate(() => window.FRAMES);
  const fps = Math.round(tokens.canvas?.fps || 30);
  for (let i = 0; i < times.length; i++) {
    const t = Math.min(times[i], (frames - 1) / fps);
    await page.evaluate((t) => window.render(t), t);
    const o = path.resolve(outdir, `still_${i}.png`);
    await page.screenshot({path: o, type: 'png'});
    console.log(`[mc still] t=${times[i]}s -> ${o}`);
  }
  await browser.close(); server.close();
} else {
  const out = path.resolve(opt('--out')), WK = Math.max(1, Number(opt('--workers', 2)));
  const fps = Math.round(tokens.canvas?.fps || 30);
  const probe = await open(); const TOTAL = await probe.page.evaluate(() => window.FRAMES); await probe.browser.close();
  const tmp = fs.mkdtempSync(path.join(path.dirname(out), '.mc_segs-'));
  const per = Math.ceil(TOTAL / WK), t0 = Date.now();
  console.log(`[mc] ${W}x${H}@${fps} frames=${TOTAL} workers=${WK}`);
  await Promise.all([...Array(WK)].map(async (_, w) => {
    const a = w * per, b = Math.min(TOTAL, a + per); if (a >= b) return;
    const {browser, page} = await open();
    const ff = spawn('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'mjpeg', '-i', '-',
      '-c:v', 'libx264', '-preset', 'medium', '-crf', '14', '-pix_fmt', 'yuv420p', `seg_${w}.mp4`], {cwd: tmp, stdio: ['pipe', 'inherit', 'inherit']});
    const closed = new Promise((r) => ff.on('close', r));
    for (let f = a; f < b; f++) {
      await page.evaluate((t) => window.render(t), f / fps);
      const buf = await page.screenshot({type: 'jpeg', quality: 95});
      if (!ff.stdin.write(buf)) await new Promise((r) => ff.stdin.once('drain', r));
      if ((f - a) % 90 === 0) console.log(`[mc] w${w} ${f - a}/${b - a} ${((Date.now() - t0) / 1000).toFixed(0)}s`);
    }
    ff.stdin.end(); await closed; await browser.close();
  }));
  const list = [...Array(WK)].map((_, w) => `seg_${w}.mp4`).filter((f) => fs.existsSync(path.join(tmp, f)));
  fs.writeFileSync(path.join(tmp, 'list.txt'), list.map((f) => `file '${f}'`).join('\n'));
  execFileSync('ffmpeg', ['-y', '-loglevel', 'error', '-f', 'concat', '-safe', '0', '-i', 'list.txt', '-c', 'copy', out], {cwd: tmp});
  fs.rmSync(tmp, {recursive: true, force: true});
  server.close();
  console.log(`[mc] done -> ${out} (${((Date.now() - t0) / 1000).toFixed(1)}s)`);
}
