---
name: code-video-style-distill
description: 参考视频 → 蒸馏风格底座（style-tokens.json）→ 换选题用 Remotion 模板量产 → 和原片对比迭代。用于底层由代码生成的动效视频（Remotion/React、GSAP/HTML、Manim、Motion Canvas、AE 表达式风格的 MG/知识类视频）。目标是高保真复刻风格，不承诺像素级一致。
---

# 代码动效视频：风格蒸馏与量产

工具目录：本 Skill 所在文件夹（下文简称 `$T`）。使用前先执行 `export T="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd)"`，或把 `$T` 设为该文件夹的绝对路径（在本仓库里即 `skills/code-video-style-distill`）。所有命令都相对于 `$T`，每一步都能单独跑。`run.sh` 会按脚本所在目录自动定位，不必再手写绝对路径。

## 什么时候用

- 手上有一条参考视频，想把它的配色、字体气质、版式、动效曲线、节奏、元件做成可复用的“风格底座”，之后只换选题批量出片。
- 参考片主体是代码/模板渲染的画面（标题卡、要点列表、图表、代码块、字幕条、转场）。实拍、AI 视频、3D 渲染为主的片子只能蒸馏包装层，先跑第 0 步确认。

## 范围门（每次开工前确认，不过就停）

1. **只处理有权参考的视频**：自己的作品、已获授权的、或仅作内部风格学习的公开视频。来源不明或明确禁止的，不做。
2. **只学风格和结构**，不搬运原片素材、截图、logo、商标、角色、配音、配乐、字体文件和原文案。
3. **字体**：原字体身份一律记 `unknown`，只用免费可商用替代（`$T/references/font-alternatives.md`）。
4. **不承诺像素级一致**：字体替代、抗锯齿、编码损伤、随机种子都会造成合理差异。对外表述用“高保真复刻”。
5. 全程本地 CLI，不装官方 REA、rea-video、dea 等项目，不调用付费服务，不注册账号，不对外发布。
6. `run.sh analyze` 要求 `RIGHTS_OK=1`，表示你已确认第 1 条。

## 前置检查

```bash
which ffmpeg ffprobe node tesseract google-chrome
ls "$T/.venv/bin/python"
```

- 没有 venv：`python3 -m venv $T/.venv && $T/.venv/bin/pip install opencv-python-headless numpy scikit-learn pillow matplotlib jsonschema scipy pyyaml`
- 没有 tesseract：`sudo apt-get install -y tesseract-ocr tesseract-ocr-chi-sim`。装不上也能跑，OCR 相关字段（字号阶梯、文字颜色、元件检测里的文字证据）会降级成 `unknown`，要靠目测补。
- 模板依赖：`cd $T/template && npm install`（Remotion 4，渲染用本机 Chrome）。
- 一条命令跑完整链路：`RIGHTS_OK=1 $T/run.sh all <ref.mp4> <work> <style-name> <script.json>`。

## 第 0 步（可选）：判断参考片是不是代码/模板生成的

```bash
$T/run.sh precheck /abs/ref.mp4 /abs/work
```

读 `work/precheck/precheck.md`：`code_template` 可以高保真复刻；`mixed_or_screen_recording` 只复刻包装层，录屏/截图要自备有权素材；`live_ai_3d` 复刻上限低，要先告诉用户能做到什么程度。这是启发式推测（平涂像素占比、色彩集中度、噪声、静止保持帧），以目测为准。思路借鉴 JuneYaooo/rea-video（Apache-2.0），没有引入它的代码。

## 第 1 步：拆解 analyze

