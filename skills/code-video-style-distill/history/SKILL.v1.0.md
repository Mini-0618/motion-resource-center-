---
name: code-video-style-distill
description: 参考视频 → 蒸馏风格底座（style-tokens.json）→ 换选题量产（渲染后端可换：Remotion / Lemo-Opuscar 页面 / Motion Canvas / HyperFrames）→ 和原片对比迭代。用于底层由代码生成的动效视频（Remotion/React、GSAP/HTML、Manim、Motion Canvas、AE 表达式风格的 MG/知识类视频）。目标是高保真复刻风格，不承诺像素级一致。
---

# 代码动效视频：风格蒸馏与量产

工具目录：本 Skill 所在文件夹（下文简称 `$T`）。使用前先执行 `export T="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"`，或把 `$T` 设为该文件夹的绝对路径（在本仓库里即 `skills/code-video-style-distill`）。所有命令都相对于 `$T`，每一步都能单独跑。

## 什么时候用

- 手上有一条参考视频，想把它的配色、字体气质、版式、动效曲线、节奏、元件做成可复用的“风格底座”，之后只换选题批量出片。
- 参考片主体是代码/模板渲染的画面（标题卡、要点列表、图表、代码块、字幕条、转场）。实拍、AI 视频、3D 渲染为主的片子只能蒸馏包装层，先跑第 0 步确认。

## 范围门（每次开工前确认，不过就停）

1. **只处理有权参考的视频**：自己的作品、已获授权的、或仅作内部风格学习的公开视频。来源不明或明确禁止的，不做。
2. **只学风格和结构**，不搬运原片素材、截图、logo、商标、角色、配音、配乐、字体文件和原文案。
3. **字体**：原字体身份一律记 `unknown`，只用免费可商用替代（`$T/references/font-alternatives.md`）。
4. **不承诺像素级一致**：字体替代、抗锯齿、编码损伤、随机种子都会造成合理差异。对外表述用“高保真复刻”。
5. 全程本地 CLI，不装官方 REA、rea-video、dea 等项目，不调用付费服务，不注册账号，不对外发布。
6. `analyze` / `all` 要求 `RIGHTS_OK=1`（或 `--rights-ok`），表示你已确认第 1 条。

## 前置检查

```bash
which ffmpeg ffprobe node tesseract google-chrome
ls $T/.venv/bin/python
```

- 没有 venv：`python3 -m venv $T/.venv && $T/.venv/bin/pip install opencv-python-headless numpy scikit-learn pillow matplotlib jsonschema scipy pyyaml`
- 没有 tesseract：`sudo apt-get install -y tesseract-ocr tesseract-ocr-chi-sim`。装不上也能跑，OCR 相关字段（字号阶梯、文字颜色、元件检测里的文字证据）会降级成 `unknown`，要靠目测补。
- 模板依赖：`cd $T/template && npm install`（Remotion 4，渲染用本机 Chrome）。
- 入口：`$T/cvsd.py`（跨平台 Python 入口，内部全用 pathlib，不依赖 bash）；`$T/run.sh` 只是把参数原样（`"$@"`）转给 cvsd.py 的壳。每个子命令写在位置参数后面的额外参数都会原样透传给对应脚本（例如 `analyze ... --no-ocr --no-videomd --scene-threshold 0.4`）。
- 两段式一键流程（不会跳过人工判断）：
  1. `RIGHTS_OK=1 $T/run.sh all <ref.mp4> <work> <style-name> <script.json>`：precheck → analyze，然后**停在人工判断点**，提示看 contact_sheet 和关键帧、填 `<work>/overrides.json`（已自动生成空模板）。precheck 判为 `live_ai_3d` 时直接停（确需继续加 `--force`）。确实不需要人工判断才加 `--skip-review`。
  2. `$T/run.sh resume <ref.mp4> <work> <style-name> <script.json> --rounds 3`：每轮 = distill（带 overrides）→ checklist（只在第一轮生成）→ **stillcheck（不过就停，不渲全片）** → render `replica_rN.mp4` → compare；账本 DONE 或 STALLED 提前结束；两轮之间会等你按 gap-report 改 overrides.json 再回车（`--no-wait` 不等）。轮数用完没 DONE 就再跑一次 `resume`。
