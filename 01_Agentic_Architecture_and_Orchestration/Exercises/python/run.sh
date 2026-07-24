#!/usr/bin/env bash
# Run all Python exercises for Domain 1 — Agentic Architecture & Orchestration
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Domain 1: Agentic Architecture & Orchestration — Python Exercises ==="
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
echo "--- Exercise 1: Agentic Loop (stop_reason control flow) ---"
python 01_agentic_loop.py

echo ""
echo "--- Exercise 2: Coordinator Dispatching to Parallel Subagents ---"
python 02_coordinator_subagents.py

echo ""
echo "--- Exercise 3: Hook-Style Interception & Normalization ---"
python 03_hook_interception.py

echo ""
echo "=== All exercises complete ==="
