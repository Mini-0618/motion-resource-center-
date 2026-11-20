#!/usr/bin/env python3
"""analyze.py — measure a (code-generated) motion video.

Usage:
  analyze.py <video> -o <analysis_dir> [--sample-fps 30] [--scene-threshold 0.30] [--no-ocr] [--ocr-lang chi_sim+eng]

Outputs (in analysis_dir):
  analysis.json            everything below in one machine-readable file
  meta.json                ffprobe metadata
  scenes.csv               scene cuts with timecodes
  keyframes/*.png          per-scene keyframes (entry / mid / settled), full resolution
  contact_sheet.png        all scenes x 3 keyframes, labelled with timecodes
  motion_energy.csv/.png   frame-difference motion energy curve + detected motion events
  palette_global.png       global palette swatches
  ocr/*.tsv                raw tesseract output (if OCR available)
  audio.wav, audio_envelope.csv/.png, audio_onsets.csv   (if audio track)
  videomd/VIDEO.md         optional VIDEO.md v1 breakdown package (spec: videomd/videomd, CC BY 4.0)
Every derived number is tagged in analysis.json as measured / inferred.
"""
import argparse
import csv
import os
import shutil
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cvsd_common import (ffprobe, extract_frame, tc, kmeans_palette, srgb_to_lab, delta_e2000,  # noqa: E402
                         rgb_to_hex, contrast_ratio, chroma, write_json, run)

import matplotlib  # noqa: E402
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ANALYSIS_W = 480  # width used for motion / scene analysis


# ------------------------------------------------------------------ decoding

def decode_frames(video, sample_fps, width=ANALYSIS_W):
    """Decode downscaled RGB frames at sample_fps via ffmpeg pipe. returns (frames uint8 [N,H,W,3], times)."""
    meta = ffprobe(video)
    w = width
    h = int(round(meta["height"] * w / meta["width"] / 2) * 2)
    cmd = ["ffmpeg", "-v", "error", "-i", video, "-vf", f"fps={sample_fps},scale={w}:{h}:flags=area",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    import subprocess
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode()[-1500:])
    buf = np.frombuffer(p.stdout, dtype=np.uint8)
    n = len(buf) // (w * h * 3)
    frames = buf[: n * w * h * 3].reshape(n, h, w, 3)
    times = np.arange(n) / sample_fps
    return frames, times


# ------------------------------------------------------------------ scenes

def hsv_hist(fr):
    hsv = cv2.cvtColor(fr, cv2.COLOR_RGB2HSV)
    hist = cv2.calcHist([hsv], [0, 1, 2], None, [16, 6, 6], [0, 180, 0, 256, 0, 256])
    cv2.normalize(hist, hist)
    return hist


def detect_scenes(frames, times, fps, threshold=0.30, min_len_s=0.5, bg_rgb=None):
    """Two signals, max-combined:
    (a) histogram/pixel change over a ~0.33s lag (photographic cuts, full-frame changes)
    (b) 'foreground replaced' ratio: share of the earlier frame's foreground pixels (≠ background) that changed.
        Build-ups inside one scene (bullets appearing, code typing, bars growing) only ADD foreground,
        so (b) stays low; a real scene change replaces existing foreground, so (b) jumps."""
    n = len(frames)
    grays = np.stack([cv2.cvtColor(f, cv2.COLOR_RGB2GRAY) for f in frames]).astype(np.int16)
    if bg_rgb is not None:
        fg = np.stack([np.sqrt(((f.astype(np.int32) - np.array(bg_rgb)) ** 2).sum(-1)) > 30 for f in frames])
    else:
        fg = None
    npx = grays[0].size
    hists = [hsv_hist(f) for f in frames]
    k = max(1, int(round(0.33 * fps)))
    score = np.zeros(n)
    for i in range(1, n):
        j = max(0, i - k)
        hd = cv2.compareHist(hists[i], hists[j], cv2.HISTCMP_BHATTACHARYYA)
        changed = float((np.abs(grays[i] - grays[j]) > 25).mean())
        hd1 = cv2.compareHist(hists[i], hists[i - 1], cv2.HISTCMP_BHATTACHARYYA)
        changed1 = float((np.abs(grays[i] - grays[i - 1]) > 25).mean())
        sc = max(0.5 * hd + changed, 0.5 * hd1 + changed1 * 1.5)
        if fg is not None:
            fj = fg[j]
            nfg = int(fj.sum())
            if nfg > npx * 0.01:
                ch = np.abs(grays[i] - grays[j]) > 25
                replaced = float((fj & ch).sum()) / nfg
                big = float((fj & ch).sum()) / npx
                sc = max(sc, replaced * min(1.0, big / 0.03) * 0.6 / 0.5)  # replaced>=0.5 of fg & >=3% of frame -> ~threshold*2
        score[i] = sc
    cuts = []
    min_gap = int(round(min_len_s * fps))
    # candidate = local maxima of score above threshold; non-max suppression
    cand = [i for i in range(1, n) if score[i] >= threshold and score[i] == score[max(0, i - k):min(n, i + k + 1)].max()]
    for i in sorted(cand, key=lambda i: -score[i]):
        if all(abs(i - c) >= min_gap for c in cuts) and i >= min_gap and (n - i) >= min_gap // 2:
            cuts.append(i)
    cuts.sort()
    # Within a window-lag the max lands at the *end* of a gradual transition; shift back to its start
    refined = []
    for c in cuts:
        s = c
        while s - 1 > 0 and score[s - 1] > threshold * 0.5 and c - s < k:
            s -= 1
        refined.append(s)
    bounds = [0] + refined + [n]
    scenes = []
    for a, b in zip(bounds[:-1], bounds[1:]):
        if b <= a:
            continue
        scenes.append({"index": len(scenes), "start_f": int(a), "end_f": int(b),
                       "start_s": round(float(times[a]), 3), "end_s": round(float(times[b - 1] + 1 / fps), 3)})
    for s in scenes:
        s["duration_s"] = round(s["end_s"] - s["start_s"], 3)
        s["start_tc"] = tc(s["start_s"])
        s["end_tc"] = tc(s["end_s"])
    return scenes, score


# ------------------------------------------------------------------ motion

def motion_energy(frames):
    g = np.stack([cv2.cvtColor(f, cv2.COLOR_RGB2GRAY) for f in frames]).astype(np.float32)
    e = np.zeros(len(g))
    area = np.zeros(len(g))
    e[1:] = np.abs(np.diff(g, axis=0)).mean(axis=(1, 2)) / 255.0
    area[1:] = (np.abs(np.diff(g, axis=0)) > 12).mean(axis=(1, 2))
    return e, area