- 测试用节拍音轨：`$T/run.sh beat out.wav --bpm 100 --seconds 60`（ffmpeg 现生成）。script.json 里的音频文件不存在时，渲染器只警告、按无音频渲染。

### Windows（PowerShell）完整步骤

```powershell
# 1) 装依赖（任选 winget 或 choco，管理员 PowerShell）
winget install -e --id Python.Python.3.12
winget install -e --id OpenJS.NodeJS.LTS
winget install -e --id Gyan.FFmpeg
winget install -e --id UB-Mannheim.TesseractOCR
#   或：choco install -y python nodejs-lts ffmpeg tesseract
#   中文 OCR 语言包：把 chi_sim.traineddata（https://github.com/tesseract-ocr/tessdata_fast）放进
#   "C:\Program Files\Tesseract-OCR\tessdata\"；装完重开 PowerShell，确认：
tesseract --list-langs     # 要看到 chi_sim 和 eng
ffmpeg -version; node -v

# 2) Python 虚拟环境（Windows 的解释器在 .venv\Scripts\python.exe）
cd <工具目录>\code-video-style-distill
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install opencv-python-headless numpy scikit-learn pillow matplotlib jsonschema scipy pyyaml

# 3) 模板依赖
cd template; npm install; cd ..

# 4) 跑（所有子命令同 run.sh）
$env:RIGHTS_OK = "1"
.venv\Scripts\python.exe cvsd.py all  D:\ref.mp4 D:\work\demo my-style examples\topic-demo-9\script.json
#   看 D:\work\demo\ref_analysis\contact_sheet.png 和 keyframes\，填 D:\work\demo\overrides.json，然后：
.venv\Scripts\python.exe cvsd.py resume D:\ref.mp4 D:\work\demo my-style examples\topic-demo-9\script.json --rounds 3
```

渲染器会依次找 `--browser`、`REMOTION_BROWSER`、Linux 常见 Chrome 路径，都没有就用 Remotion 自动下载的 Chrome Headless Shell（Windows 上就是这种情况，首次渲染会下载一次）。

## 第 0 步（可选）：判断参考片是不是代码/模板生成的

```bash
$T/run.sh precheck /abs/ref.mp4 /abs/work
```

读 `work/precheck/precheck.md`：`code_template` 可以高保真复刻；`mixed_or_screen_recording` 只复刻包装层，录屏/截图要自备有权素材；`live_ai_3d` 复刻上限低，要先告诉用户能做到什么程度。这是启发式推测（平涂像素占比、色彩集中度、噪声、静止保持帧），以目测为准。思路借鉴 JuneYaooo/rea-video（Apache-2.0），没有引入它的代码。

## 第 1 步：拆解 analyze

```bash
RIGHTS_OK=1 $T/run.sh analyze /abs/ref.mp4 /abs/work [--no-ocr] [--no-videomd] [--scene-threshold 0.4]   # 额外参数原样传给 analyze.py
```

产物在 `work/ref_analysis/`：`meta.json`（ffprobe）、`scenes.csv`（切点 + 时间码）、`keyframes/`（每个镜头的 entry/mid/settled 三帧）、`contact_sheet.png`、`palette_global.png`/`palette_foreground.png`（k-means，HEX + 占比）、`motion_energy.csv/.png`（逐帧差分能量 + 运动事件 + 光流速度曲线）、`ocr/`、`audio_*`（响度包络、起音点、BPM、音画卡点）、`analysis.json`（全部数字），以及 `videomd/VIDEO.md`（符合 VIDEO.md v1 的拆片包，规范 © videomd contributors，CC BY 4.0）。

常用参数：`--scene-threshold 0.3`（漏切调低、误切调高）、`--sample-fps`、`--no-ocr`、`--ocr-lang chi_sim+eng`、`--no-videomd`。

### 必做：用 Read 看图做视觉判断

脚本测不到的东西要靠看图补，看完写进 overrides（第 2 步）：

1. `Read work/ref_analysis/contact_sheet.png`：每行一个镜头，三列是入场中、动画中、静止后。判断字体气质（几何/人文/圆体/宋体/手写，粗细）、装饰（背景网格、光斑、噪点、描边、阴影、圆角）、质感、元件类型（脚本漏掉的图标、箭头、流程图、标注框）。
2. `Read work/ref_analysis/motion_energy.png`：红线是切点，橙色是元素入场，紫色是转场。看节奏密度、有没有回弹（spring）。
3. 只对某个镜头拿不准时，再 `Read keyframes/sceneNNN_entry.png` 等单帧。
4. 看到的写“seen + 帧文件/时间码”，推断的写“inferred”，没看清的保持 `unknown`。

