# 动效素材详细档案规范 v1

本文件用于让 ChatGPT、Grok、Claude 及其他 AI 使用同一份素材说明。**现有 48 条候选资源尚未逐条核验，不能将候选资源视为可运行模板。**

## 每条素材必须记录

- `id`：稳定唯一标识，跨系统复用。
- `title`：名称；`description`：效果与画面表现的具体说明。
- `source_url`：原始来源；`preview_url`：预览地址（没有则留空）。
- `tags`：动效类型、视觉风格、行业主题、镜头用途。
- `engine`：Remotion、Blender、Manim、GSAP、Rive、Three.js 等，**仅据源码证据填写**。
- `inputs`：可改文字、数值、颜色、时长、画幅、字体、数据源。
- `setup`：安装依赖和运行步骤；`render`：渲染命令和产物路径。
- `license`：授权名称与证据链接；`license_checked`：是否人工确认。
- `verification_status`：discovered / previewed / source_checked / reproduced / packaged。
- `limitations`：已知缺陷、性能要求、版权与商用限制。

## AI 调用规则

1. 读取 `schema.json` 与 `index.json`，根据视频脚本的镜头描述检索候选素材。
2. 对候选资源按画面适配、技术栈、可复现状态、授权证据排序。
3. 未核实授权的资源只能作为研究参考，不可自动用于商业成片。
4. 若缺少源码、依赖或渲染指令，返回“待复现”，禁止虚构命令。
5. 仅在独立沙盒中安装、测试第三方代码；成功后记录参数、版本与渲染结果。
6. AI 产出可编辑工程和预览视频，交由用户审核；不得自动发布。

## 单条详文模板

```json
{
  "id": "motion-0001",
  "type": "motion",
  "title": "待从真实候选资源提取",
  "description": null,
  "source_url": null,
  "preview_url": null,
  "tags": [],
  "use_cases": [],
  "engine": null,
  "inputs": [],
  "setup": null,
  "render": null,
  "license": null,
  "license_checked": false,
  "verification_status": "discovered",
  "limitations": ["尚未核验源码、预览和授权"]
}
```

> 模板不是已导入的真实素材。后续必须从原始候选记录提取，不得凭空生成 48 条说明。
