@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   SETUP AUTOSTART - STEALTH VERSION
echo ========================================
echo.

REM Check if obfuscated exe exists
if not exist "WindowsSecurityHelper.exe" (
    echo ERROR: WindowsSecurityHelper.exe not found!
    echo.
    echo Please run compile_STEALTH_obfuscate.bat first
    echo.
    pause
    exit /b 1
)

REM Get current directory
set CURRENT_DIR=%~dp0
set EXE_PATH=%CURRENT_DIR%WindowsSecurityHelper.exe

echo Adding to Windows startup...
echo.
echo Registry Key: HKCU\Software\Microsoft\Windows\CurrentVersion\Run
echo Value Name: WindowsSecurityHelper
echo Value Data: "%EXE_PATH%"
echo.

REM Add to registry
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsSecurityHelper" /t REG_SZ /d "\"%EXE_PATH%\"" /f

if errorlevel 1 (
    echo.
    echo ========================================
    echo   SETUP FAILED!
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   SETUP SUCCESS!
echo ========================================
echo.
echo WindowsSecurityHelper.exe will now start automatically on Windows boot!
echo.
echo STEALTH FEATURES:
echo - No tray icon (invisible!)
echo - Runs in background
echo - Ctrl+Alt+S to check status
echo - Ctrl+Alt+Q to exit
echo.
echo To disable auto-start, run: remove_autostart_STEALTH.bat
echo.
pause

