#!/usr/bin/env python3
"""checklist.py — write the PRE-DECLARED acceptance checklist BEFORE the first render.

Usage: checklist.py --tokens style-tokens.json --ref-analysis <dir> [--script script.json] [--same-content] -o acceptance.json

Tiers: must / should / out (out = explicitly out of scope, never scored).
Each item: id, tier, what, metric, op, threshold, method, evidence_in (reference side).
Thresholds are fixed here and must not be loosened after seeing results (edit the file
by hand + record why in the ledger if you really must).

Adapted from Speedrunlab/reverse-engineer-anything-self-learning-loop templates/parity-checklist.md
(MIT, Copyright 2026 Speedrun AI Labs Pty Ltd): tiered items with inputs, expectation, verification
method and evidence path. Rewritten for video style metrics.
"""
import argparse
import datetime as dt
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cvsd_common import read_json, write_json  # noqa: E402

SEG2COMP = {"title": "title_card", "bullets": "bullet_list", "bars": "bar_chart", "stat": "number_counter", "code": "code_block"}


def build(tokens, A, script=None, same_content=False):
    ra = A["files"]
    items = []

    def add(i, tier, what, metric, op, thr, method, ev):
        items.append({"id": i, "tier": tier, "what": what, "metric": metric, "op": op, "threshold": thr, "method": method, "evidence_in": ev})
    add("M1", "must", "画布尺寸与帧率一致", "canvas_equal", "==", True, "ffprobe width/height/fps", os.path.join(os.path.dirname(ra["scenes_csv"]), "meta.json"))
    add("M2", "must", "背景色一致", "bg_delta_e", "<=", 3.0, "CIEDE2000(ref bg, replica bg)；bg=边框像素众数", ra["contact_sheet"])
    add("M3", "must", "整体色板接近", "palette_weighted_delta_e", "<=", 6.0,
        "参考色板每个色块(占比≥0.5%)到复刻色板最近色的 ΔE2000，按占比加权平均", ra["palette_png"])
    add("M4", "must", "主色/强调色出现在复刻片", "role_colors_max_delta_e", "<=", 8.0,
        "tokens.palette.primary/accent 到复刻前景色板最近色的最大 ΔE2000", ra["palette_png"])
    add("M5", "must", "入场速度曲线形状一致（缓动）", "entrance_profile_corr", ">=", 0.80,
        "非转场运动事件的光流速度曲线重采样到 20 点、归一化后取平均，Pearson r", ra["motion_energy_csv"])
    add("M6", "must", "入场动画时长接近", "entrance_duration_ratio_err", "<=", 0.25, "|median(rep)/median(ref) - 1|", ra["motion_energy_csv"])
    add("M7", "must", "左边距与对齐方式一致", "margin_left_diff_pct", "<=", 2.0, "左边距百分点差；对齐方式必须相同", ra["contact_sheet"])
    req = set()
    if script:
        for s in script.get("segments", []):
            if s.get("type") in SEG2COMP:
                req.add(SEG2COMP[s["type"]])
        if any(s.get("caption") for s in script.get("segments", [])):
            req.add("subtitle_bar")
    if any(c["type"] == "progress_bar" for c in tokens.get("components", [])):
        req.add("progress_bar")
    add("M8", "must", "脚本用到的元件都被检测到", "components_missing", "==", 0,
        f"对复刻片跑 analyze+distill 的元件检测，缺失数=0；要求 {sorted(req)}", ra["contact_sheet"])
    items[-1]["required_components"] = sorted(req)
    add("S1", "should", "正文字号接近", "body_size_ratio_err", "<=", 0.15, "OCR 墨迹高度估计的正文字号比", ra["contact_sheet"])
    add("S2", "should", "标题字号接近", "h1_size_ratio_err", "<=", 0.20, "OCR 标题层字号比", ra["contact_sheet"])
    add("S3", "should", "转场类型一致且时长接近", "transition_match", "==", True, "光流方向判类型 + 核心时长误差≤30%", ra["motion_energy_png"])
    add("S4", "should", "镜头节奏接近", "shot_mean_ratio_err", "<=", 0.35, "平均镜头时长比（受脚本时长影响）", ra["scenes_csv"])
    add("S5", "should", "错峰间隔接近", "stagger_ratio_err", "<=", 0.35, "镜头内入场间隔中位数比", ra["motion_energy_csv"])
    add("S6", "should", "装饰元素一致（背景网格）", "decor_match", "==", True, "背景网格线检测结果相同", ra["contact_sheet"])
    add("S7", "should", "音画卡点比例接近（双方都有音轨时）", "av_sync_ratio_diff", "<=", 0.20, "视觉事件落在 80ms 内音频起音点的比例差", ra["motion_energy_csv"])
    add("S8" if same_content else "O1", "should" if same_content else "out", "整条运动能量曲线相关（仅同内容复刻有意义）",
        "timeline_energy_corr", ">=", 0.60, "两条运动能量曲线按归一化时间重采样 200 点后 Pearson r", ra["motion_energy_csv"])
    add("S9" if same_content else "O2", "should" if same_content else "out", "同时间点画面结构相似（仅同内容）", "mean_ssim", ">=", 0.85,
        "并排帧灰度 SSIM 平均", ra["contact_sheet"])
    add("O3", "out", "使用原片字体文件", None, None, None, "政策排除：只用免费可商用替代字体", None)
    add("O4", "out", "原片素材 / logo / 角色 / 商标", None, None, None, "政策排除：不搬运受保护资产", None)
    add("O5", "out", "像素级完全一致", None, None, None, "不承诺；尺寸/字体/编码不同则视觉主张记为 not-testable", None)
    return {"created_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "style": tokens.get("name"),
            "tokens": None, "reference_analysis": os.path.dirname(ra["scenes_csv"]), "same_content": same_content,
            "done_rule": "所有 must 项在连续两轮 compare 中都为 pass 才算完成；not-testable 不算 pass；两轮总分不动就停下来问人",
            "attribution": "Tier/gap/ledger 结构改编自 Speedrunlab/reverse-engineer-anything-self-learning-loop (MIT)；"
                           "'不可比较即 unknown/not-testable' 规则参考 morluto/rea 视觉主张合同 (MIT)。",
            "items": items}