## 第 2 步：蒸馏 distill

```bash
$T/run.sh distill /abs/work <style-name> [/abs/work/overrides.json]
# = $T/.venv/bin/python $T/scripts/distill.py work/ref_analysis -o work/style --name <style-name> --styles-dir $T/styles [--overrides ...]
```

输出 `work/style/style-tokens.json`（按 `$T/schema/style-tokens.schema.json` 校验，不合规直接报错退出）：

- `canvas`、`palette`（bg / surface / primary / accent / text / text_muted / code_text / extra + 实测色块）
- `typography`（气质、免费替代字体族、字号阶梯 display/h1/h2/body/caption/code、字重、`font_substitutions` 替代表）
- `layout`（边距、安全区、栅格、对齐、圆角、装饰）
- `motion`（时长档位、`easing` 的 cubic-bezier、`easings` CSS 字符串、`keyframes` 轨道、spring、入场类型、错峰 stagger、转场、打字速度）
- `rhythm`（平均/中位镜头时长、切换间隔、视觉/音频 BPM、音画卡点规则、**入场事件密度 `entrance_events_per_min`**＝非转场运动事件数 ÷ 时长（分钟），seen；同一次能量爆发里同时入场的多个元素只计一次）
- `components`（标题卡、要点列表、柱状图、数字滚动、代码块、证据截图框、时间线、对比双栏、流程图、关键词高亮、字幕条、进度条、转场 → 模板段落类型 + 动效库分类编号；分类表随 Skill 打包在 `$T/references/motion-taxonomy.md`（只有编号、分类名、方法关键词），每个元件写 `taxonomy.verified` 和分类名，表里查不到的编号标 `UNVERIFIED`）
- `components_style`：字幕条、进度条，以及 evidence / timeline / compare / flow 四个知识片元件的样式（尺寸、描边、圆角、标注色、入场时长）。参考片里检测到 → 用实测值，provenance=seen；没检测到 → 从 palette/motion/layout 推出缺省值，provenance=unknown。
- `provenance`：**每个字段**都有 `status`（seen / inferred / unknown）、`confidence`、`evidence`（时间码、帧文件、OCR 行、CSV）、`method`。`unknowns` 列出所有没测到的字段。`unknown` 的意思是“没测到”，不是“不存在”（规则来自 aicodeking/leanrea，MIT）。

**分类表**：默认读 Skill 内的 `$T/references/motion-taxonomy.md`；换表用 `--taxonomy <file>`（`run.sh distill <work> <name> --taxonomy x.md`）或环境变量 `CVSD_TAXONOMY`，优先级 `--taxonomy` > `CVSD_TAXONOMY` > 内置。文件不存在 → stderr 打印 `ERROR taxonomy file not found` 并把所有编号标 `UNVERIFIED`（不中断蒸馏）；检测表用到但分类表里没有的编号 → 打 WARNING 列出编号。表格式：`| 编号 | 分类名 | 关键词 |`，编号形如 `UI-09`/`V-03`/`A-01`。

**风格目录 attribution.json**：`--styles-dir` 存风格时会生成模板，填参考片来源标注（`source_label`）、你对参考片的权利（`reference_rights`：自有/授权）、风格参数的许可（`style_tokens_license`）。不填，资源库清单里就是 `UNSPECIFIED`。

**overrides.json**：视觉判断和迭代修正都写这里，不手改 tokens。格式见 `$T/examples/overrides.example.json`，可带 `_provenance` 写清依据；没写依据的会自动标 `inferred / visual review`。

## 第 3 步：预先声明验收清单（必须在第一次渲染之前）

```bash
$T/run.sh checklist /abs/work /abs/script.json            # 同内容复刻再加 --same-content
```

生成 `work/acceptance.json/.md`，分三档，阈值写死、已存在就不覆盖（看到结果后不准放宽阈值）：

