"""renderers.py — the replaceable render layer.

Contract (any backend):  style-tokens.json + script.json  ->  out.mp4   (render_video)
                         style-tokens.json + script.json + [t_s...] -> PNGs (render_stills, for stillcheck)
Both files are validated for content/style decoupling by the backend. Timeline semantics every
backend must keep (stillcheck relies on it): segments play in order, each lasts duration_s; segment i>0
starts motion.transition.duration_s earlier (overlap) unless its transition is "cut".

Backends:
  "remotion"      (default) template/ — React. Remotion has its own company licence: check
                  https://www.remotion.dev/license before commercial team use.
  "lemo"          renderers/html page (own MIT runtime, Lemo-Opuscar page contract) recorded by Lemo-Opuscar's
                  own core/render/{video,still}.mjs (MIT). Needs a local Lemo checkout: env LEMO_HOME
                  (default work/_ext/lemo-opuscar) with `npm install` done; Chrome via PLAYWRIGHT_CHROME.
  "motion-canvas" renderers/motion-canvas — Motion Canvas 3.17 (MIT) scene, captured frame-by-frame in headless
                  Chrome through the project's Player API (MC has no official headless CLI).
  "hyperframes"   the same renderers/html page + HyperFrames composition attributes, driven by HyperFrames' `hf-seek`
                  event and recorded by the `hyperframes` CLI (Apache-2.0, needs Node >= 22). Local checkout:
                  env HYPERFRAMES_HOME (default work/_ext/hyperframes, `npm install hyperframes@0.9.72`).
                  Telemetry/update checks are switched off; publish/auth/cloud commands are never called.
Select with env CVSD_RENDERER or --renderer. A backend is either two command builders (video/stills, run in
`cwd`) or two Python callables (video_fn/stills_fn) with the same contract.
"""
import datetime as _dt
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent
HTML = TOOL / "renderers" / "html"


def _chrome():
    for p in (os.environ.get("PLAYWRIGHT_CHROME"), os.environ.get("REMOTION_BROWSER"), "/usr/bin/google-chrome", "/usr/bin/chromium",
              "/usr/bin/chromium-browser", r"C:\Program Files\Google\Chrome\Application\chrome.exe"):
        if p and os.path.exists(p):
            return p
    return None


def _page(tok, scr, outdir):
    sys.path.insert(0, str(HTML))
    import build_page
    return build_page.build(tok, scr, outdir)


def _finish_mp4(silent, audio, out):
    """mux optional audio + write a unique metadata comment (every render is a distinct file for the ledger)."""
    stamp = f"code-video-style-distill render {_dt.datetime.now().isoformat()}"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", silent]
    if audio:
        cmd += ["-i", audio, "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k", "-shortest"]
    cmd += ["-c:v", "copy", "-metadata", f"comment={stamp}", "-movflags", "+faststart", out]
    return subprocess.run(cmd).returncode


def _jpgs_to_pngs(files, outdir):
    from PIL import Image
    outs = []
    for i, f in enumerate(files):
        o = str(Path(outdir) / f"still_{i}.png")
        Image.open(f).convert("RGB").save(o)
        outs.append(o)
    return outs


def lemo_home():
    return Path(os.environ.get("LEMO_HOME", TOOL / "work" / "_ext" / "lemo-opuscar"))


def _lemo_env():
    env = dict(os.environ)
    if _chrome():
        env.setdefault("PLAYWRIGHT_CHROME", _chrome())
    return env


def _lemo_video(tok, scr, out, conc):
    L = lemo_home()
    work = Path(tempfile.mkdtemp(prefix="lemo_", dir=Path(out).parent))
    info = _page(tok, scr, str(work / "demo"))
    silent = str(work / "silent.mp4")
    cmd = ["node", str(L / "core" / "render" / "video.mjs"), info["dir"], "--fps", str(info["fps"]), "--workers", str(max(1, min(conc, 6))),
           "--size", f"{info['width']}x{info['height']}", "--out", silent]
    print("[render:lemo] $", " ".join(cmd), flush=True)
    rc = subprocess.run(_node(cmd), env=_lemo_env()).returncode
    if rc == 0:
        rc = _finish_mp4(silent, info["audio"], out)
    shutil.rmtree(work, ignore_errors=True)
    return rc


