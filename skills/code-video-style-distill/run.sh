#!/usr/bin/env bash
# code-video-style-distill — bash wrapper. All logic lives in cvsd.py (cross-platform; on Windows run
# `.venv\Scripts\python.exe cvsd.py ...` in PowerShell). Every argument is passed through unchanged ("$@").
#
#   ./run.sh precheck   <ref.mp4> <work> [flags]
#   ./run.sh analyze    <ref.mp4> <work> [--no-ocr] [--no-videomd] [--scene-threshold 0.4] ...
#   ./run.sh distill    <work> <style-name> [overrides.json | --overrides f]
#   ./run.sh checklist  <work> <script.json> [--same-content]
#   ./run.sh stillcheck <work> <script.json>
#   ./run.sh render     <work> <script.json> <out.mp4>
#   ./run.sh compare    <ref.mp4> <work> <replica.mp4> [note]
#   ./run.sh beat       <out.wav> [--bpm 100] [--seconds 60]
#   ./run.sh all        <ref.mp4> <work> <style-name> <script.json> [--skip-review] [--rounds N] [--force]
#   ./run.sh resume     <ref.mp4> <work> <style-name> <script.json> [--rounds N] [--no-wait]
#
# Scope gate: only use reference videos you have the right to study. Set RIGHTS_OK=1 to confirm.
set -euo pipefail
TOOL="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PY="${PY:-$TOOL/.venv/bin/python}"
[ -x "$PY" ] || PY=python3
exec "$PY" "$TOOL/cvsd.py" "$@"
