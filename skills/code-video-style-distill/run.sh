#!/usr/bin/env bash
# code-video-style-distill pipeline. Every step can run on its own.
#
#   ./run.sh precheck <ref.mp4> <work>                         # optional step 0: code/template-generated?
#   ./run.sh analyze  <ref.mp4> <work>                         # -> <work>/ref_analysis
#   ./run.sh distill  <work> <style-name> [overrides.json]     # -> <work>/style + styles/<name>/
#   ./run.sh checklist <work> <script.json> [--same-content]   # -> <work>/acceptance.json (pre-declared, BEFORE render)
#   ./run.sh render   <work> <script.json> <out.mp4>           # tokens from <work>/style/style-tokens.json
#   ./run.sh compare  <ref.mp4> <work> <replica.mp4> [note]    # -> <work>/compare_rN, ledger
#   ./run.sh all      <ref.mp4> <work> <style-name> <script.json>
#
# Scope gate: only use reference videos you have the right to study. Set RIGHTS_OK=1 to confirm.
set -euo pipefail
TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PY:-$TOOL/.venv/bin/python}"
[ -x "$PY" ] || PY=python3
step="${1:-help}"; shift || true

gate() {
  if [ "${RIGHTS_OK:-0}" != "1" ]; then
    cat >&2 <<'MSG'
[scope gate] 只处理你有权参考的视频（自己的作品、已获授权、或仅用于内部风格学习的公开视频）。
             只学风格和结构；不搬运原片素材、字体文件、logo、商标、角色；不承诺像素级一致。
             确认后用 RIGHTS_OK=1 重新运行。
MSG
    exit 3
  fi
}

case "$step" in
  precheck)  "$PY" "$TOOL/scripts/precheck.py" "$1" -o "$2/precheck" ;;
  analyze)   gate; "$PY" "$TOOL/scripts/analyze.py" "$1" -o "$2/ref_analysis" ;;
  distill)   ov=(); [ -n "${3:-}" ] && ov=(--overrides "$3")
             "$PY" "$TOOL/scripts/distill.py" "$1/ref_analysis" -o "$1/style" --name "$2" --styles-dir "$TOOL/styles" "${ov[@]}" ;;
  checklist) "$PY" "$TOOL/scripts/checklist.py" --tokens "$1/style/style-tokens.json" --ref-analysis "$1/ref_analysis" --script "$2" ${3:-} -o "$1/acceptance.json" ;;
  render)    tok="$(realpath "$1/style/style-tokens.json")"; scr="$(realpath "$2")"; outp="$(realpath -m "$3")"
             [ -d "$TOOL/template/node_modules" ] || (cd "$TOOL/template" && npm install --no-audit --no-fund)
             (cd "$TOOL/template" && node render.mjs --tokens "$tok" --script "$scr" --out "$outp" --concurrency "${CONCURRENCY:-6}") ;;
  compare)   n=1; while [ -d "$2/compare_r$n" ]; do n=$((n+1)); done
             "$PY" "$TOOL/scripts/compare.py" --ref "$1" --rep "$3" --checklist "$2/acceptance.json" --ref-analysis "$2/ref_analysis" \
               --tokens "$2/style/style-tokens.json" -o "$2/compare_r$n" --note "${4:-}" ;;
  all)       ref="$1"; work="$2"; name="$3"; script="$4"; mkdir -p "$work"
             "$0" precheck "$ref" "$work"
             "$0" analyze "$ref" "$work"
             "$0" distill "$work" "$name"
             "$0" checklist "$work" "$script"
             "$0" render "$work" "$script" "$work/replica_r1.mp4"
             "$0" compare "$ref" "$work" "$work/replica_r1.mp4" "round 1: distilled tokens as-is" ;;
  *) sed -n '2,13p' "$0" ;;
esac
