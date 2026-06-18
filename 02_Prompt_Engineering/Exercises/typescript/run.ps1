# Run all TypeScript exercises for Module 02 — Prompt Engineering
Set-Location $PSScriptRoot

Write-Host "=== Module 02: Prompt Engineering — TypeScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
Write-Host "--- Exercise 1: Structured Output ---" -ForegroundColor Green
npx ts-node --esm 01_structured_output.ts

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
