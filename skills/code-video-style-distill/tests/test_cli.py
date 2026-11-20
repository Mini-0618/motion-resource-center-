#!/usr/bin/env python3
"""CLI regression tests (local, no network). Run: .venv/bin/python tests/test_cli.py [--fast]
Checks:
  1. analyze flags pass through run.sh / cvsd.py: --no-ocr, --no-videomd, --scene-threshold
  2. missing audio file -> renderer warns and renders without audio (still render)
  3. stillcheck blocks (exit 1) when the background colour is wrong
  4. `all` stops at the human review point (no style dir) and stops on a live/3D precheck verdict
  5. ledger: comparing the same replica file twice is flagged duplicate and never makes DONE
  6. taxonomy: skill-internal table by default, --taxonomy / CVSD_TAXONOMY override, missing file -> clear error + unverified ids
  7. export-index: styles/*/ -> asset-index manifest, schema-valid, motion_center keys = motion_center.add_resource() fields,
     missing attribution.json -> warning (and exit 1 with --strict)
  8. rhythm.entrance_events_per_min = non-transition events / minutes, provenance seen, in schema
  9. Chinese subtitle rule: split_caption() keeps every cue <= 18 chars without losing text; the Remotion template really
     shows a long caption as one-line cues <= 18 chars (OCR of the rendered still)
 10. checklist U1-U3 / S10 exist; without OCR on the reference the subtitle items downgrade to should + not-testable;
     compare reports them not-testable when the replica has no OCR
 11. render backends: remotion / lemo / motion-canvas / hyperframes registered; lemo + hyperframes stills render;
     motion-canvas rejects unsupported segment types with a clear message (skipped with --fast)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

T = Path(__file__).resolve().parent.parent
PY = sys.executable
REF = T / "examples/reference-fixture-9/reference9.mp4"
RUN9 = T / "work/run9"
env = dict(os.environ, RIGHTS_OK="1")
results = []


def sh(*args, ok=(0,)):
    p = subprocess.run([PY, str(T / "cvsd.py"), *map(str, args)], env=env, capture_output=True, text=True)
    return p.returncode, p.stdout + p.stderr


def check(name, cond, info=""):
    results.append((name, bool(cond), info))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{info}]" if info else ""), flush=True)


tmp = Path(tempfile.mkdtemp(prefix="cvsd-test-"))
clip = tmp / "clip.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0", "-t", "9", "-i", str(REF), "-c:v", "libx264", "-crf", "20", "-an", str(clip)], check=True)

# 1. passthrough (bash wrapper and python entry)
rc, out = subprocess.run(["bash", str(T / "run.sh"), "analyze", str(clip), str(tmp / "a1"), "--no-ocr", "--no-videomd", "--scene-threshold", "0.95"],
                         env=env, capture_output=True, text=True).returncode, ""
A1 = json.loads((tmp / "a1/ref_analysis/analysis.json").read_text())
check("run.sh analyze --no-ocr reaches analyze.py", A1["params"]["no_ocr"] is True and not A1["ocr"].get("available"))
check("run.sh analyze --no-videomd reaches analyze.py", A1["params"]["no_videomd"] is True and not (tmp / "a1/ref_analysis/videomd").exists())
check("run.sh analyze --scene-threshold reaches analyze.py", A1["params"]["scene_threshold"] == 0.95)
rc, out = sh("analyze", clip, tmp / "a2")
A2 = json.loads((tmp / "a2/ref_analysis/analysis.json").read_text())
check("defaults without flags: OCR on, VIDEO.md written, threshold 0.30",
      A2["params"]["scene_threshold"] == 0.30 and A2["ocr"].get("available") and (tmp / "a2/ref_analysis/videomd/VIDEO.md").exists())
rc, out = sh("analyze", clip, tmp / "a3", "--no-ocr", "--no-videomd", "--scene-threshold", "0.02")
A3 = json.loads((tmp / "a3/ref_analysis/analysis.json").read_text())
check("--scene-threshold changes scene detection", len(A1["scenes"]) < len(A3["scenes"]),
      f"0.95 -> {len(A1['scenes'])} scenes, 0.30 -> {len(A2['scenes'])}, 0.02 -> {len(A3['scenes'])}")

# 2. missing audio -> warning, still renders
scr = json.loads((T / "examples/topic-demo-9/script.json").read_text())
scr["audio"] = {"src": "does-not-exist.wav"}
scr["segments"] = scr["segments"][:2]
for s in scr["segments"]:
    s.pop("image", None)
sp = tmp / "noaudio.json"
sp.write_text(json.dumps(scr, ensure_ascii=False))
p = subprocess.run(["node", "still.mjs", "--tokens", str(RUN9 / "style/style-tokens.json"), "--script", str(sp), "--times", "1.0", "--outdir", str(tmp / "na")],
                   cwd=T / "template", capture_output=True, text=True)
check("missing audio: warns and renders without audio", p.returncode == 0 and "WITHOUT audio" in (p.stdout + p.stderr) and (tmp / "na/still_0.png").exists())

# 3. stillcheck negative: wrong bg in tokens
bad = json.loads((RUN9 / "style/style-tokens.json").read_text())
bad["palette"]["bg"] = "#20242E"
bp = tmp / "bad-tokens.json"
bp.write_text(json.dumps(bad))
p = subprocess.run([PY, str(T / "scripts/stillcheck.py"), "--acceptance", str(RUN9 / "acceptance.json"), "--tokens", str(bp), "--script",
                    str(T / "examples/topic-demo-9/script.json"), "--ref-analysis", str(RUN9 / "ref_analysis"), "-o", str(tmp / "sc_bad")],
                   capture_output=True, text=True)
check("stillcheck exits non-zero on wrong background", p.returncode == 1 and "M2" in json.loads((tmp / "sc_bad/stillcheck.json").read_text())["blocking"])

# 4. `all` stops at review point; stops on live/3D precheck
w = tmp / "allw"
rc, out = sh("all", clip, w, "t-style", T / "examples/topic-demo-9/script.json", "--no-videomd")
check("all stops at the human review point", rc == 0 and "人工判断点" in out and not (w / "style").exists() and (w / "overrides.json").exists()
      and not (w / "ref_analysis/videomd").exists())
noise = tmp / "noise.mp4"
subprocess.run(["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", "nullsrc=s=1280x720:d=4,geq=random(1)*255:128:128,gblur=sigma=1.5",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", str(noise)], check=True)
rc, out = sh("all", noise, tmp / "livew", "t2", T / "examples/topic-demo-9/script.json")
check("all stops when precheck says live_ai_3d", rc == 4 and not (tmp / "livew/ref_analysis").exists(), f"rc={rc}")

# 5. ledger duplicate (needs a finished compare in work/run9)
if "--fast" not in sys.argv and (RUN9 / "iteration-ledger.json").exists():
    w5 = tmp / "dup"
    w5.mkdir()
    shutil.copy(RUN9 / "acceptance.json", w5 / "acceptance.json")
    (w5 / "style").mkdir()
    shutil.copy(RUN9 / "style/style-tokens.json", w5 / "style/style-tokens.json")
    os.symlink(RUN9 / "ref_analysis", w5 / "ref_analysis")
    led = json.loads((RUN9 / "iteration-ledger.json").read_text())
    rep = led["rounds"][-1]["replica"]
    rep_an = Path(led["rounds"][-1]["compare_dir"]) / "rep_analysis"
    for i in range(2):
        p = subprocess.run([PY, str(T / "scripts/compare.py"), "--ref", str(REF), "--rep", rep, "--checklist", str(w5 / "acceptance.json"),
                            "--ref-analysis", str(RUN9 / "ref_analysis"), "--rep-analysis", str(rep_an), "-o", str(w5 / f"c{i}"), "--samples", "2"],
                           capture_output=True, text=True)
    L = json.loads((w5 / "iteration-ledger.json").read_text())
    check("same replica compared twice: 2nd round flagged duplicate, not DONE",
          L["rounds"][1]["duplicate_replica"] and not L["status"].startswith("DONE") and "does NOT count" in p.stdout, L["status"])

# 6. taxonomy source resolution
sys.path.insert(0, str(T / "scripts"))
dt = subprocess.run([PY, str(T / "scripts/distill.py"), str(tmp / "a2/ref_analysis"), "-o", str(tmp / "d_def"), "--name", "t6"], capture_output=True, text=True, env=env)
D6 = json.loads((tmp / "d_def/style-tokens.json").read_text())
tx = [c["taxonomy"] for c in D6["components"]]
check("taxonomy: default = skill-internal references/motion-taxonomy.md, all ids verified",
      dt.returncode == 0 and tx and all(t["source"].endswith(os.path.join("references", "motion-taxonomy.md")) and t["verified"] for t in tx))
dt = subprocess.run([PY, str(T / "scripts/distill.py"), str(tmp / "a2/ref_analysis"), "-o", str(tmp / "d_miss"), "--name", "t6", "--taxonomy", str(tmp / "nope.md")],
                    capture_output=True, text=True, env=env)
D6m = json.loads((tmp / "d_miss/style-tokens.json").read_text())
check("taxonomy: missing file -> clear ERROR and every id marked UNVERIFIED",
      "taxonomy file not found" in dt.stderr and all(not c["taxonomy"]["verified"] and "UNVERIFIED" in c["taxonomy"]["names"].values() for c in D6m["components"] if c["taxonomy"]["ui"] + c["taxonomy"]["video"]))
mini = tmp / "mini-taxo.md"
mini.write_text("| 编号 | 分类名 | 关键词 |\n|---|---|---|\n| V-01 | 文字与动态排版 | x |\n", encoding="utf-8")
dt = subprocess.run([PY, str(T / "scripts/distill.py"), str(tmp / "a2/ref_analysis"), "-o", str(tmp / "d_env"), "--name", "t6"],
                    capture_output=True, text=True, env=dict(env, CVSD_TAXONOMY=str(mini)))
D6e = json.loads((tmp / "d_env/style-tokens.json").read_text())
check("taxonomy: CVSD_TAXONOMY env overrides; ids absent from the table are flagged",
      all(c["taxonomy"]["source"] == str(mini) for c in D6e["components"]) and "missing from" in dt.stderr
      and any(not c["taxonomy"]["verified"] for c in D6e["components"]))

# 7. export-index
sd = tmp / "styles"
shutil.copytree(T / "styles/paper-terminal-9", sd / "paper-terminal-9")
(sd / "t6").mkdir()
shutil.copy(tmp / "d_def/style-tokens.json", sd / "t6/style-tokens.json")  # no attribution.json on purpose
p = subprocess.run([PY, str(T / "cvsd.py"), "export-index", "--styles-dir", str(sd), "-o", str(tmp / "idx.json")], capture_output=True, text=True, env=env)
IDX = json.loads((tmp / "idx.json").read_text())
import jsonschema  # noqa: E402
try:
    jsonschema.validate(IDX, json.loads((T / "schema/asset-index.schema.json").read_text()))
    valid = True
except jsonschema.ValidationError:
    valid = False
a0 = next(a for a in IDX["assets"] if a["name"] == "paper-terminal-9")
mc_keys = {"title", "url", "source_pool", "category", "styles", "description", "prompt", "license", "source_url"}
check("export-index: schema-valid manifest with tokens summary / components / taxonomy / provenance / refs / license",
      p.returncode == 0 and valid and IDX["count"] == 2 and a0["taxonomy_ids"] and a0["refs"] and a0["provenance"]["counts"]["seen"] > 0
      and a0["license"]["refs_distributable"] is False and a0["license"]["reference_rights"] != "UNSPECIFIED"
      and a0["tokens_summary"]["rhythm"]["entrance_events_per_min"] is not None)
check("export-index: motion_center block uses motion-resource-center add_resource() keys",
      set(a0["motion_center"]) == mc_keys and a0["motion_center"]["source_pool"] in ("daily", "evergreen"))
p2 = subprocess.run([PY, str(T / "cvsd.py"), "export-index", "--styles-dir", str(sd), "-o", str(tmp / "idx2.json"), "--strict"], capture_output=True, text=True, env=env)
check("export-index: style without attribution.json -> UNSPECIFIED warning, --strict exits 1",
      "t6: no attribution.json" in p.stdout and p2.returncode == 1)

# 8. entrance-event density
A2m = A2["motion"]
exp = round(sum(1 for e in A2m["events"] if not e.get("is_transition")) / (A2["source"]["duration_s"] / 60.0), 2)
sch = json.loads((T / "schema/style-tokens.schema.json").read_text())
check("rhythm.entrance_events_per_min = non-transition events per minute (seen, in schema)",
      D6["rhythm"]["entrance_events_per_min"] == exp and D6["provenance"]["rhythm.entrance_events_per_min"]["status"] == "seen"
      and "entrance_events_per_min" in sch["properties"]["rhythm"]["properties"], f"{exp}/min")

# 9. subtitle <= 18 chars
from subtitle_rules import split_caption, count_chars  # noqa: E402
cases = ["今天用一分钟讲清 asyncio 的核心，再看三个**常见误区**和一个完整的可运行示例，最后总结。",
         "Python asyncio event loop scheduling explained in detail today", "短句"]
ok = True
for c in cases:
    parts = split_caption(c)
    strip = lambda x: "".join(ch for ch in x.replace("**", "") if ch.strip() and ch not in "，。、；：,.;:")  # noqa: E731
    ok &= all(count_chars(x) <= 18 for x in parts) and strip("".join(parts)) == strip(c)
check("split_caption: every cue <= 18 chars, no text lost", ok)
long_cap = "今天用一分钟讲清楚异步编程里的事件循环，再看三个最常见的错误写法和改法"
sc = {"title": "t", "segments": [{"type": "title", "duration_s": 4, "title": "字幕测试", "caption": long_cap}]}
sp9 = tmp / "longcap.json"
sp9.write_text(json.dumps(sc, ensure_ascii=False), encoding="utf-8")
p = subprocess.run(["node", "still.mjs", "--tokens", str(RUN9 / "style/style-tokens.json"), "--script", str(sp9), "--times", "0.5,3.5", "--outdir", str(tmp / "cap")],
                   cwd=T / "template", capture_output=True, text=True)
import cv2  # noqa: E402
ocr_lines = []
for i in range(2):
    im = cv2.imread(str(tmp / f"cap/still_{i}.png"))
    band = 255 - cv2.cvtColor(im[int(im.shape[0] * 0.80):, :], cv2.COLOR_BGR2GRAY)
    cv2.imwrite(str(tmp / f"cap/band_{i}.png"), band)
    o = subprocess.run(["tesseract", str(tmp / f"cap/band_{i}.png"), "-", "-l", "chi_sim+eng", "--psm", "6"], capture_output=True, text=True).stdout
    ocr_lines += [ln for ln in o.splitlines() if ln.strip()]
nchars = [sum(1 for ch in ln if ch.strip() and ch not in "，。、；：,.;:|") for ln in ocr_lines]
check("template splits a long caption into one-line cues <= 18 chars (OCR of rendered stills)",
      p.returncode == 0 and len(ocr_lines) == 2 and all(n <= 18 for n in nchars) and ocr_lines[0] != ocr_lines[1], f"{ocr_lines} -> {nchars}")

# 10. checklist subtitle / density items + downgrade without OCR
import checklist as CL  # noqa: E402
script9 = json.loads((T / "examples/topic-demo/script.json").read_text())
C_ocr = CL.build(D6, A2, script9, False, D6)
ids = {i["id"]: i for i in C_ocr["items"]}
check("checklist has U1 bar colour / U2 font size / U3 <=18 chars (must when seen) and S10 density",
      all(k in ids for k in ("U1", "U2", "U3", "S10")) and ids["U3"]["threshold"] == 18
      and all(ids[k]["tier"] == "must" for k in ("U1", "U2", "U3")) and ids["S10"]["tier"] == "should")
dn = subprocess.run([PY, str(T / "scripts/distill.py"), str(tmp / "a1/ref_analysis"), "-o", str(tmp / "d_noocr"), "--name", "t10"], capture_output=True, text=True, env=env)
Dn = json.loads((tmp / "d_noocr/style-tokens.json").read_text())
C_no = CL.build(Dn, A1, script9, False, Dn)
idn = {i["id"]: i for i in C_no["items"]}
check("no OCR on the reference -> U1-U3 downgraded to should + not-testable",
      all(idn[k]["tier"] == "should" and idn[k].get("force_not_testable") for k in ("U1", "U2", "U3")))
if "--fast" not in sys.argv and (T / "work/eng_base/acceptance.json").exists():
    p = subprocess.run([PY, str(T / "scripts/compare.py"), "--ref", str(REF), "--rep", str(clip), "--checklist", str(T / "work/eng_base/acceptance.json"),
                        "--ref-analysis", str(T / "work/eng_base/ref_analysis"), "--rep-analysis", str(tmp / "a1/ref_analysis"), "-o", str(tmp / "c10"),
                        "--samples", "2", "--ledger", str(tmp / "c10-ledger.json")], capture_output=True, text=True)
    R = {r["id"]: r for r in json.loads((tmp / "c10/metrics.json").read_text())["results"]}
    check("compare: replica without OCR -> U2/U3 not-testable (never a fake pass)",
          all(R[k]["result"] == "not-testable" for k in ("U2", "U3")), str({k: R[k]["result"] for k in ("U1", "U2", "U3", "S10")}))

# 11. backends
import renderers  # noqa: E402
check("render backends registered: remotion, lemo, motion-canvas, hyperframes",
      {"remotion", "lemo", "motion-canvas", "hyperframes"} <= set(renderers.BACKENDS))
if "--fast" not in sys.argv:
    from PIL import Image  # noqa: E402
    for r in ("lemo", "hyperframes"):
        try:
            rc, files = renderers.render_stills(RUN9 / "style/style-tokens.json", T / "examples/topic-demo/script.json", [1.5, 12.0], tmp / f"st_{r}", r)
            okr = rc == 0 and all(Image.open(f).size == (1920, 1080) for f in files)
        except SystemExit as e:
            okr, files = False, [str(e)]
        check(f"{r} backend renders stills (1920x1080 PNG)", okr, str(files)[:160])
    bad9 = tmp / "mc-bad.json"
    bad9.write_text(json.dumps({"segments": [{"type": "timeline", "duration_s": 2, "events": []}]}), encoding="utf-8")
    p = subprocess.run(["node", "capture.mjs", "stills", "--tokens", str(RUN9 / "style/style-tokens.json"), "--script", str(bad9), "--times", "0.5",
                        "--outdir", str(tmp / "mcbad")], cwd=T / "renderers/motion-canvas", capture_output=True, text=True)
    check("motion-canvas: unsupported segment type -> non-zero exit with the supported list", p.returncode != 0 and "not implemented in this backend" in (p.stdout + p.stderr))

shutil.rmtree(tmp, ignore_errors=True)
print(f"\n{sum(r[1] for r in results)}/{len(results)} passed")
sys.exit(0 if all(r[1] for r in results) else 1)
