"""components_detect.py — pixel detectors for the knowledge-video components
(evidence screenshot frame, timeline, two-column compare, flow chart).

Each detector reads ONE settled keyframe PNG and returns None or a params dict whose keys
mirror style-tokens.json -> components_style.<name>. Heuristics, written from scratch for this tool.
"""
import cv2
import numpy as np

from cvsd_common import srgb_to_lab, hex_to_rgb, rgb_to_hex


def _load(png):
    img = cv2.cvtColor(cv2.imread(png), cv2.COLOR_BGR2RGB)
    return img, srgb_to_lab(img.reshape(-1, 3).astype(float)).reshape(img.shape)


def _de(lab, hexv):
    return np.sqrt(((lab - srgb_to_lab(np.array(hex_to_rgb(hexv), float))) ** 2).sum(-1))


def _r(v, n=1):
    return round(float(v), n)


def _hex_med(px):
    return rgb_to_hex(np.median(px.reshape(-1, 3), 0)) if px.size else None


def _corner_radius(mask, x, y, w, h):
    """distance along the top-left diagonal until the mask is hit (≈ r*(1-1/√2))."""
    for k in range(0, min(w, h) // 2):
        if mask[y + k, x + k]:
            return int(round(k / (1 - 1 / np.sqrt(2)))) if k > 1 else 0
    return 0


def _chromatic(rgb, lim=40):
    return (rgb.max(-1).astype(int) - rgb.min(-1).astype(int)) > lim


def detect_evidence(png, bg_hex):
    """large textured (photo/screenshot-like) region + chromatic outline box inside it."""
    img, lab = _load(png)
    H, W = img.shape[:2]
    g = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY).astype(np.float32)
    mu = cv2.blur(g, (5, 5))
    sd = np.sqrt(np.maximum(cv2.blur(g * g, (5, 5)) - mu * mu, 0))
    tex = ((sd > 2.0) & (_de(lab, bg_hex) > 8)).astype(np.uint8)
    tex = cv2.morphologyEx(tex, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lb, st, _ = cv2.connectedComponentsWithStats(tex)
    if n < 2:
        return None
    i = 1 + int(np.argmax(st[1:, 4]))
    x, y, w, h, a = st[i]
    if a < 0.10 * W * H or a / (w * h) < 0.6:
        return None
    inner = (sd[y:y + h, x:x + w] > 2.0).mean()
    if inner < 0.45:
        return None
    # frame stroke colour: thin ring just outside / on the region border
    # frame stroke: the darkest/most distinct thin row band hugging the top edge (inside → outside)
    cand = [img[yy, x + w // 4:x + 3 * w // 4] for yy in range(max(0, y - 4), min(H, y + 3))]
    ring = max(cand, key=lambda r: float(np.mean(_de(srgb_to_lab(r.astype(float)), bg_hex))))
    # highlight: chromatic connected component inside the region that is a hollow rectangle
    roi = img[y:y + h, x:x + w]
    ch = _chromatic(roi, 60).astype(np.uint8)
    m, lb2, st2, _ = cv2.connectedComponentsWithStats(ch)
    best = None
    for j in range(1, m):
        bx, by, bw, bh, ba = st2[j]
        if bw > w * 0.08 and bh > h * 0.05 and ba / (bw * bh) < 0.45:
            if best is None or ba > best[4]:
                best = (bx, by, bw, bh, ba, j)
    out = {"box_pct": [_r(x * 100 / W), _r(y * 100 / H), _r(w * 100 / W), _r(h * 100 / H)],
           "frame_color": _hex_med(ring), "textured_ratio": round(float(inner), 2)}
    if best:
        bx, by, bw, bh, ba, j = best
        out["highlight_color"] = _hex_med(roi[lb2 == j])
        out["highlight_stroke_px"] = int(round(ba / max(1, 2 * (bw + bh))))
        out["highlight_box_pct"] = [_r(bx * 100 / w), _r(by * 100 / h), _r(bw * 100 / w), _r(bh * 100 / h)]
    return out


def detect_timeline(png, bg_hex):
    """long thin horizontal line (not at frame edges) with ≥3 round nodes centred on it."""
    img, lab = _load(png)
    H, W = img.shape[:2]
    fg = (_de(lab, bg_hex) > 18).astype(np.uint8)
    line = cv2.morphologyEx(fg, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_RECT, (int(W * 0.2), 1)))
    n, lb, st, _ = cv2.connectedComponentsWithStats(line)
    cands = [st[i] for i in range(1, n) if st[i][2] > W * 0.4 and st[i][3] < H * 0.015 and H * 0.12 < st[i][1] < H * 0.85]
    if not cands:
        return None
    lx, ly, lw, lh, _ = max(cands, key=lambda s: s[2])
    cy = ly + lh / 2
    m, lb2, st2, cen = cv2.connectedComponentsWithStats(fg)
    nodes = []
    for j in range(1, m):
        x, y, w, h, a = st2[j]
        if j and abs(cen[j][1] - cy) < max(h, 6) and H * 0.012 < h < H * 0.06 and 0.6 < w / max(h, 1) < 1.6 and a / (w * h) > 0.55:
            nodes.append((x, y, w, h, j))
    if len(nodes) < 3:
        # nodes may be merged with the line in the fg mask: find blobs on the vertical profile
        band = fg[int(cy - H * 0.04):int(cy + H * 0.04), lx:lx + lw]
        thick = cv2.morphologyEx(band, cv2.MORPH_OPEN, np.ones((max(3, int(lh * 3)), max(3, int(lh * 3))), np.uint8))
        k, lb3, st3, _ = cv2.connectedComponentsWithStats(thick)
        nodes = []
        for j in range(1, k):
            x, y, w, h, a = st3[j]
            if H * 0.012 < h < H * 0.06 and 0.6 < w / max(h, 1) < 1.6:
                nodes.append((x + lx, y + int(cy - H * 0.04), w, h, None))
    if len(nodes) < 3:
        return None
    node_px = np.concatenate([img[y + h // 4:y + 3 * h // 4, x + w // 4:x + 3 * w // 4].reshape(-1, 3) for x, y, w, h, _ in nodes])
    xs = sorted(x for x, *_ in nodes)
    seg = []
    for a_, b_ in zip(xs[:-1], xs[1:]):
        mid = (a_ + b_) // 2
        seg.append(img[int(cy), max(lx, mid - 5):mid + 5])
    line_px = np.concatenate(seg) if seg else img[int(cy), lx:lx + lw]
    return {"node_count": len(nodes), "node_color": _hex_med(node_px), "node_size_px": int(np.median([h for *_, h, _ in nodes])),
            "line_color": _hex_med(line_px), "line_px": int(lh), "line_y_pct": round(float(cy) * 100 / H, 1),
            "line_span_pct": round(float(lw) * 100 / W, 1)}


def _surface_rects(img, lab, surface_hex, min_a, max_a):
    H, W = img.shape[:2]
    m = (_de(lab, surface_hex) < 8).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((15, 15), np.uint8))
    cs, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = []
    for c in cs:
        x, y, w, h = cv2.boundingRect(c)
        if min_a * W * H <= w * h <= max_a * W * H and cv2.contourArea(c) / (w * h) > 0.88:
            out.append((x, y, w, h))
    return out, m


def detect_compare(png, surface_hex):
    """exactly two equal-height surface panels side by side."""
    img, lab = _load(png)
    H, W = img.shape[:2]
    rects, m = _surface_rects(img, lab, surface_hex, 0.06, 0.45)
    best = None
    for i in range(len(rects)):
        for j in range(len(rects)):
            a, b = rects[i], rects[j]
            if i == j or a[0] >= b[0] or a[0] + a[2] > b[0]:
                continue
            if abs(a[1] - b[1]) < H * 0.03 and abs(a[3] - b[3]) < H * 0.05 and abs(a[2] - b[2]) < W * 0.08:
                best = (a, b)
    if not best:
        return None
    a, b = best
    px = np.concatenate([img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]][m[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] > 0] for r in best])
    out = {"panel_fill": _hex_med(px), "gap_pct": _r((b[0] - a[0] - a[2]) * 100 / W, 2), "radius_px": _corner_radius(m, *a),
           "panel_w_pct": _r(a[2] * 100 / W)}
    # highlight marker: thin vertical chromatic bar inside a panel
    for r in best:
        roi = img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]]
        ch = _chromatic(roi, 60).astype(np.uint8)
        k, lb, st, _ = cv2.connectedComponentsWithStats(ch)
        for j in range(1, k):
            x, y, w, h, ar = st[j]
            if 2 <= w <= 14 and H * 0.02 < h < H * 0.1 and ar / (w * h) > 0.8:
                out["highlight_color"] = _hex_med(roi[lb == j])
                break
        if "highlight_color" in out:
            break
    return out


