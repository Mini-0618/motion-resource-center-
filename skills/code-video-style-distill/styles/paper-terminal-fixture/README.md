# 风格底座：paper-terminal-fixture

- 来源视频：`$T/examples/reference-fixture/reference.mp4`（1920x1080 @ 30.0fps，22.805s）
- 蒸馏时间：2026-11-20T09:52:37+08:00
- refs/ 里的关键帧只作内部比对参考，不得随模板或成片分发。

## 色板

| 角色 | HEX | 来源 |
|---|---|---|
| bg | `#F3EFE6` | seen |
| surface | `#1F2330` | seen |
| primary | `#E4572E` | seen |
| accent | `#2E87AB` | seen |
| text | `#1E1C1D` | seen |
| text_muted | `#6E6B6B` | seen |
| code_text | `#EFF3FC` | seen |

## 动效

- 时长档位 {'fast': 0.189, 'base': 0.5, 'slow': 0.867}；入场 `slide-up`，标题 `spring-pop`；错峰 0.733 s
- 缓动 cubic-bezier(0.25, 0.2, 0.12, 1.1)（推测）；转场 {'type': 'slide', 'duration_s': 0.3}

## 元件

- subtitle_bar → 模板段 `None`，分类 ['V-13']（置信度 0.8）
- title_card → 模板段 `title`，分类 ['V-01', 'V-15']（置信度 0.6）
- bullet_list → 模板段 `bullets`，分类 ['UI-09', 'V-01', 'V-10']（置信度 0.7）
- code_block → 模板段 `code`，分类 ['UI-09', 'V-05']（置信度 0.8）
- bar_chart → 模板段 `bars`，分类 ['UI-04', 'V-02']（置信度 0.75）
- number_counter → 模板段 `stat`，分类 ['UI-04', 'V-02', 'V-01']（置信度 0.7）
- keyword_highlight → 模板段 `None`，分类 ['V-01', 'V-13']（置信度 0.65）
- progress_bar → 模板段 `None`，分类 ['UI-01', 'V-15']（置信度 0.7）
- transition → 模板段 `None`，分类 ['UI-02', 'V-07']（置信度 0.7）

## 来源统计

{'seen': 33, 'inferred': 26, 'unknown': 8}

## 待目测补全

- typography.families / vibe: 用 Read 看 contact_sheet.png，判断字形气质（几何/人文/圆体/宋体/手写）并选免费替代
- typography.scale_px.display: 大标题经常读不出来，对照关键帧目测
- layout.decor: 背景网格、光斑、噪点、描边、阴影等装饰
- motion.transition.type: wipe/fade/slide 需看 entry/mid 关键帧确认
- components: 检测器漏掉的元件（图标、箭头、流程图、标注框…）

## 验收

- 测试参考：`examples/reference-fixture/reference.mp4`（本工具自渲染的测试片，不是外部视频）。
- 迭代账本：`work/run2/iteration-ledger.md`，状态 DONE（第 2、3 轮 must 全过），总分 95.7/100；唯一未过的是 should 档 S7（音画卡点比例）。
- 最终修正：`overrides.json`（motion.durations_s.base 0.367 → 0.5）。
