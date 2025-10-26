@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   REMOVE AUTO-START - EASY CUSTOM
echo ========================================
echo.

echo Removing from Windows startup...
echo.

REM Remove from registry
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemAudioService" /f

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   AUTO-START DISABLED!
    echo ========================================
    echo.
    echo The script will no longer run automatically on Windows startup.
    echo.
) else (
    echo.
    echo NOTE: Entry may not exist or was already removed.
    echo.
)

pause

