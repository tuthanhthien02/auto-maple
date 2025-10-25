@echo off
echo ========================================
echo MULTIPLICITY PRIMARY PC SETUP
echo ========================================
echo.
echo INSTRUCTIONS:
echo 1. Download Multiplicity from: https://www.stardock.com/products/multiplicity/
echo 2. Run the installer
echo 3. Enter your license key
echo 4. Choose "PRIMARY COMPUTER"
echo 5. Complete installation
echo.
echo After installation, this script will help you configure it.
echo.
pause

echo.
echo ========================================
echo GETTING YOUR IP ADDRESS
echo ========================================
echo.
echo Your Primary PC IP address is:
ipconfig | findstr /i "IPv4"
echo.
echo IMPORTANT: Note down the IPv4 Address above!
echo Example: 192.168.1.100
echo.
set /p PRIMARY_IP="Enter your Primary PC IP address: "

echo.
echo ========================================
echo CONFIGURATION STEPS
echo ========================================
echo.
echo 1. Launch Multiplicity
echo 2. Go to Settings ^> Network
echo 3. Enable "Allow other computers to connect"
echo 4. Your IP is: %PRIMARY_IP%
echo.
echo 5. Go to Settings ^> Broadcast
echo 6. Enable "Broadcast keyboard input to all computers"
echo 7. Enable "Broadcast mouse clicks to all computers"
echo 8. Toggle broadcast hotkey: Ctrl+Shift+B
echo.
echo Press any key when configuration is complete...
pause

echo.
echo ========================================
echo FIREWALL CONFIGURATION
echo ========================================
echo.
echo Adding firewall exception for Multiplicity...

netsh advfirewall firewall add rule name="Multiplicity Server" dir=in action=allow program="C:\Program Files\Multiplicity\Multiplicity.exe" enable=yes

if %errorlevel%==0 (
    echo SUCCESS: Firewall rule added!
) else (
    echo WARNING: Failed to add firewall rule. You may need to run this as Administrator.
    echo Manual fix: Control Panel ^> Firewall ^> Allow app ^> Add Multiplicity
)

echo.
echo ========================================
echo PRIMARY PC SETUP COMPLETE!
echo ========================================
echo.
echo Next steps:
echo 1. Keep Multiplicity running on this PC
echo 2. Setup Client PCs using setup_multiplicity_client.bat
echo 3. Connect clients to IP: %PRIMARY_IP%
echo.
echo Save this IP for client setup: %PRIMARY_IP%
echo.

echo %PRIMARY_IP% > multiplicity_primary_ip.txt
echo IP saved to: multiplicity_primary_ip.txt
echo.

pause



