# G-001 任务3｜AI 原生制作研究：方法卡（待 ChatGPT 审核）

- 研究对象：Tim Simmons（频道 Theoretically Media，@TheoreticallyMedia，https://www.youtube.com/channel/UC9Ryt3XOGYBoAJVsBHNGDzA）
- 原视频：《This Cinematic AI Film Workflow Changes Everything》 https://www.youtube.com/watch?v=WKO-YgMQhLI （2026-09-17 上传，19:37，Runway 赞助）
- 本地文件：`source/WKO-YgMQhLI.mp4`（720p/29.97fps，sha256 `e6ecd777…05c`），仅供内部分析，不得二次发布
- 对应成片（未下载、未看）：The Bridge 2.0 https://youtu.be/f8FHas1dmt8 ；2025 原版 https://youtu.be/YDlME4qvER8
- **观看深度声明**：本研究基于"自动字幕全文 + 03:50–12:00 段每 5 秒抽帧 + 12 张关键全分辨率帧及放大裁切"，**不是完整观看，也没有逐帧分析**。音频没有逐段收听，只做了响度和静音统计。详见 `coverage.md`。
- 时间码说明：均指上面这条教程视频的时间，格式 MM:SS（抽帧精度 ±0.5s，字幕时间来自 YouTube 自动字幕）。
- 复核：2026-11-24 已用视频模型复核 6 个片段，并逐条用本地全分辨率帧、tesseract 和放大裁切核对；只有已核实的内容写入本文件（标注“视频模型复核 + 本地帧核实”）。
- 执行状态：三种方法都只到"已观察 + 已推断"。**没有一种已实现或已验证，不得进入正式生产技能库。**

> 选这一条的理由（简）：它是 Tim 本人用 Codex + Runway MCP 完整制作一部短片的屏幕录制，画面上直接展示了剧本、分镜表、Midjourney 提示词、每条生成任务的"理由 + 提示词 + 参考图 + 哈希"、生产看板和会话日志。我们的执行者正好是 Codex，所以可迁移性最高。候选比较见 `coverage.md`。

---

## 方法 M1｜镜头意图卡：把导演意图写成"理由 + 保留/允许/禁止 + 有量纲的运镜"再交给生成模型

### ① 来源
Tim Simmons，《This Cinematic AI Film Workflow Changes Everything》，WKO-YgMQhLI；看板中的每条生成任务详情面板。

### ② 时间码与观察证据（屏幕文字逐字转录）
- **07:18 前后**（帧 `frames/full_438.jpg`，裁切 `crop_438_panel.png`），镜头详情面板字段：
  `Status complete / Batch BR2-FINAL-LYRA / Model seedance-2.5 / Duration 8s / Ratio 21:9 / Resolution 1080p / Dimensions 2206×946 / Codec hevc / Audio yes / Size 6.6 MB / Task ID 8a86508b-… / Submitted Sep 8 04:54 PM / Completed Sep 8 04:59 PM / SHA-256 346280de1abfab6a…`
  REFERENCES：`lyra_current`、`bridge_location` 两张缩略图。
  RATIONALE："Tim approved Lyra's distrustful response as part of the revised ending and authorized fresh bridge angles. One eight-second separate reply complements the single Ghoul voiceover pass; Tim handles QC and editing."
  PROMPT（可见部分）："Create one new 8-second photorealistic cinematic dialogue reaction for The Bridge 2.0,1080p21:9. Use lyra_current as the sole ORIGINAL identity/costume/integrated-axe authority: same scrappy adult copper-haired woman. Use lyra_new_reverse for this fresh oblique medium-close reverse composition, restrained suspicious expression and cool bridge light. The rocky mountain approach is BEHIND Lyra; the castle is beyond her eyeline, never behind her reverse. She addresses the much taller [Ghoul?] camera to screen-right, looking slightly …"（后半被遮挡/截断，方括号为看不清的词）
- **07:50 前后**（`full_470.jpg`，`crop_470_prompt.png`）：
  RATIONALE："Tim explicitly directed going back to BR2-DLG-10 after rejecting the previous retry. One new eight-second performance binds the exact selected DLG10 PNG at both start and end, using concise performance-only direction. No new image or derivative angle; native output will be delivered uncropped, with any actual ratio difference recorded. Current model and requested film settings retained; Premiere untouched."
  PROMPT："Animate this exact image of Lyra for eight seconds. Preserve the image's camera, framing, character placement, eyeline, face, costume, attached axe, bridge and light throughout. Locked camera. Her body and axe remain still. Allow natural breathing, blinking, a small skeptical eyebrow movement and synchronized speech. After a short distrustful pause, Lyra says exactly: "That's it? No spell casting or a knife in my back?" Brief beat after "That's it?" Dry, unimpressed delivery, natural adult female lower register, lightly rough and resonant, conversational rather than theatrical. She …"（后续截断）
