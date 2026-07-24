#!/usr/bin/env bash
# Run all TypeScript exercises for Domain 05 — Context Management & Reliability
set -euo pipefail
cd "$(dirname "$0")"

echo "=== Domain 05: Context Management & Reliability — TypeScript Exercises ==="
echo ""

echo "[setup] Installing npm dependencies..."
npm install --silent

echo ""
echo "--- Exercise 1: Case Facts, Escalation Criteria & Structured Error Propagation ---"
npx ts-node --esm 01_context_reliability.ts

echo ""
echo "=== All exercises complete ==="
