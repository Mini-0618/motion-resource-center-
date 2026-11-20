import {interpolate, spring} from 'remotion';
import {bezier} from './theme';

// Generic entrance driven by tokens.motion. f = local frame, delay in frames.
export function enter(T: any, f: number, fps: number, delay = 0, styleOverride?: string) {
  const m = T.motion;
  const style = styleOverride || m.enter_style;
  const dur = Math.max(1, Math.round(m.durations_s.base * fps));
  let p: number;
  if (style === 'spring-pop' || style === 'spring') {
    p = spring({frame: f - delay, fps, config: {damping: m.spring.damping, stiffness: m.spring.stiffness, mass: m.spring.mass}});
  } else {
    p = interpolate(f - delay, [0, dur], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing: bezier(m.easing.enter.cubic_bezier)});
  }
  const d = m.enter_distance_px ?? 40;
  const opacity = Math.min(1, Math.max(0, style === 'spring-pop' ? p * 1.5 : p));
  let transform = '';
  if (style === 'slide-up') transform = `translateY(${(1 - p) * d}px)`;
  else if (style === 'slide-left') transform = `translateX(${(1 - p) * d}px)`;
  else if (style === 'scale') transform = `scale(${0.85 + 0.15 * p})`;
  else if (style === 'spring-pop' || style === 'spring') transform = `scale(${0.6 + 0.4 * p})`;
  return {opacity, transform, p};
}

