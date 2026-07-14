#!/usr/bin/env bash
# Run all Python exercises for Module 01 — Claude Models & API
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 01: Claude Models & API — Python Exercises ==="
echo ""

# Create and activate a virtual environment
if [ ! -d .venv ]; then
  echo "[setup] Creating virtual environment..."
  python -m venv .venv
fi
source .venv/bin/activate

# Install dependencies
if [ -f requirements.txt ]; then
  echo "[setup] Installing dependencies..."
  pip install -q -r requirements.txt
fi

echo ""
echo "--- Exercise 1: Basic Messages API ---"
python 01_basic_messages.py

echo ""
echo "--- Exercise 2: Streaming Responses ---"
python 02_streaming.py

echo ""
echo "=== All exercises complete ==="
