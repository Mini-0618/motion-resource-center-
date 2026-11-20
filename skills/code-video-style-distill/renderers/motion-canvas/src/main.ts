// Headless entry: bootstraps the Motion Canvas project WITHOUT the editor UI and exposes a frame-seek page contract
// (window.READY / DUR / render(t)) that capture.mjs records. Uses only public @motion-canvas/core classes
// (bootstrap, Renderer's PlaybackManager + Stage), mirroring what Renderer.renderFrame() does in the editor.
import {bootstrap, makeProject, MetaFile, ValueDispatcher, Renderer, PlaybackState, Vector2} from '@motion-canvas/core';
import DefaultPlugin from '@motion-canvas/core/lib/plugin/DefaultPlugin';
import scene from './scene';
import {D, deepMerge} from './lib';

(async () => {
  const cfg = (window as any).CVSD;
  const T = deepMerge(D, cfg.tokens || {});
  const fps = Math.round(T.canvas.fps), W = T.canvas.width, H = T.canvas.height;
  (scene as any).name = 'cvsd';
  (scene as any).onReplaced = new ValueDispatcher((scene as any).config);
  const project: any = bootstrap('cvsd', {core: '3.17.2', two: '3.17.2', ui: null, vitePlugin: null} as any, [DefaultPlugin()], makeProject({scenes: [scene as any]}),
    new MetaFile('project', false), new MetaFile('settings', false));
  const r: any = new Renderer(project);
  const settings: any = {name: 'cvsd', size: new Vector2(W, H), resolutionScale: 1, colorSpace: 'srgb', fps, background: T.palette.bg, range: [0, Infinity],
    exporter: {name: '@motion-canvas/core/image-sequence', options: {}}};
  r.stage.configure(settings);
  r.playback.fps = fps;
  r.playback.state = PlaybackState.Rendering;
  await r.reloadScenes(settings);
  await r.playback.recalculate();
  await r.playback.reset();
  const out = document.getElementById('out') as HTMLCanvasElement;
  out.width = W; out.height = H;
  const ctx = out.getContext('2d')!;
  (window as any).FRAMES = r.playback.duration;
  (window as any).DUR = r.playback.duration / fps;
  (window as any).render = async (t: number) => {
    const fr = Math.max(0, Math.round(t * fps));
    if (fr < r.playback.frame) await r.playback.reset();
    await r.playback.seek(fr);
    await r.stage.render(r.playback.currentScene, r.playback.previousScene);
    ctx.drawImage(r.stage.finalBuffer, 0, 0);
  };
  await (window as any).render(0);
  (window as any).READY = true;
})().catch((e) => { (window as any).ERROR = String(e && e.stack || e); console.error(e); });
