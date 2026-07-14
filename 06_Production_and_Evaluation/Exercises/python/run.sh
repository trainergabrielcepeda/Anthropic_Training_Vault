#!/usr/bin/env bash
# Run all Python exercises for Module 06 — Production & Evaluation
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 06: Production & Evaluation — Python Exercises ==="
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
echo "--- Exercise 1: Prompt Caching ---"
python 01_prompt_caching.py

echo ""
echo "--- Exercise 3: LLM-as-Judge Evaluation ---"
python 03_llm_judge.py

echo ""
echo "=== All exercises complete ==="
