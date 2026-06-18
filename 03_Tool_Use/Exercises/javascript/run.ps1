# Run all JavaScript exercises for Module 03 — Tool Use
Set-Location $PSScriptRoot

Write-Host "=== Module 03: Tool Use — JavaScript Exercises ===" -ForegroundColor Cyan
Write-Host ""

Write-Host "[setup] Installing npm dependencies..." -ForegroundColor Yellow
npm install --silent

Write-Host ""
$jsFiles = Get-ChildItem -Filter "*.js" -File
if ($jsFiles.Count -eq 0) {
    Write-Host "[info] No exercise files found yet. Check back after exercises are added." -ForegroundColor Yellow
} else {
    foreach ($f in $jsFiles) {
        Write-Host "--- Running: $($f.Name) ---" -ForegroundColor Green
        node $f.Name
        Write-Host ""
    }
}

Write-Host "=== Done ===" -ForegroundColor Cyan
