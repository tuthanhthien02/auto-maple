#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stop VMware Script - Auto stop VMware services and processes
No pause, runs automatically
"""

import subprocess
import sys
import os

def stop_vmware_service(service_name):
    """Stop a VMware service"""
    try:
        result = subprocess.run(['net', 'stop', service_name], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print(f"[OK] {service_name} stopped")
            return True
        else:
            # Service might not be running
            if 'not started' in result.stdout.lower() or 'not started' in result.stderr.lower():
                print(f"[SKIP] {service_name} not running")
            else:
                print(f"[SKIP] {service_name} - {result.stdout.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {service_name} - Taking too long")
        return False
    except Exception as e:
        print(f"[ERROR] {service_name} - {e}")
        return False

def kill_vmware_process(process_name):
    """Kill a VMware process"""
    try:
        result = subprocess.run(['taskkill', '/F', '/IM', process_name], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print(f"[OK] {process_name} killed")
            return True
        else:
            # Process might not be running
            if 'not found' in result.stdout.lower() or 'not found' in result.stderr.lower():
                print(f"[SKIP] {process_name} not running")
            else:
                print(f"[SKIP] {process_name} - {result.stdout.strip()}")
            return False
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {process_name} - Taking too long")
        return False
    except Exception as e:
        print(f"[ERROR] {process_name} - {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("  Stopping VMware for MapleStory")
    print("=" * 60)
    print()
    
    # VMware services to stop
    services = [
        'VMAuthdService',
        'VMwareHostOpen',
        'VMUSBArbService',
        'VMware NAT Service'
    ]
    
    # VMware processes to kill
    processes = [
        'vmware.exe',
        'vmware-tray.exe',
        'vmware-usbarbitrator.exe',
        'vmware-hostd.exe',
        'vmware-authd.exe'
    ]
    
    print("[1/2] Stopping VMware services...")
    print()
    
    stopped_services = 0
    for service in services:
        if stop_vmware_service(service):
            stopped_services += 1
    
    print()
    print(f"[INFO] Stopped {stopped_services} service(s)")
    print()
    
    print("[2/2] Killing VMware processes...")
    print()
    
    killed_processes = 0
    for process in processes:
        if kill_vmware_process(process):
            killed_processes += 1
    
    print()
    print(f"[INFO] Killed {killed_processes} process(es)")
    print()
    
    # Check remaining VMware processes
    print("[CHECK] Checking for remaining VMware processes...")
    try:
        result = subprocess.run(['tasklist', '/FI', 'IMAGENAME eq vmware.exe', '/FO', 'LIST'], 
                              capture_output=True, text=True)
        if 'vmware.exe' in result.stdout:
            print("[WARN] Some VMware processes still running!")
            print("[WARN] You may need to close VMware Workstation manually")
        else:
            print("[OK] No VMware processes found")
    except Exception as e:
        print(f"[ERROR] Failed to check processes: {e}")
    
    print()
    print("=" * 60)
    print("  VMware Stopped Successfully!")
    print("=" * 60)
    print()
    print("[INFO] VMware services and processes have been stopped")
    print("[INFO] You can now launch MapleStory safely")
    print("[INFO] Remember to restart VMware after gaming!")
    print()

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
        sys.exit(1)

