@echo off
setlocal
REM Change to script directory
cd /d "%~dp0"

echo ========================================
echo VMware Stealth Fix Script
echo ========================================
echo.
echo [WARNING] This script requires Administrator privileges!
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

echo [1/5] Stopping VMware processes...
REM Only kill VM processes, not Host VMware Workstation processes
taskkill /F /IM vmwaretools.exe >nul 2>&1
taskkill /F /IM vmtoolsd.exe >nul 2>&1
taskkill /F /IM vmwaretray.exe >nul 2>&1
taskkill /F /IM vmwareuser.exe >nul 2>&1
taskkill /F /IM vmwareauthd.exe >nul 2>&1
echo Done.
echo.
echo [NOTE] Skipping vmware.exe and vmware-vmx.exe (these are Host processes, not VM processes)

echo.
echo [2/5] Disabling VMware services...
sc config "VMTools" start= disabled >nul 2>&1
sc stop "VMTools" >nul 2>&1

sc config "VMUSBArbService" start= disabled >nul 2>&1
sc stop "VMUSBArbService" >nul 2>&1

sc config "VMwareHostOpen" start= disabled >nul 2>&1
sc stop "VMwareHostOpen" >nul 2>&1

sc config "vmci" start= disabled >nul 2>&1
sc stop "vmci" >nul 2>&1

sc config "VMwareAuthorizationService" start= disabled >nul 2>&1
sc stop "VMwareAuthorizationService" >nul 2>&1

sc config "VMware NAT Service" start= disabled >nul 2>&1
sc stop "VMware NAT Service" >nul 2>&1

REM Disable VMware Autostart Service
sc config "VmwareAutostartService" start= disabled >nul 2>&1
sc stop "VmwareAutostartService" >nul 2>&1

echo Done.

echo.
echo [3/5] Checking if services were disabled...
echo.

REM Check all VMware services
for %%S in (
    "VMTools"
    "vmci"
    "VMUSBArbService"
    "VMwareHostOpen"
    "VMwareAuthorizationService"
    "VMware NAT Service"
    "VmwareAutostartService"
) do (
    echo Checking: %%S
    sc query %%S 2>nul | findstr "STATE" >nul
    if %errorLevel% equ 0 (
        sc query %%S | findstr "STOPPED" >nul
        if %errorLevel% equ 0 (
            echo   [OK] %%S stopped
        ) else (
            sc query %%S | findstr "RUNNING" >nul
            if %errorLevel% equ 0 (
                echo   [WARNING] %%S still RUNNING - trying to stop again...
                sc stop %%S >nul 2>&1
                timeout /t 1 >nul
            ) else (
                echo   [INFO] %%S not found or in different state
            )
        )
    ) else (
        echo   [INFO] %%S not found
    )
    echo.
)

echo.
echo [4/5] Waiting 2 seconds...
timeout /t 2 >nul

echo.
echo [5/5] Running stealth check...
echo.
python check_vmware_stealth.py

echo.
echo ========================================
echo Fix completed!
echo ========================================
echo.
echo [IMPORTANT] 
echo   1. Restart VM to apply all changes
echo   2. Check RawInputViewer for hardware traces
echo   3. Use Arduino HID Keyboard for best stealth
echo.
pause

