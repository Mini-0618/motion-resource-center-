# AGENTS.md — 给所有 AI 的使用说明（code-video-style-distill）

> 读者：Cursor、Claude Code、Codex、ChatGPT、Grok 等任何能跑命令的 AI 助手。
> 读完这一页就能开工；细节以同目录 `SKILL.md` 为准，两者冲突时听 `SKILL.md`。

## 这是什么

一条**参考视频** → 蒸馏出**风格底座**（`style-tokens.json`：配色、字体气质、版式、动效曲线、节奏、元件）→ 换选题写 `script.json` → 用代码渲染出**同风格的新视频** → 和原片自动对比、迭代到验收通过。

- 适用：底层由代码/模板生成的动效视频（知识类 MG、Remotion/React、GSAP/HTML、Manim、Motion Canvas 风格）。
- 不适用：实拍、AI 生成视频、3D 渲染为主的片子（只能蒸馏包装层，`precheck` 会拦下）。
- 目标是**高保真复刻风格**，不是像素级一致。对用户也只能这么说。

## 开工前必须遵守（硬规则）

1. **版权**：只处理用户有权参考的视频。只学风格和结构，不搬运原片素材、截图、logo、配音、配乐、字体文件和原文案。运行 `analyze` / `all` 需要 `RIGHTS_OK=1` 或 `--rights-ok`，表示用户已确认。
2. **事实和推测分开**：tokens 每个字段都带 `seen`（视频里直接测到）/ `inferred`（推测）/ `unknown`（测不到）。汇报时不得把推测说成事实；没看过画面就不要说看过。
3. **字体身份一律 unknown**，只用免费可商用替代（`references/font-alternatives.md`）。
4. **数据要真实**，否则在画面上标“示例数据”。证据截图框（`evidence`）只能放有权素材，并在 `source` 写来源。
5. 不调用付费服务、不注册账号、不对外发布。

## 环境

需要：Python 3.10+、Node 18+、FFmpeg、Chrome/Chromium；可选 Tesseract（含 `chi_sim` 中文包，没有它 OCR 相关项会记为测不了）。

```bash
cd skills/code-video-style-distill          # 下文 $T 指这个目录
export T="$PWD"
python3 -m venv .venv && .venv/bin/pip install opencv-python-headless numpy scikit-learn pillow matplotlib jsonschema scipy pyyaml
cd template && npm install && cd ..
```

Windows 用 PowerShell，把 `.venv/bin/python` 换成 `.venv\Scripts\python.exe`，完整步骤见 `SKILL.md` 的 “Windows（PowerShell）完整步骤”。统一入口是 `cvsd.py`（跨平台）；`run.sh` 只是它的壳，参数原样透传。

## 最短路径（推荐）

```bash
# 阶段 1：预检 + 拆解，然后停在人工判断点
RIGHTS_OK=1 .venv/bin/python cvsd.py all /abs/ref.mp4 /abs/work my-style /abs/script.json

# ——人工判断点：AI 必须用看图能力打开 work 里的 contact_sheet 和关键帧，
#    核对配色/版式/元件，把纠正写进 /abs/work/overrides.json（已自动生成空模板）——

# 阶段 2：迭代，每轮 = distill → checklist → 静帧预检 → 全片渲染 → compare
.venv/bin/python cvsd.py resume /abs/ref.mp4 /abs/work my-style /abs/script.json --rounds 3
```

- 只有确认不需要人工判断时才加 `--skip-review`；`precheck` 判定为实拍/AI/3D（`live_ai_3d`）会停下，确需继续才加 `--force`。
- 轮与轮之间会等你按 `gap-report.md` 修改 `overrides.json`；无人值守时加 `--no-wait`。

## 分步命令（需要单独控制时）

