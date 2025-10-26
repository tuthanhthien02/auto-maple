@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   SETUP AUTO-START - AUTO PAUSE
echo ========================================
echo.

REM Check if compiled exe exists
if not exist "auto_pause_only.exe" (
    if not exist "WindowsUpdateHelper.exe" (
        echo ERROR: No compiled exe found!
        echo Please run compile_auto_pause.bat or compile_auto_pause_obfuscate.bat first.
        pause
        exit /b 1
    )
    set "EXE_NAME=WindowsUpdateHelper.exe"
) else (
    set "EXE_NAME=auto_pause_only.exe"
)

echo Found: %EXE_NAME%
echo.

REM Get full path
set "FULL_PATH=%~dp0%EXE_NAME%"

echo Adding to Windows startup...
echo.

REM Add to registry (Run on boot)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdateHelper" /t REG_SZ /d "\"%FULL_PATH%\"" /f

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   AUTO-START ENABLED!
    echo ========================================
    echo.
    echo %EXE_NAME% will now run automatically on Windows startup.
    echo.
    echo To disable auto-start, run: remove_autostart_auto_pause.bat
    echo.
) else (
    echo.
    echo ERROR: Failed to add to startup!
    echo.
)

pause

