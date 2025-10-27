@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   COMPILE STEALTH VERSION
echo ========================================
echo.

"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" /in "multiplicity_jitter_DESYNC_STEALTH.ahk" /out "multiplicity_jitter_DESYNC_STEALTH.exe"

if errorlevel 1 (
    echo.
    echo ========================================
    echo   COMPILATION FAILED!
    echo ========================================
    echo.
    pause
    exit /b 1
)

echo.
echo ========================================
echo   COMPILATION SUCCESS!
echo ========================================
echo.
echo Output: multiplicity_jitter_DESYNC_STEALTH.exe
echo.
echo STEALTH FEATURES:
echo - No tray icon (invisible in system tray)
echo - Runs in background silently
echo - Ctrl+Alt+S to check status
echo - Ctrl+Alt+Q to exit
echo.
echo Next steps:
echo 1. Test multiplicity_jitter_DESYNC_STEALTH.exe
echo 2. Run setup_autostart_STEALTH.bat to enable auto-start
echo.
pause

