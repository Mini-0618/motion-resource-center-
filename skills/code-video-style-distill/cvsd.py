#!/usr/bin/env python3
"""cvsd.py — cross-platform entry point for code-video-style-distill (same features as run.sh;
run.sh is now a thin wrapper around this file). Paths use pathlib; no bash needed (works in PowerShell).

  python cvsd.py precheck   <ref.mp4> <work> [precheck.py flags...]
  python cvsd.py analyze    <ref.mp4> <work> [analyze.py flags: --no-ocr --no-videomd --scene-threshold 0.4 ...]
  python cvsd.py distill    <work> <style-name> [--overrides overrides.json] [distill.py flags...]
  python cvsd.py checklist  <work> <script.json> [--same-content]
  python cvsd.py stillcheck <work> <script.json> [--renderer remotion]          # 3 settled stills: palette + layout gate
  python cvsd.py render     <work> <script.json> <out.mp4> [--renderer remotion]
  python cvsd.py compare    <ref.mp4> <work> <replica.mp4> [--note "..."] [compare.py flags...]
  python cvsd.py export-index [--styles-dir styles] [-o styles/asset-index.json] [--strict]  # styles/*/ -> asset-index manifest
  python cvsd.py beat       <out.wav> [--bpm 100] [--seconds 60]                 # ffmpeg click track for tests
  python cvsd.py all        <ref.mp4> <work> <style-name> <script.json> [--skip-review] [--rounds N] [--force] [--no-wait]
  python cvsd.py resume     <ref.mp4> <work> <style-name> <script.json> [--rounds N] [--no-wait]

`all` = stage 1 (precheck -> analyze) and STOPS at the human review point (look at the contact sheet
and keyframes, fill <work>/overrides.json), unless --skip-review. `resume` = stage 2, one round =
distill(+overrides) -> checklist (once) -> stillcheck (gate) -> render replica_rN -> compare; repeats
up to --rounds N (default 2), stops early on DONE / STALLED, and between rounds waits for you to edit
overrides.json (unless --no-wait). Every render is a new file, so an unchanged-parameter re-check is a
legitimate new round; comparing the same file twice is ignored by the ledger.

Scope gate: only reference videos you have the right to study. Set RIGHTS_OK=1 or pass --rights-ok.
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

TOOL = Path(__file__).resolve().parent
SCRIPTS = TOOL / "scripts"
sys.path.insert(0, str(SCRIPTS))
PY = sys.executable

GATE_MSG = """[scope gate] 只处理你有权参考的视频（自己的作品、已获授权、或仅用于内部风格学习的公开视频）。
             只学风格和结构；不搬运原片素材、字体文件、logo、商标、角色；不承诺像素级一致。
             确认后设置 RIGHTS_OK=1（PowerShell: $env:RIGHTS_OK=1）或加 --rights-ok 重新运行。"""

OVERRIDES_TEMPLATE = {
    "_readme": "人工判断点：看 ref_analysis/contact_sheet.png 和 ref_analysis/keyframes/ 后，把测错/没测到的值写在这里（和 style-tokens.json 同结构），"
               "并在 _provenance 里写明 status（seen=你亲眼核对过 / inferred=目测推断）。不需要修改就保持只有这两个键。",
    "_provenance": {},
}


def py(script, *args):
    cmd = [PY, str(SCRIPTS / script), *map(str, args)]
    print("[cvsd] $", " ".join(cmd), flush=True)
    return subprocess.run(cmd).returncode


def pop_flag(args, name):
    if name in args:
        args.remove(name)
        return True
    return False


def pop_opt(args, name, default=None):
    if name in args:
        i = args.index(name)
        v = args[i + 1]
        del args[i:i + 2]
        return v
    return default


def need(args, n, usage):
    if len(args) < n:
        print(f"usage: python cvsd.py {usage}")
        sys.exit(2)


def gate(args):
    if pop_flag(args, "--rights-ok") or os.environ.get("RIGHTS_OK") == "1":
        return
    print(GATE_MSG, file=sys.stderr)
    sys.exit(3)


def check(rc, what):
    if rc != 0:
        print(f"[cvsd] {what} failed (exit {rc}) — stopping.")
        sys.exit(rc)


def cmd_precheck(a):
    need(a, 2, "precheck <ref.mp4> <work> [flags]")
    return py("precheck.py", a[0], "-o", Path(a[1]) / "precheck", *a[2:])


def cmd_analyze(a):
    gate(a)
    need(a, 2, "analyze <ref.mp4> <work> [analyze.py flags]")
    return py("analyze.py", a[0], "-o", Path(a[1]) / "ref_analysis", *a[2:])


def overrides_effective(p):
    if not p or not Path(p).exists():
        return None
    d = json.loads(Path(p).read_text(encoding="utf-8"))
    return p if any(not k.startswith("_") for k in d) else None


def cmd_distill(a):
    need(a, 2, "distill <work> <style-name> [--overrides f] [flags]")
    work, name, rest = Path(a[0]), a[1], a[2:]
    ov = pop_opt(rest, "--overrides")
    if len(rest) == 1 and rest[0].endswith(".json"):  # run.sh legacy positional overrides
        ov, rest = rest[0], []
    ov = overrides_effective(ov)
    extra = ["--overrides", ov] if ov else []
    return py("distill.py", work / "ref_analysis", "-o", work / "style", "--name", name, "--styles-dir", TOOL / "styles", *extra, *rest)


def cmd_checklist(a):
    need(a, 2, "checklist <work> <script.json> [--same-content]")
    work = Path(a[0])
    return py("checklist.py", "--tokens", work / "style" / "style-tokens.json", "--ref-analysis", work / "ref_analysis", "--script", a[1],
              *a[2:], "-o", work / "acceptance.json")


def next_dir(work, prefix, suffix=""):
    n = 1
    while (Path(work) / f"{prefix}{n}{suffix}").exists():
        n += 1
    return Path(work) / f"{prefix}{n}{suffix}", n


def cmd_stillcheck(a):
    need(a, 2, "stillcheck <work> <script.json> [--renderer name]")
    work = Path(a[0])
    out, _ = next_dir(work, "stillcheck_r")
    return py("stillcheck.py", "--acceptance", work / "acceptance.json", "--tokens", work / "style" / "style-tokens.json", "--script", a[1],
              "--ref-analysis", work / "ref_analysis", "-o", out, *a[2:])


def cmd_render(a):
    need(a, 3, "render <work> <script.json> <out.mp4> [--renderer name]")
    import renderers
    rest = a[3:]
    r = pop_opt(rest, "--renderer")
    return renderers.render_video(Path(a[0]) / "style" / "style-tokens.json", a[1], a[2], r)


def cmd_compare(a):
    need(a, 3, "compare <ref.mp4> <work> <replica.mp4> [--note text] [flags]")
    ref, work, rep, rest = a[0], Path(a[1]), a[2], a[3:]
    note = pop_opt(rest, "--note", "")
    if rest and not rest[0].startswith("--"):  # run.sh legacy positional note
        note, rest = rest[0], rest[1:]
    out, _ = next_dir(work, "compare_r")
    return py("compare.py", "--ref", ref, "--rep", rep, "--checklist", work / "acceptance.json", "--ref-analysis", work / "ref_analysis",
              "--tokens", work / "style" / "style-tokens.json", "-o", out, "--note", note, *rest)


def cmd_beat(a):
    need(a, 1, "beat <out.wav> [--bpm 100] [--seconds 60]")
    bpm = float(pop_opt(a, "--bpm", 100))
    sec = float(pop_opt(a, "--seconds", 60))
    per = 60.0 / bpm
    Path(a[0]).parent.mkdir(parents=True, exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "lavfi", "-i", f"aevalsrc='0.6*sin(2*PI*1000*t)*exp(-60*mod(t,{per:.4f}))':s=44100:d={sec}",
           "-ac", "2", a[0]]
    rc = subprocess.run(cmd).returncode
    print(f"[beat] {a[0]} ({bpm} bpm, {sec}s)" if rc == 0 else "[beat] ffmpeg failed")
    return rc


def precheck_verdict(work):
    p = Path(work) / "precheck" / "precheck.json"
    return json.loads(p.read_text(encoding="utf-8")).get("verdict") if p.exists() else None


def cmd_all(a):
    need(a, 4, "all <ref.mp4> <work> <style-name> <script.json> [--skip-review] [--rounds N] [--force] [--no-wait]")
    gate(a)
    skip = pop_flag(a, "--skip-review")
    force = pop_flag(a, "--force")
    rounds = pop_opt(a, "--rounds", "2")
    nowait = pop_flag(a, "--no-wait")
    renderer = pop_opt(a, "--renderer")
    later = ["--rounds", rounds] + (["--no-wait"] if nowait else []) + (["--renderer", renderer] if renderer else [])
    ref, work, name, script = a[0], Path(a[1]), a[2], a[3]
    work.mkdir(parents=True, exist_ok=True)
    check(cmd_precheck([ref, str(work)]), "precheck")
    v = precheck_verdict(work)
    if v == "live_ai_3d" and not force:
        print(f"[cvsd] precheck verdict = {v}: 画面主体是实拍/AI/3D，本工具只能蒸馏包装层。已停止。确认仍要继续请加 --force。")
        sys.exit(4)
    check(cmd_analyze([ref, str(work), "--rights-ok", *a[4:]]), "analyze")  # remaining flags go to analyze.py
    ov = work / "overrides.json"
    if not ov.exists():
        ov.write_text(json.dumps(OVERRIDES_TEMPLATE, ensure_ascii=False, indent=2), encoding="utf-8")
    if not skip:
        ra = work / "ref_analysis"
        print(f"""
