# Run all Python exercises for Domain 05 — Context Management & Reliability
Set-Location $PSScriptRoot

Write-Host "=== Domain 05: Context Management & Reliability — Python Exercises ===" -ForegroundColor Cyan
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
Write-Host "--- Exercise 1: Case-Facts Extraction ---" -ForegroundColor Green
python 01_case_facts.py

Write-Host ""
Write-Host "--- Exercise 2: Escalation Decisions via Explicit Criteria ---" -ForegroundColor Green
python 02_escalation_decision.py

Write-Host ""
Write-Host "--- Exercise 3: Structured Error Propagation ---" -ForegroundColor Green
python 03_error_propagation.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
