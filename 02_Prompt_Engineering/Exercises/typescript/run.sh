#!/usr/bin/env bash
# Run all TypeScript exercises for Module 02 — Prompt Engineering
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 02: Prompt Engineering — TypeScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
echo "--- Exercise 1: Structured Output ---"
npx ts-node --esm 01_structured_output.ts

echo ""
echo "=== All exercises complete ==="