[cvsd] ===== 人工判断点（stage 1 完成）=====
  1. 看总览：{ra / 'contact_sheet.png'}
  2. 看关键帧：{ra / 'keyframes'}（entry / mid / settled）和 {ra / 'motion_energy.png'}
  3. 把测错或没测到的值写进 {ov}（字体气质、display 字号、转场类型、装饰…），在 _provenance 标 seen/inferred
  4. 继续：python cvsd.py resume "{ref}" "{work}" {name} "{script}" --rounds {rounds}
  （确实不需要人工判断时，可用 all ... --skip-review 一次跑完）""")
        return 0
    return cmd_resume([ref, str(work), name, script, *later])


def cmd_resume(a):
    need(a, 4, "resume <ref.mp4> <work> <style-name> <script.json> [--rounds N] [--no-wait] [--renderer name]")
    rounds = int(pop_opt(a, "--rounds", 2))
    nowait = pop_flag(a, "--no-wait")
    renderer = pop_opt(a, "--renderer")
    rflag = ["--renderer", renderer] if renderer else []
    ref, work, name, script = a[0], Path(a[1]), a[2], a[3]
    ov = work / "overrides.json"
    for i in range(rounds):
        check(cmd_distill([str(work), name, "--overrides", str(ov)]), "distill")
        if not (work / "acceptance.json").exists():
            check(cmd_checklist([str(work), script]), "checklist")
        t0 = time.time()
        rc = cmd_stillcheck([str(work), script, *rflag])
        t_still = time.time() - t0
        if rc != 0:
            print("[cvsd] 静帧预检未通过 — 不做全片渲染。按最新 stillcheck_rN/stillcheck.md 修 overrides.json 后再 resume。")
            sys.exit(rc)
        rep, n = next_dir(work, "replica_r", ".mp4")
        t0 = time.time()
        check(cmd_render([str(work), script, str(rep), *rflag]), "render")
        t_render = time.time() - t0
        print(f"[cvsd] timing round {n}: stillcheck {t_still:.1f}s vs full render {t_render:.1f}s "
              f"(a failing stillcheck saves {100 * (1 - t_still / max(t_render, 1e-6)):.0f}% of the render time)")
        check(cmd_compare([ref, str(work), str(rep), "--note", f"round {n}: overrides={'yes' if overrides_effective(str(ov)) else 'none'}"]), "compare")
        led = json.loads((work / "iteration-ledger.json").read_text(encoding="utf-8"))
        st = led.get("status", "")
        print(f"[cvsd] round {n}: ledger status = {st}")
        if st.startswith("DONE") or st.startswith("STALLED"):
            return 0
        if i < rounds - 1 and not nowait and sys.stdin.isatty():
            input(f"[cvsd] 看最新 compare_rN/gap-report.md，改 {ov} 后按回车继续下一轮（Ctrl+C 退出）…")
    print("[cvsd] 已跑完设定轮数但未 DONE：看 gap-report 后继续 `resume ... --rounds N`。")
    return 0


def cmd_export_index(a):
    return py("export_index.py", *a)


CMDS = {"export-index": cmd_export_index, "precheck": cmd_precheck, "analyze": cmd_analyze, "distill": cmd_distill, "checklist": cmd_checklist, "stillcheck": cmd_stillcheck,
        "render": cmd_render, "compare": cmd_compare, "beat": cmd_beat, "all": cmd_all, "resume": cmd_resume}

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in CMDS:
        print(__doc__)
        sys.exit(0 if len(sys.argv) < 2 else 2)
    sys.exit(CMDS[sys.argv[1]](sys.argv[2:]) or 0)
