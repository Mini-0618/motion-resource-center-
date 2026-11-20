"""renderers.py — the replaceable render layer.

Contract (any backend):  style-tokens.json + script.json  ->  out.mp4   (render_video)
                         style-tokens.json + script.json + [t_s...] -> PNGs (render_stills, for stillcheck)
Both files are validated for content/style decoupling by the backend. Timeline semantics every
backend must keep (stillcheck relies on it): segments play in order, each lasts duration_s; segment i>0
starts motion.transition.duration_s earlier (overlap) unless its transition is "cut".

Backends: "remotion" (default, template/; Remotion has its own company licence — check
https://www.remotion.dev/license before commercial team use). Planned slots: "motion-canvas" (MIT),
"hyperframes" (Apache-2.0) — add an entry to BACKENDS with the same two commands.
Select with env CVSD_RENDERER or --renderer.
"""
import os
import shutil
import subprocess
from pathlib import Path

TOOL = Path(__file__).resolve().parent.parent

BACKENDS = {
    "remotion": {
        "cwd": TOOL / "template",
        "install": ["npm", "install", "--no-audit", "--no-fund"],
        "installed": lambda: (TOOL / "template" / "node_modules").is_dir(),
        "video": lambda tok, scr, out, conc: ["node", "render.mjs", "--tokens", tok, "--script", scr, "--out", out, "--concurrency", str(conc)],
        "stills": lambda tok, scr, times, outdir: ["node", "still.mjs", "--tokens", tok, "--script", scr, "--times",
                                                   ",".join(f"{t:.3f}" for t in times), "--outdir", outdir],
    },
    # "motion-canvas": {...}, "hyperframes": {...}   <- future backends, same contract
}


def backend(name=None):
    name = name or os.environ.get("CVSD_RENDERER", "remotion")
    if name not in BACKENDS:
        raise SystemExit(f"[render] unknown renderer '{name}'. Available: {sorted(BACKENDS)}")
    b = BACKENDS[name]
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
    cmd = _node(b["video"](str(Path(tokens).resolve()), str(Path(script).resolve()), str(Path(out).resolve()), conc))
    return subprocess.run(cmd, cwd=b["cwd"]).returncode


def render_stills(tokens, script, times, outdir, renderer=None):
    b = backend(renderer)
    Path(outdir).mkdir(parents=True, exist_ok=True)
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