| 原定档 | 项目与默认阈值 |
|---|---|
| must | M1 画布一致；M2 背景 ΔE2000 ≤ 3；M3 色板加权 ΔE ≤ 6；M4 主色/强调色 ΔE ≤ 8；M5 入场速度曲线 r ≥ 0.80；M6 入场时长误差 ≤ 25%；M7 左边距差 ≤ 2pp；M8 对齐方式相同；M9 安全区差 ≤ 3pp；M10 面板圆角差 ≤ 6px；C* 脚本用到的每个元件都被检测到；知识片元件各两项几何/颜色（见下）；脚本有字幕时加中文字幕三项 U1 字幕底条色 ΔE ≤ 8、U2 字幕字号误差 ≤ 15%、U3 单条字幕 ≤ 18 字 |
| should | S1 正文字号 ≤ 15%；S2 标题字号 ≤ 20%；S3 转场类型+时长；S4 平均镜头时长 ≤ 35%；S5 错峰间隔 ≤ 35%；S6 背景装饰；S7 音画卡点比例差 ≤ 0.2；S10 入场事件密度（次/分钟）误差 ≤ 35%（受脚本内容量影响，所以是 should）；（同内容时）S8 运动曲线 r ≥ 0.6、S9 SSIM ≥ 0.85 |
| out | 原片字体文件、原素材/logo/商标、像素级完全一致；换选题时的整条曲线相关和 SSIM |

**出处分级规则（硬规则）**：每一项都记录 `source_paths`（依赖的 token 字段）和 `source_level`（这些字段 provenance 里最弱的那个：unknown < inferred < seen）。
- 只有 `seen` 的才留在 must；
- `inferred` 的 must 自动降到 should（`downgraded_reason`），gap-report 里只写“该值本身是推测，先目测确认再调参”，**不给追数建议**；
- `unknown` 的降到 should 并强制记 `not-testable`，不参与打分；
- 账本 DONE 只看**降级后**剩下的 must。目测核实过某个推测值，就在 overrides.json 写入并在 `_provenance` 标 `seen`，下次生成清单它才会回到 must。

**基准冻结**：主色/强调色、元件颜色与几何、圆角的基准，取自参考片分析（不带 overrides 的 distill，缓存在 `ref_analysis/_distill/`），建清单时写进各项 `baseline`，之后每轮都从 acceptance.json 读，**不会**随你修改 style-tokens/overrides 而漂移。

**字号**：任一侧没有 OCR、或字号来源是默认值/unknown 时，S1/S2 记 not-testable，不参与相似度计算。

**中文字幕三项（U1–U3）**：来源字段 `components_style.subtitle`。参考片 OCR 认出了底部居中的字幕行 → seen → 留在 must；参考片没 OCR 或没认出字幕 → unknown → 降为 should 并强制 not-testable。复刻侧没有 OCR 结果时，U2/U3 也记 not-testable，不会被算成通过。
- U1 底条色：复刻片字幕行局部底色与冻结基准（参考片实测 `subtitle.bg`）的 ΔE2000 ≤ 8；
- U2 字号：底部居中 OCR 行墨迹字号中位数之比 |rep/ref−1| ≤ 0.15（按画布高度归一）；
- U3 单条 ≤ 18 字：复刻片每条底部 OCR 行去掉空格和标点后的字数最大值 ≤ 18。模板（三个 HTML/Remotion/Motion Canvas 实现一致）会把超过 18 字的 `caption` 自动拆成连续的单行字幕（优先在标点处断，不拆英文单词，去掉行尾逗号句号，`**高亮**` 保留），按字数分配显示时长；`caption_cues` 里过长的条目也在各自时间窗内拆分。上限可用 `components_style.subtitle.max_chars` 改。Python 版同一规则：`scripts/subtitle_rules.py`。

知识片元件的验收项（元件没有验收项不算数）：

| 元件 | 检测项 | 颜色项 | 几何项 |
|---|---|---|---|
| evidence 证据截图框 | 复刻片检测到 `evidence_frame` | 高亮框颜色 ΔE ≤ 8 | 截图框宽度差 ≤ 6pp |
| timeline 时间线 | 检测到 `timeline` | 节点色 ΔE ≤ 8 | 节点尺寸误差 ≤ 30% |
| compare 对比双栏 | 检测到 `compare_columns` | 面板底色 ΔE ≤ 6 | 两栏间距差 ≤ 2pp |
| flow 流程图 | 检测到 `flow_chart` | 节点描边色 ΔE ≤ 8 | 节点 ≥ 3 且方向一致 |

