# Run all TypeScript exercises for Module 05 — Agentic Workflows
Set-Location $PSScriptRoot

Write-Host "=== Domain 1: Agentic Architecture & Orchestration — TypeScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
$tsFiles = Get-ChildItem -Filter "*.ts" -File
if ($tsFiles.Count -eq 0) {
    Write-Host "[info] No exercise files found yet. Check back after exercises are added." -ForegroundColor Yellow
} else {
    foreach ($f in $tsFiles) {
        Write-Host "--- Running: $($f.Name) ---" -ForegroundColor Green
        npx ts-node --esm $f.Name
        Write-Host ""
    }
}

Write-Host "=== Done ===" -ForegroundColor Cyan
