#!/usr/bin/env bash
# Run all Python exercises for Module 05 — Agentic Workflows
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 05: Agentic Workflows — Python Exercises ==="
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
echo "--- Exercise 1: Simple Agent Loop ---"
python 01_simple_agent.py

echo ""
echo "=== All exercises complete ==="
