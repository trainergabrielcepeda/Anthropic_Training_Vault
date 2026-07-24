#!/usr/bin/env bash
# Run all JavaScript exercises for Domain 05 — Context Management & Reliability
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Domain 05: Context Management & Reliability — JavaScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
echo "--- Exercise 1: Case-Facts Extraction ---"
node 01_case_facts.js

echo ""
echo "--- Exercise 2: Escalation Decisions + Structured Error Propagation ---"
node 02_escalation_and_errors.js

echo ""
echo "=== All exercises complete ==="