结构改编自 Speedrunlab/reverse-engineer-anything-self-learning-loop（MIT）的 parity checklist。

## 第 4 步：写 script.json 换选题

内容和风格分开（“配方/当期内容”分离思路参考 JuneYaooo/capsule-cinema，Apache-2.0）：`script.json` 只放选题文字、数据、时长、音频；颜色、字体、动效全在 tokens 里。混写会被 `render.mjs` 拒绝。

```json
{
  "audio": {"src": "bgm.wav", "volume": 0.8},
  "segments": [
    {"type": "title", "duration_s": 3.6, "kicker": "EP.08", "title": "一分钟看懂 **asyncio**", "subtitle": "副标题", "caption": "字幕"},
    {"type": "bullets", "duration_s": 4.8, "heading": "三个关键词", "items": ["**协程**：async def", "**await**：让出控制权"]},
    {"type": "code", "duration_s": 6, "heading": "示例", "language": "python", "filename": "main.py", "code": "print(1)", "highlight_lines": [1]},
    {"type": "bars", "duration_s": 4.8, "heading": "耗时（秒）", "unit": "s", "decimals": 1, "data": [{"label": "串行", "value": 3}, {"label": "asyncio", "value": 1, "highlight": true}]},
    {"type": "stat", "duration_s": 3.6, "heading": "吞吐量提升", "value": 3, "suffix": "×", "label": "示例数据"}
  ]
}
```

- 段落时长参照 `rhythm.shot_mean_s`；要点数和代码长度按 `motion.stagger_s`、`motion.typing_cps` 留够时间。
- `**词**` = 关键词高亮。字段全表见 `$T/template/README.md`；9 种段落齐全的例子 `$T/examples/topic-demo-9/script.json`，5 段的简单例子 `$T/examples/topic-demo/script.json`。
- 9 种段落：`title` 标题卡、`bullets` 要点、`code` 代码打字机、`bars` 柱状图、`stat` 大数字、`evidence` 证据截图框、`timeline` 时间线、`compare` 对比双栏、`flow` 流程图。
- **evidence 素材**：只能用有权使用的截图/实拍画面，`source` 字段写明来源（画面上会显示“来源：…”）。工具自带的 `examples/assets/placeholder-evidence-*.png` 是自生成占位图，只能测试用。
- 数据要真实或明确标“示例数据”。

## 第 5 步：静帧预检 stillcheck（全片渲染之前）

```bash
$T/run.sh stillcheck /abs/work /abs/script.json      # -> work/stillcheck_rN/stillcheck.md / .json / stillcheck_sheet.png
```

只渲 3 张静帧（用当前渲染后端，`--renderer` 可选）：从参考片挑 3 个有代表性的镜头（优先一个面板类：代码/对比/流程，一个文字类：要点/标题，一个其它类：时间线/柱状图/证据/数字），在复刻脚本里找同类段落，取该段停稳时刻（下一段转场开始前 0.3s）。只查两档：
- 色板：背景 ΔE（M2）、色板加权 ΔE（M3）、主色/强调色 ΔE（M4，基准取自 acceptance.json 冻结值）；
- 版式：左边距（M7）、对齐（M8）、安全区（M9）、面板圆角（M10）。

阈值和档位都从 acceptance.json 读（降级后的）。任何 must 失败 → 写差距并以非 0 退出，`resume` 会停下不渲全片。实测（43 秒 1080p 的 9 段片，8 核）：静帧预检 14–16 秒（其中渲 3 张静帧约 6 秒），全片渲染 130–135 秒，一整轮（distill+预检+渲染+compare）约 230 秒。预检不过的轮次只花约 16 秒，省掉约 88% 的渲染时间；预检通过的轮次多花约 16 秒（约 +7%）。

## 第 6 步：渲染

```bash
$T/run.sh render /abs/work /abs/script.json /abs/work/replica_r1.mp4 [--renderer remotion|lemo|motion-canvas|hyperframes]
# 或环境变量 CVSD_RENDERER=lemo；stillcheck / resume 同样接受 --renderer
```

