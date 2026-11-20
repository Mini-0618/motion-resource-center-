#!/usr/bin/env python3
"""export_index.py — export styles/*/ into ONE asset-index manifest (JSON) for the motion resource library.

Usage: export_index.py [--styles-dir styles] [-o styles/asset-index.json] [--taxonomy references/motion-taxonomy.md] [--strict]

Each asset = one style folder (style-tokens.json + refs/ + README.md [+ attribution.json]):
  name/path/version/created_at, tokens_summary (canvas/palette/typography/motion/rhythm), components
  (template segment + taxonomy ids, verified against the taxonomy table), taxonomy_ids, provenance counts,
  refs paths, license/attribution, and a `motion_center` block whose keys match
  Mini-0618/motion-resource-center- `motion_center.core.add_resource()` (title/url/source_pool/category/styles/
  description/prompt/license/source_url) so a library can import it as-is.

Licensing: attribution.json (per style) declares the reference's rights/source label. Missing → "UNSPECIFIED"
and a warning (--strict turns that into exit 1). refs/ are internal comparison frames: `distributable: false`.
Validated against schema/asset-index.schema.json.
"""
import argparse
import datetime as dt
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from distill import load_taxonomy, DEFAULT_TAXONOMY  # noqa: E402

SCHEMA = os.path.join(TOOL, "schema", "asset-index.schema.json")
SEG_OF = {"title_card": "title", "bullet_list": "bullets", "bar_chart": "bars", "number_counter": "stat", "code_block": "code",
          "evidence_frame": "evidence", "timeline": "timeline", "compare_columns": "compare", "flow_chart": "flow"}


def rel(p, base):
    return os.path.relpath(p, base).replace(os.sep, "/")


def summarize(T):
    P, ty, m, r = T.get("palette", {}), T.get("typography", {}), T.get("motion", {}), T.get("rhythm", {})
    return {
        "canvas": {k: T.get("canvas", {}).get(k) for k in ("width", "height", "fps")},
        "palette": {k: P.get(k) for k in ("bg", "surface", "primary", "accent", "text", "text_muted") if P.get(k)},
        "typography": {"families": {k: v.get("css") for k, v in (ty.get("families") or {}).items()},
                       "scale_px": ty.get("scale_px"), "font_policy": "free/open substitutes only; no reference font files"},
        "motion": {"enter_style": m.get("enter_style"), "durations_s": m.get("durations_s"), "stagger_s": m.get("stagger_s"),
                   "easing_enter": (m.get("easing") or {}).get("enter", {}).get("cubic_bezier"),
                   "transition": (m.get("transition") or {}).get("type") if isinstance(m.get("transition"), dict) else m.get("transition")},
        "rhythm": {"shot_mean_s": r.get("shot_mean_s"), "entrance_events_per_min": r.get("entrance_events_per_min")},
    }


