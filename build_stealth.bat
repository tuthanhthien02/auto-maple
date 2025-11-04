@echo off
setlocal ENABLEDELAYEDEXPANSION

REM Change to script directory
cd /d "%~dp0"

echo [~] Building ExplorerSettings (PyInstaller stealth)...

REM Ensure pip and pyinstaller
python -m pip install --upgrade pip >nul 2>&1
python -m pip install --upgrade pyinstaller >nul 2>&1

REM Clean previous builds
REM Kill ExplorerSettings.exe if running (multiple attempts)
echo [~] Stopping ExplorerSettings.exe if running...
taskkill /F /IM ExplorerSettings.exe >nul 2>&1
timeout /t 2 /nobreak >nul 2>&1
taskkill /F /IM ExplorerSettings.exe >nul 2>&1
timeout /t 2 /nobreak >nul 2>&1

REM Kill Python processes that might be locking files
echo [~] Stopping Python processes...
taskkill /F /FI "WINDOWTITLE eq *ExplorerSettings*" >nul 2>&1
timeout /t 1 /nobreak >nul 2>&1

REM Try to remove directories with retry
echo [~] Cleaning build directories...
if exist build (
    rmdir /s /q build 2>nul
    if exist build (
        timeout /t 2 /nobreak >nul 2>&1
        rmdir /s /q build 2>nul
    )
)
if exist dist (
    rmdir /s /q dist 2>nul
    if exist dist (
        timeout /t 2 /nobreak >nul 2>&1
        rmdir /s /q dist 2>nul
    )
)
if exist __pycache__ rmdir /s /q __pycache__ 2>nul
for /r %%i in (*.__pycache__) do rmdir /s /q "%%i" 2>nul

REM Run PyInstaller với spec file (tất cả options đã có trong spec file)
REM Note: Khi dùng .spec file, không thể dùng --name, --add-data, --strip, etc. trong command line
REM Use INFO level - shows major steps (Analyzing, Collecting, Building, etc.)
echo [~] Starting PyInstaller build...
echo [INFO] Estimated time: 5-20 minutes
echo [INFO] You will see progress messages below:
echo [INFO]   - "INFO: Analyzing..." = Analyzing dependencies
echo [INFO]   - "INFO: Collecting..." = Collecting files
echo [INFO]   - "INFO: Building..." = Building executable
echo [INFO]   - "INFO: Successfully" = Build complete!
echo.
echo [~] Build started at %TIME%
echo ========================================
pyinstaller --noconfirm --clean --log-level=INFO ExplorerSettings.spec
echo ========================================
echo [~] Build finished at %TIME%

set EXITCODE=%ERRORLEVEL%
if %EXITCODE% NEQ 0 (
  echo [!] Build failed with code %EXITCODE%
  pause
  exit /b %EXITCODE%
)

echo.
echo [✓] Build completed successfully!
echo [✓] Executable location: .\dist\ExplorerSettings\ExplorerSettings.exe
echo.
echo [INFO] About build folders:
echo   - dist\ = Contains your executable (USE THIS!)
echo   - build\ = Temporary build files (can be deleted)
echo.
echo [INFO] You can delete the build\ folder to save space (optional)
echo [INFO] The dist\ folder contains everything you need to run the bot
echo.
pause
endlocal


