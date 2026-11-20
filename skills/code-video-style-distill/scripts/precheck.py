#!/usr/bin/env python3
"""precheck.py — OPTIONAL step 0: is the reference video code/template-generated?

Idea borrowed (no code, no dependency) from JuneYaooo/rea-video (Apache-2.0), which classifies
shots as live / AI / 3D / code-or-template before deciding how to replicate them. Here we use
cheap pixel statistics only:
  flat_ratio      share of pixels in perfectly flat 5x5 neighbourhoods (vector/CSS fills ≫ camera)
  color_compact   share of pixels covered by the 12 most common quantised colours
  noise_sigma     robust noise estimate in flat-ish areas (sensor grain / AI texture ≫ code)
  static_hold     share of frame pairs with ~zero change (code videos hold exactly still)
Verdict per sample and overall: code_template | mixed_or_screen_recording | live_ai_3d.
All verdicts are INFERRED heuristics — always confirm by looking at the contact sheet.

Usage: precheck.py <video> -o <dir> [--samples 16]
"""
import argparse
import json
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cvsd_common import ffprobe, tc, write_json  # noqa: E402

CEILING = {
    "code_template": "可高保真复刻：版式、配色、动效曲线和节奏都能用 tokens + 模板重建（仍非像素级：字体替代、抗锯齿、编码差异）。",
    "mixed_or_screen_recording": "部分可复刻：代码动效部分可重建；录屏/截图/实拍画面必须自备有权使用的素材，模板只复刻包装层（字幕、标注、转场、节奏）。",
    "live_ai_3d": "复刻上限低：画面主体是实拍/AI 生成/3D 渲染，本 Skill 只能蒸馏包装层（字幕条、标题卡、配色、剪辑节奏），主体画面需要其它工具或自有素材。",
}


def frame_stats(img):
    g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32)
    mean = cv2.blur(g, (5, 5))
    sq = cv2.blur(g * g, (5, 5))
    std = np.sqrt(np.maximum(sq - mean * mean, 0))
    flat_ratio = float((std < 0.8).mean())
    q = (img // 16).astype(np.int32)
    keys = q[..., 0] * 256 + q[..., 1] * 16 + q[..., 2]
    _, cnt = np.unique(keys, return_counts=True)
    compact = float(np.sort(cnt)[::-1][:12].sum() / keys.size)
    lap = cv2.Laplacian(g, cv2.CV_32F)
    smooth = std < 6
    noise = float(np.median(np.abs(lap[smooth])) * 1.4826) if smooth.any() else 99.0
    return flat_ratio, compact, noise


def score(flat, compact, noise):
    s = 0.0
    s += np.clip((flat - 0.25) / 0.45, 0, 1) * 0.4
    s += np.clip((compact - 0.45) / 0.45, 0, 1) * 0.35
    s += np.clip((3.0 - noise) / 2.5, 0, 1) * 0.25
    return float(s)


def verdict(s):
    return "code_template" if s >= 0.62 else "mixed_or_screen_recording" if s >= 0.38 else "live_ai_3d"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--samples", type=int, default=16)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    meta = ffprobe(a.video)
    dur = meta["duration_s"]
    W = min(960, meta["width"])
    H = int(round(meta["height"] * W / meta["width"] / 2) * 2)
    rows = []
    for i in range(a.samples):
        t = dur * (i + 0.5) / a.samples
        p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", a.video, "-frames:v", "1", "-vf", f"scale={W}:{H}",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
        if len(p.stdout) < W * H * 3:
            continue
        img = np.frombuffer(p.stdout[: W * H * 3], np.uint8).reshape(H, W, 3)
        f, c, n = frame_stats(img)
        s = score(f, c, n)
        rows.append({"t": round(t, 3), "tc": tc(t), "flat_ratio": round(f, 3), "color_compact": round(c, 3), "noise_sigma": round(n, 2),
                     "score": round(s, 3), "verdict": verdict(s)})
    # static holds at 10 fps, 320px
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", a.video, "-vf", "fps=10,scale=320:-2", "-f", "rawvideo", "-pix_fmt", "gray", "-"], capture_output=True)
    h2 = int(round(meta["height"] * 320 / meta["width"] / 2) * 2)
    buf = np.frombuffer(p.stdout, np.uint8)
    n = len(buf) // (320 * h2)
    fr = buf[: n * 320 * h2].reshape(n, h2, 320).astype(np.int16)
    static = float((np.abs(np.diff(fr, axis=0)).mean((1, 2)) < 0.15).mean()) if n > 2 else 0.0
    mean_s = float(np.mean([r["score"] for r in rows])) if rows else 0.0
    overall = mean_s * 0.85 + np.clip(static / 0.5, 0, 1) * 0.15
    v = verdict(overall)
    share = {k: round(sum(r["verdict"] == k for r in rows) / max(1, len(rows)), 3) for k in CEILING}
    res = {"video": meta["path"], "overall_score": round(float(overall), 3), "verdict": v, "static_hold_ratio": round(static, 3),
           "sample_verdict_share": share, "replication_ceiling": CEILING[v], "samples": rows,
           "status": "inferred", "method": "pixel statistics heuristic; idea from JuneYaooo/rea-video (Apache-2.0), no code reused"}
    write_json(os.path.join(a.out, "precheck.json"), res)
    with open(os.path.join(a.out, "precheck.md"), "w", encoding="utf-8") as f:
        f.write(f"# 参考视频前置判断（推测）\n\n- 视频：`{meta['path']}`\n- 结论：**{v}**（得分 {overall:.2f}；≥0.62 代码/模板，0.38–0.62 混合/录屏，<0.38 实拍/AI/3D）\n"
                f"- 静止保持帧占比：{static:.2f}\n- 抽样分布：{share}\n- 复刻上限：{CEILING[v]}\n\n"
                "| 时间码 | flat | compact | noise | score | 判定 |\n|---|---|---|---|---|---|\n")
        for r in rows:
            f.write(f"| {r['tc']} | {r['flat_ratio']} | {r['color_compact']} | {r['noise_sigma']} | {r['score']} | {r['verdict']} |\n")
        f.write("\n思路借鉴 JuneYaooo/rea-video（Apache-2.0）的“先判镜头类型再决定复刻路线”；未引入其代码或依赖。判定为启发式推测，需目测确认。\n")
    print(f"[precheck] verdict={v} score={overall:.2f} static={static:.2f} share={share}")
    print(f"[precheck] {CEILING[v]}")


if __name__ == "__main__":
    main()