def asset(sd, styles_dir, taxo):
    T = json.load(open(os.path.join(sd, "style-tokens.json"), encoding="utf-8"))
    name = T.get("name") or os.path.basename(sd)
    comps, ids = [], set()
    for c in T.get("components", []):
        tx = c.get("taxonomy") or {}
        cid = list(tx.get("ui", [])) + list(tx.get("video", []))
        ids.update(cid)
        comps.append({"type": c["type"], "template_segment": c.get("template_segment") or SEG_OF.get(c["type"]),
                      "confidence": c.get("confidence"), "taxonomy_ids": cid,
                      "taxonomy_verified": bool(taxo) and all(i in taxo for i in cid)})
    counts = {"seen": 0, "inferred": 0, "unknown": 0}
    for k, v in (T.get("provenance") or {}).items():
        if k.startswith("_"):
            continue
        counts[v.get("status", "unknown")] = counts.get(v.get("status", "unknown"), 0) + 1
    refs = sorted(rel(p, styles_dir) for p in glob.glob(os.path.join(sd, "refs", "*")))
    att_p = os.path.join(sd, "attribution.json")
    att = json.load(open(att_p, encoding="utf-8")) if os.path.exists(att_p) else {}
    lic = {"style_tokens_license": att.get("style_tokens_license", "UNSPECIFIED"),
           "reference_rights": att.get("reference_rights", "UNSPECIFIED"),
           "source_label": att.get("source_label", "UNSPECIFIED"),
           "attribution": att.get("attribution", ""),
           "refs_distributable": False,
           "notes": "style = measured parameters only; no reference footage, logos, characters or font files are included"}
    taxo_ids = sorted(ids)
    src = T.get("source") or {}
    prompt = (f"用风格底座 {name} 渲染新选题：背景 {summarize(T)['palette'].get('bg')}，主色 {summarize(T)['palette'].get('primary')}，"
              f"入场 {T.get('motion', {}).get('enter_style')}；元件 {', '.join(c['type'] for c in comps)}")
    return {
        "id": f"cvsd-style:{name}", "name": name, "path": rel(sd, styles_dir), "version": T.get("version"),
        "created_at": src.get("distilled_at"), "description": T.get("description", ""),
        "source": {"video_file": os.path.basename(src.get("video", "")) or None, "duration_s": src.get("duration_s")},
        "tokens_file": rel(os.path.join(sd, "style-tokens.json"), styles_dir),
        "tokens_summary": summarize(T),
        "components": comps, "taxonomy_ids": taxo_ids,
        "provenance": {"counts": counts, "unknowns": [u.get("path") for u in (T.get("unknowns") or []) if isinstance(u, dict)][:20]},
        "refs": refs, "license": lic,
        "motion_center": {"title": f"风格底座 {name}", "url": f"cvsd-style://{name}", "source_pool": "evergreen",
                          "category": taxo_ids[0] if taxo_ids else "V-14",
                          "styles": [name] + sorted({c["type"] for c in comps}),
                          "description": (T.get("description") or "")[:500], "prompt": prompt,
                          "license": lic["style_tokens_license"], "source_url": lic["source_label"] if lic["source_label"] != "UNSPECIFIED" else None},
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--styles-dir", default=os.path.join(TOOL, "styles"))
    ap.add_argument("-o", "--out")
    ap.add_argument("--taxonomy", default=os.environ.get("CVSD_TAXONOMY") or DEFAULT_TAXONOMY)
    ap.add_argument("--strict", action="store_true", help="exit 1 if any style lacks attribution.json / has unverified taxonomy ids")
    a = ap.parse_args()
    sdir = os.path.abspath(a.styles_dir)
    out = a.out or os.path.join(sdir, "asset-index.json")
    taxo, terr = load_taxonomy(a.taxonomy)
    if terr:
        print(f"[export-index] ERROR {terr} — taxonomy ids will be reported unverified", file=sys.stderr)
    folders = sorted(d for d in glob.glob(os.path.join(sdir, "*")) if os.path.isfile(os.path.join(d, "style-tokens.json")))
    if not folders:
        print(f"[export-index] no style folders (with style-tokens.json) under {sdir}", file=sys.stderr)
        return 2
    assets = [asset(d, sdir, taxo) for d in folders]
    warn = []
    for x in assets:
        if x["license"]["reference_rights"] == "UNSPECIFIED":
            warn.append(f"{x['name']}: no attribution.json (rights/source label UNSPECIFIED)")
        bad = [c["type"] for c in x["components"] if not c["taxonomy_verified"]]
        if bad:
            warn.append(f"{x['name']}: unverified taxonomy ids on {bad}")
    idx = {"schema": "cvsd-asset-index/1", "generated_at": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
           "tool": "code-video-style-distill", "styles_dir": sdir,
           "taxonomy_source": os.path.abspath(a.taxonomy) if not terr else None,
           "alignment": "motion_center block = fields of Mini-0618/motion-resource-center- add_resource(); no separate asset-index format exists there (checked 2026-11-19)",
           "count": len(assets), "warnings": warn, "assets": assets}
    try:
        import jsonschema
        jsonschema.validate(idx, json.load(open(SCHEMA, encoding="utf-8")))
    except ImportError:
        print("[export-index] jsonschema not installed; skipped validation")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        json.dump(idx, f, ensure_ascii=False, indent=2)
    for w in warn:
        print("[export-index] WARNING", w)
    print(f"[export-index] wrote {out}: {len(assets)} style(s): {[x['name'] for x in assets]}")
    return 1 if (a.strict and warn) else 0


if __name__ == "__main__":
    sys.exit(main())
