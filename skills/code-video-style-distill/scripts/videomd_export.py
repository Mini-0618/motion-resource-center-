#!/usr/bin/env python3
"""videomd_export.py — write analysis/ as a VIDEO.md package (optional intermediate artefact).

Usage: videomd_export.py <analysis_dir> [-o <analysis_dir>/videomd] [--lang zh]

Format: VIDEO.md v1 by videomd/videomd — specification and docs licensed CC BY 4.0
(https://github.com/videomd/videomd, © videomd contributors); its code/schema are Apache-2.0.
This exporter is an independent implementation written from the public spec; no videomd code is
copied or installed. Seen vs inferred follows the spec: timeline keys ending in "~" are inferred.
The package is a "how this video was made" breakdown; it does NOT replace style-tokens.json.
"""
import argparse
import os
import re
import shutil
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from cvsd_common import read_json  # noqa: E402
from precheck import frame_stats, score as pc_score  # noqa: E402

TR_MAP = {"slide": "slide", "fade": "dissolve", "zoom": "zoom", "wipe": "wipe"}


def yaml_dump(d):
    import yaml
    return yaml.safe_dump(d, allow_unicode=True, sort_keys=False, default_flow_style=None, width=1000).strip()


def tok(s):
    return max(1, int(len(s) / 3))


def kebab(s):
    s = re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")
    s = re.sub(r"-+", "-", s)
    return (s or "video")[:64].strip("-") or "video"


