# 风格底座：paper-terminal-9

- 来源视频：`$T/examples/reference-fixture-9/reference9.mp4`（1920x1080 @ 30.0fps，43.2s）
- 蒸馏时间：2026-11-20T13:46:24+08:00
- refs/ 里的关键帧只作内部比对参考，不得随模板或成片分发。

## 色板

| 角色 | HEX | 来源 |
|---|---|---|
| bg | `#F3EFE6` | seen |
| surface | `#1F2330` | seen |
| primary | `#E45730` | seen |
| accent | `#3085A9` | seen |
| text | `#1E1C1D` | seen |
| text_muted | `#6E6B6B` | seen |
| code_text | `#EFF3FC` | seen |

## 动效

- 时长档位 {'fast': 0.195, 'base': 0.455, 'slow': 0.867}；入场 `slide-up`，标题 `spring-pop`；错峰 0.5 s
- 缓动 cubic-bezier(0.22, 0.4, 0.2, 1.05)（推测）；转场 {'type': 'slide', 'duration_s': 0.267}

## 元件

- subtitle_bar → 模板段 `None`，分类 ['V-13']（置信度 0.8）
- title_card → 模板段 `title`，分类 ['V-01', 'V-15']（置信度 0.6）
- bullet_list → 模板段 `bullets`，分类 ['UI-09', 'V-01', 'V-10']（置信度 0.7）
- evidence_frame → 模板段 `evidence`，分类 ['V-04', 'V-05', 'V-09']（置信度 0.75）
- evidence_frame → 模板段 `evidence`，分类 ['V-04', 'V-05', 'V-09']（置信度 0.75）
- timeline → 模板段 `timeline`，分类 ['UI-09', 'V-03', 'V-04']（置信度 0.75）
- code_block → 模板段 `code`，分类 ['UI-09', 'V-05']（置信度 0.8）
- code_block → 模板段 `code`，分类 ['UI-09', 'V-05']（置信度 0.55）
- compare_columns → 模板段 `compare`，分类 ['UI-09', 'V-03', 'V-05']（置信度 0.75）
- flow_chart → 模板段 `flow`，分类 ['UI-09', 'V-03', 'V-10']（置信度 0.75）
- bar_chart → 模板段 `bars`，分类 ['UI-04', 'V-02']（置信度 0.75）
- number_counter → 模板段 `stat`，分类 ['UI-04', 'V-02', 'V-01']（置信度 0.7）
- keyword_highlight → 模板段 `None`，分类 ['V-01', 'V-13']（置信度 0.65）
- progress_bar → 模板段 `None`，分类 ['UI-01', 'V-15']（置信度 0.7）
- transition → 模板段 `None`，分类 ['UI-02', 'V-07']（置信度 0.7）

## 来源统计

{'seen': 44, 'inferred': 27, 'unknown': 8}

## 待目测补全

- typography.families / vibe: 用 Read 看 contact_sheet.png，判断字形气质（几何/人文/圆体/宋体/手写）并选免费替代
- typography.scale_px.display: 大标题经常读不出来，对照关键帧目测
- layout.decor: 背景网格、光斑、噪点、描边、阴影等装饰
- motion.transition.type: wipe/fade/slide 需看 entry/mid 关键帧确认
- components: 检测器漏掉的元件（图标、箭头、流程图、标注框…）
