import React from 'react';
import {Img, staticFile, useCurrentFrame, useVideoConfig, interpolate} from 'remotion';
import {Frame, Heading} from './Frame';
import {enter} from '../anim';
import {bezier, compStyle} from '../theme';

// Evidence screenshot frame (V-04 证据展示 / V-05 局部高亮 / V-09 摄像机推进).
// seg.image MUST be material you have the right to use; seg.source is shown on screen.
export const Evidence: React.FC<{T: any; seg: any; delay: number}> = ({T, seg, delay}) => {
  const f = useCurrentFrame();
  const {fps, width, height} = useVideoConfig();
  const S = compStyle(T, 'evidence');
  const ty = T.typography;
  const e = enter(T, f, fps, delay, 'scale');
  const total = Math.round((seg.duration_s || 5) * fps);
  const hl = seg.highlight; // {x,y,w,h} in % of the image
  const zoom = seg.zoom === false ? 1 : interpolate(f, [delay, total], [1, S.zoom_scale], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: bezier([0.33, 0, 0.67, 1])});
  const origin = hl ? `${hl.x + hl.w / 2}% ${hl.y + hl.h / 2}%` : '50% 50%';
  const hd = delay + Math.round(S.highlight_delay_s * fps);
  const hp = interpolate(f - hd, [0, Math.round(S.enter_s * fps)], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: bezier(T.motion.easing.enter.cubic_bezier)});
  const boxW = (width * S.max_w_pct) / 100;
  const boxH = (height * S.max_h_pct) / 100;
  const src = seg.image_public ? staticFile(seg.image_public) : null;
  return (
    <Frame T={T}>
      <Heading T={T} text={seg.heading} f={f} fps={fps} level="h2" style={{opacity: e.opacity, marginBottom: ty.scale_px.body * 0.5}} />
      <div style={{opacity: e.opacity, transform: e.transform, width: boxW, height: boxH, position: 'relative', border: `${S.frame_stroke_px}px solid ${S.frame_color}`, borderRadius: S.radius_px, overflow: 'hidden', background: T.palette.surface}}>
        <div style={{position: 'absolute', inset: 0, transform: `scale(${zoom})`, transformOrigin: origin}}>
          {src ? <Img src={src} style={{width: '100%', height: '100%', objectFit: seg.fit || 'cover'}} /> : null}
          {hl ? (
            <div style={{position: 'absolute', left: `${hl.x}%`, top: `${hl.y}%`, width: `${hl.w}%`, height: `${hl.h}%`, boxSizing: 'border-box',
              border: `${S.highlight_stroke_px}px solid ${S.highlight_color}`, borderRadius: 10, opacity: hp, transform: `scale(${1.25 - 0.25 * hp})`,
              boxShadow: `0 0 0 9999px rgba(0,0,0,${0.28 * hp})`}} />
          ) : null}
        </div>
        {hl && seg.annotation ? (
          <div style={{position: 'absolute', left: `${Math.min(70, hl.x)}%`, top: `${Math.min(88, hl.y + hl.h + 2)}%`, opacity: hp, background: S.highlight_color, color: '#FFFFFF',
            fontFamily: ty.families.body.css, fontSize: ty.scale_px.caption * 0.9, fontWeight: 700, padding: '6px 14px', borderRadius: 8}}>{seg.annotation}</div>
        ) : null}
      </div>
      <div style={{opacity: e.opacity, marginTop: 14, fontFamily: ty.families.mono.css, fontSize: ty.scale_px.caption * 0.7, color: S.source_color}}>
        {seg.source ? `来源：${seg.source}` : '来源：未标注（正式使用前必须补全）'}
      </div>
    </Frame>
  );
};
