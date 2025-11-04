@echo off
REM start_vmware_after_game.bat
REM Restart VMware services after playing MapleStory

echo ========================================
echo   Restarting VMware Services
echo ========================================
echo.

echo [1/4] Starting VMAuthdService...
net start VMAuthdService 2>nul
if %errorlevel% == 0 (
    echo [OK] VMAuthdService started
) else (
    echo [ERROR] Failed to start VMAuthdService
    echo [INFO] This is normal if VMware is not installed or service doesn't exist
)

echo.
echo [2/4] Starting VMwareHostOpen...
net start VMwareHostOpen 2>nul
if %errorlevel% == 0 (
    echo [OK] VMwareHostOpen started
) else (
    echo [ERROR] Failed to start VMwareHostOpen
    echo [INFO] This is normal if VMware is not installed or service doesn't exist
)

echo.
echo [3/4] Starting VMUSBArbService...
net start VMUSBArbService 2>nul
if %errorlevel% == 0 (
    echo [OK] VMUSBArbService started
) else (
    echo [ERROR] Failed to start VMUSBArbService
    echo [INFO] This is normal if VMware is not installed or service doesn't exist
)

echo.
echo [4/4] Starting VMware NAT Service...
net start "VMware NAT Service" 2>nul
if %errorlevel% == 0 (
    echo [OK] VMware NAT Service started
) else (
    echo [ERROR] Failed to start VMware NAT Service
    echo [INFO] This is normal if VMware is not installed or service doesn't exist
)

echo.
echo ========================================
echo   VMware Services Restarted!
echo ========================================
echo.
echo [INFO] VMware services have been restarted
echo [INFO] You can now use VMware normally
echo.
pause


