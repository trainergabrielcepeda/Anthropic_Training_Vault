#!/usr/bin/env bash
# Run all JavaScript exercises for Domain 2 — Tool Design & MCP Integration
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Domain 2: Tool Design & MCP Integration — JavaScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
# Run any .js exercise files found in this directory
shopt -s nullglob
js_files=(*.js)
if [ ${#js_files[@]} -eq 0 ]; then
  echo "[info] No exercise files found yet. Check back after exercises are added."
else
  for f in "${js_files[@]}"; do
    echo "--- Running: $f ---"
    node "$f"
    echo ""
  done
fi

echo "=== Done ==="
