@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   REMOVE AUTOSTART - STEALTH VERSION
echo ========================================
echo.

echo Removing from Windows startup...
echo.
echo Registry Key: HKCU\Software\Microsoft\Windows\CurrentVersion\Run
echo Value Name: WindowsUpdateHelper
echo.

REM Remove from registry
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdateHelper" /f

if errorlevel 1 (
    echo.
    echo ========================================
    echo   VALUE NOT FOUND OR ALREADY REMOVED
    echo ========================================
    echo.
    pause
    exit /b 0
)

echo.
echo ========================================
echo   REMOVAL SUCCESS!
echo ========================================
echo.
echo WindowsUpdateHelper.exe will NO LONGER start on Windows boot
echo.
echo To re-enable auto-start, run: setup_autostart_STEALTH.bat
echo.
pause