def to_md(C):
    L = [f"# 验收清单（预先声明）— {C['style']}", "", f"- 创建：{C['created_at']}（在第一次渲染之前）", f"- 完成规则：{C['done_rule']}",
         f"- 出处：{C['attribution']}", "", "| ID | 档位 | 项目 | 指标 | 阈值 | 方法 |", "|---|---|---|---|---|---|"]
    for it in C["items"]:
        thr = "—" if it["op"] is None else f"{it['op']} {it['threshold']}"
        L.append(f"| {it['id']} | {it['tier']} | {it['what']} | {it['metric'] or '—'} | {thr} | {it['method']} |")
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--ref-analysis", required=True)
    ap.add_argument("--script")
    ap.add_argument("--same-content", action="store_true", help="replica re-renders the SAME content as the reference")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    T = read_json(a.tokens)
    A = read_json(os.path.join(a.ref_analysis, "analysis.json"))
    C = build(T, A, read_json(a.script) if a.script else None, a.same_content)
    C["tokens"] = os.path.abspath(a.tokens)
    if os.path.exists(a.out):
        print(f"[checklist] {a.out} already exists — NOT overwriting (thresholds are pre-declared). Delete it deliberately to regenerate.")
        return
    write_json(a.out, C)
    md = os.path.splitext(a.out)[0] + ".md"
    with open(md, "w", encoding="utf-8") as f:
        f.write(to_md(C))
    print(f"[checklist] wrote {a.out} and {md}: {sum(i['tier']=='must' for i in C['items'])} must / "
          f"{sum(i['tier']=='should' for i in C['items'])} should / {sum(i['tier']=='out' for i in C['items'])} out")


if __name__ == "__main__":
    main()
