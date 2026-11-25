# G-001 任务3｜实际覆盖范围与待复核点

## 选片过程（共比较 5 条候选）
| # | 视频 | 频道（已核实） | 时长 | 判断 |
|---|---|---|---|---|
| 1 | **This Cinematic AI Film Workflow Changes Everything**（WKO-YgMQhLI，2026-09-17）✅ 选中 | Theoretically Media @TheoreticallyMedia（UC9Ryt3XOGYBoAJVsBHNGDzA） | 19:37 | 完整片子的真实制作屏幕录制：剧本、分镜表、MJ 提示词、每条任务的理由/提示词/参考、看板、日志、调色、混音；执行者是 Codex，与我们的分工一致 |
| 2 | Don't Buy an AI Film Studio. Build Yours.（aTqMKA6OQ_M，2026-06-11） | 同上 | 19:35 | 同一套方法的早期版本（Claude + Martini，53 个镜头 / 160 次生成），另有文字版拆解。作为下一轮的备选对照 |
| 3 | AI Filmmaking Complete Workflow (Full Step-By-Step Roadmap)（221dH0j07Ic，2025-11-22） | Tausif Khalid @tausifkhalid（UC8NHl401h85KToXIf5VFqrQ） | 27:54 | 偏路线图，屏幕实操只在 17:17–26:03 一段，深度不如 1 |
| 4 | How to Turn ANY Storyboard Into an AI Video（12vJv4Yw5L8，2026-09-29） | Sebastien Jefferies @SebastienJefferies（UCqcCVUAeQg90KQknq7H-7uA） | 14:45 | 分镜宫格 → Seedance 的提示词实操，很具体，但只有单段短片，且带 OpenArt 联盟推广。适合作为下一轮"分镜→镜头"的专项对照 |
| 5 | Build an AI Film Studio on Your Desktop \| Tim Simmons（TC6QYbROPlo） | Teachable @TeachableTV（不是本人频道） | 63:12 | 网络研讨会，无章节；不是本人频道，放弃 |

**身份核实**：
- 只核实了频道名、ID 和链接，没有读频道 about 页。
- Tim Simmons ↔ Theoretically Media 的对应关系依据以下几点：Teachable 视频标题写明"Tim Simmons"并涉及同一主题；本片赞助链接带 `utm_content=Tim`；看板文字反复出现 "Tim approved…"、"MJ_SELECTS_TIM"；出镜者与 Teachable 视频为同一人（目测）。
- 片尾 "My name is" 之后自动字幕被截断，因此没有拿到本人自报姓名的证据。
- 结论：高置信，未做官方页面核实。

## 下载
- 视频：成功，720p mp4，`source/WKO-YgMQhLI.mp4`，sha256 `e6ecd77746100e3b73e20e75516190effd8c182369d84fa04b82f5924731305c`，1280×720，30000/1001 fps，AAC 44.1kHz 立体声，1177.39s。
- 字幕：yt-dlp 抓字幕返回 HTTP 429，没有重试，改用 TubeAlfred transcript 接口取得英文**自动**字幕（541 条），存为 `source/WKO-YgMQhLI.transcript.en.auto.json` 和 `.txt`。自动字幕有识别错误，例如 "CDS 2.5" 实为 Seedance 2.5，"Kimmy K3" 原词待复核。
- 对应成片 The Bridge 2.0（f8FHas1dmt8）和 2025 原版（YDlME4qvER8）：**没有下载，也没有观看**。本轮只看了教程里 00:54–01:24 的两版对比片段的抽帧。

## 实际看了什么（不是完整观看）
- 字幕：全片自动字幕通读一遍。
- 抽帧：每 5 秒 1 帧，拼成 3×3 宫格，实际读过的宫格覆盖原片 00:49–01:32、03:50–09:45、10:35–11:15。
- 已生成但**没有读**的宫格：01:34–01:52、09:50–10:30、11:20–12:13，以及 12:13 之后的全部（赞助段、调色、Fusion、混音、额度、结语）。这些部分的分析只依据字幕。
- 全分辨率关键帧 12 张，以及放大裁切 8 张，见 `frames/`。M1–M3 中逐字转录的屏幕文字全部来自这些裁切。
- 音频：**没有逐段收听**。只做了本地统计：
  - EBU R128 整体响度 -14.1 LUFS，LRA 4.5 LU。
  - silencedetect（-35dB，≥0.6s）未检出静音段（讲解加背景声连续）。
  - ffmpeg scene>0.3 检出 112 个切点，平均镜头约 10.4s。这个数字对录屏和画中画混合内容只作参考，未复核。
  - 结果在 `analysis/`。
