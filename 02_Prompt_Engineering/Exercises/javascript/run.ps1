# Run all JavaScript exercises for Module 02 — Prompt Engineering
Set-Location $PSScriptRoot

Write-Host "=== Module 02: Prompt Engineering — JavaScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
Write-Host "--- Exercise 1: System Prompts ---" -ForegroundColor Green
node 01_system_prompts.js

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
