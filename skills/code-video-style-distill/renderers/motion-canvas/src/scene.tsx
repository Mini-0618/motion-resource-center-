// Motion Canvas (MIT) scene for code-video-style-distill: one scene, rebuilt every frame from (tokens, script, frame)
// — the same pure "frame -> picture" mapping as template/src (Remotion) and renderers/html/runtime.js.
// Supported segment types: title, bullets, code, bars, stat (+ caption subtitles, progress bar, wipe/fade/slide/zoom/cut).
import {makeScene2D, Layout, Rect, Txt, Circle, Node} from '@motion-canvas/2d';
import {D, deepMerge, cubicBezier, prog, spring, clamp01, hexA, parseHighlight, textOn, countChars, splitCaption, timeline} from './lib';

export const SUPPORTED = ['title', 'bullets', 'code', 'bars', 'stat'];

function setup() {
  const cfg = (window as any).CVSD;
  const T = deepMerge(D, cfg.tokens || {});
  const fps = Math.round(T.canvas.fps);
  const TL = timeline(cfg.script, fps, T);
  for (const it of TL) if (!SUPPORTED.includes(it.seg.type))
    throw new Error(`[motion-canvas] segment type '${it.seg.type}' not implemented in this backend (supported: ${SUPPORTED.join(', ')}). Use --renderer remotion or lemo.`);
  const totalF = Math.max(1, (cfg.script.segments || []).reduce((a: number, s: any) => a + Math.max(1, Math.round((s.duration_s || 4) * fps)), 0));
  return {T, fps, TL, totalF};
}

function enter(T: any, f: number, fps: number, delay = 0, styleOverride?: string) {
  const m = T.motion, style = styleOverride || m.enter_style;
  const dur = Math.max(1, Math.round(m.durations_s.base * fps));
  const p = style === 'spring-pop' || style === 'spring' ? spring(f - delay, fps, m.spring) : prog(f - delay, 0, dur, cubicBezier(m.easing.enter.cubic_bezier));
  const d = m.enter_distance_px ?? 40;
  const o = {opacity: clamp01(style === 'spring-pop' ? p * 1.5 : p), dx: 0, dy: 0, s: 1, p};
  if (style === 'slide-up') o.dy = (1 - p) * d;
  else if (style === 'slide-left') o.dx = (1 - p) * d;
  else if (style === 'scale') o.s = 0.85 + 0.15 * p;
  else if (style === 'spring-pop' || style === 'spring') o.s = 0.6 + 0.4 * p;
  return o;
}
// translate without disturbing siblings: +offset on one side, -offset on the other
const Ent = (e: any, props: any, children: any) => (
  <Layout layout opacity={e.opacity} scale={e.s} margin={[e.dy, -e.dx, -e.dy, e.dx]} {...props}>{children}</Layout>
);
function rich(text: string, base: any, hi: any) {
  return <Txt {...base}>{parseHighlight(text).map((p) => <Txt text={p.t} {...(p.hi ? hi : {})} />)}</Txt>;
}
const E = (T: any) => cubicBezier(T.motion.easing.enter.cubic_bezier);

function Frame(T: any, children: any) {
  const P = T.palette, L = T.layout, W = T.canvas.width, H = T.canvas.height, m = L.margins_pct, decor = L.decor || {};
  const grid: any[] = [];
  if (decor.grid_lines) {
    const g = Math.round(W / 24), c = hexA(P.text, 0.06);
    for (let x = 0; x < W; x += g) grid.push(<Rect width={1} height={H} x={-W / 2 + x + 0.5} fill={c} />);
    for (let y = 0; y < H; y += g) grid.push(<Rect width={W} height={1} y={-H / 2 + y + 0.5} fill={c} />);
  }
  return (
    <Node>
      <Rect width={W} height={H} fill={P.bg} />
      {grid}
      <Layout layout width={W} height={H} direction="column" justifyContent="center" alignItems={L.alignment === 'center' ? 'center' : 'start'}
        textAlign={L.alignment === 'center' ? 'center' : 'left'} padding={[(m.top / 100) * H, (m.right / 100) * W, (m.bottom / 100) * H, (m.left / 100) * W]}>
        {children}
      </Layout>
    </Node>
  );
}
function Heading(T: any, text: string, level = 'h1', extra: any = {}) {
  if (!text) return null;
  const ty = T.typography, sz = ty.scale_px[level];
  return <Txt text={text} fontFamily={ty.families.display.css} fontSize={sz} fontWeight={ty.weights.h1 ?? 700} fill={T.palette.text}
    letterSpacing={ty.letter_spacing_em * sz} lineHeight="115%" margin={[0, 0, ty.scale_px.body * 0.9, 0]} {...extra} />;
}

