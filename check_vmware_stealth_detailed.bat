@echo off
setlocal
REM Change to script directory
cd /d "%~dp0"

echo ========================================
echo VMware Stealth Checker - DETAILED
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Python not found. Please install Python first.
    pause
    exit /b 1
)

echo [CHECKING] All VMware services status...
echo.

REM List all VMware services
sc query state= all | findstr /I "vmware vmci vmhgfs vmmouse vmrawdsk" >nul
if %errorLevel% equ 0 (
    echo VMware Services Found:
    sc query state= all | findstr /I "vmware vmci vmhgfs vmmouse vmrawdsk"
    echo.
) else (
    echo No VMware services found with standard names.
    echo.
)

echo [CHECKING] Running processes...
echo.
tasklist | findstr /I "vmware vmtools" | findstr /V "vmware.exe vmware-vmx.exe"
echo.

echo [CHECKING] Registry keys...
echo.
reg query "HKLM\SYSTEM\CurrentControlSet\Services\vmci" >nul 2>&1
if %errorLevel% equ 0 (
    echo [FOUND] HKLM\SYSTEM\CurrentControlSet\Services\vmci
    reg query "HKLM\SYSTEM\CurrentControlSet\Services\vmci" | findstr "Start"
) else (
    echo [NOT FOUND] vmci registry key
)
echo.

echo [RUNNING] Full stealth check...
echo.
python check_vmware_stealth.py

pause

