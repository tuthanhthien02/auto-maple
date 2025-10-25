@echo off
echo ========================================
echo MULTIPLICITY CLIENT PC SETUP
echo ========================================
echo.
echo INSTRUCTIONS:
echo 1. Download Multiplicity from: https://www.stardock.com/products/multiplicity/
echo 2. Run the installer
echo 3. Enter SAME license key as Primary PC
echo 4. Choose "SECONDARY COMPUTER"
echo 5. Complete installation
echo.
echo After installation, this script will help you connect.
echo.
pause

echo.
echo ========================================
echo CONNECTING TO PRIMARY PC
echo ========================================
echo.
set /p PRIMARY_IP="Enter Primary PC IP address (e.g., 192.168.1.100): "

echo.
echo Configuration steps:
echo 1. Launch Multiplicity
echo 2. Go to Settings ^> Network
echo 3. Click "Connect to Primary Computer"
echo 4. Enter IP: %PRIMARY_IP%
echo 5. Click "Connect"
echo.
echo You should see: "Connected to [Primary PC Name]"
echo Status indicator should be GREEN
echo.
echo Press any key when connected...
pause

echo.
echo ========================================
echo TESTING CONNECTION
echo ========================================
echo.
ping %PRIMARY_IP% -n 4

if %errorlevel%==0 (
    echo SUCCESS: Can ping Primary PC!
) else (
    echo WARNING: Cannot ping Primary PC. Check network connection.
)

echo.
echo ========================================
echo CLIENT PC SETUP COMPLETE!
echo ========================================
echo.
echo Verification:
echo - Multiplicity status: Should show "Connected"
echo - Primary IP: %PRIMARY_IP%
echo.
echo Repeat this setup on other client PCs!
echo.

pause



