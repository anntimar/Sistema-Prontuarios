param(
    [switch]$SkipAudit
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$FrontendDir = Join-Path $Root "frontend"
$PythonExe = Join-Path $Root ".venv\Scripts\python.exe"

Set-Location $Root

if (-not (Test-Path $PythonExe)) {
    throw "Ambiente virtual nao encontrado. Execute scripts/setup_dev.ps1 primeiro."
}

Write-Host "Rodando testes do backend..."
& $PythonExe -m unittest discover -s tests

Write-Host "Validando compilacao Python..."
& $PythonExe -m compileall backend scripts

Push-Location $FrontendDir
try {
    Write-Host "Gerando build do frontend..."
    npm run build

    if (-not $SkipAudit) {
        Write-Host "Rodando npm audit..."
        npm audit
    }
}
finally {
    Pop-Location
}

Write-Host ""
Write-Host "Checks concluidos."
