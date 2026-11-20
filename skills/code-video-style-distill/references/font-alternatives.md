# 字体替代表（免费 / 开源可商用）

用途：distill 只能推测“字体气质”，原字体身份一律记为 `unknown`。复刻时按气质从下表选替代字体，
**绝不复制参考片的字体文件**。表格结构思路参考 obaid1dev/dea `references/font-alternatives.md`（MIT），内容为本工具自写。

> 许可证会变：下表标“核对条款”的，使用前去官方页面确认商用范围。本机已装：Inter、Inter Tight、JetBrains Mono、Noto Sans/Serif CJK、Geist Mono、Source Sans 3。

| 常见商用/系统字体（参考片里可能是） | 气质 | 免费替代（首选 → 备选） | 许可证 |
|---|---|---|---|
| SF Pro / Helvetica Neue / Arial | 中性无衬线 | Inter → Arimo → Geist | SIL OFL 1.1 / Apache-2.0 |
| Gotham / Proxima Nova | 几何无衬线 | Montserrat → Manrope | SIL OFL 1.1 |
| Futura / Avenir | 几何圆润 | Jost → Nunito Sans | SIL OFL 1.1 |
| DIN / Eurostile | 工业窄体 | Barlow / Barlow Condensed → Rajdhani | SIL OFL 1.1 |
| SF Mono / Menlo / Consolas / Operator Mono | 代码等宽 | JetBrains Mono → Fira Code → Geist Mono | SIL OFL 1.1 |
| 苹方 / 微软雅黑 / 方正兰亭黑 | 中文现代黑体 | 思源黑体 Source Han Sans SC（= Noto Sans CJK SC）→ HarmonyOS Sans SC → MiSans | OFL / 华为、小米免费商用许可（核对条款） |
| 方正粗黑 / 汉仪旗黑 Heavy | 中文粗黑标题 | 思源黑体 Heavy → 阿里巴巴普惠体 Heavy → 站酷高端黑 | OFL / 阿里、站酷免费商用（核对条款） |
| 方正书宋 / 华文宋体 | 中文宋体 | 思源宋体 Source Han Serif SC（= Noto Serif CJK SC）| SIL OFL 1.1 |
| 手写 / 卡通中文 | 活泼手写 | 站酷快乐体 → 站酷小薇 LOGO 体 | 站酷免费商用（核对条款） |

调参顺序：先对照 `contact_sheet.png` 调字号 → 字距 (`letter_spacing_em`) → 字重 (`weights`)，再确认许可证。
