@echo off
REM Cleanup script - Kill all processes and clean directories before build

echo [~] Cleanup script - Preparing for build...
echo.

REM Kill ExplorerSettings.exe
echo [1/4] Stopping ExplorerSettings.exe...
taskkill /F /IM ExplorerSettings.exe >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo     [OK] ExplorerSettings.exe stopped
) else (
    echo     [INFO] ExplorerSettings.exe not running
)
timeout /t 2 /nobreak >nul 2>&1

REM Kill Python processes (might be running bot)
echo [2/4] Stopping Python processes...
taskkill /F /IM python.exe >nul 2>&1
taskkill /F /IM pythonw.exe >nul 2>&1
timeout /t 2 /nobreak >nul 2>&1

REM Kill any processes using files in dist directory
echo [3/4] Checking for locked files...
REM This is a best-effort attempt, may not catch all

REM Clean directories
echo [4/4] Cleaning build directories...
if exist build (
    echo     Removing build directory...
    rmdir /s /q build 2>nul
    if exist build (
        echo     [WARNING] Build directory still exists, may need manual cleanup
    ) else (
        echo     [OK] Build directory removed
    )
)

if exist dist (
    echo     Removing dist directory...
    rmdir /s /q dist 2>nul
    if exist dist (
        echo     [WARNING] Dist directory still exists, may need manual cleanup
        echo     [TIP] Close any programs that might be using files in dist folder
        echo     [TIP] Or restart your computer and try again
    ) else (
        echo     [OK] Dist directory removed
    )
)

echo.
echo [✓] Cleanup complete!
echo [INFO] You can now run build_stealth.bat
pause

