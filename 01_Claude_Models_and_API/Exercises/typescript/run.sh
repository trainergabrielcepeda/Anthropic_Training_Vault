#!/usr/bin/env bash
# Run all TypeScript exercises for Module 01 — Claude Models & API
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Module 01: Claude Models & API — TypeScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
echo "--- Exercise 1: Typed Basic Messages API ---"
npx ts-node --esm 01_basic_messages.ts

echo ""
echo "=== All exercises complete ==="
