# MotionVideo 财经动效研究

2026-11-26 核查。5 条候选方法、4 个带时间码的画廊案例。MCP 匿名检索已实测，HyperFrames 检查止于源码、参数和时间轴。5 条方法均未渲染，生产可用数为 0。

## 选镜速查

|口播需要观众看懂什么|先找现有条目|可借用的动作|使用边界|
|---|---|---|---|
|前提和判断如何衔接|title-motion、caption-editorial-emphasis|逐行揭示，公开建议每行 500–700 毫秒，行间错开 80–120 毫秒|中文按语义断行。现有逐词强调需要改写，横向擦入的方向也与逐行上揭不同。|
|哪个真实数字发生变化|chart-story、07-01 证据定位、07-05 比例比较|引线从数据点向外画，一次解释一个值，每行短标签至少停 1 秒|日期、单位、指标口径先出现。只有两次观测时可用并列端点，线段容易让人误读期间走势。|
|档案原页与现代解读如何区分|camera-rig-depth-stack、07-01|原页、注释、标题分层。库中的空间卡片提供 CSS 变量，需自行驱动时间轴|读手写字时停住原件，视差只用于编辑添加的层。|
|一个细节属于哪份证据|07-01、camera.mjs|先读细节，再从约 1.3 倍按对数尺度拉回原页，参考范围 1.5–3 秒|先检查扫描分辨率。原件边界、机构与年代须在终点可见。|
|两个对象有哪些可以比较的特征|match-cut、07-03 双栏对照|对齐切点两边的主轮廓，干净硬切。组件默认 4 秒，30 fps，切点在 1.40 秒|这三个数值属于组件默认参数。跨年代或身份时同时标识，形状相似本身无法证明因果。|

完整记录含上游参数、自拟起始值、现有资产编号、原创中文制作指令、易误读之处及日后验收条件。[候选方法 JSON](methods.json)

## 从公开案例学到什么

以下时刻来自原视频抽帧。对提示词的说明为中文概述，右栏为应用判断。

