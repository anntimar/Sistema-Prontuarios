param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 8000
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$PythonExe = Join-Path $Root ".venv\Scripts\python.exe"
$EnvFile = Join-Path $Root ".env"

Set-Location $Root

if (-not (Test-Path $PythonExe)) {
    throw "Ambiente virtual nao encontrado. Execute scripts/setup_dev.ps1 primeiro."
}

if (-not (Test-Path $EnvFile)) {
    Write-Warning ".env nao encontrado. Copie .env.example para .env e preencha as credenciais."
}

& $PythonExe -m uvicorn backend.main:app --reload --host $HostAddress --port $Port
