import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame, Heading} from './Frame';
import {enter} from '../anim';
import {parseHighlight, hexA} from '../theme';

// key points appearing one by one, **keyword** highlighted (V-01 逐条入场 / 关键词强调)
export const BulletList: React.FC<{T: any; seg: any; delay: number}> = ({T, seg, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ty = T.typography;
  const items: string[] = seg.items || [];
  const total = Math.round((seg.duration_s || 5) * fps);
  // spread items across the first ~60% of the segment, never faster than stagger_s
  const gap = Math.max(Math.round(T.motion.stagger_s * fps), Math.round((total * 0.55) / Math.max(1, items.length)));
  const h = enter(T, f, fps, delay);
  return (
    <Frame T={T}>
      <div style={{opacity: h.opacity, transform: h.transform}}>
        <Heading T={T} text={seg.heading} f={f} fps={fps} />
      </div>
      <div style={{display: 'flex', flexDirection: 'column', gap: ty.scale_px.body * 0.6}}>
        {items.map((it, i) => {
          const e = enter(T, f, fps, delay + Math.round(fps * 0.3) + i * gap);
          return (
            <div key={i} style={{opacity: e.opacity, transform: e.transform, display: 'flex', alignItems: 'center', gap: 24, fontFamily: ty.families.body.css, fontSize: ty.scale_px.body, color: T.palette.text, fontWeight: ty.weights.body, lineHeight: ty.line_height}}>
              <div style={{width: ty.scale_px.body * 0.9, height: ty.scale_px.body * 0.9, borderRadius: 8, background: hexA(T.palette.primary, 0.18), border: `2px solid ${T.palette.primary}`, color: T.palette.primary, fontFamily: ty.families.mono.css, fontSize: ty.scale_px.body * 0.5, display: 'flex', alignItems: 'center', justifyContent: 'center', flexShrink: 0}}>
                {i + 1}
              </div>
              <div>
                {parseHighlight(it).map((p, k) => (
                  <span key={k} style={p.hi ? {color: T.palette.accent, fontWeight: 700} : {}}>{p.t}</span>
                ))}
              </div>
            </div>
          );
        })}
      </div>
    </Frame>
  );
};
