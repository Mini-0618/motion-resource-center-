import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Frame, Heading} from './Frame';
import {enter} from '../anim';
import {bezier, hexA} from '../theme';

const fmt = (v: number, dec: number) => v.toLocaleString('en-US', {minimumFractionDigits: dec, maximumFractionDigits: dec});

// horizontal bar chart with rolling numbers (V-02 / UI-04 柱状图增长 + 数字计数)
export const BarChart: React.FC<{T: any; seg: any; delay: number}> = ({T, seg, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ty = T.typography;
  const data: {label: string; value: number; highlight?: boolean}[] = seg.data || [];
  const max = Math.max(...data.map((d) => d.value), 1);
  const dec = seg.decimals ?? 0;
  const grow = Math.round(T.motion.durations_s.slow * fps * 1.4);
  const h = enter(T, f, fps, delay);
  const colors = [T.palette.primary, T.palette.accent, ...(T.palette.extra || [])];
  return (
    <Frame T={T}>
      <div style={{opacity: h.opacity, transform: h.transform, width: '100%'}}>
        <Heading T={T} text={seg.heading} f={f} fps={fps} />
      </div>
      <div style={{display: 'flex', flexDirection: 'column', gap: ty.scale_px.body * 0.55, width: '100%'}}>
        {data.map((d, i) => {
          const st = delay + Math.round(fps * 0.25) + i * Math.round(T.motion.stagger_s * fps);
          const p = interpolate(f - st, [0, grow], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: bezier(T.motion.easing.enter.cubic_bezier)});
          const c = d.highlight ? T.palette.accent : seg.multicolor ? colors[i % colors.length] : T.palette.primary;
          return (
            <div key={i} style={{display: 'flex', alignItems: 'center', gap: 28, opacity: Math.min(1, p * 3)}}>
              <div style={{width: '18%', fontFamily: ty.families.body.css, fontSize: ty.scale_px.caption, color: T.palette.text_muted, textAlign: 'right'}}>{d.label}</div>
              <div style={{flex: 1, height: ty.scale_px.body * 1.1, background: hexA(T.palette.text, 0.06), borderRadius: T.layout.radius_px / 2, overflow: 'hidden'}}>
                <div style={{width: `${(d.value / max) * 100 * p}%`, height: '100%', background: c, borderRadius: T.layout.radius_px / 2}} />
              </div>
              <div style={{width: '16%', fontFamily: ty.families.mono.css, fontSize: ty.scale_px.body, color: d.highlight ? T.palette.accent : T.palette.text, fontVariantNumeric: 'tabular-nums'}}>
                {seg.prefix || ''}{fmt(d.value * p, dec)}{seg.unit || ''}
              </div>
            </div>
          );
        })}
      </div>
    </Frame>
  );
};

// single big rolling number (数字滚动)
export const StatCounter: React.FC<{T: any; seg: any; delay: number}> = ({T, seg, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ty = T.typography;
  const dur = Math.round(T.motion.durations_s.slow * fps * 1.8);
  const p = interpolate(f - delay, [0, dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: bezier(T.motion.easing.enter.cubic_bezier)});
  const e = enter(T, f, fps, delay);
  return (
    <Frame T={T}>
      <div style={{opacity: e.opacity, fontFamily: ty.families.body.css, fontSize: ty.scale_px.h2, color: T.palette.text_muted}}>{seg.heading}</div>
      <div style={{fontFamily: ty.families.mono.css, fontWeight: 700, fontSize: ty.scale_px.display * 1.6, color: T.palette.primary, fontVariantNumeric: 'tabular-nums', lineHeight: 1.1}}>
        {seg.prefix || ''}{fmt((seg.value || 0) * p, seg.decimals ?? 0)}{seg.suffix || ''}
      </div>
      {seg.label ? <div style={{opacity: e.opacity, transform: e.transform, fontFamily: ty.families.body.css, fontSize: ty.scale_px.body, color: T.palette.text, marginTop: 16}}>{seg.label}</div> : null}
    </Frame>
  );
};
