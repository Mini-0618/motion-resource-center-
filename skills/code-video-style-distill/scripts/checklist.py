#!/usr/bin/env python3
"""checklist.py — write the PRE-DECLARED acceptance checklist BEFORE the first render.

Usage: checklist.py --tokens style-tokens.json --ref-analysis <dir> [--script script.json] [--same-content] -o acceptance.json

Tiers: must / should / out (out = explicitly out of scope, never scored).

Source-level rule (provenance gate):
  every item records `source_paths` (the style-token fields it depends on) and `source_level`
  = the weakest provenance status among them (unknown < inferred < seen).
  * declared must + seen      -> stays must
  * declared must + inferred  -> downgraded to should ("该值本身是推测")
  * any tier     + unknown    -> should, and compare.py reports it as not-testable
  A must gate is therefore only ever a MEASURED value — iteration never chases a guess.

Baselines (frozen): reference-side target values (primary/accent, component colours/geometry) are
measured from the REFERENCE ANALYSIS (distill run without overrides) and written into this file
once. compare.py reads them from here, never from the (possibly edited) style-tokens.json.

Thresholds are fixed here and must not be loosened after seeing results.
Adapted from Speedrunlab/reverse-engineer-anything-self-learning-loop templates/parity-checklist.md
(MIT, Copyright 2026 Speedrun AI Labs Pty Ltd). Rewritten for video style metrics.
"""
import argparse
import datetime as dt
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cvsd_common import read_json, write_json  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
SEG2COMP = {"title": "title_card", "bullets": "bullet_list", "bars": "bar_chart", "stat": "number_counter", "code": "code_block",
            "evidence": "evidence_frame", "timeline": "timeline", "compare": "compare_columns", "flow": "flow_chart"}
COMP2STYLE = {"evidence_frame": "evidence", "timeline": "timeline", "compare_columns": "compare", "flow_chart": "flow"}
RANK = {"unknown": 0, "inferred": 1, "seen": 2}


def source_level(prov, paths, best=False):
    """weakest (or best, for component detections) provenance status covering the given paths."""
    levels = []
    for p in paths:
        st = []
        for k, v in prov.items():
            if k == p or k.startswith(p + ".") or p.startswith(k + ".") or (p.startswith("components:") and k.split(":", 1)[-1] == p.split(":", 1)[1] and k.startswith("components[")):
                st.append(v.get("status", "unknown"))
        if not st:
            levels.append("unknown")
        else:
            levels.append((max if best else min)(st, key=lambda s: RANK.get(s, 0)))
    if not levels:
        return "unknown"
    return (max if best else min)(levels, key=lambda s: RANK.get(s, 0))


def ref_measured_tokens(ref_dir):
    """distill the reference analysis WITHOUT overrides (cached in <ref_dir>/_distill)."""
    p = os.path.join(ref_dir, "_distill", "style-tokens.json")
    if not os.path.exists(p):
        subprocess.run([sys.executable, os.path.join(HERE, "distill.py"), ref_dir, "-o", os.path.join(ref_dir, "_distill"), "--name", "ref-measured"],
                       check=True, stdout=subprocess.DEVNULL)
    return read_json(p)


