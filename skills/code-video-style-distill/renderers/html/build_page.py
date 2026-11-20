#!/usr/bin/env python3
"""build_page.py — style-tokens.json + script.json -> a self-contained HTML page folder (index.html + runtime.js + assets).

The page follows the Lemo-Opuscar page contract (window.READY / window.DUR / window.render(t) / window.TEXTS(t)),
so lemo's core/render/{video,still}.mjs can record it unchanged; the same page is reused by other frame-seek
capture backends. Same content/style decoupling checks as template/prepare.mjs.

Usage: build_page.py --tokens t.json --script s.json --outdir demo/
Prints a JSON line: {"dir":..., "fps":..., "width":..., "height":..., "duration_s":..., "audio": <abs path or null>}
"""
import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STYLE_KEYS = ["palette", "typography", "layout", "motion", "canvas", "components_style"]


def build(tokens_p, script_p, outdir, hyperframes=False):
    T = json.load(open(tokens_p, encoding="utf-8"))
    S = json.load(open(script_p, encoding="utf-8"))
    leaked = [k for k in STYLE_KEYS if k in S]
    if leaked:
        sys.exit(f"[page] script.json must not carry style keys ({', '.join(leaked)}).")
    if "segments" in T:
        sys.exit("[page] style-tokens.json must not carry content (segments).")
    os.makedirs(os.path.join(outdir, "assets"), exist_ok=True)
    base = os.path.dirname(os.path.abspath(script_p))
    audio = None
    if (S.get("audio") or {}).get("src"):
        a = os.path.join(base, S["audio"]["src"])
        if os.path.exists(a):
            audio = a
        else:
            print(f"[page] WARNING audio file not found: {a} — rendering WITHOUT audio", file=sys.stderr)
        S.pop("audio", None)
    preload = []
    for i, s in enumerate(S.get("segments", [])):
        if s.get("type") == "evidence" and s.get("image"):
            src = os.path.join(base, s["image"])
            if not os.path.exists(src):
                sys.exit(f"[page] evidence image not found: {src}")
            name = f"evidence_{i}_{os.path.basename(src)}"
            shutil.copy(src, os.path.join(outdir, "assets", name))
            s["image_url"] = "assets/" + name
            preload.append(s["image_url"])
            if not s.get("source"):
                print(f"[page] WARNING segment {i}: evidence without source — add \"source\" before publishing", file=sys.stderr)
    shutil.copy(os.path.join(HERE, "runtime.js"), os.path.join(outdir, "runtime.js"))
    cv = {**{"width": 1920, "height": 1080, "fps": 30}, **(T.get("canvas") or {})}
    fps0 = round(cv["fps"])
    dur0 = sum(max(1, round((s.get("duration_s") or 4) * fps0)) for s in S.get("segments", [])) / fps0
    root_attrs = ""
    hf_js = ""
    if hyperframes:
        # HyperFrames composition contract: root element with data-composition-id/start/duration/width/height;
        # frames are driven by the runtime's `hf-seek` event (the adapter hook its Three.js/TypeGPU docs describe).
        root_attrs = (f' data-composition-id="cvsd" data-start="0" data-duration="{dur0:.4f}"'
                      f' data-width="{cv["width"]}" data-height="{cv["height"]}"')
        hf_js = ("<script>window.addEventListener('hf-seek', function (e) { var d = e.detail || {}; "
                 "var t = typeof d === 'number' ? d : (d.time != null ? d.time : d.t); if (window.render && t != null) window.render(t); });</script>")
    cfg = json.dumps({"tokens": T, "script": S, "preload": preload}, ensure_ascii=False).replace("</", "<\\/")
    html = f"""<!doctype html>
<html><head><meta charset="utf-8"><title>cvsd page</title>
<style>*{{box-sizing:border-box}}html,body{{margin:0;padding:0;background:#000;overflow:hidden}}#stage{{position:relative}}</style></head>
<body><div id="stage"{root_attrs}></div>
<script>window.CVSD = {cfg};</script>
<script src="runtime.js"></script>
{hf_js}
</body></html>
"""
    with open(os.path.join(outdir, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    fps = round(cv["fps"])
    frames = sum(max(1, round((s.get("duration_s") or 4) * fps)) for s in S.get("segments", []))
    return {"dir": os.path.abspath(outdir), "fps": fps, "width": cv["width"], "height": cv["height"], "duration_s": frames / fps, "frames": frames, "audio": audio}


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--tokens", required=True)
    ap.add_argument("--script", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--hyperframes", action="store_true", help="add the HyperFrames composition attributes + hf-seek listener")
    a = ap.parse_args()
    print(json.dumps(build(a.tokens, a.script, a.outdir, a.hyperframes)))
