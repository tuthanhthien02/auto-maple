@echo off
REM stop_vmware_for_game.bat
REM Stop VMware services and processes before playing MapleStory

echo ========================================
echo   Stopping VMware for MapleStory
echo ========================================
echo.

echo [1/6] Stopping VMAuthdService...
net stop VMAuthdService 2>nul
if %errorlevel% == 0 (
    echo [OK] VMAuthdService stopped
) else (
    echo [SKIP] VMAuthdService not running or already stopped
)

echo.
echo [2/6] Stopping VMwareHostOpen...
net stop VMwareHostOpen 2>nul
if %errorlevel% == 0 (
    echo [OK] VMwareHostOpen stopped
) else (
    echo [SKIP] VMwareHostOpen not running or already stopped
)

echo.
echo [3/6] Stopping VMUSBArbService...
net stop VMUSBArbService 2>nul
if %errorlevel% == 0 (
    echo [OK] VMUSBArbService stopped
) else (
    echo [SKIP] VMUSBArbService not running or already stopped
)

echo.
echo [4/6] Stopping VMware NAT Service...
net stop "VMware NAT Service" 2>nul
if %errorlevel% == 0 (
    echo [OK] VMware NAT Service stopped
) else (
    echo [SKIP] VMware NAT Service not running or already stopped
)

echo.
echo [5/6] Killing VMware processes...
taskkill /F /IM vmware.exe 2>nul
taskkill /F /IM vmware-tray.exe 2>nul
taskkill /F /IM vmware-usbarbitrator.exe 2>nul
taskkill /F /IM vmware-hostd.exe 2>nul
taskkill /F /IM vmware-authd.exe 2>nul
echo [OK] VMware processes killed

echo.
echo [6/6] Checking remaining VMware processes...
set vmware_found=0
for /f "tokens=1" %%i in ('tasklist /FI "IMAGENAME eq vmware.exe" /FO LIST ^| find "vmware.exe"') do (
    set vmware_found=1
)
if %vmware_found% == 1 (
    echo [WARN] Some VMware processes still running!
    echo [WARN] You may need to close VMware Workstation manually
) else (
    echo [OK] No VMware processes found
)

echo.
echo ========================================
echo   VMware Stopped Successfully!
echo ========================================
echo.
echo [INFO] VMware services and processes have been stopped
echo [INFO] You can now launch MapleStory safely
echo [INFO] Remember to restart VMware after gaming!
echo.
pause