- **08:45–09:00**（`full_530.jpg`，`crop_530_prompt.png`）：
  RATIONALE："Tim approved final Bridge coverage and varied angles after accepting the ending dialogue. This exact take supplies Contextual low over-shoulder page discovery; R3 07v1 with 06v3 hall/table geography. Ambient sound only, no music or dialogue. Tim owns output QC; this working R3 frame is not promoted to a canonical selection. Premiere stays untouched."
  PROMPT（中段可见）："[…] lateral tabletop slider move of less than half a meter, maintaining her soft shoulder in the foreground and the same hand-sized leaves below her eyeline. Lyra leans only slightly closer and quietly looks down at the leaves; she does not touch or remove them. Hard raking daylight reveals stone texture and torn paper. Briefly deepen the focus enough to feel her still figure and distant hall, then gently return attention to the leaves. End with a three-second settled hold. No cut, camera orbit around her, focus pumping or wide-angle facial distortion. / Photoreal live-action dark fantasy, native 21:9 full-…"（开头和结尾没有拍到）
- **08:30 前后**（字幕）："I was using the voice mode in Codex … I can give conversational directions … because once again, in that skill folder, essentially, the system knows how I like to prompt. So, we can essentially translate you know, my verbal directions and then create a prompt for me."
- **08:32 前后**（`full_512.jpg`，Codex 对话界面）：用户口语指令 "ok-- keep running those, but she's really tripping on Flail with a Sword. So, let's rerun that and just have her say Any Fool swing a sword, but an axe…"；Codex 回复 "The new 14-second patch is ready, with the requested line: "Any fool can swing a sword, but an axe? That requires power. Precision. Strategy."" 以及 "All three 20-second village alternatives are also saved—handheld chaos, with SFX only and no music explicitly requested. Ready for your review; Premiere remains paused." 下方显示 "Edited 40 files +1,281 -8"，右侧 Sources 列出 "Cinematic Still Creation.png / Codex App Tools / Runway"。

### ③ 创作目的与观众感受（已推断）
- 导演（Tim）只说一句口语判断，比如"她这句台词念不顺，改成……"；助手把它展开成一张结构化的意图卡。理由（RATIONALE）记录这一镜在故事里承担什么、是谁批准的；提示词则把画面拆成三类约束：**保留什么**（身份、构图、视线、光）、**允许什么**（呼吸、眨眼、一个微表情、对口型）、**禁止什么**（切镜、环绕、对焦呼吸、广角变形）。
- 观众感受：同一角色在多镜之间不"换脸"，空间方向不乱（"the castle is beyond her eyeline, never behind her reverse" 是在维护 180° 轴线和反打关系），表演克制，不会出现 AI 常见的过度运动。镜头结尾的 "three-second settled hold" 给剪辑留出可切的静止尾巴。

### ④ 可观察特征
- 运镜写成**有物理量纲的机位动作**："lateral tabletop slider move of less than half a meter"、"Locked camera"。没有写"cinematic camera movement"这类空泛词。
- 提示词同时包含**负向运镜清单**："No cut, camera orbit around her, focus pumping or wide-angle facial distortion."
- 声音在生成阶段被单独约束："Ambient sound only, no music or dialogue"、"SFX only and no music"。
- 每张卡都有批次号、任务 ID、提交和完成时间、SHA-256，可以追溯。

### ⑤ 作者自述 vs 我们推断
- **作者自述（字幕）**：用语音模式口头导演；skill 文件夹让系统"知道我喜欢怎么写提示词"，并把口头指令翻译成提示词（08:30–09:00）。剪辑他最后自己做，因为"I'm just faster"（11:41）。
- **屏幕可见（已观察）**：上面逐字转录的 RATIONALE 和 PROMPT。这些文字很可能由 Astra/Codex 生成，Tim 没有逐句讲解它们的写法。
- **我们推断**：保留/允许/禁止的三段结构、"有量纲运镜 + 负向清单"能降低漂移，这些是我们从文本归纳出来的，作者没有这样总结过，效果也没有经过测量。

### ⑥ 适用条件与失效情形
- 适用：有固定角色或固定场景、需要多镜连续的段落；对白反应镜头、证据特写这类"小动作、强构图"的镜头。
- 失效或反例：
  1. 需要强烈运动的镜头（追逐、爆发式转场）。"Locked camera" 这类约束会让画面呆板。
  2. 生成模型不服从长提示词时，约束越多越可能被部分忽略。Tim 自己也说 agent "sometimes not that great at thinking ahead"（09:41），比如它没想到 Runway 可以输出 ProRes 422 HQ。
  3. 加伊莎涉及**真实人物和真实数据**的镜头不应该用 AI 生成"真实人物表演"，这类镜头的画面责任应该交给真实证据素材（我们的原则"证据决定画面责任"）。AI 意图卡只用于隐喻、场景、氛围和重建示意镜头，并且要标明是示意。

### ⑦ AI 原生实现方案（加伊莎）
1. 输入：锁定的配音和音乐时间轴（来自 Natalie 组的声音时间轴），按句或拍切出镜头槽 `slot_id, t_in, t_out, 叙事功能, 证据责任`。
2. 每个槽先判断**画面责任**：证据（真实文件、图表、新闻截图，走程序化动效）/ 示意（AI 生成）/ 文字图形。只有"示意"槽才生成意图卡。
3. 意图卡字段：`shot_id, batch, story_function, rationale, approved_by, duration（=槽长+尾部静止留量）, ratio, refs[{tag, path, sha256, role: identity|location|style}], keep[], allow[], forbid[], camera{type: locked|slider|dolly|push, axis, magnitude_m, speed}, end_hold_s, audio: "ambient_only"|"none", prompt（由前面字段拼出）, take_ids[], status, selected_take`。
4. 口语导演：用户（或 Codex 导演）只写一句判断，Codex 按卡片模板补全；改动写进 rationale，旧版本不覆盖。
5. 生成时一律不带音乐（"ambient only / no music"），音乐和配音只在主时间轴上统一铺设，保证"声音决定叙事时间"不被各个片段自带的音乐打乱。

