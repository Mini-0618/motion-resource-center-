# 动效资源候选清单 v1（GitHub 开源项目与官方示例）

- 查询日期：2026-11-20（北京时间）；数据来源：GitHub API 实时查询（cursor-github connector）。
- 当前版本：批次 2（26 类全部有候选；主流项目 + 各类代表项目）；后续批次：核对 README 安装命令、补充各类深度（重点 UI-03/UI-04/UI-06/V-01/V-02）

- 总条数：**277**（去重后独立仓库 234 个；同一仓库可同时列入不同分类的条目已在“兼属分类”标注，主分类内不重复）。
- 分类依据：用户本人提供的 26 类分类原文（`taxonomy-from-user.md`）。
- 状态口径：只有“已发现”和“已核实来源”。**已核实来源** = 该仓库经 GitHub API 单独读取，仓库存在，星标/许可证/最近推送来自实时结果；**已发现** = 仅从实时搜索结果读到元数据。两者都**不代表可用、可复现或可商用**，未逐条阅读 README、未运行任何代码。
- “最近提交日期”取 GitHub API `pushed_at`（最近一次推送，可能含非默认分支），不是默认分支最新提交日期。
- 预览、帧率、测试结果、安装/启动命令：均为“未验证”，不得当作已验证信息。

## 一、按类别汇总

| 分类 | 名称 | 条数 | 重点类 | 覆盖 |
|---|---|---|---|---|
| UI-01 | 基础交互动效 | 12 |  | 已覆盖 |
| UI-02 | 页面与布局转场 | 10 |  | 已覆盖 |
| UI-03 | 毛玻璃与视觉材质 | 19 | ★ | 已覆盖 |
| UI-04 | 数据仪表盘动效 | 22 | ★ | 已覆盖 |
| UI-05 | 3D 空间界面 | 11 |  | 已覆盖 |
| UI-06 | AI 智能体专属动效 | 14 | ★ | 已覆盖 |
| UI-07 | 操作系统级窗口动效 | 7 |  | 已覆盖 |
| UI-08 | 科技感与背景动效 | 7 |  | 已覆盖 |
| UI-09 | 信息与内容组件 | 10 |  | 已覆盖 |
| UI-10 | 移动端与响应式动效 | 7 |  | 已覆盖 |
| UI-11 | SVG、Lottie、Rive 与图标动画 | 15 |  | 已覆盖 |
| V-01 | 文字与动态排版 | 12 | ★ | 已覆盖 |
| V-02 | 数据图表动画 | 17 | ★ | 已覆盖 |
| V-03 | 信息图与逻辑解释 | 7 |  | 已覆盖 |
| V-04 | 新闻、论文与证据展示 | 7 |  | 已覆盖 |
| V-05 | 产品演示与屏幕录制 | 7 |  | 已覆盖 |
| V-06 | 人物、故事与纪录片叙事 | 6 |  | 已覆盖 |
| V-07 | 电影化转场 | 5 |  | 已覆盖 |
| V-08 | 电影化视觉效果 | 6 |  | 已覆盖 |
| V-09 | 2.5D、视差与镜头运动 | 7 |  | 已覆盖 |
| V-10 | MG 图形动画 | 12 |  | 已覆盖 |
| V-11 | 程序化视觉与生成艺术 | 11 |  | 已覆盖 |
| V-12 | 3D 动画与场景 | 12 |  | 已覆盖 |
| V-13 | 字幕、配音与音画同步 | 15 |  | 已覆盖 |
| V-14 | 剪辑结构与镜头节奏 | 9 |  | 已覆盖 |
| V-15 | 封面、片头、片尾与品牌包装 | 10 |  | 已覆盖 |

## 二、各类候选明细