def _lemo_stills(tok, scr, times, outdir):
    L = lemo_home()
    work = Path(tempfile.mkdtemp(prefix="lemo_st_", dir=outdir))
    info = _page(tok, scr, str(work / "demo"))
    ts = [f"{t:.3f}" for t in times]
    cmd = ["node", str(L / "core" / "render" / "still.mjs"), info["dir"], *ts, "--out", str(work / "jpg"), "--size", f"{info['width']}x{info['height']}"]
    print("[stills:lemo] $", " ".join(cmd), flush=True)
    rc = subprocess.run(_node(cmd), env=_lemo_env()).returncode
    if rc == 0:
        _jpgs_to_pngs([str(work / "jpg" / f"t_{t}.jpg") for t in ts], outdir)
    shutil.rmtree(work, ignore_errors=True)
    return rc


def hf_home():
    return Path(os.environ.get("HYPERFRAMES_HOME", TOOL / "work" / "_ext" / "hyperframes"))


def _hf_bin():
    b = hf_home() / "node_modules" / ".bin" / ("hyperframes.cmd" if os.name == "nt" else "hyperframes")
    return str(b)


def _hf_env():
    env = dict(os.environ, HYPERFRAMES_NO_TELEMETRY="1", DO_NOT_TRACK="1", HYPERFRAMES_NO_UPDATE_CHECK="1", NO_UPDATE_NOTICE="1")
    if _chrome():
        env.setdefault("PUPPETEER_EXECUTABLE_PATH", _chrome())
    return env


def _hf_video(tok, scr, out, conc):
    work = Path(tempfile.mkdtemp(prefix="hf_", dir=Path(out).parent))
    info = _page_hf(tok, scr, str(work / "demo"))
    silent = str(work / "silent.mp4")
    cmd = [_hf_bin(), "render", "-o", silent, "--fps", str(info["fps"]), "--workers", str(max(1, min(conc, 6))), "--quiet"]
    print("[render:hyperframes] $", " ".join(cmd), flush=True)
    rc = subprocess.run(cmd, cwd=info["dir"], env=_hf_env()).returncode
    if rc == 0:
        rc = _finish_mp4(silent, info["audio"], out)
    shutil.rmtree(work, ignore_errors=True)
    return rc


def _hf_stills(tok, scr, times, outdir):
    work = Path(tempfile.mkdtemp(prefix="hf_st_", dir=outdir))
    info = _page_hf(tok, scr, str(work / "demo"))
    cmd = [_hf_bin(), "snapshot", info["dir"], "--at", ",".join(f"{t:.3f}" for t in times), "--no-end", "--keep", "-o", str(work / "snap")]
    print("[stills:hyperframes] $", " ".join(cmd), flush=True)
    rc = subprocess.run(cmd, env=_hf_env()).returncode
    if rc == 0:
        def nm(t):
            x = f"{t:.3f}".rstrip("0").rstrip(".")
            return work / "snap" / f"at-{x}s.png"
        _jpgs_to_pngs([str(nm(t)) for t in times], outdir)
    shutil.rmtree(work, ignore_errors=True)
    return rc


def _page_hf(tok, scr, outdir):
    sys.path.insert(0, str(HTML))
    import build_page
    return build_page.build(tok, scr, outdir, hyperframes=True)


def _mc_video(tok, scr, out, conc):
    cmd = ["node", "capture.mjs", "video", "--tokens", tok, "--script", scr, "--out", out + ".silent.mp4", "--workers", str(max(1, min(conc, 4)))]
    rc = subprocess.run(_node(cmd), cwd=TOOL / "renderers" / "motion-canvas").returncode
    if rc == 0:
        S = json.load(open(scr, encoding="utf-8"))
        a = (S.get("audio") or {}).get("src")
        audio = str(Path(scr).resolve().parent / a) if a and (Path(scr).resolve().parent / a).exists() else None
        rc = _finish_mp4(out + ".silent.mp4", audio, out)
        os.remove(out + ".silent.mp4")
    return rc


def _mc_stills(tok, scr, times, outdir):
    cmd = ["node", "capture.mjs", "stills", "--tokens", tok, "--script", scr, "--times", ",".join(f"{t:.3f}" for t in times), "--outdir", outdir]
    return subprocess.run(_node(cmd), cwd=TOOL / "renderers" / "motion-canvas").returncode

