// Shared maths/tokens for the Motion Canvas backend — same semantics as template/src (Remotion) and renderers/html/runtime.js.
export const D: any = {
  canvas: {width: 1920, height: 1080, fps: 30},
  palette: {bg: '#0B0F17', surface: '#151B26', primary: '#4F8CFF', accent: '#FFB224', text: '#F2F5FA', text_muted: '#8A94A6', extra: ['#3DDC97', '#FF5C7A']},
  typography: {families: {display: {css: '"Inter", "Noto Sans CJK SC", "Source Han Sans SC", sans-serif'}, body: {css: '"Inter", "Noto Sans CJK SC", "Source Han Sans SC", sans-serif'}, mono: {css: '"JetBrains Mono", "Noto Sans Mono CJK SC", monospace'}},
    scale_px: {display: 120, h1: 72, h2: 52, body: 40, caption: 32, code: 30}, weights: {display: 800, h1: 700, body: 500}, letter_spacing_em: -0.01, line_height: 1.35},
  layout: {margins_pct: {left: 8, right: 8, top: 10, bottom: 10}, alignment: 'left', radius_px: 16, decor: {grid_lines: false, glow: true, noise: false}},
  motion: {durations_s: {fast: 0.25, base: 0.5, slow: 0.9}, easing: {enter: {cubic_bezier: [0.16, 1, 0.3, 1]}, exit: {cubic_bezier: [0.7, 0, 0.84, 0]}, emphasis: {cubic_bezier: [0.34, 1.56, 0.64, 1]}},
    spring: {damping: 14, stiffness: 120, mass: 1}, enter_style: 'slide-up', enter_distance_px: 40, stagger_s: 0.12, transition: {type: 'wipe', duration_s: 0.5}, typing_cps: 28},
  components_style: {subtitle: {position: 'bottom', bg_opacity: 0.6}, progress_bar: true},
};
const isObj = (x: any) => typeof x === 'object' && x !== null && !Array.isArray(x);
export function deepMerge(a: any, b: any): any {
  if (Array.isArray(a) || Array.isArray(b)) return b ?? a;
  if (!isObj(a)) return b ?? a;
  const o: any = {...a};
  for (const k of Object.keys(b || {})) o[k] = isObj(b[k]) ? deepMerge(a[k] ?? {}, b[k]) : (b[k] ?? a[k]);
  return o;
}
export function cubicBezier(arr?: number[]) {
  const [x1, y1, x2, y2] = arr && arr.length === 4 ? arr : [0.16, 1, 0.3, 1];
  const A = (a: number, b: number) => 1 - 3 * b + 3 * a, B = (a: number, b: number) => 3 * b - 6 * a, C = (a: number) => 3 * a;
  const calc = (t: number, a: number, b: number) => ((A(a, b) * t + B(a, b)) * t + C(a)) * t;
  const slope = (t: number, a: number, b: number) => 3 * A(a, b) * t * t + 2 * B(a, b) * t + C(a);
  const solve = (x: number) => {
    let t = x;
    for (let i = 0; i < 8; i++) { const s = slope(t, x1, x2); if (Math.abs(s) < 1e-6) break; t -= (calc(t, x1, x2) - x) / s; }
    if (t < 0 || t > 1 || Math.abs(calc(t, x1, x2) - x) > 1e-5) { let lo = 0, hi = 1; t = x; for (let i = 0; i < 40; i++) { const v = calc(t, x1, x2); if (Math.abs(v - x) < 1e-7) break; if (v < x) lo = t; else hi = t; t = (lo + hi) / 2; } }
    return t;
  };
  return (x: number) => (x <= 0 ? 0 : x >= 1 ? 1 : calc(solve(x), y1, y2));
}
export const clamp01 = (x: number) => Math.min(1, Math.max(0, x));
export const prog = (f: number, a: number, b: number, ease?: (x: number) => number) => { const x = b === a ? (f >= b ? 1 : 0) : clamp01((f - a) / (b - a)); return ease ? ease(x) : x; };
export function spring(frame: number, fps: number, cfg: any) {
  if (frame <= 0) return 0;
  const t = frame / fps, m = cfg.mass || 1, k = cfg.stiffness || 100, c = cfg.damping || 10;
  const w0 = Math.sqrt(k / m), z = c / (2 * Math.sqrt(k * m));
  if (z < 1) { const w1 = w0 * Math.sqrt(1 - z * z); return 1 - Math.exp(-z * w0 * t) * (Math.cos(w1 * t) + (z * w0 / w1) * Math.sin(w1 * t)); }
  if (z === 1) return 1 - Math.exp(-w0 * t) * (1 + w0 * t);
  const r1 = -w0 * (z - Math.sqrt(z * z - 1)), r2 = -w0 * (z + Math.sqrt(z * z - 1));
  return 1 - (r2 * Math.exp(r1 * t) - r1 * Math.exp(r2 * t)) / (r2 - r1);
}
export function hexA(hex: string, a: number) { const x = (hex || '#000000').replace('#', ''); return `rgba(${parseInt(x.slice(0, 2), 16)},${parseInt(x.slice(2, 4), 16)},${parseInt(x.slice(4, 6), 16)},${a})`; }
export function parseHighlight(s: string) { return String(s ?? '').split(/(\*\*[^*]+\*\*)/g).filter(Boolean).map((p) => (p.startsWith('**') ? {t: p.slice(2, -2), hi: true} : {t: p, hi: false})); }
function lum(hex: string) { const x = (hex || '#000000').replace('#', ''); const c = [0, 2, 4].map((i) => parseInt(x.slice(i, i + 2), 16) / 255).map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4)); return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]; }
export function textOn(surface: string, P: any) { const lt = lum(P.text), ls = lum(surface); const r = (Math.max(lt, ls) + 0.05) / (Math.min(lt, ls) + 0.05); return r >= 4.5 ? P.text : ls < 0.3 ? '#F2F5FA' : '#15171C'; }
const PUNCT = '，。、；：！？,.;:!?';
const LAT = /[A-Za-z0-9_]/;
export const countChars = (s: string) => [...s.replace(/\*\*/g, '')].filter((c) => c.trim() !== '').length;
export function splitCaption(text: string, max = 18): string[] {
  const chars: {c: string; hi: boolean}[] = []; parseHighlight(text).forEach((p) => [...p.t].forEach((c) => chars.push({c, hi: p.hi})));
  const out: any[] = []; let cur: any[] = []; const n = (a: any[]) => a.filter((x) => x.c.trim() !== '').length;
  for (let i = 0; i < chars.length; i++) {
    cur.push(chars[i]);
    if (PUNCT.includes(chars[i].c) && n(cur) >= Math.min(8, max)) { out.push(cur); cur = []; continue; }
    if (n(cur) >= max) {
      let cut = cur.length;
      for (let k = cur.length - 1; k > 0; k--) { const a = cur[k - 1].c, b = cur[k].c; if (PUNCT.includes(a) || a === ' ' || !(LAT.test(a) && LAT.test(b))) { cut = k; break; } }
      if (i + 1 < chars.length && LAT.test(chars[i].c) && LAT.test(chars[i + 1].c)) { out.push(cur.slice(0, cut)); cur = cur.slice(cut); } else { out.push(cur); cur = []; }
    }
  }
  if (n(cur)) out.push(cur);
  return out.map((seg: any[]) => { let s = '', hi = false; seg.forEach((x) => { if (x.hi !== hi) { s += '**'; hi = x.hi; } s += x.c; }); if (hi) s += '**';
    return s.replace(/^\s+|\s+$/g, '').replace(/[，。、；：,.;:]+(\*\*)?$/, '$1').replace(/^(\*\*)?[，。、；：！？,.;:!?\s]+/, '$1'); }).filter((s) => countChars(s) > 0);
}
export function timeline(script: any, fps: number, T: any) {
  const tr = Math.round((T.motion.transition?.duration_s ?? 0.5) * fps); let cur = 0;
  return (script.segments || []).map((s: any, i: number) => {
    const d = Math.max(1, Math.round((s.duration_s || 4) * fps)), type = s.transition || script.transition || T.motion.transition?.type || 'fade';
    const overlap = i === 0 || type === 'cut' ? 0 : tr, it = {seg: s, from: cur - overlap, dur: d + overlap, overlap, type}; cur += d; return it;
  });
}