### ⑧ 交给 Codex 的验证任务（V1，低成本）
- 素材：Natalie 组产出的同一段 30–60 秒加伊莎配音时间轴（如果暂时没有，就用一段 45 秒的自录测试配音）。
- 步骤：
  1. 写 `shot_card.schema.json`，并写一个从时间轴生成卡片的脚本（不调用生成模型）。
  2. 选 3 个"示意"槽，每槽做 A/B 两版：A = 一句自由描述提示词；B = 意图卡提示词（含 keep/allow/forbid 和有量纲运镜）。每版只生成 1 次，共 6 次生成。生成次数和额度按实际记录，查不到就写"未知"。
  3. 本地测量（必须对生成文件本身测，不能对看板或预览画面测）：
     - 用 ffmpeg/OpenCV 光流测末尾 `end_hold_s` 区间的平均运动幅度。
     - 用 CLIP 或人脸 embedding 计算主体与参考图的相似度。
     - 用 ffmpeg scene 检测片内是否出现意外切镜。
- 通过标准（预先声明，属于候选阈值，不是来自 Tim）：
  - B 版 3/3 无片内意外切镜。
  - B 版末尾 hold 段的光流均值低于 A 版，且至少 2/3 镜头低于 A 版的 50%。
  - B 版参考相似度不低于 A 版。
  - 盲评（用户或 ChatGPT）3 镜中至少 2 镜偏好 B。
  - 所有卡片都能通过 schema 校验，refs 路径全部存在且哈希一致。
- 组合方式：这 3 个镜头直接放进与 Natalie 组共用的 30–60 秒验证样片，音乐退出点和留白由 Natalie 方法决定。

### 复核补充（M1）（来源：视频模型复核 + 本地全分辨率帧核实，2026-11-24；裁切图在 `verify/`）
- **07:19–07:22 Lyra 反打镜头提示词滚动后的后半段**（`verify/c4_p_pair.png`，`[?]` 为低清不确定处）："… behind her reverse. She addresses the much taller Ghoul off-camera to screen-right, looking slightly upward. Any blurred edge of his shoulder is only silent foreground framing; he never speaks. One continuous take, no cuts. She has just unexpectedly been allowed to pass. Give a half-second processing beat, a small skeptical eyebrow shift and level searching stare, then deliver her question dryly and distrustfully, with a short beat after "That's it?" She expects a trick but shows no panic. Underplay the humor. At roughly0.8–5.6seconds say EXACTLY, LYRA ONLY: "That's it? No spell casting or a knife in my back?" Then hold her wary gaze and breathe naturally to [8?] seconds. No extra words, laughs, repetitions or Ghoul answer. Voice follows current Lyra direction: natural adult female lower register, lightly rough and resonant, fully voiced, dry and forceful, a trace of breath from the trek; dramatically intimate, not whispered, shrill or theatrical. This is a fresh still-reference performance with no voice clone or old dialogue/video attached. […]ative lip-synced speech for editing."
  - 新增的可观察特征：**台词落在镜头内的秒级区间**（"At roughly 0.8–5.6 seconds"），前面留 0.5 秒“反应拍”，后面留静止注视到镜头结束。提示词还写明“谁不说话”（"he never speaks"、"LYRA ONLY"、"No … Ghoul answer"）。
  - 对加伊莎的推断：这正是“声音决定叙事时间”在单镜头层面的写法。意图卡里应写 `line_window_s:[0.8,5.6]`、`pre_beat_s:0.5`、`post_hold`，由主时间轴自动算出。
- **08:51–09:03 纸页发现镜头提示词开头和中后段**（`verify/c6_p3.png`）："REFERENCE ROLES: lyra_v3 is the sole exact identity, costume and axe authority. working_camera_frame supplies this take's composition, camera angle, lighting and staging. Re-create and animate that framing as a continuous film shot, no still-image slideshow or collage. If sc08_06_v3 is also bound, it supplies only the table and hall geography. / ONE continuous 15-second contextual discovery shot. Animate the supplied low table-edge over-shoulder composition: pages sharp across the stone, Lyra's shoulder and copper hair soft at one edge. The tagged […]"；中段 "[…] only saturated warm note where visible. Natural practical materials, fine film grain. Real restrained motion and stable geometry, no fantasy glow, no supernatural event. Audio is quiet hall air, distant wind, soft clothes or paper movement when physically appropriate. NO MUSIC, NO DIALOGUE, no speech or voiceover, no human vocalization, no mouthing words. No other person, master, apparition, ghost, vision, memory flash, magic, title, caption, subtitle, logo or black bars. No added explanation or lore. Maintain clean quiet editorial handles at both ends."；后段 "[…] is visible preserve the ONE axe from lyra_v3 secured physically in her existing back carrier, blade above HER LEFT shoulder and haft descending toward HER RIGHT. Hands empty unless the prescribed shot specifically touches a page; no extra axe or separate axe design, no floating straps, no weapon transformation. Keep her alone. No smiles, tears or theatrical emotional acting; quiet ambiguous attention without indicating what the pages mean. / The same loose cream parchment leaves lie on the existing stone table. Each leaf remains hand-held book scale, approximately the area of one open adult hand; […]"
  - 新增的可观察特征：开头先写**参考角色分工**（REFERENCE ROLES：哪张图管身份、哪张管构图机位、哪张只管场景几何），并明确禁止“静帧幻灯片或拼贴”；结尾要求两端留“clean quiet editorial handles”（剪辑余量）；用左右肩写死道具方位，防止镜像翻转。
  - 运镜核对：画面中这条 take 在看板播放器里是**暂停的静帧**（见 coverage.md 的 C6 光流记录），所以实际运镜是否符合“滑轨 < 0.5 米、景深短暂加深、结尾 3 秒静止”，**无法核实**。

