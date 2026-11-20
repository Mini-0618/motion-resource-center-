"""Shared helpers for code-video-style-distill (color math, ffprobe, frame IO)."""
import json
import os
import subprocess

import numpy as np

# ---------------------------------------------------------------- shell / ffprobe

def run(cmd, check=True, capture=True):
    r = subprocess.run(cmd, capture_output=capture, text=True)
    if check and r.returncode != 0:
        raise RuntimeError(f"command failed: {' '.join(cmd)}\n{r.stderr[-2000:]}")
    return r


def ffprobe(path):
    r = run(["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", path])
    data = json.loads(r.stdout)
    v = next((s for s in data["streams"] if s.get("codec_type") == "video"), None)
    a = next((s for s in data["streams"] if s.get("codec_type") == "audio"), None)
    if v is None:
        raise RuntimeError("no video stream found")

    def _rate(s):
        try:
            n, d = s.split("/")
            return float(n) / float(d) if float(d) else 0.0
        except Exception:
            return 0.0

    fps = _rate(v.get("avg_frame_rate", "0/0")) or _rate(v.get("r_frame_rate", "0/0")) or 30.0
    dur = float(data["format"].get("duration") or v.get("duration") or 0)
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    w, h = int(v["width"]), int(v["height"])
    if abs(rot) in (90, 270):
        w, h = h, w
    return {
        "path": os.path.abspath(path),
        "width": w,
        "height": h,
        "fps": round(fps, 3),
        "duration_s": round(dur, 3),
        "nb_frames_est": int(round(dur * fps)),
        "video_codec": v.get("codec_name"),
        "pix_fmt": v.get("pix_fmt"),
        "bit_rate": data["format"].get("bit_rate"),
        "has_audio": a is not None,
        "audio_codec": a.get("codec_name") if a else None,
        "audio_sample_rate": int(a.get("sample_rate", 0)) if a else None,
        "aspect": f"{w}:{h}",
    }


