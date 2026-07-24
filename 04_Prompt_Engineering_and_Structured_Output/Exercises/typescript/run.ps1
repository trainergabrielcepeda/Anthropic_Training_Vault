# Run all TypeScript exercises for Domain 04 — Prompt Engineering & Structured Output
Set-Location $PSScriptRoot

Write-Host "=== Domain 04: Prompt Engineering & Structured Output — TypeScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
Write-Host "--- Exercise 1: Structured Extraction (tool_choice: any) ---" -ForegroundColor Green
npx ts-node --esm 01_structured_extraction.ts

Write-Host ""
Write-Host "--- Exercise 2: Forced Tool Ordering + Validation/Retry ---" -ForegroundColor Green
npx ts-node --esm 02_validation_retry_loop.ts

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