|作品与可回查时刻|公开提示词透露了什么|适合财经片的取舍|
|---|---|---|
|Bold kinetic type showreel，3.83 秒浅底单词，18.50 秒粗体和荧光色重音。|作者以作品集为目标，只给约 15 秒的开放指令。媒体实长约 31.89 秒。|保留一处排版重音，让观众一眼找到论点；配音长度以成品为准。[原片](https://motionvideo.xyz/videos/shneural-2abdfa)|
|Japan heatwave pencil data story，21.61 秒温度计，61.22 秒地图，149.44 秒跨年柱形比较。|提示词同时描述比较问题、铅笔画风与合成音乐。|先解释量纲，再交代分布，最后和历史比较。换成财经题材时重新取数。[原片](https://motionvideo.xyz/videos/groundcontrol-61b7d8)|
|Photo print app launch film，16.86 秒网页里有拱门，24.13 秒实体相框里有相似图像。|提示词把输入素材和场景间的继承关系分开写。|可以用同一视觉锚点连接网页证据和实物。这两个采样时刻只证明画面呼应，具体切法仍需逐帧核对。[原片](https://motionvideo.xyz/videos/twoclipping-221cab)|
|PHYLLA language model launch，10.22 秒手与种子，17.43 秒标本四格，24.95 秒花与文字。|提示词分别列出参考片、原图、字体、品牌及声音。|用单个细节引出分类比较；片中品牌和媒体保留在原作者页面。[原片](https://motionvideo.xyz/videos/higgsfield_ai-edddb9)|

## 怎样接入现有技能

**找参考。** 官方公开的 motionvideo Skill 用于查询画廊、取得已公开的案例提示词、改写节奏和限制条件。同一筛选维度中的多个值取并集，不同维度取交集。技能目录记录是发现线索，各条目的技术栈和许可要回到各自仓库核对。[公开检索 Skill](https://github.com/motionvideohq/motionvideo-mcp/blob/137ecf03310e38eb42f4506d79e4f16c82adbebb/skills/motionvideo/SKILL.md)

**写镜头。** 站点仓库引用 Yiwei Ho 的 cinematic-shot，侧重界面宣传片的机位、景深、停顿和动作衔接。财经证据页可借“把第一眼留给即将发生变化的位置”，同时保持文字所在平面清晰。把观察时间码、创作意图推断和本期的验证状态分别记录。其仓库内的免费参考技能与商业 Pro Skill 分别登记。[仓库中的版本](https://github.com/motionvideohq/motionvideo.xyz/blob/a6d32f6273c1687aff87a3344ecf9ad0a5b2b403/.agents/skills/cinematic-shot/SKILL.md) · [原项目](https://github.com/1weiho/cinematic-shot)

**改提示词。** 给出可用原件和数据、观众要回答的问题、必须一直可见的限定条件、允许动画的对象、出现次序和静止阅读的时点。把所有秒数当作排练起点，接到配音后再定切点。五条中文指令由本次研究编写，均可在候选索引找到。[方法与指令](methods.json)

## MCP 检索实测

在 `https://mcp.motionvideo.xyz/mcp` 完成初始化、读取工具清单和匿名调用。线上清单有 8 个工具，其中实际验证了 4 个免费入口。仓库部分文档写作 `list-categories` 和 `browse-directory`，本次服务器公布的是 `list-filters` 和 `search-directory`。每次连接以当时的 `tools/list` 为准。[MCP 项目](https://github.com/motionvideohq/motionvideo-mcp) · [调用记录](mcp-check.json)

|调用|本次得到的结果|
|---|---|
|list-filters，scope=videos|获取画廊的筛选维度。|
|search-videos|“kinetic type”命中 293 条，“camera”73 条，“data visualization”1 条。均为当日查询命中数。|
|get-video|取回 shneural 案例的来源页，并确认作者公开了提示词。|
|search-directory，section=skills，query=hyperframes|返回 40 个匹配项，请求前 3 项。关键词命中不能证明目录内的技能支持某一渲染器。|

公开客户端 [search.py](search.py) 只查询以上 4 个方法，输出作品页和必要元数据。运行环境为 Python 3 与 requests。在参数文件输入 `{"query":"kinetic type","limit":5}` 后运行 `python search.py search-videos --input query.json`。两个个人收藏工具需要账户；Moves 的两个检索工具属于 Pro 范围。[使用条款](https://motionvideo.xyz/terms)

## HyperFrames 兼容性检查

本机 CLI 0.8.184 列出 448 个条目。校验了五个 registry 源文件的 SHA-256 与 CLI 锁记录。chart-story 暴露类型、数据、标签、重点索引及单位；match-cut 暴露颜色与两侧标签。这两项已实际装入静态宿主并传参。CLI lint 对宿主扫描 1 个文件，0 错误、0 警告。timeline 读出 0–4 秒与 4–8 秒两个子合成槽位。这项检查未执行两个组件的浏览器脚本。[检查明细](hyperframes-check.json)

caption-editorial-emphasis 带停驻的 GSAP 时间轴和示例词时序。caption-clip-wipe 按词横向擦入。camera-rig-depth-stack 只有 CSS 和注释中的时间轴示例。后两种字效与空间卡片均需结合具体文字、锚点或时间轴改写。依赖外部 GSAP 或字体的项目，交付时需核对依赖可达性与授权。[源码指纹与依赖](hyperframes-check.json)

MotionVideo 官方预告片由 Remotion/React 实现。公开首镜为 4 秒，初始放大 2.2 倍，推近因子 0.02，俯仰 32°，透视距离 1350。片中焦点插值用 0.6 秒。预设中另一组较快弹簧为阻尼 18、刚度 220、质量 0.7。这些是原实现里的值。移植到档案镜头时，优先保留局部与出处之间的关系，让纸面保持正向可读。[镜头预设](https://github.com/motionvideohq/motionvideo.xyz/blob/a6d32f6273c1687aff87a3344ecf9ad0a5b2b403/apps/videos/src/film/shots.json) · [相机实现](https://github.com/motionvideohq/motionvideo.xyz/blob/a6d32f6273c1687aff87a3344ecf9ad0a5b2b403/apps/videos/src/film/LaunchFilm.tsx#L129-L153) · [缓动与弹簧](https://github.com/motionvideohq/motionvideo.xyz/blob/a6d32f6273c1687aff87a3344ecf9ad0a5b2b403/apps/videos/src/lib/snap-cn-ui/motion.ts)

本包提供一个带上游 MIT 声明的相机参数函数。传入本地镜头时间、原图锚点、起止倍率、角度和位移；返回父层的 perspective 以及原图层的 transformOrigin 和 transform。用 HyperFrames 的 hf-seek 事件传递镜头时间，数据来自同一时刻即可反复定位。已用 Node 检查端点、越界时间、乱序求值、锚点和无效时间；未执行浏览器绘制。[相机函数](camera.mjs) · [MIT 声明](LICENSE-MotionVideo.txt)

静态检查宿主位于 [interface-check/index.html](interface-check/index.html)。复核时，将宿主复制到测试目录，在该目录分别执行 `hyperframes add chart-story --no-clipboard`、`hyperframes add match-cut --no-clipboard`、`hyperframes lint --json` 和 `hyperframes timeline --json`。应对照本包的锁指纹，registry 后续更新可能改变行为。

## 权利和入库口径

官网仓库的 MIT 许可覆盖其发布的站点源码，另有明确排除的品牌及 Pro 内容。本包仅对改编的相机代码附原许可。画廊影片、作品中的音乐、标识和字体需按项取得相应使用权。本包以来源链接和原创观察登记案例；生产媒体索引沿用原有验收门槛。研究期间使用免费接口与本地工具，付费支出为零。[项目许可说明](https://github.com/motionvideohq/motionvideo.xyz#license) · [服务条款](https://motionvideo.xyz/terms) · [来源登记](sources.json)
