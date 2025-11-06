@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM Script để copy file build vào VMware Shared Folder
REM Yêu cầu: VMware Shared Folders đã được setup

echo ========================================
echo    COPY BUILD TO VMWARE SHARED FOLDER
echo ========================================
echo.

REM Check if dist folder exists
if not exist "dist\ExplorerSettings.exe" (
    echo [X] ERROR: File build not found!
    echo     Expected: dist\ExplorerSettings.exe
    echo.
    echo Please compile bot first:
    echo   pyinstaller ExplorerSettings.spec
    echo   OR
    echo   build_stealth.bat
    echo.
    pause
    exit /b 1
)

echo [~] Found build file: dist\ExplorerSettings.exe
echo.

REM Check VMware Shared Folder path
set "SHARED_FOLDER=\\vmware-host\Shared Folders\auto-maple-build"

echo [~] Checking VMware Shared Folder...
echo     Path: %SHARED_FOLDER%
echo.

REM Test if shared folder exists
if not exist "%SHARED_FOLDER%\" (
    echo [!] WARNING: Shared folder not found!
    echo.
    echo Please setup VMware Shared Folders:
    echo   1. VM -^> Settings -^> Options -^> Shared Folders
    echo   2. Enable "Always enabled"
    echo   3. Add folder: dist (or auto-maple-build)
    echo   4. Set share name: auto-maple-build
    echo.
    echo Or use alternative methods:
    echo   - Network Share (SMB)
    echo   - USB Passthrough
    echo   - Cloud Storage
    echo.
    echo See: VMWARE_FILE_TRANSFER_GUIDE.md
    echo.
    pause
    exit /b 1
)

echo [✓] Shared folder found!
echo.

REM Copy file
echo [~] Copying file to shared folder...
copy /Y "dist\ExplorerSettings.exe" "%SHARED_FOLDER%\ExplorerSettings.exe"

if errorlevel 1 (
    echo [X] ERROR: Failed to copy file!
    echo.
    echo Possible causes:
    echo   - Shared folder not accessible
    echo   - Permission denied
    echo   - Network issue
    echo.
    pause
    exit /b 1
)

echo [✓] File copied successfully!
echo.

REM Verify
if exist "%SHARED_FOLDER%\ExplorerSettings.exe" (
    echo [✓] Verification: File exists in shared folder
    echo.
    echo ========================================
    echo    ✅ SUCCESS
    echo ========================================
    echo.
    echo File location in VM:
    echo   \\vmware-host\Shared Folders\auto-maple-build\ExplorerSettings.exe
    echo.
    echo Next steps:
    echo   1. Open VM
    echo   2. Access shared folder
    echo   3. Copy ExplorerSettings.exe to Desktop (or desired location)
    echo   4. Run ExplorerSettings.exe in VM
    echo.
) else (
    echo [X] ERROR: File not found in shared folder after copy!
    echo.
)

pause