BACKENDS = {
    "remotion": {
        "cwd": TOOL / "template",
        "install": ["npm", "install", "--no-audit", "--no-fund"],
        "installed": lambda: (TOOL / "template" / "node_modules").is_dir(),
        "video": lambda tok, scr, out, conc: ["node", "render.mjs", "--tokens", tok, "--script", scr, "--out", out, "--concurrency", str(conc)],
        "stills": lambda tok, scr, times, outdir: ["node", "still.mjs", "--tokens", tok, "--script", scr, "--times",
                                                   ",".join(f"{t:.3f}" for t in times), "--outdir", outdir],
    },
    "lemo": {
        "cwd": lemo_home(),
        "install": ["npm", "install", "--no-audit", "--no-fund"],
        "installed": lambda: (lemo_home() / "node_modules" / "playwright-core").is_dir(),
        "missing_help": "Lemo-Opuscar checkout not found. git clone https://github.com/lemomo-ai/lemo-opuscar <dir> and set LEMO_HOME=<dir> "
                        "(only core/render + package.json are used; code is MIT).",
        "video_fn": _lemo_video,
        "stills_fn": _lemo_stills,
    },
    "hyperframes": {
        "cwd": hf_home(),
        "install": ["npm", "install", "--no-audit", "--no-fund", "hyperframes@0.9.72"],
        "installed": lambda: Path(_hf_bin()).exists(),
        "missing_help": "HyperFrames not installed. mkdir <dir> && cd <dir> && npm init -y && npm install hyperframes@0.9.72, then set "
                        "HYPERFRAMES_HOME=<dir> (Apache-2.0; needs Node >= 22 and ffmpeg).",
        "video_fn": _hf_video,
        "stills_fn": _hf_stills,
    },
    "motion-canvas": {
        "cwd": TOOL / "renderers" / "motion-canvas",
        "install": ["npm", "install", "--no-audit", "--no-fund"],
        "installed": lambda: (TOOL / "renderers" / "motion-canvas" / "node_modules" / "@motion-canvas" / "core").is_dir(),
        "video_fn": _mc_video,
        "stills_fn": _mc_stills,
    },
}


def backend(name=None):
    name = name or os.environ.get("CVSD_RENDERER", "remotion")
    if name not in BACKENDS:
        raise SystemExit(f"[render] unknown renderer '{name}'. Available: {sorted(BACKENDS)}")
    b = BACKENDS[name]
    if not Path(b["cwd"]).is_dir():
        raise SystemExit(f"[render] {name}: {b.get('missing_help', 'backend folder missing: ' + str(b['cwd']))}")
    if not b["installed"]():
        npm = shutil.which("npm") or shutil.which("npm.cmd")
        subprocess.run([npm] + b["install"][1:], cwd=b["cwd"], check=True)
    return b


def _node(cmd):
    exe = shutil.which(cmd[0]) or shutil.which(cmd[0] + ".exe") or cmd[0]
    return [exe] + cmd[1:]


def render_video(tokens, script, out, renderer=None, concurrency=None):
    b = backend(renderer)
    conc = concurrency or int(os.environ.get("CONCURRENCY", "6"))
    if "video_fn" in b:
        return b["video_fn"](str(Path(tokens).resolve()), str(Path(script).resolve()), str(Path(out).resolve()), conc)
    cmd = _node(b["video"](str(Path(tokens).resolve()), str(Path(script).resolve()), str(Path(out).resolve()), conc))
    return subprocess.run(cmd, cwd=b["cwd"]).returncode


def render_stills(tokens, script, times, outdir, renderer=None):
    b = backend(renderer)
    Path(outdir).mkdir(parents=True, exist_ok=True)
    if "stills_fn" in b:
        rc = b["stills_fn"](str(Path(tokens).resolve()), str(Path(script).resolve()), times, str(Path(outdir).resolve()))
        return rc, [str(Path(outdir) / f"still_{i}.png") for i in range(len(times))]
    cmd = _node(b["stills"](str(Path(tokens).resolve()), str(Path(script).resolve()), times, str(Path(outdir).resolve())))
    rc = subprocess.run(cmd, cwd=b["cwd"]).returncode
    return rc, [str(Path(outdir) / f"still_{i}.png") for i in range(len(times))]


def segment_windows(script, tokens):
    """[(start_s, end_s, settled_s)] per segment, mirroring template/src/Main.tsx timeline()."""
    fps = round(tokens["canvas"].get("fps", 30))
    tr = round((tokens.get("motion", {}).get("transition", {}).get("duration_s", 0.5)) * fps)
    segs = script.get("segments", [])
    cur, out = 0, []
    for i, s in enumerate(segs):
        d = max(1, round((s.get("duration_s") or 4) * fps))
        nxt = segs[i + 1] if i + 1 < len(segs) else None
        ntype = (nxt or {}).get("transition") or script.get("transition") or tokens["motion"].get("transition", {}).get("type", "fade")
        next_overlap = 0 if nxt is None or ntype == "cut" else tr
        settled = cur + d - next_overlap - round(0.3 * fps)
        out.append((cur / fps, (cur + d) / fps, max(cur, settled) / fps))
        cur += d
    return out
