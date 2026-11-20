#!/usr/bin/env python3
"""distill.py — turn analysis/ into a reusable style base (style-tokens.json).

Usage:
  distill.py <analysis_dir> -o <out_dir> --name <style-name>
             [--overrides overrides.json] [--styles-dir <dir>]

* Every token gets a provenance entry: status = seen | inferred | unknown, plus evidence
  (timecodes / keyframe files / algorithm). Evidence-labelling rule adapted from
  aicodeking/leanrea (MIT): "unknown" means "not measured", never "does not exist".
* Token structure (value + evidence + confidence, motion.easings / motion.keyframes, unknowns, font
  substitution table) follows the idea of obaid1dev/dea (MIT) tokens.json; re-implemented here.
* --overrides: JSON deep-merged on top (e.g. after the AI looked at the contact sheet).
  Overridden paths are marked status=inferred, method="visual review (manual)" unless the
  override file supplies its own "_provenance" block.
* --styles-dir: also saves styles/<name>/ {style-tokens.json, refs/*.png, README.md}.
"""
import argparse
import datetime as dt
import json
import os
import re
import shutil
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import components_detect as CD  # noqa: E402
from cvsd_common import (read_json, write_json, srgb_to_lab, delta_e2000, hex_to_rgb, rgb_to_hex,  # noqa: E402
                         contrast_ratio, chroma, tc)

TOOL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCHEMA = os.path.join(TOOL_DIR, "schema", "style-tokens.schema.json")
# Motion taxonomy shipped INSIDE the skill (references/motion-taxonomy.md); override with --taxonomy or CVSD_TAXONOMY.
DEFAULT_TAXONOMY = os.path.join(TOOL_DIR, "references", "motion-taxonomy.md")


def load_taxonomy(path):
    """parse `| ID | name | keywords |` rows -> {id: name}. Returns ({}, error) when missing/empty."""
    if not path or not os.path.exists(path):
        return {}, f"taxonomy file not found: {path}"
    ids = {}
    for line in open(path, encoding="utf-8"):
        m = re.match(r"^\|\s*((?:UI|V|A)-\d+)\s*\|\s*([^|]+?)\s*\|", line)
        if m:
            ids[m.group(1)] = m.group(2)
    return (ids, None) if ids else ({}, f"no taxonomy rows (| ID | name | ...) in {path}")

# component -> (template segment, UI ids, V ids). Category names in taxonomy-from-user.md.
TAXO = {
    "title_card": ("title", [], ["V-01", "V-15"]),
    "bullet_list": ("bullets", ["UI-09"], ["V-01", "V-10"]),
    "bar_chart": ("bars", ["UI-04"], ["V-02"]),
    "number_counter": ("stat", ["UI-04"], ["V-02", "V-01"]),
    "code_block": ("code", ["UI-09"], ["V-05"]),
    "keyword_highlight": (None, [], ["V-01", "V-13"]),
    "subtitle_bar": (None, [], ["V-13"]),
    "progress_bar": (None, ["UI-01"], ["V-15"]),
    "transition": (None, ["UI-02"], ["V-07"]),
    # knowledge-video components (taxonomy-from-user.md: UI-09 时间线组件/对比面板/可视化流程图;
    # V-03 流程图/时间线/对比矩阵; V-04 证据展示/截图/新闻事件时间轴; V-05 局部高亮/前后对比; V-09 摄像机推进; V-10 线条连接)
    "evidence_frame": ("evidence", [], ["V-04", "V-05", "V-09"]),
    "timeline": ("timeline", ["UI-09"], ["V-03", "V-04"]),
    "compare_columns": ("compare", ["UI-09"], ["V-03", "V-05"]),
    "flow_chart": ("flow", ["UI-09"], ["V-03", "V-10"]),
}
# component type -> components_style key
COMP_STYLE_KEY = {"evidence_frame": "evidence", "timeline": "timeline", "compare_columns": "compare", "flow_chart": "flow"}

FREE_FONTS = {
    "sans_cjk": ["Noto Sans CJK SC / 思源黑体 Source Han Sans SC (SIL OFL 1.1)", "HarmonyOS Sans SC (华为免费商用许可，使用前核对条款)",
                 "MiSans (小米免费商用许可，使用前核对条款)"],
    "sans_latin": ["Inter / Inter Tight (SIL OFL 1.1)", "Geist (SIL OFL 1.1)", "Manrope (SIL OFL 1.1)"],
    "mono": ["JetBrains Mono (SIL OFL 1.1)", "Fira Code (SIL OFL 1.1)", "Noto Sans Mono CJK SC (SIL OFL 1.1)"],
    "serif_cjk": ["Noto Serif CJK SC / 思源宋体 (SIL OFL 1.1)"],
}


class Prov:
    def __init__(self):
        self.d = {}

    def set(self, path, status, evidence=None, method="", note="", confidence=None):
        assert status in ("seen", "inferred", "unknown")
        e = {"status": status, "confidence": {"seen": 0.9, "inferred": 0.6, "unknown": 0.2}[status]}
        if evidence:
            e["evidence"] = evidence[:8]
        if method:
            e["method"] = method
        if note:
            e["note"] = note
        if confidence is not None:
            e["confidence"] = round(float(confidence), 2)
        self.d[path] = e


def ev_frame(path, t=None):
    out = {"frame": path}
    if t is not None:
        out["tc"] = tc(t)
    return out


def deep_merge(a, b):
    if not isinstance(a, dict) or not isinstance(b, dict):
        return b
    out = dict(a)
    for k, v in b.items():
        out[k] = deep_merge(a.get(k), v) if isinstance(v, dict) and isinstance(a.get(k), dict) else v
    return out


def flatten_paths(d, prefix=""):
    out = []
    for k, v in d.items():
        p = f"{prefix}.{k}" if prefix else k
        if isinstance(v, dict) and v:
            out += flatten_paths(v, p)
        else:
            out.append(p)
    return out


def is_neutral(h, lim=22):
    return chroma(hex_to_rgb(h)) < lim


# ---------------------------------------------------------------------------------------------

