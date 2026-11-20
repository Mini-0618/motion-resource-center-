# 动效与制作资源候选清单 v2

本页是 v2 的仓库入口。

- **规模：** 595 条分类候选，对应 449 个独立 GitHub 仓库，覆盖 71 类（UI 23、视频 32、工作流 W 10、资产 A 6）。同一仓库出现在不同分类时分别计条。
- **查询日期：** 2026-11-20（北京时间）。数据来自 GitHub API 查询。
- **状态口径：** 条目状态为「已发现 / 已核实来源」。已核实来源只表示已单独读取仓库元数据（仓库存在，以及星标、许可证、最近推送等字段），**不等于已运行、已复现或已验证可用**。来源核实不等于运行验证。
- **安装命令：** 44 条已对照上游 README 原文摘录，**未运行**；其余安装命令，以及全部预览、帧率、测试结果均为「未验证」。
- **许可：** 只保留客观的代码许可证、资产许可证及证据链接，不添加风险标签，也不做商用结论。收录进本目录并不表示第三方代码或素材的产权因整理而转移，版权仍归原作者，使用前须按各自许可证核对。
- **最近推送日期：** 取 GitHub API `pushed_at` 的日期部分，可能来自非默认分支。

## 入口链接

- 索引：[`asset-index/candidates-v2.json`](../asset-index/candidates-v2.json)、[`asset-index/candidates-v2.csv`](../asset-index/candidates-v2.csv)
- 完整 v2 分类浏览（71 类版本化副本，不覆盖 v1 分类页）：[`docs/catalog-v2/`](catalog-v2/)
- v1 入口仍为 [`docs/CANDIDATES-README.md`](CANDIDATES-README.md) 与 [`asset-index/candidates-v1.json`](../asset-index/candidates-v1.json)，本批未改动。

## 一、分类覆盖

### UI 动效

| 分类 | 名称 | 条数 |
|---|---|---|
| [UI-01](catalog-v2/ui-motion/UI-01-interactions/README.md) | 基础交互动效 | 12 |
| [UI-02](catalog-v2/ui-motion/UI-02-transitions/README.md) | 页面与布局转场 | 10 |
| [UI-03](catalog-v2/ui-motion/UI-03-glass/README.md) | 毛玻璃与视觉材质 | 19 |
| [UI-04](catalog-v2/ui-motion/UI-04-dashboards/README.md) | 数据仪表盘动效 | 22 |
| [UI-05](catalog-v2/ui-motion/UI-05-3d/README.md) | 3D 空间界面 | 11 |
| [UI-06](catalog-v2/ui-motion/UI-06-ai-agents/README.md) | AI 智能体专属动效 | 22 |
| [UI-07](catalog-v2/ui-motion/UI-07-desktop/README.md) | 操作系统级窗口动效 | 7 |
| [UI-08](catalog-v2/ui-motion/UI-08-backgrounds/README.md) | 科技感与背景动效 | 7 |
| [UI-09](catalog-v2/ui-motion/UI-09-components/README.md) | 信息与内容组件 | 10 |
| [UI-10](catalog-v2/ui-motion/UI-10-mobile/README.md) | 移动端与响应式动效 | 7 |
| [UI-11](catalog-v2/ui-motion/UI-11-vector/README.md) | SVG、Lottie、Rive 与图标动画 | 15 |
| [UI-12](catalog-v2/ui-motion/UI-12-node-editors/README.md) | 可视化工作流与节点编辑器 | 14 |
| [UI-13](catalog-v2/ui-motion/UI-13-video-editor-ui/README.md) | 专业视频剪辑与创作界面 | 13 |
| [UI-14](catalog-v2/ui-motion/UI-14-maps/README.md) | 地图与地理空间交互 | 10 |
| [UI-15](catalog-v2/ui-motion/UI-15-voice-multimodal/README.md) | 语音与多模态交互 | 9 |
| [UI-16](catalog-v2/ui-motion/UI-16-design-systems/README.md) | 设计系统与主题切换动效 | 9 |
| [UI-17](catalog-v2/ui-motion/UI-17-physics/README.md) | 物理引擎交互动效 | 7 |
| [UI-18](catalog-v2/ui-motion/UI-18-collaboration/README.md) | 实时协同与多人交互 | 5 |
| [UI-19](catalog-v2/ui-motion/UI-19-accessibility/README.md) | 无障碍与低动态效果 | 5 |
| [UI-20](catalog-v2/ui-motion/UI-20-xr/README.md) | AR / VR / 空间计算界面 | 5 |
| [UI-21](catalog-v2/ui-motion/UI-21-topology-monitoring/README.md) | 动态拓扑与系统监控 | 6 |
| [UI-22](catalog-v2/ui-motion/UI-22-curve-editors/README.md) | 高级动画曲线编辑器 | 6 |
| [UI-23](catalog-v2/ui-motion/UI-23-semantic-search/README.md) | 智能搜索与语义交互 | 6 |

### 视频动效

| 分类 | 名称 | 条数 |
|---|---|---|
| [V-01](catalog-v2/video-motion/V-01-typography/README.md) | 文字与动态排版 | 18 |
| [V-02](catalog-v2/video-motion/V-02-charts/README.md) | 数据图表动画 | 17 |
| [V-03](catalog-v2/video-motion/V-03-explainers/README.md) | 信息图与逻辑解释 | 7 |
| [V-04](catalog-v2/video-motion/V-04-evidence/README.md) | 新闻、论文与证据展示 | 7 |
| [V-05](catalog-v2/video-motion/V-05-screencasts/README.md) | 产品演示与屏幕录制 | 7 |
| [V-06](catalog-v2/video-motion/V-06-documentary/README.md) | 人物、故事与纪录片叙事 | 12 |
| [V-07](catalog-v2/video-motion/V-07-transitions/README.md) | 电影化转场 | 6 |
| [V-08](catalog-v2/video-motion/V-08-vfx/README.md) | 电影化视觉效果 | 11 |
| [V-09](catalog-v2/video-motion/V-09-parallax/README.md) | 2.5D、视差与镜头运动 | 7 |
| [V-10](catalog-v2/video-motion/V-10-motion-graphics/README.md) | MG 图形动画 | 12 |
| [V-11](catalog-v2/video-motion/V-11-generative/README.md) | 程序化视觉与生成艺术 | 11 |
| [V-12](catalog-v2/video-motion/V-12-3d/README.md) | 3D 动画与场景 | 12 |
| [V-13](catalog-v2/video-motion/V-13-subtitles/README.md) | 字幕、配音与音画同步 | 15 |
| [V-14](catalog-v2/video-motion/V-14-editing/README.md) | 剪辑结构与镜头节奏 | 9 |
| [V-15](catalog-v2/video-motion/V-15-branding/README.md) | 封面、片头、片尾与品牌包装 | 10 |
| [V-16](catalog-v2/video-motion/V-16-geo-storytelling/README.md) | 地图与地理空间叙事 | 7 |
| [V-17](catalog-v2/video-motion/V-17-fui-hud/README.md) | 科幻界面与电影 FUI / HUD | 6 |
| [V-18](catalog-v2/video-motion/V-18-character-animation/README.md) | 角色动画与数字人物 | 10 |
| [V-19](catalog-v2/video-motion/V-19-compositing-tracking/README.md) | 影视合成与运动跟踪 | 8 |
| [V-20](catalog-v2/video-motion/V-20-music-visualization/README.md) | 音乐可视化与声音驱动 | 8 |
| [V-21](catalog-v2/video-motion/V-21-previs-virtual-camera/README.md) | 分镜预演与虚拟摄影 | 7 |
| [V-22](catalog-v2/video-motion/V-22-smart-reframe/README.md) | 智能重排与多画幅视频 | 6 |
| [V-23](catalog-v2/video-motion/V-23-science-simulation/README.md) | 科学实验与物理模拟 | 5 |
| [V-24](catalog-v2/video-motion/V-24-ai-explainers/README.md) | AI 模型与算法原理动画 | 6 |
| [V-25](catalog-v2/video-motion/V-25-visual-metaphor/README.md) | 视觉隐喻与抽象概念 | 4 |
| [V-26](catalog-v2/video-motion/V-26-mechanical-industrial/README.md) | 机械结构与工业动画 | 5 |
| [V-27](catalog-v2/video-motion/V-27-stop-motion-cutout/README.md) | 定格动画与剪纸动画 | 5 |
| [V-28](catalog-v2/video-motion/V-28-digital-twin/README.md) | 数字孪生与场景模拟 | 5 |
| [V-29](catalog-v2/video-motion/V-29-virtual-production/README.md) | 虚拟场景与实时电影制作 | 5 |
| [V-30](catalog-v2/video-motion/V-30-restoration/README.md) | 影像修复与画质增强 | 8 |
| [V-31](catalog-v2/video-motion/V-31-interactive-video/README.md) | 交互式与分支叙事视频 | 5 |
| [V-32](catalog-v2/video-motion/V-32-product-ads/README.md) | 产品广告与商业展示动效 | 5 |

### W 工作流

| 分类 | 名称 | 条数 |
|---|---|---|
| [W-01](catalog-v2/workflows/W-01-script-to-storyboard/README.md) | 文案自动转分镜 | 6 |
| [W-02](catalog-v2/workflows/W-02-shot-motion-matching/README.md) | 镜头与动效自动匹配 | 4 |
| [W-03](catalog-v2/workflows/W-03-parametric-rendering/README.md) | 参数化动效渲染 | 5 |
| [W-04](catalog-v2/workflows/W-04-auto-subtitles/README.md) | 自动字幕与音画同步 | 6 |
| [W-05](catalog-v2/workflows/W-05-batch-rendering/README.md) | Blender / Remotion 批量渲染 | 5 |
| [W-06](catalog-v2/workflows/W-06-auto-editing/README.md) | 自动剪辑与时间线生成 | 6 |
| [W-07](catalog-v2/workflows/W-07-multi-platform/README.md) | 多平台视频适配 | 4 |
| [W-08](catalog-v2/workflows/W-08-license-qc/README.md) | 素材授权与质量检查 | 7 |
| [W-09](catalog-v2/workflows/W-09-template-versioning/README.md) | 动效模板打包与版本管理 | 5 |
| [W-10](catalog-v2/workflows/W-10-agent-interfaces/README.md) | 多 AI 智能体调用接口 | 9 |

### A 资产

| 分类 | 名称 | 条数 |
|---|---|---|
| [A-01](catalog-v2/assets/A-01-fonts/README.md) | 字体与动态排版资产 | 7 |
| [A-02](catalog-v2/assets/A-02-icons-vector/README.md) | 图标与矢量资源 | 8 |
| [A-03](catalog-v2/assets/A-03-3d-models-materials/README.md) | 3D 模型与材质 | 4 |
| [A-04](catalog-v2/assets/A-04-sound/README.md) | 音效与声音设计 | 5 |
| [A-05](catalog-v2/assets/A-05-lut-presets/README.md) | LUT 与视觉预设 | 6 |
| [A-06](catalog-v2/assets/A-06-camera-lighting-presets/README.md) | 虚拟摄影与灯光预设 | 5 |

## 二、分类明细

