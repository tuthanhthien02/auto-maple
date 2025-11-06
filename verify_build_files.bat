@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Script để verify files cần thiết cho build trên VM
REM Chạy script này TRƯỚC KHI build để đảm bảo tất cả files đều có

echo ========================================
echo    VERIFY BUILD FILES
echo    Check files cần thiết cho build
echo ========================================
echo.

REM Change to script directory
cd /d "%~dp0"

echo [~] Current directory: %CD%
echo.

REM Required files for build
set MISSING_FILES=0

echo [~] Checking required files...
echo.

REM Check ExplorerSettings.spec
if exist "ExplorerSettings.spec" (
    echo [✓] ExplorerSettings.spec - FOUND
) else (
    echo [X] ExplorerSettings.spec - NOT FOUND
    set /a MISSING_FILES+=1
)

REM Check main.py
if exist "main.py" (
    echo [✓] main.py - FOUND
) else (
    echo [X] main.py - NOT FOUND
    set /a MISSING_FILES+=1
)

REM Check build_stealth.bat
if exist "build_stealth.bat" (
    echo [✓] build_stealth.bat - FOUND
) else (
    echo [X] build_stealth.bat - NOT FOUND
    set /a MISSING_FILES+=1
)

REM Check folders
echo.
echo [~] Checking required folders...
echo.

if exist "assets" (
    echo [✓] assets\ - FOUND
) else (
    echo [X] assets\ - NOT FOUND
    set /a MISSING_FILES+=1
)

if exist "resources" (
    echo [✓] resources\ - FOUND
) else (
    echo [X] resources\ - NOT FOUND
    set /a MISSING_FILES+=1
)

if exist "src" (
    echo [✓] src\ - FOUND
) else (
    echo [X] src\ - NOT FOUND
    set /a MISSING_FILES+=1
)

REM Check icon file
if exist "assets\explorer-icon.ico" (
    echo [✓] assets\explorer-icon.ico - FOUND
) else (
    echo [!] assets\explorer-icon.ico - NOT FOUND (optional, but recommended)
)

echo.
echo ========================================

if !MISSING_FILES! EQU 0 (
    echo    ✅ ALL FILES FOUND
    echo ========================================
    echo.
    echo [✓] All required files are present
    echo [✓] Ready to build!
    echo.
    echo Next step: Run build_stealth.bat
    echo.
) else (
    echo    ⚠️  MISSING FILES
    echo ========================================
    echo.
    echo [!] Found !MISSING_FILES! missing file(s)
    echo.
    echo Please copy missing files from Host to VM:
    echo.
    echo Option 1: Copy entire project folder
    echo Option 2: Copy only missing files
    echo.
    echo See: VMWARE_FILE_TRANSFER_GUIDE.md
    echo.
)

pause