### ⑨ 证据状态
效果：**已观察**（屏幕文字）；作用机制：**已推断**；加伊莎迁移：**未实现、未验证**。提示词开头和结尾部分**未知**（没有拍到）。

---

## 方法 M2｜参考锚点体系：角色设定图 → 视频模型 360° 旋转 → 有序带哈希的参考包；失败镜头用"首尾帧绑定同一选定静帧"修复

### ① 来源
同上视频，05:01–06:13（角色与场景参考）、07:50（修复记录）、07:58–08:15（参考清单）。

### ② 时间码与观察证据
- **05:01–05:25（字幕）**："I actually popped over to Midjourney just to get my initial character references and locations." 画面 05:10–05:20 为 Midjourney 界面中的场景图和角色图。
- **05:12 前后**（`full_312.jpg`，`crop_312_prompt.png`），Midjourney "Imagine" 场景提示词全文逐字："Photorealistic cinematic wide establishing shot, ancient weathered stone bridge crossing a narrow mountain ravine toward a severe medieval fortress built into the far cliff. One broad semicircular masonry arch, low parapets capped with rounded stones, square carved posts. Large uneven paving slabs darkened by rain, shallow puddles, sparse moss. Massive charcoal grey fortress walls, squat crenellated towers, slender Gothic spires, huge iron bound wooden gate at bridge's far end. Jagged mountain walls rising on either side, ridges fading into cold blue grey mist. Muddy rocky foreground, scattered boulders, dull olive grass. Three quarter view showing arch, deck, and fortress together. Pale overcast sky, soft cold daylight, low drifting fog, subdued slate and charcoal palette, tactile eroded masonry, dark fantasy location photography, 35mm lens, deep focus. No people, no text." 参数标签：05:12 帧为 `chaos 5`、`ar 9:16`、`stylize 500`、`profile Global V7 Profile`；05:14 帧中**同一段提示词**另一条生成的标签为 `chaos 5`、`ar 16:9`、`stylize 500`、`profile BRIGHT`（`verify/c2_mj314.png`）。也就是说，同一个场景提示词换了画幅和风格档案各出一版。（来源：视频模型复核 + 本地全分辨率帧核实，2026-11-24；裁切图在 `verify/`）
- **05:17–05:20 角色（守门人）Midjourney 提示词逐字**（来源：视频模型复核 + 本地全分辨率帧核实，2026-11-24；裁切图在 `verify/`）："Photorealistic full body portrait, ancient undead male guardian, towering and massively muscular. Enormous chest, broad back, powerful shoulders, thick neck, huge arms, heavily developed thighs. Extremely defined musculature beneath tight dry grey skin, prominent tendons and dark veins. Bald elongated head, pronounced cheekbones, hollow cheeks, narrow flattened nose, intelligent recessed amber eyes. Parchment like skin drawn across skull, mottled temples, slightly receded lips, fine cracks around mouth. Expression patient, composed, faintly amused. Fitted battered ivory iron breastplate of cracked overlapping plates, worn brown leather straps, small thin shoulder caps, low open neckline exposing thick neck and upper chest, enormous upper arms bare. Weathered bracers, narrow armored skirt panels, heavy worn boots, faded taupe cloth strips at waist. Corroded metal, frayed fabric, ancient repairs. Standing upright, hands relaxed at sides. Plain matte white background, even neutral studio lighting, eye level camera. Cinematic dark fantasy creature photography." 带 1 张图像参考缩略图；标签 `chaos 5`、`ar 9:16`、`stylize 500`、`profile V8`（`verify/c2_mj320.png`）。写法特点：先写体型和面部，再写服装材质，最后写**纯白背景 + 均匀棚拍光 + 平视机位**，这是为后续转身和抠像准备的中性设定图条件。
- **05:10–05:25（字幕）**：Tim 回忆原版用死神形象当守门人，原因是"I did not have to lip-sync him"，这次就不再受这个限制。
- **05:25–06:13（字幕）**："The next step in my workflow is to take that character sheet and then generate a 360 rotation of them utilizing whatever video model I'm planning on using. In this case, of course, like CDS 2.5 on Runway. My reasoning for going video for these turnarounds as opposed to using an image editor is … this is speculation on my part … if it's generated by the video model, then the video model knows what the back of it looks the character looks like … So you're going to have, you know, a better chance of maintaining that as you go through the image editing process." 画面 05:30–06:10：角色在灰白无缝背景上原地转身（侧面、背面），共 4 个角色。
- **06:13（字幕）**："now that we have our characters, we have a script, and we have our location back plates, it's time to move on to production."
- **07:50 RATIONALE**（见 M1）："binds the exact selected DLG10 PNG at both start and end … No new image or derivative angle"。
- **07:58 前后 Docs 页**（`full_478.jpg`，`crop_478_diary.png`、`crop_478_refs.png`）：
  "All requests explicitly set Seedance 2.5, 1080p, 21:9, 20 seconds and native sound effects. Seven ordered still references are attached; no source video or audio is bound."
  "Ordered source references" 表：`1 / lyra17`、`2 / mentor`、`3 / book`、`4 / cabin`（来源路径以 `MJ_SELECTS_TIM/theoreticallymedia_…png` 开头）、`5 / runic_pages`、`6 / torn_stubs`（`outputs/dp_revision_2026-09-08/scene_05_book_lesson/BR2-SC05-06.png`、`-07.png`）、`7 / mentor_cabin`（`work/flashback_narration_2026-09-08/Mentor_cabin_refreshed_Tim.png`），每行附 SHA-256。
  道具一致性规则逐字："The current Round 2 book rules apply: one hand-held worn book about 30 × 20cm closed, comfortably between two hands. Pages carry dense invented decorative illegible runic glyphs, no real alphabet or readable title/meaning. Already-missing leaves leave ragged binding stubs near story endings; no new tearing, illustrations, hidden objects or explanation. The original blank-page book image supplies construction/material only."
  剪辑衔接逐字："The ending is the Mentor's silent warm look, matching Tim's refreshed cabin still, to cut into the separately generated Mentor reply. The existing spoken line is not regenerated here."

