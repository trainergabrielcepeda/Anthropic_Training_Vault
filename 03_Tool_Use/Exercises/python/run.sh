#!/usr/bin/env bash
# Run all Python exercises for Module 03 — Tool Use
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 03: Tool Use — Python Exercises ==="
echo ""

if [ ! -d .venv ]; then
  echo "[setup] Creating virtual environment..."
  python -m venv .venv
fi
source .venv/bin/activate

if [ -f requirements.txt ]; then
  echo "[setup] Installing dependencies..."
  pip install -q -r requirements.txt
fi

echo ""
echo "--- Exercise 1: Single Tool ---"
python 01_single_tool.py

echo ""
echo "--- Exercise 2: Multiple Tools ---"
python 02_multi_tool.py

echo ""
echo "=== All exercises complete ==="
