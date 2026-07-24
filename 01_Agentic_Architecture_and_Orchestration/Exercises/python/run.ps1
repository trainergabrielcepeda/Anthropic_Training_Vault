# Run all Python exercises for Domain 1 — Agentic Architecture & Orchestration
Set-Location $PSScriptRoot

Write-Host "=== Domain 1: Agentic Architecture & Orchestration — Python Exercises ===" -ForegroundColor Cyan
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
Write-Host "--- Exercise 1: Agentic Loop (stop_reason control flow) ---" -ForegroundColor Green
python 01_agentic_loop.py

Write-Host ""
Write-Host "--- Exercise 2: Coordinator Dispatching to Parallel Subagents ---" -ForegroundColor Green
python 02_coordinator_subagents.py

Write-Host ""
Write-Host "--- Exercise 3: Hook-Style Interception & Normalization ---" -ForegroundColor Green
python 03_hook_interception.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