def distill_palette(A, P):
    bg = A["background"]["hex"]
    roles = A.get("palette_roles_inferred", {})
    scenes = A["scenes"]
    sample_frames = [s["keyframes"]["settled"]["path"] for s in scenes][:4]
    pal = {"bg": bg}
    P.set("palette.bg", "seen", [ev_frame(f) for f in sample_frames], "mode of quantised frame-border pixels",
          f"border share {A['background']['border_mode_share']}")

    lines = A.get("ocr", {}).get("lines", []) if A.get("ocr", {}).get("available") else []
    bg_rgb = hex_to_rgb(bg)
    # text colours from OCR ink on the main background
    text_votes, muted_votes, chroma_ink = {}, {}, {}
    for l in lines:
        if not l.get("ink_colors") or not l.get("local_bg"):
            continue
        on_bg = delta_e2000(srgb_to_lab(hex_to_rgb(l["local_bg"])), srgb_to_lab(bg_rgb)) < 8
        top = l["ink_colors"][0]["hex"]
        if on_bg and is_neutral(top):
            cr = contrast_ratio(hex_to_rgb(top), bg_rgb)
            bucket = text_votes if cr >= 7 else muted_votes
            bucket.setdefault(top, []).append(l)
        for c in l["ink_colors"]:
            if not is_neutral(c["hex"], 25) and c["ratio"] > 0.15:
                chroma_ink.setdefault(c["hex"], []).append(l)

    def best(votes):
        if not votes:
            return None, []
        k = max(votes, key=lambda k: len(votes[k]))
        return k, votes[k]

    t, tl = best(text_votes)
    if t:
        pal["text"] = t
        P.set("palette.text", "seen", [ev_frame(_kf(A, l), None) | {"ocr_line": l["text"]} for l in tl], "dominant ink colour of OCR lines on bg")
    elif roles.get("text"):
        pal["text"] = roles["text"]
        P.set("palette.text", "inferred", [], "highest-contrast neutral palette cluster vs bg")
    else:
        pal["text"] = "#F2F5FA" if contrast_ratio((242, 245, 250), bg_rgb) > 4.5 else "#15171C"
        P.set("palette.text", "unknown", [], "default: auto contrast vs bg")
    m, ml = best(muted_votes)
    if m:
        pal["text_muted"] = m
        P.set("palette.text_muted", "seen", [ev_frame(_kf(A, l)) | {"ocr_line": l["text"]} for l in ml], "ink colour of lower-contrast OCR lines")
    elif roles.get("text_muted"):
        pal["text_muted"] = roles["text_muted"]
        P.set("palette.text_muted", "inferred", [], "mid-contrast neutral palette cluster")
    else:
        tr = np.array(hex_to_rgb(pal["text"]), float)
        pal["text_muted"] = rgb_to_hex(tr * 0.55 + np.array(bg_rgb) * 0.45)
        P.set("palette.text_muted", "unknown", [], "default: 55% text / 45% bg mix")

    surfs = A.get("layout", {}).get("surfaces", [])
    if surfs:
        sf = max(surfs, key=lambda s: s["box"][2] * s["box"][3])
        pal["surface"] = sf["hex"]
        P.set("palette.surface", "seen", [{"frame": os.path.join(A["files"]["keyframes_dir"], sf["frame"]), "box": sf["box"]}],
              "median colour inside large uniform foreground box")
        # code text = light/dark ink inside that surface
        inside = [l for l in lines if _inside(l["bbox"], sf["box"]) and l.get("ink_colors")]
        neu = [l["ink_colors"][0]["hex"] for l in inside if is_neutral(l["ink_colors"][0]["hex"], 25)
               and contrast_ratio(hex_to_rgb(l["ink_colors"][0]["hex"]), sf["rgb"]) >= 4.5]
        if neu:
            pal["code_text"] = max(set(neu), key=neu.count)
            P.set("palette.code_text", "seen", [{"ocr_line": l["text"]} for l in inside][:4], "ink colour of OCR lines inside surface")
    else:
        L = srgb_to_lab(np.array(bg_rgb, float))[0]
        k = 1.12 if L < 50 else 0.94
        pal["surface"] = rgb_to_hex(np.clip(np.array(bg_rgb) * k + (8 if L < 50 else 0), 0, 255))
        P.set("palette.surface", "unknown", [], "no uniform panel found; derived from bg")

    # chromatic roles: prefer chromatic ink from text highlights + foreground clusters
    fg = A.get("palette_foreground") or A.get("palette_global", [])
    chrom = [c for c in fg if chroma(c["rgb"]) >= 25 and delta_e2000(srgb_to_lab(np.array(c["rgb"], float)), srgb_to_lab(np.array(bg_rgb, float))) > 10]
    chrom.sort(key=lambda c: -c["ratio"])
    def is_mix(rgb, base_hex):
        b = np.array(hex_to_rgb(base_hex), float)
        g = np.array(bg_rgb, float)
        for a in np.linspace(0.15, 0.9, 16):
            if delta_e2000(srgb_to_lab(b * a + g * (1 - a)), srgb_to_lab(np.array(rgb, float))) < 6:
                return True
        return False
    picked = []
    for c in chrom:
        if any(is_mix(c["rgb"], p) for p in picked):
            continue
        if all(delta_e2000(srgb_to_lab(np.array(c["rgb"], float)), srgb_to_lab(np.array(hex_to_rgb(p), float))) > 15 for p in picked):
            picked.append(c["hex"])
    ev_pal = [{"file": A["files"]["palette_png"]}]
    if picked:
        pal["primary"] = picked[0]
        P.set("palette.primary", "seen", ev_pal, "most frequent chromatic k-means cluster (Lab) of foreground pixels",
              "role assignment (primary vs accent) is inferred; the colour value is measured")
    else:
        pal["primary"] = pal["text"]
        P.set("palette.primary", "unknown", [], "no chromatic colour measured; fell back to text colour")
    if len(picked) > 1:
        pal["accent"] = picked[1]
        P.set("palette.accent", "seen", ev_pal, "second distinct chromatic cluster (ΔE2000>15 from primary)", "role is inferred")
    else:
        pal["accent"] = pal["primary"]
        P.set("palette.accent", "unknown", [], "only one chromatic colour measured")
    if len(picked) > 2:
        pal["extra"] = picked[2:5]
        P.set("palette.extra", "seen", ev_pal, "further chromatic clusters")
    pal["measured_swatches"] = [{"hex": c["hex"], "ratio": c["ratio"]} for c in A.get("palette_global", [])]
    P.set("palette.measured_swatches", "seen", ev_pal, "global k-means (k=8, Lab), merged ΔE<4")

    # gradient / glow: corners of background differ?
    kf = cv2.cvtColor(cv2.imread(sample_frames[0]), cv2.COLOR_BGR2RGB)
    h, w = kf.shape[:2]
    cs = [kf[:h // 12, :w // 12], kf[:h // 12, -w // 12:], kf[-h // 12:, :w // 12], kf[-h // 12:, -w // 12:]]
    meds = [np.median(c.reshape(-1, 3), 0) for c in cs]
    labs = [srgb_to_lab(m) for m in meds]
    spread = max(float(delta_e2000(a, b)) for a in labs for b in labs)
    return pal, spread


def _kf(A, l):
    s = A["scenes"][l["scene"]]
    return s["keyframes"]["settled"]["path"]


def _inside(b, box):
    x, y, w, h = b
    X, Y, W, H = box
    cx, cy = x + w / 2, y + h / 2
    return X <= cx <= X + W and Y <= cy <= Y + H


# ---------------------------------------------------------------------------------------------

def distill_typography(A, P, cjk_ratio, code_found):
    ocr = A.get("ocr", {})
    H = A["source"]["height"]
    lines = ocr.get("lines", []) if ocr.get("available") else []
    scale_ref = H / 1080.0
    default = {"display": 120, "h1": 72, "h2": 52, "body": 40, "caption": 32, "code": 30}
    scale = {k: round(v * scale_ref) for k, v in default.items()}
    for k in scale:
        P.set(f"typography.scale_px.{k}", "unknown", [], "default ladder scaled to canvas height")
    levels = ocr.get("type_levels", [])
    surfs = A.get("layout", {}).get("surfaces", [])
    def in_surface(l):
        kfn = os.path.basename(_kf(A, l))
        return any(sf["frame"] == kfn and _inside(l["bbox"], sf["box"]) for sf in surfs)
    noncode = [l for l in lines if not l.get("codey") and not in_surface(l) and l["pos_pct"]["y"] < 80
               and not NUM_RE.match(l["text"].replace(" ", ""))]
    if levels and noncode:
        sizes = sorted([l["est_font_size_px"] for l in noncode])
        # body = most common size cluster
        clusters = []
        for s_ in sizes:
            if clusters and abs(s_ - np.median(clusters[-1])) / np.median(clusters[-1]) < 0.15:
                clusters[-1].append(s_)
            else:
                clusters.append([s_])
        body_c = max(clusters, key=len)
        body = float(np.median(body_c))
        bigger = sorted([float(np.median(c)) for c in clusters if np.median(c) > body * 1.15], reverse=True)
        smaller = sorted([float(np.median(c)) for c in clusters if np.median(c) < body * 0.87], reverse=True)

        def evl(size):
            ls = sorted(noncode, key=lambda l: abs(l["est_font_size_px"] - size))[:3]
            return [ev_frame(_kf(A, l)) | {"ocr_line": l["text"], "bbox": l["bbox"]} for l in ls]
        scale["body"] = round(body)
        P.set("typography.scale_px.body", "seen", evl(body), "most frequent OCR line size (ink height / 0.88 CJK, /0.72 Latin)",
              "font size from ink height is an estimate (±10%)")
        if bigger:
            if bigger[0] >= body * 2.4:
                scale["display"] = round(bigger[0])
                P.set("typography.scale_px.display", "seen", evl(bigger[0]), "largest OCR size cluster (≥2.4× body)")
                rest = bigger[1:]
            else:
                rest = bigger
            if rest:
                scale["h1"] = round(rest[0])
                P.set("typography.scale_px.h1", "seen", evl(scale["h1"]), "largest OCR heading cluster above body")
            if "typography.scale_px.display" not in P.d or P.d["typography.scale_px.display"]["status"] == "unknown":
                scale["display"] = round(scale["h1"] * 1.6)
                P.set("typography.scale_px.display", "inferred", [], "h1 × 1.6 (display line not read by OCR — check contact sheet)")
            mids = [b for b in bigger if b < scale["h1"] * 0.9]
            scale["h2"] = round(mids[0]) if mids else round((scale["h1"] + body) / 2)
            P.set("typography.scale_px.h2", "seen" if mids else "inferred", evl(scale["h2"]) if mids else [], "OCR cluster between h1 and body" if mids else "midpoint h1/body")
        if smaller:
            scale["caption"] = round(smaller[0])
            P.set("typography.scale_px.caption", "seen", evl(smaller[0]), "OCR size cluster below body")
        else:
            scale["caption"] = round(body * 0.8)
            P.set("typography.scale_px.caption", "inferred", [], "body × 0.8")
    codel = [l for l in lines if in_surface(l) and l.get("ink_height_px") and len(l["text"]) >= 6] or \
            [l for l in lines if l.get("codey") and l.get("ink_height_px") and l["est_font_size_px"] < 1.3 * scale["body"]]
    if codel:
        scale["code"] = round(float(np.median([l["ink_height_px"] for l in codel])) / 0.95)
        P.set("typography.scale_px.code", "seen", [ev_frame(_kf(A, l)) | {"ocr_line": l["text"]} for l in codel][:3],
              "code-line ink height / 0.95 (mono lines span ascender→descender)")
    elif "body" in scale:
        scale["code"] = round(scale["body"] * 0.75)
        P.set("typography.scale_px.code", "inferred" if code_found else "unknown", [], "body × 0.75")

    # weight: ink coverage of the largest lines vs body lines
    big = [l for l in noncode if l["est_font_size_px"] >= scale.get("h1", 72) * 0.9 and l.get("ink_ratio")]
    small = [l for l in noncode if abs(l["est_font_size_px"] - scale["body"]) / scale["body"] < 0.2 and l.get("ink_ratio")]
    weights = {"display": 800, "h1": 700, "body": 500}
    if big and small:
        r = np.median([l["ink_ratio"] for l in big]) / max(1e-6, np.median([l["ink_ratio"] for l in small]))
        weights["display"] = 900 if r > 1.25 else 800 if r > 1.1 else 700 if r > 0.95 else 500
        weights["h1"] = min(900, weights["display"] - 100) if weights["display"] > 500 else 500
        P.set("typography.weights", "inferred", [{"ocr_line": l["text"]} for l in big[:3]], f"heading/body ink-coverage ratio = {r:.2f}",
              "weight from ink coverage is a rough guess; confirm on the contact sheet")
    else:
        P.set("typography.weights", "unknown", [], "default")
    vibe = []
    vibe.append("CJK 无衬线（黑体系）" if cjk_ratio > 0.2 else "拉丁无衬线")
    if code_found:
        vibe.append("技术感：代码块用等宽字体")
    fam_css_sans = '"Inter", "Noto Sans CJK SC", "Source Han Sans SC", "HarmonyOS Sans SC", sans-serif'
    fam = {
        "display": {"css": '"Inter Tight", "Noto Sans CJK SC", "Source Han Sans SC", sans-serif', "vibe": "粗黑几何无衬线（推测）",
                    "free_substitutes": FREE_FONTS["sans_latin"] + FREE_FONTS["sans_cjk"],
                    "license_note": "只用开源/免费可商用替代字体，不复制参考片的字体文件"},
        "body": {"css": fam_css_sans, "vibe": "中性无衬线（推测）", "free_substitutes": FREE_FONTS["sans_cjk"] + FREE_FONTS["sans_latin"]},
        "mono": {"css": '"JetBrains Mono", "Noto Sans Mono CJK SC", monospace', "vibe": "等宽代码字体", "free_substitutes": FREE_FONTS["mono"]},
    }
    P.set("typography.families", "unknown", [], "font identity cannot be measured from pixels",
          "families are free substitutes chosen by vibe; original font name is UNKNOWN — confirm vibe on contact sheet")
    P.set("typography.vibe", "inferred", [], "OCR script mix + code detection")
    P.set("typography.letter_spacing_em", "unknown", [], "default")
    P.set("typography.line_height", "unknown", [], "default")
    return {"vibe": "；".join(vibe), "families": fam, "scale_px": scale, "weights": weights, "letter_spacing_em": -0.01, "line_height": 1.35}


# ---------------------------------------------------------------------------------------------

def detect_grid_lines(img, bg_rgb):
    lab = srgb_to_lab(img.reshape(-1, 3)).reshape(img.shape)
    ref = np.median(lab.reshape(-1, 3), axis=0)  # this frame's own background (encoder shifts colours slightly)
    d = np.sqrt(((lab - ref) ** 2).sum(-1))
    faint = (d > 2.5) & (d < 15)
    rows = faint.mean(1) > 0.45
    cols = faint.mean(0) > 0.45
    def periodic(v):
        idx = np.where(v)[0]
        if len(idx) < 4:
            return None
        gaps = np.diff(idx)
        gaps = gaps[gaps > 2]
        if len(gaps) < 3:
            return None
        g = np.median(gaps)
        return float(g) if (np.abs(gaps - g) <= 2).mean() > 0.6 else None
    return periodic(rows), periodic(cols)


def corner_radius(img, box, surf_rgb):
    x, y, w, h = box
    reg = img[y:y + h, x:x + w].astype(int)
    m = (np.abs(reg - np.array(surf_rgb)).max(-1) < 14).astype(np.uint8)
    ys, xs = np.where(m)
    if len(xs) == 0:
        return None
    # tight bbox of the panel itself (layout boxes include drop shadows)
    x, y = x + int(xs.min()), y + int(ys.min())
    w = int(xs.max() - xs.min())
    h = int(ys.max() - ys.min())
    for d in range(0, min(w, h) // 2):
        px = img[min(img.shape[0] - 1, y + d), min(img.shape[1] - 1, x + d)].astype(int)
        if np.abs(px - np.array(surf_rgb)).max() < 14:
            return round(d / (1 - 1 / np.sqrt(2)))
    return None


def distill_layout(A, P, pal):
    L = A.get("layout", {})
    W, H = A["source"]["width"], A["source"]["height"]
    kfs = [s["keyframes"]["settled"]["path"] for s in A["scenes"]]
    ev = [ev_frame(p) for p in kfs[:4]]
    out = {}
    if "margins_pct" in L:
        m = L["margins_pct"]
        align = L.get("dominant_alignment", "left")
        left = m["left"] if m["left"] > 1 else 6
        right = left if align == "left" else m["right"]
        vert = float(np.clip(m["bottom"], 4, 15))
        out["margins_pct"] = {"left": round(left, 2), "right": round(right, 2), "top": round(vert, 2), "bottom": round(vert, 2)}
        P.set("layout.margins_pct.left", "seen", ev, "5th percentile of foreground-box left edges")
        P.set("layout.margins_pct.right", "inferred" if align == "left" else "seen", ev,
              "mirrored from left (content does not reach right edge)" if align == "left" else "95th pct right edge")
        P.set("layout.margins_pct.top", "inferred", ev, "clipped bottom margin; vertical centring assumed")
        P.set("layout.margins_pct.bottom", "seen", ev, "lowest foreground edge (subtitle)")
        out["alignment"] = align
        P.set("layout.alignment", "inferred", ev, f"left-aligned boxes {L.get('left_aligned_box_ratio')}, centred {L.get('centered_box_ratio')}")
        out["safe_area_pct"] = L.get("safe_area_pct_estimate")
        P.set("layout.safe_area_pct", "inferred", ev, "min(margins)")
        out["grid"] = {"columns": L.get("grid_columns_guess"), "gutter_pct": 2.0, "fit_ratio": L.get("grid_fit_ratio")}
        P.set("layout.grid", "inferred", ev, "best-fit column grid to box left edges", "gutter is a default")
        out["common_left_edges_px"] = L.get("common_left_edges_px")
    else:
        out["margins_pct"] = {"left": 8, "right": 8, "top": 10, "bottom": 10}
        out["alignment"] = "left"
        P.set("layout.margins_pct", "unknown", [], "no foreground boxes")
        P.set("layout.alignment", "unknown", [], "default")
    img = cv2.cvtColor(cv2.imread(kfs[0]), cv2.COLOR_BGR2RGB)
    gr, gc = detect_grid_lines(img, hex_to_rgb(pal["bg"]))
    out["decor"] = {"grid_lines": bool(gr or gc), "glow": False, "noise": False}
    P.set("layout.decor.grid_lines", "seen" if (gr or gc) else "inferred", [ev_frame(kfs[0])],
          "rows/cols of faint (ΔE 1.2–12) pixels repeating at a regular period", f"period≈{gr or gc}px" if (gr or gc) else "none found")
    P.set("layout.decor.glow", "unknown", [], "radial glow not measured automatically — check contact sheet")
    P.set("layout.decor.noise", "unknown", [], "film grain/noise not measured")
    out["radius_px"] = 16
    P.set("layout.radius_px", "unknown", [], "default")
    for sf in L.get("surfaces", []):
        kp = os.path.join(A["files"]["keyframes_dir"], sf["frame"])
        r = corner_radius(cv2.cvtColor(cv2.imread(kp), cv2.COLOR_BGR2RGB), sf["box"], sf["rgb"])
        if r:
            out["radius_px"] = int(r)
            P.set("layout.radius_px", "seen", [{"frame": kp, "box": sf["box"]}], "diagonal scan from panel corner to first surface pixel")
            break
    return out


# ---------------------------------------------------------------------------------------------

def typing_span(video, t0, t1, box, surf_rgb, fps=15):
    """seconds between 5% and 97% of final ink inside the code panel (typewriter span)."""
    import subprocess
    x, y, w, h = box
    cmd = ["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-t", f"{t1 - t0:.3f}", "-i", video,
           "-vf", f"crop={w}:{h}:{x}:{y},fps={fps},scale={max(2, w // 4 * 2 // 2)}:-2", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.run(cmd, capture_output=True)
    sw = max(2, w // 4 * 2 // 2)
    sh = int(round(h * sw / w / 2) * 2)
    buf = np.frombuffer(p.stdout, np.uint8)
    n = len(buf) // (sw * sh * 3)
    if n < 5:
        return None
    fr = buf[: n * sw * sh * 3].reshape(n, sh, sw, 3).astype(int)
    ink = (np.abs(fr - np.array(surf_rgb)).max(-1) > 60).mean((1, 2))
    from scipy.ndimage import median_filter
    ink = median_filter(ink, size=5)
    final = ink.max()
    if final <= 0:
        return None
    a = np.argmax(ink > 0.05 * final)
    b = np.argmax(ink >= 0.97 * final)
    return (b - a) / fps if b > a else None


def easings_keyframes(m):
    """dea-style motion block (structure idea: obaid1dev/dea, MIT): named CSS easings + keyframe tracks."""
    b = m["easing"]["enter"]["cubic_bezier"]
    css = lambda v: f"cubic-bezier({v[0]}, {v[1]}, {v[2]}, {v[3]})"
    sp = m["spring"]
    easings = {"enter": css(b), "exit": css(m["easing"]["exit"]["cubic_bezier"]), "emphasis": css(m["easing"]["emphasis"]["cubic_bezier"]),
               "spring": f"spring(damping={sp['damping']}, stiffness={sp['stiffness']}, mass={sp['mass']})"}
    d = m["enter_distance_px"]

    def track(style):
        if style == "slide-up":
            return [{"offset": 0, "opacity": 0, "transform": f"translateY({d}px)"}, {"offset": 1, "opacity": 1, "transform": "translateY(0)"}]
        if style == "slide-left":
            return [{"offset": 0, "opacity": 0, "transform": f"translateX({d}px)"}, {"offset": 1, "opacity": 1, "transform": "translateX(0)"}]
        if style == "scale":
            return [{"offset": 0, "opacity": 0, "transform": "scale(0.85)"}, {"offset": 1, "opacity": 1, "transform": "scale(1)"}]
        if style == "spring-pop":
            return [{"offset": 0, "opacity": 0, "transform": "scale(0.6)"}, {"offset": 0.6, "opacity": 1, "transform": "scale(1.06)"},
                    {"offset": 1, "opacity": 1, "transform": "scale(1)"}]
        return [{"offset": 0, "opacity": 0}, {"offset": 1, "opacity": 1}]
    t = m["transition"]["type"]
    tr = {"slide": [{"offset": 0, "transform": "translateX(100%)"}, {"offset": 1, "transform": "translateX(0)"}],
          "wipe": [{"offset": 0, "clipPath": "inset(0 100% 0 0)"}, {"offset": 1, "clipPath": "inset(0 0 0 0)"}],
          "zoom": [{"offset": 0, "opacity": 0, "transform": "scale(1.15)"}, {"offset": 1, "opacity": 1, "transform": "scale(1)"}],
          "fade": [{"offset": 0, "opacity": 0}, {"offset": 1, "opacity": 1}], "cut": []}.get(t, [])
    kf = {"enter": {"duration_s": m["durations_s"]["base"], "easing": "enter", "frames": track(m["enter_style"])},
          "title_enter": {"duration_s": m["durations_s"]["slow"], "easing": "spring" if m["title_enter_style"] == "spring-pop" else "enter",
                          "frames": track(m["title_enter_style"])},
          "transition_in": {"duration_s": m["transition"]["duration_s"], "easing": "enter", "frames": tr},
          "typewriter": {"chars_per_s": m["typing_cps"], "caret_blink_s": 0.5}}
    return easings, kf


def font_table(typo):
    rows = []
    for role, fam in typo["families"].items():
        subs = fam.get("free_substitutes", [])
        rows.append({"role": role, "observed_vibe": fam.get("vibe"), "original_font": "unknown",
                     "substitute": fam["css"].split(",")[0].strip('" '), "license": "SIL OFL 1.1" if "Noto" in fam["css"] or "Inter" in fam["css"] or "JetBrains" in fam["css"] else "check",
                     "alternatives": subs[:4], "size_px": typo["scale_px"].get({"display": "display", "body": "body", "mono": "code"}[role]),
                     "adjust": "先对照参考关键帧调字号/字距/字重，再确认许可证；不得使用参考片的字体文件"})
    return rows


ENTRY_MAP = {"slide-up": "slide-up", "slide-down": "slide-up", "slide-left": "slide-left", "slide-right": "slide-left",
             "scale-in": "scale", "scale-out": "scale", "fade": "fade", "fade/mixed": "fade"}


def distill_motion(A, P, comps):
    M = A["motion"]
    ev_all = M["events"]
    non = [e for e in ev_all if not e["is_transition"]]
    tr = [e for e in ev_all if e["is_transition"]]
    efile = {"file": A["files"]["motion_energy_csv"]}

    def evs(es):
        return [efile] + [{"tc": e["start_tc"], "event_duration_s": e["duration_s"]} for e in es[:6]]
    tiers = M.get("duration_tiers_s") or []
    if len(tiers) >= 3:
        d = {"fast": tiers[0], "base": tiers[1], "slow": tiers[2]}
    elif len(tiers) == 2:
        d = {"fast": tiers[0], "base": tiers[1], "slow": round(tiers[1] * 1.6, 3)}
    elif len(tiers) == 1:
        d = {"fast": round(tiers[0] * 0.6, 3), "base": tiers[0], "slow": round(tiers[0] * 1.6, 3)}
    else:
        d = {"fast": 0.25, "base": 0.5, "slow": 0.9}
    d = {k: float(np.clip(v, 0.08, 3.0)) for k, v in d.items()}
    P.set("motion.durations_s", "seen" if tiers else "unknown", evs(non), "1-D k-means of motion-event durations (frame-diff threshold)",
          "event length excludes the sub-threshold tail of ease-out curves → real tween may be ~10–25% longer")
    fam = M.get("dominant_easing_guess")
    entry_like = [e for e in non if e.get("easing_guess") in ("ease-out", "spring", "ease-in-out") and e.get("bezier_rmse", 1) < 0.08]
    bez = np.median([e["cubic_bezier_fit"] for e in entry_like], axis=0).round(2).tolist() if entry_like else None
    if not bez:
        bez = [0.16, 1, 0.3, 1]
        P.set("motion.easing.enter", "unknown", [], "default ease-out")
    else:
        bez = [float(np.clip(bez[0], 0, 1)), float(bez[1]), float(np.clip(bez[2], 0, 1)), float(bez[3])]
        P.set("motion.easing.enter", "inferred", evs(entry_like), "least-squares cubic-bezier fit to cumulative optical-flow speed per event (median)")
    easing = {"family_guess": fam, "enter": {"cubic_bezier": bez}, "exit": {"cubic_bezier": [0.7, 0, 0.84, 0]},
              "emphasis": {"cubic_bezier": [0.34, 1.56, 0.64, 1]}}
    P.set("motion.easing.family_guess", "inferred", evs(non), "velocity-profile peak position / oscillation")
    P.set("motion.easing.exit", "unknown", [], "exits not separately measured")
    P.set("motion.easing.emphasis", "unknown", [], "default overshoot")
    # entrance style
    votes = {}
    for e in non:
        k = ENTRY_MAP.get(e.get("entry_type_guess"), "fade")
        if e.get("entry_type_guess") == "slide-right" and e.get("velocity_source", "").startswith("optical"):
            continue  # left→right growth (bars/typing) is not an entrance
        votes.setdefault(k, []).append(e)
    enter_style = max(votes, key=lambda k: len(votes[k])) if votes else "fade"
    P.set("motion.enter_style", "inferred" if votes else "unknown", evs(votes.get(enter_style, [])), "majority optical-flow direction of entrance events")
    first = [e for e in non if e["start_s"] < A["scenes"][0]["end_s"]]
    title_style = "spring-pop" if first and first[0].get("easing_guess") == "spring" else enter_style
    P.set("motion.title_enter_style", "inferred", evs(first[:1]), "easing family of first event in scene 0")
    stagger = A["rhythm"].get("stagger_median_s")
    P.set("motion.stagger_s", "inferred" if stagger else "unknown", evs(non), "median interval between entrance onsets within a scene")
    # transition
    if tr:
        tv = {}
        for e in tr:
            g = e.get("entry_type_guess", "fade")
            t = "slide" if g.startswith("slide") else "zoom" if g.startswith("scale") else "fade"
            tv.setdefault(t, []).append(e)
        ttype = max(tv, key=lambda k: len(tv[k]))
        tdur = float(np.clip(M.get("transition_core_duration_median_s") or 0.5, 0.15, 1.5))
        P.set("motion.transition.type", "inferred", evs(tr), "optical-flow direction during events spanning a cut",
              "wipe vs fade cannot be told apart by flow; check keyframes")
        P.set("motion.transition.duration_s", "seen", evs(tr), "frames with energy ≥20% of peak around the cut")
    else:
        ttype, tdur = "cut", 0.0
        P.set("motion.transition", "inferred", [], "no motion around detected cuts → hard cuts")
    spring = {"damping": 12, "stiffness": 140, "mass": 1}
    P.set("motion.spring", "inferred" if fam == "spring" or title_style == "spring-pop" else "unknown", [], "generic under-damped spring; not fitted")
    enter_dist = round(40 * A["source"]["height"] / 1080)
    P.set("motion.enter_distance_px", "unknown", [], "default (flow magnitude not converted to distance)")
    # typing speed from code scenes
    cps = 28
    code_sc = next((c for c in comps if c["type"] == "code_block"), None)
    if code_sc:
        s = A["scenes"][code_sc["scenes"][0]]
        chars = sum(len(l["text"]) for l in A["ocr"].get("lines", []) if l["scene"] == s["index"] and l.get("codey"))
        evs_in = [e for e in non if s["start_s"] <= e["start_s"] < s["end_s"]]
        quiet_t = s["keyframes"]["settled"]["time_s"]
        span = max(0.5, (max([e["end_s"] for e in evs_in], default=quiet_t) - s["start_s"]) - d["base"])
        sf = [x for x in A.get("layout", {}).get("surfaces", []) if x["frame"] == os.path.basename(s["keyframes"]["settled"]["path"])]
        if sf:
            inl = [l for l in A["ocr"].get("lines", []) if l["scene"] == s["index"] and _inside(l["bbox"], sf[0]["box"])
                   and l["bbox"][1] > sf[0]["box"][1] + sf[0]["box"][3] * 0.15]  # skip the window title bar
            chars = max(chars, sum(len(l["text"]) for l in inl))
            ts = typing_span(A["source"]["path"], s["start_s"], s["end_s"], sf[0]["box"], sf[0]["rgb"])
            if ts:
                span = ts
        if chars > 10:
            cps = round(chars / span, 1)
            P.set("motion.typing_cps", "inferred", [{"tc": s["start_tc"], "chars_ocr": chars, "typing_span_s": round(span, 2)}],
                  "OCR code chars / ink-growth span inside code panel (5%→97% of final ink)", "OCR misses characters → value is likely LOW")
    if "motion.typing_cps" not in P.d:
        P.set("motion.typing_cps", "unknown", [], "default")
    return {"durations_s": {k: round(v, 3) for k, v in d.items()}, "easing": easing, "spring": spring,
            "enter_style": enter_style, "title_enter_style": title_style, "enter_distance_px": enter_dist,
            "stagger_s": round(float(stagger), 3) if stagger else 0.15,
            "transition": {"type": ttype, "duration_s": round(tdur, 3)}, "typing_cps": cps}


# ---------------------------------------------------------------------------------------------

NUM_RE = re.compile(r"^[+\-$¥€]?\d[\d.,]*\s*[%xX万亿kKmMB+]?$")


def detect_components(A, P, pal):
    W, H = A["source"]["width"], A["source"]["height"]
    lines = A.get("ocr", {}).get("lines", []) if A.get("ocr", {}).get("available") else []
    scenes = A["scenes"]
    comps = []
    body_sizes = [l["est_font_size_px"] for l in lines if not l.get("codey")]
    body = float(np.median(body_sizes)) if body_sizes else H * 0.04

    def add(t, sc, evidence, conf, params=None):
        seg, ui, v = TAXO[t]
        comps.append({"type": t, "template_segment": seg, "scenes": sorted(set(sc)), "evidence": evidence,
                      "confidence": round(conf, 2), "taxonomy": {"ui": ui, "video": v, "source": TAXO_SRC,
                                   "verified": bool(TAXO_SRC) and all(i in TAXO_IDS for i in ui + v),
                                   "names": {i: TAXO_IDS.get(i, "UNVERIFIED") for i in ui + v}}, "params": params or {}})

    # subtitle bar
    subs = [l for l in lines if l["pos_pct"]["y"] > 78 and abs(l["pos_pct"]["cx"] - 50) < 6]
    sub_scenes = sorted(set(l["scene"] for l in subs))
    if len(sub_scenes) >= max(1, len(scenes) // 2):
        lb = [l.get("local_bg") for l in subs if l.get("local_bg")]
        params = {}
        if lb:
            params = {"bg": max(set(lb), key=lb.count), "color": subs[0]["ink_colors"][0]["hex"] if subs[0].get("ink_colors") else None,
                      "position": "bottom", "y_pct": round(float(np.median([l["pos_pct"]["y"] for l in subs])), 1)}
        add("subtitle_bar", sub_scenes, f"centred OCR lines at y>78% in {len(sub_scenes)}/{len(scenes)} scenes, e.g. '{subs[0]['text']}'", 0.8, params)
    sub_ids = {id(l) for l in subs}
    body_lines = [l for l in lines if id(l) not in sub_ids]
    surfs = A.get("layout", {}).get("surfaces", [])
    for s in scenes:
        sl = [l for l in body_lines if l["scene"] == s["index"]]
        evs = [e for e in A["motion"]["events"] if s["start_s"] <= e["start_s"] < s["end_s"] and not e["is_transition"]]
        kf = s["keyframes"]["settled"]["path"]
        # knowledge components first (their panels are surfaces and would look like code blocks)
        hit = None
        for t, fn in (("evidence_frame", lambda: CD.detect_evidence(kf, pal["bg"])),
                      ("compare_columns", lambda: CD.detect_compare(kf, pal.get("surface", pal["bg"]))),
                      ("flow_chart", lambda: CD.detect_flow(kf, pal.get("surface", pal["bg"]), pal["bg"])),
                      ("timeline", lambda: CD.detect_timeline(kf, pal["bg"]))):
            try:
                prm = fn()
            except Exception as ex:  # a detector bug must not kill the whole distill
                print(f"[distill] detector {t} failed on {os.path.basename(kf)}: {ex}")
                prm = None
            if prm:
                hit = (t, prm)
                break
        if hit:
            t, prm = hit
            add(t, [s["index"]], f"{t} pixel detector on {os.path.basename(kf)} @ {s['start_tc']}: {json.dumps(prm, ensure_ascii=False)[:160]}", 0.75, prm)
            continue
        # code block
        sf = [x for x in surfs if x["frame"] == os.path.basename(kf)]
        codey = [l for l in sl if l.get("codey")]
        if sf and (codey or len([l for l in sl if any(_inside(l["bbox"], x["box"]) for x in sf)]) >= 2):
            add("code_block", [s["index"]], f"uniform panel {sf[0]['hex']} + {len(codey)} code-like OCR lines @ {s['start_tc']}", 0.8 if codey else 0.55)
            continue
        # bars: rectangles filled with chromatic palette colours
        bars = find_bars(kf, [pal["primary"], pal["accent"]] + pal.get("extra", []), W, H)
        if len(bars) >= 2:
            add("bar_chart", [s["index"]], f"{len(bars)} aligned solid rectangles in {os.path.basename(kf)}", 0.75, {"bars": bars[:8]})
            continue
        nums = [l for l in sl if NUM_RE.match(l["text"].replace(" ", "")) and l["est_font_size_px"] > body * 1.6]
        if nums:
            add("number_counter", [s["index"]], f"large numeric OCR '{nums[0]['text']}' ({nums[0]['est_font_size_px']}px) @ {s['start_tc']}", 0.7)
            continue
        if len(sl) >= 3:
            sizes = sorted(l["est_font_size_px"] for l in sl)
            similar = [l for l in sl if abs(l["est_font_size_px"] - np.median(sizes)) / np.median(sizes) < 0.2]
            lefts = [l["bbox"][0] for l in similar]
            if len(similar) >= 2 and np.std(lefts) < W * 0.04:
                add("bullet_list", [s["index"]], f"{len(similar)} stacked same-size lines, left x≈{int(np.median(lefts))}px, {len(evs)} staggered entrances @ {s['start_tc']}",
                    0.7 if len(evs) >= 2 else 0.5)
                continue
        if len(sl) <= 3 and (s["index"] == 0 or any(l["est_font_size_px"] > body * 1.8 for l in sl)):
            add("title_card", [s["index"]], f"≤3 text lines with large heading @ {s['start_tc']}", 0.6)
            continue
        if s["index"] == 0:
            add("title_card", [0], "first scene (fallback)", 0.4)
    # keyword highlight
    hi = [l for l in body_lines if l.get("ink_colors") and len(l["ink_colors"]) >= 2
          and any(not is_neutral(c["hex"], 25) and c["ratio"] > 0.12 for c in l["ink_colors"])
          and any(is_neutral(c["hex"], 25) and c["ratio"] > 0.2 for c in l["ink_colors"])]
    if hi:
        add("keyword_highlight", [l["scene"] for l in hi], f"{len(hi)} OCR lines mixing neutral + chromatic ink, e.g. '{hi[0]['text']}'", 0.65,
            {"syntax": "use **keyword** in script.json text"})
    eb = A.get("layout", {}).get("edge_bars", [])
    if len(eb) >= 2 and len(set(b[2] for b in eb)) >= 2:
        add("progress_bar", [], f"{len(eb)} thin edge bars with growing widths {[b[2] for b in eb][:5]}", 0.7,
            {"position": "top" if np.median([b[1] for b in eb]) < H / 2 else "bottom"})
    tr = [e for e in A["motion"]["events"] if e["is_transition"]]
    if tr:
        add("transition", [], f"{len(tr)} motion events straddling cuts at {[e['start_tc'] for e in tr][:4]}", 0.7)
    return comps


def knowledge_style(key, found, pal, layout, motion):
    """components_style.<key>: measured params when the reference shows the component, else defaults
    derived from palette / motion / layout (status unknown)."""
    base = motion["durations_s"]["base"]
    stg = motion.get("stagger_s", 0.4)
    D = {
        "evidence": {"frame_color": pal["text"], "frame_stroke_px": 3, "radius_px": layout.get("radius_px", 12), "highlight_color": pal["accent"],
                     "highlight_stroke_px": 6, "source_color": pal.get("text_muted", pal["text"]), "zoom_scale": 1.12, "enter_s": base,
                     "highlight_delay_s": 0.9},
        "timeline": {"line_color": pal.get("text_muted", pal["text"]), "line_px": 4, "node_color": pal["primary"], "node_size_px": 28,
                     "date_color": pal["primary"], "label_color": pal["text"], "enter_stagger_s": max(stg, 0.25), "enter_s": base},
        "compare": {"panel_fill": pal.get("surface", pal["bg"]), "title_color": pal["accent"], "gap_pct": 4, "radius_px": layout.get("radius_px", 12),
                    "highlight_color": pal["primary"], "enter_stagger_s": max(stg * 0.6, 0.2), "enter_s": base},
        "flow": {"node_fill": pal.get("surface", pal["bg"]), "node_stroke": pal["primary"], "node_stroke_px": 3, "radius_px": layout.get("radius_px", 12),
                 "arrow_color": pal.get("text_muted", pal["text"]), "arrow_px": 4, "step_s": max(stg, 0.35), "enter_s": base, "orientation": "horizontal"},
    }[key]
    if not found:
        return D, "unknown", []
    p = {}
    for c in found:  # merge across detections: a scene caught before the highlight/annotation appeared lacks those keys
        for k, v in c["params"].items():
            if p.get(k) in (None, 0):
                p[k] = v
    keep = {"evidence": ["frame_color", "highlight_color", "highlight_stroke_px"],
            "timeline": ["line_color", "line_px", "node_color", "node_size_px"],
            "compare": ["panel_fill", "gap_pct", "radius_px", "highlight_color"],
            "flow": ["node_fill", "node_stroke", "arrow_color", "radius_px", "orientation"]}[key]
    out = dict(D)
    for k in keep:
        if p.get(k) not in (None, 0):
            out[k] = p[k]
    if key == "timeline":
        out["date_color"] = out["node_color"]
    for k in ("node_count", "box_pct", "highlight_box_pct", "line_span_pct", "panel_w_pct", "node_w_pct"):
        if k in p:
            out.setdefault("measured", {})[k] = p[k]
    return out, "seen", [{"evidence": c["evidence"]} for c in found[:3]]


def find_bars(png, hexes, W, H):
    img = cv2.cvtColor(cv2.imread(png), cv2.COLOR_BGR2RGB)
    small = img[::2, ::2]
    lab = srgb_to_lab(small.reshape(-1, 3)).reshape(small.shape)
    out = []
    for hx in hexes:
        d = np.sqrt(((lab - srgb_to_lab(np.array(hex_to_rgb(hx), float))) ** 2).sum(-1))
        m = (d < 10).astype(np.uint8)
        n, _, st, _ = cv2.connectedComponentsWithStats(m)
        for i in range(1, n):
            x, y, w, h, a = st[i]
            if w * 2 > W * 0.03 and H * 0.012 < h * 2 < H * 0.15 and a / (w * h) > 0.85 and w > h * 1.5:
                out.append([int(x * 2), int(y * 2), int(w * 2), int(h * 2)])
    out.sort(key=lambda b: b[1])
    lefts = [b[0] for b in out]
    if len(out) >= 2 and np.std(lefts) > W * 0.02:
        med = np.median(lefts)
        out = [b for b in out if abs(b[0] - med) < W * 0.02]
    return out


# ---------------------------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("analysis_dir")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--name", required=True, help="style name, lowercase-kebab, e.g. paper-terminal")
    ap.add_argument("--overrides", help="JSON deep-merged on top (visual-review corrections)")
    ap.add_argument("--styles-dir", help="also store the style asset under <styles-dir>/<name>/")
    ap.add_argument("--taxonomy", help="motion taxonomy table (default: references/motion-taxonomy.md in the skill; env CVSD_TAXONOMY)")
    args = ap.parse_args()

    A = read_json(os.path.join(args.analysis_dir, "analysis.json"))
    global TAXO_SRC, TAXO_IDS
    tpath = args.taxonomy or os.environ.get("CVSD_TAXONOMY") or DEFAULT_TAXONOMY
    TAXO_IDS, terr = load_taxonomy(tpath)
    if terr:
        print(f"[distill] ERROR {terr} — component taxonomy ids will be marked UNVERIFIED", file=sys.stderr)
        TAXO_SRC = ""
    else:
        TAXO_SRC = os.path.abspath(tpath)
        bad = sorted({i for _, ui, v in TAXO.values() for i in ui + v} - set(TAXO_IDS))
        if bad:
            print(f"[distill] WARNING taxonomy ids used by the detector table but missing from {tpath}: {bad}", file=sys.stderr)
    P = Prov()
    meta = A["source"]
    ocr = A.get("ocr", {})
    canvas = {"width": meta["width"], "height": meta["height"], "fps": round(meta["fps"]), "aspect": meta["aspect"]}
    for k in ("width", "height", "fps"):
        P.set(f"canvas.{k}", "seen", [{"file": os.path.join(args.analysis_dir, "meta.json")}], "ffprobe")

    palette, corner_spread = distill_palette(A, P)
    comps = detect_components(A, P, palette)
    code_found = any(c["type"] == "code_block" for c in comps)
    typo = distill_typography(A, P, ocr.get("cjk_line_ratio", 0) if ocr.get("available") else 0, code_found)
    layout = distill_layout(A, P, palette)
    if corner_spread > 6:
        layout["decor"]["glow"] = True
        P.set("layout.decor.glow", "inferred", [], f"background corners differ by ΔE {corner_spread:.1f} → gradient/glow")
    motion = distill_motion(A, P, comps)
    R = A["rhythm"]
    au = A.get("audio") or {}
    sync = au.get("av_sync") or {}
    rhythm = {
        "shot_mean_s": R.get("shot_duration_mean_s"), "shot_median_s": R.get("shot_duration_median_s"),
        "motion_onset_interval_s": R.get("motion_onset_interval_median_s"), "visual_bpm": R.get("visual_bpm_estimate"),
        "audio_bpm": au.get("tempo_bpm_estimate"),
        "av_sync": {"rule": ("视觉事件起点对齐音频起音点（容差 80 ms）" if sync.get("match_ratio", 0) >= 0.5 else
                             "音画为松散同步：只有少数切点落在起音点上" if sync else "无音轨或未测"),
                    "match_ratio": sync.get("match_ratio"), "median_offset_ms": sync.get("median_offset_ms")},
        "entrance_events_per_min": entrance_density(A),
        "pacing_rule": (f"平均每 {R.get('shot_duration_mean_s')} s 一个镜头；镜头内元素约每 {R.get('stagger_median_s')} s 入场一个"
                        if R.get("shot_duration_mean_s") else "unknown"),
    }
    sc_ev = [{"file": A["files"]["scenes_csv"]}] + [{"tc": s["start_tc"]} for s in A["scenes"][1:6]]
    P.set("rhythm.shot_mean_s", "seen", sc_ev, "detected cuts")
    P.set("rhythm.shot_median_s", "seen", sc_ev, "detected cuts")
    if rhythm["entrance_events_per_min"] is not None:
        P.set("rhythm.entrance_events_per_min", "seen", [{"file": A["files"].get("motion_events_json", "analysis.json#motion.events")}],
              "non-transition motion events / duration × 60 (scripts/distill.py entrance_density)",
              "events are motion-energy bursts: simultaneous entrances inside one burst count once")
    else:
        P.set("rhythm.entrance_events_per_min", "unknown", [], "no motion events in analysis")
    P.set("rhythm.motion_onset_interval_s", "inferred", [{"file": A["files"]["motion_energy_csv"]}], "median interval between motion onsets")
    P.set("rhythm.visual_bpm", "inferred", [], "60 / onset interval folded into 60–180")
    if au.get("onsets_s") is not None:
        P.set("rhythm.audio_bpm", "inferred", [{"file": os.path.join(args.analysis_dir, "audio_onsets.csv")}], "spectral-flux autocorrelation")
        P.set("rhythm.av_sync", "seen", [{"pairs": sync.get("pairs", [])[:4]}], "nearest audio onset to each cut/entrance")
    else:
        P.set("rhythm.audio_bpm", "unknown", [], "no audio track")
        P.set("rhythm.av_sync", "unknown", [], "no audio track")
    P.set("rhythm.pacing_rule", "inferred", [], "summary of shot + stagger stats")

    comp_style = {"progress_bar": any(c["type"] == "progress_bar" for c in comps)}
    sub = next((c for c in comps if c["type"] == "subtitle_bar"), None)
    if sub and sub["params"].get("bg"):
        comp_style["subtitle"] = {"position": "bottom", "bg": sub["params"]["bg"], "bg_opacity": 1.0,
                                  "color": sub["params"].get("color") or "#FFFFFF"}
        P.set("components_style.subtitle", "seen", [{"evidence": sub["evidence"]}], "local background + ink of subtitle OCR lines")
    else:
        comp_style["subtitle"] = {"position": "bottom", "bg_opacity": 0.6}
        P.set("components_style.subtitle", "unknown", [], "default")
    P.set("components_style.progress_bar", "seen" if comp_style["progress_bar"] else "unknown", [], "edge-bar detection")
    for t, key in COMP_STYLE_KEY.items():
        comp_style[key], st, ev = knowledge_style(key, [c for c in comps if c["type"] == t], palette, layout, motion)
        P.set(f"components_style.{key}", st, ev, f"{t} pixel detector (scripts/components_detect.py)" if st == "seen" else
              "not detected in reference → default mapping from palette/motion/layout (unknown ≠ absent)")
    for i, c in enumerate(comps):
        P.set(f"components[{i}]:{c['type']}", "seen" if c["confidence"] >= 0.7 else "inferred", [{"evidence": c["evidence"]}], "heuristic detector",
              "taxonomy mapping is a manual table" + ("" if TAXO_SRC else " — taxonomy file NOT found, ids unverified"), confidence=c["confidence"])

    motion["easings"], motion["keyframes"] = easings_keyframes(motion)
    P.set("motion.easings", P.d.get("motion.easing.enter", {}).get("status", "unknown"), [], "CSS strings derived from motion.easing / spring",
          confidence=P.d.get("motion.easing.enter", {}).get("confidence", 0.2))
    P.set("motion.keyframes", "inferred", [], "keyframe tracks reconstructed from enter_style / transition type + measured durations")
    typo["font_substitutions"] = font_table(typo)
    P.set("typography.font_substitutions", "inferred", [], "vibe → free substitute table (references/font-alternatives.md)",
          "original font identity is UNKNOWN; never ship the original font file")
    tokens = {
        "name": args.name, "version": 1,
        "description": f"Style base distilled from {os.path.basename(meta['path'])}",
        "source": {"video": meta["path"], "analysis_dir": os.path.abspath(args.analysis_dir),
                   "distilled_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"), "duration_s": meta["duration_s"]},
        "canvas": canvas, "palette": palette, "typography": typo, "layout": layout, "motion": motion,
        "rhythm": rhythm, "components": comps, "components_style": comp_style,
    }
    manual = []
    if args.overrides:
        ov = read_json(args.overrides)
        ov_prov = ov.pop("_provenance", {})
        tokens = deep_merge(tokens, ov)
        for pth in flatten_paths(ov):
            manual.append(pth)
            # replace any provenance covering this path or its parent
            for k in list(P.d):
                if k == pth or pth.startswith(k + ".") or k.startswith(pth + "."):
                    P.d.pop(k)
            e = ov_prov.get(pth, {"status": "inferred", "method": "visual review (manual override)", "evidence": [{"file": os.path.abspath(args.overrides)}]})
            e.setdefault("confidence", {"seen": 0.9, "inferred": 0.6, "unknown": 0.2}.get(e.get("status"), 0.5))
            P.d[pth] = e
        # derived blocks must follow the overridden values
        tokens["motion"]["easings"], tokens["motion"]["keyframes"] = easings_keyframes(tokens["motion"])
        tokens["typography"]["font_substitutions"] = font_table(tokens["typography"])
    statuses = {}
    for v in P.d.values():
        statuses[v["status"]] = statuses.get(v["status"], 0) + 1
    tokens["provenance"] = dict(sorted(P.d.items()))
    tokens["unknowns"] = [{"path": k, "why": v.get("method", "")} for k, v in sorted(P.d.items()) if v["status"] == "unknown"]
    tokens["fidelity_notes"] = {
        "rule": "seen = measured from pixels/audio with evidence; inferred = derived by heuristic or visual judgement; unknown = not measured (≠ absent). Rule adapted from aicodeking/leanrea (MIT).",
        "status_counts": statuses,
        "measured": sorted(k for k, v in P.d.items() if v["status"] == "seen"),
        "inferred": sorted(k for k, v in P.d.items() if v["status"] == "inferred"),
        "defaults": sorted(k for k, v in P.d.items() if v["status"] == "unknown"),
        "needs_visual_review": [
            "typography.families / vibe: 用 Read 看 contact_sheet.png，判断字形气质（几何/人文/圆体/宋体/手写）并选免费替代",
            "typography.scale_px.display: 大标题经常读不出来，对照关键帧目测",
            "layout.decor: 背景网格、光斑、噪点、描边、阴影等装饰",
            "motion.transition.type: wipe/fade/slide 需看 entry/mid 关键帧确认",
            "components: 检测器漏掉的元件（图标、箭头、流程图、标注框…）",
        ],
        "manual_overrides": manual,
        "not_pixel_identical_because": ["原字体文件不复制，只用免费替代字体", "原素材/logo/角色不搬运", "随机种子、抗锯齿和编码损伤不可复原",
                                        "缓动曲线是从像素运动反推的近似"],
    }
    os.makedirs(args.out, exist_ok=True)
    outp = os.path.join(args.out, "style-tokens.json")
    write_json(outp, tokens)
    try:
        import jsonschema
        jsonschema.validate(tokens, read_json(SCHEMA))
        print("[distill] schema: valid")
    except ImportError:
        print("[distill] jsonschema not installed; skipped validation")
    except Exception as ex:
        print(f"[distill] SCHEMA ERROR: {str(ex)[:600]}")
        sys.exit(1)
    print(f"[distill] wrote {outp}  provenance: {statuses}")
    print(f"[distill] components: {[c['type'] for c in comps]}")

    if args.styles_dir:
        sd = os.path.join(args.styles_dir, args.name)
        refs = os.path.join(sd, "refs")
        os.makedirs(refs, exist_ok=True)
        shutil.copy(outp, os.path.join(sd, "style-tokens.json"))
        for k in ("contact_sheet", "motion_energy_png", "palette_png"):
            shutil.copy(A["files"][k], refs)
        for s in A["scenes"][:12]:
            shutil.copy(s["keyframes"]["settled"]["path"], refs)
        with open(os.path.join(sd, "README.md"), "w", encoding="utf-8") as f:
            f.write(style_readme(tokens, A))
        att = os.path.join(sd, "attribution.json")
        if not os.path.exists(att):  # template; export-index flags UNSPECIFIED until the user fills it
            write_json(att, {"source_label": "UNSPECIFIED", "reference_rights": "UNSPECIFIED",
                             "style_tokens_license": "UNSPECIFIED", "attribution": "",
                             "_help": "填写参考片来源标注与你拥有的权利（自有/授权），export-index 会读取；未填写时资源库清单标记 UNSPECIFIED"})
        print(f"[distill] style asset saved -> {sd}")


def style_readme(T, A):
    P = T["palette"]
    lines = [f"# 风格底座：{T['name']}", "",
             f"- 来源视频：`{T['source']['video']}`（{A['source']['width']}x{A['source']['height']} @ {A['source']['fps']}fps，{A['source']['duration_s']}s）",
             f"- 蒸馏时间：{T['source']['distilled_at']}",
             "- refs/ 里的关键帧只作内部比对参考，不得随模板或成片分发。", "",
             "## 色板", "", "| 角色 | HEX | 来源 |", "|---|---|---|"]
    for k in ("bg", "surface", "primary", "accent", "text", "text_muted", "code_text"):
        if k in P:
            lines.append(f"| {k} | `{P[k]}` | {T['provenance'].get('palette.' + k, {}).get('status', '?')} |")
    m = T["motion"]
    lines += ["", "## 动效", "", f"- 时长档位 {m['durations_s']}；入场 `{m['enter_style']}`，标题 `{m['title_enter_style']}`；错峰 {m['stagger_s']} s",
              f"- 缓动 cubic-bezier{tuple(m['easing']['enter']['cubic_bezier'])}（推测）；转场 {m['transition']}",
              "", "## 元件", ""]
    for c in T["components"]:
        lines.append(f"- {c['type']} → 模板段 `{c['template_segment']}`，分类 {c['taxonomy']['ui'] + c['taxonomy']['video']}（置信度 {c['confidence']}）")
    lines += ["", "## 来源统计", "", f"{T['fidelity_notes']['status_counts']}", "", "## 待目测补全", ""]
    lines += [f"- {x}" for x in T["fidelity_notes"]["needs_visual_review"]]
    return "\n".join(lines) + "\n"


TAXO_SRC = ""
TAXO_IDS = {}


def entrance_density(A):
    """入场事件密度（次/分钟）= 非转场运动事件数 / 时长(分钟)."""
    ev = (A.get("motion") or {}).get("events")
    dur = (A.get("source") or {}).get("duration_s") or 0
    if ev is None or dur <= 0:
        return None
    n = sum(1 for e in ev if not e.get("is_transition"))
    return round(n / (dur / 60.0), 2)

if __name__ == "__main__":
    main()
