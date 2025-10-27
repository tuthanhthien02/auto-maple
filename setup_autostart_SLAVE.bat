@echo off
cd /d "%~dp0"

echo ========================================
echo   SETUP AUTOSTART - SLAVE VERSION
echo ========================================
echo.
echo This will add SystemAudioService.exe to Windows startup
echo Run this in EACH VM!
echo.

REM Check if exe exists
if not exist "SystemAudioService.exe" (
    echo ERROR: SystemAudioService.exe not found!
    echo Please compile first using compile_SLAVE_obfuscate.bat
    pause
    exit /b 1
)

REM Get current directory
set "CURRENT_DIR=%CD%"
set "EXE_PATH=%CURRENT_DIR%\SystemAudioService.exe"

echo Exe path: %EXE_PATH%
echo.
echo Adding to Windows startup registry...

REM Add to registry (HKCU for current user)
reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" /v "SystemAudioService" /t REG_SZ /d "\"%EXE_PATH%\"" /f

if errorlevel 1 (
    echo.
    echo ERROR: Failed to add to registry!
    pause
    exit /b 1
)

echo.
echo ========================================
echo   AUTOSTART SETUP SUCCESSFUL!
echo ========================================
echo.
echo SystemAudioService.exe will run automatically on Windows startup!
echo.
echo To remove autostart, run: remove_autostart_SLAVE.bat
echo.
pause