渲染层是可替换接口（`$T/scripts/renderers.py`）：style-tokens.json + script.json 进、mp4（或静帧 PNG）出，四个后端用同一套时间线语义（段落顺序播放，后一段提前 `transition.duration_s` 叠入，`cut` 不叠），所以 stillcheck 的取帧时刻、compare 的验收对所有后端通用。每次渲染都在 mp4 元数据写入渲染时间，成片哈希各不相同。

| 后端 | 实现 | 段落支持 | 依赖 / 许可 |
|---|---|---|---|
| `remotion`（默认） | `template/`（React） | 9 种全部 | Remotion 自有许可证，团队商用前核对 https://www.remotion.dev/license |
| `lemo` | `renderers/html/`：自写的无框架页面（`runtime.js`，MIT），符合 Lemo-Opuscar 页面契约（`window.READY` / `window.DUR` / 确定性 `window.render(t)` / `window.TEXTS(t)`），由 Lemo 自己的 `core/render/video.mjs`、`still.mjs` 录制 | 9 种全部 | Lemo-Opuscar 代码 MIT（文档 CC BY-NC 4.0，未拷贝）；需要本地 checkout：`git clone https://github.com/lemomo-ai/lemo-opuscar <dir> && cd <dir> && npm install`，设 `LEMO_HOME=<dir>`（默认 `$T/work/_ext/lemo-opuscar`） |
| `motion-canvas` | `renderers/motion-canvas/`：Motion Canvas 3.17 场景（`src/scene.tsx`），不用编辑器 UI，`src/main.ts` 用 core 的 `bootstrap` + `Renderer` 的 PlaybackManager/Stage 逐帧 seek，`capture.mjs` 用无头 Chrome 截帧送 ffmpeg | title / bullets / code / bars / stat + 字幕 + 进度条 + 5 种转场；其它 4 种直接报错并列出支持的类型 | MIT；`cd $T/renderers/motion-canvas && npm install`（首跑自动 vite build） |
| `hyperframes` | 同一个 `renderers/html` 页面，加 HyperFrames 合成属性（`data-composition-id/start/duration/width/height`），画面由 HyperFrames 运行时的 `hf-seek` 事件驱动，`hyperframes render` / `snapshot` 录制 | 9 种全部 | Apache-2.0，Node ≥ 22；`mkdir <dir> && cd <dir> && npm init -y && npm install hyperframes@0.9.72`，设 `HYPERFRAMES_HOME=<dir>`（默认 `$T/work/_ext/hyperframes`）。调用时自动关遥测和更新检查（`HYPERFRAMES_NO_TELEMETRY=1`、`DO_NOT_TRACK=1`、`HYPERFRAMES_NO_UPDATE_CHECK=1`）；**不要用** publish / auth / cloud / share 等联网命令 |

Lemo / Motion Canvas / HyperFrames 都用本机 Chrome（`PLAYWRIGHT_CHROME` / `PUPPETEER_EXECUTABLE_PATH`，默认找 `/usr/bin/google-chrome`），音频由 `renderers.py` 用 ffmpeg 混进去。单独预览 HTML 页面：`python renderers/html/build_page.py --tokens t.json --script s.json --outdir demo/`，浏览器打开 `demo/index.html`。

## 第 7 步：compare 迭代（2–3 轮）

```bash
$T/run.sh compare /abs/ref.mp4 /abs/work /abs/work/replica_r1.mp4 "round 1: tokens as distilled"
```

每轮输出 `work/compare_rN/`：

- `report.md`：总分（must 70% + should 30%，not-testable 项不进分母）和清单逐项 pass / fail / not-testable / mismatch，每项带原定档位、出处等级、来源字段
- `gap-report.md`：失败项按 must → should 排序，每项标出处等级；seen 的给具体要改的 token 和建议值，inferred 的只提示先目测确认，unknown 的说明为何 not-testable
- `sidebyside_grid.png`（同一归一化时间点的左右对比帧）、`sidebyside.mp4`（并排对比片）
- `metrics.json`：色板 ΔE、入场曲线相关、整条运动曲线相关、逐像素通道阈值差异和变化比例（尺寸不一致记 `mismatch`，不算通过，思路来自 morluto/rea `pngVisualDiff.ts`，Python 重写）、12 条水平风格带 ΔE（思路来自 obaid1dev/dea）
- `work/iteration-ledger.json/.md`：迭代账本，每轮的分数、Δ、成片 sha256、tokens 指纹、改了什么、失败项