def bezier_fit(progress_x, progress_y):
    """grid-search cubic-bezier(x1,y1,x2,y2) best fitting y(x). returns (params, rmse)."""
    s = np.linspace(0, 1, 60)
    x1 = np.arange(0, 1.01, 0.05)
    y1 = np.arange(0, 1.51, 0.1)
    x2 = np.arange(0, 1.01, 0.05)
    y2 = np.arange(0, 1.21, 0.1)
    P = np.array(np.meshgrid(x1, y1, x2, y2, indexing="ij")).reshape(4, -1).T  # (M,4)
    a = 3 * (1 - s) ** 2 * s
    b = 3 * (1 - s) * s ** 2
    c = s ** 3
    BX = P[:, [0]] * a + P[:, [2]] * b + c  # (M,60)
    BY = P[:, [1]] * a + P[:, [3]] * b + c
    # ensure x monotonic
    mono = (np.diff(BX, axis=1) >= -1e-9).all(axis=1)
    P, BX, BY = P[mono], BX[mono], BY[mono]
    qx = np.asarray(progress_x)
    qy = np.asarray(progress_y)
    # interpolate each curve at qx
    idx = np.clip((BX[:, None, :] <= qx[None, :, None]).sum(axis=2) - 1, 0, BX.shape[1] - 2)  # (M,Q)
    rows = np.arange(len(P))[:, None]
    x0 = BX[rows, idx]
    x1_ = BX[rows, idx + 1]
    y0 = BY[rows, idx]
    y1_ = BY[rows, idx + 1]
    t = np.where(x1_ - x0 > 1e-9, (qx[None, :] - x0) / (x1_ - x0 + 1e-12), 0)
    yi = y0 + t * (y1_ - y0)
    err = np.sqrt(((yi - qy[None, :]) ** 2).mean(axis=1))
    best = int(np.argmin(err))
    return [round(float(v), 2) for v in P[best]], float(err[best])


def classify_event(energy_slice, fps):
    """infer easing family from an energy (≈|velocity|) profile. All results are INFERRED."""
    e = np.asarray(energy_slice, dtype=float)
    e = np.maximum(e - e.min() * 0.5, 0)
    n = len(e)
    if n < 3 or e.sum() <= 0:
        return {"easing_guess": "unknown", "confidence": 0.0, "inferred": True}
    prog = np.concatenate([[0], np.cumsum(e)]) / e.sum()
    xs = np.linspace(0, 1, n + 1)
    params, rmse = bezier_fit(xs, prog)
    peak = int(np.argmax(e))
    p = peak / max(1, n - 1)
    cv = float(e.std() / (e.mean() + 1e-9))
    # oscillation: local maxima after the main peak with decaying amplitude
    after = e[peak:]
    lm = [i for i in range(1, len(after) - 1) if after[i] > after[i - 1] and after[i] >= after[i + 1] and after[i] > 0.15 * e[peak]]
    if len(lm) >= 1 and n / fps >= 0.3 and p < 0.5:
        fam, conf = "spring", 0.45 + 0.1 * min(len(lm), 3)
    elif cv < 0.35:
        fam, conf = "linear", 0.6
    elif p <= 0.3:
        fam, conf = "ease-out", 0.55 + 0.3 * (0.3 - p)
    elif p >= 0.7:
        fam, conf = "ease-in", 0.55 + 0.3 * (p - 0.7)
    else:
        fam, conf = "ease-in-out", 0.5
    return {"easing_guess": fam, "confidence": round(min(conf, 0.9), 2), "cubic_bezier_fit": params,
            "bezier_rmse": round(rmse, 4), "peak_pos": round(p, 2), "energy_cv": round(cv, 2), "inferred": True}


def velocity_profile(frames, a0, b, energy, width=320):
    """Per-frame speed proxy for one motion event.
    Frame differencing saturates when an object moves more than its stroke width per frame (thin text),
    which flattens the fast part of ease-out curves. Dense optical flow (Farneback) magnitude summed over
    the frame ~ speed x moving area, so it keeps the true shape. Falls back to frame-diff for pure fades."""
    h0, w0 = frames[0].shape[:2]
    hh = int(h0 * width / w0)
    g = [cv2.resize(cv2.cvtColor(frames[i], cv2.COLOR_RGB2GRAY), (width, hh), interpolation=cv2.INTER_AREA) for i in range(a0, b + 1)]
    mags = []
    vx = vy = div = 0.0
    yy, xx = np.mgrid[0:hh, 0:width]
    rx, ry = xx - width / 2, yy - hh / 2
    rn = np.hypot(rx, ry) + 1e-6
    for i in range(1, len(g)):
        fl = cv2.calcOpticalFlowFarneback(g[i - 1], g[i], None, 0.5, 3, 15, 3, 5, 1.2, 0)
        m = np.hypot(fl[..., 0], fl[..., 1])
        mv = m > 0.3
        mags.append(float(m[mv].sum()) / m.size)
        if mv.any():
            vx += float(fl[..., 0][mv].sum())
            vy += float(fl[..., 1][mv].sum())
            div += float(((fl[..., 0] * rx + fl[..., 1] * ry) / rn)[mv].sum())
    mags = np.array(mags)
    e = np.asarray(energy[a0 + 1:b + 1], float)
    tot = float(mags.sum() * width * hh) + 1e-9
    direction = {"mean_dx": round(vx / tot, 3), "mean_dy": round(vy / tot, 3), "radial": round(div / tot, 3)}
    if len(mags) >= 3 and mags.sum() > 0.02 * len(mags):
        return mags, "optical-flow", direction
    return e, "frame-diff (no coherent motion; fade/colour change)", direction


def classify_entry(direction, src):
    """INFERRED entrance/transition type from flow direction (unit-less ratios of coherent motion)."""
    if not direction or src.startswith("frame-diff"):
        return "fade"
    dx, dy, rad = direction["mean_dx"], direction["mean_dy"], direction["radial"]
    if abs(rad) > 0.5 and abs(rad) > max(abs(dx), abs(dy)):
        return "scale-in" if rad < 0 else "scale-out"
    if abs(dy) >= abs(dx) and abs(dy) > 0.3:
        return "slide-up" if dy < 0 else "slide-down"
    if abs(dx) > 0.3:
        return "slide-left" if dx < 0 else "slide-right"
    return "fade/mixed"


