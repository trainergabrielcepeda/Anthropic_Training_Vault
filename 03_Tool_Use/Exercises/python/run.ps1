# Run all Python exercises for Module 03 — Tool Use
Set-Location $PSScriptRoot

Write-Host "=== Module 03: Tool Use — Python Exercises ===" -ForegroundColor Cyan
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
Write-Host "--- Exercise 1: Single Tool ---" -ForegroundColor Green
python 01_single_tool.py

Write-Host ""
Write-Host "--- Exercise 2: Multiple Tools ---" -ForegroundColor Green
python 02_multi_tool.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
