#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."
if [[ ! -x .venv/bin/nvis-hub ]]; then
  printf '%s\n' 'Create the Python 3.12+ .venv and run: .venv/bin/python -m pip install -e ".[dev]"' >&2
  exit 1
fi
exec .venv/bin/nvis-hub serve --host 127.0.0.1 --port "${NVIS_HUB_PORT:-8000}"
