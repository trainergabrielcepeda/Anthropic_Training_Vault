# Run all Python exercises for Domain 2 — Tool Design & MCP Integration
Set-Location $PSScriptRoot

Write-Host "=== Domain 2: Tool Design & MCP Integration — Python Exercises ===" -ForegroundColor Cyan
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
Write-Host "--- Exercise 1: Tool Description Design ---" -ForegroundColor Green
python 01_tool_description_design.py

Write-Host ""
Write-Host "--- Exercise 2: Structured MCP Errors ---" -ForegroundColor Green
python 02_structured_errors.py

Write-Host ""
Write-Host "--- Exercise 3: tool_choice Modes ---" -ForegroundColor Green
python 03_tool_choice_modes.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