```bash
RIGHTS_OK=1 $T/run.sh analyze /abs/ref.mp4 /abs/work      # = $T/.venv/bin/python $T/scripts/analyze.py ref.mp4 -o work/ref_analysis
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
- `rhythm`（平均镜头时长、切换间隔、视觉/音频 BPM、音画卡点规则）
- `components`（标题卡、要点列表、柱状图、数字滚动、代码块、关键词高亮、字幕条、进度条、转场 → 模板段落类型 + 动效库分类 UI-01~UI-11 / V-01~V-15；动效库分类文档为可选说明，若本地有 taxonomy 笔记可通过环境变量 `CVSD_TAXONOMY_MD` 指向）
- `provenance`：**每个字段**都有 `status`（seen / inferred / unknown）、`confidence`、`evidence`（时间码、帧文件、OCR 行、CSV）、`method`。`unknowns` 列出所有没测到的字段。`unknown` 的意思是“没测到”，不是“不存在”（规则来自 aicodeking/leanrea，MIT）。

**overrides.json**：视觉判断和迭代修正都写这里，不手改 tokens。格式见 `$T/examples/overrides.example.json`，可带 `_provenance` 写清依据；没写依据的会自动标 `inferred / visual review`。

## 第 3 步：预先声明验收清单（必须在第一次渲染之前）

```bash
$T/run.sh checklist /abs/work /abs/script.json            # 同内容复刻再加 --same-content
```

生成 `work/acceptance.json/.md`，分三档，阈值写死、已存在就不覆盖（看到结果后不准放宽阈值）：

| 档 | 项目与默认阈值 |
|---|---|
| must | 画布一致；背景 ΔE2000 ≤ 3；色板加权 ΔE ≤ 6；主色/强调色 ΔE ≤ 8；入场速度曲线相关 r ≥ 0.80；入场时长误差 ≤ 25%；左边距差 ≤ 2 个百分点且对齐方式相同；脚本用到的元件全部被检测到 |
| should | 正文字号误差 ≤ 15%；标题字号 ≤ 20%；转场类型一致且时长 ≤ 30%；平均镜头时长 ≤ 35%；错峰间隔 ≤ 35%；背景装饰一致；音画卡点比例差 ≤ 0.2；（同内容时）整条运动曲线 r ≥ 0.6、SSIM ≥ 0.85 |
| out | 原片字体文件、原素材/logo/商标、像素级完全一致；换选题时的整条曲线相关和 SSIM |

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
- `**词**` = 关键词高亮。字段全表见 `$T/template/README.md`，完整例子 `$T/examples/topic-demo/script.json`。
- 数据要真实或明确标“示例数据”。

## 第 5 步：渲染

```bash
$T/run.sh render /abs/work /abs/script.json /abs/work/replica_r1.mp4
```

1080p、20 秒左右的片子，8 核机器约 1–1.5 分钟。

## 第 6 步：compare 迭代（2–3 轮）

```bash
$T/run.sh compare /abs/ref.mp4 /abs/work /abs/work/replica_r1.mp4 "round 1: tokens as distilled"
```

每轮输出 `work/compare_rN/`：

- `report.md`：总分（must 70% + should 30%）和清单逐项 pass / fail / not-testable / mismatch
- `gap-report.md`：失败项按 must → should 排序，每项给出具体要改的 token 和建议值
- `sidebyside_grid.png`（同一归一化时间点的左右对比帧）、`sidebyside.mp4`（并排对比片）
- `metrics.json`：色板 ΔE、入场曲线相关、整条运动曲线相关、逐像素通道阈值差异和变化比例（尺寸不一致记 `mismatch`，不算通过，思路来自 morluto/rea `pngVisualDiff.ts`，Python 重写）、12 条水平风格带 ΔE（思路来自 obaid1dev/dea）
- `work/iteration-ledger.json/.md`：迭代账本，每轮的分数、Δ、tokens 指纹、改了什么、失败项

迭代规则：

1. 先 `Read sidebyside_grid.png` 目测，再看 `gap-report.md`。
2. 一次只修一批（优先 must），改动写进 overrides.json，带 `_provenance` 说明依据（例如“round 1 gap M6”）。
3. `distill` → `render`（新文件名 `replica_r2.mp4`）→ `compare`，note 写清这轮改了什么。
4. **所有 must 项连续两轮都 pass，账本状态才变成 DONE**。not-testable 和 mismatch 都不算 pass。
5. 连续三轮分数不动，账本显示 STALLED：停下来问人，不要乱调。

## 第 7 步：风格资产命名与存放

- 位置：`$T/styles/<style-name>/`，`<style-name>` 用小写短横线，描述风格不描述来源，例如 `paper-terminal`、`neon-dashboard`。
- 内容：`style-tokens.json`（最终版，含 provenance）、`README.md`（色板、动效、元件、待目测清单）、`refs/`（联系表、运动曲线、色板图、静止关键帧）。
- 迭代收敛后把最终 overrides 一起存进去（`styles/<name>/overrides.json`），并在 README 记一句验收结论和账本路径。
- `refs/` 里的原片帧只作内部对照，**不得**随模板、成片或资产包对外分发。
- 量产时：`--tokens $T/styles/<name>/style-tokens.json` 加新的 script.json 就行。

## 事实与推测怎么写

- tokens：看 `provenance.<字段>.status`。给人汇报时，seen 的附时间码或帧文件，inferred 的写“推测”和依据，unknown 的写“未测到”。
- VIDEO.md：时间线里键名带 `~` 的是推断（`made~`），不带的是看到或测到的。
- 不要把 unknown 写成“没有”，不要把推测写成实测。

## 已知局限

- 缓动是从像素运动反推的（光流速度 → 累积进度 → cubic-bezier 拟合），只能保证曲线形状接近，参数不唯一。spring 参数没有拟合，用的是通用值。
- 事件时长按能量阈值测，ease-out 的尾巴会被截掉，测出来通常比真实时长短 10–25%，靠 compare 的 M6 校正。
- OCR（tesseract）读不出超大标题，也会漏读彩色代码，字号阶梯里的 display 常常是推测值，打字速度通常偏低。
- 转场类型只能区分 slide / zoom / 其它；wipe 和 fade 需要目测。
- 字体身份测不出来，只有气质推测。
- 模板现有 5 个元件（标题卡、要点、柱状图/数字滚动、代码打字机、字幕条）、进度条和 5 种转场；流程图、图标动画、3D 等元件需要按需补组件。
- 换选题时，并排对比只比风格；像素差和 SSIM 只有在同内容复刻时才有意义。

## 出处

借鉴思路的项目和许可证见 `$T/THIRD_PARTY_NOTICES.md`。内部调研笔记为可选说明，不随本 Skill 分发。
