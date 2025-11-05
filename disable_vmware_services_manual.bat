@echo off
setlocal
REM Change to script directory
cd /d "%~dp0"

echo ========================================
echo VMware Services - Manual Disable Guide
echo ========================================
echo.
echo This script will help you disable VMware services manually.
echo.

REM Check admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run as Administrator!
    echo.
    echo Right-click and select "Run as administrator"
    pause
    exit /b 1
)

echo [STEP 1] Listing all VMware-related services...
echo.
sc query state= all | findstr /I /C:"SERVICE_NAME" | findstr /I "vmware vmci vmhgfs vmmouse vmrawdsk vm3dservice"
echo.

echo [STEP 2] Disabling VMware services...
echo.

REM Try to disable all possible VMware service names
for %%S in (
    "VMTools"
    "VMware Tools"
    "vmci"
    "VMCI"
    "VMUSBArbService"
    "VMware USB Arbitration Service"
    "VMwareHostOpen"
    "VMware Host Open Service"
    "VMwareAuthorizationService"
    "VMware Authorization Service"
    "VMware NAT Service"
    "VmwareAutostartService"
    "VMware Autostart Service"
    "vmhgfs"
    "VMHGFS"
    "vmmouse"
    "VMMouse"
    "vmrawdsk"
    "VMRawDisk"
    "vm3dservice"
    "VM3DService"
) do (
    echo Trying: %%S
    sc config %%S start= disabled >nul 2>&1
    if %errorLevel% equ 0 (
        echo   [OK] Disabled: %%S
        sc stop %%S >nul 2>&1
    ) else (
        echo   [SKIP] Service not found: %%S
    )
)

echo.
echo [STEP 3] Stopping all running VMware services...
echo.
for %%S in (
    "VMTools"
    "vmci"
    "VMUSBArbService"
    "VMwareHostOpen"
    "VMwareAuthorizationService"
    "VMware NAT Service"
    "VmwareAutostartService"
    "vmhgfs"
    "vmmouse"
    "vmrawdsk"
    "vm3dservice"
) do (
    sc stop %%S >nul 2>&1
    if %errorLevel% equ 0 (
        echo   [OK] Stopped: %%S
    )
)

echo.
echo [STEP 4] Final status check...
echo.
sc query state= all | findstr /I /C:"SERVICE_NAME" | findstr /I "vmware vmci vmhgfs vmmouse vmrawdsk vm3dservice"
echo.

echo ========================================
echo Done! Please restart VM and run check_vmware_stealth.bat again.
echo ========================================
echo.
pause

