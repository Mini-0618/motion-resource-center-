#!/usr/bin/env python3
"""stillcheck.py — still-frame precheck BEFORE the full render.

Renders only 3 settled frames (renderStill) for 3 representative reference scenes and checks the
palette tier (bg ΔE, palette weighted ΔE, primary/accent ΔE) and the layout tier (left margin,
alignment, safe area, panel corner radius). Thresholds and tiers are read from acceptance.json
(post-downgrade), baselines too. Any failing MUST item -> gap report + exit code 1 (do not render).

Usage: stillcheck.py --acceptance <work>/acceptance.json --tokens <style-tokens.json> --script <script.json>
                     --ref-analysis <work>/ref_analysis -o <work>/stillcheck_rN [--renderer remotion]
"""
import argparse
import json
import os
import sys
import time

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cvsd_common import minor_chromatic, read_json, write_json, kmeans_palette, srgb_to_lab, delta_e2000, rgb_to_hex, hex_to_rgb  # noqa: E402
import analyze as AZ  # noqa: E402
from distill import corner_radius  # noqa: E402
import renderers  # noqa: E402

SURFACE_FIRST = ["code", "compare", "flow"]
TEXT = ["bullets", "title"]
OTHER = ["timeline", "bars", "evidence", "stat"]
METRICS = ["bg_delta_e", "palette_weighted_delta_e", "role_colors_max_delta_e", "margin_left_diff_pct", "alignment_match",
           "safe_area_diff_pct", "radius_diff_px"]


def lab(h):
    return srgb_to_lab(np.array(hex_to_rgb(h), float))


def pick_scenes(A, RT, script):
    """3 (ref scene index, script segment index, segment type) pairs: one panel scene, one text scene, one other."""
    seg_types = [s.get("type") for s in script.get("segments", [])]
    by_type = {}
    for c in RT.get("components", []):
        t = c.get("template_segment")
        if t and c.get("scenes"):
            by_type.setdefault(t, c["scenes"][-1])
    picks = []
    for group in (SURFACE_FIRST, TEXT, OTHER):
        for t in group:
            if t in by_type and t in seg_types and not any(p[2] == t for p in picks):
                picks.append((by_type[t], seg_types.index(t), t))
                break
    # fallback: spread over remaining scenes / segments
    n_sc, n_sg = len(A["scenes"]), len(seg_types)
    k = 0
    while len(picks) < 3 and k < 6:
        f = (k + 0.5) / 3
        sc, sg = min(n_sc - 1, int(f * n_sc)), min(n_sg - 1, int(f * n_sg))
        if not any(p[0] == sc or p[1] == sg for p in picks):
            picks.append((sc, sg, seg_types[sg]))
        k += 1
    return picks[:3]


def frame_bg(img):
    px = AZ.border_pixels(img)
    q = (px // 4).astype(np.int32)
    keys, counts = np.unique(q[:, 0] * 65536 + q[:, 1] * 256 + q[:, 2], return_counts=True)
    sel = q[:, 0] * 65536 + q[:, 1] * 256 + q[:, 2] == keys[np.argmax(counts)]
    return np.median(px[sel], 0)


def side_stats(paths):
    imgs = [cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2RGB) for p in paths]
    H, W = imgs[0].shape[:2]
    bg = np.median([frame_bg(i) for i in imgs], 0)
    allpx = np.concatenate([i.reshape(-1, 3)[::7] for i in imgs])
    pal = kmeans_palette(allpx, k=8)
    fgpx = allpx[delta_e2000(srgb_to_lab(allpx.astype(float)), srgb_to_lab(bg.astype(float))) > 8]
    pal_fg = kmeans_palette(fgpx, k=8) if len(fgpx) > 50 else []
    L = AZ.estimate_layout(paths, [int(v) for v in bg], W, H)
    radii = []
    for sf in L.get("surfaces", []):
        img = imgs[[os.path.basename(p) for p in paths].index(sf["frame"])]
        r = corner_radius(img, sf["box"], sf["rgb"])
        if r:
            radii.append(r)
    minor = minor_chromatic(imgs, bg)
    return {"W": W, "H": H, "bg": rgb_to_hex(bg), "palette": pal, "palette_fg": pal_fg, "minor": minor, "layout": L,
            "radius_px": float(np.median(radii)) if radii else None}


