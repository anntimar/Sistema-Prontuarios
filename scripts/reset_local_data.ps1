$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$seed = Join-Path $root "backend\data\local_seed.json"
$database = Join-Path $root "backend\data\local_db.json"
$storage = Join-Path $root "backend\data\storage"

if (-not (Test-Path $seed)) {
    throw "Seed local nao encontrado em $seed"
}

Copy-Item $seed $database -Force

if (Test-Path $storage) {
    Remove-Item $storage -Recurse -Force
}
New-Item -ItemType Directory -Path $storage | Out-Null

Write-Host "Base local restaurada em backend/data/local_db.json"
