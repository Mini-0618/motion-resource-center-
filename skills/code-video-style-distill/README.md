# code-video-style-distill

参考视频 → 蒸馏风格底座（`style-tokens.json`）→ 换选题用 Remotion 模板量产 → 与原片对比迭代。

用于底层由代码生成的动效视频（Remotion/React、GSAP/HTML、Manim、Motion Canvas，以及 AE 表达式风格的 MG/知识类视频）。目标是高保真复刻风格，不承诺像素级一致。完整流程见 [SKILL.md](./SKILL.md)。

## 安装

需要：Python 3、Node.js、ffmpeg / ffprobe、Chrome（渲染用）。可选：`tesseract-ocr` 和 `tesseract-ocr-chi-sim`；没有也能跑，OCR 相关字段会标为 `unknown`。

```bash
cd skills/code-video-style-distill   # 若已在本目录可省略
export T="$(pwd)"

python3 -m venv .venv && .venv/bin/pip install opencv-python-headless numpy scikit-learn pillow matplotlib jsonschema scipy pyyaml

cd template && npm install && cd ..
```

## 一条命令跑完整链路

```bash
export T="$(pwd)"
RIGHTS_OK=1 "$T/run.sh" all <ref.mp4> <work> <style-name> <script.json>
```

本仓库不附带测试片的视频和音频；`examples/` 里保留了脚本和风格 JSON，可换上你自己的参考视频后运行。`run.sh` 会按脚本所在目录自动定位工具根目录（即 `$T`）。

## 版权与范围门

1. 只处理你有权参考的视频（自己的作品、已获授权，或仅作内部风格学习的公开视频）。
2. 只学风格和结构，不搬运原片素材、截图、logo、商标、角色、配音、配乐、字体文件和原文案。
3. 字体身份记为 `unknown`，只用免费可商用替代（见 `references/font-alternatives.md`）。
4. 不承诺像素级一致。
5. 运行 `analyze` / `all` 前必须设置 `RIGHTS_OK=1`，表示已确认第 1 条。

## 第三方出处

见 [THIRD_PARTY_NOTICES.md](./THIRD_PARTY_NOTICES.md)。本工具与官方 REA 等项目无隶属关系。
