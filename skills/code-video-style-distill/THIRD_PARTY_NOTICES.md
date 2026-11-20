# Third-party ideas and notices

本工具目录里的代码全部是自写的 Python / TypeScript；下列项目只借了**思路或结构**，没有安装、没有作为依赖、没有复制源码。
来源核实见 `/workspace/ip-team/deliverables/video-reverse/REA调研-可复用点.md`（第一轮 + 第二轮补充）。

| 项目 | 许可证 | 借了什么 | 用在哪 |
|---|---|---|---|
| [aicodeking/leanrea](https://github.com/aicodeking/leanrea) | MIT | 证据标记规则：seen / inferred / unknown，unknown ≠ 不存在 | `scripts/distill.py` provenance、`schema/style-tokens.schema.json` |
| [obaid1dev/dea](https://github.com/obaid1dev/dea) | MIT | token 结构（value + evidence + confidence、motion.easings / keyframes、unknowns）、字体替代表、条带式风格对比 | `scripts/distill.py`、`references/font-alternatives.md`、`scripts/compare.py` band_similarity |
| [Speedrunlab/reverse-engineer-anything-self-learning-loop](https://github.com/Speedrunlab/reverse-engineer-anything-self-learning-loop) | MIT（© 2026 Speedrun AI Labs Pty Ltd） | parity checklist 的 must/should/out 分档、gap report、run ledger、“must 连续两轮通过才算完成”、分数不动就停 | `scripts/checklist.py`、`scripts/compare.py` |
| [morluto/rea](https://github.com/morluto/rea) | MIT | 视觉主张合同（不可比较记 unknown，不算 pass）；`src/domain/pngVisualDiff.ts` 的逐像素通道阈值 + 变化比例 + 尺寸不一致记 mismatch | `scripts/compare.py` pixel_channel_diff（Python 重写） |
| [JuneYaooo/rea-video](https://github.com/JuneYaooo/rea-video) | Apache-2.0 | 先判镜头是否代码/模板生成再定复刻路线；并排对比片作为交付形态 | `scripts/precheck.py`、`scripts/compare.py` sidebyside.mp4 |
| [JuneYaooo/capsule-cinema](https://github.com/JuneYaooo/capsule-cinema) | Apache-2.0 | “配方 / 当期内容”分离纪律 | `template/render.mjs` 解耦检查、SKILL.md |
| [videomd/videomd](https://github.com/videomd/videomd) | 规范与文档 CC BY 4.0；代码/Schema Apache-2.0 | VIDEO.md v1 包格式（按公开规范自写导出器） | `scripts/videomd_export.py` |

VIDEO.md 规范署名（CC BY 4.0）：“VIDEO.md specification” © videomd contributors, https://github.com/videomd/videomd ，许可 https://creativecommons.org/licenses/by/4.0/ 。导出器若用本地只读副本 `/workspace/ip-team/research/rea/videomd/src` 的参考校验器做符合性检查，只是 import 运行，不安装。

本工具与官方 REA、rea-video 等项目无隶属关系，不得宣传成官方工具。

## 运行时依赖与渲染后端

| 组件 | 许可证 | 说明 |
|---|---|---|
| FFmpeg | LGPL/GPL（看构建） | 拆帧、编码、并排片、节拍音轨（本机命令行调用，不打包） |
| OpenCV / NumPy / scikit-learn / Pillow / SciPy | Apache-2.0 / BSD / HPND | 分析脚本（pip 安装在 .venv） |
| Tesseract OCR | Apache-2.0 | 文字与字号（本机命令行调用） |
| Remotion 4 | Remotion License（公司自有许可证，个人和小团队免费，较大公司商用需买授权） | 当前默认渲染后端 `template/`；通过 `scripts/renderers.py` 接口调用，可替换 |
| Motion Canvas（MIT）/ HyperFrames（Apache-2.0） | — | 尚未接入，只在 `scripts/renderers.py` 预留后端位置；未使用其代码 |

知识片元件（evidence / timeline / compare / flow）的组件与像素检测器（`template/src/components/{Evidence,Timeline,CompareColumns,Flow}.tsx`、`scripts/components_detect.py`）为本工具自写；分类编号来自用户自己的动效库分类表 `/workspace/ip-team/deliverables/motion/taxonomy-from-user.md`。
`examples/assets/placeholder-evidence-*.png` 由代码生成，无第三方素材。
