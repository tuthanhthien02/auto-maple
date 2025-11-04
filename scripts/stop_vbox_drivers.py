#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Stop VirtualBox Drivers - Stop VirtualBox drivers installed by LDPlayer
These drivers may trigger NGS detection even when LDPlayer is closed
"""

import subprocess
import sys
import os

def stop_vbox_driver(driver_name):
    """Stop a VirtualBox driver"""
    try:
        print(f"[STOP] Stopping {driver_name}...")
        result = subprocess.run(['sc', 'stop', driver_name], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"[OK] {driver_name} stopped")
            return True
        else:
            # Driver might not be running or might not exist
            if 'not found' in result.stdout.lower() or 'not found' in result.stderr.lower():
                print(f"[SKIP] {driver_name} not found")
            elif 'not started' in result.stdout.lower() or 'not started' in result.stderr.lower():
                print(f"[SKIP] {driver_name} not started")
            else:
                print(f"[SKIP] {driver_name} - {result.stdout.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {driver_name} - Taking too long")
        return False
    except Exception as e:
        print(f"[ERROR] {driver_name} - {e}")
        return False

def disable_vbox_driver(driver_name):
    """Disable a VirtualBox driver"""
    try:
        print(f"[DISABLE] Disabling {driver_name}...")
        result = subprocess.run(['sc', 'config', driver_name, 'start=', 'disabled'], 
                              capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            print(f"[OK] {driver_name} disabled")
            return True
        else:
            print(f"[SKIP] {driver_name} - {result.stdout.strip()}")
            return False
            
    except subprocess.TimeoutExpired:
        print(f"[TIMEOUT] {driver_name} - Taking too long")
        return False
    except Exception as e:
        print(f"[ERROR] {driver_name} - {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("  Stopping VirtualBox Drivers")
    print("  (Installed by LDPlayer)")
    print("=" * 60)
    print()
    
    # VirtualBox drivers to stop
    vbox_drivers = [
        'VBoxUSBMon',
        'VBoxUSB',
        'VBoxNetAdp',
        'VBoxNetFlt',
        'VBoxNetLwf',
        'VBoxDrv',
        'VBoxSF'
    ]
    
    print("[1/2] Stopping VirtualBox drivers...")
    print()
    
    stopped_count = 0
    for driver in vbox_drivers:
        if stop_vbox_driver(driver):
            stopped_count += 1
    
    print()
    print(f"[INFO] Stopped {stopped_count} driver(s)")
    print()
    
    print("[2/2] Disabling VirtualBox drivers (prevent auto-start)...")
    print()
    
    disabled_count = 0
    for driver in vbox_drivers:
        if disable_vbox_driver(driver):
            disabled_count += 1
    
    print()
    print(f"[INFO] Disabled {disabled_count} driver(s)")
    print()
    
    print("=" * 60)
    print("  VirtualBox Drivers Stopped!")
    print("=" * 60)
    print()
    print("[INFO] VirtualBox drivers have been stopped and disabled")
    print("[INFO] They will not start automatically on next boot")
    print("[INFO] You can now launch MapleStory safely")
    print()
    print("⚠️ NOTE: If you need LDPlayer again, you may need to:")
    print("  - Re-enable drivers: sc config VBoxUSBMon start= demand")
    print("  - Or restart LDPlayer (it will re-enable drivers)")
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

