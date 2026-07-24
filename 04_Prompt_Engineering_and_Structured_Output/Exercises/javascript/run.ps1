# Run all JavaScript exercises for Domain 04 — Prompt Engineering & Structured Output
Set-Location $PSScriptRoot

Write-Host "=== Domain 04: Prompt Engineering & Structured Output — JavaScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
Write-Host "--- Exercise 1: Structured Extraction + Validation Retry ---" -ForegroundColor Green
node 01_structured_extraction.js

Write-Host ""
Write-Host "--- Exercise 2: Few-Shot Consistency ---" -ForegroundColor Green
node 02_few_shot_consistency.js

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