### UI-01 基础交互动效（12 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-01-001 | [motion](https://github.com/motiondivision/motion) | MIT | https://github.com/motiondivision/motion | 不适用（代码/工具条目） | 不适用 | 35372 | 2026-11-19 | 已核实来源 |
| UI-01-002 | [motion-primitives](https://github.com/ibelick/motion-primitives) | MIT | https://github.com/ibelick/motion-primitives | 不适用（代码/工具条目） | 不适用 | 6987 | 2026-09-28 | 已核实来源 |
| UI-01-003 | [auto-animate](https://github.com/formkit/auto-animate) | MIT | https://github.com/formkit/auto-animate | 不适用（代码/工具条目） | 不适用 | 13976 | 2026-11-07 | 已核实来源 |
| UI-01-004 | [pragmatic-drag-and-drop](https://github.com/atlassian/pragmatic-drag-and-drop) | NOASSERTION | https://github.com/atlassian/pragmatic-drag-and-drop | 不适用（代码/工具条目） | 不适用 | 12798 | 2026-11-19 | 已核实来源 |
| UI-01-005 | [dnd-kit](https://github.com/clauderic/dnd-kit) | MIT | https://github.com/clauderic/dnd-kit | 不适用（代码/工具条目） | 不适用 | 17816 | 2026-10-31 | 已核实来源 |
| UI-01-006 | [react-spring](https://github.com/pmndrs/react-spring) | MIT | https://github.com/pmndrs/react-spring | 不适用（代码/工具条目） | 不适用 | 29318 | 2026-11-01 | 已核实来源 |
| UI-01-007 | [use-gesture](https://github.com/pmndrs/use-gesture) | MIT | https://github.com/pmndrs/use-gesture | 不适用（代码/工具条目） | 不适用 | 9626 | 2024-07-15 | 已核实来源 |
| UI-01-008 | [animate.css](https://github.com/animate-css/animate.css) | NOASSERTION | https://github.com/animate-css/animate.css | 不适用（代码/工具条目） | 不适用 | 83031 | 2024-07-29 | 已核实来源 |
| UI-01-009 | [Hover](https://github.com/IanLunn/Hover) | NOASSERTION | https://github.com/IanLunn/Hover | 不适用（代码/工具条目） | 不适用 | 29414 | 2023-10-28 | 已核实来源 |
| UI-01-010 | [SpinKit](https://github.com/tobiasahlin/SpinKit) | MIT | https://github.com/tobiasahlin/SpinKit | 不适用（代码/工具条目） | 不适用 | 19309 | 2020-08-01 | 已核实来源 |
| UI-01-011 | [svg-spinners](https://github.com/n3r4zzurr0/svg-spinners) | MIT | https://github.com/n3r4zzurr0/svg-spinners | 不适用（代码/工具条目） | 不适用 | 7021 | 2023-05-05 | 已核实来源 |
| UI-01-012 | [react-loading-skeleton](https://github.com/dvtng/react-loading-skeleton) | MIT | https://github.com/dvtng/react-loading-skeleton | 不适用（代码/工具条目） | 不适用 | 4213 | 2026-03-05 | 已核实来源 |

### UI-02 页面与布局转场（10 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-02-001 | [next-view-transitions](https://github.com/shuding/next-view-transitions) | MIT | https://github.com/shuding/next-view-transitions | 不适用（代码/工具条目） | 不适用 | 2382 | 2026-03-06 | 已核实来源 |
| UI-02-002 | [barba](https://github.com/barbajs/barba) | MIT | https://github.com/barbajs/barba | 不适用（代码/工具条目） | 不适用 | 13002 | 2024-12-02 | 已核实来源 |
| UI-02-003 | [swup](https://github.com/swup/swup) | MIT | https://github.com/swup/swup | 不适用（代码/工具条目） | 不适用 | 5252 | 2026-11-03 | 已核实来源 |
| UI-02-004 | [locomotive-scroll](https://github.com/locomotivemtl/locomotive-scroll) | MIT | https://github.com/locomotivemtl/locomotive-scroll | 不适用（代码/工具条目） | 不适用 | 8896 | 2026-11-16 | 已核实来源 |
| UI-02-005 | [lenis](https://github.com/darkroomengineering/lenis) | MIT | https://github.com/darkroomengineering/lenis | 不适用（代码/工具条目） | 不适用 | 17371 | 2026-11-19 | 已核实来源 |
| UI-02-006 | [aos](https://github.com/michalsnik/aos) | MIT | https://github.com/michalsnik/aos | 不适用（代码/工具条目） | 不适用 | 28056 | 2024-03-26 | 已核实来源 |
| UI-02-007 | [rellax](https://github.com/dixonandmoe/rellax) | MIT | https://github.com/dixonandmoe/rellax | 不适用（代码/工具条目） | 不适用 | 7115 | 2024-08-24 | 已核实来源 |
| UI-02-008 | [vaul](https://github.com/emilkowalski/vaul) | MIT | https://github.com/emilkowalski/vaul | 不适用（代码/工具条目） | 不适用 | 8755 | 2025-10-03 | 已核实来源 |
| UI-02-009 | [tldraw](https://github.com/tldraw/tldraw) | NOASSERTION | https://github.com/tldraw/tldraw | 不适用（代码/工具条目） | 不适用 | 51495 | 2026-11-19 | 已核实来源 |
| UI-02-010 | [motion](https://github.com/motiondivision/motion) | MIT | https://github.com/motiondivision/motion | 不适用（代码/工具条目） | 不适用 | 35372 | 2026-11-19 | 已核实来源 |

### UI-03 毛玻璃与视觉材质（19 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-03-001 | [liquid-glass-react](https://github.com/rdev/liquid-glass-react) | MIT | https://github.com/rdev/liquid-glass-react | 不适用（代码/工具条目） | 不适用 | 6746 | 2025-06-13 | 已核实来源 |
| UI-03-002 | [liquid-dom](https://github.com/AndrewPrifer/liquid-dom) | MIT | https://github.com/AndrewPrifer/liquid-dom | 不适用（代码/工具条目） | 不适用 | 2604 | 2026-09-06 | 已核实来源 |
| UI-03-003 | [liquid-glass-js](https://github.com/dashersw/liquid-glass-js) | MIT | https://github.com/dashersw/liquid-glass-js | 不适用（代码/工具条目） | 不适用 | 1829 | 2025-06-12 | 已核实来源 |
| UI-03-004 | [liquidGL](https://github.com/naughtyduk/liquidGL) | NOASSERTION | https://github.com/naughtyduk/liquidGL | 不适用（代码/工具条目） | 不适用 | 1087 | 2026-10-01 | 已核实来源 |
| UI-03-005 | [liquidglass](https://github.com/ybouane/liquidglass) | 无（未检出） | https://github.com/ybouane/liquidglass | 不适用（代码/工具条目） | 不适用 | 648 | 2026-09-30 | 已核实来源 |
| UI-03-006 | [liquid-glass](https://github.com/archisvaze/liquid-glass) | MIT | https://github.com/archisvaze/liquid-glass | 不适用（代码/工具条目） | 不适用 | 843 | 2026-11-10 | 已核实来源 |
| UI-03-007 | [liquid-glass](https://github.com/nikdelvin/liquid-glass) | MIT | https://github.com/nikdelvin/liquid-glass | 不适用（代码/工具条目） | 不适用 | 119 | 2025-12-24 | 已核实来源 |
| UI-03-008 | [vaso](https://github.com/huozhi/vaso) | 无（未检出） | https://github.com/huozhi/vaso | 不适用（代码/工具条目） | 不适用 | 389 | 2026-11-15 | 已核实来源 |
| UI-03-009 | [liquid-glass-vue](https://github.com/WXperia/liquid-glass-vue) | 无（未检出） | https://github.com/WXperia/liquid-glass-vue | 不适用（代码/工具条目） | 不适用 | 295 | 2025-07-04 | 已核实来源 |
| UI-03-010 | [plasma-ui](https://github.com/CruxGarden/plasma-ui) | MIT | https://github.com/CruxGarden/plasma-ui | 不适用（代码/工具条目） | 不适用 | 337 | 2026-11-01 | 已核实来源 |
| UI-03-011 | [glass-ui](https://github.com/themesberg/glass-ui) | 无（未检出） | https://github.com/themesberg/glass-ui | 不适用（代码/工具条目） | 不适用 | 413 | 2026-02-27 | 已核实来源 |
| UI-03-012 | [css.glass](https://github.com/miketromba/css.glass) | 无（未检出） | https://github.com/miketromba/css.glass | 不适用（代码/工具条目） | 不适用 | 458 | 2025-09-15 | 已核实来源 |
| UI-03-013 | [liquid-glass-effect-macos](https://github.com/lucasromerodb/liquid-glass-effect-macos) | 无（未检出） | https://github.com/lucasromerodb/liquid-glass-effect-macos | 不适用（代码/工具条目） | 不适用 | 827 | 2025-06-10 | 已核实来源 |
| UI-03-014 | [dashdot](https://github.com/MauriceNino/dashdot) | MIT | https://github.com/MauriceNino/dashdot | 不适用（代码/工具条目） | 不适用 | 3756 | 2026-11-15 | 已核实来源 |
| UI-03-015 | [Cloudy](https://github.com/skydoves/Cloudy) | Apache-2.0 | https://github.com/skydoves/Cloudy | 不适用（代码/工具条目） | 不适用 | 1293 | 2026-09-13 | 已核实来源 |
| UI-03-016 | [AndroidLiquidGlass](https://github.com/Kyant0/AndroidLiquidGlass) | Apache-2.0 | https://github.com/Kyant0/AndroidLiquidGlass | 不适用（代码/工具条目） | 不适用 | 4719 | 2026-11-12 | 已核实来源 |
| UI-03-017 | [liquid_glass_widgets](https://github.com/sdegenaar/liquid_glass_widgets) | MIT | https://github.com/sdegenaar/liquid_glass_widgets | 不适用（代码/工具条目） | 不适用 | 864 | 2026-11-19 | 已核实来源 |
| UI-03-018 | [liquid-glass](https://github.com/callstack/liquid-glass) | MIT | https://github.com/callstack/liquid-glass | 不适用（代码/工具条目） | 不适用 | 1737 | 2026-09-15 | 已核实来源 |
| UI-03-019 | [LiquidGlassReference](https://github.com/conorluddy/LiquidGlassReference) | 无（未检出） | https://github.com/conorluddy/LiquidGlassReference | 不适用（代码/工具条目） | 不适用 | 345 | 2026-03-08 | 已核实来源 |

### UI-04 数据仪表盘动效（22 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-04-001 | [echarts](https://github.com/apache/echarts) | Apache-2.0 | https://github.com/apache/echarts | 不适用（代码/工具条目） | 不适用 | 67755 | 2026-10-13 | 已核实来源 |
| UI-04-002 | [echarts-examples](https://github.com/apache/echarts-examples) | Apache-2.0 | https://github.com/apache/echarts-examples | 不适用（代码/工具条目） | 不适用 | 402 | 2026-10-29 | 已核实来源 |
| UI-04-003 | [d3](https://github.com/d3/d3) | ISC | https://github.com/d3/d3 | 不适用（代码/工具条目） | 不适用 | 113973 | 2026-11-03 | 已核实来源 |
| UI-04-004 | [plot](https://github.com/observablehq/plot) | ISC | https://github.com/observablehq/plot | 不适用（代码/工具条目） | 不适用 | 5431 | 2026-11-05 | 已核实来源 |
| UI-04-005 | [Chart.js](https://github.com/chartjs/Chart.js) | MIT | https://github.com/chartjs/Chart.js | 不适用（代码/工具条目） | 不适用 | 67813 | 2026-11-17 | 已核实来源 |
| UI-04-006 | [recharts](https://github.com/recharts/recharts) | MIT | https://github.com/recharts/recharts | 不适用（代码/工具条目） | 不适用 | 27723 | 2026-11-19 | 已核实来源 |
| UI-04-007 | [visx](https://github.com/airbnb/visx) | MIT | https://github.com/airbnb/visx | 不适用（代码/工具条目） | 不适用 | 21115 | 2026-06-22 | 已核实来源 |
| UI-04-008 | [nivo](https://github.com/plouc/nivo) | MIT | https://github.com/plouc/nivo | 不适用（代码/工具条目） | 不适用 | 14143 | 2026-07-21 | 已核实来源 |
| UI-04-009 | [tremor](https://github.com/tremorlabs/tremor) | Apache-2.0 | https://github.com/tremorlabs/tremor | 不适用（代码/工具条目） | 不适用 | 3704 | 2025-10-10 | 已核实来源 |
| UI-04-010 | [number-flow](https://github.com/barvian/number-flow) | MIT | https://github.com/barvian/number-flow | 不适用（代码/工具条目） | 不适用 | 7827 | 2026-09-20 | 已核实来源 |
| UI-04-011 | [uPlot](https://github.com/leeoniya/uPlot) | MIT | https://github.com/leeoniya/uPlot | 不适用（代码/工具条目） | 不适用 | 10662 | 2026-11-17 | 已核实来源 |
| UI-04-012 | [apexcharts.js](https://github.com/apexcharts/apexcharts.js) | NOASSERTION | https://github.com/apexcharts/apexcharts.js | 不适用（代码/工具条目） | 不适用 | 15189 | 2026-11-18 | 已核实来源 |
| UI-04-013 | [G2](https://github.com/antvis/G2) | MIT | https://github.com/antvis/G2 | 不适用（代码/工具条目） | 不适用 | 12670 | 2026-11-14 | 已核实来源 |
| UI-04-014 | [gridstack.js](https://github.com/gridstack/gridstack.js) | MIT | https://github.com/gridstack/gridstack.js | 不适用（代码/工具条目） | 不适用 | 9257 | 2026-11-17 | 已核实来源 |
| UI-04-015 | [perspective](https://github.com/perspective-dev/perspective) | Apache-2.0 | https://github.com/perspective-dev/perspective | 不适用（代码/工具条目） | 不适用 | 11605 | 2026-11-19 | 已核实来源 |
| UI-04-016 | [grafana](https://github.com/grafana/grafana) | AGPL-3.0 | https://github.com/grafana/grafana | 不适用（代码/工具条目） | 不适用 | 78003 | 2026-11-20 | 已核实来源 |
| UI-04-017 | [superset](https://github.com/apache/superset) | Apache-2.0 | https://github.com/apache/superset | 不适用（代码/工具条目） | 不适用 | 75582 | 2026-11-20 | 已核实来源 |
| UI-04-018 | [langfuse](https://github.com/langfuse/langfuse) | NOASSERTION | https://github.com/langfuse/langfuse | 不适用（代码/工具条目） | 不适用 | 37641 | 2026-11-20 | 已核实来源 |
| UI-04-019 | [free-react-tailwind-admin-dashboard](https://github.com/TailAdmin/free-react-tailwind-admin-dashboard) | MIT | https://github.com/TailAdmin/free-react-tailwind-admin-dashboard | 不适用（代码/工具条目） | 不适用 | 1307 | 2026-11-17 | 已核实来源 |
| UI-04-020 | [dashboardblocks](https://github.com/LGLabGreg/dashboardblocks) | MIT | https://github.com/LGLabGreg/dashboardblocks | 不适用（代码/工具条目） | 不适用 | 32 | 2026-11-19 | 已核实来源 |
| UI-04-021 | [microcharts](https://github.com/ganapativs/microcharts) | MIT | https://github.com/ganapativs/microcharts | 不适用（代码/工具条目） | 不适用 | 209 | 2026-11-19 | 已核实来源 |
| UI-04-022 | [chartbrew](https://github.com/chartbrew/chartbrew) | NOASSERTION | https://github.com/chartbrew/chartbrew | 不适用（代码/工具条目） | 不适用 | 4096 | 2026-11-14 | 已核实来源 |

### UI-05 3D 空间界面（11 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-05-001 | [three.js](https://github.com/mrdoob/three.js) | MIT | https://github.com/mrdoob/three.js | 不适用（代码/工具条目） | 不适用 | 118971 | 2026-11-20 | 已核实来源 |
| UI-05-002 | [react-three-fiber](https://github.com/pmndrs/react-three-fiber) | MIT | https://github.com/pmndrs/react-three-fiber | 不适用（代码/工具条目） | 不适用 | 33838 | 2026-10-21 | 已核实来源 |
| UI-05-003 | [drei](https://github.com/pmndrs/drei) | MIT | https://github.com/pmndrs/drei | 不适用（代码/工具条目） | 不适用 | 10178 | 2026-11-17 | 已核实来源 |
| UI-05-004 | [3d-force-graph](https://github.com/vasturiano/3d-force-graph) | MIT | https://github.com/vasturiano/3d-force-graph | 不适用（代码/工具条目） | 不适用 | 6581 | 2026-11-05 | 已核实来源 |
| UI-05-005 | [react-force-graph](https://github.com/vasturiano/react-force-graph) | MIT | https://github.com/vasturiano/react-force-graph | 不适用（代码/工具条目） | 不适用 | 3373 | 2026-09-29 | 已核实来源 |
| UI-05-006 | [globe.gl](https://github.com/vasturiano/globe.gl) | MIT | https://github.com/vasturiano/globe.gl | 不适用（代码/工具条目） | 不适用 | 3237 | 2026-08-22 | 已核实来源 |
| UI-05-007 | [uikit](https://github.com/pmndrs/uikit) | NOASSERTION | https://github.com/pmndrs/uikit | 不适用（代码/工具条目） | 不适用 | 3270 | 2026-10-27 | 已核实来源 |
| UI-05-008 | [G6](https://github.com/antvis/G6) | MIT | https://github.com/antvis/G6 | 不适用（代码/工具条目） | 不适用 | 12396 | 2026-11-13 | 已核实来源 |
| UI-05-009 | [vis-network](https://github.com/visjs/vis-network) | Apache-2.0 | https://github.com/visjs/vis-network | 不适用（代码/工具条目） | 不适用 | 3642 | 2026-11-19 | 已核实来源 |
| UI-05-010 | [cytoscape.js](https://github.com/cytoscape/cytoscape.js) | MIT | https://github.com/cytoscape/cytoscape.js | 不适用（代码/工具条目） | 不适用 | 11295 | 2026-11-10 | 已核实来源 |
| UI-05-011 | [postprocessing](https://github.com/pmndrs/postprocessing) | Zlib | https://github.com/pmndrs/postprocessing | 不适用（代码/工具条目） | 不适用 | 2986 | 2026-11-01 | 已核实来源 |

### UI-06 AI 智能体专属动效（22 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-06-001 | [ai](https://github.com/vercel/ai) | NOASSERTION | https://github.com/vercel/ai | 不适用（代码/工具条目） | 不适用 | 28094 | 2026-11-20 | 已核实来源 |
| UI-06-002 | [assistant-ui](https://github.com/assistant-ui/assistant-ui) | MIT | https://github.com/assistant-ui/assistant-ui | 不适用（代码/工具条目） | 不适用 | 13341 | 2026-11-20 | 已核实来源 |
| UI-06-003 | [CopilotKit](https://github.com/CopilotKit/CopilotKit) | MIT | https://github.com/CopilotKit/CopilotKit | 不适用（代码/工具条目） | 不适用 | 38824 | 2026-11-20 | 已核实来源 |
| UI-06-004 | [ag-ui](https://github.com/ag-ui-protocol/ag-ui) | MIT | https://github.com/ag-ui-protocol/ag-ui | 不适用（代码/工具条目） | 不适用 | 20638 | 2026-11-19 | 已核实来源 |
| UI-06-005 | [ai-elements](https://github.com/vercel/ai-elements) | NOASSERTION | https://github.com/vercel/ai-elements | 不适用（代码/工具条目） | 不适用 | 2531 | 2026-10-14 | 已核实来源 |
| UI-06-006 | [streamdown](https://github.com/vercel/streamdown) | NOASSERTION | https://github.com/vercel/streamdown | 不适用（代码/工具条目） | 不适用 | 5778 | 2026-11-18 | 已核实来源 |
| UI-06-007 | [thinking-orbs](https://github.com/Jakubantalik/thinking-orbs) | MIT | https://github.com/Jakubantalik/thinking-orbs | 不适用（代码/工具条目） | 不适用 | 4051 | 2026-08-16 | 已核实来源 |
| UI-06-008 | [gaia-ui](https://github.com/theexperiencecompany/gaia-ui) | MIT | https://github.com/theexperiencecompany/gaia-ui | 不适用（代码/工具条目） | 不适用 | 225 | 2026-09-03 | 已核实来源 |
| UI-06-009 | [xyflow](https://github.com/xyflow/xyflow) | MIT | https://github.com/xyflow/xyflow | 不适用（代码/工具条目） | 不适用 | 39088 | 2026-11-19 | 已核实来源 |
| UI-06-010 | [langflow](https://github.com/langflow-ai/langflow) | MIT | https://github.com/langflow-ai/langflow | 不适用（代码/工具条目） | 不适用 | 156782 | 2026-11-20 | 已核实来源 |
| UI-06-011 | [n8n](https://github.com/n8n-io/n8n) | NOASSERTION | https://github.com/n8n-io/n8n | 不适用（代码/工具条目） | 不适用 | 211434 | 2026-11-20 | 已核实来源 |
| UI-06-012 | [open-webui](https://github.com/open-webui/open-webui) | NOASSERTION | https://github.com/open-webui/open-webui | 不适用（代码/工具条目） | 不适用 | 159104 | 2026-11-19 | 已核实来源 |
| UI-06-013 | [NextChat](https://github.com/ChatGPTNextWeb/NextChat) | MIT | https://github.com/ChatGPTNextWeb/NextChat | 不适用（代码/工具条目） | 不适用 | 88988 | 2026-10-20 | 已核实来源 |
| UI-06-014 | [Flowise](https://github.com/FlowiseAI/Flowise) | NOASSERTION | https://github.com/FlowiseAI/Flowise | 不适用（代码/工具条目） | 不适用 | 55574 | 2026-08-13 | 已核实来源 |
| UI-06-015 | [agent-chat-ui](https://github.com/langchain-ai/agent-chat-ui) | MIT | https://github.com/langchain-ai/agent-chat-ui | 不适用（代码/工具条目） | 不适用 | 3253 | 2026-11-03 | 已核实来源 |
| UI-06-016 | [prompt-kit](https://github.com/ibelick/prompt-kit) | MIT | https://github.com/ibelick/prompt-kit | 不适用（代码/工具条目） | 不适用 | 3162 | 2026-09-28 | 已核实来源 |
| UI-06-017 | [lobehub](https://github.com/lobehub/lobehub) | NOASSERTION | https://github.com/lobehub/lobehub | 不适用（代码/工具条目） | 不适用 | 85869 | 2026-11-20 | 已核实来源 |
| UI-06-018 | [chatkit-js](https://github.com/openai/chatkit-js) | Apache-2.0 | https://github.com/openai/chatkit-js | 不适用（代码/工具条目） | 不适用 | 1971 | 2026-07-31 | 已核实来源 |
| UI-06-019 | [chatbot](https://github.com/vercel/chatbot) | NOASSERTION | https://github.com/vercel/chatbot | 不适用（代码/工具条目） | 不适用 | 21064 | 2026-11-03 | 已核实来源 |
| UI-06-020 | [ui](https://github.com/elevenlabs/ui) | MIT | https://github.com/elevenlabs/ui | 不适用（代码/工具条目） | 不适用 | 2461 | 2026-11-16 | 已核实来源 |
| UI-06-021 | [phoenix](https://github.com/Arize-ai/phoenix) | NOASSERTION | https://github.com/Arize-ai/phoenix | 不适用（代码/工具条目） | 不适用 | 12357 | 2026-11-20 | 已核实来源 |
| UI-06-022 | [langfuse](https://github.com/langfuse/langfuse) | NOASSERTION | https://github.com/langfuse/langfuse | 不适用（代码/工具条目） | 不适用 | 37641 | 2026-11-20 | 已核实来源 |

### UI-07 操作系统级窗口动效（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-07-001 | [daedalOS](https://github.com/DustinBrett/daedalOS) | MIT | https://github.com/DustinBrett/daedalOS | 不适用（代码/工具条目） | 不适用 | 13102 | 2026-10-22 | 已核实来源 |
| UI-07-002 | [macos-web](https://github.com/PuruVJ/macos-web) | MIT | https://github.com/PuruVJ/macos-web | 不适用（代码/工具条目） | 不适用 | 2685 | 2026-07-05 | 已核实来源 |
| UI-07-003 | [winbox](https://github.com/nextapps-de/winbox) | Apache-2.0 | https://github.com/nextapps-de/winbox | 不适用（代码/工具条目） | 不适用 | 6457 | 2024-08-15 | 已核实来源 |
| UI-07-004 | [react-rnd](https://github.com/bokuweb/react-rnd) | MIT | https://github.com/bokuweb/react-rnd | 不适用（代码/工具条目） | 不适用 | 4326 | 2026-05-12 | 已核实来源 |
| UI-07-005 | [FlexLayout](https://github.com/caplin/FlexLayout) | MIT | https://github.com/caplin/FlexLayout | 不适用（代码/工具条目） | 不适用 | 1388 | 2026-11-18 | 已核实来源 |
| UI-07-006 | [cmdk](https://github.com/dip/cmdk) | MIT | https://github.com/dip/cmdk | 不适用（代码/工具条目） | 不适用 | 13166 | 2025-10-29 | 已核实来源 |
| UI-07-007 | [sonner](https://github.com/emilkowalski/sonner) | MIT | https://github.com/emilkowalski/sonner | 不适用（代码/工具条目） | 不适用 | 13239 | 2026-08-10 | 已核实来源 |

### UI-08 科技感与背景动效（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-08-001 | [magicui](https://github.com/magicuidesign/magicui) | MIT | https://github.com/magicuidesign/magicui | 不适用（代码/工具条目） | 不适用 | 23380 | 2026-11-17 | 已核实来源 |
| UI-08-002 | [tsparticles](https://github.com/tsparticles/tsparticles) | MIT | https://github.com/tsparticles/tsparticles | 不适用（代码/工具条目） | 不适用 | 9117 | 2026-11-18 | 已核实来源 |
| UI-08-003 | [shaders](https://github.com/paper-design/shaders) | Apache-2.0 | https://github.com/paper-design/shaders | 不适用（代码/工具条目） | 不适用 | 3989 | 2026-11-19 | 已核实来源 |
| UI-08-004 | [vanta](https://github.com/tengbao/vanta) | MIT | https://github.com/tengbao/vanta | 不适用（代码/工具条目） | 不适用 | 7399 | 2024-03-03 | 已核实来源 |
| UI-08-005 | [matrix](https://github.com/Rezmason/matrix) | MIT | https://github.com/Rezmason/matrix | 不适用（代码/工具条目） | 不适用 | 3869 | 2025-06-23 | 已核实来源 |
| UI-08-006 | [react-bits](https://github.com/DavidHDev/react-bits) | NOASSERTION | https://github.com/DavidHDev/react-bits | 不适用（代码/工具条目） | 不适用 | 52329 | 2026-11-19 | 已核实来源 |
| UI-08-007 | [three.js](https://github.com/mrdoob/three.js) | MIT | https://github.com/mrdoob/three.js | 不适用（代码/工具条目） | 不适用 | 118971 | 2026-11-20 | 已核实来源 |

### UI-09 信息与内容组件（10 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-09-001 | [shiki](https://github.com/shikijs/shiki) | MIT | https://github.com/shikijs/shiki | 不适用（代码/工具条目） | 不适用 | 13941 | 2026-11-02 | 已核实来源 |
| UI-09-002 | [shiki-magic-move](https://github.com/shikijs/shiki-magic-move) | MIT | https://github.com/shikijs/shiki-magic-move | 不适用（代码/工具条目） | 不适用 | 1509 | 2026-06-03 | 已核实来源 |
| UI-09-003 | [xterm.js](https://github.com/xtermjs/xterm.js) | MIT | https://github.com/xtermjs/xterm.js | 不适用（代码/工具条目） | 不适用 | 21369 | 2026-11-16 | 已核实来源 |
| UI-09-004 | [mermaid](https://github.com/mermaid-js/mermaid) | MIT | https://github.com/mermaid-js/mermaid | 不适用（代码/工具条目） | 不适用 | 91165 | 2026-11-19 | 已核实来源 |
| UI-09-005 | [table](https://github.com/TanStack/table) | MIT | https://github.com/TanStack/table | 不适用（代码/工具条目） | 不适用 | 28591 | 2026-11-18 | 已核实来源 |
| UI-09-006 | [react-window](https://github.com/bvaughn/react-window) | MIT | https://github.com/bvaughn/react-window | 不适用（代码/工具条目） | 不适用 | 17213 | 2026-11-15 | 已核实来源 |
| UI-09-007 | [masonry](https://github.com/desandro/masonry) | 无（未检出） | https://github.com/desandro/masonry | 不适用（代码/工具条目） | 不适用 | 16681 | 2024-06-07 | 已核实来源 |
| UI-09-008 | [TimelineJS3](https://github.com/NUKnightLab/TimelineJS3) | MPL-2.0 | https://github.com/NUKnightLab/TimelineJS3 | 不适用（代码/工具条目） | 不适用 | 3236 | 2026-11-16 | 已核实来源 |
| UI-09-009 | [xyflow](https://github.com/xyflow/xyflow) | MIT | https://github.com/xyflow/xyflow | 不适用（代码/工具条目） | 不适用 | 39088 | 2026-11-19 | 已核实来源 |
| UI-09-010 | [streamdown](https://github.com/vercel/streamdown) | NOASSERTION | https://github.com/vercel/streamdown | 不适用（代码/工具条目） | 不适用 | 5778 | 2026-11-18 | 已核实来源 |

### UI-10 移动端与响应式动效（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-10-001 | [react-native-reanimated](https://github.com/software-mansion/react-native-reanimated) | MIT | https://github.com/software-mansion/react-native-reanimated | 不适用（代码/工具条目） | 不适用 | 11084 | 2026-11-19 | 已核实来源 |
| UI-10-002 | [react-native-gesture-handler](https://github.com/software-mansion/react-native-gesture-handler) | MIT | https://github.com/software-mansion/react-native-gesture-handler | 不适用（代码/工具条目） | 不适用 | 6807 | 2026-11-19 | 已核实来源 |
| UI-10-003 | [react-native-skia](https://github.com/wcandillon/react-native-skia) | MIT | https://github.com/wcandillon/react-native-skia | 不适用（代码/工具条目） | 不适用 | 8784 | 2026-11-19 | 已核实来源 |
| UI-10-004 | [react-native-bottom-sheet](https://github.com/gorhom/react-native-bottom-sheet) | MIT | https://github.com/gorhom/react-native-bottom-sheet | 不适用（代码/工具条目） | 不适用 | 9113 | 2026-05-09 | 已核实来源 |
| UI-10-005 | [swiper](https://github.com/nolimits4web/swiper) | MIT | https://github.com/nolimits4web/swiper | 不适用（代码/工具条目） | 不适用 | 41908 | 2026-10-30 | 已核实来源 |
| UI-10-006 | [ionic-framework](https://github.com/ionic-team/ionic-framework) | MIT | https://github.com/ionic-team/ionic-framework | 不适用（代码/工具条目） | 不适用 | 52771 | 2026-11-20 | 已核实来源 |
| UI-10-007 | [flash-list](https://github.com/Shopify/flash-list) | MIT | https://github.com/Shopify/flash-list | 不适用（代码/工具条目） | 不适用 | 7249 | 2026-10-01 | 已核实来源 |

### UI-11 SVG、Lottie、Rive 与图标动画（15 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-11-001 | [lottie-web](https://github.com/airbnb/lottie-web) | MIT | https://github.com/airbnb/lottie-web | 不适用（代码/工具条目） | 不适用 | 32524 | 2025-09-01 | 已核实来源 |
| UI-11-002 | [dotlottie-web](https://github.com/LottieFiles/dotlottie-web) | MIT | https://github.com/LottieFiles/dotlottie-web | 不适用（代码/工具条目） | 不适用 | 951 | 2026-11-18 | 已核实来源 |
| UI-11-003 | [rive-react](https://github.com/rive-app/rive-react) | MIT | https://github.com/rive-app/rive-react | 不适用（代码/工具条目） | 不适用 | 1191 | 2026-11-19 | 已核实来源 |
| UI-11-004 | [rive-wasm](https://github.com/rive-app/rive-wasm) | MIT | https://github.com/rive-app/rive-wasm | 不适用（代码/工具条目） | 不适用 | 1031 | 2026-11-19 | 已核实来源 |
| UI-11-005 | [lottie-ios](https://github.com/airbnb/lottie-ios) | Apache-2.0 | https://github.com/airbnb/lottie-ios | 不适用（代码/工具条目） | 不适用 | 26945 | 2026-10-06 | 已核实来源 |
| UI-11-006 | [lottie-android](https://github.com/airbnb/lottie-android) | Apache-2.0 | https://github.com/airbnb/lottie-android | 不适用（代码/工具条目） | 不适用 | 35774 | 2026-02-15 | 已核实来源 |
| UI-11-007 | [lottie-react](https://github.com/LottieFiles/lottie-react) | MIT | https://github.com/LottieFiles/lottie-react | 不适用（代码/工具条目） | 不适用 | 798 | 2026-04-08 | 已核实来源 |
| UI-11-008 | [thorvg](https://github.com/thorvg/thorvg) | MIT | https://github.com/thorvg/thorvg | 不适用（代码/工具条目） | 不适用 | 1926 | 2026-11-20 | 已核实来源 |
| UI-11-009 | [vivus](https://github.com/maxwellito/vivus) | MIT | https://github.com/maxwellito/vivus | 不适用（代码/工具条目） | 不适用 | 15484 | 2022-07-06 | 已核实来源 |
| UI-11-010 | [svg.js](https://github.com/svgdotjs/svg.js) | NOASSERTION | https://github.com/svgdotjs/svg.js | 不适用（代码/工具条目） | 不适用 | 11944 | 2026-08-04 | 已核实来源 |
| UI-11-011 | [lucide](https://github.com/lucide-icons/lucide) | NOASSERTION | https://github.com/lucide-icons/lucide | 不适用（代码/工具条目） | 不适用 | 25870 | 2026-11-19 | 已核实来源 |
| UI-11-012 | [icons](https://github.com/pqoqubbw/icons) | MIT | https://github.com/pqoqubbw/icons | 不适用（代码/工具条目） | 不适用 | 8303 | 2026-11-15 | 已核实来源 |
| UI-11-013 | [progressbar.js](https://github.com/kimmobrunfeldt/progressbar.js) | MIT | https://github.com/kimmobrunfeldt/progressbar.js | 不适用（代码/工具条目） | 不适用 | 7845 | 2024-11-02 | 已核实来源 |
| UI-11-014 | [anime](https://github.com/juliangarnier/anime) | MIT | https://github.com/juliangarnier/anime | 不适用（代码/工具条目） | 不适用 | 74909 | 2026-11-02 | 已核实来源 |
| UI-11-015 | [mojs](https://github.com/mojs/mojs) | MIT | https://github.com/mojs/mojs | 不适用（代码/工具条目） | 不适用 | 18933 | 2026-07-30 | 已核实来源 |

### V-01 文字与动态排版（18 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-01-001 | [remotion](https://github.com/remotion-dev/remotion) | NOASSERTION | https://github.com/remotion-dev/remotion | 不适用（代码/工具条目） | 不适用 | 74360 | 2026-11-19 | 已核实来源 |
| V-01-002 | [template-tiktok](https://github.com/remotion-dev/template-tiktok) | 无（未检出） | https://github.com/remotion-dev/template-tiktok | 不适用（代码/工具条目） | 不适用 | 308 | 2026-11-09 | 已核实来源 |
| V-01-003 | [template-code-hike](https://github.com/remotion-dev/template-code-hike) | 无（未检出） | https://github.com/remotion-dev/template-code-hike | 不适用（代码/工具条目） | 不适用 | 223 | 2026-11-02 | 已核实来源 |
| V-01-004 | [remocn](https://github.com/Remocn/remocn) | MIT | https://github.com/Remocn/remocn | 不适用（代码/工具条目） | 不适用 | 1809 | 2026-11-19 | 已核实来源 |
| V-01-005 | [remotion-templates](https://github.com/reactvideoeditor/remotion-templates) | 无（未检出） | https://github.com/reactvideoeditor/remotion-templates | 不适用（代码/工具条目） | 不适用 | 296 | 2026-04-21 | 已核实来源 |
| V-01-006 | [motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | https://github.com/motion-canvas/motion-canvas | 不适用（代码/工具条目） | 不适用 | 20072 | 2026-07-02 | 已核实来源 |
| V-01-007 | [revideo](https://github.com/midrender/revideo) | MIT | https://github.com/midrender/revideo | 不适用（代码/工具条目） | 不适用 | 4218 | 2026-07-15 | 已核实来源 |
| V-01-008 | [GSAP](https://github.com/greensock/GSAP) | 无（未检出） | https://github.com/greensock/GSAP | 不适用（代码/工具条目） | 不适用 | 30958 | 2026-11-04 | 已核实来源 |
| V-01-009 | [anime](https://github.com/juliangarnier/anime) | MIT | https://github.com/juliangarnier/anime | 不适用（代码/工具条目） | 不适用 | 74909 | 2026-11-02 | 已核实来源 |
| V-01-010 | [typed.js](https://github.com/mattboldt/typed.js) | NOASSERTION | https://github.com/mattboldt/typed.js | 不适用（代码/工具条目） | 不适用 | 16274 | 2026-01-25 | 已核实来源 |
| V-01-011 | [source-han-sans](https://github.com/adobe-fonts/source-han-sans) | NOASSERTION | https://github.com/adobe-fonts/source-han-sans | 不适用（代码/工具条目） | 不适用 | 17490 | 2025-06-25 | 已核实来源 |
| V-01-012 | [LxgwWenKai](https://github.com/lxgw/LxgwWenKai) | OFL-1.1 | https://github.com/lxgw/LxgwWenKai | 不适用（代码/工具条目） | 不适用 | 27122 | 2026-11-19 | 已核实来源 |
| V-01-013 | [magicui](https://github.com/magicuidesign/magicui) | MIT | https://github.com/magicuidesign/magicui | 不适用（代码/工具条目） | 不适用 | 23380 | 2026-11-17 | 已核实来源 |
| V-01-014 | [motion-primitives](https://github.com/ibelick/motion-primitives) | MIT | https://github.com/ibelick/motion-primitives | 不适用（代码/工具条目） | 不适用 | 6987 | 2026-09-28 | 已核实来源 |
| V-01-015 | [animate-ui](https://github.com/imskyleen/animate-ui) | NOASSERTION | https://github.com/imskyleen/animate-ui | 不适用（代码/工具条目） | 不适用 | 5091 | 2026-11-15 | 已核实来源 |
| V-01-016 | [Splitting](https://github.com/shshaw/Splitting) | MIT | https://github.com/shshaw/Splitting | 不适用（代码/工具条目） | 不适用 | 1757 | 2024-06-19 | 已核实来源 |
| V-01-017 | [SplitType](https://github.com/lukePeavey/SplitType) | 无（未检出） | https://github.com/lukePeavey/SplitType | 不适用（代码/工具条目） | 不适用 | 735 | 2023-12-03 | 已核实来源 |
| V-01-018 | [satori](https://github.com/vercel/satori) | MPL-2.0 | https://github.com/vercel/satori | 不适用（代码/工具条目） | 不适用 | 14208 | 2026-11-12 | 已核实来源 |

### V-02 数据图表动画（17 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-02-001 | [manim](https://github.com/ManimCommunity/manim) | MIT | https://github.com/ManimCommunity/manim | 不适用（代码/工具条目） | 不适用 | 42703 | 2026-11-17 | 已核实来源 |
| V-02-002 | [manim](https://github.com/3b1b/manim) | MIT | https://github.com/3b1b/manim | 不适用（代码/工具条目） | 不适用 | 96689 | 2026-09-09 | 已核实来源 |
| V-02-003 | [bar_chart_race](https://github.com/dexplo/bar_chart_race) | MIT | https://github.com/dexplo/bar_chart_race | 不适用（代码/工具条目） | 不适用 | 1452 | 2024-06-27 | 已核实来源 |
| V-02-004 | [vega-lite](https://github.com/vega/vega-lite) | BSD-3-Clause | https://github.com/vega/vega-lite | 不适用（代码/工具条目） | 不适用 | 5562 | 2026-11-13 | 已核实来源 |
| V-02-005 | [plotly.js](https://github.com/plotly/plotly.js) | MIT | https://github.com/plotly/plotly.js | 不适用（代码/工具条目） | 不适用 | 18383 | 2026-11-20 | 已核实来源 |
| V-02-006 | [deck.gl](https://github.com/visgl/deck.gl) | MIT | https://github.com/visgl/deck.gl | 不适用（代码/工具条目） | 不适用 | 14777 | 2026-11-20 | 已核实来源 |
| V-02-007 | [template-audiogram](https://github.com/remotion-dev/template-audiogram) | 无（未检出） | https://github.com/remotion-dev/template-audiogram | 不适用（代码/工具条目） | 不适用 | 279 | 2026-11-16 | 已核实来源 |
| V-02-008 | [vega](https://github.com/vega/vega) | BSD-3-Clause | https://github.com/vega/vega | 不适用（代码/工具条目） | 不适用 | 12050 | 2026-11-19 | 已核实来源 |
| V-02-009 | [plotly.py](https://github.com/plotly/plotly.py) | MIT | https://github.com/plotly/plotly.py | 不适用（代码/工具条目） | 不适用 | 18913 | 2026-11-19 | 已核实来源 |
| V-02-010 | [gganimate](https://github.com/thomasp85/gganimate) | NOASSERTION | https://github.com/thomasp85/gganimate | 不适用（代码/工具条目） | 不适用 | 1984 | 2025-09-04 | 已核实来源 |
| V-02-011 | [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) | NOASSERTION | https://github.com/maplibre/maplibre-gl-js | 不适用（代码/工具条目） | 不适用 | 12135 | 2026-11-19 | 已核实来源 |
| V-02-012 | [pyecharts](https://github.com/pyecharts/pyecharts) | MIT | https://github.com/pyecharts/pyecharts | 不适用（代码/工具条目） | 不适用 | 15780 | 2026-10-26 | 已核实来源 |
| V-02-013 | [matplotlib](https://github.com/matplotlib/matplotlib) | 无（未检出） | https://github.com/matplotlib/matplotlib | 不适用（代码/工具条目） | 不适用 | 23491 | 2026-11-20 | 已核实来源 |
| V-02-014 | [videos](https://github.com/3b1b/videos) | NOASSERTION | https://github.com/3b1b/videos | 不适用（代码/工具条目） | 不适用 | 11507 | 2026-11-10 | 已核实来源 |
| V-02-015 | [echarts](https://github.com/apache/echarts) | Apache-2.0 | https://github.com/apache/echarts | 不适用（代码/工具条目） | 不适用 | 67755 | 2026-10-13 | 已核实来源 |
| V-02-016 | [d3](https://github.com/d3/d3) | ISC | https://github.com/d3/d3 | 不适用（代码/工具条目） | 不适用 | 113973 | 2026-11-03 | 已核实来源 |
| V-02-017 | [d3-sankey](https://github.com/d3/d3-sankey) | BSD-3-Clause | https://github.com/d3/d3-sankey | 不适用（代码/工具条目） | 不适用 | 947 | 2023-11-13 | 已核实来源 |

### V-03 信息图与逻辑解释（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-03-001 | [mermaid](https://github.com/mermaid-js/mermaid) | MIT | https://github.com/mermaid-js/mermaid | 不适用（代码/工具条目） | 不适用 | 91165 | 2026-11-19 | 已核实来源 |
| V-03-002 | [excalidraw](https://github.com/excalidraw/excalidraw) | MIT | https://github.com/excalidraw/excalidraw | 不适用（代码/工具条目） | 不适用 | 135981 | 2026-11-19 | 已核实来源 |
| V-03-003 | [d2](https://github.com/d2lang/d2) | MPL-2.0 | https://github.com/d2lang/d2 | 不适用（代码/工具条目） | 不适用 | 25866 | 2026-11-20 | 已核实来源 |
| V-03-004 | [xyflow](https://github.com/xyflow/xyflow) | MIT | https://github.com/xyflow/xyflow | 不适用（代码/工具条目） | 不适用 | 39088 | 2026-11-19 | 已核实来源 |
| V-03-005 | [motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | https://github.com/motion-canvas/motion-canvas | 不适用（代码/工具条目） | 不适用 | 20072 | 2026-07-02 | 已核实来源 |
| V-03-006 | [manim](https://github.com/ManimCommunity/manim) | MIT | https://github.com/ManimCommunity/manim | 不适用（代码/工具条目） | 不适用 | 42703 | 2026-11-17 | 已核实来源 |
| V-03-007 | [d3-sankey](https://github.com/d3/d3-sankey) | BSD-3-Clause | https://github.com/d3/d3-sankey | 不适用（代码/工具条目） | 不适用 | 947 | 2023-11-13 | 已核实来源 |

### V-04 新闻、论文与证据展示（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-04-001 | [rough-notation](https://github.com/rough-stuff/rough-notation) | MIT | https://github.com/rough-stuff/rough-notation | 不适用（代码/工具条目） | 不适用 | 9758 | 2024-03-18 | 已核实来源 |
| V-04-002 | [playwright](https://github.com/microsoft/playwright) | Apache-2.0 | https://github.com/microsoft/playwright | 不适用（代码/工具条目） | 不适用 | 100618 | 2026-11-20 | 已核实来源 |
| V-04-003 | [puppeteer](https://github.com/puppeteer/puppeteer) | Apache-2.0 | https://github.com/puppeteer/puppeteer | 不适用（代码/工具条目） | 不适用 | 95875 | 2026-11-19 | 已核实来源 |
| V-04-004 | [pdf.js](https://github.com/mozilla/pdf.js) | Apache-2.0 | https://github.com/mozilla/pdf.js | 不适用（代码/工具条目） | 不适用 | 54161 | 2026-11-20 | 已核实来源 |
| V-04-005 | [shot-scraper](https://github.com/simonw/shot-scraper) | Apache-2.0 | https://github.com/simonw/shot-scraper | 不适用（代码/工具条目） | 不适用 | 2609 | 2026-10-14 | 已核实来源 |
| V-04-006 | [client](https://github.com/hypothesis/client) | NOASSERTION | https://github.com/hypothesis/client | 不适用（代码/工具条目） | 不适用 | 743 | 2026-11-17 | 已核实来源 |
| V-04-007 | [annotorious](https://github.com/annotorious/annotorious) | BSD-3-Clause | https://github.com/annotorious/annotorious | 不适用（代码/工具条目） | 不适用 | 875 | 2026-11-18 | 已核实来源 |

### V-05 产品演示与屏幕录制（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-05-001 | [Cap](https://github.com/CapSoftware/Cap) | NOASSERTION | https://github.com/CapSoftware/Cap | 不适用（代码/工具条目） | 不适用 | 25299 | 2026-11-20 | 已核实来源 |
| V-05-002 | [vhs](https://github.com/charmbracelet/vhs) | MIT | https://github.com/charmbracelet/vhs | 不适用（代码/工具条目） | 不适用 | 21347 | 2026-11-06 | 已核实来源 |
| V-05-003 | [asciinema](https://github.com/asciinema/asciinema) | GPL-3.0 | https://github.com/asciinema/asciinema | 不适用（代码/工具条目） | 不适用 | 17975 | 2026-11-17 | 已核实来源 |
| V-05-004 | [screenity](https://github.com/alyssaxuu/screenity) | GPL-3.0 | https://github.com/alyssaxuu/screenity | 不适用（代码/工具条目） | 不适用 | 19002 | 2026-11-08 | 已核实来源 |
| V-05-005 | [obs-studio](https://github.com/obsproject/obs-studio) | GPL-2.0 | https://github.com/obsproject/obs-studio | 不适用（代码/工具条目） | 不适用 | 79776 | 2026-11-20 | 已核实来源 |
| V-05-006 | [FFmpeg](https://github.com/FFmpeg/FFmpeg) | NOASSERTION | https://github.com/FFmpeg/FFmpeg | 不适用（代码/工具条目） | 不适用 | 67653 | 2026-11-20 | 已核实来源 |
| V-05-007 | [template-code-hike](https://github.com/remotion-dev/template-code-hike) | 无（未检出） | https://github.com/remotion-dev/template-code-hike | 不适用（代码/工具条目） | 不适用 | 223 | 2026-11-02 | 已核实来源 |

### V-06 人物、故事与纪录片叙事（12 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-06-001 | [TimelineJS3](https://github.com/NUKnightLab/TimelineJS3) | MPL-2.0 | https://github.com/NUKnightLab/TimelineJS3 | 不适用（代码/工具条目） | 不适用 | 3236 | 2026-11-16 | 已核实来源 |
| V-06-002 | [StoryMapJS](https://github.com/NUKnightLab/StoryMapJS) | NOASSERTION | https://github.com/NUKnightLab/StoryMapJS | 不适用（代码/工具条目） | 不适用 | 253 | 2026-09-13 | 已核实来源 |
| V-06-003 | [vis-timeline](https://github.com/visjs/vis-timeline) | NOASSERTION | https://github.com/visjs/vis-timeline | 不适用（代码/工具条目） | 不适用 | 2583 | 2026-11-19 | 已核实来源 |
| V-06-004 | [Gource](https://github.com/acaudwell/Gource) | GPL-3.0 | https://github.com/acaudwell/Gource | 不适用（代码/工具条目） | 不适用 | 13219 | 2026-03-06 | 已核实来源 |
| V-06-005 | [DepthFlow](https://github.com/BrokenSource/DepthFlow) | AGPL-3.0 | https://github.com/BrokenSource/DepthFlow | 不适用（代码/工具条目） | 不适用 | 1592 | 2026-11-13 | 已核实来源 |
| V-06-006 | [Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | Apache-2.0 | https://github.com/DepthAnything/Depth-Anything-V2 | 不适用（代码/工具条目） | 不适用 | 9179 | 2026-03-24 | 已核实来源 |
| V-06-007 | [juxtapose](https://github.com/NUKnightLab/juxtapose) | NOASSERTION | https://github.com/NUKnightLab/juxtapose | 不适用（代码/工具条目） | 不适用 | 886 | 2026-10-13 | 已核实来源 |
| V-06-008 | [scrollama](https://github.com/russellsamora/scrollama) | MIT | https://github.com/russellsamora/scrollama | 不适用（代码/工具条目） | 不适用 | 6014 | 2025-11-13 | 已核实来源 |
| V-06-009 | [idyll](https://github.com/idyll-lang/idyll) | MIT | https://github.com/idyll-lang/idyll | 不适用（代码/工具条目） | 不适用 | 2042 | 2023-02-04 | 已核实来源 |
| V-06-010 | [3d-photo-inpainting](https://github.com/vt-vl-lab/3d-photo-inpainting) | NOASSERTION | https://github.com/vt-vl-lab/3d-photo-inpainting | 不适用（代码/工具条目） | 不适用 | 7103 | 2024-08-30 | 已核实来源 |
| V-06-011 | [DeOldify](https://github.com/jantic/DeOldify) | MIT | https://github.com/jantic/DeOldify | 不适用（代码/工具条目） | 不适用 | 18445 | 2024-10-19 | 已核实来源 |
| V-06-012 | [LivePortrait](https://github.com/KlingAIResearch/LivePortrait) | NOASSERTION | https://github.com/KlingAIResearch/LivePortrait | 不适用（代码/工具条目） | 不适用 | 19534 | 2026-06-01 | 已核实来源 |

### V-07 电影化转场（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-07-001 | [gl-transitions](https://github.com/gl-transitions/gl-transitions) | NOASSERTION | https://github.com/gl-transitions/gl-transitions | 不适用（代码/工具条目） | 不适用 | 2261 | 2026-11-18 | 已核实来源 |
| V-07-002 | [ffmpeg-concat](https://github.com/transitive-bullshit/ffmpeg-concat) | 无（未检出） | https://github.com/transitive-bullshit/ffmpeg-concat | 不适用（代码/工具条目） | 不适用 | 993 | 2026-01-24 | 已核实来源 |
| V-07-003 | [editly](https://github.com/mifi/editly) | MIT | https://github.com/mifi/editly | 不适用（代码/工具条目） | 不适用 | 5633 | 2025-05-12 | 已核实来源 |
| V-07-004 | [mlt](https://github.com/mltframework/mlt) | LGPL-2.1 | https://github.com/mltframework/mlt | 不适用（代码/工具条目） | 不适用 | 1880 | 2026-11-19 | 已核实来源 |
| V-07-005 | [remocn](https://github.com/Remocn/remocn) | MIT | https://github.com/Remocn/remocn | 不适用（代码/工具条目） | 不适用 | 1809 | 2026-11-19 | 已核实来源 |
| V-07-006 | [VideoContext](https://github.com/bbc/VideoContext) | Apache-2.0 | https://github.com/bbc/VideoContext | 不适用（代码/工具条目） | 不适用 | 1353 | 2026-10-16 | 已核实来源 |

### V-08 电影化视觉效果（11 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-08-001 | [glfx.js](https://github.com/evanw/glfx.js) | MIT | https://github.com/evanw/glfx.js | 不适用（代码/工具条目） | 不适用 | 3460 | 2023-10-23 | 已核实来源 |
| V-08-002 | [OpenColorIO](https://github.com/AcademySoftwareFoundation/OpenColorIO) | BSD-3-Clause | https://github.com/AcademySoftwareFoundation/OpenColorIO | 不适用（代码/工具条目） | 不适用 | 2143 | 2026-10-01 | 已核实来源 |
| V-08-003 | [Natron](https://github.com/NatronGitHub/Natron) | GPL-2.0 | https://github.com/NatronGitHub/Natron | 不适用（代码/工具条目） | 不适用 | 5746 | 2026-11-20 | 已核实来源 |
| V-08-004 | [blender](https://github.com/blender/blender) | NOASSERTION | https://github.com/blender/blender | 不适用（代码/工具条目） | 不适用 | 22236 | 2026-11-19 | 已核实来源 |
| V-08-005 | [postprocessing](https://github.com/pmndrs/postprocessing) | Zlib | https://github.com/pmndrs/postprocessing | 不适用（代码/工具条目） | 不适用 | 2986 | 2026-11-01 | 已核实来源 |
| V-08-006 | [tsparticles](https://github.com/tsparticles/tsparticles) | MIT | https://github.com/tsparticles/tsparticles | 不适用（代码/工具条目） | 不适用 | 9117 | 2026-11-18 | 已核实来源 |
| V-08-007 | [react-postprocessing](https://github.com/pmndrs/react-postprocessing) | MIT | https://github.com/pmndrs/react-postprocessing | 不适用（代码/工具条目） | 不适用 | 1670 | 2026-10-21 | 已核实来源 |
| V-08-008 | [Effekseer](https://github.com/effekseer/Effekseer) | MIT | https://github.com/effekseer/Effekseer | 不适用（代码/工具条目） | 不适用 | 2114 | 2026-10-30 | 已核实来源 |
| V-08-009 | [three-nebula](https://github.com/creativelifeform/three-nebula) | MIT | https://github.com/creativelifeform/three-nebula | 不适用（代码/工具条目） | 不适用 | 1251 | 2026-10-22 | 已核实来源 |
| V-08-010 | [lygia](https://github.com/patriciogonzalezvivo/lygia) | NOASSERTION | https://github.com/patriciogonzalezvivo/lygia | 不适用（代码/工具条目） | 不适用 | 3504 | 2026-10-24 | 已核实来源 |
| V-08-011 | [gmic](https://github.com/GreycLab/gmic) | NOASSERTION | https://github.com/GreycLab/gmic | 不适用（代码/工具条目） | 不适用 | 242 | 2026-11-19 | 已核实来源 |

### V-09 2.5D、视差与镜头运动（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-09-001 | [DepthFlow](https://github.com/BrokenSource/DepthFlow) | AGPL-3.0 | https://github.com/BrokenSource/DepthFlow | 不适用（代码/工具条目） | 不适用 | 1592 | 2026-11-13 | 已核实来源 |
| V-09-002 | [3d-photo-inpainting](https://github.com/vt-vl-lab/3d-photo-inpainting) | NOASSERTION | https://github.com/vt-vl-lab/3d-photo-inpainting | 不适用（代码/工具条目） | 不适用 | 7103 | 2024-08-30 | 已核实来源 |
| V-09-003 | [3d-ken-burns](https://github.com/sniklaus/3d-ken-burns) | NOASSERTION | https://github.com/sniklaus/3d-ken-burns | 不适用（代码/工具条目） | 不适用 | 1579 | 2026-11-19 | 已核实来源 |
| V-09-004 | [Depth-Anything-V2](https://github.com/DepthAnything/Depth-Anything-V2) | Apache-2.0 | https://github.com/DepthAnything/Depth-Anything-V2 | 不适用（代码/工具条目） | 不适用 | 9179 | 2026-03-24 | 已核实来源 |
| V-09-005 | [ml-depth-pro](https://github.com/apple-aiml-research/ml-depth-pro) | NOASSERTION | https://github.com/apple-aiml-research/ml-depth-pro | 不适用（代码/工具条目） | 不适用 | 5786 | 2026-09-11 | 已核实来源 |
| V-09-006 | [rellax](https://github.com/dixonandmoe/rellax) | MIT | https://github.com/dixonandmoe/rellax | 不适用（代码/工具条目） | 不适用 | 7115 | 2024-08-24 | 已核实来源 |
| V-09-007 | [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) | NOASSERTION | https://github.com/maplibre/maplibre-gl-js | 不适用（代码/工具条目） | 不适用 | 12135 | 2026-11-19 | 已核实来源 |

### V-10 MG 图形动画（12 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-10-001 | [theatre](https://github.com/theatre-js/theatre) | Apache-2.0 | https://github.com/theatre-js/theatre | 不适用（代码/工具条目） | 不适用 | 13067 | 2024-08-14 | 已核实来源 |
| V-10-002 | [remotion](https://github.com/remotion-dev/remotion) | NOASSERTION | https://github.com/remotion-dev/remotion | 不适用（代码/工具条目） | 不适用 | 74360 | 2026-11-19 | 已核实来源 |
| V-10-003 | [motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | https://github.com/motion-canvas/motion-canvas | 不适用（代码/工具条目） | 不适用 | 20072 | 2026-07-02 | 已核实来源 |
| V-10-004 | [revideo](https://github.com/midrender/revideo) | MIT | https://github.com/midrender/revideo | 不适用（代码/工具条目） | 不适用 | 4218 | 2026-07-15 | 已核实来源 |
| V-10-005 | [fframes](https://github.com/dmtrKovalenko/fframes) | MIT | https://github.com/dmtrKovalenko/fframes | 不适用（代码/工具条目） | 不适用 | 3112 | 2026-11-15 | 已核实来源 |
| V-10-006 | [remocn](https://github.com/Remocn/remocn) | MIT | https://github.com/Remocn/remocn | 不适用（代码/工具条目） | 不适用 | 1809 | 2026-11-19 | 已核实来源 |
| V-10-007 | [hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | https://github.com/heygen-com/hyperframes | 不适用（代码/工具条目） | 不适用 | 87050 | 2026-11-20 | 已核实来源 |
| V-10-008 | [effectcraft](https://github.com/storytold/effectcraft) | Apache-2.0 | https://github.com/storytold/effectcraft | 不适用（代码/工具条目） | 不适用 | 8994 | 2026-11-20 | 已核实来源 |
| V-10-009 | [openmotion](https://github.com/nexu-io/openmotion) | Apache-2.0 | https://github.com/nexu-io/openmotion | 不适用（代码/工具条目） | 不适用 | 12916 | 2026-11-20 | 已核实来源 |
| V-10-010 | [anime](https://github.com/juliangarnier/anime) | MIT | https://github.com/juliangarnier/anime | 不适用（代码/工具条目） | 不适用 | 74909 | 2026-11-02 | 已核实来源 |
| V-10-011 | [mojs](https://github.com/mojs/mojs) | MIT | https://github.com/mojs/mojs | 不适用（代码/工具条目） | 不适用 | 18933 | 2026-07-30 | 已核实来源 |
| V-10-012 | [motion-skills](https://github.com/iart-ai/motion-skills) | MIT | https://github.com/iart-ai/motion-skills | 不适用（代码/工具条目） | 不适用 | 1923 | 2026-11-18 | 已核实来源 |

### V-11 程序化视觉与生成艺术（11 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-11-001 | [p5.js](https://github.com/processing/p5.js) | LGPL-2.1 | https://github.com/processing/p5.js | 不适用（代码/工具条目） | 不适用 | 24399 | 2026-11-17 | 已核实来源 |
| V-11-002 | [canvas-sketch](https://github.com/mattdesl/canvas-sketch) | MIT | https://github.com/mattdesl/canvas-sketch | 不适用（代码/工具条目） | 不适用 | 5330 | 2026-06-02 | 已核实来源 |
| V-11-003 | [openrndr](https://github.com/openrndr/openrndr) | NOASSERTION | https://github.com/openrndr/openrndr | 不适用（代码/工具条目） | 不适用 | 988 | 2026-11-19 | 已核实来源 |
| V-11-004 | [cables](https://github.com/cables-gl/cables) | 无（未检出） | https://github.com/cables-gl/cables | 不适用（代码/工具条目） | 不适用 | 575 | 2026-11-19 | 已核实来源 |
| V-11-005 | [hydra](https://github.com/hydra-synth/hydra) | AGPL-3.0 | https://github.com/hydra-synth/hydra | 不适用（代码/工具条目） | 不适用 | 2764 | 2026-04-25 | 已核实来源 |
| V-11-006 | [audioMotion-analyzer](https://github.com/hvianna/audioMotion-analyzer) | AGPL-3.0 | https://github.com/hvianna/audioMotion-analyzer | 不适用（代码/工具条目） | 不适用 | 982 | 2026-07-19 | 已核实来源 |
| V-11-007 | [meyda](https://github.com/meyda/meyda) | MIT | https://github.com/meyda/meyda | 不适用（代码/工具条目） | 不适用 | 1673 | 2024-07-15 | 已核实来源 |
| V-11-008 | [three.js](https://github.com/mrdoob/three.js) | MIT | https://github.com/mrdoob/three.js | 不适用（代码/工具条目） | 不适用 | 118971 | 2026-11-20 | 已核实来源 |
| V-11-009 | [shaders](https://github.com/paper-design/shaders) | Apache-2.0 | https://github.com/paper-design/shaders | 不适用（代码/工具条目） | 不适用 | 3989 | 2026-11-19 | 已核实来源 |
| V-11-010 | [tsparticles](https://github.com/tsparticles/tsparticles) | MIT | https://github.com/tsparticles/tsparticles | 不适用（代码/工具条目） | 不适用 | 9117 | 2026-11-18 | 已核实来源 |
| V-11-011 | [Graphite](https://github.com/GraphiteEditor/Graphite) | Apache-2.0 | https://github.com/GraphiteEditor/Graphite | 不适用（代码/工具条目） | 不适用 | 27985 | 2026-11-19 | 已核实来源 |

### V-12 3D 动画与场景（12 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-12-001 | [template-three](https://github.com/remotion-dev/template-three) | MIT | https://github.com/remotion-dev/template-three | 不适用（代码/工具条目） | 不适用 | 123 | 2026-11-16 | 已核实来源 |
| V-12-002 | [three.js](https://github.com/mrdoob/three.js) | MIT | https://github.com/mrdoob/three.js | 不适用（代码/工具条目） | 不适用 | 118971 | 2026-11-20 | 已核实来源 |
| V-12-003 | [react-three-fiber](https://github.com/pmndrs/react-three-fiber) | MIT | https://github.com/pmndrs/react-three-fiber | 不适用（代码/工具条目） | 不适用 | 33838 | 2026-10-21 | 已核实来源 |
| V-12-004 | [drei](https://github.com/pmndrs/drei) | MIT | https://github.com/pmndrs/drei | 不适用（代码/工具条目） | 不适用 | 10178 | 2026-11-17 | 已核实来源 |
| V-12-005 | [model-viewer](https://github.com/google/model-viewer) | Apache-2.0 | https://github.com/google/model-viewer | 不适用（代码/工具条目） | 不适用 | 8348 | 2026-11-18 | 已核实来源 |
| V-12-006 | [Babylon.js](https://github.com/BabylonJS/Babylon.js) | Apache-2.0 | https://github.com/BabylonJS/Babylon.js | 不适用（代码/工具条目） | 不适用 | 26404 | 2026-11-19 | 已核实来源 |
| V-12-007 | [glTF-Blender-IO](https://github.com/KhronosGroup/glTF-Blender-IO) | Apache-2.0 | https://github.com/KhronosGroup/glTF-Blender-IO | 不适用（代码/工具条目） | 不适用 | 1684 | 2026-11-19 | 已核实来源 |
| V-12-008 | [mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) | MIT | https://github.com/ahujasid/mcp-for-blender | 不适用（代码/工具条目） | 不适用 | 35056 | 2026-11-18 | 已核实来源 |
| V-12-009 | [BlenderProc](https://github.com/DLR-RM/BlenderProc) | GPL-3.0 | https://github.com/DLR-RM/BlenderProc | 不适用（代码/工具条目） | 不适用 | 3802 | 2026-01-20 | 已核实来源 |
| V-12-010 | [gltfjsx](https://github.com/pmndrs/gltfjsx) | MIT | https://github.com/pmndrs/gltfjsx | 不适用（代码/工具条目） | 不适用 | 5905 | 2024-11-04 | 已核实来源 |
| V-12-011 | [cesium](https://github.com/CesiumGS/cesium) | Apache-2.0 | https://github.com/CesiumGS/cesium | 不适用（代码/工具条目） | 不适用 | 15969 | 2026-11-19 | 已核实来源 |
| V-12-012 | [blender](https://github.com/blender/blender) | NOASSERTION | https://github.com/blender/blender | 不适用（代码/工具条目） | 不适用 | 22236 | 2026-11-19 | 已核实来源 |

### V-13 字幕、配音与音画同步（15 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-13-001 | [whisper](https://github.com/openai/whisper) | MIT | https://github.com/openai/whisper | 不适用（代码/工具条目） | 不适用 | 113124 | 2026-08-31 | 已核实来源 |
| V-13-002 | [whisperX](https://github.com/m-bain/whisperX) | BSD-2-Clause | https://github.com/m-bain/whisperX | 不适用（代码/工具条目） | 不适用 | 25499 | 2026-11-12 | 已核实来源 |
| V-13-003 | [whisper.cpp](https://github.com/ggml-org/whisper.cpp) | MIT | https://github.com/ggml-org/whisper.cpp | 不适用（代码/工具条目） | 不适用 | 55344 | 2026-11-19 | 已核实来源 |
| V-13-004 | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | MIT | https://github.com/SYSTRAN/faster-whisper | 不适用（代码/工具条目） | 不适用 | 26876 | 2026-11-12 | 已核实来源 |
| V-13-005 | [stable-ts](https://github.com/jianfch/stable-ts) | MIT | https://github.com/jianfch/stable-ts | 不适用（代码/工具条目） | 不适用 | 2284 | 2026-05-30 | 已核实来源 |
| V-13-006 | [Montreal-Forced-Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) | MIT | https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner | 不适用（代码/工具条目） | 不适用 | 1917 | 2026-11-16 | 已核实来源 |
| V-13-007 | [FunASR](https://github.com/modelscope/FunASR) | MIT | https://github.com/modelscope/FunASR | 不适用（代码/工具条目） | 不适用 | 21073 | 2026-11-19 | 已核实来源 |
| V-13-008 | [wavesurfer.js](https://github.com/katspaugh/wavesurfer.js) | BSD-3-Clause | https://github.com/katspaugh/wavesurfer.js | 不适用（代码/工具条目） | 不适用 | 10481 | 2026-11-12 | 已核实来源 |
| V-13-009 | [librosa](https://github.com/librosa/librosa) | ISC | https://github.com/librosa/librosa | 不适用（代码/工具条目） | 不适用 | 9038 | 2026-11-19 | 已核实来源 |
| V-13-010 | [subtitleedit](https://github.com/SubtitleEdit/subtitleedit) | MIT | https://github.com/SubtitleEdit/subtitleedit | 不适用（代码/工具条目） | 不适用 | 15064 | 2026-11-19 | 已核实来源 |
| V-13-011 | [libass](https://github.com/libass/libass) | ISC | https://github.com/libass/libass | 不适用（代码/工具条目） | 不适用 | 1195 | 2026-11-18 | 已核实来源 |
| V-13-012 | [pysubs2](https://github.com/tkarabela/pysubs2) | MIT | https://github.com/tkarabela/pysubs2 | 不适用（代码/工具条目） | 不适用 | 448 | 2026-11-10 | 已核实来源 |
| V-13-013 | [template-tiktok](https://github.com/remotion-dev/template-tiktok) | 无（未检出） | https://github.com/remotion-dev/template-tiktok | 不适用（代码/工具条目） | 不适用 | 308 | 2026-11-09 | 已核实来源 |
| V-13-014 | [template-audiogram](https://github.com/remotion-dev/template-audiogram) | 无（未检出） | https://github.com/remotion-dev/template-audiogram | 不适用（代码/工具条目） | 不适用 | 279 | 2026-11-16 | 已核实来源 |
| V-13-015 | [audioMotion-analyzer](https://github.com/hvianna/audioMotion-analyzer) | AGPL-3.0 | https://github.com/hvianna/audioMotion-analyzer | 不适用（代码/工具条目） | 不适用 | 982 | 2026-07-19 | 已核实来源 |

### V-14 剪辑结构与镜头节奏（9 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-14-001 | [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | Apache-2.0 | https://github.com/AcademySoftwareFoundation/OpenTimelineIO | 不适用（代码/工具条目） | 不适用 | 2104 | 2026-11-19 | 已核实来源 |
| V-14-002 | [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | BSD-3-Clause | https://github.com/Breakthrough/PySceneDetect | 不适用（代码/工具条目） | 不适用 | 5586 | 2026-11-18 | 已核实来源 |
| V-14-003 | [auto-editor](https://github.com/WyattBlue/auto-editor) | Unlicense | https://github.com/WyattBlue/auto-editor | 不适用（代码/工具条目） | 不适用 | 6010 | 2026-11-20 | 已核实来源 |
| V-14-004 | [moviepy](https://github.com/Zulko/moviepy) | MIT | https://github.com/Zulko/moviepy | 不适用（代码/工具条目） | 不适用 | 15173 | 2026-08-26 | 已核实来源 |
| V-14-005 | [lossless-cut](https://github.com/mifi/lossless-cut) | GPL-2.0 | https://github.com/mifi/lossless-cut | 不适用（代码/工具条目） | 不适用 | 46211 | 2026-11-14 | 已核实来源 |
| V-14-006 | [shotcut](https://github.com/mltframework/shotcut) | GPL-3.0 | https://github.com/mltframework/shotcut | 不适用（代码/工具条目） | 不适用 | 15733 | 2026-11-17 | 已核实来源 |
| V-14-007 | [editly](https://github.com/mifi/editly) | MIT | https://github.com/mifi/editly | 不适用（代码/工具条目） | 不适用 | 5633 | 2025-05-12 | 已核实来源 |
| V-14-008 | [OpenMontage](https://github.com/OpenMontageInc/OpenMontage) | AGPL-3.0 | https://github.com/OpenMontageInc/OpenMontage | 不适用（代码/工具条目） | 不适用 | 81762 | 2026-11-16 | 已核实来源 |
| V-14-009 | [hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | https://github.com/heygen-com/hyperframes | 不适用（代码/工具条目） | 不适用 | 87050 | 2026-11-20 | 已核实来源 |

### V-15 封面、片头、片尾与品牌包装（10 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-15-001 | [satori](https://github.com/vercel/satori) | MPL-2.0 | https://github.com/vercel/satori | 不适用（代码/工具条目） | 不适用 | 14208 | 2026-11-12 | 已核实来源 |
| V-15-002 | [sharp](https://github.com/lovell/sharp) | Apache-2.0 | https://github.com/lovell/sharp | 不适用（代码/工具条目） | 不适用 | 32862 | 2026-11-16 | 已核实来源 |
| V-15-003 | [Pillow](https://github.com/python-pillow/Pillow) | NOASSERTION | https://github.com/python-pillow/Pillow | 不适用（代码/工具条目） | 不适用 | 13998 | 2026-11-19 | 已核实来源 |
| V-15-004 | [style-dictionary](https://github.com/style-dictionary/style-dictionary) | Apache-2.0 | https://github.com/style-dictionary/style-dictionary | 不适用（代码/工具条目） | 不适用 | 4887 | 2026-11-03 | 已核实来源 |
| V-15-005 | [noto-cjk](https://github.com/notofonts/noto-cjk) | 无（未检出） | https://github.com/notofonts/noto-cjk | 不适用（代码/工具条目） | 不适用 | 4164 | 2025-12-16 | 已核实来源 |
| V-15-006 | [source-han-sans](https://github.com/adobe-fonts/source-han-sans) | NOASSERTION | https://github.com/adobe-fonts/source-han-sans | 不适用（代码/工具条目） | 不适用 | 17490 | 2025-06-25 | 已核实来源 |
| V-15-007 | [LxgwWenKai](https://github.com/lxgw/LxgwWenKai) | OFL-1.1 | https://github.com/lxgw/LxgwWenKai | 不适用（代码/工具条目） | 不适用 | 27122 | 2026-11-19 | 已核实来源 |
| V-15-008 | [node-canvas](https://github.com/Automattic/node-canvas) | 无（未检出） | https://github.com/Automattic/node-canvas | 不适用（代码/工具条目） | 不适用 | 10699 | 2026-11-14 | 已核实来源 |
| V-15-009 | [remocn](https://github.com/Remocn/remocn) | MIT | https://github.com/Remocn/remocn | 不适用（代码/工具条目） | 不适用 | 1809 | 2026-11-19 | 已核实来源 |
| V-15-010 | [remotion](https://github.com/remotion-dev/remotion) | NOASSERTION | https://github.com/remotion-dev/remotion | 不适用（代码/工具条目） | 不适用 | 74360 | 2026-11-19 | 已核实来源 |

### UI-12 可视化工作流与节点编辑器（14 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-12-001 | [xyflow](https://github.com/xyflow/xyflow) | MIT | https://github.com/xyflow/xyflow | 不适用（代码/工具条目） | 不适用 | 39088 | 2026-11-19 | 已核实来源 |
| UI-12-002 | [rete](https://github.com/retejs/rete) | MIT | https://github.com/retejs/rete | 不适用（代码/工具条目） | 不适用 | 12317 | 2026-10-25 | 已核实来源 |
| UI-12-003 | [litegraph.js](https://github.com/jagenjo/litegraph.js) | MIT | https://github.com/jagenjo/litegraph.js | 不适用（代码/工具条目） | 不适用 | 8187 | 2024-08-01 | 已核实来源 |
| UI-12-004 | [litegraph.js](https://github.com/Comfy-Org/litegraph.js) | MIT | https://github.com/Comfy-Org/litegraph.js | 不适用（代码/工具条目） | 不适用 | 256 | 2026-01-14 | 已核实来源 |
| UI-12-005 | [ComfyUI](https://github.com/Comfy-Org/ComfyUI) | GPL-3.0 | https://github.com/Comfy-Org/ComfyUI | 不适用（代码/工具条目） | 不适用 | 147682 | 2026-11-20 | 已核实来源 |
| UI-12-006 | [n8n](https://github.com/n8n-io/n8n) | NOASSERTION | https://github.com/n8n-io/n8n | 不适用（代码/工具条目） | 不适用 | 211434 | 2026-11-20 | 已核实来源 |
| UI-12-007 | [langflow](https://github.com/langflow-ai/langflow) | MIT | https://github.com/langflow-ai/langflow | 不适用（代码/工具条目） | 不适用 | 156782 | 2026-11-20 | 已核实来源 |
| UI-12-008 | [dify](https://github.com/langgenius/dify) | NOASSERTION | https://github.com/langgenius/dify | 不适用（代码/工具条目） | 不适用 | 161528 | 2026-11-20 | 已核实来源 |
| UI-12-009 | [node-red](https://github.com/node-red/node-red) | Apache-2.0 | https://github.com/node-red/node-red | 不适用（代码/工具条目） | 不适用 | 23861 | 2026-11-17 | 已核实来源 |
| UI-12-010 | [X6](https://github.com/antvis/X6) | MIT | https://github.com/antvis/X6 | 不适用（代码/工具条目） | 不适用 | 6768 | 2026-11-13 | 已核实来源 |
| UI-12-011 | [baklavajs](https://github.com/newcat/baklavajs) | MIT | https://github.com/newcat/baklavajs | 不适用（代码/工具条目） | 不适用 | 2097 | 2026-10-23 | 已核实来源 |
| UI-12-012 | [react-diagrams](https://github.com/projectstorm/react-diagrams) | MIT | https://github.com/projectstorm/react-diagrams | 不适用（代码/工具条目） | 不适用 | 9439 | 2025-04-03 | 已核实来源 |
| UI-12-013 | [Drawflow](https://github.com/jerosoler/Drawflow) | MIT | https://github.com/jerosoler/Drawflow | 不适用（代码/工具条目） | 不适用 | 6171 | 2024-10-19 | 已核实来源 |
| UI-12-014 | [Flowise](https://github.com/FlowiseAI/Flowise) | NOASSERTION | https://github.com/FlowiseAI/Flowise | 不适用（代码/工具条目） | 不适用 | 55574 | 2026-08-13 | 已核实来源 |

### UI-13 专业视频剪辑与创作界面（13 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-13-001 | [react-timeline-editor](https://github.com/xzdarcy/react-timeline-editor) | MIT | https://github.com/xzdarcy/react-timeline-editor | 不适用（代码/工具条目） | 不适用 | 802 | 2026-01-25 | 已核实来源 |
| UI-13-002 | [wavesurfer.js](https://github.com/katspaugh/wavesurfer.js) | BSD-3-Clause | https://github.com/katspaugh/wavesurfer.js | 不适用（代码/工具条目） | 不适用 | 10481 | 2026-11-12 | 已核实来源 |
| UI-13-003 | [peaks.js](https://github.com/bbc/peaks.js) | LGPL-3.0 | https://github.com/bbc/peaks.js | 不适用（代码/工具条目） | 不适用 | 3413 | 2026-10-21 | 已核实来源 |
| UI-13-004 | [theatre](https://github.com/theatre-js/theatre) | Apache-2.0 | https://github.com/theatre-js/theatre | 不适用（代码/工具条目） | 不适用 | 13067 | 2024-08-14 | 已核实来源 |
| UI-13-005 | [omniclip](https://github.com/omni-media/omniclip) | MIT | https://github.com/omni-media/omniclip | 不适用（代码/工具条目） | 不适用 | 1474 | 2026-11-15 | 已核实来源 |
| UI-13-006 | [react-video-editor](https://github.com/openvideodev/react-video-editor) | NOASSERTION | https://github.com/openvideodev/react-video-editor | 不适用（代码/工具条目） | 不适用 | 1844 | 2026-06-30 | 已核实来源 |
| UI-13-007 | [core](https://github.com/diffusionstudio/core) | MPL-2.0 | https://github.com/diffusionstudio/core | 不适用（代码/工具条目） | 不适用 | 1249 | 2025-11-18 | 已核实来源 |
| UI-13-008 | [twick](https://github.com/ncounterspecialist/twick) | NOASSERTION | https://github.com/ncounterspecialist/twick | 不适用（代码/工具条目） | 不适用 | 550 | 2026-06-04 | 已核实来源 |
| UI-13-009 | [shotcut](https://github.com/mltframework/shotcut) | GPL-3.0 | https://github.com/mltframework/shotcut | 不适用（代码/工具条目） | 不适用 | 15733 | 2026-11-17 | 已核实来源 |
| UI-13-010 | [kdenlive](https://github.com/KDE/kdenlive) | GPL-3.0 | https://github.com/KDE/kdenlive | 不适用（代码/工具条目） | 不适用 | 6149 | 2026-11-20 | 已核实来源 |
| UI-13-011 | [openshot-qt](https://github.com/OpenShot/openshot-qt) | NOASSERTION | https://github.com/OpenShot/openshot-qt | 不适用（代码/工具条目） | 不适用 | 6815 | 2026-11-19 | 已核实来源 |
| UI-13-012 | [olive](https://github.com/olive-editor/olive) | GPL-3.0 | https://github.com/olive-editor/olive | 不适用（代码/工具条目） | 不适用 | 9160 | 2024-12-05 | 已核实来源 |
| UI-13-013 | [lossless-cut](https://github.com/mifi/lossless-cut) | GPL-2.0 | https://github.com/mifi/lossless-cut | 不适用（代码/工具条目） | 不适用 | 46211 | 2026-11-14 | 已核实来源 |

### UI-14 地图与地理空间交互（10 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-14-001 | [maplibre-gl-js](https://github.com/maplibre/maplibre-gl-js) | NOASSERTION | https://github.com/maplibre/maplibre-gl-js | 不适用（代码/工具条目） | 不适用 | 12135 | 2026-11-19 | 已核实来源 |
| UI-14-002 | [deck.gl](https://github.com/visgl/deck.gl) | MIT | https://github.com/visgl/deck.gl | 不适用（代码/工具条目） | 不适用 | 14777 | 2026-11-20 | 已核实来源 |
| UI-14-003 | [cesium](https://github.com/CesiumGS/cesium) | Apache-2.0 | https://github.com/CesiumGS/cesium | 不适用（代码/工具条目） | 不适用 | 15969 | 2026-11-19 | 已核实来源 |
| UI-14-004 | [Leaflet](https://github.com/Leaflet/Leaflet) | BSD-2-Clause | https://github.com/Leaflet/Leaflet | 不适用（代码/工具条目） | 不适用 | 45956 | 2026-11-19 | 已核实来源 |
| UI-14-005 | [openlayers](https://github.com/openlayers/openlayers) | BSD-2-Clause | https://github.com/openlayers/openlayers | 不适用（代码/工具条目） | 不适用 | 12662 | 2026-11-20 | 已核实来源 |
| UI-14-006 | [kepler.gl](https://github.com/keplergl/kepler.gl) | MIT | https://github.com/keplergl/kepler.gl | 不适用（代码/工具条目） | 不适用 | 12102 | 2026-11-20 | 已核实来源 |
| UI-14-007 | [L7](https://github.com/antvis/L7) | MIT | https://github.com/antvis/L7 | 不适用（代码/工具条目） | 不适用 | 4081 | 2026-11-13 | 已核实来源 |
| UI-14-008 | [react-globe.gl](https://github.com/vasturiano/react-globe.gl) | MIT | https://github.com/vasturiano/react-globe.gl | 不适用（代码/工具条目） | 不适用 | 1469 | 2026-05-16 | 已核实来源 |
| UI-14-009 | [openglobus](https://github.com/openglobus/openglobus) | Apache-2.0 | https://github.com/openglobus/openglobus | 不适用（代码/工具条目） | 不适用 | 958 | 2026-11-19 | 已核实来源 |
| UI-14-010 | [react-map-gl](https://github.com/visgl/react-map-gl) | NOASSERTION | https://github.com/visgl/react-map-gl | 不适用（代码/工具条目） | 不适用 | 8513 | 2026-10-24 | 已核实来源 |

### UI-15 语音与多模态交互（9 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-15-001 | [pipecat](https://github.com/pipecat-ai/pipecat) | BSD-2-Clause | https://github.com/pipecat-ai/pipecat | 不适用（代码/工具条目） | 不适用 | 17348 | 2026-11-20 | 已核实来源 |
| UI-15-002 | [voice-ui-kit](https://github.com/pipecat-ai/voice-ui-kit) | BSD-2-Clause | https://github.com/pipecat-ai/voice-ui-kit | 不适用（代码/工具条目） | 不适用 | 419 | 2026-11-09 | 已核实来源 |
| UI-15-003 | [components-js](https://github.com/livekit/components-js) | Apache-2.0 | https://github.com/livekit/components-js | 不适用（代码/工具条目） | 不适用 | 477 | 2026-11-19 | 已核实来源 |
| UI-15-004 | [agents](https://github.com/livekit/agents) | Apache-2.0 | https://github.com/livekit/agents | 不适用（代码/工具条目） | 不适用 | 15283 | 2026-11-20 | 已核实来源 |
| UI-15-005 | [openai-realtime-console](https://github.com/openai/openai-realtime-console) | MIT | https://github.com/openai/openai-realtime-console | 不适用（代码/工具条目） | 不适用 | 3617 | 2025-08-28 | 已核实来源 |
| UI-15-006 | [openai-realtime-agents](https://github.com/openai/openai-realtime-agents) | MIT | https://github.com/openai/openai-realtime-agents | 不适用（代码/工具条目） | 不适用 | 7018 | 2026-01-07 | 已核实来源 |
| UI-15-007 | [vad](https://github.com/ricky0123/vad) | NOASSERTION | https://github.com/ricky0123/vad | 不适用（代码/工具条目） | 不适用 | 2079 | 2026-09-12 | 已核实来源 |
| UI-15-008 | [transformers.js](https://github.com/huggingface/transformers.js) | Apache-2.0 | https://github.com/huggingface/transformers.js | 不适用（代码/工具条目） | 不适用 | 16434 | 2026-11-18 | 已核实来源 |
| UI-15-009 | [ui](https://github.com/elevenlabs/ui) | MIT | https://github.com/elevenlabs/ui | 不适用（代码/工具条目） | 不适用 | 2461 | 2026-11-16 | 已核实来源 |

### UI-16 设计系统与主题切换动效（9 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-16-001 | [ui](https://github.com/shadcn-ui/ui) | MIT | https://github.com/shadcn-ui/ui | 不适用（代码/工具条目） | 不适用 | 128588 | 2026-11-19 | 已核实来源 |
| UI-16-002 | [next-themes](https://github.com/pacocoursey/next-themes) | MIT | https://github.com/pacocoursey/next-themes | 不适用（代码/工具条目） | 不适用 | 6353 | 2026-02-25 | 已核实来源 |
| UI-16-003 | [themes](https://github.com/radix-ui/themes) | MIT | https://github.com/radix-ui/themes | 不适用（代码/工具条目） | 不适用 | 8857 | 2026-04-11 | 已核实来源 |
| UI-16-004 | [style-dictionary](https://github.com/style-dictionary/style-dictionary) | Apache-2.0 | https://github.com/style-dictionary/style-dictionary | 不适用（代码/工具条目） | 不适用 | 4887 | 2026-11-03 | 已核实来源 |
| UI-16-005 | [material-color-utilities](https://github.com/material-foundation/material-color-utilities) | Apache-2.0 | https://github.com/material-foundation/material-color-utilities | 不适用（代码/工具条目） | 不适用 | 2304 | 2026-11-20 | 已核实来源 |
| UI-16-006 | [daisyui](https://github.com/saadeghi/daisyui) | MIT | https://github.com/saadeghi/daisyui | 不适用（代码/工具条目） | 不适用 | 42908 | 2026-11-16 | 已核实来源 |
| UI-16-007 | [chakra-ui](https://github.com/chakra-ui/chakra-ui) | MIT | https://github.com/chakra-ui/chakra-ui | 不适用（代码/工具条目） | 不适用 | 40744 | 2026-11-19 | 已核实来源 |
| UI-16-008 | [primitives](https://github.com/primer/primitives) | MIT | https://github.com/primer/primitives | 不适用（代码/工具条目） | 不适用 | 422 | 2026-11-02 | 已核实来源 |
| UI-16-009 | [figma-plugin](https://github.com/tokens-studio/figma-plugin) | MIT | https://github.com/tokens-studio/figma-plugin | 不适用（代码/工具条目） | 不适用 | 1631 | 2026-11-19 | 已核实来源 |

### UI-17 物理引擎交互动效（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-17-001 | [matter-js](https://github.com/liabru/matter-js) | MIT | https://github.com/liabru/matter-js | 不适用（代码/工具条目） | 不适用 | 18660 | 2026-09-30 | 已核实来源 |
| UI-17-002 | [rapier.js](https://github.com/dimforge/rapier.js) | Apache-2.0 | https://github.com/dimforge/rapier.js | 不适用（代码/工具条目） | 不适用 | 700 | 2026-07-12 | 已核实来源 |
| UI-17-003 | [react-three-rapier](https://github.com/pmndrs/react-three-rapier) | MIT | https://github.com/pmndrs/react-three-rapier | 不适用（代码/工具条目） | 不适用 | 1694 | 2026-10-12 | 已核实来源 |
| UI-17-004 | [cannon-es](https://github.com/pmndrs/cannon-es) | MIT | https://github.com/pmndrs/cannon-es | 不适用（代码/工具条目） | 不适用 | 2094 | 2024-01-06 | 已核实来源 |
| UI-17-005 | [box2d](https://github.com/erincatto/box2d) | MIT | https://github.com/erincatto/box2d | 不适用（代码/工具条目） | 不适用 | 10506 | 2026-11-17 | 已核实来源 |
| UI-17-006 | [react-spring](https://github.com/pmndrs/react-spring) | MIT | https://github.com/pmndrs/react-spring | 不适用（代码/工具条目） | 不适用 | 29318 | 2026-11-01 | 已核实来源 |
| UI-17-007 | [use-gesture](https://github.com/pmndrs/use-gesture) | MIT | https://github.com/pmndrs/use-gesture | 不适用（代码/工具条目） | 不适用 | 9626 | 2024-07-15 | 已核实来源 |

### UI-18 实时协同与多人交互（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-18-001 | [yjs](https://github.com/yjs/yjs) | NOASSERTION | https://github.com/yjs/yjs | 不适用（代码/工具条目） | 不适用 | 23083 | 2026-11-16 | 已核实来源 |
| UI-18-002 | [liveblocks](https://github.com/liveblocks/liveblocks) | NOASSERTION | https://github.com/liveblocks/liveblocks | 不适用（代码/工具条目） | 不适用 | 4772 | 2026-11-19 | 已核实来源 |
| UI-18-003 | [excalidraw](https://github.com/excalidraw/excalidraw) | MIT | https://github.com/excalidraw/excalidraw | 不适用（代码/工具条目） | 不适用 | 135981 | 2026-11-19 | 已核实来源 |
| UI-18-004 | [tldraw](https://github.com/tldraw/tldraw) | NOASSERTION | https://github.com/tldraw/tldraw | 不适用（代码/工具条目） | 不适用 | 51495 | 2026-11-19 | 已核实来源 |
| UI-18-005 | [partykit](https://github.com/partykit/partykit) | MIT | https://github.com/partykit/partykit | 不适用（代码/工具条目） | 不适用 | 5751 | 2026-10-09 | 已核实来源 |

### UI-19 无障碍与低动态效果（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-19-001 | [react-spectrum](https://github.com/adobe/react-spectrum) | Apache-2.0 | https://github.com/adobe/react-spectrum | 不适用（代码/工具条目） | 不适用 | 16050 | 2026-11-20 | 已核实来源 |
| UI-19-002 | [primitives](https://github.com/radix-ui/primitives) | MIT | https://github.com/radix-ui/primitives | 不适用（代码/工具条目） | 不适用 | 19527 | 2026-10-14 | 已核实来源 |
| UI-19-003 | [axe-core](https://github.com/dequelabs/axe-core) | MPL-2.0 | https://github.com/dequelabs/axe-core | 不适用（代码/工具条目） | 不适用 | 7861 | 2026-11-19 | 已核实来源 |
| UI-19-004 | [focus-trap](https://github.com/focus-trap/focus-trap) | MIT | https://github.com/focus-trap/focus-trap | 不适用（代码/工具条目） | 不适用 | 1564 | 2026-11-18 | 已核实来源 |
| UI-19-005 | [motion](https://github.com/motiondivision/motion) | MIT | https://github.com/motiondivision/motion | 不适用（代码/工具条目） | 不适用 | 35372 | 2026-11-19 | 已核实来源 |

### UI-20 AR / VR / 空间计算界面（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-20-001 | [xr](https://github.com/pmndrs/xr) | NOASSERTION | https://github.com/pmndrs/xr | 不适用（代码/工具条目） | 不适用 | 2626 | 2026-10-15 | 已核实来源 |
| UI-20-002 | [uikit](https://github.com/pmndrs/uikit) | NOASSERTION | https://github.com/pmndrs/uikit | 不适用（代码/工具条目） | 不适用 | 3270 | 2026-10-27 | 已核实来源 |
| UI-20-003 | [webxr-samples](https://github.com/immersive-web/webxr-samples) | MIT | https://github.com/immersive-web/webxr-samples | 不适用（代码/工具条目） | 不适用 | 1167 | 2026-11-19 | 已核实来源 |
| UI-20-004 | [aframe](https://github.com/aframevr/aframe) | MIT | https://github.com/aframevr/aframe | 不适用（代码/工具条目） | 不适用 | 17714 | 2026-07-13 | 已核实来源 |
| UI-20-005 | [Babylon.js](https://github.com/BabylonJS/Babylon.js) | Apache-2.0 | https://github.com/BabylonJS/Babylon.js | 不适用（代码/工具条目） | 不适用 | 26404 | 2026-11-19 | 已核实来源 |

### UI-21 动态拓扑与系统监控（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-21-001 | [cytoscape.js](https://github.com/cytoscape/cytoscape.js) | MIT | https://github.com/cytoscape/cytoscape.js | 不适用（代码/工具条目） | 不适用 | 11295 | 2026-11-10 | 已核实来源 |
| UI-21-002 | [force-graph](https://github.com/vasturiano/force-graph) | MIT | https://github.com/vasturiano/force-graph | 不适用（代码/工具条目） | 不适用 | 2171 | 2026-09-28 | 已核实来源 |
| UI-21-003 | [grafana](https://github.com/grafana/grafana) | AGPL-3.0 | https://github.com/grafana/grafana | 不适用（代码/工具条目） | 不适用 | 78003 | 2026-11-20 | 已核实来源 |
| UI-21-004 | [kiali](https://github.com/kiali/kiali) | Apache-2.0 | https://github.com/kiali/kiali | 不适用（代码/工具条目） | 不适用 | 3648 | 2026-11-19 | 已核实来源 |
| UI-21-005 | [netdata](https://github.com/netdata/netdata) | GPL-3.0 | https://github.com/netdata/netdata | 不适用（代码/工具条目） | 不适用 | 81509 | 2026-11-20 | 已核实来源 |
| UI-21-006 | [G6](https://github.com/antvis/G6) | MIT | https://github.com/antvis/G6 | 不适用（代码/工具条目） | 不适用 | 12396 | 2026-11-13 | 已核实来源 |

### UI-22 高级动画曲线编辑器（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-22-001 | [theatre](https://github.com/theatre-js/theatre) | Apache-2.0 | https://github.com/theatre-js/theatre | 不适用（代码/工具条目） | 不适用 | 13067 | 2024-08-14 | 已核实来源 |
| UI-22-002 | [cubic-bezier](https://github.com/LeaVerou/cubic-bezier) | MIT | https://github.com/LeaVerou/cubic-bezier | 不适用（代码/工具条目） | 不适用 | 184 | 2024-07-15 | 已核实来源 |
| UI-22-003 | [bezier-easing](https://github.com/gre/bezier-easing) | MIT | https://github.com/gre/bezier-easing | 不适用（代码/工具条目） | 不适用 | 1781 | 2026-11-15 | 已核实来源 |
| UI-22-004 | [leva](https://github.com/pmndrs/leva) | MIT | https://github.com/pmndrs/leva | 不适用（代码/工具条目） | 不适用 | 6277 | 2025-11-09 | 已核实来源 |
| UI-22-005 | [tweakpane](https://github.com/cocopon/tweakpane) | MIT | https://github.com/cocopon/tweakpane | 不适用（代码/工具条目） | 不适用 | 4714 | 2026-03-15 | 已核实来源 |
| UI-22-006 | [react-timeline-editor](https://github.com/xzdarcy/react-timeline-editor) | MIT | https://github.com/xzdarcy/react-timeline-editor | 不适用（代码/工具条目） | 不适用 | 802 | 2026-01-25 | 已核实来源 |

### UI-23 智能搜索与语义交互（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| UI-23-001 | [cmdk](https://github.com/dip/cmdk) | MIT | https://github.com/dip/cmdk | 不适用（代码/工具条目） | 不适用 | 13166 | 2025-10-29 | 已核实来源 |
| UI-23-002 | [instantsearch](https://github.com/algolia/instantsearch) | MIT | https://github.com/algolia/instantsearch | 不适用（代码/工具条目） | 不适用 | 4063 | 2026-11-19 | 已核实来源 |
| UI-23-003 | [meilisearch](https://github.com/meilisearch/meilisearch) | NOASSERTION | https://github.com/meilisearch/meilisearch | 不适用（代码/工具条目） | 不适用 | 59926 | 2026-11-19 | 已核实来源 |
| UI-23-004 | [Fuse](https://github.com/krisk/Fuse) | Apache-2.0 | https://github.com/krisk/Fuse | 不适用（代码/工具条目） | 不适用 | 20534 | 2026-08-09 | 已核实来源 |
| UI-23-005 | [deepscatter](https://github.com/nomic-ai/deepscatter) | NOASSERTION | https://github.com/nomic-ai/deepscatter | 不适用（代码/工具条目） | 不适用 | 1161 | 2025-05-29 | 已核实来源 |
| UI-23-006 | [umap](https://github.com/lmcinnes/umap) | BSD-3-Clause | https://github.com/lmcinnes/umap | 不适用（代码/工具条目） | 不适用 | 8336 | 2026-11-19 | 已核实来源 |

### V-16 地图与地理空间叙事（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-16-001 | [deck.gl](https://github.com/visgl/deck.gl) | MIT | https://github.com/visgl/deck.gl | 不适用（代码/工具条目） | 不适用 | 14777 | 2026-11-20 | 已核实来源 |
| V-16-002 | [kepler.gl](https://github.com/keplergl/kepler.gl) | MIT | https://github.com/keplergl/kepler.gl | 不适用（代码/工具条目） | 不适用 | 12102 | 2026-11-20 | 已核实来源 |
| V-16-003 | [cesium](https://github.com/CesiumGS/cesium) | Apache-2.0 | https://github.com/CesiumGS/cesium | 不适用（代码/工具条目） | 不适用 | 15969 | 2026-11-19 | 已核实来源 |
| V-16-004 | [globe.gl](https://github.com/vasturiano/globe.gl) | MIT | https://github.com/vasturiano/globe.gl | 不适用（代码/工具条目） | 不适用 | 3237 | 2026-08-22 | 已核实来源 |
| V-16-005 | [BlenderGIS](https://github.com/domlysz/BlenderGIS) | GPL-3.0 | https://github.com/domlysz/BlenderGIS | 不适用（代码/工具条目） | 不适用 | 9657 | 2025-12-20 | 已核实来源 |
| V-16-006 | [d3-geo](https://github.com/d3/d3-geo) | NOASSERTION | https://github.com/d3/d3-geo | 不适用（代码/工具条目） | 不适用 | 1119 | 2026-11-03 | 已核实来源 |
| V-16-007 | [StoryMapJS](https://github.com/NUKnightLab/StoryMapJS) | NOASSERTION | https://github.com/NUKnightLab/StoryMapJS | 不适用（代码/工具条目） | 不适用 | 253 | 2026-09-13 | 已核实来源 |

### V-17 科幻界面与电影 FUI / HUD（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-17-001 | [arwes](https://github.com/arwes/arwes) | MIT | https://github.com/arwes/arwes | 不适用（代码/工具条目） | 不适用 | 7575 | 2026-07-05 | 已核实来源 |
| V-17-002 | [augmented-ui](https://github.com/propjockey/augmented-ui) | BSD-2-Clause | https://github.com/propjockey/augmented-ui | 不适用（代码/工具条目） | 不适用 | 1413 | 2024-05-28 | 已核实来源 |
| V-17-003 | [edex-ui](https://github.com/GitSquared/edex-ui) | GPL-3.0 | https://github.com/GitSquared/edex-ui | 不适用（代码/工具条目） | 不适用 | 45038 | 2021-10-19 | 已核实来源 |
| V-17-004 | [cool-retro-term](https://github.com/Swordfish90/cool-retro-term) | 无（未检出） | https://github.com/Swordfish90/cool-retro-term | 不适用（代码/工具条目） | 不适用 | 26575 | 2026-05-31 | 已核实来源 |
| V-17-005 | [matrix](https://github.com/Rezmason/matrix) | MIT | https://github.com/Rezmason/matrix | 不适用（代码/工具条目） | 不适用 | 3869 | 2025-06-23 | 已核实来源 |
| V-17-006 | [postprocessing](https://github.com/pmndrs/postprocessing) | Zlib | https://github.com/pmndrs/postprocessing | 不适用（代码/工具条目） | 不适用 | 2986 | 2026-11-01 | 已核实来源 |

### V-18 角色动画与数字人物（10 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-18-001 | [three-vrm](https://github.com/pixiv/three-vrm) | MIT | https://github.com/pixiv/three-vrm | 不适用（代码/工具条目） | 不适用 | 2299 | 2026-10-22 | 已核实来源 |
| V-18-002 | [TalkingHead](https://github.com/met4citizen/TalkingHead) | MIT | https://github.com/met4citizen/TalkingHead | 不适用（代码/工具条目） | 不适用 | 1687 | 2026-11-04 | 已核实来源 |
| V-18-003 | [rhubarb-lip-sync](https://github.com/DanielSWolf/rhubarb-lip-sync) | NOASSERTION | https://github.com/DanielSWolf/rhubarb-lip-sync | 不适用（代码/工具条目） | 不适用 | 2787 | 2026-06-16 | 已核实来源 |
| V-18-004 | [AnimatedDrawings](https://github.com/facebookresearch/AnimatedDrawings) | MIT | https://github.com/facebookresearch/AnimatedDrawings | 不适用（代码/工具条目） | 不适用 | 12808 | 2025-09-03 | 已核实来源 |
| V-18-005 | [LivePortrait](https://github.com/KlingAIResearch/LivePortrait) | NOASSERTION | https://github.com/KlingAIResearch/LivePortrait | 不适用（代码/工具条目） | 不适用 | 19534 | 2026-06-01 | 已核实来源 |
| V-18-006 | [SadTalker](https://github.com/OpenTalker/SadTalker) | NOASSERTION | https://github.com/OpenTalker/SadTalker | 不适用（代码/工具条目） | 不适用 | 14212 | 2024-06-26 | 已核实来源 |
| V-18-007 | [Wav2Lip](https://github.com/Rudrabha/Wav2Lip) | 无（未检出） | https://github.com/Rudrabha/Wav2Lip | 不适用（代码/工具条目） | 不适用 | 13284 | 2025-06-22 | 已核实来源 |
| V-18-008 | [kalidokit](https://github.com/yeemachine/kalidokit) | MIT | https://github.com/yeemachine/kalidokit | 不适用（代码/工具条目） | 不适用 | 5731 | 2025-08-18 | 已核实来源 |
| V-18-009 | [mediapipe](https://github.com/google-ai-edge/mediapipe) | Apache-2.0 | https://github.com/google-ai-edge/mediapipe | 不适用（代码/工具条目） | 不适用 | 37747 | 2026-11-19 | 已核实来源 |
| V-18-010 | [spine-runtimes](https://github.com/EsotericSoftware/spine-runtimes) | NOASSERTION | https://github.com/EsotericSoftware/spine-runtimes | 不适用（代码/工具条目） | 不适用 | 5372 | 2026-11-18 | 已核实来源 |

### V-19 影视合成与运动跟踪（8 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-19-001 | [Natron](https://github.com/NatronGitHub/Natron) | GPL-2.0 | https://github.com/NatronGitHub/Natron | 不适用（代码/工具条目） | 不适用 | 5746 | 2026-11-20 | 已核实来源 |
| V-19-002 | [sam2](https://github.com/facebookresearch/sam2) | Apache-2.0 | https://github.com/facebookresearch/sam2 | 不适用（代码/工具条目） | 不适用 | 20190 | 2026-05-30 | 已核实来源 |
| V-19-003 | [RobustVideoMatting](https://github.com/PeterL1n/RobustVideoMatting) | GPL-3.0 | https://github.com/PeterL1n/RobustVideoMatting | 不适用（代码/工具条目） | 不适用 | 9624 | 2024-04-02 | 已核实来源 |
| V-19-004 | [rembg](https://github.com/danielgatis/rembg) | MIT | https://github.com/danielgatis/rembg | 不适用（代码/工具条目） | 不适用 | 25586 | 2026-11-06 | 已核实来源 |
| V-19-005 | [co-tracker](https://github.com/facebookresearch/co-tracker) | NOASSERTION | https://github.com/facebookresearch/co-tracker | 不适用（代码/工具条目） | 不适用 | 5206 | 2026-03-03 | 已核实来源 |
| V-19-006 | [Cutie](https://github.com/hkchengrex/Cutie) | MIT | https://github.com/hkchengrex/Cutie | 不适用（代码/工具条目） | 不适用 | 1133 | 2024-11-08 | 已核实来源 |
| V-19-007 | [opencv](https://github.com/opencv/opencv) | Apache-2.0 | https://github.com/opencv/opencv | 不适用（代码/工具条目） | 不适用 | 91646 | 2026-11-19 | 已核实来源 |
| V-19-008 | [colmap](https://github.com/colmap/colmap) | NOASSERTION | https://github.com/colmap/colmap | 不适用（代码/工具条目） | 不适用 | 13258 | 2026-11-18 | 已核实来源 |

### V-20 音乐可视化与声音驱动（8 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-20-001 | [butterchurn](https://github.com/jberg/butterchurn) | MIT | https://github.com/jberg/butterchurn | 不适用（代码/工具条目） | 不适用 | 1996 | 2026-04-20 | 已核实来源 |
| V-20-002 | [projectm](https://github.com/projectM-visualizer/projectm) | LGPL-2.1 | https://github.com/projectM-visualizer/projectm | 不适用（代码/工具条目） | 不适用 | 4587 | 2026-11-01 | 已核实来源 |
| V-20-003 | [audioMotion-analyzer](https://github.com/hvianna/audioMotion-analyzer) | AGPL-3.0 | https://github.com/hvianna/audioMotion-analyzer | 不适用（代码/工具条目） | 不适用 | 982 | 2026-07-19 | 已核实来源 |
| V-20-004 | [librosa](https://github.com/librosa/librosa) | ISC | https://github.com/librosa/librosa | 不适用（代码/工具条目） | 不适用 | 9038 | 2026-11-19 | 已核实来源 |
| V-20-005 | [aubio](https://github.com/aubio/aubio) | GPL-3.0 | https://github.com/aubio/aubio | 不适用（代码/工具条目） | 不适用 | 3790 | 2026-04-10 | 已核实来源 |
| V-20-006 | [Tone.js](https://github.com/Tonejs/Tone.js) | MIT | https://github.com/Tonejs/Tone.js | 不适用（代码/工具条目） | 不适用 | 14932 | 2026-11-15 | 已核实来源 |
| V-20-007 | [essentia](https://github.com/MTG/essentia) | AGPL-3.0 | https://github.com/MTG/essentia | 不适用（代码/工具条目） | 不适用 | 3811 | 2026-11-18 | 已核实来源 |
| V-20-008 | [template-audiogram](https://github.com/remotion-dev/template-audiogram) | 无（未检出） | https://github.com/remotion-dev/template-audiogram | 不适用（代码/工具条目） | 不适用 | 279 | 2026-11-16 | 已核实来源 |

### V-21 分镜预演与虚拟摄影（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-21-001 | [storyboarder](https://github.com/wonderunit/storyboarder) | 无（未检出） | https://github.com/wonderunit/storyboarder | 不适用（代码/工具条目） | 不适用 | 3960 | 2024-03-17 | 已核实来源 |
| V-21-002 | [camera-controls](https://github.com/yomotsu/camera-controls) | MIT | https://github.com/yomotsu/camera-controls | 不适用（代码/工具条目） | 不适用 | 2452 | 2026-10-21 | 已核实来源 |
| V-21-003 | [theatre](https://github.com/theatre-js/theatre) | Apache-2.0 | https://github.com/theatre-js/theatre | 不适用（代码/工具条目） | 不适用 | 13067 | 2024-08-14 | 已核实来源 |
| V-21-004 | [OpenUSD](https://github.com/PixarAnimationStudios/OpenUSD) | NOASSERTION | https://github.com/PixarAnimationStudios/OpenUSD | 不适用（代码/工具条目） | 不适用 | 7659 | 2026-11-18 | 已核实来源 |
| V-21-005 | [GaussianSplats3D](https://github.com/mkkellogg/GaussianSplats3D) | MIT | https://github.com/mkkellogg/GaussianSplats3D | 不适用（代码/工具条目） | 不适用 | 2972 | 2025-10-19 | 已核实来源 |
| V-21-006 | [nerfstudio](https://github.com/nerfstudio-project/nerfstudio) | Apache-2.0 | https://github.com/nerfstudio-project/nerfstudio | 不适用（代码/工具条目） | 不适用 | 12231 | 2025-07-29 | 已核实来源 |
| V-21-007 | [blender](https://github.com/blender/blender) | NOASSERTION | https://github.com/blender/blender | 不适用（代码/工具条目） | 不适用 | 22236 | 2026-11-19 | 已核实来源 |

### V-22 智能重排与多画幅视频（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-22-001 | [smartcrop.js](https://github.com/jwagner/smartcrop.js) | MIT | https://github.com/jwagner/smartcrop.js | 不适用（代码/工具条目） | 不适用 | 12961 | 2024-03-16 | 已核实来源 |
| V-22-002 | [clipsai](https://github.com/ClipsAI/clipsai) | MIT | https://github.com/ClipsAI/clipsai | 不适用（代码/工具条目） | 不适用 | 577 | 2024-01-17 | 已核实来源 |
| V-22-003 | [mediapipe](https://github.com/google-ai-edge/mediapipe) | Apache-2.0 | https://github.com/google-ai-edge/mediapipe | 不适用（代码/工具条目） | 不适用 | 37747 | 2026-11-19 | 已核实来源 |
| V-22-004 | [AI-Youtube-Shorts-Generator](https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator) | MIT | https://github.com/Anil-matcha/AI-Youtube-Shorts-Generator | 不适用（代码/工具条目） | 不适用 | 6328 | 2026-11-12 | 已核实来源 |
| V-22-005 | [satori](https://github.com/vercel/satori) | MPL-2.0 | https://github.com/vercel/satori | 不适用（代码/工具条目） | 不适用 | 14208 | 2026-11-12 | 已核实来源 |
| V-22-006 | [FFmpeg](https://github.com/FFmpeg/FFmpeg) | NOASSERTION | https://github.com/FFmpeg/FFmpeg | 不适用（代码/工具条目） | 不适用 | 67653 | 2026-11-20 | 已核实来源 |

### V-23 科学实验与物理模拟（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-23-001 | [taichi](https://github.com/taichi-dev/taichi) | Apache-2.0 | https://github.com/taichi-dev/taichi | 不适用（代码/工具条目） | 不适用 | 28466 | 2026-10-05 | 已核实来源 |
| V-23-002 | [genesis-world](https://github.com/Genesis-Embodied-AI/genesis-world) | Apache-2.0 | https://github.com/Genesis-Embodied-AI/genesis-world | 不适用（代码/工具条目） | 不适用 | 30268 | 2026-11-20 | 已核实来源 |
| V-23-003 | [mujoco](https://github.com/google-deepmind/mujoco) | Apache-2.0 | https://github.com/google-deepmind/mujoco | 不适用（代码/工具条目） | 不适用 | 18323 | 2026-11-20 | 已核实来源 |
| V-23-004 | [matter-js](https://github.com/liabru/matter-js) | MIT | https://github.com/liabru/matter-js | 不适用（代码/工具条目） | 不适用 | 18660 | 2026-09-30 | 已核实来源 |
| V-23-005 | [manim](https://github.com/ManimCommunity/manim) | MIT | https://github.com/ManimCommunity/manim | 不适用（代码/工具条目） | 不适用 | 42703 | 2026-11-17 | 已核实来源 |

### V-24 AI 模型与算法原理动画（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-24-001 | [transformer-explainer](https://github.com/poloclub/transformer-explainer) | MIT | https://github.com/poloclub/transformer-explainer | 不适用（代码/工具条目） | 不适用 | 9196 | 2026-06-06 | 已核实来源 |
| V-24-002 | [llm-viz](https://github.com/bbycroft/llm-viz) | MIT | https://github.com/bbycroft/llm-viz | 不适用（代码/工具条目） | 不适用 | 5598 | 2026-08-10 | 已核实来源 |
| V-24-003 | [cnn-explainer](https://github.com/poloclub/cnn-explainer) | MIT | https://github.com/poloclub/cnn-explainer | 不适用（代码/工具条目） | 不适用 | 9121 | 2023-10-14 | 已核实来源 |
| V-24-004 | [playground](https://github.com/tensorflow/playground) | Apache-2.0 | https://github.com/tensorflow/playground | 不适用（代码/工具条目） | 不适用 | 13113 | 2026-06-10 | 已核实来源 |
| V-24-005 | [algorithm-visualizer](https://github.com/algorithm-visualizer/algorithm-visualizer) | MIT | https://github.com/algorithm-visualizer/algorithm-visualizer | 不适用（代码/工具条目） | 不适用 | 49549 | 2024-06-09 | 已核实来源 |
| V-24-006 | [manim](https://github.com/ManimCommunity/manim) | MIT | https://github.com/ManimCommunity/manim | 不适用（代码/工具条目） | 不适用 | 42703 | 2026-11-17 | 已核实来源 |

### V-25 视觉隐喻与抽象概念（4 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-25-001 | [p5.js](https://github.com/processing/p5.js) | LGPL-2.1 | https://github.com/processing/p5.js | 不适用（代码/工具条目） | 不适用 | 24399 | 2026-11-17 | 已核实来源 |
| V-25-002 | [hydra](https://github.com/hydra-synth/hydra) | AGPL-3.0 | https://github.com/hydra-synth/hydra | 不适用（代码/工具条目） | 不适用 | 2764 | 2026-04-25 | 已核实来源 |
| V-25-003 | [openrndr](https://github.com/openrndr/openrndr) | NOASSERTION | https://github.com/openrndr/openrndr | 不适用（代码/工具条目） | 不适用 | 988 | 2026-11-19 | 已核实来源 |
| V-25-004 | [motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | https://github.com/motion-canvas/motion-canvas | 不适用（代码/工具条目） | 不适用 | 20072 | 2026-07-02 | 已核实来源 |

### V-26 机械结构与工业动画（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-26-001 | [FreeCAD](https://github.com/FreeCAD/FreeCAD) | LGPL-2.1 | https://github.com/FreeCAD/FreeCAD | 不适用（代码/工具条目） | 不适用 | 35623 | 2026-11-19 | 已核实来源 |
| V-26-002 | [mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie) | NOASSERTION | https://github.com/google-deepmind/mujoco_menagerie | 不适用（代码/工具条目） | 不适用 | 4385 | 2026-11-10 | 已核实来源 |
| V-26-003 | [urdf-loaders](https://github.com/gkjohnson/urdf-loaders) | Apache-2.0 | https://github.com/gkjohnson/urdf-loaders | 不适用（代码/工具条目） | 不适用 | 822 | 2026-10-31 | 已核实来源 |
| V-26-004 | [openscad](https://github.com/openscad/openscad) | NOASSERTION | https://github.com/openscad/openscad | 不适用（代码/工具条目） | 不适用 | 10687 | 2026-11-20 | 已核实来源 |
| V-26-005 | [blender](https://github.com/blender/blender) | NOASSERTION | https://github.com/blender/blender | 不适用（代码/工具条目） | 不适用 | 22236 | 2026-11-19 | 已核实来源 |

### V-27 定格动画与剪纸动画（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-27-001 | [synfig](https://github.com/synfig/synfig) | GPL-3.0 | https://github.com/synfig/synfig | 不适用（代码/工具条目） | 不适用 | 2454 | 2026-11-15 | 已核实来源 |
| V-27-002 | [opentoonz](https://github.com/opentoonz/opentoonz) | NOASSERTION | https://github.com/opentoonz/opentoonz | 不适用（代码/工具条目） | 不适用 | 8310 | 2026-11-19 | 已核实来源 |
| V-27-003 | [pencil](https://github.com/pencil2d/pencil) | GPL-2.0 | https://github.com/pencil2d/pencil | 不适用（代码/工具条目） | 不适用 | 1912 | 2026-11-13 | 已核实来源 |
| V-27-004 | [tahoma2d](https://github.com/tahoma2d/tahoma2d) | NOASSERTION | https://github.com/tahoma2d/tahoma2d | 不适用（代码/工具条目） | 不适用 | 693 | 2026-10-17 | 已核实来源 |
| V-27-005 | [AnimatedDrawings](https://github.com/facebookresearch/AnimatedDrawings) | MIT | https://github.com/facebookresearch/AnimatedDrawings | 不适用（代码/工具条目） | 不适用 | 12808 | 2025-09-03 | 已核实来源 |

### V-28 数字孪生与场景模拟（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-28-001 | [itwinjs-core](https://github.com/iTwin/itwinjs-core) | MIT | https://github.com/iTwin/itwinjs-core | 不适用（代码/工具条目） | 不适用 | 742 | 2026-11-19 | 已核实来源 |
| V-28-002 | [carla](https://github.com/carla-simulator/carla) | MIT | https://github.com/carla-simulator/carla | 不适用（代码/工具条目） | 不适用 | 14657 | 2026-11-20 | 已核实来源 |
| V-28-003 | [sumo](https://github.com/eclipse-sumo/sumo) | EPL-2.0 | https://github.com/eclipse-sumo/sumo | 不适用（代码/工具条目） | 不适用 | 4288 | 2026-11-19 | 已核实来源 |
| V-28-004 | [cesium](https://github.com/CesiumGS/cesium) | Apache-2.0 | https://github.com/CesiumGS/cesium | 不适用（代码/工具条目） | 不适用 | 15969 | 2026-11-19 | 已核实来源 |
| V-28-005 | [GaussianSplats3D](https://github.com/mkkellogg/GaussianSplats3D) | MIT | https://github.com/mkkellogg/GaussianSplats3D | 不适用（代码/工具条目） | 不适用 | 2972 | 2025-10-19 | 已核实来源 |

### V-29 虚拟场景与实时电影制作（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-29-001 | [godot](https://github.com/godotengine/godot) | MIT | https://github.com/godotengine/godot | 不适用（代码/工具条目） | 不适用 | 120441 | 2026-11-19 | 已核实来源 |
| V-29-002 | [o3de](https://github.com/o3de/o3de) | NOASSERTION | https://github.com/o3de/o3de | 不适用（代码/工具条目） | 不适用 | 9892 | 2026-11-19 | 已核实来源 |
| V-29-003 | [engine](https://github.com/playcanvas/engine) | MIT | https://github.com/playcanvas/engine | 不适用（代码/工具条目） | 不适用 | 17335 | 2026-11-19 | 已核实来源 |
| V-29-004 | [bevy](https://github.com/bevyengine/bevy) | Apache-2.0 | https://github.com/bevyengine/bevy | 不适用（代码/工具条目） | 不适用 | 49878 | 2026-11-19 | 已核实来源 |
| V-29-005 | [Babylon.js](https://github.com/BabylonJS/Babylon.js) | Apache-2.0 | https://github.com/BabylonJS/Babylon.js | 不适用（代码/工具条目） | 不适用 | 26404 | 2026-11-19 | 已核实来源 |

### V-30 影像修复与画质增强（8 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-30-001 | [Real-ESRGAN](https://github.com/xinntao/Real-ESRGAN) | BSD-3-Clause | https://github.com/xinntao/Real-ESRGAN | 不适用（代码/工具条目） | 不适用 | 37573 | 2024-08-06 | 已核实来源 |
| V-30-002 | [GFPGAN](https://github.com/TencentARC/GFPGAN) | NOASSERTION | https://github.com/TencentARC/GFPGAN | 不适用（代码/工具条目） | 不适用 | 37724 | 2024-07-26 | 已核实来源 |
| V-30-003 | [CodeFormer](https://github.com/sczhou/CodeFormer) | NOASSERTION | https://github.com/sczhou/CodeFormer | 不适用（代码/工具条目） | 不适用 | 18254 | 2025-11-18 | 已核实来源 |
| V-30-004 | [ECCV2022-RIFE](https://github.com/hzwer/ECCV2022-RIFE) | MIT | https://github.com/hzwer/ECCV2022-RIFE | 不适用（代码/工具条目） | 不适用 | 5707 | 2025-09-10 | 已核实来源 |
| V-30-005 | [chaiNNer](https://github.com/chaiNNer-org/chaiNNer) | GPL-3.0 | https://github.com/chaiNNer-org/chaiNNer | 不适用（代码/工具条目） | 不适用 | 6177 | 2026-11-13 | 已核实来源 |
| V-30-006 | [All-In-One-Deflicker](https://github.com/ChenyangLEI/All-In-One-Deflicker) | Apache-2.0 | https://github.com/ChenyangLEI/All-In-One-Deflicker | 不适用（代码/工具条目） | 不适用 | 765 | 2026-07-14 | 已核实来源 |
| V-30-007 | [vid.stab](https://github.com/georgmartius/vid.stab) | NOASSERTION | https://github.com/georgmartius/vid.stab | 不适用（代码/工具条目） | 不适用 | 997 | 2026-08-14 | 已核实来源 |
| V-30-008 | [DeOldify](https://github.com/jantic/DeOldify) | MIT | https://github.com/jantic/DeOldify | 不适用（代码/工具条目） | 不适用 | 18445 | 2024-10-19 | 已核实来源 |

### V-31 交互式与分支叙事视频（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-31-001 | [ink](https://github.com/inkle/ink) | MIT | https://github.com/inkle/ink | 不适用（代码/工具条目） | 不适用 | 5027 | 2026-11-16 | 已核实来源 |
| V-31-002 | [twinejs](https://github.com/klembot/twinejs) | GPL-3.0 | https://github.com/klembot/twinejs | 不适用（代码/工具条目） | 不适用 | 2957 | 2026-10-07 | 已核实来源 |
| V-31-003 | [YarnSpinner](https://github.com/YarnSpinnerTool/YarnSpinner) | MIT | https://github.com/YarnSpinnerTool/YarnSpinner | 不适用（代码/工具条目） | 不适用 | 2876 | 2026-11-19 | 已核实来源 |
| V-31-004 | [renpy](https://github.com/renpy/renpy) | 无（未检出） | https://github.com/renpy/renpy | 不适用（代码/工具条目） | 不适用 | 7037 | 2026-11-20 | 已核实来源 |
| V-31-005 | [video.js](https://github.com/videojs/video.js) | NOASSERTION | https://github.com/videojs/video.js | 不适用（代码/工具条目） | 不适用 | 40225 | 2026-11-20 | 已核实来源 |

### V-32 产品广告与商业展示动效（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| V-32-001 | [model-viewer](https://github.com/google/model-viewer) | Apache-2.0 | https://github.com/google/model-viewer | 不适用（代码/工具条目） | 不适用 | 8348 | 2026-11-18 | 已核实来源 |
| V-32-002 | [drei](https://github.com/pmndrs/drei) | MIT | https://github.com/pmndrs/drei | 不适用（代码/工具条目） | 不适用 | 10178 | 2026-11-17 | 已核实来源 |
| V-32-003 | [three-gpu-pathtracer](https://github.com/gkjohnson/three-gpu-pathtracer) | MIT | https://github.com/gkjohnson/three-gpu-pathtracer | 不适用（代码/工具条目） | 不适用 | 2059 | 2026-11-20 | 已核实来源 |
| V-32-004 | [engine](https://github.com/playcanvas/engine) | MIT | https://github.com/playcanvas/engine | 不适用（代码/工具条目） | 不适用 | 17335 | 2026-11-19 | 已核实来源 |
| V-32-005 | [blender](https://github.com/blender/blender) | NOASSERTION | https://github.com/blender/blender | 不适用（代码/工具条目） | 不适用 | 22236 | 2026-11-19 | 已核实来源 |

### W-01 文案自动转分镜（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-01-001 | [MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo) | MIT | https://github.com/harry0703/MoneyPrinterTurbo | 不适用（代码/工具条目） | 不适用 | 144718 | 2026-11-19 | 已核实来源 |
| W-01-002 | [MoneyPrinter](https://github.com/FujiwaraChoki/MoneyPrinter) | MIT | https://github.com/FujiwaraChoki/MoneyPrinter | 不适用（代码/工具条目） | 不适用 | 14226 | 2026-03-26 | 已核实来源 |
| W-01-003 | [ShortGPT](https://github.com/RayVentura/ShortGPT) | MIT | https://github.com/RayVentura/ShortGPT | 不适用（代码/工具条目） | 不适用 | 8184 | 2025-02-10 | 已核实来源 |
| W-01-004 | [Text-To-Video-AI](https://github.com/SamurAIGPT/Text-To-Video-AI) | MIT | https://github.com/SamurAIGPT/Text-To-Video-AI | 不适用（代码/工具条目） | 不适用 | 7 | 2026-10-08 | 已核实来源 |
| W-01-005 | [NarratoAI](https://github.com/linyqh/NarratoAI) | MIT | https://github.com/linyqh/NarratoAI | 不适用（代码/工具条目） | 不适用 | 11884 | 2026-10-24 | 已核实来源 |
| W-01-006 | [storyboarder](https://github.com/wonderunit/storyboarder) | 无（未检出） | https://github.com/wonderunit/storyboarder | 不适用（代码/工具条目） | 不适用 | 3960 | 2024-03-17 | 已核实来源 |

### W-02 镜头与动效自动匹配（4 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-02-001 | [OpenMontage](https://github.com/OpenMontageInc/OpenMontage) | AGPL-3.0 | https://github.com/OpenMontageInc/OpenMontage | 不适用（代码/工具条目） | 不适用 | 81762 | 2026-11-16 | 已核实来源 |
| W-02-002 | [hyperframes](https://github.com/heygen-com/hyperframes) | Apache-2.0 | https://github.com/heygen-com/hyperframes | 不适用（代码/工具条目） | 不适用 | 87050 | 2026-11-20 | 已核实来源 |
| W-02-003 | [motion-skills](https://github.com/iart-ai/motion-skills) | MIT | https://github.com/iart-ai/motion-skills | 不适用（代码/工具条目） | 不适用 | 1923 | 2026-11-18 | 已核实来源 |
| W-02-004 | [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | BSD-3-Clause | https://github.com/Breakthrough/PySceneDetect | 不适用（代码/工具条目） | 不适用 | 5586 | 2026-11-18 | 已核实来源 |

### W-03 参数化动效渲染（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-03-001 | [remotion](https://github.com/remotion-dev/remotion) | NOASSERTION | https://github.com/remotion-dev/remotion | 不适用（代码/工具条目） | 不适用 | 74360 | 2026-11-19 | 已核实来源 |
| W-03-002 | [revideo](https://github.com/midrender/revideo) | MIT | https://github.com/midrender/revideo | 不适用（代码/工具条目） | 不适用 | 4218 | 2026-07-15 | 已核实来源 |
| W-03-003 | [motion-canvas](https://github.com/motion-canvas/motion-canvas) | MIT | https://github.com/motion-canvas/motion-canvas | 不适用（代码/工具条目） | 不适用 | 20072 | 2026-07-02 | 已核实来源 |
| W-03-004 | [nexrender](https://github.com/inlife/nexrender) | MIT | https://github.com/inlife/nexrender | 不适用（代码/工具条目） | 不适用 | 1867 | 2026-06-03 | 已核实来源 |
| W-03-005 | [editly](https://github.com/mifi/editly) | MIT | https://github.com/mifi/editly | 不适用（代码/工具条目） | 不适用 | 5633 | 2025-05-12 | 已核实来源 |

### W-04 自动字幕与音画同步（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-04-001 | [whisperX](https://github.com/m-bain/whisperX) | BSD-2-Clause | https://github.com/m-bain/whisperX | 不适用（代码/工具条目） | 不适用 | 25499 | 2026-11-12 | 已核实来源 |
| W-04-002 | [stable-ts](https://github.com/jianfch/stable-ts) | MIT | https://github.com/jianfch/stable-ts | 不适用（代码/工具条目） | 不适用 | 2284 | 2026-05-30 | 已核实来源 |
| W-04-003 | [whisper-timestamped](https://github.com/linto-ai/whisper-timestamped) | AGPL-3.0 | https://github.com/linto-ai/whisper-timestamped | 不适用（代码/工具条目） | 不适用 | 2860 | 2026-09-28 | 已核实来源 |
| W-04-004 | [VideoCaptioner](https://github.com/WEIFENG2333/VideoCaptioner) | GPL-3.0 | https://github.com/WEIFENG2333/VideoCaptioner | 不适用（代码/工具条目） | 不适用 | 16583 | 2026-09-12 | 已核实来源 |
| W-04-005 | [faster-whisper](https://github.com/SYSTRAN/faster-whisper) | MIT | https://github.com/SYSTRAN/faster-whisper | 不适用（代码/工具条目） | 不适用 | 26876 | 2026-11-12 | 已核实来源 |
| W-04-006 | [Montreal-Forced-Aligner](https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner) | MIT | https://github.com/MontrealCorpusTools/Montreal-Forced-Aligner | 不适用（代码/工具条目） | 不适用 | 1917 | 2026-11-16 | 已核实来源 |

### W-05 Blender / Remotion 批量渲染（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-05-001 | [remotion](https://github.com/remotion-dev/remotion) | NOASSERTION | https://github.com/remotion-dev/remotion | 不适用（代码/工具条目） | 不适用 | 74360 | 2026-11-19 | 已核实来源 |
| W-05-002 | [BlenderProc](https://github.com/DLR-RM/BlenderProc) | GPL-3.0 | https://github.com/DLR-RM/BlenderProc | 不适用（代码/工具条目） | 不适用 | 3802 | 2026-01-20 | 已核实来源 |
| W-05-003 | [OpenCue](https://github.com/AcademySoftwareFoundation/OpenCue) | Apache-2.0 | https://github.com/AcademySoftwareFoundation/OpenCue | 不适用（代码/工具条目） | 不适用 | 1009 | 2026-11-19 | 已核实来源 |
| W-05-004 | [cgru](https://github.com/CGRU/cgru) | LGPL-3.0 | https://github.com/CGRU/cgru | 不适用（代码/工具条目） | 不适用 | 302 | 2026-10-18 | 已核实来源 |
| W-05-005 | [nexrender](https://github.com/inlife/nexrender) | MIT | https://github.com/inlife/nexrender | 不适用（代码/工具条目） | 不适用 | 1867 | 2026-06-03 | 已核实来源 |

### W-06 自动剪辑与时间线生成（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-06-001 | [auto-editor](https://github.com/WyattBlue/auto-editor) | Unlicense | https://github.com/WyattBlue/auto-editor | 不适用（代码/工具条目） | 不适用 | 6010 | 2026-11-20 | 已核实来源 |
| W-06-002 | [PySceneDetect](https://github.com/Breakthrough/PySceneDetect) | BSD-3-Clause | https://github.com/Breakthrough/PySceneDetect | 不适用（代码/工具条目） | 不适用 | 5586 | 2026-11-18 | 已核实来源 |
| W-06-003 | [moviepy](https://github.com/Zulko/moviepy) | MIT | https://github.com/Zulko/moviepy | 不适用（代码/工具条目） | 不适用 | 15173 | 2026-08-26 | 已核实来源 |
| W-06-004 | [OpenTimelineIO](https://github.com/AcademySoftwareFoundation/OpenTimelineIO) | Apache-2.0 | https://github.com/AcademySoftwareFoundation/OpenTimelineIO | 不适用（代码/工具条目） | 不适用 | 2104 | 2026-11-19 | 已核实来源 |
| W-06-005 | [FunClip](https://github.com/modelscope/FunClip) | MIT | https://github.com/modelscope/FunClip | 不适用（代码/工具条目） | 不适用 | 6591 | 2026-11-01 | 已核实来源 |
| W-06-006 | [clipsai](https://github.com/ClipsAI/clipsai) | MIT | https://github.com/ClipsAI/clipsai | 不适用（代码/工具条目） | 不适用 | 577 | 2024-01-17 | 已核实来源 |

### W-07 多平台视频适配（4 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-07-001 | [FFmpeg](https://github.com/FFmpeg/FFmpeg) | NOASSERTION | https://github.com/FFmpeg/FFmpeg | 不适用（代码/工具条目） | 不适用 | 67653 | 2026-11-20 | 已核实来源 |
| W-07-002 | [HandBrake](https://github.com/HandBrake/HandBrake) | NOASSERTION | https://github.com/HandBrake/HandBrake | 不适用（代码/工具条目） | 不适用 | 25063 | 2026-11-18 | 已核实来源 |
| W-07-003 | [smartcrop.js](https://github.com/jwagner/smartcrop.js) | MIT | https://github.com/jwagner/smartcrop.js | 不适用（代码/工具条目） | 不适用 | 12961 | 2024-03-16 | 已核实来源 |
| W-07-004 | [satori](https://github.com/vercel/satori) | MPL-2.0 | https://github.com/vercel/satori | 不适用（代码/工具条目） | 不适用 | 14208 | 2026-11-12 | 已核实来源 |

### W-08 素材授权与质量检查（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-08-001 | [vmaf](https://github.com/Netflix/vmaf) | NOASSERTION | https://github.com/Netflix/vmaf | 不适用（代码/工具条目） | 不适用 | 5607 | 2026-11-16 | 已核实来源 |
| W-08-002 | [IQA-PyTorch](https://github.com/chaofengc/IQA-PyTorch) | NOASSERTION | https://github.com/chaofengc/IQA-PyTorch | 不适用（代码/工具条目） | 不适用 | 3452 | 2026-11-12 | 已核实来源 |
| W-08-003 | [scancode-toolkit](https://github.com/aboutcode-org/scancode-toolkit) | NOASSERTION | https://github.com/aboutcode-org/scancode-toolkit | 不适用（代码/工具条目） | 不适用 | 2675 | 2026-11-11 | 已核实来源 |
| W-08-004 | [licensee](https://github.com/licensee/licensee) | MIT | https://github.com/licensee/licensee | 不适用（代码/工具条目） | 不适用 | 922 | 2026-11-16 | 已核实来源 |
| W-08-005 | [c2pa-rs](https://github.com/contentauth/c2pa-rs) | NOASSERTION | https://github.com/contentauth/c2pa-rs | 不适用（代码/工具条目） | 不适用 | 452 | 2026-11-19 | 已核实来源 |
| W-08-006 | [exiftool](https://github.com/exiftool/exiftool) | GPL-3.0 | https://github.com/exiftool/exiftool | 不适用（代码/工具条目） | 不适用 | 5279 | 2026-11-16 | 已核实来源 |
| W-08-007 | [MediaInfo](https://github.com/MediaArea/MediaInfo) | BSD-2-Clause | https://github.com/MediaArea/MediaInfo | 不适用（代码/工具条目） | 不适用 | 2072 | 2026-11-19 | 已核实来源 |

### W-09 动效模板打包与版本管理（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-09-001 | [git-lfs](https://github.com/git-lfs/git-lfs) | NOASSERTION | https://github.com/git-lfs/git-lfs | 不适用（代码/工具条目） | 不适用 | 14605 | 2026-11-06 | 已核实来源 |
| W-09-002 | [dvc](https://github.com/treeverse/dvc) | Apache-2.0 | https://github.com/treeverse/dvc | 不适用（代码/工具条目） | 不适用 | 15984 | 2026-11-16 | 已核实来源 |
| W-09-003 | [changesets](https://github.com/changesets/changesets) | MIT | https://github.com/changesets/changesets | 不适用（代码/工具条目） | 不适用 | 12586 | 2026-11-19 | 已核实来源 |
| W-09-004 | [storybook](https://github.com/storybookjs/storybook) | MIT | https://github.com/storybookjs/storybook | 不适用（代码/工具条目） | 不适用 | 91655 | 2026-11-19 | 已核实来源 |
| W-09-005 | [dotlottie-web](https://github.com/LottieFiles/dotlottie-web) | MIT | https://github.com/LottieFiles/dotlottie-web | 不适用（代码/工具条目） | 不适用 | 951 | 2026-11-18 | 已核实来源 |

### W-10 多 AI 智能体调用接口（9 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| W-10-001 | [servers](https://github.com/modelcontextprotocol/servers) | NOASSERTION | https://github.com/modelcontextprotocol/servers | 不适用（代码/工具条目） | 不适用 | 92117 | 2026-11-19 | 已核实来源 |
| W-10-002 | [A2A](https://github.com/a2aproject/A2A) | Apache-2.0 | https://github.com/a2aproject/A2A | 不适用（代码/工具条目） | 不适用 | 26597 | 2026-11-18 | 已核实来源 |
| W-10-003 | [ag-ui](https://github.com/ag-ui-protocol/ag-ui) | MIT | https://github.com/ag-ui-protocol/ag-ui | 不适用（代码/工具条目） | 不适用 | 20638 | 2026-11-19 | 已核实来源 |
| W-10-004 | [autogen](https://github.com/microsoft/autogen) | CC-BY-4.0 | https://github.com/microsoft/autogen | 不适用（代码/工具条目） | 不适用 | 61946 | 2026-11-12 | 已核实来源 |
| W-10-005 | [crewAI](https://github.com/crewAIInc/crewAI) | MIT | https://github.com/crewAIInc/crewAI | 不适用（代码/工具条目） | 不适用 | 61107 | 2026-11-20 | 已核实来源 |
| W-10-006 | [langgraph](https://github.com/langchain-ai/langgraph) | MIT | https://github.com/langchain-ai/langgraph | 不适用（代码/工具条目） | 不适用 | 45164 | 2026-11-20 | 已核实来源 |
| W-10-007 | [openai-agents-python](https://github.com/openai/openai-agents-python) | MIT | https://github.com/openai/openai-agents-python | 不适用（代码/工具条目） | 不适用 | 30774 | 2026-11-20 | 已核实来源 |
| W-10-008 | [litellm](https://github.com/BerriAI/litellm) | NOASSERTION | https://github.com/BerriAI/litellm | 不适用（代码/工具条目） | 不适用 | 63564 | 2026-11-20 | 已核实来源 |
| W-10-009 | [mcp-for-blender](https://github.com/ahujasid/mcp-for-blender) | MIT | https://github.com/ahujasid/mcp-for-blender | 不适用（代码/工具条目） | 不适用 | 35056 | 2026-11-18 | 已核实来源 |

### A-01 字体与动态排版资产（7 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| A-01-001 | [source-han-sans](https://github.com/adobe-fonts/source-han-sans) | NOASSERTION | https://github.com/adobe-fonts/source-han-sans | OFL-1.1 | https://github.com/adobe-fonts/source-han-sans/blob/HEAD/LICENSE.txt | 17490 | 2025-06-25 | 已核实来源 |
| A-01-002 | [source-han-serif](https://github.com/adobe-fonts/source-han-serif) | NOASSERTION | https://github.com/adobe-fonts/source-han-serif | OFL-1.1 | https://github.com/adobe-fonts/source-han-serif/blob/HEAD/LICENSE.txt | 9846 | 2024-07-30 | 已核实来源 |
| A-01-003 | [LxgwWenKai](https://github.com/lxgw/LxgwWenKai) | OFL-1.1 | https://github.com/lxgw/LxgwWenKai | OFL-1.1 | https://github.com/lxgw/LxgwWenKai | 27122 | 2026-11-19 | 已核实来源 |
| A-01-004 | [smiley-sans](https://github.com/atelier-anchor/smiley-sans) | OFL-1.1 | https://github.com/atelier-anchor/smiley-sans | OFL-1.1 | https://github.com/atelier-anchor/smiley-sans | 14964 | 2024-12-10 | 已核实来源 |
| A-01-005 | [Sarasa-Gothic](https://github.com/be5invis/Sarasa-Gothic) | NOASSERTION | https://github.com/be5invis/Sarasa-Gothic | OFL-1.1 | https://github.com/be5invis/Sarasa-Gothic/blob/HEAD/LICENSE | 13055 | 2026-10-25 | 已核实来源 |
| A-01-006 | [noto-cjk](https://github.com/notofonts/noto-cjk) | 无（未检出） | https://github.com/notofonts/noto-cjk | 未声明（根目录与 README 未检出，字体子目录未核查） | https://github.com/notofonts/noto-cjk | 4164 | 2025-12-16 | 已核实来源 |
| A-01-007 | [fonts](https://github.com/google/fonts) | 无（未检出） | https://github.com/google/fonts | 多种（逐字体不同：OFL/Apache/UFL 等） | https://github.com/google/fonts#license | 20785 | 2026-11-20 | 已核实来源 |

### A-02 图标与矢量资源（8 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| A-02-001 | [lucide](https://github.com/lucide-icons/lucide) | NOASSERTION | https://github.com/lucide-icons/lucide | ISC（部分图标 MIT） | https://github.com/lucide-icons/lucide/blob/HEAD/LICENSE | 25870 | 2026-11-19 | 已核实来源 |
| A-02-002 | [tabler-icons](https://github.com/tabler/tabler-icons) | MIT | https://github.com/tabler/tabler-icons | MIT | https://github.com/tabler/tabler-icons | 22722 | 2026-11-16 | 已核实来源 |
| A-02-003 | [material-design-icons](https://github.com/google/material-design-icons) | Apache-2.0 | https://github.com/google/material-design-icons | Apache-2.0 | https://github.com/google/material-design-icons | 54334 | 2026-10-23 | 已核实来源 |
| A-02-004 | [icons](https://github.com/twbs/icons) | MIT | https://github.com/twbs/icons | MIT | https://github.com/twbs/icons | 8185 | 2026-11-14 | 已核实来源 |
| A-02-005 | [fluentui-emoji](https://github.com/microsoft/fluentui-emoji) | MIT | https://github.com/microsoft/fluentui-emoji | MIT | https://github.com/microsoft/fluentui-emoji/blob/HEAD/LICENSE | 10231 | 2026-08-24 | 已核实来源 |
| A-02-006 | [twemoji](https://github.com/jdecked/twemoji) | MIT | https://github.com/jdecked/twemoji | 图形 CC-BY-4.0（代码 MIT） | https://github.com/jdecked/twemoji/blob/HEAD/LICENSE-GRAPHICS | 1925 | 2026-06-01 | 已核实来源 |
| A-02-007 | [simple-icons](https://github.com/simple-icons/simple-icons) | CC0-1.0 | https://github.com/simple-icons/simple-icons | CC0-1.0（项目整体；单个图标许可不一定是 CC0，且含品牌商标） | https://github.com/simple-icons/simple-icons/blob/HEAD/DISCLAIMER.md | 26238 | 2026-11-19 | 已核实来源 |
| A-02-008 | [icon-sets](https://github.com/iconify/icon-sets) | 无（未检出） | https://github.com/iconify/icon-sets | 多种（逐图标集不同） | https://github.com/iconify/icon-sets/blob/HEAD/collections.md | 1089 | 2026-11-19 | 已核实来源 |

### A-03 3D 模型与材质（4 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| A-03-001 | [glTF-Sample-Assets](https://github.com/KhronosGroup/glTF-Sample-Assets) | 无（未检出） | https://github.com/KhronosGroup/glTF-Sample-Assets | 多种（逐模型不同，如 CC0/CC-BY 等） | https://github.com/KhronosGroup/glTF-Sample-Assets#readme | 1168 | 2026-11-17 | 已核实来源 |
| A-03-002 | [glTF-Sample-Environments](https://github.com/KhronosGroup/glTF-Sample-Environments) | 无（未检出） | https://github.com/KhronosGroup/glTF-Sample-Environments | 未声明 | https://github.com/KhronosGroup/glTF-Sample-Environments | 99 | 2026-10-06 | 已核实来源 |
| A-03-003 | [drei-assets](https://github.com/pmndrs/drei-assets) | 无（未检出） | https://github.com/pmndrs/drei-assets | 未声明（README 有 Attribution 段） | https://github.com/pmndrs/drei-assets#attribution | 29 | 2023-01-04 | 已核实来源 |
| A-03-004 | [mujoco_menagerie](https://github.com/google-deepmind/mujoco_menagerie) | NOASSERTION | https://github.com/google-deepmind/mujoco_menagerie | 多种（逐模型 LICENSE；其余内容 Apache-2.0） | https://github.com/google-deepmind/mujoco_menagerie#license-and-disclaimer | 4385 | 2026-11-10 | 已核实来源 |

### A-04 音效与声音设计（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| A-04-001 | [ZzFX](https://github.com/KilledByAPixel/ZzFX) | MIT | https://github.com/KilledByAPixel/ZzFX | MIT（音效由代码参数生成，无独立音频素材） | https://github.com/KilledByAPixel/ZzFX | 815 | 2026-11-03 | 已核实来源 |
| A-04-002 | [jsfxr](https://github.com/chr15m/jsfxr) | Unlicense | https://github.com/chr15m/jsfxr | Unlicense（音效由代码生成） | https://github.com/chr15m/jsfxr | 467 | 2026-05-05 | 已核实来源 |
| A-04-003 | [blanket](https://github.com/rafaelmardojai/blanket) | GPL-3.0 | https://github.com/rafaelmardojai/blanket | 逐条不同：CC0 / CC BY / CC BY-SA 等 | https://github.com/rafaelmardojai/blanket/blob/HEAD/SOUNDS_LICENSING.md | 2245 | 2026-11-14 | 已核实来源 |
| A-04-004 | [freesound](https://github.com/MTG/freesound) | AGPL-3.0 | https://github.com/MTG/freesound | 不适用（仓库只有网站代码，无音效）；freesound.org 上的音效逐条授权 | https://github.com/MTG/freesound#license | 389 | 2026-11-19 | 已核实来源 |
| A-04-005 | [use-sound](https://github.com/joshwcomeau/use-sound) | MIT | https://github.com/joshwcomeau/use-sound | 不适用（不含音效素材） | https://github.com/joshwcomeau/use-sound | 3163 | 2025-06-10 | 已核实来源 |

### A-05 LUT 与视觉预设（6 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| A-05-001 | [OpenColorIO-Config-ACES](https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES) | BSD-3-Clause | https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES | BSD-3-Clause | https://github.com/AcademySoftwareFoundation/OpenColorIO-Config-ACES | 440 | 2026-10-27 | 已核实来源 |
| A-05-002 | [aces-core](https://github.com/aces-aswf/aces-core) | Apache-2.0 | https://github.com/aces-aswf/aces-core | Apache-2.0 | https://github.com/aces-aswf/aces-core | 863 | 2026-09-11 | 已核实来源 |
| A-05-003 | [t3mujinpack](https://github.com/t3mujinpack/t3mujinpack) | MIT | https://github.com/t3mujinpack/t3mujinpack | MIT | https://github.com/t3mujinpack/t3mujinpack | 1095 | 2025-04-02 | 已核实来源 |
| A-05-004 | [AgX](https://github.com/sobotka/AgX) | 无（未检出） | https://github.com/sobotka/AgX | 未声明 | https://github.com/sobotka/AgX | 337 | 2025-03-26 | 已核实来源 |
| A-05-005 | [darktable](https://github.com/darktable-org/darktable) | GPL-3.0 | https://github.com/darktable-org/darktable | GPL-3.0（随软件） | https://github.com/darktable-org/darktable | 13477 | 2026-11-19 | 已核实来源 |
| A-05-006 | [OpenColorIO](https://github.com/AcademySoftwareFoundation/OpenColorIO) | BSD-3-Clause | https://github.com/AcademySoftwareFoundation/OpenColorIO | BSD-3-Clause（随软件） | https://github.com/AcademySoftwareFoundation/OpenColorIO | 2143 | 2026-10-01 | 已核实来源 |

### A-06 虚拟摄影与灯光预设（5 条）

| ID | 项目来源 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 | 星标数 | 最近推送日期 | 状态 |
|---|---|---|---|---|---|---|---|---|
| A-06-001 | [camera-controls](https://github.com/yomotsu/camera-controls) | MIT | https://github.com/yomotsu/camera-controls | MIT（预设为代码） | https://github.com/yomotsu/camera-controls | 2452 | 2026-10-21 | 已核实来源 |
| A-06-002 | [drei](https://github.com/pmndrs/drei) | MIT | https://github.com/pmndrs/drei | MIT（代码）；Environment 预设引用的 HDRI 来自外部资源，未核查 | https://github.com/pmndrs/drei | 10178 | 2026-11-17 | 已核实来源 |
| A-06-003 | [theatre](https://github.com/theatre-js/theatre) | Apache-2.0 | https://github.com/theatre-js/theatre | Apache-2.0（代码） | https://github.com/theatre-js/theatre | 13067 | 2024-08-14 | 已核实来源 |
| A-06-004 | [three-gpu-pathtracer](https://github.com/gkjohnson/three-gpu-pathtracer) | MIT | https://github.com/gkjohnson/three-gpu-pathtracer | MIT（代码）；示例模型/HDRI 未核查 | https://github.com/gkjohnson/three-gpu-pathtracer | 2059 | 2026-11-20 | 已核实来源 |
| A-06-005 | [OpenUSD](https://github.com/PixarAnimationStudios/OpenUSD) | NOASSERTION | https://github.com/PixarAnimationStudios/OpenUSD | 自定义（GitHub 标记 Other） | https://github.com/PixarAnimationStudios/OpenUSD | 7659 | 2026-11-18 | 已核实来源 |

## 三、覆盖情况

- 有候选分类：71/71；空类：无。
- 条目最少的分类（各 4 条）：V-25、W-02、W-07、A-03。

## 四、Top 20

| # | 项目来源 | 推荐理由 | 代码许可证 | 代码许可证证据 | 资产许可证 | 资产许可证证据 |
|---|---|---|---|---|---|---|
| 1 | [apache/echarts](https://github.com/apache/echarts) | 数据图表与仪表盘动画，配有 echarts-examples。 | Apache-2.0 | https://github.com/apache/echarts | 不适用（代码/工具条目） | 不适用 |
| 2 | [greensock/GSAP](https://github.com/greensock/GSAP) | 文字拆分、时间线与交互动画。 | 无（未检出） | https://github.com/greensock/GSAP | 不适用（代码/工具条目） | 不适用 |
| 3 | [motiondivision/motion](https://github.com/motiondivision/motion) | 交互、布局动画与 reduced-motion 接口。 | MIT | https://github.com/motiondivision/motion | 不适用（代码/工具条目） | 不适用 |
| 4 | [remotion-dev/remotion](https://github.com/remotion-dev/remotion) | React 参数化视频与批量渲染。 | NOASSERTION | https://github.com/remotion-dev/remotion | 不适用（代码/工具条目） | 不适用 |
| 5 | [xyflow/xyflow](https://github.com/xyflow/xyflow) | React/Svelte Flow 节点编辑器与多 Agent 调度画布。 | MIT | https://github.com/xyflow/xyflow | 不适用（代码/工具条目） | 不适用 |
| 6 | [assistant-ui/assistant-ui](https://github.com/assistant-ui/assistant-ui) | 聊天、工具调用与流式消息组件。 | MIT | https://github.com/assistant-ui/assistant-ui | 不适用（代码/工具条目） | 不适用 |
| 7 | [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | 将智能体运行事件连接到前端交互。 | MIT | https://github.com/ag-ui-protocol/ag-ui | 不适用（代码/工具条目） | 不适用 |
| 8 | [CopilotKit/CopilotKit](https://github.com/CopilotKit/CopilotKit) | 生成式 UI 与人机协同组件。 | MIT | https://github.com/CopilotKit/CopilotKit | 不适用（代码/工具条目） | 不适用 |
| 9 | [rdev/liquid-glass-react](https://github.com/rdev/liquid-glass-react) | React 液态玻璃视觉组件。 | MIT | https://github.com/rdev/liquid-glass-react | 不适用（代码/工具条目） | 不适用 |
| 10 | [barvian/number-flow](https://github.com/barvian/number-flow) | 数字滚动与翻牌动画。 | MIT | https://github.com/barvian/number-flow | 不适用（代码/工具条目） | 不适用 |
| 11 | [motion-canvas/motion-canvas](https://github.com/motion-canvas/motion-canvas) | 代码化矢量动画与编辑器。 | MIT | https://github.com/motion-canvas/motion-canvas | 不适用（代码/工具条目） | 不适用 |
| 12 | [ManimCommunity/manim](https://github.com/ManimCommunity/manim) | 数学、算法和原理讲解动画。 | MIT | https://github.com/ManimCommunity/manim | 不适用（代码/工具条目） | 不适用 |
| 13 | [mrdoob/three.js](https://github.com/mrdoob/three.js) | 3D 交互与产品展示基础引擎。 | MIT | https://github.com/mrdoob/three.js | 不适用（代码/工具条目） | 不适用 |
| 14 | [theatre-js/theatre](https://github.com/theatre-js/theatre) | 关键帧曲线与镜头轨迹编辑。 | Apache-2.0 | https://github.com/theatre-js/theatre | Apache-2.0（代码） | https://github.com/theatre-js/theatre |
| 15 | [xzdarcy/react-timeline-editor](https://github.com/xzdarcy/react-timeline-editor) | 可编程多轨时间线与关键帧组件。 | MIT | https://github.com/xzdarcy/react-timeline-editor | 不适用（代码/工具条目） | 不适用 |
| 16 | [m-bain/whisperX](https://github.com/m-bain/whisperX) | 逐词时间戳与字幕对齐。 | BSD-2-Clause | https://github.com/m-bain/whisperX | 不适用（代码/工具条目） | 不适用 |
| 17 | [visgl/deck.gl](https://github.com/visgl/deck.gl) | 地理空间数据与航线可视化。 | MIT | https://github.com/visgl/deck.gl | 不适用（代码/工具条目） | 不适用 |
| 18 | [pmndrs/postprocessing](https://github.com/pmndrs/postprocessing) | 景深、颗粒、光晕等后期效果。 | Zlib | https://github.com/pmndrs/postprocessing | 不适用（代码/工具条目） | 不适用 |
| 19 | [liabru/matter-js](https://github.com/liabru/matter-js) | 2D 物理交互与科学模拟。 | MIT | https://github.com/liabru/matter-js | 不适用（代码/工具条目） | 不适用 |
| 20 | [lxgw/LxgwWenKai](https://github.com/lxgw/LxgwWenKai) | 中文字体，适合字幕与引用排版。 | OFL-1.1 | https://github.com/lxgw/LxgwWenKai | OFL-1.1 | https://github.com/lxgw/LxgwWenKai |

## 五、文件清单

- 本说明：[`docs/CANDIDATES-V2.md`](CANDIDATES-V2.md)
- v2 索引：[`asset-index/candidates-v2.json`](../asset-index/candidates-v2.json)、[`asset-index/candidates-v2.csv`](../asset-index/candidates-v2.csv)（UTF-8 BOM）
- v2 分类浏览（71 类）：[`docs/catalog-v2/`](catalog-v2/)
- 本批在仓库根目录新增加的 45 个分类 README（此前不存在的 UI-12～UI-23、V-16～V-32、W-01～W-10、A-01～A-06）
- v1 历史文件未改动：`asset-index/candidates-v1.csv`、`asset-index/candidates-v1.json`、`docs/CANDIDATES-README.md`，以及 `ui-motion/UI-01`～`UI-11`、`video-motion/V-01`～`V-15` 的原分类 README
