@echo off
cd /d "%~dp0"

echo ========================================
echo   REMOVE AUTOSTART - SLAVE VERSION
echo ========================================
echo.
echo Removing SystemAudioService from Windows startup...

REM Remove from registry
reg delete "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemAudioService" /f

if errorlevel 1 (
    echo.
    echo Note: SystemAudioService was not in startup registry
    echo (This is OK if you never ran setup_autostart_SLAVE.bat)
) else (
    echo.
    echo ========================================
    echo   AUTOSTART REMOVED!
    echo ========================================
    echo.
    echo SystemAudioService will no longer run on Windows startup
)

echo.
pause

