#!/usr/bin/env bash
# Run all JavaScript exercises for Domain 04 — Prompt Engineering & Structured Output
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Domain 04: Prompt Engineering & Structured Output — JavaScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
echo "--- Exercise 1: Structured Extraction + Validation Retry ---"
node 01_structured_extraction.js

echo ""
echo "--- Exercise 2: Few-Shot Consistency ---"
node 02_few_shot_consistency.js

echo ""
echo "=== All exercises complete ==="
