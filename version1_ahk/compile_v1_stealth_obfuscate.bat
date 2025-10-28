@echo off
cd /d "%~dp0"

echo.
echo ========================================
echo   COMPILE STEALTH - OBFUSCATED
echo ========================================
echo.

echo Step 1: Compiling AHK script...
"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" /in "multiplicity_jitter_DESYNC_STEALTH.ahk" /out "multiplicity_jitter_DESYNC_STEALTH_temp.exe"

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
echo Step 2: Obfuscating filename...

REM Delete old obfuscated file if exists
if exist "WindowsSecurityHelper.exe" (
    del /F /Q "WindowsSecurityHelper.exe"
)

REM Rename to obfuscated name
move /Y "multiplicity_jitter_DESYNC_STEALTH_temp.exe" "WindowsSecurityHelper.exe"

echo.
echo ========================================
echo   COMPILATION SUCCESS!
echo ========================================
echo.
echo Output: WindowsSecurityHelper.exe
echo.
echo ANTI-DETECTION FEATURES:
echo - Obfuscated filename (looks like Windows service)
echo - No tray icon (invisible in system tray)
echo - Compiled to .exe (harder to detect than .ahk)
echo - Desync delay breaks Multiplicity synchronization
echo - Jitter makes timing unpredictable
echo - Behavioral pauses mimic human breaks
echo.
echo STEALTH HOTKEYS:
echo - Ctrl+Alt+T = Toggle ON/OFF
echo - Ctrl+Alt+S = Check status
echo - Ctrl+Alt+Q = Exit script
echo.
echo Next steps:
echo 1. Test WindowsSecurityHelper.exe
echo 2. Run setup_autostart_STEALTH.bat to enable auto-start
echo 3. Use remove_autostart_STEALTH.bat to disable if needed
echo.
pause

