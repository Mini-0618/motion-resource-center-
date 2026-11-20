// Shared by render.mjs and still.mjs: load tokens + script, enforce content/style decoupling,
// copy audio / evidence images into public/, pick a browser.
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));

export function prepare(args) {
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
    if (!fs.existsSync(src)) {
      console.warn(`[render] WARNING audio file not found: ${src} — rendering WITHOUT audio (make one with: python cvsd.py beat --out <file.wav> --bpm 100 --seconds 60)`);
      delete script.audio;
    } else {
      const name = 'audio_' + path.basename(src);
      fs.copyFileSync(src, path.join(pub, name));
      script.audio.public_name = name;
    }
  }

  // evidence images: copy into public/ (must be material you have the right to use)
  (script.segments || []).forEach((s, i) => {
    if (s.type === 'evidence' && s.image) {
      const src = path.resolve(path.dirname(args.script), s.image);
      if (!fs.existsSync(src)) { console.error(`[render] evidence image not found: ${src}`); process.exit(2); }
      const name = `evidence_${i}_${path.basename(src)}`;
      fs.copyFileSync(src, path.join(pub, name));
      s.image_public = name;
      if (!s.source) console.warn(`[render] WARNING segment ${i}: evidence without source — add "source" before publishing`);
    }
  });

  const browserCandidates = [args.browser, process.env.REMOTION_BROWSER, '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser'];
  const browserExecutable = browserCandidates.find((p) => p && fs.existsSync(p)) || null;

  return {tokens, script, browserExecutable, pub, here};
}
