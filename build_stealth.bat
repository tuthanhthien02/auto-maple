@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Change to script directory
cd /d "%~dp0"

echo [~] Building ExplorerSettings (PyInstaller stealth)...

REM Ensure pip and pyinstaller
python -m pip install --upgrade pip >nul 2>&1
python -m pip install --upgrade pyinstaller >nul 2>&1

REM Clean previous builds
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist __pycache__ rmdir /s /q __pycache__
for /r %%i in (*.__pycache__) do rmdir /s /q "%%i" >nul 2>&1

REM Run PyInstaller
pyinstaller --noconfirm --clean ^
  --name "ExplorerSettings" ^
  --windowed ^
  --icon "assets/explorer-icon.ico" ^
  --add-data "assets;assets" ^
  --add-data "resources;resources" ^
  --add-data "src;src" ^
  main.py

set EXITCODE=%ERRORLEVEL%
if %EXITCODE% NEQ 0 (
  echo [!] Build failed with code %EXITCODE%
  pause
  exit /b %EXITCODE%
)

echo [✓] Build OK: .\dist\ExplorerSettings\ExplorerSettings.exe
pause
endlocal


