import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame, Heading} from './Frame';
import {enter} from '../anim';
import {compStyle, textOn, parseHighlight, hexA} from '../theme';

// Two-column comparison (before/after, A/B): rows enter alternately, highlighted rows marked
// (UI-09 对比面板 / V-03 对比矩阵 / V-05 前后效果对比).
export const CompareColumns: React.FC<{T: any; seg: any; delay: number}> = ({T, seg, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const S = compStyle(T, 'compare');
  const ty = T.typography;
  const txt = S.panel_text || textOn(S.panel_fill, T.palette);
  const cols = [seg.left || {}, seg.right || {}];
  const hi: number[] = seg.highlight_rows || [];
  const h = enter(T, f, fps, delay);
  const rows = Math.max(...cols.map((c) => (c.items || []).length), 0);
  return (
    <Frame T={T}>
      <div style={{opacity: h.opacity, transform: h.transform}}><Heading T={T} text={seg.heading} f={f} fps={fps} /></div>
      <div style={{display: 'flex', width: '100%', gap: `${S.gap_pct}%`}}>
        {cols.map((c, ci) => {
          const pe = enter(T, f, fps, delay + ci * Math.round(fps * 0.15), 'fade');
          return (
            <div key={ci} style={{flex: 1, opacity: pe.opacity, background: S.panel_fill, borderRadius: S.radius_px, padding: '32px 40px', minHeight: ty.scale_px.body * (2.4 + rows * 1.7)}}>
              <div style={{fontFamily: ty.families.display.css, fontWeight: 800, fontSize: ty.scale_px.h2 * 0.8, color: S.title_color, marginBottom: 24}}>{c.title}</div>
              {(c.items || []).map((it: string, ri: number) => {
                const st = delay + Math.round(fps * 0.4) + (ri * 2 + ci) * Math.round(S.enter_stagger_s * fps);
                const e = enter(T, f, fps, st);
                const isHi = hi.includes(ri);
                return (
                  <div key={ri} style={{opacity: e.opacity, transform: e.transform, display: 'flex', alignItems: 'center', gap: 16, fontFamily: ty.families.body.css, fontSize: ty.scale_px.body * 0.85, color: txt, padding: '10px 14px', marginBottom: 8, borderRadius: 8,
                    background: isHi ? hexA(S.highlight_color, 0.18) : 'transparent', borderLeft: `6px solid ${isHi ? S.highlight_color : 'transparent'}`}}>
                    {parseHighlight(it).map((p, k) => <span key={k} style={p.hi ? {color: S.highlight_color, fontWeight: 700} : {}}>{p.t}</span>)}
                  </div>
                );
              })}
            </div>
          );
        })}
      </div>
    </Frame>
  );
};
