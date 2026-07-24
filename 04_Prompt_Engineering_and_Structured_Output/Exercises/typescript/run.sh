#!/usr/bin/env bash
# Run all TypeScript exercises for Domain 04 — Prompt Engineering & Structured Output
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Domain 04: Prompt Engineering & Structured Output — TypeScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
echo "--- Exercise 1: Structured Extraction (tool_choice: any) ---"
npx ts-node --esm 01_structured_extraction.ts

echo ""
echo "--- Exercise 2: Forced Tool Ordering + Validation/Retry ---"
npx ts-node --esm 02_validation_retry_loop.ts

echo ""
echo "=== All exercises complete ==="
