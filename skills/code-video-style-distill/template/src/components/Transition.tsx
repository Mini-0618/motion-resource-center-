import React from 'react';
import {AbsoluteFill, useCurrentFrame, interpolate} from 'remotion';
import {bezier} from '../theme';

// Incoming-segment transition (V-07): wipe | fade | slide | zoom | cut. Applied over the first `dur` frames.
export const TransitionIn: React.FC<{type: string; dur: number; easing: number[]; children: React.ReactNode}> = ({type, dur, easing, children}) => {
  const f = useCurrentFrame();
  if (type === 'cut' || dur <= 0) return <AbsoluteFill>{children}</AbsoluteFill>;
  const p = interpolate(f, [0, dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: bezier(easing)});
  let style: React.CSSProperties = {};
  if (type === 'wipe') style = {clipPath: `inset(0 ${100 - p * 100}% 0 0)`};
  else if (type === 'fade') style = {opacity: p};
  else if (type === 'slide') style = {transform: `translateX(${(1 - p) * 100}%)`};
  else if (type === 'zoom') style = {opacity: p, transform: `scale(${1.15 - 0.15 * p})`};
  return <AbsoluteFill style={style}>{children}</AbsoluteFill>;
};
