# Remotion 模板（风格 × 内容解耦）

- `style-tokens.json`（风格底座，可复用的“方法”）：canvas / palette / typography / layout / motion / components_style。**不含选题文字。**
- `script.json`（当期内容）：segments、文案、数据、可选音频。**不含颜色、字体、动效参数。** `render.mjs` 会拒绝混写。

渲染：`node render.mjs --tokens <style-tokens.json> --script <script.json> --out out.mp4 [--concurrency 6]`
静帧：`node still.mjs --tokens <t.json> --script <s.json> --times 3.2,9.8,15.1 --outdir dir`（静帧预检用）
（浏览器依次找 `--browser`、`REMOTION_BROWSER`、`/usr/bin/google-chrome`、chromium，找不到就用 Remotion 自带的；首次 `npm install`。）
音频文件不存在时只警告、按无音频渲染。每次渲染都会在 mp4 元数据里写入渲染时间，所以文件哈希每次都不同（账本靠它区分“新成片”）。

渲染层接口（可替换）：`scripts/renderers.py` 规定了 “style-tokens.json + script.json → mp4 / 静帧 PNG” 的契约和时间轴语义。
现在的后端是 Remotion（注意 Remotion 是公司自有许可证，团队商用前先看 https://www.remotion.dev/license）；
以后换 Motion Canvas（MIT）或 HyperFrames（Apache-2.0）时，在 `BACKENDS` 里加一项、实现同样两条命令即可，风格 JSON 和分析脚本不用动。

## script.json 段落类型

| type | 元件 | 字段 |
|---|---|---|
| `title` | 标题卡（V-01/V-15） | `title`（支持 `**高亮**`）、`kicker`、`subtitle` |
| `bullets` | 要点逐条入场（V-01, UI-09） | `heading`、`items[]`（支持 `**高亮**`） |
| `bars` | 柱状图 + 数字滚动（V-02, UI-04） | `heading`、`data[{label,value,highlight}]`、`unit`、`prefix`、`decimals`、`multicolor` |
| `stat` | 大数字滚动（V-02） | `heading`、`value`、`prefix`、`suffix`、`decimals`、`label` |
| `code` | 代码块打字机（UI-09, V-05） | `heading`、`code`、`language`、`filename`、`highlight_lines[]`、`typing_cps` |
| `evidence` | 证据截图框（V-04 证据展示, V-05 局部高亮, V-09 镜头推进） | `heading`、`image`（相对 script.json 的图片路径）、`source`（来源，必填）、`highlight{x,y,w,h}`（占图片的百分比）、`annotation`（高亮旁的标注）、`zoom`（默认推进，`false` 关闭）、`fit`（cover/contain） |
| `timeline` | 时间线（UI-09, V-03, V-04 新闻事件时间轴） | `heading`、`events[{date,label}]`（建议 3–6 个，逐个入场） |
| `compare` | 对比双栏（UI-09, V-03 对比矩阵, V-05 前后对比） | `heading`、`left{title,items[]}`、`right{title,items[]}`、`highlight_rows[]`（行号从 0 开始，标出差异行；items 支持 `**高亮**`） |
| `flow` | 流程图（UI-09, V-03, V-10 线条连接） | `heading`、`steps[]`（3–6 个节点，逐个出现，箭头随后画出）、`direction`（horizontal / vertical） |

> **evidence 素材规则**：`image` 必须是你**有权使用**的截图或实拍画面（自己拍的、自己截的且平台允许、已获授权），并在 `source` 写清来源（媒体/网址/日期/作者），画面左下会显示“来源：…”。
> 本仓库 `examples/assets/placeholder-evidence-*.png` 是工具自己生成的占位图，只用于测试。没写 `source` 时渲染器会警告。

### 新元件的样式字段（style-tokens.json → components_style，缺省值从 palette / motion / layout 推出）

| 元件 | 字段 |
|---|---|
| `evidence` | `frame_color`、`frame_stroke_px`、`radius_px`、`highlight_color`（缺省 accent）、`highlight_stroke_px`、`source_color`、`zoom_scale`、`enter_s`、`highlight_delay_s` |
| `timeline` | `line_color`（缺省 text_muted）、`line_px`、`node_color`（缺省 primary）、`node_size_px`、`date_color`、`label_color`、`enter_stagger_s`、`enter_s` |
| `compare` | `panel_fill`（缺省 surface）、`panel_text`、`title_color`、`gap_pct`、`radius_px`、`highlight_color`（缺省 primary）、`enter_stagger_s`、`enter_s` |
| `flow` | `node_fill`（缺省 surface）、`node_stroke`（缺省 primary）、`node_stroke_px`、`node_text`、`radius_px`、`arrow_color`、`arrow_px`、`step_s`、`enter_s`、`orientation` |

每段通用：`duration_s`、`caption`（字幕条，V-13）或 `caption_cues[{t,text}]`、`transition`（wipe/fade/slide/zoom/cut，覆盖 tokens）。
全局：`transition`、`audio {src, volume}`（路径相对 script.json）。进度条由 `components_style.progress_bar` 控制。

加新元件：在 `src/components/` 写组件，在 `src/Main.tsx` 的 `REGISTRY` 注册，只从 `T`（tokens）取样式。

## 字幕（中文口径）

`caption` 超过 18 个字（不计空格；`**高亮**` 标记不计）时自动拆成连续的单行字幕：优先在标点处断、不拆英文单词、去掉行尾逗号句号，按字数分配显示时长；`caption_cues` 里过长的条目在各自时间窗内拆分。上限改 `components_style.subtitle.max_chars`。同一规则在 `renderers/html/runtime.js`、`renderers/motion-canvas/src/lib.ts`、`scripts/subtitle_rules.py` 里各有一份实现，改一处要同步三处。
