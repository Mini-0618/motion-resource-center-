import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Frame} from './Frame';
import {enter} from '../anim';
import {bezier, parseHighlight} from '../theme';

// UI/V: title card (V-01 typography, V-15 chapter title)
export const TitleCard: React.FC<{T: any; seg: any; delay: number}> = ({T, seg, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ty = T.typography;
  const a = enter(T, f, fps, delay, T.motion.title_enter_style || T.motion.enter_style);
  const b = enter(T, f, fps, delay + Math.round(T.motion.stagger_s * fps * 2));
  const lineW = interpolate(f - delay, [0, Math.round(T.motion.durations_s.slow * fps)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: bezier(T.motion.easing.enter.cubic_bezier)});
  return (
    <Frame T={T}>
      {seg.kicker ? (
        <div style={{...b, fontFamily: ty.families.mono.css, fontSize: ty.scale_px.caption, color: T.palette.accent, letterSpacing: '0.12em', textTransform: 'uppercase', marginBottom: 24}}>{seg.kicker}</div>
      ) : null}
      <div style={{opacity: a.opacity, transform: a.transform, fontFamily: ty.families.display.css, fontWeight: ty.weights.display, fontSize: ty.scale_px.display, lineHeight: 1.08, color: T.palette.text, letterSpacing: `${ty.letter_spacing_em}em`}}>
        {parseHighlight(seg.title).map((p, i) => (
          <span key={i} style={{color: p.hi ? T.palette.primary : undefined}}>{p.t}</span>
        ))}
      </div>
      <div style={{height: 8, width: `${lineW * 30}%`, background: T.palette.primary, borderRadius: 4, margin: '36px 0'}} />
      {seg.subtitle ? (
        <div style={{opacity: b.opacity, transform: b.transform, fontFamily: ty.families.body.css, fontSize: ty.scale_px.h2 * 0.75, color: T.palette.text_muted, fontWeight: ty.weights.body}}>{seg.subtitle}</div>
      ) : null}
    </Frame>
  );
};
