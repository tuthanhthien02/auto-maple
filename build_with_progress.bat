@echo off
REM Build wrapper with progress indicator
REM This script runs build_stealth.bat and shows progress dots

echo [~] Starting build with progress indicator...
echo [INFO] Build may take 5-20 minutes
echo [INFO] Dots (.) indicate build is running - please wait...
echo.

REM Start build in background and show progress
start /B cmd /c "build_stealth.bat > build_output.log 2>&1"

REM Show progress dots while build is running
set COUNTER=0
:loop
timeout /t 5 /nobreak >nul 2>&1
set /a COUNTER+=1
set /a DOT=COUNTER %% 4
if %DOT%==0 echo [%TIME%] Build running... (checking for completion)
if exist "dist\ExplorerSettings\ExplorerSettings.exe" (
    echo.
    echo [✓] Build completed successfully!
    echo [✓] Executable: dist\ExplorerSettings\ExplorerSettings.exe
    type build_output.log | findstr /C:"INFO:" /C:"WARNING:" /C:"ERROR:" /C:"Successfully"
    del build_output.log 2>nul
    pause
    exit /b 0
)
REM Check if build failed
findstr /C:"Build failed" build_output.log >nul 2>&1
if %ERRORLEVEL%==0 (
    echo.
    echo [!] Build failed - check build_output.log for details
    type build_output.log
    pause
    exit /b 1
)
goto loop

