import React from 'react';
import {Composition} from 'remotion';
import {Main} from './Main';
import {resolveTokens} from './theme';

const demoProps = {
  tokens: {},
  script: {segments: [{type: 'title', duration_s: 3, title: 'Hello **Style Tokens**', subtitle: 'edit script.json'}]},
};

export const RemotionRoot: React.FC = () => (
  <Composition
    id="Main"
    component={Main as any}
    width={1920}
    height={1080}
    fps={30}
    durationInFrames={90}
    defaultProps={demoProps as any}
    calculateMetadata={({props}: any) => {
      const T = resolveTokens(props.tokens);
      const fps = Math.round(T.canvas.fps);
      const total = (props.script.segments || []).reduce((a: number, s: any) => a + Math.max(1, Math.round((s.duration_s || 4) * fps)), 0);
      return {durationInFrames: Math.max(1, total), fps, width: T.canvas.width, height: T.canvas.height};
    }}
  />
);
