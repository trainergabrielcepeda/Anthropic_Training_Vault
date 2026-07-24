#!/usr/bin/env bash
# Run all Python exercises for Domain 04 — Prompt Engineering & Structured Output
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Domain 04: Prompt Engineering & Structured Output — Python Exercises ==="
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
echo "--- Exercise 1: Structured Extraction via tool_use ---"
python 01_structured_extraction.py

echo ""
echo "--- Exercise 2: Validation & Retry Loop ---"
python 02_validation_retry_loop.py

echo ""
echo "--- Exercise 3: Few-Shot Consistency ---"
python 03_few_shot_consistency.py

echo ""
echo "=== All exercises complete ==="
