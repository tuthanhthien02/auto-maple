$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

Write-Host "[~] Building ExplorerSettings (PyInstaller stealth)..."

python -m pip install --upgrade pip | Out-Null
python -m pip install --upgrade pyinstaller | Out-Null

if (Test-Path build) { Remove-Item build -Recurse -Force }
if (Test-Path dist) { Remove-Item dist -Recurse -Force }

pyinstaller --noconfirm --clean `
  --name "ExplorerSettings" `
  --windowed `
  --icon "assets/explorer-icon.ico" `
  --add-data "assets;assets" `
  --add-data "resources;resources" `
  --add-data "src;src" `
  main.py

if ($LASTEXITCODE -ne 0) {
  Write-Host "[!] Build failed with code $LASTEXITCODE"
  Read-Host "Press Enter to exit"
  exit $LASTEXITCODE
}

Write-Host "[✓] Build OK: .\dist\ExplorerSettings\ExplorerSettings.exe"
Read-Host "Press Enter to exit"