### ③ 创作目的与观众感受（已推断）
- 用一组带角色标签的锚点（身份、场景、道具、上一镜结尾）来约束生成，让观众在多镜之间认得出"同一个人、同一本书、同一个地方"。道具连贯性写成规则：尺寸、文字不可读、缺页状态只增不减。
- 修复时**不重新生成新角度**，而是把选定的那张静帧同时作为首帧和尾帧，只改表演。这样修好的镜头能无缝插回原来的剪辑位置，相邻镜头不受影响。
- 结尾刻意设计成"无声的温暖目光"，是为了与下一个独立生成的回应镜头**按动作和情绪衔接**。这就是 AI 版的匹配剪辑和反应镜头。

### ④ 可观察特征
场景背板明确要求 "No people, no text"；角色转身在中性灰背景上完成；参考按顺序编号并带语义标签和哈希；道具有尺寸和状态规则；修复记录写明"不改哪些东西"（No new image or derivative angle / Premiere untouched）。

### ⑤ 作者自述 vs 我们推断
- **作者自述**：用 Midjourney 做初始角色和场景参考；用视频模型生成 360° 旋转，理由是"视频模型自己生成的背面更容易被它记住"。**他明确说这是 speculation（猜测）**，没有给出对比数据。
- **已观察（屏幕）**：参考清单、道具规则、首尾帧绑定的修复理由。
- **我们推断**：首尾帧绑定能稳定插回剪辑点；有序参考加哈希能减少"用错参考版本"；360° 视频转身是否真比图像编辑稳定，**未知，需要我们自己测**。

### ⑥ 适用条件与失效情形
- 适用：加伊莎系列里反复出现的**原创**主体，如虚构主持人或角色、标志性道具（账本、芯片模型、K 线屏幕）、固定场景（办公室、交易大厅），以及需要跨镜连续的段落。
- 失效或反例：
  1. 真实公众人物（比如黄仁勋）不应该用 AI 锚点去"生成本人"，有肖像和误导风险，应改用真实证据素材。
  2. 一次性出现的画面不值得建锚点，这时预演决定不投入。
  3. 首尾帧绑定只能修表演和微动作，修不了构图本身错误的镜头。构图错了就应该回到分镜重新生成静帧。
  4. 360° 转身对文字、logo 等细节可能产生幻觉，需要人工挑帧。

### ⑦ AI 原生实现方案
1. **锚点包** `anchors/<entity>/`：`sheet.png`（设定图）、`turnaround.mp4`（视频模型 360°）、`angles/*.png`（从转身视频抽 8 个角度：0/45/…/315°，由人工挑选）、`rules.md`（尺寸、颜色、可变和不可变状态，参照 Tim 的 book rules 写法）、`manifest.json`（tag、role、sha256、来源、授权）。
2. 场景背板一律 "no people, no text"。文字信息由程序化图层后加，保证证据文字可读、准确，不让 AI 去画字。
3. 每次生成按 `identity → location → prop → previous_end_frame` 的顺序传参考，并写入意图卡（M1）。
4. **失败镜头修复梯度**：
   - 表演问题：同一静帧做首尾帧绑定，只改表演提示。
   - 运镜问题：保留静帧，只改 camera 字段。
   - 构图或身份问题：回到静帧阶段重做。
   每次修复都记录 rationale，并写明"不改什么"。
5. **镜头衔接**：上一镜的结尾帧作为下一镜首帧参考，或者设计相同主体位置和运动方向的匹配剪辑，并在意图卡里写 `exit_state` 和 `entry_state`。