- 三层时间轴：本片是教程，没有输出完整的 shots.csv 和 audio-timeline.csv，只按"作者讲解的制作步骤"建立了内容段落轴（章节加字幕）。如需完整 V1.1 七件套，另行安排。

## 待复核点
1. 三处提示词都只拍到一部分。2026-11-24 复核后，07:18 Lyra 反打镜头的后半段、08:50 纸页镜头的开头和中后段已经通过本地帧补全（见 methods.md M1 复核补充）。07:50 DLG10 修复镜头的后半段在窗口内没有滚动，仍未知。
2. 看板标签计数（BTS、References）和顶部状态条的文字看不清。
3. 360° 转身用的是哪个模型、提示词是什么，画面上没有出现。字幕说的是 Seedance 2.5 on Runway。
4. 所有 RATIONALE 和 PROMPT 文字推测是 Astra/Codex 生成的，Tim 是否逐条修改过，未知。
5. 本片由 Runway 赞助，涉及 Runway 功能的评价（ProRes、Ruby）需要按赞助内容看待。
6. Tim 说"约 1 天半完成"和"约用掉周额度 70%"均为本人自述，未核实。
7. 我们这边的额度：本轮调用了 1 次 TubeAlfred transcript（接口回报 credits_charged 1，剩余 47）。yt-dlp 和 ffmpeg 都是本地运行，没有调用视频生成模型。其余模型消耗我这里查不到明细。

## 文件
- `methods.md`：3 张方法卡
- `clips/`：6 段 ≤40s 片段，以及 `QUESTIONS.md`、`SHA256SUMS`
- `frames/`：宫格、关键帧、裁切
- `analysis/`：切点、静音、响度
- `source/`：原片、字幕、5 条候选的精简元数据

## 视频模型复核结果的本地核对（2026-11-24）
方法：只在 C1–C6 的原片时间窗内抽帧（1 fps，共 225 帧），用 tesseract（OMP_THREAD_LIMIT=1）做 OCR 粗筛，再对关键帧做放大裁切后看图逐字核对。C6 运镜用 10 fps 灰度帧做相位相关位移、帧间平均差和拉普拉斯方差测量（脚本 `verify/flow_measure.py`，结果 `verify/flow_520_546.csv`）。没有全片重扫，也没有再调用视频模型。
背景：视频模型把 6 段当成了一条 40 秒合辑处理，可能被降采样，长段“逐字转录”存在幻觉风险。