def detect_flow(png, surface_hex, bg_hex):
    """≥3 similar surface boxes aligned in a row or column; stroke ring + connector colour."""
    img, lab = _load(png)
    H, W = img.shape[:2]
    rects, m = _surface_rects(img, lab, surface_hex, 0.004, 0.06)
    if len(rects) < 3:
        return None
    for orient in ("horizontal", "vertical"):
        key = (lambda r: r[1] + r[3] / 2) if orient == "horizontal" else (lambda r: r[0] + r[2] / 2)
        tol = H * 0.02 if orient == "horizontal" else W * 0.02
        rects.sort(key=key)
        groups, cur = [], [rects[0]]
        for r in rects[1:]:
            if abs(key(r) - key(cur[-1])) < tol:
                cur.append(r)
            else:
                groups.append(cur)
                cur = [r]
        groups.append(cur)
        g = max(groups, key=len)
        if len(g) >= 3 and np.std([r[2] * r[3] for r in g]) / np.mean([r[2] * r[3] for r in g]) < 0.35:
            break
    else:
        return None
    g.sort(key=(lambda r: r[0]) if orient == "horizontal" else (lambda r: r[1]))
    px = np.concatenate([img[r[1]:r[1] + r[3], r[0]:r[0] + r[2]][m[r[1]:r[1] + r[3], r[0]:r[0] + r[2]] > 0] for r in g])
    x, y, w, h = g[0]
    ring = np.concatenate([img[max(0, y - 2), x + 10:x + w - 10], img[min(H - 1, y + h + 1), x + 10:x + w - 10]])
    conn = []
    bgd = _de(lab, bg_hex)
    for a, b in zip(g[:-1], g[1:]):
        if orient == "horizontal":
            yy = int(a[1] + a[3] / 2)
            seg = slice(a[0] + a[2] + 6, b[0] - 6)
            sel = bgd[yy, seg] > 15
            conn.append(img[yy, seg][sel])
        else:
            xx = int(a[0] + a[2] / 2)
            seg = slice(a[1] + a[3] + 6, b[1] - 6)
            sel = bgd[seg, xx] > 15
            conn.append(img[seg, xx][sel])
    cp = np.concatenate(conn) if conn else np.zeros((0, 3))
    return {"node_count": len(g), "orientation": orient, "node_fill": _hex_med(px), "node_stroke": _hex_med(ring),
            "arrow_color": _hex_med(cp) if len(cp) else None, "radius_px": _corner_radius(m, *g[0]),
            "node_w_pct": _r(np.median([r[2] for r in g]) * 100 / W)}
