@echo off
echo ═══════════════════════════════════════════════════════
echo RUNNING TEST_JITTER_NOW.ahk AS ADMINISTRATOR
echo ═══════════════════════════════════════════════════════
echo.

REM Get the full path to the AHK file
set "AHK_FILE=%~dp0TEST_JITTER_NOW.ahk"

echo File: %AHK_FILE%
echo.

REM Check if file exists
if not exist "%AHK_FILE%" (
    echo ❌ ERROR: TEST_JITTER_NOW.ahk not found!
    pause
    exit /b 1
)

echo Starting with Administrator privileges...
echo.

REM Run as admin
powershell -Command "Start-Process 'AutoHotkey.exe' -ArgumentList '%AHK_FILE%' -Verb RunAs"

echo.
echo ✅ Script launched!
echo Check system tray for "H" icon.
echo.
pause

