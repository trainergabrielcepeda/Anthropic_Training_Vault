# Run all Python exercises for Module 01 — Claude Models & API
Set-Location $PSScriptRoot

Write-Host "=== Module 01: Claude Models & API — Python Exercises ===" -ForegroundColor Cyan
Write-Host ""

# Create and activate a virtual environment
if (-not (Test-Path ".venv")) {
    Write-Host "[setup] Creating virtual environment..." -ForegroundColor Yellow
    python -m venv .venv
}
. .venv\Scripts\Activate.ps1

# Install dependencies
if (Test-Path "requirements.txt") {
    Write-Host "[setup] Installing dependencies..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
}

Write-Host ""
Write-Host "--- Exercise 1: Basic Messages API ---" -ForegroundColor Green
python 01_basic_messages.py

Write-Host ""
Write-Host "--- Exercise 2: Streaming Responses ---" -ForegroundColor Green
python 02_streaming.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