def detect_events(energy, area, times, fps, scenes, frames=None):
    nz = energy[1:]
    floor = float(np.percentile(nz, 30)) if len(nz) else 0.0
    thr = max(floor * 4, 0.0004)
    active = energy > thr
    # close gaps of <=2 frames
    idx = np.where(active)[0]
    events = []
    if len(idx):
        start = prev = idx[0]
        for i in idx[1:]:
            if i - prev > 3:
                events.append((start, prev))
                start = i
            prev = i
        events.append((start, prev))
    cut_frames = [s["start_f"] for s in scenes[1:]]
    out = []
    for a, b in events:
        if b - a + 1 < 2:
            continue
        a0 = max(0, a - 1)  # energy[i] is diff(i-1,i) => motion starts at a-1
        dur = (b - a0 + 1) / fps
        ev = {"start_s": round(float(times[a0]), 3), "end_s": round(float(times[b]), 3), "duration_s": round(dur, 3),
              "peak_s": round(float(times[a + int(np.argmax(energy[a:b + 1]))]), 3),
              "peak_energy": round(float(energy[a:b + 1].max()), 5),
              "mean_changed_area": round(float(area[a:b + 1].mean()), 4)}
        seg_e = energy[a:b + 1]
        pk = int(np.argmax(seg_e))
        lo_, hi_ = pk, pk
        while lo_ > 0 and seg_e[lo_ - 1] >= 0.2 * seg_e[pk]:
            lo_ -= 1
        while hi_ < len(seg_e) - 1 and seg_e[hi_ + 1] >= 0.2 * seg_e[pk]:
            hi_ += 1
        ev["core_duration_s"] = round((hi_ - lo_ + 2) / fps, 3)  # frames with energy >= 20% of peak
        ev["is_transition"] = any(a0 - 3 <= c <= b + 3 for c in cut_frames)
        prof, src, direction = velocity_profile(frames, a0, b, energy) if frames is not None else (energy[a:b + 1], "frame-diff", None)
        ev.update(classify_event(prof, fps))
        ev["velocity_source"] = src
        pr = np.asarray(prof, float)
        if len(pr) >= 2 and pr.max() > 0:
            ev["velocity_profile_20"] = [round(float(v), 4) for v in np.interp(np.linspace(0, len(pr) - 1, 20), np.arange(len(pr)), pr / pr.max())]
        ev["flow_direction"] = direction
        ev["entry_type_guess"] = classify_entry(direction, src)
        ev["start_tc"] = tc(ev["start_s"])
        out.append(ev)
    return out, thr


def tiers_1d(values, kmax=3):
    v = np.sort(np.asarray(values, dtype=float))
    if len(v) == 0:
        return []
    if len(v) < 4:
        return [round(float(np.median(v)), 3)]
    from sklearn.cluster import KMeans
    k = min(kmax, len(np.unique(np.round(v, 2))))
    km = KMeans(n_clusters=k, n_init=4, random_state=0).fit(v.reshape(-1, 1))
    cs = sorted(float(c) for c in km.cluster_centers_.ravel())
    return [round(c, 3) for c in cs]


def rhythm_stats(events, scenes, fps):
    onsets = np.array([e["start_s"] for e in events if not e["is_transition"]])
    iv = np.diff(onsets) if len(onsets) > 1 else np.array([])
    iv = iv[iv > 1.5 / fps]
    med_iv = float(np.median(iv)) if len(iv) else None
    bpm = None
    if med_iv:
        bpm = 60.0 / med_iv
        while bpm < 60:
            bpm *= 2
        while bpm > 180:
            bpm /= 2
    # stagger: per scene, intervals between consecutive short entrance events
    stag = []
    for s in scenes:
        ons = [e["start_s"] for e in events if s["start_s"] <= e["start_s"] < s["end_s"] and not e["is_transition"]]
        d = np.diff(ons)
        stag += [x for x in d if 1.5 / fps < x < 1.0]
    durs = [s["duration_s"] for s in scenes]
    return {
        "scene_count": len(scenes),
        "shot_duration_mean_s": round(float(np.mean(durs)), 3) if durs else None,
        "shot_duration_median_s": round(float(np.median(durs)), 3) if durs else None,
        "shot_duration_min_s": round(float(np.min(durs)), 3) if durs else None,
        "shot_duration_max_s": round(float(np.max(durs)), 3) if durs else None,
        "motion_onset_interval_median_s": round(med_iv, 3) if med_iv else None,
        "visual_bpm_estimate": round(bpm, 1) if bpm else None,
        "stagger_median_s": round(float(np.median(stag)), 3) if stag else None,
        "notes": "shot stats measured from detected cuts; BPM/stagger inferred from motion-onset intervals",
    }


# ------------------------------------------------------------------ palette / bg

def border_pixels(fr, frac=0.04):
    h, w = fr.shape[:2]
    bh, bw = max(1, int(h * frac)), max(1, int(w * frac))
    return np.concatenate([fr[:bh].reshape(-1, 3), fr[-bh:].reshape(-1, 3), fr[:, :bw].reshape(-1, 3), fr[:, -bw:].reshape(-1, 3)])


def infer_roles(palette, bg_rgb):
    """assign palette roles. INFERRED."""
    bg_lab = srgb_to_lab(np.array(bg_rgb, float))
    cands = [c for c in palette if delta_e2000(c["lab"], bg_lab) > 6]
    roles = {"bg": rgb_to_hex(bg_rgb)}
    if not cands:
        return roles
    # surface: low-contrast-ish near bg (dE 6-25) and decent ratio
    surf = [c for c in cands if delta_e2000(c["lab"], bg_lab) < 25 and chroma(c["rgb"]) < 30]
    if surf:
        roles["surface"] = max(surf, key=lambda c: c["ratio"])["hex"]
    # text: highest contrast vs bg among colours with low chroma
    neutral = [c for c in cands if chroma(c["rgb"]) < 25]
    pool = neutral or cands
    text = max(pool, key=lambda c: contrast_ratio(c["rgb"], bg_rgb) * (0.5 + min(c["ratio"] * 20, 1)))
    roles["text"] = text["hex"]
    # muted text: neutral with mid contrast
    muted = [c for c in neutral if c["hex"] != text["hex"] and 2.0 < contrast_ratio(c["rgb"], bg_rgb) < contrast_ratio(text["rgb"], bg_rgb)]
    if muted:
        roles["text_muted"] = max(muted, key=lambda c: c["ratio"])["hex"]
    # chromatic: primary = most frequent chromatic, accent = most saturated other
    chrom = sorted([c for c in cands if chroma(c["rgb"]) >= 25], key=lambda c: -c["ratio"])
    if chrom:
        roles["primary"] = chrom[0]["hex"]
        rest = [c for c in chrom[1:] if delta_e2000(c["lab"], chrom[0]["lab"]) > 15]
        if rest:
            roles["accent"] = max(rest, key=lambda c: chroma(c["rgb"]) * (0.3 + c["ratio"] * 10))["hex"]
            more = [c["hex"] for c in rest if c["hex"] != roles["accent"]]
            if more:
                roles["extra"] = more[:3]
    return roles


