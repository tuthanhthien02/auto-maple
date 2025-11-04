$ErrorActionPreference = 'Stop'
Set-Location -Path $PSScriptRoot

Write-Host "[~] Building ExplorerSettings (PyInstaller stealth)..."

python -m pip install --upgrade pip | Out-Null
python -m pip install --upgrade pyinstaller | Out-Null

# Kill ExplorerSettings.exe if running (multiple attempts)
Write-Host "[~] Stopping ExplorerSettings.exe if running..."
Get-Process -Name "ExplorerSettings" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2
Get-Process -Name "ExplorerSettings" -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

# Kill Python processes that might be locking files
Write-Host "[~] Stopping Python processes..."
Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowTitle -like "*ExplorerSettings*" } | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 1

# Try to remove directories with retry
Write-Host "[~] Cleaning build directories..."
if (Test-Path build) {
    Remove-Item build -Recurse -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    if (Test-Path build) {
        Start-Sleep -Seconds 2
        Remove-Item build -Recurse -Force -ErrorAction SilentlyContinue
    }
}
if (Test-Path dist) {
    Remove-Item dist -Recurse -Force -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 1
    if (Test-Path dist) {
        Start-Sleep -Seconds 2
        Remove-Item dist -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Run PyInstaller với spec file (tất cả options đã có trong spec file)
# Note: Khi dùng .spec file, không thể dùng --name, --add-data, --strip, etc. trong command line
pyinstaller --noconfirm --clean ExplorerSettings.spec

if ($LASTEXITCODE -ne 0) {
  Write-Host "[!] Build failed with code $LASTEXITCODE"
  Read-Host "Press Enter to exit"
  exit $LASTEXITCODE
}

Write-Host "[✓] Build OK: .\dist\ExplorerSettings\ExplorerSettings.exe"
Read-Host "Press Enter to exit"


