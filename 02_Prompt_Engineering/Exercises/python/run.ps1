# Run all Python exercises for Module 02 — Prompt Engineering
Set-Location $PSScriptRoot

Write-Host "=== Module 02: Prompt Engineering — Python Exercises ===" -ForegroundColor Cyan
Write-Host ""

if (Test-Path "requirements.txt") {
    Write-Host "[setup] Installing dependencies..." -ForegroundColor Yellow
    pip install -q -r requirements.txt
}

Write-Host ""
Write-Host "--- Exercise 1: System Prompts ---" -ForegroundColor Green
python 01_system_prompts.py

Write-Host ""
Write-Host "--- Exercise 2: Few-Shot Prompting ---" -ForegroundColor Green
python 02_few_shot.py

Write-Host ""
Write-Host "--- Exercise 3: Chain-of-Thought Prompting ---" -ForegroundColor Green
python 03_chain_of_thought.py

Write-Host ""
Write-Host "=== All exercises complete ===" -ForegroundColor Cyan
