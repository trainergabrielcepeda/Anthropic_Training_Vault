# Run all TypeScript exercises for Domain 05 — Context Management & Reliability
Set-Location $PSScriptRoot

Write-Host "=== Domain 05: Context Management & Reliability — TypeScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
Write-Host "--- Exercise 1: Case Facts, Escalation Criteria & Structured Error Propagation ---" -ForegroundColor Green
npx ts-node --esm 01_context_reliability.ts

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
