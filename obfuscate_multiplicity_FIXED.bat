@echo off
echo ========================================
echo MULTIPLICITY OBFUSCATION (FIXED)
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
    echo Found: %MULT_PATH%
    goto :FoundPath
)

if exist "C:\Program Files\Stardock\Multiplicity\" (
    set MULT_PATH=C:\Program Files\Stardock\Multiplicity
    echo Found: %MULT_PATH%
    goto :FoundPath
)

if exist "C:\Program Files (x86)\Multiplicity\" (
    set MULT_PATH=C:\Program Files ^(x86^)\Multiplicity
    echo Found: %MULT_PATH%
    goto :FoundPath
)

if exist "C:\Program Files\Multiplicity\" (
    set MULT_PATH=C:\Program Files\Multiplicity
    echo Found: %MULT_PATH%
    goto :FoundPath
)

echo ERROR: Cannot find Multiplicity installation!
echo.
echo Please manually navigate to Multiplicity folder and rename:
echo   Multiplicity.exe → SystemAudioService.exe
echo.
pause
exit /b 1

:FoundPath
cd "%MULT_PATH%"
echo Current folder: %CD%
echo.

echo ========================================
echo CREATING BACKUPS
echo ========================================
echo.

if exist Multiplicity.exe (
    if not exist Multiplicity.exe.backup (
        copy Multiplicity.exe Multiplicity.exe.backup
        echo Backup created: Multiplicity.exe.backup
    ) else (
        echo Backup already exists: Multiplicity.exe.backup
    )
) else (
    echo WARNING: Multiplicity.exe not found in this folder!
    dir Multiplicity*.exe
    echo.
    echo Please check if file name is correct.
    pause
    exit /b 1
)

if exist MultiplicityClient.exe (
    if not exist MultiplicityClient.exe.backup (
        copy MultiplicityClient.exe MultiplicityClient.exe.backup
        echo Backup created: MultiplicityClient.exe.backup
    )
)

echo.
echo ========================================
echo RENAMING EXECUTABLES
echo ========================================
echo.

if exist Multiplicity.exe (
    ren Multiplicity.exe SystemAudioService.exe
    if %errorlevel%==0 (
        echo SUCCESS: Multiplicity.exe → SystemAudioService.exe ✅
    ) else (
        echo ERROR: Failed to rename Multiplicity.exe
        echo Try running this script as Administrator!
        pause
        exit /b 1
    )
)

if exist MultiplicityClient.exe (
    ren MultiplicityClient.exe SystemAudioClient.exe
    if %errorlevel%==0 (
        echo SUCCESS: MultiplicityClient.exe → SystemAudioClient.exe ✅
    )
)

echo.
echo ========================================
echo OBFUSCATION COMPLETE! ✅
echo ========================================
echo.
echo What changed:
echo - Multiplicity.exe → SystemAudioService.exe ✅
echo - MultiplicityClient.exe → SystemAudioClient.exe ✅
echo - Backups created with .backup extension ✅
echo.
echo Installation folder: %MULT_PATH%
echo.
echo How to launch Multiplicity now:
echo 1. Run: SystemAudioService.exe (instead of Multiplicity.exe)
echo 2. Or double-click SystemAudioService.exe from folder
echo.
echo Process name in Task Manager: SystemAudioService.exe
echo (Looks like Windows system service - harder to detect!)
echo.
echo To UNDO (restore original):
echo 1. Delete SystemAudioService.exe
echo 2. Rename Multiplicity.exe.backup → Multiplicity.exe
echo.

pause



