# Run all Python exercises for Domain 04 — Prompt Engineering & Structured Output
Set-Location $PSScriptRoot

Write-Host "=== Domain 04: Prompt Engineering & Structured Output — Python Exercises ===" -ForegroundColor Cyan
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
Write-Host "--- Exercise 1: Structured Extraction via tool_use ---" -ForegroundColor Green
python 01_structured_extraction.py

Write-Host ""
Write-Host "--- Exercise 2: Validation & Retry Loop ---" -ForegroundColor Green
python 02_validation_retry_loop.py

Write-Host ""
Write-Host "--- Exercise 3: Few-Shot Consistency ---" -ForegroundColor Green
python 03_few_shot_consistency.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
