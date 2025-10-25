@echo off
echo ========================================
echo SETUP AUTO-START FOR COMPILED SCRIPTS
echo ========================================
echo.
echo This will make scripts start automatically on Windows boot.
echo.
pause

set STARTUP_FOLDER=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup

echo.
echo Creating shortcuts in Startup folder...
echo.

if exist "WindowsAudioDriver.exe" (
    echo Creating shortcut for WindowsAudioDriver.exe
    powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%STARTUP_FOLDER%\WindowsAudioDriver.lnk');$s.TargetPath='%CD%\WindowsAudioDriver.exe';$s.Save()"
    echo ✅ WindowsAudioDriver.exe will auto-start on boot
    echo.
)

if exist "SystemInputService.exe" (
    echo Creating shortcut for SystemInputService.exe
    powershell "$s=(New-Object -COM WScript.Shell).CreateShortcut('%STARTUP_FOLDER%\SystemInputService.lnk');$s.TargetPath='%CD%\SystemInputService.exe';$s.Save()"
    echo ✅ SystemInputService.exe will auto-start on boot
    echo.
)

echo.
echo ========================================
echo AUTO-START CONFIGURED!
echo ========================================
echo.
echo Scripts will start automatically when Windows boots.
echo.
echo To remove auto-start:
echo 1. Press Win+R
echo 2. Type: shell:startup
echo 3. Delete the shortcuts
echo.

pause



