@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   COMPILE ULTRA STEALTH - OBFUSCATED
echo ========================================
echo.

echo Step 1: Compiling AHK script...
"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" /in "multiplicity_v1_stealth.ahk" /out "multiplicity_v1_stealth_temp.exe"

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
echo Step 2: Ultra stealth obfuscation...

REM Delete old obfuscated file if exists
if exist "WindowsUpdateHelper.exe" (
    del /F /Q "WindowsUpdateHelper.exe"
)

REM Rename to obfuscated name
move /Y "multiplicity_v1_stealth_temp.exe" "WindowsUpdateHelper.exe"

echo.
echo ========================================
echo   ULTRA STEALTH COMPILATION SUCCESS!
echo ========================================
echo.
echo Output: WindowsUpdateHelper.exe
echo.
echo ULTRA STEALTH FEATURES:
echo - Obfuscated filename (WindowsUpdateHelper.exe)
echo - NO tray icon (completely invisible!)
echo - NO startup beep or tooltip
echo - Compiled to .exe (harder to detect)
echo - Desync delay breaks synchronization
echo - Jitter makes timing unpredictable
echo - Behavioral pauses mimic human breaks
echo - Process runs in background silently
echo.
echo STEALTH HOTKEYS:
echo - Ctrl+Alt+T = Toggle ON/OFF
echo - Ctrl+Alt+S = Check status
echo - Ctrl+Alt+Q = Exit script
echo.
echo IMPORTANT: Check system tray - NO icon should be visible!
echo.
echo Next steps:
echo 1. Test WindowsUpdateHelper.exe (should be invisible)
echo 2. Run setup_autostart_v1_stealth.bat to enable auto-start
echo 3. Use remove_autostart_v1_stealth.bat to disable if needed
echo.
pause
