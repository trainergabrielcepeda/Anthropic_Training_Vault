#!/usr/bin/env bash
# Run all Python exercises for Domain 2 — Tool Design & MCP Integration
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Domain 2: Tool Design & MCP Integration — Python Exercises ==="
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
echo "--- Exercise 1: Tool Description Design ---"
python 01_tool_description_design.py

echo ""
echo "--- Exercise 2: Structured MCP Errors ---"
python 02_structured_errors.py

echo ""
echo "--- Exercise 3: tool_choice Modes ---"
python 03_tool_choice_modes.py

echo ""
echo "=== All exercises complete ==="
