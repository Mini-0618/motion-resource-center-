# Motion Resource Center

公开动效资源候选采集项目。当前仅收集公开仓库元数据，不下载或运行第三方源码。采集任务配置为每 15 分钟运行，每次最多收集 24 组候选，实际数量取决于来源与去重结果。

## 查看采集结果

- [最近一次采集](https://github.com/Mini-0618/motion-resource-center-/blob/data/motion-center-v4/motion-data/latest-run.json)记录本次运行的概况。
- [按日浏览候选](https://github.com/Mini-0618/motion-resource-center-/tree/data/motion-center-v4/motion-data/daily)查看历史结果。
- [候选数据示例](sample-resource.json)展示候选条目的字段。

## 使用视频风格工具

[代码动效视频风格工作流](skills/code-video-style-distill/SKILL.md)介绍如何从参考视频提取风格参数、用 Remotion 渲染新选题，并对比渲染结果。

## 维护采集器

- [采集脚本](scripts/discover.py)检索公开动效仓库并写入候选元数据。
- [采集流程](.github/workflows/motion-discovery.yml)定义定时运行和结果更新。采集结果保存在 `data/motion-center-v4` 分支。
- [测试目录](tests)包含候选采集和处理逻辑的测试。
