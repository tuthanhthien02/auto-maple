#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check VMware Processes - Diagnostic tool for NGS detection
Lists all VMware processes and services that might trigger NGS detection
"""

import subprocess
import sys
import os

def check_vmware_processes():
    """Check for running VMware processes"""
    print("=" * 60)
    print("VMware Processes Check")
    print("=" * 60)
    print()
    
    # Common VMware process names
    vmware_processes = [
        'vmware.exe',
        'vmware-vmx.exe',
        'vmware-usbarbitrator.exe',
        'vmware-hostd.exe',
        'vmware-authd.exe',
        'vmware-tray.exe',
        'vmware-converter.exe',
        'vmware-vprobe.exe',
        'vmware-player.exe',
        'vmware-workstation.exe'
    ]
    
    print("Checking for VMware processes...")
    print()
    
    found_processes = []
    
    try:
        # Use tasklist on Windows
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        tasklist_output = result.stdout.lower()
        
        for process_name in vmware_processes:
            if process_name.lower() in tasklist_output:
                # Extract process info
                lines = result.stdout.split('\n')
                for line in lines:
                    if process_name.lower() in line.lower():
                        found_processes.append(line.strip())
                        print(f"[FOUND] {process_name}")
                        print(f"  Details: {line.strip()}")
                        print()
        
        if not found_processes:
            print("[OK] No VMware processes found running")
            print()
        else:
            print(f"[WARN] Found {len(found_processes)} VMware process(es)")
            print("[WARN] These processes may trigger NGS detection!")
            print()
            
    except Exception as e:
        print(f"[ERROR] Failed to check processes: {e}")
        print()
    
    return found_processes


def check_vmware_services():
    """Check for running VMware services"""
    print("=" * 60)
    print("VMware Services Check")
    print("=" * 60)
    print()
    
    vmware_services = [
        'VMAuthdService',
        'VMwareHostOpen',
        'VMUSBArbService',
        'VMware NAT Service',
        'VMwareUSBArbitratorService',
        'vmware-converter',
        'vmware-converter-server'
    ]
    
    print("Checking for VMware services...")
    print()
    
    found_services = []
    
    try:
        result = subprocess.run(['sc', 'query', 'type=', 'service', 'state=', 'all'], 
                               capture_output=True, text=True)
        services_output = result.stdout.lower()
        
        for service_name in vmware_services:
            if service_name.lower() in services_output:
                # Get service status
                try:
                    status_result = subprocess.run(['sc', 'query', service_name], 
                                                  capture_output=True, text=True)
                    if 'RUNNING' in status_result.stdout:
                        found_services.append(service_name)
                        print(f"[FOUND] {service_name} - RUNNING")
                        print(f"  Status: {status_result.stdout.split('STATE')[1].split('\\n')[0].strip()}")
                        print()
                except:
                    pass
        
        if not found_services:
            print("[OK] No VMware services found running")
            print()
        else:
            print(f"[WARN] Found {len(found_services)} VMware service(s) running")
            print("[WARN] These services may trigger NGS detection!")
            print()
            
    except Exception as e:
        print(f"[ERROR] Failed to check services: {e}")
        print()
    
    return found_services


def check_vmware_registry():
    """Check for VMware registry keys"""
    print("=" * 60)
    print("VMware Registry Keys Check")
    print("=" * 60)
    print()
    
    registry_keys = [
        r'HKLM\SOFTWARE\VMware, Inc.',
        r'HKLM\SYSTEM\CurrentControlSet\Services\VMAuthdService',
        r'HKLM\SYSTEM\CurrentControlSet\Services\VMwareHostOpen',
        r'HKLM\SYSTEM\CurrentControlSet\Services\VMUSBArbService'
    ]
    
    print("Checking for VMware registry keys...")
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
            print("[OK] No VMware registry keys found (or no access)")
            print()
        else:
            print(f"[WARN] Found {len(found_keys)} VMware registry key(s)")
            print("[WARN] These registry keys may trigger NGS detection!")
            print()
            
    except ImportError:
        print("[SKIP] Cannot check registry (winreg not available)")
        print()
    except Exception as e:
        print(f"[ERROR] Failed to check registry: {e}")
        print()
    
    return found_keys


def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("VMware Detection Diagnostic Tool")
    print("For NGS (Nexon Game Security) Detection Troubleshooting")
    print("=" * 60)
    print()
    
    processes = check_vmware_processes()
    services = check_vmware_services()
    registry_keys = check_vmware_registry()
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    
    total_findings = len(processes) + len(services) + len(registry_keys)
    
    if total_findings == 0:
        print("[OK] No VMware components detected!")
        print("[OK] Your system should be safe from NGS VMware detection")
    else:
        print(f"[WARN] Found {total_findings} VMware component(s) that may trigger NGS detection")
        print()
        print("Recommendations:")
        print("1. Stop VMware services before playing MapleStory")
        print("2. Close VMware Workstation before playing")
        print("3. Use 'stop_vmware_for_game.bat' script")
        print("4. Or run MapleStory on VM instead of Host")
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


