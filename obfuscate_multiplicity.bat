@echo off
echo ========================================
echo MULTIPLICITY OBFUSCATION (LAYER 7 PREVIEW)
echo ========================================
echo.
echo WARNING: This will rename Multiplicity executable to hide it from detection.
echo Make sure Multiplicity is CLOSED before proceeding!
echo.
echo This script will:
echo 1. Backup original Multiplicity.exe
echo 2. Rename to SystemAudioService.exe (looks like Windows service)
echo 3. Update shortcuts
echo.
echo Press Ctrl+C to cancel, or
pause

echo.
echo Checking if Multiplicity is running...
tasklist | find /i "Multiplicity.exe" >nul
if %errorlevel%==0 (
    echo ERROR: Multiplicity is still running!
    echo Please close Multiplicity first, then run this script again.
    pause
    exit /b 1
)

echo.
echo ========================================
echo FINDING MULTIPLICITY INSTALLATION
echo ========================================
echo.

REM Try all possible installation paths
set MULT_PATH=

if exist "C:\Program Files (x86)\Stardock\Multiplicity\" (
    set MULT_PATH=C:\Program Files ^(x86^)\Stardock\Multiplicity
    goto :FoundPath
)

if exist "C:\Program Files\Stardock\Multiplicity\" (
    set MULT_PATH=C:\Program Files\Stardock\Multiplicity
    goto :FoundPath
)

if exist "C:\Program Files (x86)\Multiplicity\" (
    set MULT_PATH=C:\Program Files ^(x86^)\Multiplicity
    goto :FoundPath
)

if exist "C:\Program Files\Multiplicity\" (
    set MULT_PATH=C:\Program Files\Multiplicity
    goto :FoundPath
)

echo ERROR: Cannot find Multiplicity installation folder!
echo Please install Multiplicity first.
pause
exit /b 1

:FoundPath
cd "%MULT_PATH%"

echo Found Multiplicity folder: %CD%
echo.

echo Creating backup...
if exist Multiplicity.exe (
    copy Multiplicity.exe Multiplicity.exe.backup
    echo Backup created: Multiplicity.exe.backup
)

if exist MultiplicityClient.exe (
    copy MultiplicityClient.exe MultiplicityClient.exe.backup
    echo Backup created: MultiplicityClient.exe.backup
)

echo.
echo Renaming executables...

if exist Multiplicity.exe (
    ren Multiplicity.exe SystemAudioService.exe
    if %errorlevel%==0 (
        echo SUCCESS: Multiplicity.exe → SystemAudioService.exe
    ) else (
        echo ERROR: Failed to rename. Run as Administrator?
    )
)

if exist MultiplicityClient.exe (
    ren MultiplicityClient.exe SystemAudioClient.exe
    if %errorlevel%==0 (
        echo SUCCESS: MultiplicityClient.exe → SystemAudioClient.exe
    ) else (
        echo ERROR: Failed to rename. Run as Administrator?
    )
)

echo.
echo ========================================
echo OBFUSCATION COMPLETE!
echo ========================================
echo.
echo What changed:
echo - Multiplicity.exe → SystemAudioService.exe
echo - MultiplicityClient.exe → SystemAudioClient.exe
echo.
echo How to launch:
echo - Run: SystemAudioService.exe (instead of Multiplicity.exe)
echo - Process name in Task Manager: SystemAudioService.exe
echo - Looks like Windows system service ✅
echo.
echo To UNDO (restore original):
echo - Delete SystemAudioService.exe
echo - Rename Multiplicity.exe.backup → Multiplicity.exe
echo.
echo IMPORTANT: You'll need to update shortcuts!
echo Right-click shortcut → Properties → Target:
echo Change to: "C:\Program Files\Multiplicity\SystemAudioService.exe"
echo.

pause

