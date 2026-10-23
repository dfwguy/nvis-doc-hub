#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
shopt -s nullglob
configs=(sources/*.json)
if [[ ${#configs[@]} -eq 0 ]]; then
  printf '%s\n' 'No source registrations found in sources/*.json.' >&2
  exit 1
fi
for config in "${configs[@]}"; do
  .venv/bin/nvis-hub register "$config"
done
exec .venv/bin/nvis-hub refresh --all
