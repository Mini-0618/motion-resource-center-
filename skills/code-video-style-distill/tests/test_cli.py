#!/usr/bin/env python3
"""CLI regression tests (local, no network). Run: .venv/bin/python tests/test_cli.py [--fast]
Checks:
  1. analyze flags pass through run.sh / cvsd.py: --no-ocr, --no-videomd, --scene-threshold
  2. missing audio file -> renderer warns and renders without audio (still render)
  3. stillcheck blocks (exit 1) when the background colour is wrong
  4. `all` stops at the human review point (no style dir) and stops on a live/3D precheck verdict
  5. ledger: comparing the same replica file twice is flagged duplicate and never makes DONE
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

shutil.rmtree(tmp, ignore_errors=True)
print(f"\n{sum(r[1] for r in results)}/{len(results)} passed")
sys.exit(0 if all(r[1] for r in results) else 1)
