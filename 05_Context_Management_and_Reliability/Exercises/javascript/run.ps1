# Run all JavaScript exercises for Domain 05 — Context Management & Reliability
Set-Location $PSScriptRoot

Write-Host "=== Domain 05: Context Management & Reliability — JavaScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
Write-Host "--- Exercise 1: Case-Facts Extraction ---" -ForegroundColor Green
node 01_case_facts.js

Write-Host ""
Write-Host "--- Exercise 2: Escalation Decisions + Structured Error Propagation ---" -ForegroundColor Green
node 02_escalation_and_errors.js

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
