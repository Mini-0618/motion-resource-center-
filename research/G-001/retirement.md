# G-001 任务1：旧创作体系退出（本地标记）

- 任务依据：用户指令 t37u / 指挥任务 G-001 任务1。
- 标记日期：2026-11-24（America/New_York）。
- 范围：只做本地文件层面的状态标记。
- 未删除、未移动任何原始档案。
- 未推送 GitHub，未提交 git。
- 未修改 skill 库（`/home/box/agent-data/workflows/`、`/home/box/sand-data/workflows/` 均未改动）。

## 一、退出默认的资产

| 路径 | 原状态 | 新状态 | 本地条目（能从现有 index/json 读出的） |
|---|---|---|---|
| `/workspace/ip-team/tools/code-video-style-distill/` | 代码动效风格蒸馏与量产工具，此前作为默认创作/复刻流程入口 | **专项技术工具**（2026-11-24 起退出默认创作流程）。仅在明确需要复刻代码动效风格时调用；不作为加伊莎默认创作依据。已在 `SKILL.md`、`AGENTS.md` 顶部加标记。其余内容未改。 | 工具本身，不是动效候选清单。同目录 `styles/asset-index.json` 是风格底座导出（当前 2 条 style assets），不属于 595 条候选库，未按候选资产降级。 |
| `/workspace/ip-team/deliverables/motion/` | 动效与制作资源候选清单及仓库预分组目录；清单字段「状态」为「已核实来源」（只表示来源元数据已核对），「测试结果」全部为「未验证」 | **候选资产（未验证）**。2026-11-24 起降级，不作为成熟技能使用；保留原始档案。验证通过后才可进入正式生产技能库。已在该顶层目录放 `ARCHIVE-STATUS.md`。 | v2：595 条、449 个独立仓库、71 类；测试结果 595/595「未验证」。v1（历史版）：277 条、234 个独立仓库；测试结果 277/277「未验证」。`repo-staging/` 71 个分类文件夹均为 README-only。`repo-staging/asset-index/` 与顶层 v1/v2 文件内容相同，不重复计数。 |
| `/tmp/motion-resource-center-upload/` | GitHub 仓库 `Mini-0618/motion-resource-center-` 的本地工作副本，当前检出 **main**（本地 `HEAD` / 已跟踪的 `origin/main` 均为 `d7ac5b5`） | 本次**未在该工作副本写入** `ARCHIVE-STATUS.md`，也未切换或检出其他分支，以免弄脏待推送的 git 工作区。 | 工作区只有 `motion_center/`（发现/导入用的 Python 包代码，不是 216 条数据档案）和 `skills/code-video-style-distill/`（工具副本）。`motion-candidates-v1`、`data/motion-center-v4` 对应目录在本地未检出，故无处可放标记。 |

检索范围仅限 `/workspace/ip-team` 与 `/tmp/motion-resource-center-upload`（已排除 `node_modules`、`.git`、`.venv`、`research/rea`）。未发现除此之外的本地 `motion-candidates` / `motion-center-v4` 数据目录。

## 二、保留的标准

以下标准继续有效，作为研究与验收依据，不随本次退出而作废：

- **REA V1.1**
- **三层时间轴**
- **证据标准**（seen / inferred / unknown；作者自述与推断分开；不能获取原片时必须标明，不得冒充完整观看或逐帧分析）

上述标准由 skill **`video-distill-master`**（AI 视频蒸馏与制作知识库 · 总控指令 V1.1）承载。本地 skill 目录存在于 `/home/box/agent-data/workflows/video-distill-master` 与 `/home/box/sand-data/workflows/video-distill-master`。按任务要求，本次**没有修改**这些 skill 文件。

本地预处理、切镜/音频统计、对比验证等可在本机用 FFmpeg/Python 完成的能力仍可使用；`code-video-style-distill` 仅作为专项技术工具，不再作为默认创作依据。

## 三、未删除声明

- 所有原始档案均保留在原路径。
- 未删除、未移动、未重命名候选 json/csv、分类文件夹、taxonomy、ai-index-design 或工具源码。
- 未把任何未验证方法写入正式生产技能库。

## 四、GitHub 仓库尚未加标记（需用户批准后才推送）

仓库：https://github.com/Mini-0618/motion-resource-center-

本次只用 `git ls-remote --heads` 核对远端分支仍然存在，**没有 fetch、没有 checkout、没有 commit、没有 push**。因此 GitHub 上的对应分支都还没有本次的退出/降级标记。

| 远端分支 | ls-remote 提示提交 | 对应内容 | 标记情况 |
|---|---|---|---|
| `main` | `c29bfcd0be9521159648abc313b8c597bbeb6aa8` | 其上有 `skills/code-video-style-distill`。注意：本地工作副本跟踪的 `origin/main` 仍为 `d7ac5b5`（2026-11-20），与当前远端 `main` 提示提交不一致；本次未拉取，也未把本地 `SKILL.md` / `AGENTS.md` 的标记同步到该工作副本或远端。 | **尚未加标记** |
| `motion-candidates-v1` | `df1cd2e375551df6f290490e93bedd8f835fbfd5` | 595 条动效候选（与本地 `candidates-v2.json` 一致：595 条、449 仓库、71 类，测试结果未验证；分类文件夹为 README-only） | **尚未加标记** |
| `data/motion-center-v4` | `40442ed3f2f38c7ee4d60133c985410f4540a9b0` | 此前盘点为 216 条 DISCOVERED 记录。该分支未在本地检出；本轮 GitHub API 因未认证限额返回 403，**未能在本轮重新点数**，216 条沿用既有盘点，不算本次复测。 | **尚未加标记** |

另外，远端目前还有 `feature/unified-asset-index-20261119`（`93d2a15c`）和 `codex/organize-repository-readme`（`66acacca`）。前者此前盘点为尚未填入的空索引，本次同样未加标记、未推送。

如需把本次说明推到 GitHub，须先获得用户明确批准，再决定是改 `main` 上的 skill 说明、在候选分支补 `ARCHIVE-STATUS.md`，还是只在某一分支提交。
