#!/usr/bin/env bash
# Run all JavaScript exercises for Module 02 — Prompt Engineering
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 02: Prompt Engineering — JavaScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
echo "--- Exercise 1: System Prompts ---"
node 01_system_prompts.js

echo ""
echo "=== All exercises complete ==="