def clean(s):
    return str(s).replace("|", "/").replace("\n", " ").strip()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("analysis_dir")
    ap.add_argument("-o", "--out")
    ap.add_argument("--lang", default="zh")
    a = ap.parse_args()
    A = read_json(os.path.join(a.analysis_dir, "analysis.json"))
    out = a.out or os.path.join(a.analysis_dir, "videomd")
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(os.path.join(out, "video", "shots"))
    os.makedirs(os.path.join(out, "frames"))
    src = A["source"]
    scenes = A["scenes"]
    events = A["motion"]["events"]
    subs_scenes = {l["scene"] for l in A.get("ocr", {}).get("lines", []) if l["pos_pct"]["y"] > 78 and abs(l["pos_pct"]["cx"] - 50) < 6}
    lines, made_tot = [], {}
    nd = max(2, len(str(len(scenes))))
    for s in scenes:
        n = s["index"] + 1
        t0, t1 = round(s["start_s"], 3), round(min(s["end_s"], src["duration_s"]), 3)
        # frames: entry/mid/settled side by side
        ims = [cv2.imread(s["keyframes"][k]["path"]) for k in ("entry", "mid", "settled")]
        ims = [cv2.resize(i, (480, int(i.shape[0] * 480 / i.shape[1]))) for i in ims]
        fpath = f"frames/{n:0{nd}d}.jpg"
        cv2.imwrite(os.path.join(out, fpath), np.hstack(ims))
        img = cv2.cvtColor(cv2.imread(s["keyframes"]["settled"]["path"]), cv2.COLOR_BGR2RGB)
        f, c, nz = frame_stats(cv2.resize(img, (960, int(img.shape[0] * 960 / img.shape[1]))))
        p = round(min(0.97, max(0.03, pc_score(f, c, nz))), 2)
        made = "code_render" if p >= 0.5 else "live_action"
        pm = p if made == "code_render" else round(1 - p, 2)
        made_tot[made] = made_tot.get(made, 0) + (t1 - t0)
        txt = [clean(x) for x in s.get("ocr_lines", [])][:4]
        sev = [e for e in events if t0 <= e["start_s"] < t1 and not e["is_transition"]]
        tr = [e for e in events if e["is_transition"] and abs(e["start_s"] - t0) < 1.0 and n > 1]
        overlays = ["subtitle"] if s["index"] in subs_scenes else []
        if txt:
            overlays.append("styled_text")
        seen = f"画面文字：{' / '.join(txt)}" if txt else "无可读文字"
        fields = [f"seen {seen}；{len(sev)} 个入场/运动事件", "camera static"]
        trans = None
        if tr:
            g = tr[0].get("entry_type_guess", "fade")
            trans = "slide" if g.startswith("slide") else "zoom" if g.startswith("scale") else "dissolve"
            fields.append(f"transition {trans} {tr[0]['core_duration_s']}s")
        if overlays:
            fields.append(f"overlay {', '.join(overlays)}")
        fields.append(f"made~ {'code render' if made == 'code_render' else 'filmed'} {int(pm * 100)}%")
        fields.append("remake 用 style-tokens.json + Remotion 模板重建，换 script.json 内容")
        if pm < 0.6:
            fields.append("flag low confidence")
        lines.append(f"#{n:0{nd}d} {t0}-{t1} | " + " | ".join(clean(x) for x in fields))
        fm = {"videomd": 1, "part": "shot", "shot": n, "time": [t0, t1], "camera": "static", "overlays": overlays,
              "inferred": {"made": made, "p": pm, "alternatives": {("live_action" if made == "code_render" else "code_render"): round(1 - pm, 2)},
                           "decided_by": "tools", "real_material": made != "code_render"},
              "flags": ["low_confidence"] if pm < 0.6 else [], "frames": {"sheet": fpath}}
        if trans:
            fm["transition_in"] = {"type": trans, "time": [round(max(0, tr[0]["start_s"]), 3), round(max(t0 + 0.001, min(t1, tr[0]["end_s"])), 3)]}
            if not (fm["transition_in"]["time"][0] <= t0 <= fm["transition_in"]["time"][1]):
                fm["transition_in"]["time"] = [round(max(0, t0 - 0.01), 3), round(min(t1, t0 + tr[0]["core_duration_s"]), 3)]
        body = (f"# Shot {n} · {t0}–{t1}s\n\n## Seen\n\n{seen}。运动事件起点：{', '.join(e['start_tc'] for e in sev) or '无'}。\n\n"
                f"## Inferred\n\n{'代码/模板渲染' if made == 'code_render' else '实拍'}（{int(pm * 100)}%）：平涂像素占比 {f:.2f}、色彩集中度 {c:.2f}、噪声 σ {nz:.2f}。"
                f"缓动推测：{', '.join(sorted({e['easing_guess'] for e in sev})) or '—'}。\n\n## Remake\n\n用风格底座 tokens + Remotion 模板重建本镜头结构，内容换成新选题。\n")
        fm["tokens"] = tok(body) + 60
        with open(os.path.join(out, "video", "shots", f"{n:0{nd}d}.md"), "w", encoding="utf-8") as fh:
            fh.write("---\n" + yaml_dump(fm) + "\n---\n\n" + body)
    tl_body = "# Timeline\n\n```videomd-timeline\n" + "\n".join(lines) + "\n```\n"
    with open(os.path.join(out, "video", "timeline.md"), "w", encoding="utf-8") as fh:
        fh.write("---\n" + yaml_dump({"videomd": 1, "part": "timeline", "shots": len(scenes), "tokens": tok(tl_body)}) + "\n---\n\n" + tl_body)
    D = src["duration_s"]
    mix = {k: round(v / D, 2) for k, v in made_tot.items()}
    texts = [x for s in scenes for x in s.get("ocr_lines", [])][:3]
    desc = (f"A {D:.0f}-second motion video in {len(scenes)} shots" + (f" with on-screen text such as '{clean(texts[0])}'" if texts else "") +
            f". Made with (inferred): " + ", ".join(f"{k} {int(v * 100)}%" for k, v in mix.items()) + ".")
    card = {"videomd": 1, "name": kebab(os.path.splitext(os.path.basename(src["path"]))[0]), "description": desc[:1000],
            "source": {"file": os.path.basename(src["path"]), "duration": D, "size": f"{src['width']}x{src['height']}", "fps": src["fps"],
                       "aspect": src["aspect"]},
            "shots": len(scenes), "lang": a.lang, "made_mix": mix, "confidence": 0.7, "readers": ["tools"],
            "open_questions": 1, "generator": {"name": "code-video-style-distill", "version": "1"}}
    shot_tok = max(1, int(np.mean([tok(open(os.path.join(out, "video", "shots", x), encoding="utf-8").read()) for x in os.listdir(os.path.join(out, "video", "shots"))])))
    body = (f"# {os.path.basename(src['path'])}\n\n**What it shows**: {desc}\n\n## Open questions\n\n"
            "- 字体气质、装饰元素、转场类型（wipe/fade）需要看 `frames/` 确认。\n\n## Map\n\n```videomd-map\n"
            f"video/timeline.md | {tok(tl_body)} | One line per shot · which shot does what\n"
            f"video/shots/*.md | {shot_tok} | One file per shot · checking one shot\n"
            "frames/ | - | Shot frames (entry / mid / settled) · checking by eye\n```\n\n"
            "Read the timeline first, then one shot file. Keys ending in `~` are inferred.\n\n"
            "_Format: VIDEO.md v1, specification © videomd contributors, CC BY 4.0 — https://github.com/videomd/videomd_\n")
    with open(os.path.join(out, "VIDEO.md"), "w", encoding="utf-8") as fh:
        fh.write("---\n" + yaml_dump(card) + "\n---\n\n" + body)
    print(f"[videomd] wrote {out}/VIDEO.md ({len(scenes)} shots)")
    # optional: validate with a LOCAL read-only copy of the reference checker if present (not installed)
    ref = os.environ.get("VIDEOMD_SRC", "/workspace/ip-team/research/rea/videomd/src")
    if os.path.isdir(os.path.join(ref, "videomd")):
        sys.path.insert(0, ref)
        try:
            import videomd
            errs = videomd.check(out)
            print("[videomd] reference checker: " + ("conforms" if not errs else "ERRORS:\n  " + "\n  ".join(map(str, errs))))
        except Exception as ex:
            print(f"[videomd] reference checker unavailable: {ex}")


if __name__ == "__main__":
    main()
