@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   COMPILE STEALTH VERSION
echo ========================================
echo.

"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" /in "multiplicity_v1_stealth.ahk" /out "multiplicity_v1_stealth.exe"

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
echo Output: multiplicity_v1_stealth.exe
echo.
echo STEALTH FEATURES:
echo - No tray icon (invisible in system tray)
echo - Runs in background silently
echo - Ctrl+Alt+S to check status
echo - Ctrl+Alt+Q to exit
echo.
echo Next steps:
echo 1. Test multiplicity_v1_stealth.exe
echo 2. Run setup_autostart_v1_stealth.bat to enable auto-start
echo.
pause

