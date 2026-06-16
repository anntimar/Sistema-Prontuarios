param(
    [string]$HostAddress = "127.0.0.1",
    [int]$Port = 5173
)

$ErrorActionPreference = "Stop"

$Root = Split-Path -Parent $PSScriptRoot
$FrontendDir = Join-Path $Root "frontend"

if (-not (Test-Path (Join-Path $FrontendDir "node_modules"))) {
    throw "Dependencias do frontend nao encontradas. Execute scripts/setup_dev.ps1 primeiro."
}

Push-Location $FrontendDir
try {
    npm run dev -- --host $HostAddress --port $Port
}
finally {
    Pop-Location
}
