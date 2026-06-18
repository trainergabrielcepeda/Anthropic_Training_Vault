# Run all Python exercises for Module 05 — Agentic Workflows
Set-Location $PSScriptRoot

Write-Host "=== Module 05: Agentic Workflows — Python Exercises ===" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "requirements.txt") {
    Write-Host "[setup] Installing dependencies..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
}

Write-Host ""
Write-Host "--- Exercise 1: Simple Agent Loop ---" -ForegroundColor Green
python 01_simple_agent.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
