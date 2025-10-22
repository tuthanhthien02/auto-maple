@echo off
REM ============================================================
REM TAO DESKTOP SHORTCUT (Khong can pywin32)
REM ============================================================
echo.
echo ============================================================
echo TAO DESKTOP SHORTCUT CHO AUTO MAPLE
echo ============================================================
echo.

REM Lay duong dan hien tai
set "CURRENT_DIR=%~dp0"
set "CURRENT_DIR=%CURRENT_DIR:~0,-1%"

REM Tao VBScript de tao shortcut
set "VBS_FILE=%TEMP%\create_shortcut.vbs"

echo Set oWS = WScript.CreateObject("WScript.Shell") > "%VBS_FILE%"
echo sLinkFile = oWS.SpecialFolders("Desktop") ^& "\Auto Maple.lnk" >> "%VBS_FILE%"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%VBS_FILE%"
echo oLink.TargetPath = "cmd.exe" >> "%VBS_FILE%"
echo oLink.Arguments = "/k cd /d ""%CURRENT_DIR%"" && conda activate automaple && python main.py" >> "%VBS_FILE%"
echo oLink.WorkingDirectory = "%CURRENT_DIR%" >> "%VBS_FILE%"
echo oLink.IconLocation = "%CURRENT_DIR%\assets\icon.ico" >> "%VBS_FILE%"
echo oLink.Description = "Auto Maple Bot - Luminous" >> "%VBS_FILE%"
echo oLink.Save >> "%VBS_FILE%"

REM Chay VBScript
cscript //nologo "%VBS_FILE%"

REM Xoa VBScript tam
del "%VBS_FILE%"

echo.
echo ============================================================
echo THANH CONG!
echo ============================================================
echo.
echo Da tao shortcut "Auto Maple" tren Desktop
echo.
echo Luu y: Shortcut se:
echo 1. Kich hoat conda environment "automaple"
echo 2. Chay python main.py
echo 3. Giu cua so mo sau khi bot tat
echo.
pause