def extract_frame(video, t, out_png, width=None):
    vf = [] if not width else ["-vf", f"scale={width}:-2"]
    run(["ffmpeg", "-y", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", video, "-frames:v", "1", *vf, out_png])
    return out_png


def tc(t, fps=None):
    """seconds -> HH:MM:SS.mmm (+frame if fps)"""
    t = max(0.0, float(t))
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = t % 60
    out = f"{h:02d}:{m:02d}:{s:06.3f}"
    if fps:
        out += f" (f{int(round(t * fps))})"
    return out

# ---------------------------------------------------------------- color math

def srgb_to_lab(rgb):
    """rgb: (...,3) uint8/float 0-255 -> CIE Lab (D65)."""
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    M = np.array([[0.4124564, 0.3575761, 0.1804375],
                  [0.2126729, 0.7151522, 0.0721750],
                  [0.0193339, 0.1191920, 0.9503041]])
    xyz = c @ M.T
    xyz = xyz / np.array([0.95047, 1.0, 1.08883])
    e = 216 / 24389
    k = 24389 / 27
    f = np.where(xyz > e, np.cbrt(xyz), (k * xyz + 16) / 116)
    L = 116 * f[..., 1] - 16
    a = 500 * (f[..., 0] - f[..., 1])
    b = 200 * (f[..., 1] - f[..., 2])
    return np.stack([L, a, b], axis=-1)


def delta_e2000(lab1, lab2):
    """CIEDE2000, broadcastable (...,3)."""
    lab1 = np.asarray(lab1, dtype=np.float64)
    lab2 = np.asarray(lab2, dtype=np.float64)
    L1, a1, b1 = lab1[..., 0], lab1[..., 1], lab1[..., 2]
    L2, a2, b2 = lab2[..., 0], lab2[..., 1], lab2[..., 2]
    C1 = np.hypot(a1, b1)
    C2 = np.hypot(a2, b2)
    Cb = (C1 + C2) / 2
    G = 0.5 * (1 - np.sqrt(Cb ** 7 / (Cb ** 7 + 25 ** 7)))
    a1p, a2p = (1 + G) * a1, (1 + G) * a2
    C1p, C2p = np.hypot(a1p, b1), np.hypot(a2p, b2)
    h1p = np.degrees(np.arctan2(b1, a1p)) % 360
    h2p = np.degrees(np.arctan2(b2, a2p)) % 360
    dLp = L2 - L1
    dCp = C2p - C1p
    dhp = h2p - h1p
    dhp = np.where(dhp > 180, dhp - 360, dhp)
    dhp = np.where(dhp < -180, dhp + 360, dhp)
    dhp = np.where(C1p * C2p == 0, 0, dhp)
    dHp = 2 * np.sqrt(C1p * C2p) * np.sin(np.radians(dhp / 2))
    Lbp = (L1 + L2) / 2
    Cbp = (C1p + C2p) / 2
    hsum = h1p + h2p
    hbp = np.where(np.abs(h1p - h2p) > 180, (hsum + 360) / 2, hsum / 2)
    hbp = np.where(C1p * C2p == 0, hsum, hbp)
    T = (1 - 0.17 * np.cos(np.radians(hbp - 30)) + 0.24 * np.cos(np.radians(2 * hbp))
         + 0.32 * np.cos(np.radians(3 * hbp + 6)) - 0.20 * np.cos(np.radians(4 * hbp - 63)))
    dtheta = 30 * np.exp(-(((hbp - 275) / 25) ** 2))
    Rc = 2 * np.sqrt(Cbp ** 7 / (Cbp ** 7 + 25 ** 7))
    Sl = 1 + (0.015 * (Lbp - 50) ** 2) / np.sqrt(20 + (Lbp - 50) ** 2)
    Sc = 1 + 0.045 * Cbp
    Sh = 1 + 0.015 * Cbp * T
    Rt = -np.sin(np.radians(2 * dtheta)) * Rc
    return np.sqrt((dLp / Sl) ** 2 + (dCp / Sc) ** 2 + (dHp / Sh) ** 2 + Rt * (dCp / Sc) * (dHp / Sh))


def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    r, g, b = [int(round(max(0, min(255, x)))) for x in rgb]
    return f"#{r:02X}{g:02X}{b:02X}"


def rel_luminance(rgb):
    c = np.asarray(rgb, dtype=np.float64) / 255.0
    c = np.where(c <= 0.03928, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    return float(0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2])


def contrast_ratio(rgb1, rgb2):
    l1, l2 = rel_luminance(rgb1), rel_luminance(rgb2)
    hi, lo = max(l1, l2), min(l1, l2)
    return (hi + 0.05) / (lo + 0.05)


def chroma(rgb):
    lab = srgb_to_lab(np.array(rgb, dtype=np.float64))
    return float(np.hypot(lab[1], lab[2]))


def kmeans_palette(pixels_rgb, k=8, seed=0, max_samples=60000):
    """pixels_rgb: (N,3) uint8. returns list of {hex, rgb, ratio, lab} sorted by ratio desc."""
    from sklearn.cluster import KMeans
    px = np.asarray(pixels_rgb).reshape(-1, 3)
    if len(px) == 0:
        return []
    rng = np.random.default_rng(seed)
    if len(px) > max_samples:
        px = px[rng.choice(len(px), max_samples, replace=False)]
    lab = srgb_to_lab(px)
    uniq = np.unique(np.round(lab).astype(int), axis=0)
    k = int(max(1, min(k, len(uniq))))
    km = KMeans(n_clusters=k, n_init=4, random_state=seed).fit(lab)
    labels = km.labels_
    out = []
    for i in range(k):
        m = labels == i
        if not m.any():
            continue
        # use median RGB of members (robust, keeps real colors)
        rgb = np.median(px[m], axis=0)
        out.append({"hex": rgb_to_hex(rgb), "rgb": [int(x) for x in rgb], "ratio": float(m.mean()),
                    "lab": [round(float(x), 2) for x in srgb_to_lab(rgb)]})
    out.sort(key=lambda d: -d["ratio"])
    # merge near-duplicates (dE<4)
    merged = []
    for c in out:
        for mm in merged:
            if delta_e2000(c["lab"], mm["lab"]) < 4:
                mm["ratio"] += c["ratio"]
                break
        else:
            merged.append(dict(c))
    for c in merged:
        c["ratio"] = round(c["ratio"], 4)
    return merged


def write_json(path, obj):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)


def read_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)
