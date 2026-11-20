import React from 'react';
import {AbsoluteFill} from 'remotion';
import {hexA} from '../theme';

// Background + optional decor (grid lines / glow / noise) + safe-area padding.
export const Frame: React.FC<{T: any; children: React.ReactNode}> = ({T, children}) => {
  const {palette: P, layout: L, canvas: C} = T;
  const m = L.margins_pct;
  const decor = L.decor || {};
  const bg = P.gradient
    ? `linear-gradient(${P.gradient.angle ?? 135}deg, ${P.gradient.from}, ${P.gradient.to})`
    : P.bg;
  return (
    <AbsoluteFill style={{background: bg}}>
      {decor.grid_lines ? (
        <AbsoluteFill
          style={{
            backgroundImage: `linear-gradient(${hexA(P.text, 0.06)} 1px, transparent 1px), linear-gradient(90deg, ${hexA(P.text, 0.06)} 1px, transparent 1px)`,
            backgroundSize: `${Math.round(C.width / 24)}px ${Math.round(C.width / 24)}px`,
          }}
        />
      ) : null}
      {decor.glow ? (
        <AbsoluteFill style={{background: `radial-gradient(circle at 80% 20%, ${hexA(P.primary, 0.22)}, transparent 45%), radial-gradient(circle at 10% 90%, ${hexA(P.accent, 0.12)}, transparent 40%)`}} />
      ) : null}
      <AbsoluteFill
        style={{
          paddingLeft: `${m.left}%`, paddingRight: `${m.right}%`, paddingTop: `${(m.top * C.height) / C.width}%`, paddingBottom: `${(m.bottom * C.height) / C.width}%`,
          display: 'flex', flexDirection: 'column', justifyContent: 'center',
          alignItems: L.alignment === 'center' ? 'center' : 'flex-start', textAlign: L.alignment === 'center' ? 'center' : 'left',
        }}
      >
        {children}
      </AbsoluteFill>
    </AbsoluteFill>
  );
};

export const Heading: React.FC<{T: any; text?: string; f: number; fps: number; style?: any; level?: 'h1' | 'h2'}> = ({T, text, style, level = 'h1'}) => {
  if (!text) return null;
  const ty = T.typography;
  return (
    <div style={{fontFamily: ty.families.display.css, fontSize: ty.scale_px[level], fontWeight: ty.weights.h1 ?? 700, color: T.palette.text, letterSpacing: `${ty.letter_spacing_em}em`, lineHeight: 1.15, marginBottom: ty.scale_px.body * 0.9, ...style}}>
      {text}
    </div>
  );
};
