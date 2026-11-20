// Reads style-tokens.json (see ../schema/style-tokens.schema.json) with safe defaults.
import {Easing} from 'remotion';

export type Tokens = any;
export type Script = any;

const D = {
  canvas: {width: 1920, height: 1080, fps: 30},
  palette: {bg: '#0B0F17', surface: '#151B26', primary: '#4F8CFF', accent: '#FFB224', text: '#F2F5FA', text_muted: '#8A94A6', extra: ['#3DDC97', '#FF5C7A']},
  typography: {
    families: {
      display: {css: '"Inter", "Noto Sans CJK SC", "Source Han Sans SC", sans-serif'},
      body: {css: '"Inter", "Noto Sans CJK SC", "Source Han Sans SC", sans-serif'},
      mono: {css: '"JetBrains Mono", "Noto Sans Mono CJK SC", monospace'},
    },
    scale_px: {display: 120, h1: 72, h2: 52, body: 40, caption: 32, code: 30},
    weights: {display: 800, h1: 700, body: 500},
    letter_spacing_em: -0.01,
    line_height: 1.35,
  },
  layout: {margins_pct: {left: 8, right: 8, top: 10, bottom: 10}, alignment: 'left', radius_px: 16, decor: {grid_lines: false, glow: true, noise: false}},
  motion: {
    durations_s: {fast: 0.25, base: 0.5, slow: 0.9},
    easing: {enter: {cubic_bezier: [0.16, 1, 0.3, 1]}, exit: {cubic_bezier: [0.7, 0, 0.84, 0]}, emphasis: {cubic_bezier: [0.34, 1.56, 0.64, 1]}},
    spring: {damping: 14, stiffness: 120, mass: 1},
    enter_style: 'slide-up', // slide-up | slide-left | fade | scale | spring-pop
    enter_distance_px: 40,
    stagger_s: 0.12,
    transition: {type: 'wipe', duration_s: 0.5}, // wipe | fade | slide | zoom | cut
    typing_cps: 28,
  },
  components_style: {subtitle: {position: 'bottom', bg_opacity: 0.6}, progress_bar: true},
};

function deepMerge(a: any, b: any): any {
  if (Array.isArray(a) || Array.isArray(b)) return b ?? a;
  if (typeof a !== 'object' || a === null) return b ?? a;
  const out: any = {...a};
  for (const k of Object.keys(b || {})) {
    out[k] = typeof b[k] === 'object' && b[k] !== null && !Array.isArray(b[k]) ? deepMerge(a[k] ?? {}, b[k]) : b[k] ?? a[k];
  }
  return out;
}

export function resolveTokens(t: Tokens) {
  return deepMerge(D, t || {});
}

export function bezier(arr?: number[]) {
  const a = arr && arr.length === 4 ? arr : [0.16, 1, 0.3, 1];
  return Easing.bezier(a[0], a[1], a[2], a[3]);
}

export function hexA(hex: string, alpha: number) {
  const h = (hex || '#000000').replace('#', '');
  const r = parseInt(h.slice(0, 2), 16), g = parseInt(h.slice(2, 4), 16), b = parseInt(h.slice(4, 6), 16);
  return `rgba(${r},${g},${b},${alpha})`;
}

// "plain **keyword** text" -> spans, keyword in accent colour
export function parseHighlight(s: string): {t: string; hi: boolean}[] {
  const parts = String(s ?? '').split(/(\*\*[^*]+\*\*)/g).filter(Boolean);
  return parts.map((p) => (p.startsWith('**') ? {t: p.slice(2, -2), hi: true} : {t: p, hi: false}));
}

export function luminance(hex: string) {
  const h = (hex || '#000000').replace('#', '');
  const c = [0, 2, 4].map((i) => parseInt(h.slice(i, i + 2), 16) / 255).map((v) => (v <= 0.03928 ? v / 12.92 : ((v + 0.055) / 1.055) ** 2.4));
  return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
}
// readable text colour on top of a given surface: prefer palette.text, else flip to light/dark
export function textOn(surface: string, P: any) {
  const lt = luminance(P.text), ls = luminance(surface);
  const ratio = (Math.max(lt, ls) + 0.05) / (Math.min(lt, ls) + 0.05);
  if (ratio >= 4.5) return P.text;
  return ls < 0.3 ? '#F2F5FA' : '#15171C';
}