### ⑧ 交给 Codex 的验证任务（V2，低成本）
- 建 1 个原创锚点（建议一个虚构的"加伊莎研究员"角色或一件标志性道具，不用真人肖像）：
  - 设定图 1 张；视频转身 1 次；抽 8 个角度。
  - 另做对照组：用图像编辑生成 3 个角度。
  - 两组各用于生成 2 个镜头，共 4 次。
- 本地测量：
  - 主体与 `sheet.png` 的 embedding 相似度，比较两组均值。
  - 修复测试：取 1 个表演失败的镜头，做首尾帧绑定重生成，测首帧和尾帧与选定静帧的 SSIM。
- 通过标准（候选阈值，需要在第一次试跑后校准）：
  - 首尾帧 SSIM ≥ 0.90。
  - 修复后的镜头插回时间轴后，相邻剪辑点不需要再调整（人工确认）。
  - 360° 组的相似度不低于对照组，否则"视频转身"这一步不进技能库，Tim 的猜测按未验证处理。
- 组合：锚点角色或道具出现在共用的 30–60 秒样片中的 2–3 个示意镜头里。

### 复核补充（M2）（来源：视频模型复核 + 本地全分辨率帧核实，2026-11-24；裁切图在 `verify/`）
- **References 页（07:30–07:31，`verify/c4_ref_zoom.png`）**：守门人参考卡命名为 `GUARDIAN-TURN-002_back.png`、`GUARDIAN-TURN-002_facing_screen_left.png`、`GUARDIAN-TURN-002_facing_screen_right.png`、`GUARDIAN-TURN-002_four-view.jpg`，每张标注 “selected frame”。同页下方 LOCATIONS 区有 “Stone bridge” 场景卡。
  - 这条直接支持“转身视频 → 挑选关键角度帧 → 带朝向语义的文件名 → 进入参考包”的流程（已观察）。朝向写成“facing_screen_left/right”，与 M1 提示词里的 “screen-right” 视线方向对应，可以推断是为了维护轴线。
- **05:43–06:12 转身画面（`verify/c3_tile.png`）**：画面中没有任何工具界面（已核实）。白发导师和戴冠反派站在圆形底座上原地转动，呈转台式展示；守门人这段背景是城堡和人群，不是灰底；Lyra 背景为浅蓝灰。转台还是机位环绕，从 1 fps 帧只能初判为转台式；光影是否随转身变化未定量，待复核。
- **字幕原话**（自动字幕）："to be clear, this is speculation on my part, but I I have the sneaky feeling that …"（05:45–05:53）——已核实。作者对“视频转身更稳”的限定确为猜测。

### ⑨ 证据状态
参考清单、提示词和规则：**已观察**；360° 优势：作者自述为猜测，**未知**；首尾帧修复效果：**已推断**；迁移：**未实现、未验证**。

---

## 方法 M3｜制作办公室 + 覆盖看板 + 会话日志：让 AI 制作可追溯、可接力，并诚实区分"已请求"和"已验证"

### ① 来源
同上视频，03:52–04:40（studio skill 文件夹）、06:35–08:20（生产看板、会话日志）、17:29（额度）。

