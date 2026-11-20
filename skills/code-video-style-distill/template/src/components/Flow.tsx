import React from 'react';
import {useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Frame, Heading} from './Frame';
import {enter} from '../anim';
import {bezier, compStyle, textOn} from '../theme';

// Flow chart: nodes + arrow connectors appear step by step, horizontal or vertical
// (UI-09 可视化流程图 / V-03 流程图 / V-10 线条连接).
export const Flow: React.FC<{T: any; seg: any; delay: number}> = ({T, seg, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const S = compStyle(T, 'flow');
  const ty = T.typography;
  const steps: string[] = seg.steps || [];
  const vertical = seg.direction === 'vertical';
  const txt = S.node_text || textOn(S.node_fill, T.palette);
  const h = enter(T, f, fps, delay);
  const stepF = Math.round(S.step_s * fps);
  const arrowLen = vertical ? ty.scale_px.body * 1.2 : ty.scale_px.body * 1.6;
  return (
    <Frame T={T}>
      <div style={{opacity: h.opacity, transform: h.transform}}><Heading T={T} text={seg.heading} f={f} fps={fps} /></div>
      <div style={{display: 'flex', flexDirection: vertical ? 'column' : 'row', alignItems: 'center', width: vertical ? 'auto' : '100%'}}>
        {steps.map((s, i) => {
          const st = delay + Math.round(fps * 0.3) + i * stepF;
          const e = enter(T, f, fps, st, 'scale');
          const ap = interpolate(f - st + Math.round(stepF * 0.6), [0, Math.round(stepF * 0.6)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: bezier(T.motion.easing.enter.cubic_bezier)});
          return (
            <React.Fragment key={i}>
              {i > 0 ? (
                <svg width={vertical ? 24 : arrowLen} height={vertical ? arrowLen : 24} style={{flexShrink: 0}}>
                  {vertical ? (
                    <g stroke={S.arrow_color} strokeWidth={S.arrow_px} fill="none" strokeLinecap="round" opacity={ap > 0.01 ? 1 : 0}>
                      <line x1={12} y1={2} x2={12} y2={2 + (arrowLen - 6) * ap} />
                      {ap > 0.95 ? <polyline points={`4,${arrowLen - 12} 12,${arrowLen - 4} 20,${arrowLen - 12}`} /> : null}
                    </g>
                  ) : (
                    <g stroke={S.arrow_color} strokeWidth={S.arrow_px} fill="none" strokeLinecap="round" opacity={ap > 0.01 ? 1 : 0}>
                      <line x1={2} y1={12} x2={2 + (arrowLen - 6) * ap} y2={12} />
                      {ap > 0.95 ? <polyline points={`${arrowLen - 12},4 ${arrowLen - 4},12 ${arrowLen - 12},20`} /> : null}
                    </g>
                  )}
                </svg>
              ) : null}
              <div style={{opacity: e.opacity, transform: e.transform, flex: vertical ? undefined : 1, minWidth: vertical ? ty.scale_px.body * 9 : undefined,
                background: S.node_fill, border: `${S.node_stroke_px}px solid ${S.node_stroke}`, borderRadius: S.radius_px, padding: vertical ? '18px 32px' : '30px 20px',
                textAlign: 'center', fontFamily: ty.families.body.css, fontWeight: 600, fontSize: ty.scale_px.body * 0.8, color: txt}}>
                {s}
              </div>
            </React.Fragment>
          );
        })}
      </div>
    </Frame>
  );
};