### UI-01 基础交互动效（12 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-01-001 | [motion](https://github.com/motiondivision/motion) | MIT | 35372 | 2026-11-19 | 已核实来源 | 无 |
| UI-01-002 | [motion-primitives](https://github.com/ibelick/motion-primitives) | MIT | 6987 | 2026-09-28 | 已核实来源 | 无 |
| UI-01-003 | [auto-animate](https://github.com/formkit/auto-animate) | MIT | 13976 | 2026-11-07 | 已核实来源 | 无 |
| UI-01-004 | [pragmatic-drag-and-drop](https://github.com/atlassian/pragmatic-drag-and-drop) | NOASSERTION | 12798 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-01-005 | [dnd-kit](https://github.com/clauderic/dnd-kit) | MIT | 17816 | 2026-10-31 | 已核实来源 | 无 |
| UI-01-006 | [react-spring](https://github.com/pmndrs/react-spring) | MIT | 29318 | 2026-11-01 | 已核实来源 | 无 |
| UI-01-007 | [use-gesture](https://github.com/pmndrs/use-gesture) | MIT | 9626 | 2024-07-15 | 已核实来源 | 超过 12 个月无推送 |
| UI-01-008 | [animate.css](https://github.com/animate-css/animate.css) | NOASSERTION | 83031 | 2024-07-29 | 已核实来源 | 自定义/多重许可证（需人工核查）；超过 12 个月无推送 |
| UI-01-009 | [Hover](https://github.com/IanLunn/Hover) | NOASSERTION | 29414 | 2023-10-28 | 已核实来源 | 自定义/多重许可证（需人工核查）；超过 12 个月无推送 |
| UI-01-010 | [SpinKit](https://github.com/tobiasahlin/SpinKit) | MIT | 19309 | 2020-08-01 | 已核实来源 | 超过 12 个月无推送 |
| UI-01-011 | [svg-spinners](https://github.com/n3r4zzurr0/svg-spinners) | MIT | 7021 | 2023-05-05 | 已核实来源 | 超过 12 个月无推送 |
| UI-01-012 | [react-loading-skeleton](https://github.com/dvtng/react-loading-skeleton) | MIT | 4213 | 2026-03-05 | 已核实来源 | 无 |

### UI-02 页面与布局转场（10 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-02-001 | [next-view-transitions](https://github.com/shuding/next-view-transitions) | MIT | 2382 | 2026-03-06 | 已核实来源 | 无 |
| UI-02-002 | [barba](https://github.com/barbajs/barba) | MIT | 13002 | 2024-12-02 | 已核实来源 | 超过 12 个月无推送 |
| UI-02-003 | [swup](https://github.com/swup/swup) | MIT | 5252 | 2026-11-03 | 已核实来源 | 无 |
| UI-02-004 | [locomotive-scroll](https://github.com/locomotivemtl/locomotive-scroll) | MIT | 8896 | 2026-11-16 | 已核实来源 | 无 |
| UI-02-005 | [lenis](https://github.com/darkroomengineering/lenis) | MIT | 17371 | 2026-11-19 | 已核实来源 | 无 |
| UI-02-006 | [aos](https://github.com/michalsnik/aos) | MIT | 28056 | 2024-03-26 | 已核实来源 | 超过 12 个月无推送 |
| UI-02-007 | [rellax](https://github.com/dixonandmoe/rellax) | MIT | 7115 | 2024-08-24 | 已核实来源 | 超过 12 个月无推送 |
| UI-02-008 | [vaul](https://github.com/emilkowalski/vaul) | MIT | 8755 | 2025-10-03 | 已核实来源 | 超过 12 个月无推送 |
| UI-02-009 | [tldraw](https://github.com/tldraw/tldraw) | NOASSERTION | 51495 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-02-010 | [motion](https://github.com/motiondivision/motion) | MIT | 35372 | 2026-11-19 | 已核实来源 | 无 |

### UI-03 毛玻璃与视觉材质（19 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-03-001 | [liquid-glass-react](https://github.com/rdev/liquid-glass-react) | MIT | 6746 | 2025-06-13 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产）；超过 12 个月无推送 |
| UI-03-002 | [liquid-dom](https://github.com/AndrewPrifer/liquid-dom) | MIT | 2604 | 2026-09-06 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-003 | [liquid-glass-js](https://github.com/dashersw/liquid-glass-js) | MIT | 1829 | 2025-06-12 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产）；超过 12 个月无推送 |
| UI-03-004 | [liquidGL](https://github.com/naughtyduk/liquidGL) | NOASSERTION | 1087 | 2026-10-01 | 已核实来源 | 自定义/多重许可证（需人工核查）；含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-005 | [liquidglass](https://github.com/ybouane/liquidglass) | 无（未检出） | 648 | 2026-09-30 | 已核实来源 | 许可证不清（GitHub 未检出）；含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-006 | [liquid-glass](https://github.com/archisvaze/liquid-glass) | MIT | 843 | 2026-11-10 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-007 | [liquid-glass](https://github.com/nikdelvin/liquid-glass) | MIT | 119 | 2025-12-24 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-008 | [vaso](https://github.com/huozhi/vaso) | 无（未检出） | 389 | 2026-11-15 | 已核实来源 | 许可证不清（GitHub 未检出）；含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-009 | [liquid-glass-vue](https://github.com/WXperia/liquid-glass-vue) | 无（未检出） | 295 | 2025-07-04 | 已核实来源 | 许可证不清（GitHub 未检出）；含苹果品牌/风格参考（需确认不含 Apple 资产）；超过 12 个月无推送 |
| UI-03-010 | [plasma-ui](https://github.com/CruxGarden/plasma-ui) | MIT | 337 | 2026-11-01 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-011 | [glass-ui](https://github.com/themesberg/glass-ui) | 无（未检出） | 413 | 2026-02-27 | 已核实来源 | 许可证不清（GitHub 未检出） |
| UI-03-012 | [css.glass](https://github.com/miketromba/css.glass) | 无（未检出） | 458 | 2025-09-15 | 已核实来源 | 许可证不清（GitHub 未检出）；超过 12 个月无推送 |
| UI-03-013 | [liquid-glass-effect-macos](https://github.com/lucasromerodb/liquid-glass-effect-macos) | 无（未检出） | 827 | 2025-06-10 | 已核实来源 | 许可证不清（GitHub 未检出）；含苹果品牌/风格参考（需确认不含 Apple 资产）；超过 12 个月无推送 |
| UI-03-014 | [dashdot](https://github.com/MauriceNino/dashdot) | MIT | 3756 | 2026-11-15 | 已核实来源 | 无 |
| UI-03-015 | [Cloudy](https://github.com/skydoves/Cloudy) | Apache-2.0 | 1293 | 2026-09-13 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-016 | [AndroidLiquidGlass](https://github.com/Kyant0/AndroidLiquidGlass) | Apache-2.0 | 4719 | 2026-11-12 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-017 | [liquid_glass_widgets](https://github.com/sdegenaar/liquid_glass_widgets) | MIT | 864 | 2026-11-19 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-018 | [liquid-glass](https://github.com/callstack/liquid-glass) | MIT | 1737 | 2026-09-15 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-03-019 | [LiquidGlassReference](https://github.com/conorluddy/LiquidGlassReference) | 无（未检出） | 345 | 2026-03-08 | 已核实来源 | 许可证不清（GitHub 未检出）；含苹果品牌/风格参考（需确认不含 Apple 资产） |

### UI-04 数据仪表盘动效（22 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-04-001 | [echarts](https://github.com/apache/echarts) | Apache-2.0 | 67755 | 2026-10-13 | 已核实来源 | 无 |
| UI-04-002 | [echarts-examples](https://github.com/apache/echarts-examples) | Apache-2.0 | 402 | 2026-10-29 | 已核实来源 | 无 |
| UI-04-003 | [d3](https://github.com/d3/d3) | ISC | 113973 | 2026-11-03 | 已核实来源 | 无 |
| UI-04-004 | [plot](https://github.com/observablehq/plot) | ISC | 5431 | 2026-11-05 | 已核实来源 | 无 |
| UI-04-005 | [Chart.js](https://github.com/chartjs/Chart.js) | MIT | 67813 | 2026-11-17 | 已核实来源 | 无 |
| UI-04-006 | [recharts](https://github.com/recharts/recharts) | MIT | 27723 | 2026-11-19 | 已核实来源 | 无 |
| UI-04-007 | [visx](https://github.com/airbnb/visx) | MIT | 21115 | 2026-06-22 | 已核实来源 | 无 |
| UI-04-008 | [nivo](https://github.com/plouc/nivo) | MIT | 14143 | 2026-07-21 | 已核实来源 | 无 |
| UI-04-009 | [tremor](https://github.com/tremorlabs/tremor) | Apache-2.0 | 3704 | 2025-10-10 | 已核实来源 | 超过 12 个月无推送 |
| UI-04-010 | [number-flow](https://github.com/barvian/number-flow) | MIT | 7827 | 2026-09-20 | 已核实来源 | 无 |
| UI-04-011 | [uPlot](https://github.com/leeoniya/uPlot) | MIT | 10662 | 2026-11-17 | 已核实来源 | 无 |
| UI-04-012 | [apexcharts.js](https://github.com/apexcharts/apexcharts.js) | NOASSERTION | 15189 | 2026-11-18 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-04-013 | [G2](https://github.com/antvis/G2) | MIT | 12670 | 2026-11-14 | 已核实来源 | 无 |
| UI-04-014 | [gridstack.js](https://github.com/gridstack/gridstack.js) | MIT | 9257 | 2026-11-17 | 已核实来源 | 无 |
| UI-04-015 | [perspective](https://github.com/perspective-dev/perspective) | Apache-2.0 | 11605 | 2026-11-19 | 已核实来源 | 无 |
| UI-04-016 | [grafana](https://github.com/grafana/grafana) | AGPL-3.0 | 78003 | 2026-11-20 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| UI-04-017 | [superset](https://github.com/apache/superset) | Apache-2.0 | 75582 | 2026-11-20 | 已核实来源 | 无 |
| UI-04-018 | [langfuse](https://github.com/langfuse/langfuse) | NOASSERTION | 37641 | 2026-11-20 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-04-019 | [free-react-tailwind-admin-dashboard](https://github.com/TailAdmin/free-react-tailwind-admin-dashboard) | MIT | 1307 | 2026-11-17 | 已核实来源 | 无 |
| UI-04-020 | [dashboardblocks](https://github.com/LGLabGreg/dashboardblocks) | MIT | 32 | 2026-11-19 | 已核实来源 | 无 |
| UI-04-021 | [microcharts](https://github.com/ganapativs/microcharts) | MIT | 209 | 2026-11-19 | 已核实来源 | 无 |
| UI-04-022 | [chartbrew](https://github.com/chartbrew/chartbrew) | NOASSERTION | 4096 | 2026-11-14 | 已核实来源 | 自定义/多重许可证（需人工核查） |

### UI-05 3D 空间界面（11 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-05-001 | [three.js](https://github.com/mrdoob/three.js) | MIT | 118971 | 2026-11-20 | 已核实来源 | 无 |
| UI-05-002 | [react-three-fiber](https://github.com/pmndrs/react-three-fiber) | MIT | 33838 | 2026-10-21 | 已核实来源 | 无 |
| UI-05-003 | [drei](https://github.com/pmndrs/drei) | MIT | 10178 | 2026-11-17 | 已核实来源 | 无 |
| UI-05-004 | [3d-force-graph](https://github.com/vasturiano/3d-force-graph) | MIT | 6581 | 2026-11-05 | 已核实来源 | 无 |
| UI-05-005 | [react-force-graph](https://github.com/vasturiano/react-force-graph) | MIT | 3373 | 2026-09-29 | 已核实来源 | 无 |
| UI-05-006 | [globe.gl](https://github.com/vasturiano/globe.gl) | MIT | 3237 | 2026-08-22 | 已核实来源 | 无 |
| UI-05-007 | [uikit](https://github.com/pmndrs/uikit) | NOASSERTION | 3270 | 2026-10-27 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-05-008 | [G6](https://github.com/antvis/G6) | MIT | 12396 | 2026-11-13 | 已核实来源 | 无 |
| UI-05-009 | [vis-network](https://github.com/visjs/vis-network) | Apache-2.0 | 3642 | 2026-11-19 | 已核实来源 | 无 |
| UI-05-010 | [cytoscape.js](https://github.com/cytoscape/cytoscape.js) | MIT | 11295 | 2026-11-10 | 已核实来源 | 无 |
| UI-05-011 | [postprocessing](https://github.com/pmndrs/postprocessing) | Zlib | 2986 | 2026-11-01 | 已核实来源 | 无 |

### UI-06 AI 智能体专属动效（14 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-06-001 | [ai](https://github.com/vercel/ai) | NOASSERTION | 28094 | 2026-11-20 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-06-002 | [assistant-ui](https://github.com/assistant-ui/assistant-ui) | MIT | 13341 | 2026-11-20 | 已核实来源 | 无 |
| UI-06-003 | [CopilotKit](https://github.com/CopilotKit/CopilotKit) | MIT | 38824 | 2026-11-20 | 已核实来源 | 无 |
| UI-06-004 | [ag-ui](https://github.com/ag-ui-protocol/ag-ui) | MIT | 20638 | 2026-11-19 | 已核实来源 | 无 |
| UI-06-005 | [ai-elements](https://github.com/vercel/ai-elements) | NOASSERTION | 2531 | 2026-10-14 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-06-006 | [streamdown](https://github.com/vercel/streamdown) | NOASSERTION | 5778 | 2026-11-18 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-06-007 | [thinking-orbs](https://github.com/Jakubantalik/thinking-orbs) | MIT | 4051 | 2026-08-16 | 已核实来源 | 无 |
| UI-06-008 | [gaia-ui](https://github.com/theexperiencecompany/gaia-ui) | MIT | 225 | 2026-09-03 | 已核实来源 | 无 |
| UI-06-009 | [xyflow](https://github.com/xyflow/xyflow) | MIT | 39088 | 2026-11-19 | 已核实来源 | 无 |
| UI-06-010 | [langflow](https://github.com/langflow-ai/langflow) | MIT | 156782 | 2026-11-20 | 已核实来源 | 无 |
| UI-06-011 | [n8n](https://github.com/n8n-io/n8n) | NOASSERTION | 211434 | 2026-11-20 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-06-012 | [open-webui](https://github.com/open-webui/open-webui) | NOASSERTION | 159104 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-06-013 | [NextChat](https://github.com/ChatGPTNextWeb/NextChat) | MIT | 88988 | 2026-10-20 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-06-014 | [Flowise](https://github.com/FlowiseAI/Flowise) | NOASSERTION | 55574 | 2026-08-13 | 已核实来源 | 自定义/多重许可证（需人工核查）；仓库已归档 |

### UI-07 操作系统级窗口动效（7 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-07-001 | [daedalOS](https://github.com/DustinBrett/daedalOS) | MIT | 13102 | 2026-10-22 | 已核实来源 | 无 |
| UI-07-002 | [macos-web](https://github.com/PuruVJ/macos-web) | MIT | 2685 | 2026-07-05 | 已核实来源 | 含苹果品牌/风格参考（需确认不含 Apple 资产） |
| UI-07-003 | [winbox](https://github.com/nextapps-de/winbox) | Apache-2.0 | 6457 | 2024-08-15 | 已核实来源 | 超过 12 个月无推送 |
| UI-07-004 | [react-rnd](https://github.com/bokuweb/react-rnd) | MIT | 4326 | 2026-05-12 | 已核实来源 | 无 |
| UI-07-005 | [FlexLayout](https://github.com/caplin/FlexLayout) | MIT | 1388 | 2026-11-18 | 已核实来源 | 无 |
| UI-07-006 | [cmdk](https://github.com/dip/cmdk) | MIT | 13166 | 2025-10-29 | 已核实来源 | 超过 12 个月无推送 |
| UI-07-007 | [sonner](https://github.com/emilkowalski/sonner) | MIT | 13239 | 2026-08-10 | 已核实来源 | 无 |

### UI-08 科技感与背景动效（7 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-08-001 | [magicui](https://github.com/magicuidesign/magicui) | MIT | 23380 | 2026-11-17 | 已核实来源 | 无 |
| UI-08-002 | [tsparticles](https://github.com/tsparticles/tsparticles) | MIT | 9117 | 2026-11-18 | 已核实来源 | 无 |
| UI-08-003 | [shaders](https://github.com/paper-design/shaders) | Apache-2.0 | 3989 | 2026-11-19 | 已核实来源 | 无 |
| UI-08-004 | [vanta](https://github.com/tengbao/vanta) | MIT | 7399 | 2024-03-03 | 已核实来源 | 超过 12 个月无推送 |
| UI-08-005 | [matrix](https://github.com/Rezmason/matrix) | MIT | 3869 | 2025-06-23 | 已核实来源 | 超过 12 个月无推送 |
| UI-08-006 | [react-bits](https://github.com/DavidHDev/react-bits) | NOASSERTION | 52329 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-08-007 | [three.js](https://github.com/mrdoob/three.js) | MIT | 118971 | 2026-11-20 | 已核实来源 | 无 |

### UI-09 信息与内容组件（10 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-09-001 | [shiki](https://github.com/shikijs/shiki) | MIT | 13941 | 2026-11-02 | 已核实来源 | 无 |
| UI-09-002 | [shiki-magic-move](https://github.com/shikijs/shiki-magic-move) | MIT | 1509 | 2026-06-03 | 已核实来源 | 仓库已归档 |
| UI-09-003 | [xterm.js](https://github.com/xtermjs/xterm.js) | MIT | 21369 | 2026-11-16 | 已核实来源 | 无 |
| UI-09-004 | [mermaid](https://github.com/mermaid-js/mermaid) | MIT | 91165 | 2026-11-19 | 已核实来源 | 无 |
| UI-09-005 | [table](https://github.com/TanStack/table) | MIT | 28591 | 2026-11-18 | 已核实来源 | 无 |
| UI-09-006 | [react-window](https://github.com/bvaughn/react-window) | MIT | 17213 | 2026-11-15 | 已核实来源 | 无 |
| UI-09-007 | [masonry](https://github.com/desandro/masonry) | 无（未检出） | 16681 | 2024-06-07 | 已核实来源 | 许可证不清（GitHub 未检出）；超过 12 个月无推送 |
| UI-09-008 | [TimelineJS3](https://github.com/NUKnightLab/TimelineJS3) | MPL-2.0 | 3236 | 2026-11-16 | 已核实来源 | 弱 Copyleft（MPL，需合规评估） |
| UI-09-009 | [xyflow](https://github.com/xyflow/xyflow) | MIT | 39088 | 2026-11-19 | 已核实来源 | 无 |
| UI-09-010 | [streamdown](https://github.com/vercel/streamdown) | NOASSERTION | 5778 | 2026-11-18 | 已核实来源 | 自定义/多重许可证（需人工核查） |

### UI-10 移动端与响应式动效（7 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-10-001 | [react-native-reanimated](https://github.com/software-mansion/react-native-reanimated) | MIT | 11084 | 2026-11-19 | 已核实来源 | 无 |
| UI-10-002 | [react-native-gesture-handler](https://github.com/software-mansion/react-native-gesture-handler) | MIT | 6807 | 2026-11-19 | 已核实来源 | 无 |
| UI-10-003 | [react-native-skia](https://github.com/wcandillon/react-native-skia) | MIT | 8784 | 2026-11-19 | 已核实来源 | 无 |
| UI-10-004 | [react-native-bottom-sheet](https://github.com/gorhom/react-native-bottom-sheet) | MIT | 9113 | 2026-05-09 | 已核实来源 | 无 |
| UI-10-005 | [swiper](https://github.com/nolimits4web/swiper) | MIT | 41908 | 2026-10-30 | 已核实来源 | 无 |
| UI-10-006 | [ionic-framework](https://github.com/ionic-team/ionic-framework) | MIT | 52771 | 2026-11-20 | 已核实来源 | 无 |
| UI-10-007 | [flash-list](https://github.com/Shopify/flash-list) | MIT | 7249 | 2026-10-01 | 已核实来源 | 无 |

### UI-11 SVG、Lottie、Rive 与图标动画（15 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| UI-11-001 | [lottie-web](https://github.com/airbnb/lottie-web) | MIT | 32524 | 2025-09-01 | 已核实来源 | 超过 12 个月无推送 |
| UI-11-002 | [dotlottie-web](https://github.com/LottieFiles/dotlottie-web) | MIT | 951 | 2026-11-18 | 已核实来源 | 无 |
| UI-11-003 | [rive-react](https://github.com/rive-app/rive-react) | MIT | 1191 | 2026-11-19 | 已核实来源 | 无 |
| UI-11-004 | [rive-wasm](https://github.com/rive-app/rive-wasm) | MIT | 1031 | 2026-11-19 | 已核实来源 | 无 |
| UI-11-005 | [lottie-ios](https://github.com/airbnb/lottie-ios) | Apache-2.0 | 26945 | 2026-10-06 | 已核实来源 | 无 |
| UI-11-006 | [lottie-android](https://github.com/airbnb/lottie-android) | Apache-2.0 | 35774 | 2026-02-15 | 已核实来源 | 无 |
| UI-11-007 | [lottie-react](https://github.com/LottieFiles/lottie-react) | MIT | 798 | 2026-04-08 | 已核实来源 | 仓库已归档 |
| UI-11-008 | [thorvg](https://github.com/thorvg/thorvg) | MIT | 1926 | 2026-11-20 | 已核实来源 | 无 |
| UI-11-009 | [vivus](https://github.com/maxwellito/vivus) | MIT | 15484 | 2022-07-06 | 已核实来源 | 超过 12 个月无推送 |
| UI-11-010 | [svg.js](https://github.com/svgdotjs/svg.js) | NOASSERTION | 11944 | 2026-08-04 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-11-011 | [lucide](https://github.com/lucide-icons/lucide) | NOASSERTION | 25870 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| UI-11-012 | [icons](https://github.com/pqoqubbw/icons) | MIT | 8303 | 2026-11-15 | 已核实来源 | 无 |
| UI-11-013 | [progressbar.js](https://github.com/kimmobrunfeldt/progressbar.js) | MIT | 7845 | 2024-11-02 | 已核实来源 | 超过 12 个月无推送 |
| UI-11-014 | [anime](https://github.com/juliangarnier/anime) | MIT | 74909 | 2026-11-02 | 已核实来源 | 无 |
| UI-11-015 | [mojs](https://github.com/mojs/mojs) | MIT | 18933 | 2026-07-30 | 已核实来源 | 无 |

### V-01 文字与动态排版（12 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-01-001 | [remotion](https://github.com/remotion-dev/remotion) | NOASSERTION | 74360 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-01-002 | [template-tiktok](https://github.com/remotion-dev/template-tiktok) | 无（未检出） | 308 | 2026-11-09 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-01-003 | [template-code-hike](https://github.com/remotion-dev/template-code-hike) | 无（未检出） | 223 | 2026-11-02 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-01-004 | [remocn](https://github.com/Remocn/remocn) | MIT | 1809 | 2026-11-19 | 已核实来源 | 无 |
| V-01-005 | [remotion-templates](https://github.com/reactvideoeditor/remotion-templates) | 无（未检出） | 296 | 2026-04-21 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-01-006 | [motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | 20072 | 2026-07-02 | 已核实来源 | 无 |
| V-01-007 | [revideo](https://github.com/midrender/revideo) | MIT | 4218 | 2026-07-15 | 已核实来源 | 无 |
| V-01-008 | [GSAP](https://github.com/greensock/GSAP) | 无（未检出） | 30958 | 2026-11-04 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-01-009 | [anime](https://github.com/juliangarnier/anime) | MIT | 74909 | 2026-11-02 | 已核实来源 | 无 |
| V-01-010 | [typed.js](https://github.com/mattboldt/typed.js) | NOASSERTION | 16274 | 2026-01-25 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-01-011 | [source-han-sans](https://github.com/adobe-fonts/source-han-sans) | NOASSERTION | 17490 | 2025-06-25 | 已核实来源 | 自定义/多重许可证（需人工核查）；超过 12 个月无推送 |
| V-01-012 | [LxgwWenKai](https://github.com/lxgw/LxgwWenKai) | OFL-1.1 | 27122 | 2026-11-19 | 已核实来源 | 无 |

### V-02 数据图表动画（17 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-02-001 | [manim](https://github.com/ManimCommunity/manim) | MIT | 42703 | 2026-11-17 | 已核实来源 | 无 |
| V-02-002 | [manim](https://github.com/3b1b/manim) | MIT | 96689 | 2026-09-09 | 已核实来源 | 无 |
| V-02-003 | [bar_chart_race](https://github.com/dexplo/bar_chart_race) | MIT | 1452 | 2024-06-27 | 已核实来源 | 超过 12 个月无推送 |
| V-02-004 | [vega-lite](https://github.com/vega/vega-lite) | BSD-3-Clause | 5562 | 2026-11-13 | 已核实来源 | 无 |
| V-02-005 | [plotly.js](https://github.com/plotly/plotly.js) | MIT | 18383 | 2026-11-20 | 已核实来源 | 无 |
| V-02-006 | [deck.gl](https://github.com/visgl/deck.gl) | MIT | 14777 | 2026-11-20 | 已核实来源 | 无 |
| V-02-007 | [template-audiogram](https://github.com/remotion-dev/template-audiogram) | 无（未检出） | 279 | 2026-11-16 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-02-008 | [vega](https://github.com/vega/vega) | BSD-3-Clause | 12050 | 2026-11-19 | 已核实来源 | 无 |
| V-02-009 | [plotly.py](https://github.com/plotly/plotly.py) | MIT | 18913 | 2026-11-19 | 已核实来源 | 无 |
| V-02-010 | [gganimate](https://github.com/thomasp85/gganimate) | NOASSERTION | 1984 | 2025-09-04 | 已核实来源 | 自定义/多重许可证（需人工核查）；超过 12 个月无推送 |
| V-02-011 | [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) | NOASSERTION | 12135 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-02-012 | [pyecharts](https://github.com/pyecharts/pyecharts) | MIT | 15780 | 2026-10-26 | 已核实来源 | 无 |
| V-02-013 | [matplotlib](https://github.com/matplotlib/matplotlib) | 无（未检出） | 23491 | 2026-11-20 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-02-014 | [videos](https://github.com/3b1b/videos) | NOASSERTION | 11507 | 2026-11-10 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-02-015 | [echarts](https://github.com/apache/echarts) | Apache-2.0 | 67755 | 2026-10-13 | 已核实来源 | 无 |
| V-02-016 | [d3](https://github.com/d3/d3) | ISC | 113973 | 2026-11-03 | 已核实来源 | 无 |
| V-02-017 | [d3-sankey](https://github.com/d3/d3-sankey) | BSD-3-Clause | 947 | 2023-11-13 | 已核实来源 | 超过 12 个月无推送 |

### V-03 信息图与逻辑解释（7 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-03-001 | [mermaid](https://github.com/mermaid-js/mermaid) | MIT | 91165 | 2026-11-19 | 已核实来源 | 无 |
| V-03-002 | [excalidraw](https://github.com/excalidraw/excalidraw) | MIT | 135980 | 2026-11-19 | 已核实来源 | 无 |
| V-03-003 | [d2](https://github.com/d2lang/d2) | MPL-2.0 | 25866 | 2026-11-20 | 已核实来源 | 弱 Copyleft（MPL，需合规评估） |
| V-03-004 | [xyflow](https://github.com/xyflow/xyflow) | MIT | 39088 | 2026-11-19 | 已核实来源 | 无 |
| V-03-005 | [motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | 20072 | 2026-07-02 | 已核实来源 | 无 |
| V-03-006 | [manim](https://github.com/ManimCommunity/manim) | MIT | 42703 | 2026-11-17 | 已核实来源 | 无 |
| V-03-007 | [d3-sankey](https://github.com/d3/d3-sankey) | BSD-3-Clause | 947 | 2023-11-13 | 已核实来源 | 超过 12 个月无推送 |

### V-04 新闻、论文与证据展示（7 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-04-001 | [rough-notation](https://github.com/rough-stuff/rough-notation) | MIT | 9758 | 2024-03-18 | 已核实来源 | 超过 12 个月无推送 |
| V-04-002 | [playwright](https://github.com/microsoft/playwright) | Apache-2.0 | 100618 | 2026-11-20 | 已核实来源 | 无 |
| V-04-003 | [puppeteer](https://github.com/puppeteer/puppeteer) | Apache-2.0 | 95875 | 2026-11-19 | 已核实来源 | 无 |
| V-04-004 | [pdf.js](https://github.com/mozilla/pdf.js) | Apache-2.0 | 54161 | 2026-11-20 | 已核实来源 | 无 |
| V-04-005 | [shot-scraper](https://github.com/simonw/shot-scraper) | Apache-2.0 | 2609 | 2026-10-14 | 已核实来源 | 无 |
| V-04-006 | [client](https://github.com/hypothesis/client) | NOASSERTION | 743 | 2026-11-17 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-04-007 | [annotorious](https://github.com/annotorious/annotorious) | BSD-3-Clause | 875 | 2026-11-18 | 已核实来源 | 无 |

### V-05 产品演示与屏幕录制（7 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-05-001 | [Cap](https://github.com/CapSoftware/Cap) | NOASSERTION | 25299 | 2026-11-20 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-05-002 | [vhs](https://github.com/charmbracelet/vhs) | MIT | 21347 | 2026-11-06 | 已核实来源 | 无 |
| V-05-003 | [asciinema](https://github.com/asciinema/asciinema) | GPL-3.0 | 17975 | 2026-11-17 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-05-004 | [screenity](https://github.com/alyssaxuu/screenity) | GPL-3.0 | 19002 | 2026-11-08 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-05-005 | [obs-studio](https://github.com/obsproject/obs-studio) | GPL-2.0 | 79776 | 2026-11-20 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-05-006 | [FFmpeg](https://github.com/FFmpeg/FFmpeg) | NOASSERTION | 67653 | 2026-11-20 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-05-007 | [template-code-hike](https://github.com/remotion-dev/template-code-hike) | 无（未检出） | 223 | 2026-11-02 | 已核实来源 | 许可证不清（GitHub 未检出） |

### V-06 人物、故事与纪录片叙事（6 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-06-001 | [TimelineJS3](https://github.com/NUKnightLab/TimelineJS3) | MPL-2.0 | 3236 | 2026-11-16 | 已核实来源 | 弱 Copyleft（MPL，需合规评估） |
| V-06-002 | [StoryMapJS](https://github.com/NUKnightLab/StoryMapJS) | NOASSERTION | 253 | 2026-09-13 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-06-003 | [vis-timeline](https://github.com/visjs/vis-timeline) | NOASSERTION | 2583 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-06-004 | [Gource](https://github.com/acaudwell/Gource) | GPL-3.0 | 13219 | 2026-03-06 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-06-005 | [DepthFlow](https://github.com/BrokenSource/DepthFlow) | AGPL-3.0 | 1592 | 2026-11-13 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-06-006 | [Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | Apache-2.0 | 9179 | 2026-03-24 | 已核实来源 | 无 |

### V-07 电影化转场（5 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-07-001 | [gl-transitions](https://github.com/gl-transitions/gl-transitions) | NOASSERTION | 2261 | 2026-11-18 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-07-002 | [ffmpeg-concat](https://github.com/transitive-bullshit/ffmpeg-concat) | 无（未检出） | 993 | 2026-01-24 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-07-003 | [editly](https://github.com/mifi/editly) | MIT | 5633 | 2025-05-12 | 已核实来源 | 超过 12 个月无推送 |
| V-07-004 | [mlt](https://github.com/mltframework/mlt) | LGPL-2.1 | 1880 | 2026-11-19 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-07-005 | [remocn](https://github.com/Remocn/remocn) | MIT | 1809 | 2026-11-19 | 已核实来源 | 无 |

### V-08 电影化视觉效果（6 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-08-001 | [glfx.js](https://github.com/evanw/glfx.js) | MIT | 3460 | 2023-10-23 | 已核实来源 | 超过 12 个月无推送 |
| V-08-002 | [OpenColorIO](https://github.com/AcademySoftwareFoundation/OpenColorIO) | BSD-3-Clause | 2143 | 2026-10-01 | 已核实来源 | 无 |
| V-08-003 | [Natron](https://github.com/NatronGitHub/Natron) | GPL-2.0 | 5746 | 2026-11-20 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-08-004 | [blender](https://github.com/blender/blender) | NOASSERTION | 22236 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-08-005 | [postprocessing](https://github.com/pmndrs/postprocessing) | Zlib | 2986 | 2026-11-01 | 已核实来源 | 无 |
| V-08-006 | [tsparticles](https://github.com/tsparticles/tsparticles) | MIT | 9117 | 2026-11-18 | 已核实来源 | 无 |

### V-09 2.5D、视差与镜头运动（7 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-09-001 | [DepthFlow](https://github.com/BrokenSource/DepthFlow) | AGPL-3.0 | 1592 | 2026-11-13 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-09-002 | [3d-photo-inpainting](https://github.com/vt-vl-lab/3d-photo-inpainting) | NOASSERTION | 7103 | 2024-08-30 | 已核实来源 | 自定义/多重许可证（需人工核查）；超过 12 个月无推送 |
| V-09-003 | [3d-ken-burns](https://github.com/sniklaus/3d-ken-burns) | NOASSERTION | 1579 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-09-004 | [Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | Apache-2.0 | 9179 | 2026-03-24 | 已核实来源 | 无 |
| V-09-005 | [ml-depth-pro](https://github.com/apple-aiml-research/ml-depth-pro) | NOASSERTION | 5786 | 2026-09-11 | 已核实来源 | 自定义/多重许可证（需人工核查）；含苹果品牌/风格参考（需确认不含 Apple 资产） |
| V-09-006 | [rellax](https://github.com/dixonandmoe/rellax) | MIT | 7115 | 2024-08-24 | 已核实来源 | 超过 12 个月无推送 |
| V-09-007 | [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) | NOASSERTION | 12135 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |

### V-10 MG 图形动画（12 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-10-001 | [theatre](https://github.com/theatre-js/theatre) | Apache-2.0 | 13067 | 2024-08-14 | 已核实来源 | 超过 12 个月无推送 |
| V-10-002 | [remotion](https://github.com/remotion-dev/remotion) | NOASSERTION | 74360 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-10-003 | [motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | 20072 | 2026-07-02 | 已核实来源 | 无 |
| V-10-004 | [revideo](https://github.com/midrender/revideo) | MIT | 4218 | 2026-07-15 | 已核实来源 | 无 |
| V-10-005 | [fframes](https://github.com/dmtrKovalenko/fframes) | MIT | 3112 | 2026-11-15 | 已核实来源 | 无 |
| V-10-006 | [remocn](https://github.com/Remocn/remocn) | MIT | 1809 | 2026-11-19 | 已核实来源 | 无 |
| V-10-007 | [hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | 87050 | 2026-11-20 | 已核实来源 | 无 |
| V-10-008 | [effectcraft](https://github.com/storytold/effectcraft) | Apache-2.0 | 8994 | 2026-11-20 | 已核实来源 | 无 |
| V-10-009 | [openmotion](https://github.com/nexu-io/openmotion) | Apache-2.0 | 12916 | 2026-11-20 | 已核实来源 | 无 |
| V-10-010 | [anime](https://github.com/juliangarnier/anime) | MIT | 74909 | 2026-11-02 | 已核实来源 | 无 |
| V-10-011 | [mojs](https://github.com/mojs/mojs) | MIT | 18933 | 2026-07-30 | 已核实来源 | 无 |
| V-10-012 | [motion-skills](https://github.com/iart-ai/motion-skills) | MIT | 1923 | 2026-11-18 | 已核实来源 | 无 |

### V-11 程序化视觉与生成艺术（11 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-11-001 | [p5.js](https://github.com/processing/p5.js) | LGPL-2.1 | 24399 | 2026-11-17 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-11-002 | [canvas-sketch](https://github.com/mattdesl/canvas-sketch) | MIT | 5330 | 2026-06-02 | 已核实来源 | 无 |
| V-11-003 | [openrndr](https://github.com/openrndr/openrndr) | NOASSERTION | 988 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-11-004 | [cables](https://github.com/cables-gl/cables) | 无（未检出） | 575 | 2026-11-19 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-11-005 | [hydra](https://github.com/hydra-synth/hydra) | AGPL-3.0 | 2764 | 2026-04-25 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-11-006 | [audioMotion-analyzer](https://github.com/hvianna/audioMotion-analyzer) | AGPL-3.0 | 982 | 2026-07-19 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-11-007 | [meyda](https://github.com/meyda/meyda) | MIT | 1673 | 2024-07-15 | 已核实来源 | 超过 12 个月无推送 |
| V-11-008 | [three.js](https://github.com/mrdoob/three.js) | MIT | 118971 | 2026-11-20 | 已核实来源 | 无 |
| V-11-009 | [shaders](https://github.com/paper-design/shaders) | Apache-2.0 | 3989 | 2026-11-19 | 已核实来源 | 无 |
| V-11-010 | [tsparticles](https://github.com/tsparticles/tsparticles) | MIT | 9117 | 2026-11-18 | 已核实来源 | 无 |
| V-11-011 | [Graphite](https://github.com/GraphiteEditor/Graphite) | Apache-2.0 | 27985 | 2026-11-19 | 已核实来源 | 无 |

### V-12 3D 动画与场景（12 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-12-001 | [template-three](https://github.com/remotion-dev/template-three) | MIT | 123 | 2026-11-16 | 已核实来源 | 无 |
| V-12-002 | [three.js](https://github.com/mrdoob/three.js) | MIT | 118971 | 2026-11-20 | 已核实来源 | 无 |
| V-12-003 | [react-three-fiber](https://github.com/pmndrs/react-three-fiber) | MIT | 33838 | 2026-10-21 | 已核实来源 | 无 |
| V-12-004 | [drei](https://github.com/pmndrs/drei) | MIT | 10178 | 2026-11-17 | 已核实来源 | 无 |
| V-12-005 | [model-viewer](https://github.com/google/model-viewer) | Apache-2.0 | 8348 | 2026-11-18 | 已核实来源 | 无 |
| V-12-006 | [Babylon.js](https://github.com/BabylonJS/Babylon.js) | Apache-2.0 | 26404 | 2026-11-19 | 已核实来源 | 无 |
| V-12-007 | [glTF-Blender-IO](https://github.com/KhronosGroup/glTF-Blender-IO) | Apache-2.0 | 1684 | 2026-11-19 | 已核实来源 | 无 |
| V-12-008 | [mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) | MIT | 35056 | 2026-11-18 | 已核实来源 | 无 |
| V-12-009 | [BlenderProc](https://github.com/DLR-RM/BlenderProc) | GPL-3.0 | 3802 | 2026-01-20 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-12-010 | [gltfjsx](https://github.com/pmndrs/gltfjsx) | MIT | 5905 | 2024-11-04 | 已核实来源 | 超过 12 个月无推送 |
| V-12-011 | [cesium](https://github.com/CesiumGS/cesium) | Apache-2.0 | 15969 | 2026-11-19 | 已核实来源 | 无 |
| V-12-012 | [blender](https://github.com/blender/blender) | NOASSERTION | 22236 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |

### V-13 字幕、配音与音画同步（15 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-13-001 | [whisper](https://github.com/openai/whisper) | MIT | 113124 | 2026-08-31 | 已核实来源 | 无 |
| V-13-002 | [whisperX](https://github.com/m-bain/whisperX) | BSD-2-Clause | 25499 | 2026-11-12 | 已核实来源 | 无 |
| V-13-003 | [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | MIT | 55344 | 2026-11-19 | 已核实来源 | 无 |
| V-13-004 | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | MIT | 26876 | 2026-11-12 | 已核实来源 | 无 |
| V-13-005 | [stable-ts](https://github.com/jianfch/stable-ts) | MIT | 2284 | 2026-05-30 | 已核实来源 | 仓库已归档 |
| V-13-006 | [Montreal-Forced-Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) | MIT | 1917 | 2026-11-16 | 已核实来源 | 无 |
| V-13-007 | [FunASR](https://github.com/modelscope/FunASR) | MIT | 21073 | 2026-11-19 | 已核实来源 | 无 |
| V-13-008 | [wavesurfer.js](https://github.com/katspaugh/wavesurfer.js) | BSD-3-Clause | 10481 | 2026-11-12 | 已核实来源 | 无 |
| V-13-009 | [librosa](https://github.com/librosa/librosa) | ISC | 9038 | 2026-11-19 | 已核实来源 | 无 |
| V-13-010 | [subtitleedit](https://github.com/SubtitleEdit/subtitleedit) | MIT | 15064 | 2026-11-19 | 已核实来源 | 无 |
| V-13-011 | [libass](https://github.com/libass/libass) | ISC | 1195 | 2026-11-18 | 已核实来源 | 无 |
| V-13-012 | [pysubs2](https://github.com/tkarabela/pysubs2) | MIT | 448 | 2026-11-10 | 已核实来源 | 无 |
| V-13-013 | [template-tiktok](https://github.com/remotion-dev/template-tiktok) | 无（未检出） | 308 | 2026-11-09 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-13-014 | [template-audiogram](https://github.com/remotion-dev/template-audiogram) | 无（未检出） | 279 | 2026-11-16 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-13-015 | [audioMotion-analyzer](https://github.com/hvianna/audioMotion-analyzer) | AGPL-3.0 | 982 | 2026-07-19 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |

### V-14 剪辑结构与镜头节奏（9 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-14-001 | [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | Apache-2.0 | 2104 | 2026-11-19 | 已核实来源 | 无 |
| V-14-002 | [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | BSD-3-Clause | 5586 | 2026-11-18 | 已核实来源 | 无 |
| V-14-003 | [auto-editor](https://github.com/WyattBlue/auto-editor) | Unlicense | 6010 | 2026-11-20 | 已核实来源 | 无 |
| V-14-004 | [moviepy](https://github.com/Zulko/moviepy) | MIT | 15173 | 2026-08-26 | 已核实来源 | 无 |
| V-14-005 | [lossless-cut](https://github.com/mifi/lossless-cut) | GPL-2.0 | 46211 | 2026-11-14 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-14-006 | [shotcut](https://github.com/mltframework/shotcut) | GPL-3.0 | 15733 | 2026-11-17 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-14-007 | [editly](https://github.com/mifi/editly) | MIT | 5633 | 2025-05-12 | 已核实来源 | 超过 12 个月无推送 |
| V-14-008 | [OpenMontage](https://github.com/OpenMontageInc/OpenMontage) | AGPL-3.0 | 81762 | 2026-11-16 | 已核实来源 | Copyleft 许可证（使用前需合规评估） |
| V-14-009 | [hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | 87050 | 2026-11-20 | 已核实来源 | 无 |

### V-15 封面、片头、片尾与品牌包装（10 条）

| ID | 项目 | 许可证 | 星标 | 最近提交 | 状态 | 风险标记 |
|---|---|---|---|---|---|---|
| V-15-001 | [satori](https://github.com/vercel/satori) | MPL-2.0 | 14208 | 2026-11-12 | 已核实来源 | 弱 Copyleft（MPL，需合规评估） |
| V-15-002 | [sharp](https://github.com/lovell/sharp) | Apache-2.0 | 32862 | 2026-11-16 | 已核实来源 | 无 |
| V-15-003 | [Pillow](https://github.com/python-pillow/Pillow) | NOASSERTION | 13998 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |
| V-15-004 | [style-dictionary](https://github.com/style-dictionary/style-dictionary) | Apache-2.0 | 4887 | 2026-11-03 | 已核实来源 | 无 |
| V-15-005 | [noto-cjk](https://github.com/notofonts/noto-cjk) | 无（未检出） | 4163 | 2025-12-16 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-15-006 | [source-han-sans](https://github.com/adobe-fonts/source-han-sans) | NOASSERTION | 17490 | 2025-06-25 | 已核实来源 | 自定义/多重许可证（需人工核查）；超过 12 个月无推送 |
| V-15-007 | [LxgwWenKai](https://github.com/lxgw/LxgwWenKai) | OFL-1.1 | 27122 | 2026-11-19 | 已核实来源 | 无 |
| V-15-008 | [node-canvas](https://github.com/Automattic/node-canvas) | 无（未检出） | 10699 | 2026-11-14 | 已核实来源 | 许可证不清（GitHub 未检出） |
| V-15-009 | [remocn](https://github.com/Remocn/remocn) | MIT | 1809 | 2026-11-19 | 已核实来源 | 无 |
| V-15-010 | [remotion](https://github.com/remotion-dev/remotion) | NOASSERTION | 74360 | 2026-11-19 | 已核实来源 | 自定义/多重许可证（需人工核查） |

## 三、覆盖情况与缺口说明

- 已有候选的分类：26/26；暂无候选的分类：无。
- 缺口原因：当前批次优先收录重点类（UI-03/UI-06/UI-04/V-01/V-02）及官方主流项目；其余类别在后续批次补全。
- 局限：许多视频类需求（如 V-04 证据展示、V-06 纪录片叙事、V-14 剪辑节奏）在 GitHub 上多为工具/框架而非现成“效果模板”，列入的是可复现的底层工具，需后续用具体镜头需求二次筛选。
- 局限：未下载、未克隆、未运行任何仓库代码；仓库里的文字一律只当数据。

## 四、风险统计

| 风险类型 | 条数 |
|---|---|
| 许可证不清 | 21 |
| 自定义/多重许可证 | 42 |
| Copyleft | 21 |
| 弱 Copyleft | 4 |
| 非商用 | 0 |
| 苹果品牌 | 19 |
| 仓库已归档 | 4 |
| 超过 12 个月 | 38 |
| 无风险标记 | 152 |

“无风险标记”只表示本脚本规则未触发，不代表许可证已通过人工审查。含苹果风格/品牌参考的条目（如 Liquid Glass 系列）需确认不含 Apple 图标、字体或专有素材。

## 五、重点推荐 Top 20（暂定，后续批次会调整）

推荐仅表示“值得优先做来源/许可证/复现核验”，不表示可用或可商用。

| # | 项目 | 分类 | 推荐理由 | 风险/注意 | 星标 | 最近提交 |
|---|---|---|---|---|---|---|
| 1 | [apache/echarts](https://github.com/apache/echarts) | V-02 数据图表动画 | 覆盖 UI-04/V-02 两个重点类；官方仓库另有 echarts-examples 可对照复现；支持真实数据输入（以官方文档为准，未验证）。 | 无 | 67755 | 2026-10-13 |
| 2 | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | V-15 封面、片头、片尾与品牌包装 | V-01/V-02/V-13 的核心引擎，React 参数化渲染视频，贴合“模板可替换参数重复生成”。 | 自定义/多重许可证（需人工核查） | 74360 | 2026-11-19 |
| 3 | [greensock/GSAP](https://github.com/greensock/GSAP) | V-01 文字与动态排版 | 文字拆分/时间线类动画事实标准之一；覆盖 UI-01/UI-02/V-01。 | 许可证不清（GitHub 未检出） | 30958 | 2026-11-04 |
| 4 | [motiondivision/motion](https://github.com/motiondivision/motion) | UI-02 页面与布局转场 | Motion（原 Framer Motion），UI-01/UI-02 交互与布局动画的主力库。 | 无 | 35372 | 2026-11-19 |
| 5 | [vercel/ai](https://github.com/vercel/ai) | UI-06 AI 智能体专属动效 | UI-06 智能体流式文本、工具调用的 SDK，可与真实系统状态绑定。 | 自定义/多重许可证（需人工核查） | 28094 | 2026-11-20 |
| 6 | [assistant-ui/assistant-ui](https://github.com/assistant-ui/assistant-ui) | UI-06 AI 智能体专属动效 | UI-06 聊天/消息流/工具调用 React 组件库。 | 无 | 13341 | 2026-11-20 |
| 7 | [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | UI-06 AI 智能体专属动效 | 把智能体运行事件接入前端的协议，利于“动效绑定真实状态”。 | 无 | 20638 | 2026-11-19 |
| 8 | [xyflow/xyflow](https://github.com/xyflow/xyflow) | V-03 信息图与逻辑解释 | UI-06/UI-09 节点工作流图（节点运行/等待/失败可自行绑定状态）。 | 无 | 39088 | 2026-11-19 |
| 9 | [Jakubantalik/thinking-orbs](https://github.com/Jakubantalik/thinking-orbs) | UI-06 AI 智能体专属动效 | UI-06 “思考/等待”状态指示器，体量小、易复现；星标与许可证见表。 | 无 | 4051 | 2026-08-16 |
| 10 | [rdev/liquid-glass-react](https://github.com/rdev/liquid-glass-react) | UI-03 毛玻璃与视觉材质 | UI-03 重点类：液态玻璃 React 组件，星标高；注意苹果风格参考与近一年未推送。 | 含苹果品牌/风格参考（需确认不含 Apple 资产）；超过 12 个月无推送 | 6746 | 2025-06-13 |
| 11 | [AndrewPrifer/liquid-dom](https://github.com/AndrewPrifer/liquid-dom) | UI-03 毛玻璃与视觉材质 | UI-03 Web 液态玻璃实现，MIT；需实测 GPU 开销与文字可读性。 | 含苹果品牌/风格参考（需确认不含 Apple 资产） | 2604 | 2026-09-06 |
| 12 | [nikdelvin/liquid-glass](https://github.com/nikdelvin/liquid-glass) | UI-03 毛玻璃与视觉材质 | UI-03 纯 CSS+SVG 滤镜方案，依赖少，利于低性能降级对比。 | 含苹果品牌/风格参考（需确认不含 Apple 资产） | 119 | 2025-12-24 |
| 13 | [tremorlabs/tremor](https://github.com/tremorlabs/tremor) | UI-04 数据仪表盘动效 | UI-04 KPI/仪表盘组件，Apache-2.0；注意最近推送较早。 | 超过 12 个月无推送 | 3704 | 2025-10-10 |
| 14 | [barvian/number-flow](https://github.com/barvian/number-flow) | UI-04 数据仪表盘动效 | UI-04/V-01 数字滚动/翻牌，MIT。 | 无 | 7827 | 2026-09-20 |
| 15 | [leeoniya/uPlot](https://github.com/leeoniya/uPlot) | UI-04 数据仪表盘动效 | UI-04 实时监控曲线/时间序列，轻量高性能。 | 无 | 10662 | 2026-11-17 |
| 16 | [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | V-10 MG 图形动画 | V-01/V-02/V-03 代码化矢量动画+编辑器，MIT；注意近期推送时间。 | 无 | 20072 | 2026-07-02 |
| 17 | [ManimCommunity/manim](https://github.com/ManimCommunity/manim) | V-03 信息图与逻辑解释 | V-02/V-03 数据与概念讲解动画，MIT。 | 无 | 42703 | 2026-11-17 |
| 18 | [mrdoob/three.js](https://github.com/mrdoob/three.js) | V-12 3D 动画与场景 | UI-05/V-12 3D 基础引擎，官方 examples 丰富。 | 无 | 118971 | 2026-11-20 |
| 19 | [rive-app/rive-react](https://github.com/rive-app/rive-react) | UI-11 SVG、Lottie、Rive 与图标动画 | UI-11 Rive 状态机在 React 中的运行时。 | 无 | 1191 | 2026-11-19 |
| 20 | [airbnb/lottie-web](https://github.com/airbnb/lottie-web) | UI-11 SVG、Lottie、Rive 与图标动画 | UI-11 Lottie 播放；注意最近推送较早。 | 超过 12 个月无推送 | 32524 | 2025-09-01 |

## 六、文件清单

- `candidates-v1.csv`（UTF-8 带 BOM）、`candidates-v1.json`：内容一致。
- `repo-staging/`：可直接提交到仓库的文件副本（asset-index、docs、ui-motion、video-motion 各分类 README）；只含索引与文档，不含第三方源码/素材；尚未向任何 GitHub 仓库写入。
