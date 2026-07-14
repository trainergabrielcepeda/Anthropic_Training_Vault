#!/usr/bin/env bash
# Run all Python exercises for Module 04 — Responsible AI
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 04: Responsible AI — Python Exercises ==="
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
echo "--- Exercise 1: Operator System Prompts ---"
python 01_operator_system_prompts.py

echo ""
echo "--- Exercise 2: Harm Testing ---"
python 02_harm_testing.py

echo ""
echo "=== All exercises complete ==="
