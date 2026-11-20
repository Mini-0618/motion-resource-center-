import React from 'react';
import {useCurrentFrame, useVideoConfig} from 'remotion';
import {Frame, Heading} from './Frame';
import {enter} from '../anim';
import {hexA, textOn} from '../theme';

// tiny tokenizer-free highlighter: keywords / strings / comments / numbers
const KW = /\b(const|let|var|function|return|if|else|for|while|import|from|export|def|class|async|await|new|in|of|print|True|False|None|true|false|null)\b/;
function colorize(line: string, T: any) {
  const P = T.palette;
  const base = P.code_text || textOn(P.surface, P);
  const cmt = line.match(/(\/\/.*|#.*)$/);
  const body = cmt ? line.slice(0, cmt.index) : line;
  const parts = body.split(/("[^"]*"?|'[^']*'?|\b\d+(?:\.\d+)?\b|\b\w+\b)/g).filter((s) => s !== '');
  const out = parts.map((p, i) => {
    let c = base;
    if (/^["']/.test(p)) c = (P.extra && P.extra[0]) || P.accent;
    else if (/^\d/.test(p)) c = P.accent;
    else if (KW.test(p) && p.match(KW)![0] === p) c = P.primary;
    return <span key={i} style={{color: c}}>{p}</span>;
  });
  if (cmt) out.push(<span key="c" style={{color: hexA(base, 0.5)}}>{cmt[0]}</span>);
  return out;
}

// code block with typewriter effect + caret (UI-09 代码展示组件 / V-05 代码运行过程)
export const CodeBlock: React.FC<{T: any; seg: any; delay: number}> = ({T, seg, delay}) => {
  const f = useCurrentFrame();
  const {fps} = useVideoConfig();
  const ty = T.typography;
  const code: string = seg.code || '';
  const cps = seg.typing_cps || T.motion.typing_cps || 28;
  const startType = delay + Math.round(T.motion.durations_s.base * fps);
  const n = Math.max(0, Math.floor(((f - startType) / fps) * cps));
  const shown = code.slice(0, n);
  const lines = shown.split('\n');
  const caretOn = Math.floor(f / (fps * 0.5)) % 2 === 0 || n < code.length;
  const e = enter(T, f, fps, delay, 'scale');
  const hl: number[] = seg.highlight_lines || [];
  return (
    <Frame T={T}>
      <Heading T={T} text={seg.heading} f={f} fps={fps} level="h2" style={{opacity: e.opacity}} />
      <div style={{opacity: e.opacity, transform: e.transform, width: '100%', background: T.palette.surface, borderRadius: T.layout.radius_px, border: `1px solid ${hexA(T.palette.text, 0.1)}`, boxShadow: `0 30px 80px ${hexA('#000000', 0.35)}`, overflow: 'hidden'}}>
        <div style={{display: 'flex', gap: 10, padding: '18px 24px', borderBottom: `1px solid ${hexA(T.palette.text, 0.08)}`, alignItems: 'center'}}>
          {['#FF5F57', '#FEBC2E', '#28C840'].map((c) => <div key={c} style={{width: 14, height: 14, borderRadius: 7, background: c}} />)}
          <div style={{marginLeft: 16, fontFamily: ty.families.mono.css, fontSize: ty.scale_px.code * 0.7, color: hexA(T.palette.code_text || textOn(T.palette.surface, T.palette), 0.55)}}>{seg.filename || seg.language || ''}</div>
        </div>
        <div style={{padding: '28px 32px', fontFamily: ty.families.mono.css, fontSize: ty.scale_px.code, lineHeight: 1.55, whiteSpace: 'pre', minHeight: ty.scale_px.code * 1.55 * Math.max(4, code.split('\n').length)}}>
          {lines.map((ln, i) => (
            <div key={i} style={{display: 'flex', background: hl.includes(i + 1) && n >= code.length ? hexA(T.palette.primary, 0.14) : 'transparent'}}>
              <span style={{width: ty.scale_px.code * 2, color: hexA(T.palette.code_text || textOn(T.palette.surface, T.palette), 0.35), flexShrink: 0}}>{i + 1}</span>
              <span>
                {colorize(ln, T)}
                {i === lines.length - 1 && caretOn ? <span style={{background: T.palette.accent, color: T.palette.accent}}>▍</span> : null}
              </span>
            </div>
          ))}
        </div>
      </div>
    </Frame>
  );
};
