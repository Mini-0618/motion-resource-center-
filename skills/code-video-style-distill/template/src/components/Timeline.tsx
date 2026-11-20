import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Frame, Heading} from './Frame';
import {enter} from '../anim';
import {bezier, compStyle} from '../theme';

// Timeline: horizontal axis grows, nodes enter one by one with date + label (UI-09 时间线 / V-03 时间线 / V-04 新闻事件时间轴).
export const Timeline: React.FC<{T: any; seg: any; delay: number}> = ({T, seg, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const S = compStyle(T, 'timeline');
  const ty = T.typography;
  const events: {date: string; label: string}[] = seg.events || [];
  const n = Math.max(1, events.length);
  const h = enter(T, f, fps, delay);
  const lineP = interpolate(f - delay, [0, Math.round(T.motion.durations_s.slow * fps)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: bezier(T.motion.easing.enter.cubic_bezier)});
  return (
    <Frame T={T}>
      <div style={{opacity: h.opacity, transform: h.transform}}><Heading T={T} text={seg.heading} f={f} fps={fps} /></div>
      <div style={{position: 'relative', width: '100%', height: ty.scale_px.body * 6}}>
        <div style={{position: 'absolute', left: 0, top: '50%', height: S.line_px, marginTop: -S.line_px / 2, width: `${lineP * 100}%`, background: S.line_color, borderRadius: S.line_px}} />
        {events.map((ev, i) => {
          const x = ((i + 0.5) / n) * 100;
          const st = delay + Math.round(fps * 0.3) + i * Math.round(S.enter_stagger_s * fps);
          const e = enter(T, f, fps, st);
          return (
            <div key={i} style={{position: 'absolute', left: `${x}%`, top: 0, height: '100%', width: 0, opacity: e.opacity}}>
              <div style={{position: 'absolute', top: '50%', left: -S.node_size_px / 2, marginTop: -S.node_size_px / 2, width: S.node_size_px, height: S.node_size_px, borderRadius: '50%', background: S.node_color, transform: `scale(${0.4 + 0.6 * e.p})`}} />
              <div style={{position: 'absolute', bottom: `calc(50% + ${S.node_size_px * 1.4}px)`, left: -200, width: 400, textAlign: 'center', fontFamily: ty.families.mono.css, fontWeight: 700, fontSize: ty.scale_px.body * 0.8, color: S.date_color, transform: e.transform}}>{ev.date}</div>
              <div style={{position: 'absolute', top: `calc(50% + ${S.node_size_px * 1.4}px)`, left: -200, width: 400, textAlign: 'center', fontFamily: ty.families.body.css, fontSize: ty.scale_px.body * 0.75, color: S.label_color, transform: e.transform}}>{ev.label}</div>
            </div>
          );
        })}
      </div>
    </Frame>
  );
};