| 步骤 | 命令 | 产出 |
|---|---|---|
| 0 预检 | `cvsd.py precheck <ref.mp4> <work>` | 是否为代码/模板生成 |
| 1 拆解 | `cvsd.py analyze <ref.mp4> <work> [--no-ocr --no-videomd --scene-threshold 0.4]` | 镜头切分、关键帧、色板、运动能量、OCR、音频节拍、VIDEO.md |
| 2 蒸馏 | `cvsd.py distill <work> <style-name> [--overrides overrides.json] [--taxonomy 文件]` | `styles/<style-name>/style-tokens.json` |
| 3 验收清单 | `cvsd.py checklist <work> <script.json>` | `acceptance.json`（**必须在第一次渲染前生成**，阈值和基准就此冻结） |
| 4 静帧预检 | `cvsd.py stillcheck <work> <script.json>` | 3 张定格帧，只查色板和版式，不过就非 0 退出 |
| 5 渲染 | `cvsd.py render <work> <script.json> <out.mp4> [--renderer ...]` | 成片 mp4 |
| 6 对比 | `cvsd.py compare <ref.mp4> <work> <replica.mp4>` | `report.md`、`gap-report.md`、并排图、迭代账本 |
| 导出 | `cvsd.py export-index` | `styles/asset-index.json`（给动效资源库） |
| 测试音轨 | `cvsd.py beat out.wav --bpm 100 --seconds 60` | ffmpeg 生成的节拍音 |

## 换选题：写 script.json

内容和风格分开：`script.json` 只放文字、数据、时长、音频；颜色、字体、动效全在 tokens 里，混写会被拒绝。9 种段落：

`title` 标题卡 · `bullets` 要点 · `code` 代码打字机 · `bars` 柱状图 · `stat` 大数字 · `evidence` 证据截图框 · `timeline` 时间线 · `compare` 对比双栏 · `flow` 流程图

字段全表见 `template/README.md`，完整例子见 `examples/topic-demo-9/script.json`。`**词**` 表示关键词高亮；字幕会自动按每条 ≤18 字断行。

## 渲染引擎（可切换）

`--renderer` 或环境变量 `CVSD_RENDERER`：

| 引擎 | 许可 | 段落支持 | 备注 |
|---|---|---|---|
| `remotion`（默认） | 自定义许可：个人及 ≤3 人公司免费，更大团队需商业授权 | 9 种 | 最稳 |
| `hyperframes` | Apache-2.0 | 9 种 | 最快；需自行安装 |
| `lemo` | MIT（lemo-opuscar） | 9 种 | 需自行安装；入场时长测量会偏一帧，见已知局限 |
| `motion-canvas` | MIT | 5 种（title/bullets/code/bars/stat） | 最慢 |

## 怎么判断做完了（验收规则）

- 清单分 `must` / `should` / `out` 三档。**只有 `seen` 字段能留在 must**；`inferred` 自动降到 should；`unknown` 降到 should 并记 not-testable（不算通过，也不算分）。
- **DONE**：降级后的所有 must 项，在**连续两轮、两个不同成片文件**（sha256 不同）上都通过。同一个文件比两次不算。
- **STALLED**：连续 3 轮分数没进展，停下来交给人判断，不要硬调。
- `gap-report.md` 会给每个失败项的修改建议；inferred 项只提示“先目测确认再调参”，不要盲目追数。

## 汇报给用户时

- 报总分、must 是否全过、账本状态（ITERATING / DONE / STALLED）、未通过项和原因。
- 附 `compare_rN/sidebyside_grid.png` 并排对比图。
- 区分哪些是测到的、哪些是推测的；没实跑的东西不要说“通过”。

## 已知局限（别对用户夸大）

- 缓动曲线是近似拟合；入场时长按能量阈值测，通常偏短 10–25%。
- OCR 读不出超大标题，字号阶梯里的 display 常是推测值；字体身份测不出。
- 转场只能区分 slide / zoom / 其它，wipe 和 fade 要目测。
- 元件检测是像素启发式：纯色截图、竖向时间线、菱形或曲线连线的流程图认不出。
- 自带测试用的参考片是工具自己渲染的，分数偏乐观；真实外部视频的表现需要实测。

## 测试

```bash
.venv/bin/python tests/test_cli.py      # 26 项，约 2.5 分钟
```

## 出处

借鉴思路的开源项目和许可证见 `THIRD_PARTY_NOTICES.md`。
