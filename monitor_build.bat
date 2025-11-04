@echo off
REM Simple progress indicator script
REM Run this in a separate window while build_stealth.bat is running

:loop
echo [%TIME%] Build still running... (Press Ctrl+C to stop this monitor)
timeout /t 30 /nobreak >nul 2>&1
if exist "dist\ExplorerSettings\ExplorerSettings.exe" (
    echo [✓] Build completed! Executable found in dist\ExplorerSettings\
    pause
    exit /b 0
)
goto loop

