$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot

Write-Host "AI QUANT TRADER — установка зависимостей" -ForegroundColor Cyan
if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python Launcher (py) не найден. Установите Python 3.12 и повторите."
}
if (-not (Test-Path ".venv\Scripts\python.exe")) {
    py -3.12 -m venv .venv
}
$Python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $Python)) { throw "Не удалось создать виртуальное окружение: $Python" }

& $Python -m pip install --upgrade pip
if ($LASTEXITCODE -ne 0) { throw "Не удалось обновить pip." }
& $Python -m pip install -r requirements.txt
if ($LASTEXITCODE -ne 0) { throw "Не удалось установить зависимости." }

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Copy-Item ".env.example" ".env"
    Write-Host "Создан .env из .env.example. Проверьте OLLAMA_MODEL при необходимости." -ForegroundColor Yellow
}

& $Python -m compileall -q app tests
if ($LASTEXITCODE -ne 0) { throw "Ошибка компиляции Python." }
& $Python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "Автоматические тесты завершились с ошибками." }

Write-Host "Установка и проверки завершены. Сервер НЕ запускался." -ForegroundColor Green
