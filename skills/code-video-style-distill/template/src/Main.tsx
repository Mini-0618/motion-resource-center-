import React from 'react';
import {AbsoluteFill, Sequence, Audio, staticFile, useVideoConfig} from 'remotion';
import {resolveTokens} from './theme';
import {TitleCard} from './components/TitleCard';
import {BulletList} from './components/BulletList';
import {BarChart, StatCounter} from './components/BarChart';
import {CodeBlock} from './components/CodeBlock';
import {Subtitle, ProgressBar} from './components/Subtitle';
import {TransitionIn} from './components/Transition';
import {Evidence} from './components/Evidence';
import {Timeline} from './components/Timeline';
import {CompareColumns} from './components/CompareColumns';
import {Flow} from './components/Flow';

const REGISTRY: Record<string, React.FC<any>> = {
  title: TitleCard,
  bullets: BulletList,
  bars: BarChart,
  stat: StatCounter,
  code: CodeBlock,
  evidence: Evidence,
  timeline: Timeline,
  compare: CompareColumns,
  flow: Flow,
};

export function timeline(script: any, fps: number, T: any) {
  const trDur = Math.round((T.motion.transition?.duration_s ?? 0.5) * fps);
  let cur = 0;
  return (script.segments || []).map((s: any, i: number) => {
    const d = Math.max(1, Math.round((s.duration_s || 4) * fps));
    const type = s.transition || script.transition || T.motion.transition?.type || 'fade';
    const overlap = i === 0 || type === 'cut' ? 0 : trDur;
    const item = {seg: s, from: cur - overlap, dur: d + overlap, overlap, type};
    cur += d;
    return item;
  });
}

export const Main: React.FC<{tokens: any; script: any}> = ({tokens, script}) => {
  const T = resolveTokens(tokens);
  const {fps, durationInFrames} = useVideoConfig();
  const tl = timeline(script, fps, T);
  return (
    <AbsoluteFill style={{background: T.palette.bg}}>
      {tl.map((it: any, i: number) => {
        const C = REGISTRY[it.seg.type];
        if (!C) throw new Error(`unknown segment type: ${it.seg.type} (known: ${Object.keys(REGISTRY).join(', ')})`);
        return (
          <Sequence key={i} from={it.from} durationInFrames={it.dur} name={`${i}:${it.seg.type}`}>
            <TransitionIn type={it.type} dur={it.overlap} easing={T.motion.easing.enter.cubic_bezier}>
              <C T={T} seg={it.seg} delay={Math.round(it.overlap * 0.6)} />
              <Subtitle T={T} text={it.seg.caption} cues={it.seg.caption_cues} total={it.dur} />
            </TransitionIn>
          </Sequence>
        );
      })}
      {T.components_style?.progress_bar ? <ProgressBar T={T} total={durationInFrames} /> : null}
      {script.audio?.public_name ? <Audio src={staticFile(script.audio.public_name)} volume={script.audio.volume ?? 1} /> : null}
    </AbsoluteFill>
  );
};