# ------------------------------------------------------------------ layout

def layout_boxes(frame_rgb, bg_rgb, de_thr=12.0):
    h, w = frame_rgb.shape[:2]
    small = cv2.resize(frame_rgb, (w // 2, h // 2), interpolation=cv2.INTER_AREA) if w > 1000 else frame_rgb
    sh, sw = small.shape[:2]
    lab = srgb_to_lab(small.reshape(-1, 3)).reshape(sh, sw, 3)
    d = np.sqrt(((lab - srgb_to_lab(np.array(bg_rgb, float))) ** 2).sum(-1))
    mask = (d > de_thr).astype(np.uint8) * 255
    kx = max(3, sw // 60)
    ky = max(3, sh // 120)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (kx, ky)))
    n, _, stats, _ = cv2.connectedComponentsWithStats(mask)
    scale = w / sw
    boxes = []
    edge_bars = []
    surfaces = []
    for i in range(1, n):
        x, y, bw, bh, a = stats[i]
        if a < (sw * sh) * 0.0004:
            continue
        if bw >= sw * 0.98 and bh >= sh * 0.98:
            continue
        touches = x <= 1 or y <= 1 or x + bw >= sw - 1 or y + bh >= sh - 1
        if touches and (bh < sh * 0.02 or bw < sw * 0.02):
            edge_bars.append([int(x * scale), int(y * scale), int(bw * scale), int(bh * scale)])
            continue
        boxes.append([int(x * scale), int(y * scale), int(bw * scale), int(bh * scale)])
        if bw * bh > sw * sh * 0.04:
            inner = small[y + bh // 5: y + bh - bh // 5, x + bw // 5: x + bw - bw // 5].reshape(-1, 3)
            if len(inner):
                med = np.median(inner, axis=0)
                share = float((np.abs(inner.astype(int) - med).max(1) < 12).mean())
                if share > 0.6:
                    surfaces.append({"rgb": [int(v) for v in med], "hex": rgb_to_hex(med), "share": round(share, 3),
                                     "box": [int(x * scale), int(y * scale), int(bw * scale), int(bh * scale)]})
    fg_ratio = float((mask > 0).mean())
    return boxes, fg_ratio, edge_bars, surfaces


def cluster_positions(vals, tol):
    vals = sorted(vals)
    groups = []
    for v in vals:
        if groups and abs(v - np.mean(groups[-1])) <= tol:
            groups[-1].append(v)
        else:
            groups.append([v])
    return [(round(float(np.mean(g)), 1), len(g)) for g in groups]


def estimate_layout(keyframe_paths, bg_rgb, W, H):
    all_boxes = []
    edge_bars_all = []
    surfaces_all = []
    per_frame = []
    for p in keyframe_paths:
        fr = cv2.cvtColor(cv2.imread(p), cv2.COLOR_BGR2RGB)
        boxes, fg, bars, surfs = layout_boxes(fr, bg_rgb)
        surfaces_all += [dict(sf, frame=os.path.basename(p)) for sf in surfs]
        per_frame.append({"frame": os.path.basename(p), "boxes": boxes, "edge_bars": bars, "fg_ratio": round(fg, 4)})
        edge_bars_all += bars
        all_boxes += boxes
    if not all_boxes:
        return {"note": "no foreground boxes found", "inferred": True}
    B = np.array(all_boxes, float)
    lefts, tops = B[:, 0], B[:, 1]
    rights, bottoms = B[:, 0] + B[:, 2], B[:, 1] + B[:, 3]
    ml = float(np.percentile(lefts, 5))
    mr = float(W - np.percentile(rights, 95))
    mt = float(np.percentile(tops, 5))
    mb = float(H - np.percentile(bottoms, 95))
    cx = (lefts + rights) / 2
    centered = float((np.abs(cx - W / 2) < W * 0.02).mean())
    left_groups = [g for g in cluster_positions(lefts, W * 0.01) if g[1] >= 2]
    left_aligned = float(sum(g[1] for g in left_groups) / len(lefts))
    align = "center" if centered > 0.5 else ("left" if left_aligned > 0.4 else "mixed")
    # grid columns fit
    best = None
    for cols in (12, 8, 6, 4):
        gut = W * 0.02
        content = W - 2 * max(ml, W * 0.04)
        colw = (content - gut * (cols - 1)) / cols
        lines = [max(ml, W * 0.04) + i * (colw + gut) for i in range(cols)]
        hit = float(np.mean([min(abs(l - x) for x in lines) < W * 0.012 for l in lefts]))
        if best is None or hit > best[1] + 0.05:
            best = (cols, hit)
    return {
        "margins_px": {"left": round(ml), "right": round(mr), "top": round(mt), "bottom": round(mb)},
        "margins_pct": {"left": round(ml / W * 100, 2), "right": round(mr / W * 100, 2), "top": round(mt / H * 100, 2), "bottom": round(mb / H * 100, 2)},
        "safe_area_pct_estimate": {"x": round(min(ml, mr) / W * 100, 2), "y": round(min(mt, mb) / H * 100, 2)},
        "dominant_alignment": align,
        "centered_box_ratio": round(centered, 3),
        "left_aligned_box_ratio": round(left_aligned, 3),
        "common_left_edges_px": [g[0] for g in sorted(left_groups, key=lambda g: -g[1])[:6]],
        "grid_columns_guess": best[0], "grid_fit_ratio": round(best[1], 3),
        "box_count": len(all_boxes),
        "edge_bars": edge_bars_all[:20],
        "surfaces": surfaces_all[:20],
        "edge_bar_note": "thin bars touching the frame edge (progress bars / letterbox) are excluded from margins",
        "per_frame": per_frame,
        "measured": ["margins_px", "margins_pct", "box positions"],
        "inferred": ["dominant_alignment", "grid_columns_guess", "safe_area_pct_estimate"],
    }


# ------------------------------------------------------------------ OCR

CODE_CHARS = set("{}()[];=<>/_$#`'\"|&*+:")


def ocr_available():
    return shutil.which("tesseract") is not None


def ocr_frame(png, lang, out_tsv_base):
    langs_avail = run(["tesseract", "--list-langs"], check=False).stdout + run(["tesseract", "--list-langs"], check=False).stderr
    use = "+".join([l for l in lang.split("+") if l in langs_avail]) or "eng"
    lines_all = []
    img = cv2.imread(png, cv2.IMREAD_GRAYSCALE)
    inv_png = out_tsv_base + "_inv.png"
    cv2.imwrite(inv_png, 255 - img)
    for variant, src in (("", png), ("_inv", inv_png)):
        run(["tesseract", src, out_tsv_base + variant, "-l", use, "--psm", "11", "tsv"], check=False)
        lines_all += _parse_tsv(out_tsv_base + variant + ".tsv")
    os.remove(inv_png)
    # targeted pass on the bottom band (subtitle bars: light text on a dark pill is often missed by the full-frame pass)
    H0 = img.shape[0]
    y0 = int(H0 * 0.72)
    band_png = out_tsv_base + "_band.png"
    cv2.imwrite(band_png, 255 - img[y0:])
    run(["tesseract", band_png, out_tsv_base + "_band", "-l", use, "--psm", "6", "tsv"], check=False)
    os.remove(band_png)
    for l in _parse_tsv(out_tsv_base + "_band.tsv"):
        l["bbox"] = [l["bbox"][0], l["bbox"][1] + y0, l["bbox"][2], l["bbox"][3]]
        bx, by, bw, bh = l["bbox"]
        dup = False
        for o in lines_all:
            ox, oy, ow, oh = o["bbox"]
            ix = max(0, min(bx + bw, ox + ow) - max(bx, ox))
            iy = max(0, min(by + bh, oy + oh) - max(by, oy))
            if ix * iy > 0.3 * min(bw * bh, ow * oh) and (l["text"][:4] in o["text"] or o["text"][:4] in l["text"]):
                dup = True
                break
        if not dup:
            lines_all.append(l)
    rgb = cv2.cvtColor(cv2.imread(png), cv2.COLOR_BGR2RGB)
    for l in lines_all:
        x, y, w, h = l["bbox"]
        crop = rgb[max(0, y):y + h, max(0, x):x + w].reshape(-1, 3).astype(int)
        if len(crop) < 10:
            continue
        border = np.concatenate([rgb[max(0, y), max(0, x):x + w], rgb[min(rgb.shape[0] - 1, y + h), max(0, x):x + w]]).astype(int)
        local_bg = np.median(border, axis=0) if len(border) else np.median(crop, axis=0)
        ink = np.abs(crop - local_bg).max(1) > 40
        l["ink_ratio"] = round(float(ink.mean()), 3)
        rows = np.where(ink.reshape(h if y >= 0 else -1, -1).mean(1) > 0.01)[0] if ink.size == w * h else np.array([])
        if len(rows) >= 2:
            ink_h = int(rows[-1] - rows[0] + 1)
            l["ink_height_px"] = ink_h
            # CJK glyph ink ≈ 0.88em; Latin line with ascenders ≈ 0.72em (caps only ≈0.70)
            l["est_font_size_px"] = round(ink_h / (0.88 if l["cjk"] else 0.72), 1)
        l["local_bg"] = rgb_to_hex(local_bg)
        if ink.sum() > 20:
            inkpx = crop[ink]
            l["ink_colors"] = [{"hex": c["hex"], "ratio": c["ratio"]} for c in kmeans_palette(inkpx, k=3)]
    # merge duplicates (same text region found in both passes): keep higher confidence
    lines_all.sort(key=lambda l: -l["conf"])
    kept = []
    for l in lines_all:
        x, y, w, h = l["bbox"]
        dup = False
        for k in kept:
            X, Y, W, H = k["bbox"]
            ix = max(0, min(x + w, X + W) - max(x, X))
            iy = max(0, min(y + h, Y + H) - max(y, Y))
            if ix * iy > 0.4 * min(w * h, W * H):
                dup = True
                break
        if not dup:
            kept.append(l)
    kept.sort(key=lambda l: (l["bbox"][1], l["bbox"][0]))
    return kept


def _parse_tsv(path):
    lines = {}
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8", errors="ignore") as f:
        rd = csv.DictReader(f, delimiter="\t", quoting=csv.QUOTE_NONE)
        for r in rd:
            try:
                conf = float(r["conf"])
            except Exception:
                continue
            txt = (r.get("text") or "").strip()
            if conf < 55 or not txt:
                continue
            key = (r["block_num"], r["par_num"], r["line_num"])
            x, y, w, h = int(r["left"]), int(r["top"]), int(r["width"]), int(r["height"])
            L = lines.setdefault(key, {"words": [], "x0": x, "y0": y, "x1": x + w, "y1": y + h, "confs": [], "hs": []})
            L["words"].append(txt)
            L["confs"].append(conf)
            L["hs"].append(h)
            L["x0"], L["y0"] = min(L["x0"], x), min(L["y0"], y)
            L["x1"], L["y1"] = max(L["x1"], x + w), max(L["y1"], y + h)
    out = []
    for L in lines.values():
        cjk = any("\u4e00" <= ch <= "\u9fff" for w in L["words"] for ch in w)
        text = ("" if cjk else " ").join(L["words"])
        if len(text.strip()) < 2:
            continue
        bw_, bh_ = L["x1"] - L["x0"], L["y1"] - L["y0"]
        if bw_ < 0.35 * bh_ * len(text.replace(" ", "")):
            continue  # geometrically implausible box (tesseract hallucination on big glyphs/graphics)
        out.append({"text": text, "bbox": [L["x0"], L["y0"], L["x1"] - L["x0"], L["y1"] - L["y0"]],
                    "glyph_height_px": int(np.median(L["hs"])), "est_font_size_px": round(float(np.median(L["hs"])) / (0.9 if cjk else 0.78), 1), "conf": round(float(np.mean(L["confs"])), 1),
                    "codey": sum(ch in CODE_CHARS for ch in text) / max(1, len(text)) > 0.08, "cjk": cjk})
    return out


def type_levels(heights, H):
    if not heights:
        return []
    hs = sorted(heights, reverse=True)
    levels = []
    for h in hs:
        if levels and abs(h - levels[-1]["h"]) / levels[-1]["h"] < 0.18:
            levels[-1]["members"].append(h)
            levels[-1]["h"] = float(np.median(levels[-1]["members"]))
        else:
            levels.append({"h": h, "members": [h]})
    names = ["display", "h1", "h2", "body", "caption", "micro"]
    out = []
    for i, l in enumerate(levels[:6]):
        gh = l["h"]
        out.append({"level": names[i], "est_font_size_px": round(gh, 1),
                    "est_font_size_pct_of_height": round(gh / H * 100, 2), "count": len(l["members"])})
    return out


# ------------------------------------------------------------------ audio

def analyze_audio(video, outdir):
    import subprocess
    wav = os.path.join(outdir, "audio.wav")
    run(["ffmpeg", "-y", "-v", "error", "-i", video, "-vn", "-ac", "1", "-ar", "22050", wav])
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", wav, "-f", "f32le", "-"], capture_output=True)
    y = np.frombuffer(p.stdout, dtype=np.float32)
    sr = 22050
    if len(y) < sr * 0.2:
        return None
    hop, win = 512, 1024
    nfr = 1 + (len(y) - win) // hop
    idx = np.arange(win)[None, :] + hop * np.arange(nfr)[:, None]
    frames = y[idx] * np.hanning(win)[None, :]
    rms = np.sqrt((frames ** 2).mean(1))
    db = 20 * np.log10(rms + 1e-9)
    t = (np.arange(nfr) * hop + win / 2) / sr
    mag = np.abs(np.fft.rfft(frames, axis=1))
    logm = np.log1p(100 * mag)
    flux = np.maximum(np.diff(logm, axis=0), 0).sum(1)
    flux = np.concatenate([[0], flux])
    flux = flux / (flux.max() + 1e-9)
    # adaptive peak picking
    from scipy.ndimage import median_filter  # type: ignore
    base = median_filter(flux, size=int(0.5 * sr / hop) | 1)
    min_gap = int(0.1 * sr / hop)
    onsets = []
    for i in range(1, len(flux) - 1):
        if flux[i] > flux[i - 1] and flux[i] >= flux[i + 1] and flux[i] > base[i] + 0.08 and db[i] > db.max() - 45:
            if not onsets or i - onsets[-1] >= min_gap:
                onsets.append(i)
    onset_t = t[onsets] if onsets else np.array([])
    # tempo by autocorrelation of flux
    bpm = None
    fr_rate = sr / hop
    ac = np.correlate(flux - flux.mean(), flux - flux.mean(), mode="full")[len(flux) - 1:]
    lo, hi = int(fr_rate * 60 / 180), int(fr_rate * 60 / 60)
    if hi < len(ac) and len(onset_t) >= 4:
        lag = lo + int(np.argmax(ac[lo:hi]))
        bpm = round(60 * fr_rate / lag, 1)
    with open(os.path.join(outdir, "audio_envelope.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["time_s", "rms_db", "onset_strength"])
        for a, b, c in zip(t, db, flux):
            wr.writerow([f"{a:.3f}", f"{b:.2f}", f"{c:.4f}"])
    with open(os.path.join(outdir, "audio_onsets.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["time_s", "timecode"])
        for a in onset_t:
            wr.writerow([f"{a:.3f}", tc(a)])
    fig, ax = plt.subplots(2, 1, figsize=(14, 5), sharex=True)
    ax[0].plot(t, db, lw=0.8)
    ax[0].set_ylabel("RMS dB")
    ax[1].plot(t, flux, lw=0.8, color="tab:orange")
    for o in onset_t:
        ax[1].axvline(o, color="r", alpha=0.3, lw=0.8)
    ax[1].set_ylabel("onset strength")
    ax[1].set_xlabel("time (s)")
    fig.tight_layout()
    fig.savefig(os.path.join(outdir, "audio_envelope.png"), dpi=110)
    plt.close(fig)
    return {"wav": wav, "duration_s": round(len(y) / sr, 3), "loudness_peak_db": round(float(db.max()), 2),
            "loudness_mean_db": round(float(db[db > db.max() - 60].mean()), 2),
            "onset_count": int(len(onset_t)), "onsets_s": [round(float(x), 3) for x in onset_t],
            "tempo_bpm_estimate": bpm, "tempo_note": "autocorrelation of spectral flux; INFERRED, unreliable for speech-only tracks"}


def sync_points(audio_onsets, visual_times, tol=0.08):
    if not audio_onsets or not visual_times:
        return None
    ao = np.array(audio_onsets)
    pairs = []
    for v in visual_times:
        d = ao - v
        j = int(np.argmin(np.abs(d)))
        if abs(d[j]) <= tol:
            pairs.append({"visual_s": round(v, 3), "audio_s": round(float(ao[j]), 3), "offset_ms": round(float(d[j]) * 1000, 1)})
    return {"tolerance_ms": tol * 1000, "visual_events": len(visual_times), "matched": len(pairs),
            "match_ratio": round(len(pairs) / len(visual_times), 3),
            "median_offset_ms": round(float(np.median([p["offset_ms"] for p in pairs])), 1) if pairs else None,
            "pairs": pairs[:200]}


# ------------------------------------------------------------------ contact sheet

def contact_sheet(rows, out_png, title, thumb_w=400):
    from PIL import Image, ImageDraw, ImageFont
    try:
        font = ImageFont.truetype("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc", 16)
    except Exception:
        try:
            font = ImageFont.truetype("DejaVuSans.ttf", 16)
        except Exception:
            font = ImageFont.load_default()
    imgs = []
    for row in rows:
        r = []
        for (p, label) in row:
            im = Image.open(p).convert("RGB")
            th = int(im.height * thumb_w / im.width)
            r.append((im.resize((thumb_w, th)), label))
        imgs.append(r)
    th = imgs[0][0][0].height
    cols = max(len(r) for r in imgs)
    pad, lab_h = 8, 24
    W = cols * (thumb_w + pad) + pad
    H = 40 + len(imgs) * (th + lab_h + pad) + pad
    sheet = Image.new("RGB", (W, H), (24, 24, 24))
    d = ImageDraw.Draw(sheet)
    d.text((pad, 10), title, fill=(230, 230, 230), font=font)
    for ri, r in enumerate(imgs):
        for ci, (im, label) in enumerate(r):
            x = pad + ci * (thumb_w + pad)
            y = 40 + ri * (th + lab_h + pad)
            d.text((x, y + 2), label, fill=(200, 200, 200), font=font)
            sheet.paste(im, (x, y + lab_h))
    sheet.save(out_png)
    return out_png


def palette_png(palette, out_png, title="palette"):
    from PIL import Image, ImageDraw
    W, H = 900, 140
    im = Image.new("RGB", (W, H), (255, 255, 255))
    d = ImageDraw.Draw(im)
    x = 0
    tot = sum(c["ratio"] for c in palette) or 1
    for c in palette:
        w = max(4, int(W * c["ratio"] / tot))
        d.rectangle([x, 0, x + w, 100], fill=tuple(c["rgb"]))
        d.text((x + 3, 105), f"{c['hex']}", fill=(0, 0, 0))
        d.text((x + 3, 120), f"{c['ratio'] * 100:.1f}%", fill=(0, 0, 0))
        x += w
    im.save(out_png)


# ------------------------------------------------------------------ main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--sample-fps", type=float, default=None, help="analysis fps (default=min(source fps,30))")
    ap.add_argument("--scene-threshold", type=float, default=0.30)
    ap.add_argument("--min-scene-s", type=float, default=0.5)
    ap.add_argument("--k", type=int, default=8, help="global palette size")
    ap.add_argument("--no-ocr", action="store_true")
    ap.add_argument("--ocr-lang", default="chi_sim+eng")
    ap.add_argument("--max-scenes-sheet", type=int, default=30)
    ap.add_argument("--no-videomd", action="store_true", help="skip the VIDEO.md package export")
    args = ap.parse_args()

    out = os.path.abspath(args.out)
    kf_dir = os.path.join(out, "keyframes")
    os.makedirs(kf_dir, exist_ok=True)
    meta = ffprobe(args.video)
    write_json(os.path.join(out, "meta.json"), meta)
    fps = args.sample_fps or min(meta["fps"], 30.0)
    print(f"[analyze] {meta['width']}x{meta['height']} @ {meta['fps']}fps, {meta['duration_s']}s, audio={meta['has_audio']}; sampling {fps}fps")

    frames, times = decode_frames(args.video, fps)
    if len(frames) < 2:
        raise SystemExit("video too short to analyze")
    # background colour: mode of border pixels (quantised)
    sample_idx = np.linspace(0, len(frames) - 1, min(60, len(frames))).astype(int)
    bp = np.concatenate([border_pixels(frames[i]) for i in sample_idx])
    q = (bp // 8).astype(np.int32)
    keys = q[:, 0] * 1024 + q[:, 1] * 32 + q[:, 2]
    vals, cnts = np.unique(keys, return_counts=True)
    mode = vals[np.argmax(cnts)]
    sel = bp[keys == mode]
    bg_rgb = [int(x) for x in np.median(sel, axis=0)]
    bg_conf = float(cnts.max() / len(keys))

    scenes, scene_score = detect_scenes(frames, times, fps, args.scene_threshold, args.min_scene_s, bg_rgb)
    energy, area = motion_energy(frames)
    events, thr = detect_events(energy, area, times, fps, scenes, frames)
    print(f"[analyze] scenes={len(scenes)} motion_events={len(events)}")

    # global palette
    allpx = np.concatenate([frames[i].reshape(-1, 3)[::7] for i in sample_idx])
    pal = kmeans_palette(allpx, k=args.k)
    palette_png(pal, os.path.join(out, "palette_global.png"))
    # foreground-only palette (exclude bg) gives better accents
    lab_bg = srgb_to_lab(np.array(bg_rgb, float))
    fgpx = allpx[delta_e2000(srgb_to_lab(allpx), lab_bg) > 8] if len(allpx) else allpx
    pal_fg = kmeans_palette(fgpx, k=args.k) if len(fgpx) > 50 else []
    if pal_fg:
        palette_png(pal_fg, os.path.join(out, "palette_foreground.png"))
    roles = infer_roles(pal_fg or pal, bg_rgb)

    # keyframes per scene: entry(+15%), mid(50%), settled(min-energy in last 60%)
    rows = []
    settled_paths = []
    for s in scenes:
        a, b = s["start_f"], s["end_f"]
        L = b - a
        entry = a + max(1, int(L * 0.15)) if L > 2 else a
        mid = a + L // 2
        lo = a + int(L * 0.4)
        # settled = the LATEST quiet frame before the outgoing transition (all build-ups finished)
        tail = max(lo + 1, b - int(round(0.35 * fps)))
        end_t = float(times[b - 1])
        for e in events:
            if e["is_transition"] and e["start_s"] <= end_t + 0.5 and e["end_s"] >= end_t - 0.5 and e["start_s"] > float(times[a]) + 0.3:
                tail = max(lo + 1, min(tail, int(e["start_s"] * fps) - 1))
                s["outgoing_transition_start_s"] = e["start_s"]
        quiet = [i for i in range(lo, tail) if energy[i] <= thr and (i + 1 >= len(energy) or energy[i + 1] <= thr)]
        if quiet:
            settled = quiet[-1]
        else:
            seg = energy[lo:b] if b > lo else energy[a:b]
            settled = lo + int(np.argmin(seg)) if len(seg) else mid
        kfs = []
        for name, fi in (("entry", entry), ("mid", mid), ("settled", settled)):
            fi = min(max(fi, 0), len(times) - 1)
            t = float(times[fi]) + 0.5 / fps
            p = os.path.join(kf_dir, f"scene{s['index']:03d}_{name}.png")
            extract_frame(args.video, t, p)
            kfs.append((p, f"S{s['index']} {name} {tc(t)}"))
            s.setdefault("keyframes", {})[name] = {"path": p, "time_s": round(t, 3), "tc": tc(t)}
        settled_paths.append(kfs[2][0])
        rows.append(kfs)
        # per-scene palette from analysis frames
        spx = np.concatenate([frames[i].reshape(-1, 3)[::5] for i in range(a, b, max(1, L // 6))])
        s["palette"] = [{k: v for k, v in c.items() if k != "lab"} for c in kmeans_palette(spx, k=5)]
        s["motion_events"] = sum(1 for e in events if s["start_s"] <= e["start_s"] < s["end_s"])
    step = max(1, int(np.ceil(len(rows) / args.max_scenes_sheet)))
    contact_sheet(rows[::step], os.path.join(out, "contact_sheet.png"),
                  f"{os.path.basename(args.video)}  {meta['width']}x{meta['height']} {meta['fps']}fps {meta['duration_s']}s  scenes={len(scenes)}")

    with open(os.path.join(out, "scenes.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["index", "start_s", "end_s", "duration_s", "start_tc", "end_tc"])
        for s in scenes:
            wr.writerow([s["index"], s["start_s"], s["end_s"], s["duration_s"], s["start_tc"], s["end_tc"]])

    with open(os.path.join(out, "motion_energy.csv"), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["time_s", "energy", "changed_area", "scene_score"])
        for t, e, a_, sc in zip(times, energy, area, scene_score):
            wr.writerow([f"{t:.3f}", f"{e:.6f}", f"{a_:.5f}", f"{sc:.4f}"])
    fig, ax = plt.subplots(figsize=(14, 4))
    ax.plot(times, energy, lw=0.9, label="motion energy (mean |Δ|)")
    ax.axhline(thr, color="gray", ls="--", lw=0.7, label="event threshold")
    for s in scenes[1:]:
        ax.axvline(s["start_s"], color="red", alpha=0.5, lw=1)
    for e in events:
        ax.axvspan(e["start_s"], e["end_s"], color="orange" if not e["is_transition"] else "purple", alpha=0.12)
    ax.set_xlabel("time (s)")
    ax.set_title("motion energy — red=scene cuts, orange=motion events, purple=transition events")
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(os.path.join(out, "motion_energy.png"), dpi=110)
    plt.close(fig)

    # motion summary
    non_tr = [e for e in events if not e["is_transition"]]
    tr = [e for e in events if e["is_transition"]]
    fam_counts = {}
    for e in non_tr:
        fam_counts[e["easing_guess"]] = fam_counts.get(e["easing_guess"], 0) + 1
    beziers = [e["cubic_bezier_fit"] for e in non_tr if "cubic_bezier_fit" in e and e["bezier_rmse"] < 0.08]
    motion = {
        "event_threshold": round(thr, 5),
        "event_count": len(events), "transition_event_count": len(tr),
        "duration_tiers_s": tiers_1d([e["duration_s"] for e in non_tr]),
        "duration_median_s": round(float(np.median([e["duration_s"] for e in non_tr])), 3) if non_tr else None,
        "transition_duration_median_s": round(float(np.median([e["duration_s"] for e in tr])), 3) if tr else None,
        "transition_core_duration_median_s": round(float(np.median([e["core_duration_s"] for e in tr])), 3) if tr else None,
        "easing_family_counts": fam_counts,
        "dominant_easing_guess": max(fam_counts, key=fam_counts.get) if fam_counts else None,
        "median_cubic_bezier_fit": [round(float(x), 2) for x in np.median(beziers, axis=0)] if beziers else None,
        "events": events,
        "notes": "energy = mean abs frame difference; progress≈cumulative energy (assumes uniform object area); easing/bezier are INFERRED",
    }
    rhythm = rhythm_stats(events, scenes, fps)

    layout = estimate_layout(settled_paths, bg_rgb, meta["width"], meta["height"])

    ocr = {"available": False}
    if not args.no_ocr and ocr_available():
        od = os.path.join(out, "ocr")
        os.makedirs(od, exist_ok=True)
        lines_all = []
        for s, p in zip(scenes, settled_paths):
            ls = ocr_frame(p, args.ocr_lang, os.path.join(od, f"scene{s['index']:03d}"))
            for l in ls:
                l["scene"] = s["index"]
                b = l["bbox"]
                l["pos_pct"] = {"x": round(b[0] / meta["width"] * 100, 1), "y": round(b[1] / meta["height"] * 100, 1),
                                "cx": round((b[0] + b[2] / 2) / meta["width"] * 100, 1)}
            s["ocr_lines"] = [l["text"] for l in ls]
            lines_all += ls
        ocr = {"available": True, "engine": "tesseract", "lang": args.ocr_lang, "lines": lines_all,
               "type_levels": type_levels([l["est_font_size_px"] for l in lines_all], meta["height"]),
               "code_line_ratio": round(sum(l["codey"] for l in lines_all) / max(1, len(lines_all)), 3),
               "cjk_line_ratio": round(sum(l["cjk"] for l in lines_all) / max(1, len(lines_all)), 3),
               "notes": "font size ≈ OCR line-box height / 0.9 (CJK) or / 0.78 (Latin) — INFERRED; OCR text may contain errors; each frame is OCR-ed normal + inverted (light-on-dark)"}
    elif not args.no_ocr:
        ocr["note"] = "tesseract not installed — OCR skipped (install: apt-get install tesseract-ocr tesseract-ocr-chi-sim)"

    audio = None
    if meta["has_audio"]:
        try:
            audio = analyze_audio(args.video, out)
        except Exception as ex:  # keep going without audio
            audio = {"error": str(ex)}
        if audio and "onsets_s" in audio:
            vis = [s["start_s"] for s in scenes[1:]] + [e["start_s"] for e in non_tr]
            audio["av_sync"] = sync_points(audio["onsets_s"], sorted(vis))

    analysis = {
        "tool": "code-video-style-distill/analyze.py", "version": 1, "params": {k: v for k, v in vars(args).items() if k not in ("video", "out")},
        "source": meta, "sample_fps": fps,
        "background": {"rgb": bg_rgb, "hex": rgb_to_hex(bg_rgb), "border_mode_share": round(bg_conf, 3), "measured": True},
        "palette_global": [{k: v for k, v in c.items() if k != "lab"} for c in pal],
        "palette_foreground": [{k: v for k, v in c.items() if k != "lab"} for c in pal_fg],
        "palette_roles_inferred": roles,
        "scenes": scenes, "motion": motion, "rhythm": rhythm, "layout": layout, "ocr": ocr, "audio": audio,
        "files": {"contact_sheet": os.path.join(out, "contact_sheet.png"), "motion_energy_png": os.path.join(out, "motion_energy.png"),
                  "motion_energy_csv": os.path.join(out, "motion_energy.csv"), "scenes_csv": os.path.join(out, "scenes.csv"),
                  "palette_png": os.path.join(out, "palette_global.png"), "keyframes_dir": kf_dir},
        "fidelity": {
            "measured": ["source metadata", "scene cut times", "keyframes", "palette HEX+ratio", "background colour",
                         "motion energy curve", "motion event start/end/duration", "foreground box margins",
                         "OCR text+bbox (if available)", "audio loudness/onsets (if audio)"],
            "inferred": ["palette roles", "easing family + cubic-bezier fit", "visual BPM/stagger", "grid columns/alignment",
                         "font sizes from glyph height", "audio tempo"],
        },
    }
    write_json(os.path.join(out, "analysis.json"), analysis)
    if not args.no_videomd:
        try:
            import subprocess as _sp
            _sp.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "videomd_export.py"), out], check=True)
        except Exception as ex:
            print(f"[analyze] VIDEO.md export failed (non-fatal): {ex}")
    print(f"[analyze] done -> {out}/analysis.json")
    print(f"[analyze] look at: {analysis['files']['contact_sheet']}  and  {analysis['files']['motion_energy_png']}")


if __name__ == "__main__":
    main()