迭代规则：

1. 先 `Read sidebyside_grid.png` 目测，再看 `gap-report.md`。
2. 一次只修一批（优先 must），改动写进 overrides.json，带 `_provenance` 说明依据（例如“round 1 gap M6”）。
3. 每轮固定顺序：`distill` → `stillcheck`（不过就回到第 2 条）→ `render`（新文件 `replica_rN.mp4`）→ `compare`，note 写清这轮改了什么。`resume --rounds N` 会自动按这个顺序跑。
4. **降级后的所有 must 项，在连续两轮、两个不同成片文件（按 sha256 判断）上都 pass，账本才变成 DONE**。同一个文件重复 compare 会警告且不计轮次；想不改参数复查，就重新渲染出一个新文件。not-testable 和 mismatch 都不算 pass。
5. 连续三轮分数不动，账本显示 STALLED：停下来问人，不要乱调。

## 第 8 步：风格资产命名与存放

- 位置：`$T/styles/<style-name>/`，`<style-name>` 用小写短横线，描述风格不描述来源，例如 `paper-terminal`、`neon-dashboard`。
- 内容：`style-tokens.json`（最终版，含 provenance）、`README.md`（色板、动效、元件、待目测清单）、`refs/`（联系表、运动曲线、色板图、静止关键帧）。
- 迭代收敛后把最终 overrides 一起存进去（`styles/<name>/overrides.json`），并在 README 记一句验收结论和账本路径。
- `refs/` 里的原片帧只作内部对照，**不得**随模板、成片或资产包对外分发。
- 量产时：`--tokens $T/styles/<name>/style-tokens.json` 加新的 script.json 就行。

### 导出到动效资源库：export-index

```bash
$T/run.sh export-index [--styles-dir $T/styles] [-o $T/styles/asset-index.json] [--taxonomy x.md] [--strict]
```

把 `styles/*/` 汇总成一个 manifest（格式 `cvsd-asset-index/1`，校验 `$T/schema/asset-index.schema.json`）。每个风格一条：名称、路径、tokens 摘要（画布、色板、字体族与字号、入场方式/时长/缓动/转场、镜头时长与入场密度）、元件（模板段落类型 + 分类编号 + 是否在分类表里查得到）、`taxonomy_ids`、provenance 计数（seen/inferred/unknown）和未测字段、`refs/` 路径、license/attribution（读 `attribution.json`；`refs_distributable` 固定 false）。另带一个 `motion_center` 块，字段与 Mini-0618/motion-resource-center- 仓库 `motion_center/core.py` 的 `add_resource()` 一致（title / url / source_pool / category / styles / description / prompt / license / source_url），那个仓库没有单独的 asset-index 格式（2026-11-19 核对过），所以对齐它的资源记录字段。没填 attribution.json 的风格会打 WARNING，`--strict` 时退出码 1。

## 事实与推测怎么写

- tokens：看 `provenance.<字段>.status`。给人汇报时，seen 的附时间码或帧文件，inferred 的写“推测”和依据，unknown 的写“未测到”。
- VIDEO.md：时间线里键名带 `~` 的是推断（`made~`），不带的是看到或测到的。
- 不要把 unknown 写成“没有”，不要把推测写成实测。

## 已知局限

