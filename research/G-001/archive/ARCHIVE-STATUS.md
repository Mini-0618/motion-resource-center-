# ARCHIVE-STATUS

**状态：候选资产（未验证）。2026-11-24 起降级，不作为成熟技能使用；保留原始档案。验证通过后才可进入正式生产技能库。**

本目录是本地动效候选资源的顶层档案。本次只做状态标记，未移动、未删除任何文件。

## 条目统计（从本目录现有 index 读取，2026-11-24）

| 文件 | 条目数 | 独立仓库 | 测试结果 | 状态字段（仅表示来源已核对，不是制作验证） |
|---|---:|---:|---|---|
| `candidates-v2.json` / `candidates-v2.csv` | 595 | 449 | 全部「未验证」 | 全部「已核实来源」 |
| `candidates-v1.json` / `candidates-v1.csv` | 277 | 234 | 全部「未验证」 | 全部「已核实来源」 |

补充：

- `candidates-v2.json` 的 `meta.总条数` 为 595；`meta.分类体系` 为 UI-01~UI-23、V-01~V-32、W-01~W-10、A-01~A-06，共 71 类。安装命令 44 条已对照 README 摘录但未运行，其余 551 条安装命令未验证。
- `repo-staging/asset-index/` 中的 v1/v2 json 与 csv 与上表文件内容相同（sha256 一致），不另计一套。
- `repo-staging/` 含 71 个分类文件夹（ui-motion 23 + video-motion 32 + workflows 10 + assets 6），每个文件夹目前只有 README.md，没有已验证的可运行技能。
- `ai-index-design/` 为索引设计草稿与示例，不是已验证技能。
- `taxonomy-from-user.md` 为分类表，随本档案一并保留。

v2 覆盖 v1 的清单范围，日常以 v2（595 条）为准；v1 作为历史版本保留。
