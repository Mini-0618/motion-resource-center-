import React from 'react';
import {AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {hexA, parseHighlight, splitCaption, countChars} from '../theme';

// subtitle bar overlay (V-13 字幕条). Shows seg.caption for the whole segment (or timed cues).
export const Subtitle: React.FC<{T: any; text?: string; cues?: {t: number; text: string}[]; total: number}> = ({T, text, cues, total}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const st0 = T.components_style?.subtitle || {};
  const maxChars = st0.max_chars ?? 18;
  let cur = text;
  if ((!cues || !cues.length) && text && countChars(text) > maxChars) {
    // split into consecutive one-line cues, time share proportional to length
    const chunks = splitCaption(text, maxChars);
    const totalChars = chunks.reduce((a, c) => a + countChars(c), 0);
    let acc = 0;
    cues = chunks.map((c) => { const cue = {t: (acc / totalChars) * (total / fps), text: c}; acc += countChars(c); return cue; });
  }
  else if (cues && cues.length) {
    // explicit cues: split any cue longer than maxChars inside its own time window
    const end = total / fps;
    cues = cues.flatMap((c, i) => {
      if (countChars(c.text) <= maxChars) return [c];
      const t1 = i + 1 < cues!.length ? cues![i + 1].t : end;
      const chunks = splitCaption(c.text, maxChars);
      const tot = chunks.reduce((a, x) => a + countChars(x), 0);
      let acc = 0;
      return chunks.map((x) => { const cue = {t: c.t + (acc / tot) * (t1 - c.t), text: x}; acc += countChars(x); return cue; });
    });
  }
  if (cues && cues.length) {
    const t = f / fps;
    const c = [...cues].reverse().find((c) => t >= c.t);
    cur = c ? c.text : undefined;
  }
  if (!cur) return null;
  const st = T.components_style?.subtitle || {};
  const ty = T.typography;
  const o = interpolate(f, [0, 6, total - 6, total], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  const bottom = st.position === 'top' ? undefined : `${Math.max(4, T.layout.margins_pct.bottom * 0.45)}%`;
  return (
    <AbsoluteFill style={{justifyContent: st.position === 'top' ? 'flex-start' : 'flex-end', alignItems: 'center', pointerEvents: 'none'}}>
      <div style={{marginBottom: bottom, opacity: o, background: hexA(st.bg || '#000000', st.bg_opacity ?? 0.6), color: st.color || '#FFFFFF', fontFamily: ty.families.body.css, fontSize: ty.scale_px.caption, fontWeight: 500, padding: '12px 28px', borderRadius: 10, maxWidth: '90%', whiteSpace: 'nowrap', textAlign: 'center'}}>
        {parseHighlight(cur).map((p, i) => <span key={i} style={p.hi ? {color: T.palette.accent} : {}}>{p.t}</span>)}
      </div>
    </AbsoluteFill>
  );
};

// global progress bar (UI-01 进度指示 / V-15 包装)
export const ProgressBar: React.FC<{T: any; total: number}> = ({T, total}) => {
  const f = useCurrentFrame();
  return (
    <AbsoluteFill style={{justifyContent: 'flex-start'}}>
      <div style={{height: 6, width: `${(f / Math.max(1, total - 1)) * 100}%`, background: T.palette.primary}} />
    </AbsoluteFill>
  );
};
