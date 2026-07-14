# Run all Python exercises for Module 04 — Responsible AI
Set-Location $PSScriptRoot

Write-Host "=== Module 04: Responsible AI — Python Exercises ===" -ForegroundColor Cyan
Write-Host ""

if (-not (Test-Path ".venv")) {
    Write-Host "[setup] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}
. .venv\Scripts\Activate.ps1

if (Test-Path "requirements.txt") {
    Write-Host "[setup] Installing dependencies..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
}

Write-Host ""
Write-Host "--- Exercise 1: Operator System Prompts ---" -ForegroundColor Green
python 01_operator_system_prompts.py

Write-Host ""
Write-Host "--- Exercise 2: Harm Testing ---" -ForegroundColor Green
python 02_harm_testing.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
