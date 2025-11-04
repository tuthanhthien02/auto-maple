#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check LDPlayer Traces - Check for leftover traces after LDPlayer was closed
LDPlayer có thể để lại services, registry keys, drivers sau khi đóng
"""

import subprocess
import sys
import os

def check_ldplayer_services():
    """Check for LDPlayer services (even if not running)"""
    print("=" * 60)
    print("LDPlayer Services Check (Including Stopped)")
    print("=" * 60)
    print()
    
    ldplayer_services = [
        'LdVBoxSVC',
        'LdVBoxSDS',
        'LDPlayerService',
        'dnservice',
        'LDBoxService'
    ]
    
    print("Checking for LDPlayer services...")
    print()
    
    found_services = []
    
    try:
        result = subprocess.run(['sc', 'query', 'type=', 'service', 'state=', 'all'], 
                               capture_output=True, text=True)
        services_output = result.stdout.lower()
        
        for service_name in ldplayer_services:
            if service_name.lower() in services_output:
                # Get service status
                try:
                    status_result = subprocess.run(['sc', 'query', service_name], 
                                                  capture_output=True, text=True)
                    if 'RUNNING' in status_result.stdout:
                        status = "RUNNING"
                    elif 'STOPPED' in status_result.stdout:
                        status = "STOPPED"
                    else:
                        status = "UNKNOWN"
                    
                    found_services.append({'name': service_name, 'status': status})
                    print(f"[FOUND] {service_name} - {status}")
                    
                    # Extract display name
                    if 'DISPLAY_NAME' in status_result.stdout:
                        for line in status_result.stdout.split('\n'):
                            if 'DISPLAY_NAME' in line:
                                print(f"  {line.strip()}")
                    print()
                except:
                    pass
        
        if not found_services:
            print("[OK] No LDPlayer services found")
            print()
        else:
            print(f"[WARN] Found {len(found_services)} LDPlayer service(s)")
            print("[WARN] Even STOPPED services may trigger NGS detection!")
            print()
            
    except Exception as e:
        print(f"[ERROR] Failed to check services: {e}")
        print()
    
    return found_services


def check_ldplayer_registry():
    """Check for LDPlayer registry keys"""
    print("=" * 60)
    print("LDPlayer Registry Keys Check")
    print("=" * 60)
    print()
    
    registry_keys = [
        r'HKLM\SOFTWARE\LDPlayer',
        r'HKLM\SOFTWARE\WOW6432Node\LDPlayer',
        r'HKLM\SYSTEM\CurrentControlSet\Services\LdVBoxSVC',
        r'HKLM\SYSTEM\CurrentControlSet\Services\LdVBoxSDS',
        r'HKLM\SOFTWARE\VirtualBox',
        r'HKLM\SOFTWARE\WOW6432Node\VirtualBox'
    ]
    
    print("Checking for LDPlayer/VirtualBox registry keys...")
    print()
    
    found_keys = []
    
    try:
        import winreg
        
        for key_path in registry_keys:
            try:
                # Parse registry path
                if key_path.startswith('HKLM\\'):
                    key_path_clean = key_path.replace('HKLM\\', '')
                    hkey = winreg.HKEY_LOCAL_MACHINE
                    
                    # Try to open key
                    try:
                        key = winreg.OpenKey(hkey, key_path_clean)
                        winreg.CloseKey(key)
                        found_keys.append(key_path)
                        print(f"[FOUND] {key_path}")
                    except FileNotFoundError:
                        pass
                    except Exception as e:
                        print(f"[INFO] {key_path} - Check failed: {e}")
            except Exception as e:
                print(f"[ERROR] Failed to check {key_path}: {e}")
        
        if not found_keys:
            print("[OK] No LDPlayer/VirtualBox registry keys found")
            print()
        else:
            print(f"[WARN] Found {len(found_keys)} LDPlayer/VirtualBox registry key(s)")
            print("[WARN] Registry keys may trigger NGS detection!")
            print()
            
    except ImportError:
        print("[SKIP] Cannot check registry (winreg not available)")
        print()
    except Exception as e:
        print(f"[ERROR] Failed to check registry: {e}")
        print()
    
    return found_keys


def check_virtualbox_drivers():
    """Check for VirtualBox drivers (LDPlayer uses VirtualBox)"""
    print("=" * 60)
    print("VirtualBox Drivers Check")
    print("=" * 60)
    print()
    
    vbox_drivers = [
        'VBoxUSBMon',
        'VBoxUSB',
        'VBoxNetAdp',
        'VBoxNetFlt',
        'VBoxNetLwf',
        'VBoxDrv',
        'VBoxSF'
    ]
    
    print("Checking for VirtualBox drivers...")
    print()
    
    found_drivers = []
    
    try:
        result = subprocess.run(['sc', 'query', 'type=', 'driver'], 
                               capture_output=True, text=True)
        drivers_output = result.stdout.lower()
        
        for driver_name in vbox_drivers:
            if driver_name.lower() in drivers_output:
                try:
                    status_result = subprocess.run(['sc', 'query', driver_name], 
                                                  capture_output=True, text=True)
                    if 'RUNNING' in status_result.stdout:
                        status = "RUNNING"
                    elif 'STOPPED' in status_result.stdout:
                        status = "STOPPED"
                    else:
                        status = "UNKNOWN"
                    
                    found_drivers.append({'name': driver_name, 'status': status})
                    print(f"[FOUND] {driver_name} - {status}")
                    
                    # Extract display name
                    if 'DISPLAY_NAME' in status_result.stdout:
                        for line in status_result.stdout.split('\n'):
                            if 'DISPLAY_NAME' in line:
                                print(f"  {line.strip()}")
                    print()
                except:
                    pass
        
        if not found_drivers:
            print("[OK] No VirtualBox drivers found")
            print()
        else:
            print(f"[WARN] Found {len(found_drivers)} VirtualBox driver(s)")
            print("[WARN] Drivers may trigger NGS detection!")
            print()
            
    except Exception as e:
        print(f"[ERROR] Failed to check drivers: {e}")
        print()
    
    return found_drivers


def check_process_combo():
    """Check for VMware + LDPlayer combination"""
    print("=" * 60)
    print("VMware + LDPlayer Combination Check")
    print("=" * 60)
    print()
    
    vmware_found = False
    ldplayer_found = False
    
    try:
        # Check VMware
        vmware_result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq vmware.exe'], 
                                      capture_output=True, text=True)
        if 'vmware.exe' in vmware_result.stdout:
            vmware_found = True
        
        # Check VMware services
        vmware_services = ['VMAuthdService', 'VMUSBArbService']
        for service in vmware_services:
            try:
                result = subprocess.run(['sc', 'query', service], 
                                       capture_output=True, text=True)
                if 'RUNNING' in result.stdout:
                    vmware_found = True
                    break
            except:
                pass
        
        # Check LDPlayer traces
        ldplayer_services = check_ldplayer_services()
        if ldplayer_services:
            ldplayer_found = True
        
        print(f"[INFO] VMware detected: {vmware_found}")
        print(f"[INFO] LDPlayer traces detected: {ldplayer_found}")
        print()
        
        if vmware_found and ldplayer_found:
            print("[CRITICAL] ⚠️ BOTH VMware AND LDPlayer traces found!")
            print("[CRITICAL] Combination may trigger NGS detection!")
            print("[CRITICAL] NGS may have flagged your system!")
            print()
        elif vmware_found:
            print("[WARN] Only VMware detected")
            print("[WARN] VMware alone may trigger NGS detection")
            print()
        elif ldplayer_found:
            print("[WARN] Only LDPlayer traces detected")
            print("[WARN] LDPlayer traces may trigger NGS detection")
            print()
        else:
            print("[OK] No VMware or LDPlayer detected")
            print()
            
    except Exception as e:
        print(f"[ERROR] Failed to check combination: {e}")
        print()
    
    return vmware_found, ldplayer_found


def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("LDPlayer Traces Detection Tool")
    print("Check for leftover traces after LDPlayer was closed")
    print("=" * 60)
    print()
    
    ldplayer_services = check_ldplayer_services()
    ldplayer_registry = check_ldplayer_registry()
    vbox_drivers = check_virtualbox_drivers()
    vmware_found, ldplayer_found = check_process_combo()
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    
    total_traces = len(ldplayer_services) + len(ldplayer_registry) + len(vbox_drivers)
    
    print(f"[INFO] LDPlayer Services: {len(ldplayer_services)}")
    print(f"[INFO] LDPlayer Registry Keys: {len(ldplayer_registry)}")
    print(f"[INFO] VirtualBox Drivers: {len(vbox_drivers)}")
    print(f"[INFO] Total Traces: {total_traces}")
    print()
    
    if total_traces == 0 and not vmware_found:
        print("[OK] No LDPlayer/VirtualBox traces found!")
        print("[OK] System should be clean")
    elif total_traces > 0:
        print(f"[WARN] Found {total_traces} LDPlayer/VirtualBox trace(s)")
        print()
        print("⚠️ CRITICAL:")
        print("  - LDPlayer traces REMAIN after closing LDPlayer")
        print("  - These traces may trigger NGS detection")
        print("  - Combination với VMware increases detection risk")
        print()
        print("Recommendations:")
        print("1. Disable LDPlayer services (even if stopped)")
        print("2. Clean LDPlayer registry keys (if possible)")
        print("3. Stop VMware before playing game")
        print("4. Or run game on VM instead of Host")
        print()
    elif vmware_found:
        print("[WARN] VMware detected (but no LDPlayer traces)")
        print("[WARN] VMware alone may trigger NGS detection")
        print()
        print("Recommendations:")
        print("1. Stop VMware services before playing game")
        print("2. Use 'stop_vmware_for_game.bat' script")
        print("3. Or run game on VM instead of Host")
        print()
    
    print()
    input("Press Enter to exit...")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Exiting...")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        input("\nPress Enter to exit...")

