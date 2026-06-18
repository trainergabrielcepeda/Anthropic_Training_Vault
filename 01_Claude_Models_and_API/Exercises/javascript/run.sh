#!/usr/bin/env bash
# Run all JavaScript exercises for Module 01 — Claude Models & API
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 01: Claude Models & API — JavaScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
echo "--- Exercise 1: Basic Messages API ---"
node 01_basic_messages.js

echo ""
echo "=== All exercises complete ==="
