#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Arduino Device Name
Verify device name after Phase 2 implementation
"""

import sys
import ctypes
from ctypes import wintypes

def check_arduino_device_name():
    """Check Arduino device name"""
    print("=" * 70)
    print("Arduino Device Name Check")
    print("=" * 70)
    print()
    
    try:
        # Load Windows API
        user32 = ctypes.windll.user32
        
        # Constants
        RID_INPUT = 0x10000003
        RID_HEADER = 0x10000005
        
        RIM_TYPEKEYBOARD = 1
        RIDI_DEVICENAME = 0x20000007
        
        # Get Raw Input devices
        device_count = wintypes.UINT(0)
        result = user32.GetRawInputDeviceList(None, ctypes.byref(device_count), ctypes.sizeof(wintypes.HANDLE * 2))
        
        if device_count.value == 0:
            print("[✗] No Raw Input devices found!")
            return False
        
        # Allocate buffer
        class RAWINPUTDEVICELIST(ctypes.Structure):
            _fields_ = [
                ("hDevice", wintypes.HANDLE),
                ("dwType", wintypes.DWORD)
            ]
        
        device_buffer = (RAWINPUTDEVICELIST * device_count.value)()
        result = user32.GetRawInputDeviceList(device_buffer, ctypes.byref(device_count), ctypes.sizeof(RAWINPUTDEVICELIST))
        
        if result == -1:
            print("[✗] Failed to get Raw Input device list!")
            return False
        
        # Check each device
        arduino_devices = []
        keyboard_devices = []
        
        for i in range(device_count.value):
            device = device_buffer[i]
            if device.dwType == RIM_TYPEKEYBOARD:
                # Get device name
                name_size = wintypes.UINT(0)
                user32.GetRawInputDeviceInfoW(
                    device.hDevice,
                    RIDI_DEVICENAME,
                    None,
                    ctypes.byref(name_size)
                )
                
                if name_size.value > 0:
                    name_buffer = ctypes.create_unicode_buffer(name_size.value)
                    result = user32.GetRawInputDeviceInfoW(
                        device.hDevice,
                        RIDI_DEVICENAME,
                        name_buffer,
                        ctypes.byref(name_size)
                    )
                    
                    if result > 0:
                        device_name = name_buffer.value if name_buffer.value else ""
                        keyboard_devices.append({
                            'handle': device.hDevice,
                            'name': device_name
                        })
                        
                        # Check if Arduino device
                        device_name_lower = device_name.lower()
                        if any(keyword in device_name_lower for keyword in ['arduino', 'micro', 'leonardo']):
                            arduino_devices.append({
                                'handle': device.hDevice,
                                'name': device_name
                            })
        
        # Print results
        print(f"[INFO] Found {len(keyboard_devices)} keyboard device(s)")
        print()
        
        if arduino_devices:
            print("[⚠️] Arduino devices detected:")
            print()
            for device in arduino_devices:
                print(f"   Handle: 0x{device['handle']:016X}")
                print(f"   Name: {device['name']}")
                print()
            print("[✗] Phase 2 NOT applied - Device name still contains 'Arduino'")
            print()
            print("Please:")
            print("1. Run modify_arduino_device_name.py")
            print("2. Upload firmware to COM13")
            print("3. Check device name again")
            return False
        else:
            print("[✓] No Arduino devices detected!")
            print()
            print("All keyboard devices:")
            for device in keyboard_devices:
                print(f"   - {device['name']}")
            print()
            print("[✓] Phase 2 applied successfully - No 'Arduino' in device names")
            return True
        
    except Exception as e:
        print(f"[✗] Error: {e}")
        return False

def main():
    """Main function"""
    success = check_arduino_device_name()
    
    if success:
        print("=" * 70)
        print("RESULT: Phase 2 Applied Successfully")
        print("=" * 70)
        return 0
    else:
        print("=" * 70)
        print("RESULT: Phase 2 Not Applied")
        print("=" * 70)
        return 1

if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[✗] Error: {e}")
        sys.exit(1)

