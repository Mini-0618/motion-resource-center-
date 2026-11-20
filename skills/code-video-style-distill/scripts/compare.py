#!/usr/bin/env python3
"""compare.py — score a replica against the reference with a PRE-DECLARED checklist.

Usage:
  compare.py --ref ref.mp4 --rep replica.mp4 --checklist acceptance.json -o <compare_dir>
             [--ref-analysis dir] [--rep-analysis dir] [--tokens style-tokens.json]
             [--ledger iteration-ledger.json] [--samples 8] [--note "what changed this round"]

Outputs (compare_dir):
  frames/t??.png        side-by-side frames at the same normalised times (left=reference, right=replica)
  sidebyside_grid.png   all pairs in one sheet
  sidebyside.mp4        both videos side by side (shorter one padded by freezing its last frame)
  pixel_diff/*.png      per-pixel channel-threshold diff masks (only when sizes match)
  metrics.json          every measured number
  report.md             scores + checklist results
  gap-report.md         failing items sorted must→should with concrete token edits
  ledger (json + md)    one row per round; DONE when all must items pass in 2 consecutive rounds

Provenance of ideas (all re-implemented in Python here, nothing installed):
  * checklist tiers / gap report / run ledger / two-consecutive-rounds rule — adapted from
    Speedrunlab/reverse-engineer-anything-self-learning-loop (MIT, © 2026 Speedrun AI Labs Pty Ltd)
  * side-by-side comparison video as the deliverable shape — idea from JuneYaooo/rea-video (Apache-2.0)
  * horizontal style-band colour comparison for different content — idea from obaid1dev/dea scripts/compare.py (MIT)
  * per-pixel per-channel threshold diff + changed-pixel ratio; size mismatch => "mismatch", never pass —
    idea from morluto/rea src/domain/pngVisualDiff.ts (MIT); this is an independent Python rewrite.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
import subprocess
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cvsd_common import (ffprobe, read_json, write_json, srgb_to_lab, delta_e2000, hex_to_rgb, extract_frame, tc, run)  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"


def ensure_analysis(video, adir):
    if not os.path.exists(os.path.join(adir, "analysis.json")):
        print(f"[compare] analyzing {video} -> {adir}")
        subprocess.run([PY, os.path.join(HERE, "analyze.py"), video, "-o", adir], check=True)
    return read_json(os.path.join(adir, "analysis.json"))


def ensure_tokens(adir, name):
    out = os.path.join(adir, "_distill")
    p = os.path.join(out, "style-tokens.json")
    if not os.path.exists(p):
        subprocess.run([PY, os.path.join(HERE, "distill.py"), adir, "-o", out, "--name", name], check=True, capture_output=True)
    return read_json(p)


# ------------------------------------------------------------------ metrics

def lab(h):
    return srgb_to_lab(np.array(hex_to_rgb(h), float))


def palette_weighted_de(ref_pal, rep_pal, min_ratio=0.005):
    rep_labs = [lab(c["hex"]) for c in rep_pal]
    tot = num = 0.0
    rows = []
    for c in ref_pal:
        if c["ratio"] < min_ratio:
            continue
        d = min(float(delta_e2000(lab(c["hex"]), r)) for r in rep_labs)
        num += d * c["ratio"]
        tot += c["ratio"]
        rows.append({"ref": c["hex"], "ratio": c["ratio"], "nearest_de": round(d, 2)})
    return (num / tot if tot else None), rows


def nearest_de(hexv, pals):
    labs = [lab(c["hex"]) for p in pals for c in p]
    return min(float(delta_e2000(lab(hexv), l)) for l in labs) if labs else None


def mean_profile(A):
    ps = [e["velocity_profile_20"] for e in A["motion"]["events"] if not e["is_transition"] and e.get("velocity_profile_20")
          and e.get("velocity_source", "").startswith("optical")]
    return np.mean(ps, axis=0) if ps else None


def pearson(a, b):
    a, b = np.asarray(a, float), np.asarray(b, float)
    if a.std() < 1e-9 or b.std() < 1e-9:
        return None
    return float(np.corrcoef(a, b)[0, 1])


def energy_curve(adir, n=200):
    import csv
    t, e = [], []
    with open(os.path.join(adir, "motion_energy.csv")) as f:
        for r in csv.DictReader(f):
            t.append(float(r["time_s"]))
            e.append(float(r["energy"]))
    t, e = np.array(t), np.array(e)
    k = np.ones(5) / 5
    e = np.convolve(e, k, mode="same")
    x = np.linspace(0, t[-1], n)
    return np.interp(x, t, e)


def ssim(a, b):
    a = a.astype(np.float64)
    b = b.astype(np.float64)
    C1, C2 = (0.01 * 255) ** 2, (0.03 * 255) ** 2
    mu1, mu2 = cv2.GaussianBlur(a, (11, 11), 1.5), cv2.GaussianBlur(b, (11, 11), 1.5)
    s1 = cv2.GaussianBlur(a * a, (11, 11), 1.5) - mu1 ** 2
    s2 = cv2.GaussianBlur(b * b, (11, 11), 1.5) - mu2 ** 2
    s12 = cv2.GaussianBlur(a * b, (11, 11), 1.5) - mu1 * mu2
    m = ((2 * mu1 * mu2 + C1) * (2 * s12 + C2)) / ((mu1 ** 2 + mu2 ** 2 + C1) * (s1 + s2 + C2))
    return float(m.mean())


def pixel_channel_diff(a, b, channel_threshold=16):
    """Per-pixel diff: a pixel 'changed' if ANY RGB channel differs by > channel_threshold.
    Size mismatch returns status 'mismatch' (never pass)."""
    if a.shape != b.shape:
        return {"status": "mismatch", "ref_size": list(a.shape[:2][::-1]), "rep_size": list(b.shape[:2][::-1])}, None
    d = np.abs(a.astype(np.int16) - b.astype(np.int16)).max(-1)
    mask = d > channel_threshold
    return {"status": "compared", "channel_threshold": channel_threshold, "changed_ratio": round(float(mask.mean()), 4),
            "max_channel_delta": int(d.max()), "mean_channel_delta": round(float(d.mean()), 2)}, mask


def band_similarity(a, b, n=12):
    """Style-band check for DIFFERENT content (idea: obaid1dev/dea compare.py, MIT — re-implemented):
    resize both to the same width, cut into n horizontal bands, compare each band's mean colour (ΔE2000)
    and luminance structure. Returns per-band ΔE list; the worst bands tell where the style drifts."""
    h = int(round(a.shape[0] * 480 / a.shape[1]))
    A_ = cv2.resize(a, (480, h), interpolation=cv2.INTER_AREA)
    B_ = cv2.resize(b, (480, h), interpolation=cv2.INTER_AREA)
    out = []
    for i in range(n):
        y0, y1 = i * h // n, (i + 1) * h // n
        ma, mb = A_[y0:y1].reshape(-1, 3).mean(0), B_[y0:y1].reshape(-1, 3).mean(0)
        out.append(round(float(delta_e2000(srgb_to_lab(ma), srgb_to_lab(mb))), 2))
    return out


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", required=True)
    ap.add_argument("--rep", required=True)
    ap.add_argument("--checklist", required=True)
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--ref-analysis")
    ap.add_argument("--rep-analysis")
    ap.add_argument("--tokens")
    ap.add_argument("--ledger")
    ap.add_argument("--samples", type=int, default=8)
    ap.add_argument("--channel-threshold", type=int, default=16)
    ap.add_argument("--note", default="")
    a = ap.parse_args()
    out = os.path.abspath(a.out)
    os.makedirs(os.path.join(out, "frames"), exist_ok=True)
    C = read_json(a.checklist)
    tokens = read_json(a.tokens or C["tokens"])
    ref_dir = a.ref_analysis or C.get("reference_analysis") or os.path.join(out, "ref_analysis")
    rep_dir = a.rep_analysis or os.path.join(out, "rep_analysis")
    RA = ensure_analysis(a.ref, ref_dir)
    PA = ensure_analysis(a.rep, rep_dir)
    RT = ensure_tokens(ref_dir, "ref-measured")
    PT = ensure_tokens(rep_dir, "rep-measured")
    rm, pm = RA["source"], PA["source"]

    # ---- side-by-side frames + pixel diff
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype(FONT, 22)
    except Exception:
        font = ImageFont.load_default()
    pairs, ssims, pix = [], [], []
    os.makedirs(os.path.join(out, "pixel_diff"), exist_ok=True)
    for i in range(a.samples):
        f = (i + 0.5) / a.samples
        tr, tp = f * rm["duration_s"], f * pm["duration_s"]
        r_png = extract_frame(a.ref, tr, os.path.join(out, "frames", f"ref_{i:02d}.png"))
        p_png = extract_frame(a.rep, tp, os.path.join(out, "frames", f"rep_{i:02d}.png"))
        ri, pi = Image.open(r_png).convert("RGB"), Image.open(p_png).convert("RGB")
        ra_, pa_ = np.array(ri), np.array(pi)
        res, mask = pixel_channel_diff(ra_, pa_, a.channel_threshold)
        res.update({"i": i, "ref_tc": tc(tr), "rep_tc": tc(tp)})
        if mask is not None:
            cv2.imwrite(os.path.join(out, "pixel_diff", f"diff_{i:02d}.png"), mask.astype(np.uint8) * 255)
            ssims.append(ssim(cv2.cvtColor(ra_, cv2.COLOR_RGB2GRAY), cv2.cvtColor(pa_, cv2.COLOR_RGB2GRAY)))
        res["bands"] = band_similarity(ra_, pa_)
        pix.append(res)
        w = 800
        rr = ri.resize((w, int(ri.height * w / ri.width)))
        pp = pi.resize((w, int(pi.height * w / pi.width)))
        hh = max(rr.height, pp.height)
        canvas = Image.new("RGB", (2 * w + 30, hh + 40), (20, 20, 20))
        canvas.paste(rr, (10, 36))
        canvas.paste(pp, (w + 20, 36))
        d = ImageDraw.Draw(canvas)
        d.text((10, 6), f"REFERENCE {tc(tr)}", fill=(230, 230, 230), font=font)
        d.text((w + 20, 6), f"REPLICA {tc(tp)}  ({f * 100:.0f}% of timeline)", fill=(230, 230, 230), font=font)
        pth = os.path.join(out, "frames", f"t{i:02d}.png")
        canvas.save(pth)
        pairs.append(pth)
        os.remove(r_png)
        os.remove(p_png)
    ims = [Image.open(p) for p in pairs]
    grid = Image.new("RGB", (ims[0].width, sum(i.height for i in ims)), (0, 0, 0))
    y = 0
    for im in ims:
        grid.paste(im, (0, y))
        y += im.height
    grid_path = os.path.join(out, "sidebyside_grid.png")
    grid.thumbnail((1640, 100000))
    grid.save(grid_path)

    # ---- side-by-side mp4 (half-height each, freeze shorter one)
    sbs = os.path.join(out, "sidebyside.mp4")
    D = max(rm["duration_s"], pm["duration_s"])
    lab_ = f":fontfile={FONT}" if os.path.exists(FONT) else ""
    fc = (f"[0:v]scale=-2:540,setsar=1,tpad=stop_mode=clone:stop_duration={D:.2f},drawtext=text='REFERENCE'{lab_}:x=20:y=20:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.5[l];"
          f"[1:v]scale=-2:540,setsar=1,tpad=stop_mode=clone:stop_duration={D:.2f},drawtext=text='REPLICA'{lab_}:x=20:y=20:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.5[r];"
          f"[l][r]hstack=inputs=2,fps=30[v]")
    cmd = ["ffmpeg", "-y", "-v", "error", "-i", a.ref, "-i", a.rep, "-filter_complex", fc, "-map", "[v]"]
    if rm["has_audio"]:
        cmd += ["-map", "0:a", "-c:a", "aac"]
    cmd += ["-t", f"{D:.2f}", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "23", sbs]
    run(cmd)

    # ---- metrics
    M = {}
    M["canvas_equal"] = (rm["width"], rm["height"], round(rm["fps"])) == (pm["width"], pm["height"], round(pm["fps"]))
    M["bg_delta_e"] = round(float(delta_e2000(lab(RA["background"]["hex"]), lab(PA["background"]["hex"]))), 2)
    wde, rows = palette_weighted_de(RA["palette_global"], PA["palette_global"] + PA.get("palette_foreground", []))
    M["palette_weighted_delta_e"] = round(wde, 2) if wde is not None else None
    M["palette_rows"] = rows
    pals = [PA["palette_global"], PA.get("palette_foreground", [])]
    roles = [tokens["palette"].get("primary"), tokens["palette"].get("accent")]
    M["role_colors_delta_e"] = {h: round(nearest_de(h, pals), 2) for h in roles if h}
    M["role_colors_max_delta_e"] = max(M["role_colors_delta_e"].values()) if M["role_colors_delta_e"] else None
    rp, pp_ = mean_profile(RA), mean_profile(PA)
    M["entrance_profile_ref"] = rp.round(3).tolist() if rp is not None else None
    M["entrance_profile_rep"] = pp_.round(3).tolist() if pp_ is not None else None
    M["entrance_profile_corr"] = round(pearson(rp, pp_), 3) if rp is not None and pp_ is not None and pearson(rp, pp_) is not None else None
    rd = [e["duration_s"] for e in RA["motion"]["events"] if not e["is_transition"]]
    pd_ = [e["duration_s"] for e in PA["motion"]["events"] if not e["is_transition"]]
    M["entrance_duration_ref_s"] = float(np.median(rd)) if rd else None
    M["entrance_duration_rep_s"] = float(np.median(pd_)) if pd_ else None
    M["entrance_duration_ratio_err"] = round(abs(M["entrance_duration_rep_s"] / M["entrance_duration_ref_s"] - 1), 3) if rd and pd_ else None
    rl, pl = RA["layout"].get("margins_pct"), PA["layout"].get("margins_pct")
    align_same = RA["layout"].get("dominant_alignment") == PA["layout"].get("dominant_alignment")
    M["alignment"] = {"ref": RA["layout"].get("dominant_alignment"), "rep": PA["layout"].get("dominant_alignment")}
    M["margin_left_diff_pct"] = round(abs(rl["left"] - pl["left"]), 2) if rl and pl and align_same else (99.0 if rl and pl else None)
    have = {c["type"] for c in PT["components"]}
    req = next((it.get("required_components", []) for it in C["items"] if it["id"] == "M8"), [])
    M["components_detected"] = sorted(have)
    M["components_missing_list"] = sorted(set(req) - have)
    M["components_missing"] = len(M["components_missing_list"])
    rs = RT["typography"]["scale_px"]
    k_ = rm["height"] / pm["height"]  # compare type sizes relative to canvas height
    ps = {k: v * k_ for k, v in PT["typography"]["scale_px"].items()}
    M["body_size"] = {"ref": rs["body"], "rep": ps["body"]}
    M["body_size_ratio_err"] = round(abs(ps["body"] / rs["body"] - 1), 3)
    M["h1_size"] = {"ref": rs["h1"], "rep": ps["h1"]}
    M["h1_size_ratio_err"] = round(abs(ps["h1"] / rs["h1"] - 1), 3)
    rtz, ptz = RT["motion"]["transition"], PT["motion"]["transition"]
    M["transition"] = {"ref": rtz, "rep": ptz}
    M["transition_match"] = rtz["type"] == ptz["type"] and (rtz["duration_s"] == 0 or abs(ptz["duration_s"] / max(rtz["duration_s"], 1e-6) - 1) <= 0.3)
    M["shot_mean"] = {"ref": RA["rhythm"]["shot_duration_mean_s"], "rep": PA["rhythm"]["shot_duration_mean_s"]}
    M["shot_mean_ratio_err"] = round(abs(PA["rhythm"]["shot_duration_mean_s"] / RA["rhythm"]["shot_duration_mean_s"] - 1), 3)
    rsg, psg = RA["rhythm"].get("stagger_median_s"), PA["rhythm"].get("stagger_median_s")
    M["stagger"] = {"ref": rsg, "rep": psg}
    M["stagger_ratio_err"] = round(abs(psg / rsg - 1), 3) if rsg and psg else None
    M["decor_match"] = RT["layout"]["decor"]["grid_lines"] == PT["layout"]["decor"]["grid_lines"]
    ras, pas = (RA.get("audio") or {}).get("av_sync"), (PA.get("audio") or {}).get("av_sync")
    M["av_sync_ratio_diff"] = round(abs(ras["match_ratio"] - pas["match_ratio"]), 3) if ras and pas else None
    rc, pc = energy_curve(ref_dir), energy_curve(rep_dir)
    M["timeline_energy_corr"] = round(pearson(rc, pc), 3) if pearson(rc, pc) is not None else None
    M["mean_ssim"] = round(float(np.mean(ssims)), 3) if ssims else None
    M["pixel_diff"] = pix
    bands = np.array([p["bands"] for p in pix])
    M["band_mean_delta_e"] = bands.mean(0).round(2).tolist()
    worst = np.argsort(-bands.mean(0))[:4]
    M["worst_bands"] = [{"band": int(i), "y_pct": [round(float(i * 100 / bands.shape[1]), 1), round(float((i + 1) * 100 / bands.shape[1]), 1)], "mean_delta_e": float(bands.mean(0)[i].round(2))} for i in worst]
    M["pixel_size_status"] = "mismatch" if any(p["status"] == "mismatch" for p in pix) else "compared"
    M["pixel_changed_ratio_mean"] = round(float(np.mean([p["changed_ratio"] for p in pix if p["status"] == "compared"])), 4) if M["pixel_size_status"] == "compared" else None

    # ---- evaluate checklist
    results = []
    for it in C["items"]:
        if it["tier"] == "out":
            results.append({**it, "value": None, "result": "out"})
            continue
        v = M.get(it["metric"])
        if it["metric"] == "mean_ssim" and M["pixel_size_status"] == "mismatch":
            r = "mismatch"
        elif v is None:
            r = "not-testable"
        else:
            op, thr = it["op"], it["threshold"]
            ok = (v <= thr) if op == "<=" else (v >= thr) if op == ">=" else (v == thr)
            r = "pass" if ok else "fail"
        results.append({**it, "value": v, "result": r})
    must = [r for r in results if r["tier"] == "must"]
    should = [r for r in results if r["tier"] == "should"]
    must_pass = all(r["result"] == "pass" for r in must)
    score = round(100 * (0.7 * sum(r["result"] == "pass" for r in must) / max(1, len(must)) +
                         0.3 * sum(r["result"] == "pass" for r in should) / max(1, len(should))), 1)
    write_json(os.path.join(out, "metrics.json"), {"metrics": M, "results": results, "score": score, "must_pass": must_pass})

    # ---- ledger
    ledger_path = a.ledger or os.path.join(os.path.dirname(os.path.abspath(a.checklist)), "iteration-ledger.json")
    ledger = read_json(ledger_path) if os.path.exists(ledger_path) else {"rounds": []}
    tok_hash = hashlib.sha1(json.dumps(tokens, sort_keys=True).encode()).hexdigest()[:10]
    rnd = len(ledger["rounds"]) + 1
    prev = ledger["rounds"][-1] if ledger["rounds"] else None
    entry = {"round": rnd, "at": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "replica": os.path.abspath(a.rep),
             "tokens_sha1": tok_hash, "note": a.note, "score": score, "must_pass": must_pass,
             "results": {r["id"]: r["result"] for r in results if r["tier"] != "out"}, "compare_dir": out,
             "score_delta": round(score - prev["score"], 1) if prev else None}
    ledger["rounds"].append(entry)
    last2 = ledger["rounds"][-2:]
    done = len(last2) == 2 and all(x["must_pass"] for x in last2)
    stalled = len(ledger["rounds"]) >= 3 and len({x["score"] for x in ledger["rounds"][-3:]}) == 1
    ledger["status"] = "DONE (must items passed 2 consecutive rounds)" if done else ("STALLED — ask a human" if stalled else "ITERATING")
    write_json(ledger_path, ledger)
    with open(os.path.splitext(ledger_path)[0] + ".md", "w", encoding="utf-8") as f:
        f.write("# 迭代账本\n\n结构改编自 Speedrunlab/reverse-engineer-anything-self-learning-loop `templates/run-ledger.md`（MIT）。\n\n"
                f"状态：**{ledger['status']}**\n\n| 轮 | 时间 | 分数 | Δ | must 全过 | tokens | 改了什么 | 失败项 |\n|---|---|---|---|---|---|---|---|\n")
        for x in ledger["rounds"]:
            fails = [k for k, v in x["results"].items() if v != "pass"]
            f.write(f"| {x['round']} | {x['at']} | {x['score']} | {x['score_delta']} | {x['must_pass']} | {x['tokens_sha1']} | {x['note']} | {', '.join(fails) or '—'} |\n")

    # ---- reports
    def fmt(v):
        if isinstance(v, float):
            return f"{v:.3f}"
        return json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else str(v)
    L = [f"# Compare report — round {rnd}", "",
         f"- 参考：`{os.path.abspath(a.ref)}`（{rm['width']}x{rm['height']} {rm['fps']}fps {rm['duration_s']}s）",
         f"- 复刻：`{os.path.abspath(a.rep)}`（{pm['width']}x{pm['height']} {pm['fps']}fps {pm['duration_s']}s）",
         f"- 清单：`{os.path.abspath(a.checklist)}`（预先声明）", f"- **总分 {score}/100**（must 70% + should 30%）；must 全过：**{must_pass}**；账本状态：**{ledger['status']}**",
         f"- 并排帧：`{grid_path}`", f"- 并排视频：`{sbs}`", "",
         "## 关键分数", "",
         f"- 色板加权 ΔE2000：{M['palette_weighted_delta_e']}；背景 ΔE：{M['bg_delta_e']}；主/强调色 ΔE：{M['role_colors_delta_e']}",
         f"- 入场速度曲线相关性 r：{M['entrance_profile_corr']}；入场时长 ref {M['entrance_duration_ref_s']}s / rep {M['entrance_duration_rep_s']}s",
         f"- 整条运动能量曲线相关性 r：{M['timeline_energy_corr']}（不同选题时仅供参考）",
         f"- 逐像素通道阈值差异（>{a.channel_threshold}/255 任一通道）：尺寸 {M['pixel_size_status']}，平均变化像素比例 {M['pixel_changed_ratio_mean']}；SSIM {M['mean_ssim']}",
         f"- 风格条带（12 条水平带平均色 ΔE，换选题时看风格是否跑偏，思路来自 obaid1dev/dea compare.py, MIT）：最差 4 条 {M['worst_bands']}",
         "", "## 清单结果", "", "| ID | 档位 | 项目 | 值 | 阈值 | 结果 |", "|---|---|---|---|---|---|"]
    for r in results:
        thr = "—" if r["op"] is None else f"{r['op']} {r['threshold']}"
        L.append(f"| {r['id']} | {r['tier']} | {r['what']} | {fmt(r['value'])} | {thr} | **{r['result']}** |")
    L += ["", "> 视觉主张合同：尺寸不一致记 mismatch，测不到记 not-testable，二者都不算通过（思路参考 morluto/rea，MIT）。",
          "> 不同选题的复刻，像素差异和 SSIM 只作参考，属于 out 档。"]
    with open(os.path.join(out, "report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")

    G = [f"# Gap report — round {rnd}", "", "改编自 Speedrunlab/reverse-engineer-anything-self-learning-loop `templates/gap-report.md`（MIT）。",
         "排序：must（挡住验收）→ should（外观差异）。一次只修一批，修完重跑 render + compare。", ""]
    gaps = [r for r in results if r["tier"] in ("must", "should") and r["result"] != "pass"]
    gaps.sort(key=lambda r: (r["tier"] != "must", r["id"]))
    if not gaps:
        G.append("无差距项。下一轮仍需复跑一次，确认 must 项连续两轮通过。")
    for r in gaps:
        G.append(f"## {r['id']} [{r['tier']}] {r['what']} — {r['result']}")
        G.append(f"- 值 {fmt(r['value'])}，阈值 {r['op']} {r['threshold']}；证据：`{os.path.join(out, 'metrics.json')}`，参考侧 `{r['evidence_in']}`")
        G.append(f"- 建议：{suggest(r, M, tokens, RT, PT)}")
        G.append("")
    with open(os.path.join(out, "gap-report.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(G) + "\n")
    print(f"[compare] round {rnd}: score {score}, must_pass={must_pass}, ledger={ledger['status']}")
    for r in results:
        if r["tier"] != "out":
            print(f"   {r['id']:3s} {r['tier']:6s} {r['result']:12s} {r['metric']} = {fmt(r['value'])}")
    print(f"[compare] report: {os.path.join(out, 'report.md')}\n[compare] gaps: {os.path.join(out, 'gap-report.md')}\n[compare] sbs: {sbs}")


def suggest(r, M, T, RT, PT):
    m = r["metric"]
    if m == "bg_delta_e":
        return f"palette.bg 改成参考实测值（参考 {RT['palette']['bg']}，复刻 {PT['palette']['bg']}）"
    if m in ("palette_weighted_delta_e", "role_colors_max_delta_e"):
        bad = [x for x in M.get("palette_rows", []) if x["nearest_de"] > 6]
        return f"这些参考色在复刻片里没对上：{bad[:4]}；检查 palette 角色分配和元件用色（主色是否用于标题/柱子）"
    if m == "entrance_profile_corr":
        return f"调整 motion.easing.enter.cubic_bezier（当前 {T['motion']['easing']['enter']['cubic_bezier']}）；参考曲线 {M['entrance_profile_ref']}，复刻 {M['entrance_profile_rep']}：峰值越靠前越接近 ease-out"
    if m == "entrance_duration_ratio_err":
        ref, rep = M["entrance_duration_ref_s"], M["entrance_duration_rep_s"]
        cur = T["motion"]["durations_s"]["base"]
        return f"motion.durations_s.base 当前 {cur}s，按比例改成 ≈{round(cur * ref / rep, 3)}s（参考事件 {ref}s / 复刻 {rep}s）"
    if m == "margin_left_diff_pct":
        return f"layout.margins_pct.left / alignment 对齐参考（{M['alignment']}）"
    if m == "components_missing":
        return f"复刻片里没检测到 {M['components_missing_list']}：确认 script.json 用了对应段落类型，或该元件样式差太多"
    if m in ("body_size_ratio_err", "h1_size_ratio_err"):
        k = "body" if m.startswith("body") else "h1"
        ref, rep = RT["typography"]["scale_px"][k], PT["typography"]["scale_px"][k]
        cur = T["typography"]["scale_px"][k]
        return f"typography.scale_px.{k} 当前 {cur}px → 约 {round(cur * ref / rep)}px（参考测得 {ref} / 复刻测得 {rep}）"
    if m == "transition_match":
        rt, pt = M["transition"]["ref"], M["transition"]["rep"]
        cur = T["motion"]["transition"]
        dur = round(cur["duration_s"] * rt["duration_s"] / max(pt["duration_s"], 1e-6), 3) if pt["duration_s"] else cur["duration_s"]
        return f"motion.transition 改为 type={rt['type']}，duration_s≈{dur}（参考 {rt} / 复刻 {pt}）"
    if m == "stagger_ratio_err":
        s = M["stagger"]
        return f"motion.stagger_s 当前 {T['motion']['stagger_s']} → ≈{round(T['motion']['stagger_s'] * s['ref'] / s['rep'], 3) if s['rep'] else '?'}；注意 bullets 组件会按段落时长自动放大间隔"
    if m == "shot_mean_ratio_err":
        return f"script.json 各段 duration_s 向参考平均镜头时长 {M['shot_mean']['ref']}s 靠拢"
    if m == "decor_match":
        return "layout.decor.grid_lines 与参考保持一致"
    if m == "av_sync_ratio_diff":
        return "把段落切点/入场时间对齐到音频起音点（rhythm.av_sync）"
    return "看并排帧和 metrics.json 手动判断"


if __name__ == "__main__":
    main()