def nearest(hexv, pals):
    labs = [lab(c["hex"]) for p in pals for c in p]
    return min(float(delta_e2000(lab(hexv), x)) for x in labs) if labs else None


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--acceptance", required=True)
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--ref-analysis", required=True)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--renderer")
    a = ap.parse_args()
    t0 = time.time()
    C, T, S = read_json(a.acceptance), read_json(a.tokens), read_json(a.script)
    A = read_json(os.path.join(a.ref_analysis, "analysis.json"))
    rtp = C.get("ref_measured_tokens") or os.path.join(a.ref_analysis, "_distill", "style-tokens.json")
    RT = read_json(rtp) if os.path.exists(rtp) else T
    picks = pick_scenes(A, RT, S)
    win = renderers.segment_windows(S, T)
    times = [win[sg][2] for _, sg, _ in picks]
    os.makedirs(a.out, exist_ok=True)
    t_r = time.time()
    rc, stills = renderers.render_stills(a.tokens, a.script, times, os.path.join(a.out, "stills"), a.renderer)
    render_s = time.time() - t_r
    if rc != 0:
        print("[stillcheck] renderer failed")
        sys.exit(2)
    ref_frames = [A["scenes"][sc]["keyframes"]["settled"]["path"] for sc, _, _ in picks]
    R, P = side_stats(ref_frames), side_stats(stills)

    M = {}
    M["bg_delta_e"] = round(float(delta_e2000(lab(R["bg"]), lab(P["bg"]))), 2)
    num = tot = 0.0
    for c in R["palette"]:
        if c["ratio"] >= 0.005:
            num += nearest(c["hex"], [P["palette"], P["palette_fg"]]) * c["ratio"]
            tot += c["ratio"]
    M["palette_weighted_delta_e"] = round(num / tot, 2) if tot else None
    items = {it.get("metric"): it for it in C["items"]}
    base = (items.get("role_colors_max_delta_e", {}).get("baseline") or
            {"primary": RT["palette"].get("primary"), "accent": RT["palette"].get("accent")})
    M["role_colors_delta_e"] = {h: round(nearest(h, [P["palette"], P["palette_fg"], P["minor"]]), 2) for h in base.values() if h}
    M["role_colors_max_delta_e"] = max(M["role_colors_delta_e"].values()) if M["role_colors_delta_e"] else None
    rl, pl = R["layout"], P["layout"]
    if "margins_pct" in rl and "margins_pct" in pl:
        M["margin_left_diff_pct"] = round(abs(rl["margins_pct"]["left"] - pl["margins_pct"]["left"]), 2)
        M["alignment_match"] = rl["dominant_alignment"] == pl["dominant_alignment"]
        rs, ps = rl["safe_area_pct_estimate"], pl["safe_area_pct_estimate"]
        M["safe_area_diff_pct"] = round(max(abs(rs["x"] - ps["x"]), abs(rs["y"] - ps["y"])), 2)
    rr = (items.get("radius_diff_px", {}).get("baseline") or {}).get("radius_px") or R["radius_px"]
    M["radius_diff_px"] = round(abs(rr - P["radius_px"] * R["H"] / P["H"]), 1) if rr and P["radius_px"] else None
    M["layout_ref"] = {k: rl.get(k) for k in ("margins_pct", "dominant_alignment", "safe_area_pct_estimate")}
    M["layout_rep"] = {k: pl.get(k) for k in ("margins_pct", "dominant_alignment", "safe_area_pct_estimate")}
    M["radius"] = {"ref_baseline": rr, "rep": P["radius_px"]}

    results = []
    for m in METRICS:
        it = items.get(m)
        if not it:
            continue
        v = M.get(m)
        if it.get("force_not_testable") or v is None:
            r = "not-testable"
        else:
            op, thr = it["op"], it["threshold"]
            r = "pass" if ((v <= thr) if op == "<=" else (v >= thr) if op == ">=" else (v == thr)) else "fail"
        results.append({"id": it["id"], "tier": it["tier"], "source_level": it.get("source_level", "seen"), "what": it["what"], "metric": m,
                        "value": v, "op": it["op"], "threshold": it["threshold"], "result": r})
    blocking = [r for r in results if r["tier"] == "must" and r["result"] == "fail"]
    ok = not blocking
    wall = round(time.time() - t0, 1)
    rep = {"ok": ok, "wall_s": wall, "render_stills_s": round(render_s, 1), "picks": [{"ref_scene": sc, "segment": sg, "type": t, "replica_t_s": round(tt, 3),
           "ref_frame": rf, "still": st} for (sc, sg, t), tt, rf, st in zip(picks, times, ref_frames, stills)],
           "metrics": M, "results": results, "blocking": [r["id"] for r in blocking]}
    write_json(os.path.join(a.out, "stillcheck.json"), rep)

    # side-by-side sheet
    tiles = []
    for rf, st in zip(ref_frames, stills):
        r_, p_ = cv2.imread(rf), cv2.imread(st)
        r_ = cv2.resize(r_, (640, int(r_.shape[0] * 640 / r_.shape[1])))
        p_ = cv2.resize(p_, (640, int(p_.shape[0] * 640 / p_.shape[1])))
        tiles.append(np.hstack([r_, np.full((r_.shape[0], 10, 3), 30, np.uint8), p_]))
    cv2.imwrite(os.path.join(a.out, "stillcheck_sheet.png"), np.vstack(tiles))
    L = [f"# 静帧预检 — {'通过，可以全片渲染' if ok else '未通过，先别全片渲染'}", "",
         f"- 用时 {wall}s（其中渲 3 张静帧 {round(render_s, 1)}s）", f"- 对照图：`{os.path.join(a.out, 'stillcheck_sheet.png')}`（左参考 settled 帧 / 右复刻静帧）",
         f"- 选取：{[(p['type'], 'ref scene ' + str(p['ref_scene']), 'replica t=' + str(p['replica_t_s']) + 's') for p in rep['picks']]}", "",
         "| ID | 档位 | 出处等级 | 项目 | 值 | 阈值 | 结果 |", "|---|---|---|---|---|---|---|"]
    for r in results:
        L.append(f"| {r['id']} | {r['tier']} | {r['source_level']} | {r['what']} | {r['value']} | {r['op']} {r['threshold']} | **{r['result']}** |")
    L += ["", "## 差距", ""]
    for r in results:
        if r["result"] == "pass":
            continue
        if r["source_level"] == "inferred":
            tip = "该值本身是推测，先目测确认再调参"
        elif r["result"] == "not-testable":
            tip = "测不到（静帧里没有对应元素，或来源 unknown），不阻塞"
        else:
            tip = {"bg_delta_e": f"palette.bg 对齐参考 {R['bg']}（复刻 {P['bg']}）",
                   "palette_weighted_delta_e": "检查 palette 各角色和元件用色",
                   "role_colors_max_delta_e": f"primary/accent 基准 {base}，复刻最近色差 {M['role_colors_delta_e']}",
                   "margin_left_diff_pct": f"layout.margins_pct.left：参考 {M['layout_ref']['margins_pct']} / 复刻 {M['layout_rep']['margins_pct']}",
                   "alignment_match": f"对齐：参考 {rl.get('dominant_alignment')} / 复刻 {pl.get('dominant_alignment')}",
                   "safe_area_diff_pct": f"安全区：参考 {M['layout_ref']['safe_area_pct_estimate']} / 复刻 {M['layout_rep']['safe_area_pct_estimate']}",
                   "radius_diff_px": f"layout.radius_px：基准 {rr} / 复刻 {P['radius_px']}"}.get(r["metric"], "")
        L.append(f"- {r['id']} [{r['tier']}] {r['what']} = {r['value']} → {r['result']}：{tip}")
    with open(os.path.join(a.out, "stillcheck.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    print(f"[stillcheck] {'PASS' if ok else 'FAIL'} in {wall}s (stills {round(render_s, 1)}s) — {os.path.join(a.out, 'stillcheck.md')}")
    for r in results:
        print(f"   {r['id']:4s} {r['tier']:6s} {r['source_level']:8s} {r['result']:12s} {r['metric']} = {r['value']}")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