### ② 时间码与观察证据
- **04:10–04:20**（`full_252.jpg`）幻灯片逐字："Inside the project / Film Project/ — CLAUDE.md + SKILL.md: Entry instructions and workflow; references/: Guides, story notes and style; brief/: Prompts and shot lists; assets/: Images, selects and video[s]; tracking/: Status, continuity and resu[lts]"（右侧被画中画遮挡，方括号为推测补全）。
- **04:25–04:30 及 06:20**（`full_268.jpg`）逐字："The production workflow — 01 Story & style: Script, scenes, visual direction; 02 Cast & locations: Character looks, sets and hero props; 03 Shots & stills: Coverage plan, grids, human selects; 04 Video & review: Prompts, takes, selection"。
- **04:38（字幕）**："I can point Claude to it, I can point Codex to it, I can point Kimmy K3 to it. And all of those models will know exactly how my films are structured and how to execute them."
- **05:01（字幕）**："having Astra go through well, like literally watch the first version of it. Obviously, with all of that material, it was able to generate out a script and a shot list." 画面 05:05（`full_305.jpg`，`crop_305_shotlist.png`）："THE BRIDGE / Script + shot breakdown / INITIAL DEVELOPMENT / SEPTEMBER 2026"，"INITIAL SHOT LIST — 38 picture/title shots / 12 black intervals / 33 dialogue entries"，表头 `SHOT / IN / FRAMING / VISIBLE ACTION`，例行：`BR01-S001 00:00:00:00 Wide rear tracking — Red-haired, armored woman walks up a wet, rocky approach toward a stone bridge and ruined fortress. A double-headed axe is strapped across her back.`；`BR01-S004 00:00:09:14 Over-shoulder wide — A hooded skeletal figure stands facing her on the bridge; her shoulder is soft in the right foreground.`；`BR01-S011 00:00:32:10 Rear over-shoulder insert / axe detail`。
- **06:35–07:00（字幕）**："the solution this time around was to build a production dashboard … a very simple HTML file that … sits on my desktop pointed at the folder."
- **06:58**（`full_418.jpg`）看板 Overview：
  - 标签栏（07:48 帧放大 `verify/c4_tabs468.png`）：`Overview`、`BTS / Making Of 28`（另一帧像 29，末位待复核）、`Takes 93`、`Storyboards 107`、`References 8`、`Source Film 38`、`Coverage`、`Docs 122`、`Activity`。顶部状态条低清读数为“80 takes complete · 3 failed · 107/107 storyboards · 0 discarded · 8 reference images · 38 source shots”，字很小，待复核。（来源：视频模型复核 + 本地全分辨率帧核实，2026-11-24；裁切图在 `verify/`）
  - Coverage 页的序列追踪表（07:41 帧 `verify/c5_tracker.png`）列名为 `SEQUENCE / SHOTS / CAST / LOCATIONS / PROPS / FOOTAGE / BOARDS`。FOOTAGE 状态取值可见 `TESTED`（绿）、`NONE`、`n/a`。示例行：`Approach / mountain trek — 2 shots — LYRA (ADULT) — MOUNTAIN APPROACH, STONE BRIDGE — LYRA'S DOUBLE-BLADED AXE — TESTED: BR2-TREK-001, BR2-TREK-002, BR2-TREK-004 — 4 boards`；`Bridge encounter — 14 — LYRA (ADULT), GUARDIAN (GHOUL) — STONE BRIDGE — … — TESTED: BR2-MEET-001…, BR2-OPEN-001…006 — 16 boards`；`Transition (blacks) — 11 — n/a`；`Burning village (apparent flashback) — 6 — YOUNGER LYRA, RAIDERS, CROWNED ANTAGONIST — BURNING VILLAGE (NIGHT) — NONE — 10 boards`。每一行都把“故事序列 → 所需演员、场景、道具 → 已测成片 ID → 分镜数”连起来。（来源：视频模型复核 + 本地全分辨率帧核实，2026-11-24；裁切图在 `verify/`）
  - Storyboards 页卡片命名（07:26 帧 `verify/c4_sb_zoom.png`）：`BR2-SC01-05 [21:9] face · 3 references`、`BR2-SC01-06 [21:9]`（附一句镜头说明，并注明 “3 references”）。（来源：视频模型复核 + 本地全分辨率帧核实，2026-11-24；裁切图在 `verify/`）
  - "WHERE THINGS STAND (from START_HERE.md)"，"BATCHES AT A GLANCE"（如 `BR2-FINAL-LYRA 7 complete`、`BR2-FLASH-ASHEN 0 complete, 1 failed`）。
  - "COVERAGE SUMMARY"：`Footage tested: Approach / mountain trek, Bridge encounter`；`Storyboarded only: Burning village (apparent flashback), Mentor memories (apparent flashback), Training montage (apparent flashback), Cabin memory (apparent flashback), Snowy memory (apparent flashback), Beyond the bridge`；`Nothing yet: none`；`Cast with a reference: Lyra (adult), Guardian (ghoul)`；`Cast still needed: Mentor, Crowned antagonist, Younger Lyra, Raiders`。
- **07:45–08:15（字幕 + 画面）**："this basically served as a little diary for Astra just to know essentially what … we did in every session … when I forgot, it could remind me about stuff." NOTES 列表可见 `START_HERE.md`、`COLOR_CORRECTION_HANDOFF_2026-09-08.md`、`FINAL_LYRA_AXE_RETRY_2026-09-08.md`、`PRODUCTION_CLOSEOUT_2026-09-08.md`、`PROJECT_HANDOFF.md`、`SESSION_STOP_2026-09-10.md`、`README.md` 等。
- **07:58 Docs 页逐字**："All three originals have measured container duration 20.064 seconds, 2206 × 946 video and an audio stream. This verifies metadata only; the requested silence/music constraints and creative performance are not checked by the assistant." 以及 "Requested sound: irregular quiet hearth crackle, parchment, cloth/fur rustle and subtle wood creaks. ABSOLUTELY NO MUSIC, score, pulse, drone, choir, singing, humming, narration or dialogue. These are instructions, not verified properties of output audio."
- **17:29（字幕）**："I used about 70% of my weekly usage on this … I am on like the max spendy pants plan … I left it on ultra a number of times on accident … I probably could have gotten away with like doing it on like medium to low for a lot of this stuff." 17:52："I had it like download and install DaVinci Resolve for me … That was just a total waste of tokens."

### ③ 创作目的与观众感受（已推断）
这一条不直接作用于观众，它保证的是**连续叙事能被做完**：
- 覆盖看板让导演一眼看出哪些段落已经有成片、哪些只有分镜、哪些角色还缺参考，从而决定把额度投在哪里（对应我们的"预演决定哪些镜头值得投入"）。
- 会话日志让多个 AI 或多次会话之间能接力。
- "已请求 ≠ 已验证"的诚实标注，正好对应用户对我们的要求。

### ④ 可观察特征
- 单一文件夹作为"制作办公室"，入口文件是 CLAUDE.md + SKILL.md。
- 四阶段流程：故事风格 → 演员和场景 → 镜头和静帧 → 视频和审片。
- 静态 HTML 看板读取文件夹；镜头 ID 规则形如 `BR01-S001`、`BR2-FINAL-LYRA`、`BR2-FLASH-BOOK-001`。
- 每次会话自动写日志；验证只承认测得的元数据。