def build(tokens, A, script=None, same_content=False, ref_tokens=None):
    ra = A["files"]
    prov = tokens.get("provenance", {})
    RT = ref_tokens or tokens
    items = []

    def add(i, tier, what, metric, op, thr, method, ev, paths, best=False, **extra):
        lvl = source_level(prov, paths, best) if paths else "seen"
        it = {"id": i, "declared_tier": tier, "tier": tier, "what": what, "metric": metric, "op": op, "threshold": thr, "method": method,
              "evidence_in": ev, "source_paths": paths, "source_level": lvl, **extra}
        if tier == "must" and lvl == "inferred":
            it["tier"], it["downgraded_reason"] = "should", "来源字段是推测值（inferred）：降为 should，先目测确认再调参"
        if tier in ("must", "should") and lvl == "unknown":
            it["tier"], it["force_not_testable"] = "should", True
            it["downgraded_reason"] = "来源字段未测到（unknown）：降为 should，记 not-testable"
        items.append(it)

    meta = os.path.join(os.path.dirname(ra["scenes_csv"]), "meta.json")
    add("M1", "must", "画布尺寸与帧率一致", "canvas_equal", "==", True, "ffprobe width/height/fps", meta, ["canvas.width", "canvas.height", "canvas.fps"])
    add("M2", "must", "背景色一致", "bg_delta_e", "<=", 3.0, "CIEDE2000(ref bg, replica bg)；bg=边框像素众数", ra["contact_sheet"], ["palette.bg"])
    add("M3", "must", "整体色板接近", "palette_weighted_delta_e", "<=", 6.0,
        "参考色板每个色块(占比≥0.5%)到复刻色板最近色的 ΔE2000，按占比加权平均", ra["palette_png"], ["palette.measured_swatches"])
    add("M4", "must", "主色/强调色出现在复刻片", "role_colors_max_delta_e", "<=", 8.0,
        "基准=参考片分析测得的 primary/accent（建清单时冻结）到复刻前景色板最近色的最大 ΔE2000", ra["palette_png"], ["palette.primary", "palette.accent"],
        baseline={"primary": RT["palette"].get("primary"), "accent": RT["palette"].get("accent")})
    add("M5", "must", "入场速度曲线形状一致（缓动）", "entrance_profile_corr", ">=", 0.80,
        "非转场运动事件的光流速度曲线重采样到 20 点、归一化后取平均，Pearson r", ra["motion_energy_csv"], ["motion.easing.enter"])
    add("M6", "must", "入场动画时长接近", "entrance_duration_ratio_err", "<=", 0.25, "|median(rep)/median(ref) - 1|", ra["motion_energy_csv"], ["motion.durations_s"])
    add("M7", "must", "左边距一致", "margin_left_diff_pct", "<=", 2.0, "左边距百分点差", ra["contact_sheet"], ["layout.margins_pct.left"])
    add("M8", "must", "对齐方式一致", "alignment_match", "==", True, "dominant_alignment 相同", ra["contact_sheet"], ["layout.alignment"])
    add("M9", "must", "安全区接近", "safe_area_diff_pct", "<=", 3.0, "四边安全区百分点差的最大值", ra["contact_sheet"], ["layout.safe_area_pct"])
    add("M10", "must", "面板圆角接近", "radius_diff_px", "<=", 6.0, "面板圆角像素差（按画布高度归一）", ra["contact_sheet"], ["layout.radius_px"],
        baseline={"radius_px": RT["layout"].get("radius_px")})

    # components required by the script: one detection item each (+ geometry/colour items for knowledge components)
    req = []
    if script:
        for s in script.get("segments", []):
            c = SEG2COMP.get(s.get("type"))
            if c and c not in req:
                req.append(c)
        if any(s.get("caption") for s in script.get("segments", [])):
            req.append("subtitle_bar")
    if any(c["type"] == "progress_bar" for c in tokens.get("components", [])):
        req.append("progress_bar")
    n = 0
    for c in req:
        n += 1
        add(f"C{n}", "must", f"元件 {c} 在复刻片中被检测到", "component_detected", "==", True,
            f"对复刻片跑 analyze+distill 的元件检测，要求出现 {c}", ra["contact_sheet"], [f"components:{c}"], best=True, component=c)
        key = COMP2STYLE.get(c)
        if not key:
            continue
        cs = (RT.get("components_style") or {}).get(key, {})
        pth = [f"components_style.{key}"]
        if key == "evidence":
            add(f"C{n}a", "must", "证据框高亮色一致", "evidence_highlight_delta_e", "<=", 8.0, "复刻测得 highlight_color 与基准 ΔE2000", ra["contact_sheet"], pth,
                component=c, baseline={"highlight_color": cs.get("highlight_color")})
            add(f"C{n}b", "must", "证据框尺寸接近", "evidence_box_w_diff_pct", "<=", 6.0, "截图框宽度占画面百分比之差", ra["contact_sheet"], pth,
                component=c, baseline={"box_w_pct": (cs.get("measured", {}).get("box_pct") or [None] * 4)[2]})
        elif key == "timeline":
            add(f"C{n}a", "must", "时间线节点色一致", "timeline_node_delta_e", "<=", 8.0, "复刻测得 node_color 与基准 ΔE2000", ra["contact_sheet"], pth,
                component=c, baseline={"node_color": cs.get("node_color")})
            add(f"C{n}b", "must", "时间线节点尺寸接近", "timeline_node_size_ratio_err", "<=", 0.30, "|node_size(rep)/node_size(ref) - 1|（按画布高度归一）",
                ra["contact_sheet"], pth, component=c, baseline={"node_size_px": cs.get("node_size_px")})
        elif key == "compare":
            add(f"C{n}a", "must", "对比双栏面板色一致", "compare_panel_delta_e", "<=", 6.0, "复刻测得 panel_fill 与基准 ΔE2000", ra["contact_sheet"], pth,
                component=c, baseline={"panel_fill": cs.get("panel_fill")})
            add(f"C{n}b", "must", "对比双栏间距接近", "compare_gap_diff_pct", "<=", 2.0, "两栏间距占画面宽度百分点差", ra["contact_sheet"], pth,
                component=c, baseline={"gap_pct": cs.get("gap_pct")})
        elif key == "flow":
            add(f"C{n}a", "must", "流程图节点描边色一致", "flow_stroke_delta_e", "<=", 8.0, "复刻测得 node_stroke 与基准 ΔE2000", ra["contact_sheet"], pth,
                component=c, baseline={"node_stroke": cs.get("node_stroke")})
            add(f"C{n}b", "must", "流程图节点≥3 且方向一致", "flow_geometry_ok", "==", True, "node_count≥3 且 orientation 与基准相同", ra["contact_sheet"], pth,
                component=c, baseline={"orientation": cs.get("orientation")})

    add("S1", "should", "正文字号接近", "body_size_ratio_err", "<=", 0.15, "OCR 墨迹高度估计的正文字号比（任一侧无 OCR 或默认值 → not-testable）",
        ra["contact_sheet"], ["typography.scale_px.body"])
    add("S2", "should", "标题字号接近", "h1_size_ratio_err", "<=", 0.20, "OCR 标题层字号比（任一侧无 OCR 或默认值 → not-testable）", ra["contact_sheet"],
        ["typography.scale_px.h1"])
    add("S3", "should", "转场类型一致且时长接近", "transition_match", "==", True, "光流方向判类型 + 核心时长误差≤30%", ra["motion_energy_png"],
        ["motion.transition.type", "motion.transition.duration_s"])
    add("S4", "should", "镜头节奏接近", "shot_mean_ratio_err", "<=", 0.35, "平均镜头时长比（受脚本时长影响）", ra["scenes_csv"], ["rhythm.shot_mean_s"])
    add("S5", "should", "错峰间隔接近", "stagger_ratio_err", "<=", 0.35, "镜头内入场间隔中位数比", ra["motion_energy_csv"], ["motion.stagger_s"])
    add("S6", "should", "装饰元素一致（背景网格）", "decor_match", "==", True, "背景网格线检测结果相同", ra["contact_sheet"], ["layout.decor.grid_lines"])
    add("S7", "should", "音画卡点比例接近（双方都有音轨时）", "av_sync_ratio_diff", "<=", 0.20, "视觉事件落在 80ms 内音频起音点的比例差", ra["motion_energy_csv"],
        ["rhythm.av_sync"])
    add("S8" if same_content else "O1", "should" if same_content else "out", "整条运动能量曲线相关（仅同内容复刻有意义）",
        "timeline_energy_corr", ">=", 0.60, "两条运动能量曲线按归一化时间重采样 200 点后 Pearson r", ra["motion_energy_csv"], [])
    add("S9" if same_content else "O2", "should" if same_content else "out", "同时间点画面结构相似（仅同内容）", "mean_ssim", ">=", 0.85,
        "并排帧灰度 SSIM 平均", ra["contact_sheet"], [])
    add("O3", "out", "使用原片字体文件", None, None, None, "政策排除：只用免费可商用替代字体", None, [])
    add("O4", "out", "原片素材 / logo / 角色 / 商标", None, None, None, "政策排除：不搬运受保护资产", None, [])
    add("O5", "out", "像素级完全一致", None, None, None, "不承诺；尺寸/字体/编码不同则视觉主张记为 not-testable", None, [])
    return {"created_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "style": tokens.get("name"),
            "tokens": None, "reference_analysis": os.path.dirname(ra["scenes_csv"]), "same_content": same_content, "checklist_version": 2,
            "source_level_rule": "must 只对 seen 字段生效；inferred → should；unknown → should + not-testable。",
            "baseline_rule": "主色/强调色/元件基准来自参考片分析（不带 overrides 的 distill），建清单时冻结在各项 baseline 字段，之后不随 style-tokens 改动。",
            "done_rule": "降级后剩下的所有 must 项，在连续两轮、两个不同成片文件（sha256 不同）的 compare 中都为 pass 才算完成；not-testable 不算 pass；"
                         "同一文件重复比较不计新一轮；两轮总分不动就停下来问人",
            "attribution": "Tier/gap/ledger 结构改编自 Speedrunlab/reverse-engineer-anything-self-learning-loop (MIT)；"
                           "'不可比较即 unknown/not-testable' 规则参考 morluto/rea 视觉主张合同 (MIT)；seen/inferred/unknown 分级参考 aicodeking/leanrea (MIT)。",
            "items": items}


