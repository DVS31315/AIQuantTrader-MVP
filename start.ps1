$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot
$Python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) {
    throw "Окружение не найдено. Сначала выполните: .\install.ps1"
}
if (-not (Test-Path ".env")) {
    if (Test-Path ".env.example") { Copy-Item ".env.example" ".env" }
    else { throw ".env и .env.example не найдены." }
}
Write-Host "Запуск AI QUANT TRADER в PAPER MODE. Реальные ордера не поддерживаются." -ForegroundColor Cyan
& $Python -m app.run
