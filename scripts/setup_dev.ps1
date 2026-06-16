param(
    [switch]$SkipPythonInstall,
    [switch]$SkipNodeInstall,
    [switch]$ForceEnv
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$FrontendDir = Join-Path $Root "frontend"
$PythonExe = Join-Path $Root ".venv\Scripts\python.exe"
$EnvFile = Join-Path $Root ".env"
$EnvExample = Join-Path $Root ".env.example"
$FrontendEnvFile = Join-Path $FrontendDir ".env"
$FrontendEnvExample = Join-Path $FrontendDir ".env.example"

Set-Location $Root

if (-not (Test-Path $PythonExe)) {
    Write-Host "Criando ambiente virtual Python..."
    python -m venv .venv
}

if (-not $SkipPythonInstall) {
    Write-Host "Instalando dependencias Python..."
    & $PythonExe -m pip install -r requirements.txt
}

if ((-not (Test-Path $EnvFile)) -or $ForceEnv) {
    Write-Host "Copiando .env.example para .env..."
    Copy-Item -Path $EnvExample -Destination $EnvFile -Force
}

if ((-not (Test-Path $FrontendEnvFile)) -or $ForceEnv) {
    Write-Host "Copiando frontend/.env.example para frontend/.env..."
    Copy-Item -Path $FrontendEnvExample -Destination $FrontendEnvFile -Force
}

if (-not $SkipNodeInstall) {
    Write-Host "Instalando dependencias do frontend..."
    Push-Location $FrontendDir
    try {
        npm install
    }
    finally {
        Pop-Location
    }
}

Write-Host ""
Write-Host "Setup concluido."
Write-Host "Agora preencha o arquivo .env com SUPABASE_URL, SUPABASE_KEY e SECRET_KEY."
Write-Host "Depois execute scripts/run_backend.ps1 e scripts/run_frontend.ps1 em terminais separados."