def to_md(C):
    L = [f"# 验收清单（预先声明）— {C['style']}", "", f"- 创建：{C['created_at']}（在第一次渲染之前）", f"- 出处分级：{C['source_level_rule']}",
         f"- 基准冻结：{C['baseline_rule']}", f"- 完成规则：{C['done_rule']}", f"- 出处：{C['attribution']}", "",
         "| ID | 档位 | 原定档位 | 出处等级 | 来源字段 | 项目 | 指标 | 阈值 | 方法 |", "|---|---|---|---|---|---|---|---|---|"]
    for it in C["items"]:
        thr = "—" if it["op"] is None else f"{it['op']} {it['threshold']}"
        tier = it["tier"] + (" (not-testable)" if it.get("force_not_testable") else "")
        L.append(f"| {it['id']} | {tier} | {it.get('declared_tier', it['tier'])} | {it.get('source_level', '—')} | {', '.join(it.get('source_paths') or []) or '—'} "
                 f"| {it['what']} | {it['metric'] or '—'} | {thr} | {it['method']} |")
    must = [i["id"] for i in C["items"] if i["tier"] == "must"]
    down = [f"{i['id']}（{i['source_level']}）" for i in C["items"] if i.get("downgraded_reason")]
    L += ["", f"- 降级后 must：{', '.join(must)}", f"- 被降级：{', '.join(down) or '无'}"]
    return "\n".join(L) + "\n"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--ref-analysis", required=True)
    ap.add_argument("--script")
    ap.add_argument("--same-content", action="store_true", help="replica re-renders the SAME content as the reference")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    if os.path.exists(a.out):
        print(f"[checklist] {a.out} already exists — NOT overwriting (thresholds and baselines are pre-declared). Delete it deliberately to regenerate.")
        return
    T = read_json(a.tokens)
    A = read_json(os.path.join(a.ref_analysis, "analysis.json"))
    RT = ref_measured_tokens(a.ref_analysis)
    C = build(T, A, read_json(a.script) if a.script else None, a.same_content, RT)
    C["tokens"] = os.path.abspath(a.tokens)
    C["ref_measured_tokens"] = os.path.join(os.path.abspath(a.ref_analysis), "_distill", "style-tokens.json")
    write_json(a.out, C)
    md = os.path.splitext(a.out)[0] + ".md"
    with open(md, "w", encoding="utf-8") as f:
        f.write(to_md(C))
    print(f"[checklist] wrote {a.out} and {md}: {sum(i['tier']=='must' for i in C['items'])} must / "
          f"{sum(i['tier']=='should' for i in C['items'])} should / {sum(i['tier']=='out' for i in C['items'])} out; "
          f"downgraded: {[i['id'] + ':' + i['source_level'] for i in C['items'] if i.get('downgraded_reason')]}")


if __name__ == "__main__":
    main()
