#!/usr/bin/env bash
# Run all Python exercises for Module 02 — Prompt Engineering
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 02: Prompt Engineering — Python Exercises ==="
echo ""

if [ -f requirements.txt ]; then
  echo "[setup] Installing dependencies..."
  pip install -q -r requirements.txt
fi

echo ""
echo "--- Exercise 1: System Prompts ---"
python 01_system_prompts.py

echo ""
echo "--- Exercise 2: Few-Shot Prompting ---"
python 02_few_shot.py

echo ""
echo "--- Exercise 3: Chain-of-Thought Prompting ---"
python 03_chain_of_thought.py

echo ""
echo "=== All exercises complete ==="