| # | 片段 | 视频模型的说法 | 结果 | 本地证据 / 实际内容 |
|---|---|---|---|---|
| 1 | C1 | 幻灯片 Film Project/、CLAUDE.md + SKILL.md、references/、brief/、assets/、tracking/ | 已核实 | `frames/full_252.jpg` |
| 2 | C1 | 第 4 阶段 “04 Video & review” | 已核实 | `frames/full_268.jpg` |
| 3 | C1 | tracking/ = “Status, continuity and results” | 部分核实 | “Status, continuity and resu…” 可见；04:10–04:24 每一帧尾词都被画中画遮挡，“results” 无法核实 |
| 4 | C1 | assets/ = “Images, selects and video” | 部分核实 | “Images, selects and video…” 可见，词尾（video/videos）被遮挡 |
| 5 | C2 | BR01-S012 “The guardian raises a rusted sword…” | 与画面不符 | 实际为 “The guardian turns from a slight side angle to[…]”（后半被遮挡） |
| 6 | C2 | BR01-S013 “The woman's eyes widen slightly…” | 与画面不符 | 实际为 “Close-up — The woman speaks forcefully, then fixes the[…]”（`verify/c2_rows.png`） |
| 7 | C2 | 角色 MJ 提示词 “Full body 3/4 turn character sheet … --ar 16:9 --v 6.0 --style raw” | 与画面不符 | 实际为 “Photorealistic full body portrait, ancient undead male guardian …”，标签 chaos 5 / ar 9:16 / stylize 500 / profile V8（`verify/c2_mj320.png`，已写入 M2） |
| 8 | C2 | Tim 说用死神是 “because I did not have to lip sync him” | 已核实 | 自动字幕 05:20–05:25 |
| 9 | C3 | 转台式旋转 | 部分核实 | 导师、反派站在圆形底座上原地转动，呈转台式；1 fps 无法区分全部片段（`verify/c3_tile.png`） |
| 10 | C3 | 灰背景固定 | 与画面不符 | 导师和反派是浅灰底；守门人背景为城堡和人群；Lyra 为浅蓝灰 |
| 11 | C3 | 光影随转身变化 | 无法核实 | 未做定量测量 |
| 12 | C3 | 无工具界面 | 已核实 | 05:43–06:12 每秒帧均无界面 |
| 13 | C3 | 限定语 “to be clear this is speculation on my part”、“I have this sneaky feeling” | 已核实 | 字幕原文为 “…to be clear, this is speculation on my part, but I I have **the** sneaky feeling…”（一词之差） |
| 14 | C4 | PROMPT 开头 “Cinematic 24p over-the-shoulder … Aloy-esque … Slow push-in.” | 与画面不符 | 实际开头 “Create one new 8-second photorealistic cinematic dialogue reaction for The Bridge 2.0 …”，滚动后段已转录进 M1 |
| 15 | C4 | 标签 SHOTS(56) STORYBOARDS(27) REFERENCES(18) ORIGINAL FILM(48) … | 与画面不符 | 实际为 BTS / Making Of 28(29?)、Takes 93、Storyboards 107、References 8、Source Film 38、Coverage、Docs 122、Activity |
| 16 | C4 | Storyboards 命名如 BR01-S001-v1 | 与画面不符 | 实际为 `BR2-SC01-05 [21:9] … 3 references` |
| 17 | C4 | References 按角色（Lyra、Guardian）分组 | 部分核实 | 窗口内只看到 Guardian 组（GUARDIAN-TURN-002_*）和 LOCATIONS（Stone bridge），没有看到 Lyra 组 |
| 18 | C5 | 追踪表列 SCENES, SHOTS, ASSETS, GREEN GEN, PROPS, FINALS | 与画面不符 | 实际为 SEQUENCE / SHOTS / CAST / LOCATIONS / PROPS / FOOTAGE / BOARDS |
| 19 | C5 | 状态 COMPLETE(绿)/MISSING(红) | 与画面不符 | 实际为 TESTED（绿）/ NONE / n/a |
| 20 | C5 | PROMPT 后半 “…no body movement whatsoever … DO NOT animate the pages … at 6 seconds she looks up … Dry, uncompressed delivery …” | 与画面不符 | 窗口内面板没有滚动，可见文字为 “Locked camera. Her body and axe remain still … Dry, unimpressed delivery …”；视频模型的说法均未出现 |
| 21 | C5 | 日志标题 Desk lesson montage / Runway - working out camera bugs / … | 与画面不符 | 实际标题见 M3 复核补充（如 “Book lesson montage — September 8, 2026”），日期均为 Sep 8 |
| 22 | C6 | 用户口语指令：去掉转头和摇镜、盯着剑皱眉 | 与画面不符 | 实际为 “ok-- keep running those, but she's really tripping on Flail with a Sword. So, let's rerun that and just have her say Any Fool swing a sword, but an axe…” |
| 23 | C6 | 助手回复提到 “new 14-second patch” | 已核实 | “The new 14-second patch is ready, with the requested line: …”（`frames/full_512.jpg`） |
| 24 | C6 | 编辑文件 docs/Desk_lesson_montage_2025-09-08.md、BR01-FINAL-P504-001_* | 与画面不符 | 实际为 work/flashback_narration_2026-09-08/flail_patch/maxim_voice_upload.json、work/generation/BR2-FLASH-LYRA-002-PATCH-002/submitted_request.json、…/dialogue.json |
| 25 | C6 | PROMPT 开头 “C&E continuous 14-second center-cut discovery shot.” | 与画面不符 | 实际开头 “REFERENCE ROLES: lyra_v3 is the sole exact identity …”，正文为 “ONE continuous 15-second contextual discovery shot.”（`verify/c6_p3.png`） |
| 26 | C6 | 纸页镜头实际是锁定机位，没有横移和景深变化 | 无法核实 | 08:46.5–09:03.5 看板播放器区域的帧间平均差约 0.00–0.04（0–255 灰度），相位相关位移 0 px，拉普拉斯方差稳定在 794–807：画面是**暂停的静帧**，不是播放中的成片。静帧不能证明机位锁定，所以视频模型这条判断没有依据 |

合计：已核实 6，部分核实 4，与画面不符 14，无法核实 2。只有“已核实”和“部分核实中可见的部分”写入了 methods.md。

### 新增待复核（来自上表）
- #3、#4 尾词：需要无画中画的源（例如 Tim 的 newsletter 或教程原稿）。
- #11 转身光影变化：需对 05:43–06:12 做逐帧亮度分布测量。
- #26 纸页镜头的实际运镜：要下载成片 The Bridge 2.0（f8FHas1dmt8），定位该镜头后再做光流测量。成片尚未取得。
- #15 BTS 计数是 28 还是 29，以及顶部状态条的读数（低清）。
- 07:20 提示词中的 “breathe naturally to [8?] seconds” 一处低清词。
- 视频模型这次复核的结论整体不可直接采信。以后视频模型的输出一律先标“待本地核实”。
