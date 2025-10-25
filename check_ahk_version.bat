@echo off
echo ═══════════════════════════════════════════════════════
echo CHECKING AUTOHOTKEY INSTALLATION
echo ═══════════════════════════════════════════════════════
echo.

echo [1] Checking if AutoHotkey is installed...
where autohotkey.exe >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ AutoHotkey found!
    echo.
    echo [2] Location:
    where autohotkey.exe
    echo.
) else (
    echo ❌ AutoHotkey NOT found in PATH!
    echo.
    echo This might be normal. Checking registry...
    echo.
)

echo [3] Checking version...
echo.

REM Try to get version from registry
reg query "HKEY_LOCAL_MACHINE\SOFTWARE\AutoHotkey" /v Version 2>nul
if %errorlevel% equ 0 (
    echo.
    echo ✅ Found in registry!
) else (
    reg query "HKEY_CURRENT_USER\SOFTWARE\AutoHotkey" /v Version 2>nul
    if %errorlevel% equ 0 (
        echo.
        echo ✅ Found in user registry!
    ) else (
        echo ❌ Not found in registry!
    )
)

echo.
echo ═══════════════════════════════════════════════════════
echo.
echo If AutoHotkey is installed, you should see version above.
echo.
echo Expected: Version 1.1.x.x ✅
echo Wrong:    Version 2.x.x ❌ (need to install v1.1 instead)
echo.
echo ═══════════════════════════════════════════════════════
echo.
pause

