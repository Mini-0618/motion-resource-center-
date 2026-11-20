# Remotion 模板（风格 × 内容解耦）

- `style-tokens.json`（风格底座，可复用的“方法”）：canvas / palette / typography / layout / motion / components_style。**不含选题文字。**
- `script.json`（当期内容）：segments、文案、数据、可选音频。**不含颜色、字体、动效参数。** `render.mjs` 会拒绝混写。

渲染：`node render.mjs --tokens <style-tokens.json> --script <script.json> --out out.mp4 [--concurrency 6]`
（用本机 `/usr/bin/google-chrome`；首次 `npm install`。）

## script.json 段落类型

| type | 元件 | 字段 |
|---|---|---|
| `title` | 标题卡（V-01/V-15） | `title`（支持 `**高亮**`）、`kicker`、`subtitle` |
| `bullets` | 要点逐条入场（V-01, UI-09） | `heading`、`items[]`（支持 `**高亮**`） |
| `bars` | 柱状图 + 数字滚动（V-02, UI-04） | `heading`、`data[{label,value,highlight}]`、`unit`、`prefix`、`decimals`、`multicolor` |
| `stat` | 大数字滚动（V-02） | `heading`、`value`、`prefix`、`suffix`、`decimals`、`label` |
| `code` | 代码块打字机（UI-09, V-05） | `heading`、`code`、`language`、`filename`、`highlight_lines[]`、`typing_cps` |

每段通用：`duration_s`、`caption`（字幕条，V-13）或 `caption_cues[{t,text}]`、`transition`（wipe/fade/slide/zoom/cut，覆盖 tokens）。
全局：`transition`、`audio {src, volume}`（路径相对 script.json）。进度条由 `components_style.progress_bar` 控制。

加新元件：在 `src/components/` 写组件，在 `src/Main.tsx` 的 `REGISTRY` 注册，只从 `T`（tokens）取样式。
