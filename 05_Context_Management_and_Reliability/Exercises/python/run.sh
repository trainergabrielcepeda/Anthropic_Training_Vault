#!/usr/bin/env bash
# Run all Python exercises for Domain 05 — Context Management & Reliability
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Domain 05: Context Management & Reliability — Python Exercises ==="
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
echo "--- Exercise 1: Case-Facts Extraction ---"
python 01_case_facts.py

echo ""
echo "--- Exercise 2: Escalation Decisions via Explicit Criteria ---"
python 02_escalation_decision.py

echo ""
echo "--- Exercise 3: Structured Error Propagation ---"
python 03_error_propagation.py

echo ""
echo "=== All exercises complete ==="
