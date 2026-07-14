# Run all Python exercises for Module 06 — Production & Evaluation
Set-Location $PSScriptRoot

Write-Host "=== Module 06: Production & Evaluation — Python Exercises ===" -ForegroundColor Cyan
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
Write-Host "--- Exercise 1: Prompt Caching ---" -ForegroundColor Green
python 01_prompt_caching.py

Write-Host ""
Write-Host "--- Exercise 3: LLM-as-Judge Evaluation ---" -ForegroundColor Green
python 03_llm_judge.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
