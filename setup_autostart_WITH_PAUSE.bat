@echo off
REM ═══════════════════════════════════════════════════════════
REM SETUP AUTOSTART FOR WITH_PAUSE SCRIPT
REM ═══════════════════════════════════════════════════════════

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║   🚀 SETUP AUTOSTART 🚀                               ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM List available .exe files
echo 📦 Available compiled scripts:
echo.
dir /b *.exe 2>nul
echo.

if errorlevel 1 (
    echo ❌ No .exe files found!
    echo.
    echo Please compile first:
    echo    1. Run compile_WITH_PAUSE.bat OR
    echo    2. Run compile_WITH_PAUSE_obfuscate.bat
    echo.
    pause
    exit /b 1
)

REM Ask user which file to autostart
set /p EXENAME="Enter .exe filename (from list above): "

if not exist "%EXENAME%" (
    echo.
    echo ❌ ERROR: %EXENAME% not found!
    echo.
    pause
    exit /b 1
)

REM Get full path
set FULLPATH=%CD%\%EXENAME%

echo.
echo 🔧 Setting up autostart for: %EXENAME%
echo 📂 Path: %FULLPATH%
echo.

REM Create registry entry
REG ADD "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsJitterService" /t REG_SZ /d "\"%FULLPATH%\"" /f

if errorlevel 1 (
    echo.
    echo ❌ FAILED to create registry entry!
    echo.
    echo Try running as Administrator!
    echo.
    pause
    exit /b 1
)

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║   ✅ AUTOSTART SETUP SUCCESSFUL! ✅                   ║
echo ║                                                        ║
echo ║   Script will now run on Windows startup!             ║
echo ║                                                        ║
echo ║   Registry: HKCU\...\Run                              ║
echo ║   Name: WindowsJitterService                          ║
echo ║   Path: %EXENAME%
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo 🎯 What happens now:
echo    - Script runs automatically when Windows starts
echo    - No need to manually run it
echo    - Works after reboot ✅
echo.
echo 🧪 Test now:
echo    1. Restart computer
echo    2. After login, check system tray for "H" icon
echo    3. Should be running automatically! ✅
echo.
echo ⚠️ To REMOVE autostart:
echo    Run: remove_autostart_custom.bat
echo.
pause

