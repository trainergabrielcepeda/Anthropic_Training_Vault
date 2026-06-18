# Run all TypeScript exercises for Module 01 — Claude Models & API
Set-Location $PSScriptRoot

Write-Host "=== Module 01: Claude Models & API — TypeScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
Write-Host "--- Exercise 1: Typed Basic Messages API ---" -ForegroundColor Green
npx ts-node --esm 01_basic_messages.ts

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
