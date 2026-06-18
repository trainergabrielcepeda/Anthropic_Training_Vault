# Run all JavaScript exercises for Module 01 — Claude Models & API
Set-Location $PSScriptRoot

Write-Host "=== Module 01: Claude Models & API — JavaScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
Write-Host "--- Exercise 1: Basic Messages API ---" -ForegroundColor Green
node 01_basic_messages.js

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