- 缓动是从像素运动反推的（光流速度 → 累积进度 → cubic-bezier 拟合），只能保证曲线形状接近，参数不唯一；`motion.easing.enter` 是 inferred，所以 M5 默认被降到 should。spring 参数没有拟合。
- 事件时长按能量阈值测，ease-out 的尾巴会被截掉，测出来通常比真实时长短 10–25%，靠 compare 的 M6 校正。
- OCR（tesseract）读不出超大标题，也会漏读彩色代码（底部字幕区另做一遍反色 OCR 来补漏），字号阶梯里的 display 常常是推测值，打字速度通常偏低。
- 转场类型只能区分 slide / zoom / 其它；wipe 和 fade 需要目测。字体身份测不出来，只有气质推测。
- 渲染后端：Motion Canvas 后端目前只实现 5 种核心段落；HTML 页面（Lemo/HyperFrames）与 Remotion 模板是逐组件移植，同脚本同 tokens 下画面接近但不逐像素一致（spring 用闭式解、字体抗锯齿、JPEG 截帧）。HyperFrames 在没有 chrome-headless-shell 时退回截图模式（较慢，结果仍确定）。引擎实测（5 段脚本、同一份 tokens 与冻结验收）：Remotion / HyperFrames 首轮 must 全过；Motion Canvas 按 gap 建议改一次时长后通过；Lemo 录制的成片 M6 卡在 0.295（第 5 个入场事件比同一页面在 HyperFrames 下少 1 帧），改 base、fast 档都不动，ledger 判 STALLED——Lemo 后端能出片，但 M6 这一项要人工判断。
- 入场事件密度按运动能量事件计，同一爆发内多个元素同时入场只算一次，换选题后内容量不同密度自然会变，所以只放 should。
- 字幕三项依赖 tesseract 能读出字幕行；底条为半透明时 U1 测到的是混合后的底色。
- 元件：模板现有 9 种段落（标题卡、要点、代码打字机、柱状图、大数字、证据截图框、时间线、对比双栏、流程图）+ 字幕条、进度条、关键词高亮、5 种转场。图标动画、地图、3D、人物/角色、Lottie 类元件还没有。
- 四个知识片元件的检测器是像素启发式：证据框要求截图区域占画面 ≥10% 且有纹理（纯色 UI 截图可能认不出），时间线要求一条横线上 ≥3 个圆点（竖向时间线认不出），对比双栏要求两块等高的 surface 色面板，流程图要求 ≥3 个同色节点排成一行/一列（菱形、曲线连线认不出）。认不出时 tokens 记 unknown，对应验收项降为 should + not-testable。
- 证据框的 Ken Burns 推进会让分析把一个段落切成两个镜头，镜头节奏（S4）会偏。
- 静帧预检只看 3 帧，抓不到动效和节奏问题；元件和字号仍要靠全片 compare。
- 换选题时，并排对比只比风格；像素差和 SSIM 只有在同内容复刻时才有意义。
- 测试用的参考片是本工具自己渲染的，分数偏乐观；真实外部视频还没测过。

## 测试（装依赖 + 运行）

测试脚本 `$T/tests/test_cli.py`，全部本地运行、不联网（除了首次 npm install）。依赖：Python venv（上面的 pip 包，含 `jsonschema`）、ffmpeg、tesseract（含 chi_sim）、Node ≥ 22、Chrome、`template/` 和 `renderers/motion-canvas/` 的 npm 依赖；后端测试还需要 Lemo 和 HyperFrames 的本地 checkout（见第 6 步，没装时这两项判 FAIL 并给出原因）。测试会用 `work/run9`（9 段回归的产物）和 `work/eng_base`（引擎对比的验收清单），没有就先跑一次第 7 步的回归。

Linux / macOS：

```bash
cd $T
python3 -m venv .venv && .venv/bin/pip install opencv-python-headless numpy scikit-learn pillow matplotlib jsonschema scipy pyyaml
sudo apt-get install -y ffmpeg tesseract-ocr tesseract-ocr-chi-sim      # macOS: brew install ffmpeg tesseract tesseract-lang
(cd template && npm install) && (cd renderers/motion-canvas && npm install)
.venv/bin/python tests/test_cli.py          # 全量（约 5–8 分钟）
.venv/bin/python tests/test_cli.py --fast   # 跳过账本、compare 和后端渲染项
```

Windows（PowerShell，依赖按上文“Windows 完整步骤”装好）：

```powershell
cd <工具目录>\code-video-style-distill
.venv\Scripts\python.exe -m pip install jsonschema
cd template; npm install; cd ..\renderers\motion-canvas; npm install; cd ..\..
$env:RIGHTS_OK = "1"
.venv\Scripts\python.exe tests\test_cli.py --fast
```

注意：第 1 项会调用 `bash run.sh`，Windows 上没有 bash 时这一项会失败，其余项走 `cvsd.py`。

## 出处

借鉴思路的项目和许可证见 `$T/THIRD_PARTY_NOTICES.md`；调研依据 `/workspace/ip-team/deliverables/video-reverse/REA调研-可复用点.md`。