const C: Record<string, (T: any, seg: any, f: number, fps: number, delay: number) => any> = {};
C.title = (T, seg, f, fps, delay) => {
  const ty = T.typography, W = T.canvas.width, m = T.layout.margins_pct;
  const a = enter(T, f, fps, delay, T.motion.title_enter_style || T.motion.enter_style);
  const b = enter(T, f, fps, delay + Math.round(T.motion.stagger_s * fps * 2));
  const lineW = prog(f - delay, 0, Math.round(T.motion.durations_s.slow * fps), E(T));
  const contentW = W * (1 - (m.left + m.right) / 100);
  return Frame(T, [
    seg.kicker ? Ent(b, {}, <Txt text={String(seg.kicker).toUpperCase()} fontFamily={ty.families.mono.css} fontSize={ty.scale_px.caption} fill={T.palette.accent}
      letterSpacing={0.12 * ty.scale_px.caption} margin={[0, 0, 24, 0]} />) : null,
    Ent(a, {}, rich(seg.title, {fontFamily: ty.families.display.css, fontWeight: ty.weights.display, fontSize: ty.scale_px.display, lineHeight: '108%', fill: T.palette.text,
      letterSpacing: ty.letter_spacing_em * ty.scale_px.display}, {fill: T.palette.primary})),
    <Rect height={8} width={Math.max(0.001, lineW * 0.3 * contentW)} fill={T.palette.primary} radius={4} margin={[36, 0, 36, 0]} />,
    seg.subtitle ? Ent(b, {}, <Txt text={seg.subtitle} fontFamily={ty.families.body.css} fontSize={ty.scale_px.h2 * 0.75} fill={T.palette.text_muted} fontWeight={ty.weights.body} />) : null,
  ]);
};
C.bullets = (T, seg, f, fps, delay) => {
  const ty = T.typography, items: string[] = seg.items || [], total = Math.round((seg.duration_s || 5) * fps);
  const gap = Math.max(Math.round(T.motion.stagger_s * fps), Math.round((total * 0.55) / Math.max(1, items.length)));
  const hd = enter(T, f, fps, delay), bs = ty.scale_px.body * 0.9;
  return Frame(T, [
    Ent(hd, {}, Heading(T, seg.heading)),
    <Layout layout direction="column" gap={ty.scale_px.body * 0.6}>
      {items.map((it, i) => {
        const e = enter(T, f, fps, delay + Math.round(fps * 0.3) + i * gap);
        return Ent(e, {direction: 'row', alignItems: 'center', gap: 24}, [
          <Rect width={bs} height={bs} radius={8} fill={hexA(T.palette.primary, 0.18)} stroke={T.palette.primary} lineWidth={2} layout justifyContent="center" alignItems="center" shrink={0}>
            <Txt text={String(i + 1)} fontFamily={ty.families.mono.css} fontSize={ty.scale_px.body * 0.5} fill={T.palette.primary} />
          </Rect>,
          rich(it, {fontFamily: ty.families.body.css, fontSize: ty.scale_px.body, fill: T.palette.text, fontWeight: ty.weights.body, lineHeight: `${ty.line_height * 100}%`}, {fill: T.palette.accent, fontWeight: 700}),
        ]);
      })}
    </Layout>,
  ]);
};
const fmt = (v: number, dec: number) => v.toLocaleString('en-US', {minimumFractionDigits: dec, maximumFractionDigits: dec});
C.bars = (T, seg, f, fps, delay) => {
  const ty = T.typography, data: any[] = seg.data || [], max = Math.max(...data.map((d) => d.value), 1), dec = seg.decimals ?? 0;
  const grow = Math.round(T.motion.durations_s.slow * fps * 1.4), hd = enter(T, f, fps, delay);
  const colors = [T.palette.primary, T.palette.accent, ...(T.palette.extra || [])], R = T.layout.radius_px / 2;
  return Frame(T, [
    Ent(hd, {width: '100%'}, Heading(T, seg.heading)),
    <Layout layout direction="column" gap={ty.scale_px.body * 0.55} width="100%">
      {data.map((d, i) => {
        const st = delay + Math.round(fps * 0.25) + i * Math.round(T.motion.stagger_s * fps), p = prog(f - st, 0, grow, E(T));
        const c = d.highlight ? T.palette.accent : seg.multicolor ? colors[i % colors.length] : T.palette.primary;
        return (
          <Layout layout direction="row" alignItems="center" gap={28} opacity={Math.min(1, p * 3)}>
            <Txt text={d.label} width="18%" textAlign="right" fontFamily={ty.families.body.css} fontSize={ty.scale_px.caption} fill={T.palette.text_muted} />
            <Rect grow={1} height={ty.scale_px.body * 1.1} fill={hexA(T.palette.text, 0.06)} radius={R} clip layout alignItems="stretch">
              <Rect width={`${Math.max(0.0001, (d.value / max) * 100 * p)}%`} height="100%" fill={c} radius={R} />
            </Rect>
            <Txt text={`${seg.prefix || ''}${fmt(d.value * p, dec)}${seg.unit || ''}`} width="16%" fontFamily={ty.families.mono.css} fontSize={ty.scale_px.body}
              fill={d.highlight ? T.palette.accent : T.palette.text} />
          </Layout>
        );
      })}
    </Layout>,
  ]);
};
C.stat = (T, seg, f, fps, delay) => {
  const ty = T.typography, dur = Math.round(T.motion.durations_s.slow * fps * 1.8);
  const p = prog(f - delay, 0, dur, E(T)), e = enter(T, f, fps, delay);
  return Frame(T, [
    <Txt text={seg.heading || ''} opacity={e.opacity} fontFamily={ty.families.body.css} fontSize={ty.scale_px.h2} fill={T.palette.text_muted} />,
    <Txt text={`${seg.prefix || ''}${fmt((seg.value || 0) * p, seg.decimals ?? 0)}${seg.suffix || ''}`} fontFamily={ty.families.mono.css} fontWeight={700}
      fontSize={ty.scale_px.display * 1.6} fill={T.palette.primary} lineHeight="110%" />,
    seg.label ? Ent(e, {margin: [16 + e.dy, 0, -e.dy, 0]}, <Txt text={seg.label} fontFamily={ty.families.body.css} fontSize={ty.scale_px.body} fill={T.palette.text} />) : null,
  ]);
};
const KW = /\b(const|let|var|function|return|if|else|for|while|import|from|export|def|class|async|await|new|in|of|print|True|False|None|true|false|null)\b/;
function codeSpans(line: string, T: any) {
  const P = T.palette, base = P.code_text || textOn(P.surface, P);
  const cmt = line.match(/(\/\/.*|#.*)$/), body = cmt ? line.slice(0, cmt.index) : line;
  const out = body.split(/("[^"]*"?|'[^']*'?|\b\d+(?:\.\d+)?\b|\b\w+\b)/g).filter((s) => s !== '').map((p) => {
    let c = base;
    if (/^["']/.test(p)) c = (P.extra && P.extra[0]) || P.accent; else if (/^\d/.test(p)) c = P.accent; else if (KW.test(p) && p.match(KW)![0] === p) c = P.primary;
    return <Txt text={p} fill={c} />;
  });
  if (cmt) out.push(<Txt text={cmt[0]} fill={hexA(base, 0.5)} />);
  return out;
}
C.code = (T, seg, f, fps, delay) => {
  const ty = T.typography, code: string = seg.code || '', cps = seg.typing_cps || T.motion.typing_cps || 28;
  const startType = delay + Math.round(T.motion.durations_s.base * fps);
  const n = Math.max(0, Math.floor(((f - startType) / fps) * cps)), lines = code.slice(0, n).split('\n');
  const caretOn = Math.floor(f / (fps * 0.5)) % 2 === 0 || n < code.length;
  const e = enter(T, f, fps, delay, 'scale'), hl: number[] = seg.highlight_lines || [];
  const ct = T.palette.code_text || textOn(T.palette.surface, T.palette), cs = ty.scale_px.code, lh = cs * 1.55;
  return Frame(T, [
    Heading(T, seg.heading, 'h2', {opacity: e.opacity}),
    <Rect layout direction="column" width="100%" opacity={e.opacity} scale={e.s} fill={T.palette.surface} radius={T.layout.radius_px} stroke={hexA(T.palette.text, 0.1)} lineWidth={1}
      shadowColor={hexA('#000000', 0.35)} shadowBlur={80} shadowOffset={[0, 30]} clip>
      <Layout layout direction="row" gap={10} padding={[18, 24]} alignItems="center">
        {['#FF5F57', '#FEBC2E', '#28C840'].map((c) => <Circle size={14} fill={c} />)}
        <Txt text={seg.filename || seg.language || ''} margin={[0, 0, 0, 16]} fontFamily={ty.families.mono.css} fontSize={cs * 0.7} fill={hexA(ct, 0.55)} />
      </Layout>
      <Rect width="100%" height={1} fill={hexA(T.palette.text, 0.08)} />
      <Layout layout direction="column" padding={[28, 32]} minHeight={lh * Math.max(4, code.split("\n").length)}>
        {lines.map((ln, i) => (
          <Rect layout direction="row" alignItems="center" height={lh} fill={hl.includes(i + 1) && n >= code.length ? hexA(T.palette.primary, 0.14) : 'rgba(0,0,0,0)'}>
            <Txt text={String(i + 1)} width={cs * 2} shrink={0} fontFamily={ty.families.mono.css} fontSize={cs} fill={hexA(ct, 0.35)} />
            <Layout layout direction="row" fontFamily={ty.families.mono.css} fontSize={cs} textWrap="pre">{ln.length ? codeSpans(ln, T) : [<Txt text=" " fill={ct} />]}</Layout>
            {i === lines.length - 1 && caretOn ? <Rect width={cs * 0.6} height={cs * 1.2} fill={T.palette.accent} /> : null}
          </Rect>
        ))}
      </Layout>
    </Rect>,
  ]);
};

function Subtitle(T: any, text: string, cues: any[], total: number, f: number, fps: number) {
  const st = T.components_style?.subtitle || {}, max = st.max_chars ?? 18;
  let cur: string | undefined = text;
  if ((!cues || !cues.length) && text && countChars(text) > max) {
    const ch = splitCaption(text, max), tot = ch.reduce((a, c) => a + countChars(c), 0); let acc = 0;
    cues = ch.map((c) => { const q = {t: (acc / tot) * (total / fps), text: c}; acc += countChars(c); return q; });
  } else if (cues && cues.length) {
    const end = total / fps, src = cues;
    cues = src.flatMap((c: any, i: number) => { if (countChars(c.text) <= max) return [c]; const t1 = i + 1 < src.length ? src[i + 1].t : end; const ch = splitCaption(c.text, max), tot = ch.reduce((a, x) => a + countChars(x), 0); let acc = 0;
      return ch.map((x) => { const q = {t: c.t + (acc / tot) * (t1 - c.t), text: x}; acc += countChars(x); return q; }); });
  }
  if (cues && cues.length) { const t = f / fps; const c = [...cues].reverse().find((c: any) => t >= c.t); cur = c ? c.text : undefined; }
  if (!cur) return null;
  const ty = T.typography, W = T.canvas.width, H = T.canvas.height;
  const o = f < 6 ? prog(f, 0, 6) : f > total - 6 ? 1 - prog(f, total - 6, total) : 1;
  const mb = st.position === 'top' ? 0 : (Math.max(4, T.layout.margins_pct.bottom * 0.45) / 100) * W; // CSS % margins resolve against width
  return (
    <Layout layout width={W} height={H} direction="column" justifyContent={st.position === 'top' ? 'start' : 'end'} alignItems="center" padding={[0, 0, mb, 0]}>
      <Rect layout opacity={o} fill={hexA(st.bg || '#000000', st.bg_opacity ?? 0.6)} radius={10} padding={[12, 28]}>
        {rich(cur, {fontFamily: ty.families.body.css, fontSize: ty.scale_px.caption, fontWeight: 500, fill: st.color || '#FFFFFF'}, {fill: T.palette.accent})}
      </Rect>
    </Layout>
  );
}
function withTransition(type: string, dur: number, f: number, T: any, child: any) {
  const W = T.canvas.width, H = T.canvas.height;
  if (type === 'cut' || dur <= 0) return child;
  const p = prog(f, 0, dur, cubicBezier(T.motion.easing.enter.cubic_bezier));
  if (type === 'fade') return <Node opacity={p}>{child}</Node>;
  if (type === 'slide') return <Node x={(1 - p) * W}>{child}</Node>;
  if (type === 'zoom') return <Node opacity={p} scale={1.15 - 0.15 * p}>{child}</Node>;
  if (type === 'wipe') { const w = Math.max(0.001, W * p); return <Rect width={w} height={H} x={-W / 2 + w / 2} clip><Node x={W / 2 - w / 2}>{child}</Node></Rect>; }
  return child;
}

export default makeScene2D(function* (view) {
  const {T, fps, TL, totalF} = setup();
  const W = T.canvas.width, H = T.canvas.height;
  for (let F = 0; F < totalF; F++) {
    for (const c of view.children()) c.dispose();
    view.removeChildren();
    view.add(<Rect width={W} height={H} fill={T.palette.bg} />);
    TL.forEach((it: any) => {
      if (F < it.from || F >= it.from + it.dur) return;
      const f = F - it.from;
      view.add(withTransition(it.type, it.overlap, f, T, <Node>{C[it.seg.type](T, it.seg, f, fps, Math.round(it.overlap * 0.6))}{Subtitle(T, it.seg.caption, it.seg.caption_cues, it.dur, f, fps)}</Node>));
    });
    if (T.components_style?.progress_bar) { const w = Math.max(0.001, (F / Math.max(1, totalF - 1)) * W); view.add(<Rect width={w} height={6} x={-W / 2 + w / 2} y={-H / 2 + 3} fill={T.palette.primary} />); }
    yield;
  }
});
