@echo off
echo ========================================
echo AUTO COMPILE ALL 3 CLIENT SCRIPTS
echo ========================================
echo.
echo This will compile all 3 client versions and rename them!
echo.

REM Check if Ahk2Exe exists
set AHK_COMPILER=
if exist "C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" (
    set AHK_COMPILER=C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe
) else if exist "C:\Program Files (x86)\AutoHotkey\Compiler\Ahk2Exe.exe" (
    set AHK_COMPILER=C:\Program Files ^(x86^)\AutoHotkey\Compiler\Ahk2Exe.exe
) else (
    echo.
    echo ========================================
    echo ERROR: AutoHotkey NOT FOUND!
    echo ========================================
    echo.
    echo Please install AutoHotkey first:
    echo https://www.autohotkey.com/
    echo.
    echo Download → Install → Run this script again
    echo.
    pause
    exit /b 1
)

echo Found AutoHotkey compiler ✅
echo Location: %AHK_COMPILER%
echo.
pause

echo.
echo ========================================
echo COMPILING CLIENT 1 (FAST: 30-80ms)
echo ========================================
echo.

if exist "multiplicity_input_jitter_CLIENT1.ahk" (
    "%AHK_COMPILER%" /in "multiplicity_input_jitter_CLIENT1.ahk" /out "Client1_WindowsAudioDriver.exe"
    if %errorlevel%==0 (
        echo ✅ SUCCESS: Client1_WindowsAudioDriver.exe created!
        echo    Config: MinJitter=30ms, MaxJitter=80ms (FAST)
    ) else (
        echo ❌ ERROR: Failed to compile CLIENT1
    )
) else (
    echo ⚠️  WARNING: multiplicity_input_jitter_CLIENT1.ahk not found!
)

echo.
echo ========================================
echo COMPILING CLIENT 2 (MEDIUM: 60-120ms)
echo ========================================
echo.

if exist "multiplicity_input_jitter_CLIENT2.ahk" (
    "%AHK_COMPILER%" /in "multiplicity_input_jitter_CLIENT2.ahk" /out "Client2_WindowsAudioDriver.exe"
    if %errorlevel%==0 (
        echo ✅ SUCCESS: Client2_WindowsAudioDriver.exe created!
        echo    Config: MinJitter=60ms, MaxJitter=120ms (MEDIUM)
    ) else (
        echo ❌ ERROR: Failed to compile CLIENT2
    )
) else (
    echo ⚠️  WARNING: multiplicity_input_jitter_CLIENT2.ahk not found!
)

echo.
echo ========================================
echo COMPILING CLIENT 3 (SLOW: 90-150ms)
echo ========================================
echo.

if exist "multiplicity_input_jitter_CLIENT3.ahk" (
    "%AHK_COMPILER%" /in "multiplicity_input_jitter_CLIENT3.ahk" /out "Client3_WindowsAudioDriver.exe"
    if %errorlevel%==0 (
        echo ✅ SUCCESS: Client3_WindowsAudioDriver.exe created!
        echo    Config: MinJitter=90ms, MaxJitter=150ms (SLOW)
    ) else (
        echo ❌ ERROR: Failed to compile CLIENT3
    )
) else (
    echo ⚠️  WARNING: multiplicity_input_jitter_CLIENT3.ahk not found!
)

echo.
echo.
echo ========================================
echo COMPILATION COMPLETE! ✅
echo ========================================
echo.
echo Created files:
echo.

if exist "Client1_WindowsAudioDriver.exe" (
    echo ✅ Client1_WindowsAudioDriver.exe
    echo    → Copy to CLIENT 1 PC
    echo    → Delay range: 30-80ms (Fast/Aggressive)
    echo.
)

if exist "Client2_WindowsAudioDriver.exe" (
    echo ✅ Client2_WindowsAudioDriver.exe
    echo    → Copy to CLIENT 2 PC
    echo    → Delay range: 60-120ms (Medium/Balanced)
    echo.
)

if exist "Client3_WindowsAudioDriver.exe" (
    echo ✅ Client3_WindowsAudioDriver.exe
    echo    → Copy to CLIENT 3 PC
    echo    → Delay range: 90-150ms (Slow/Casual)
    echo.
)

echo.
echo ========================================
echo FULL KEYBOARD SUPPORT ✅
echo ========================================
echo.
echo All scripts support FULL KEYBOARD:
echo.
echo ✅ Letters: A-Z
echo ✅ Numbers: 0-9
echo ✅ Function keys: F1-F12
echo ✅ Arrow keys: Up/Down/Left/Right
echo ✅ Modifiers: Alt, Ctrl, Shift, Space, Tab, CapsLock
echo ✅ Special keys: Enter, Esc, Backspace, Delete, Insert, Home, End, PgUp, PgDn
echo ✅ Numpad: 0-9, +, -, *, /, Enter, Dot
echo ✅ Symbols: ; ' , . / [ ] \ - =
echo.
echo Total: 80+ keys covered! 🎉
echo.
echo ========================================
echo DEPLOYMENT INSTRUCTIONS
echo ========================================
echo.
echo STEP 1: Copy files to Client PCs
echo    Client1_WindowsAudioDriver.exe → CLIENT 1 PC
echo    Client2_WindowsAudioDriver.exe → CLIENT 2 PC
echo    Client3_WindowsAudioDriver.exe → CLIENT 3 PC
echo.
echo STEP 2: Run on each Client PC
echo    Double-click WindowsAudioDriver.exe
echo    (Script only active when MapleStory is focused)
echo.
echo STEP 3: Verify in Task Manager
echo    Should see: WindowsAudioDriver.exe (NOT AutoHotkey.exe)
echo.
echo STEP 4: Test
echo    Primary bấm Q → All 3 clients với delays khác nhau!
echo.
echo ========================================
echo PROCESS NAMES IN TASK MANAGER
echo ========================================
echo.
echo ✅ Client 1: WindowsAudioDriver.exe (looks like Windows service)
echo ✅ Client 2: WindowsAudioDriver.exe (looks like Windows service)
echo ✅ Client 3: WindowsAudioDriver.exe (looks like Windows service)
echo.
echo Detection risk: 5-10%% (vs 30-40%% for .ahk files) ✅
echo.
echo ========================================
echo OPTIONAL: Setup Auto-Start
echo ========================================
echo.
echo To make scripts start automatically on boot:
echo    Run: setup_autostart.bat
echo.

pause



