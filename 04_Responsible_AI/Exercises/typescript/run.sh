#!/usr/bin/env bash
# Run all TypeScript exercises for Module 04 — Responsible AI
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 04: Responsible AI — TypeScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
shopt -s nullglob
ts_files=(*.ts)
if [ ${#ts_files[@]} -eq 0 ]; then
  echo "[info] No exercise files found yet. Check back after exercises are added."
else
  for f in "${ts_files[@]}"; do
    echo "--- Running: $f ---"
    npx ts-node --esm "$f"
    echo ""
  done
fi

echo "=== Done ==="