### ⑤ 作者自述 vs 我们推断
- **作者自述**：文件夹结构让任何模型都知道怎么做他的片子；看板是"absolute game-changer"；日志用来提醒他；额度约用掉周额度的 70%，并自承有浪费。
- **已观察**：幻灯片、看板字段、日志文字。
- **我们推断**：覆盖看板可以直接作为"预演决定投入"的决策界面；Codex 与 Muse 共享同一个 tracking 目录可以避免重复研究和重复生成。这一条**未验证**。

### ⑥ 适用条件与失效情形
- 适用：超过 10 个镜头、跨多次会话或多个 AI 协作的项目。
- 失效或反例：
  1. 单条 15 秒短视频，建办公室的成本高于收益。
  2. 看板字段如果不是从文件自动生成，而是靠人工维护，很快就会失真。
  3. Tim 的经验显示，让 agent 去做电脑操作类杂活（装软件、在 Premiere 里拖时间线）很慢，也很浪费额度（11:16、17:52）。剪辑最终仍由他本人完成。

### ⑦ AI 原生实现方案
在 `/workspace/ip-team/projects/<片名>/` 建：
- `START_HERE.md`
- `brief/`（脚本、声音时间轴、镜头槽表）
- `references/`（锚点包，见 M2）
- `cards/`（意图卡 JSON，见 M1）
- `assets/takes/`（生成结果，文件名 = shot_id + take 号）
- `tracking/`（`coverage.json`、`sessions/YYYY-MM-DD.md`、`budget.csv`：每次生成的模型、时长、实际可查的额度，查不到就写 unknown）
- `dashboard.html`（读取上述文件的静态页）

Codex 和 Muse 都只从这个目录读写。覆盖状态分五档：已有成片 / 只有分镜 / 只有声音槽 / 缺参考 / 证据素材待取。

### ⑧ 交给 Codex 的验证任务（V3，零生成成本）
- 用 V1 和 V2 的产物搭这个目录和 `dashboard.html`（纯本地，不调用生成模型）。
- 通过标准：
  1. 共用样片的最终时间轴里，每个片段都能在看板上追溯到 意图卡 → 提示词 → 参考（带哈希）→ take 文件（带哈希），覆盖率 100%。
  2. coverage 由脚本从文件自动计算，删除一个 take 后刷新看板，状态自动变化。
  3. 每次会话结束自动追加一条日志。
  4. `budget.csv` 中所有数字都标明来源，无法取得的写 unknown，不估算。
- 组合：这就是共用 30–60 秒样片的项目容器。

### 复核补充（M3）（来源：视频模型复核 + 本地全分辨率帧核实，2026-11-24；裁切图在 `verify/`）
- 会话日志左侧列表（07:58–08:03，`verify/c5_diarylist.png`）逐字可见：`The Bridge 2.0 — pages and final reaction coverage`（outputs/final_push/pages_reaction/README.md · Sep 8 05:02 PM）、`The Bridge 2.0 — approved ending dialogue`、`Remaining flashback montage batch — September 8, 2026`、`Generation Log`（studio/tracking/generation-log.md）、`The Bridge — remaining flashback montages`、`SC03 blades-to-axe montage — September 8, 2026`、`The Bridge 2.0 — blades-to-axe training alternatives`、`Book lesson montage — September 8, 2026`（development/BOOK_MONTAGE_2026-09-08.md）、`The Bridge 2.0 — book lesson montage`、`SC04 winter training montage — September 8`、`Training-end montage — September 8, 2026`、`The Bridge 2.0 — winter montage alternatives`。日志按“产出 README（outputs/…）+ 开发记录（development/…）”两类文件成对出现，每条带路径和时间。
- **方法结论的变化**：本轮复核中，视频模型对 6 个片段的长段“逐字转录”大部分**与画面不符**（26 项核对中：已核实 6、部分核实 4、与画面不符 14、无法核实 2；见 coverage.md）。这是一次真实的“模型报告 ≠ 实际内容”实例，与 Tim 看板里 “These are instructions, not verified properties of output audio” 是同一类问题。由此给 M3 增加一条规则：**任何模型给出的转录、计数、运镜判断，都必须经本地帧、OCR 或测量核实后才能写成“已观察”**；看板中把“模型报告”和“本地核实”分成两栏。同时修正 M1 验证任务 V1 的测量要求：光流必须对生成文件本身测，不能对看板或预览里的暂停帧测（本轮 C6 就是一个暂停的静帧，测得运动近乎为 0，并不说明机位锁定）。
- 原先设想的“C6 实际运镜与提示词不符，可以证明提示词≠结果”**不成立**：画面只给出暂停静帧，**无法核实**，因此没有把它作为证据写入。

### ⑨ 证据状态
结构和字段：**已观察**；效果：作者自述加我们推断；迁移：**未实现、未验证**。

---

## 与 Natalie 组合成同一条验证样片的建议
1. 先用 Natalie 方法锁定配音和音乐时间轴（声音决定叙事时间）。
2. 按时间轴切出镜头槽，为每个槽判定画面责任：证据槽走程序化动效和真实素材，示意槽走 M1 意图卡加 M2 锚点。
3. 生成一律不带音乐，统一在主时间轴混音。
4. M3 目录全程记录。
5. 通过 V1–V3 的标准后，交 ChatGPT 审核；通过审核的方法才可以申请进入正式技能库。
