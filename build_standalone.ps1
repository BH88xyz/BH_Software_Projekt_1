$ErrorActionPreference = "Stop"

Set-Location -LiteralPath $PSScriptRoot
$python = Join-Path $PSScriptRoot ".venv\Scripts\python.exe"

if (-not (Test-Path -LiteralPath $python)) {
    py -m venv .venv
    if ($LASTEXITCODE -ne 0) {
        throw "Could not create the project build environment."
    }
}

& $python -m pip install --upgrade pyinstaller
if ($LASTEXITCODE -ne 0) {
    throw "Could not install PyInstaller in the project build environment."
}

& $python -m PyInstaller --noconfirm --clean --onefile --name BH_Arithmetic --add-data "index.html;." --add-data "styles.css;." --add-data "app.js;." app.py
if ($LASTEXITCODE -ne 0) {
    throw "The standalone build failed. See the PyInstaller output above."
}

Write-Output "Standalone app built: $PSScriptRoot\dist\BH_Arithmetic.exe"