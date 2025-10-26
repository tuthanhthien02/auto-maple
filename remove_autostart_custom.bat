@echo off
REM ═══════════════════════════════════════════════════════════
REM REMOVE AUTOSTART FOR CUSTOM JITTER
REM ═══════════════════════════════════════════════════════════

REM Change to the directory where this batch file is located
cd /d "%~dp0"

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║   🗑️ REMOVE AUTOSTART 🗑️                             ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

echo Removing autostart entry...
echo.

REG DELETE "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsJitterService" /f

if errorlevel 1 (
    echo ❌ Entry not found or already removed!
) else (
    echo ✅ Autostart removed successfully!
)

echo.
echo Script will NO LONGER run on Windows startup.
echo.
pause

