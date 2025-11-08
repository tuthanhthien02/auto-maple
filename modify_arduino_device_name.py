#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arduino Phase 2 Implementation - Modify Device Name and VID/PID in boards.txt
Modify boards.txt để change device name và VID/PID cho Arduino Pro Micro
"""

import os
import shutil
import re
from pathlib import Path

# Device name configuration
NEW_PRODUCT_NAME = "USB Keyboard"
NEW_MANUFACTURER_NAME = "Generic"

# VID/PID configuration (Optional - can be None to skip)
# WARNING: Only use valid, unregistered VID/PID combinations
# Example: Use generic keyboard manufacturer VID/PID
# Option 1: Logitech VID/PID (like in the image - VID_046D&PID_C31C)
NEW_VID = "0x046D"  # Logitech VID (VID_046D in the image)
NEW_PID = "0xC31C"  # Logitech Gaming Keyboard PID (PID_C31C in the image)
# Option 2: Generic keyboard VID/PID (safer - no legal issues)
# NEW_VID = "0x04D9"  # Holtek (generic keyboard)
# NEW_PID = "0x0001"  # Generic keyboard PID
# Option 3: Keep Arduino VID/PID (current - CHANGE_VID_PID = False)
# NEW_VID = "0x2341"  # Arduino LLC (default)
# NEW_PID = "0x0037"  # Arduino Micro (default)

# Set to None to skip VID/PID change (only change device name)
# CHANGE_VID_PID = False  # Disable VID/PID change (safer - only change device name)
CHANGE_VID_PID = True  # Enable VID/PID change (change vendor to Logitech VID_046D)

# Backup suffix
BACKUP_SUFFIX = ".backup_phase2"

def find_boards_txt():
    """Tìm boards.txt file"""
    possible_paths = [
        r"C:\Program Files\Arduino\hardware\arduino\avr\boards.txt",
        r"C:\Program Files (x86)\Arduino\hardware\arduino\avr\boards.txt",
        os.path.expanduser(r"~\AppData\Local\Arduino15\packages\arduino\hardware\avr"),
    ]
    
    # Find latest version
    for base_path in possible_paths:
        if os.path.isdir(base_path):
            # Check for version folders
            try:
                version_folders = [f for f in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, f)) and re.match(r'^\d+\.\d+\.\d+$', f)]
                if version_folders:
                    # Use latest version
                    latest_version = sorted(version_folders, key=lambda x: [int(i) for i in x.split('.')])[-1]
                    base_path = os.path.join(base_path, latest_version)
            except:
                pass
            
            boards_txt_path = os.path.join(base_path, "boards.txt")
            if os.path.exists(boards_txt_path):
                return base_path, boards_txt_path
        elif os.path.isfile(base_path):
            if os.path.exists(base_path):
                return os.path.dirname(base_path), base_path
    
    return None, None

def backup_file(file_path):
    """Backup file"""
    if not os.path.exists(file_path):
        return False
    
    backup_path = file_path + BACKUP_SUFFIX
    if os.path.exists(backup_path):
        print(f"[INFO] Backup already exists: {backup_path}")
        return True
    
    try:
        shutil.copy2(file_path, backup_path)
        print(f"[✓] Backed up: {file_path} → {backup_path}")
        return True
    except Exception as e:
        print(f"[✗] Failed to backup {file_path}: {e}")
        return False

def modify_boards_txt(boards_txt_path, change_vid_pid=False):
    """Modify boards.txt to change device name and optionally VID/PID for Pro Micro"""
    if not os.path.exists(boards_txt_path):
        print(f"[✗] File not found: {boards_txt_path}")
        return False
    
    # Backup file
    if not backup_file(boards_txt_path):
        return False
    
    try:
        # Read file
        with open(boards_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        original_content = content
        modifications = []
        
        # Modify Pro Micro USB product name
        # Pattern: pro.menu.usb.0.product=Arduino Micro
        content_before = content
        content = re.sub(
            r'(pro\.menu\.usb\.\d+\.product=)([^\n]*)',
            rf'\1{NEW_PRODUCT_NAME}',
            content,
            flags=re.IGNORECASE
        )
        if content != content_before:
            modifications.append("Product Name")
        
        # Modify Pro Micro USB manufacturer name
        # Pattern: pro.menu.usb.0.manufacturer=Arduino LLC
        content_before = content
        content = re.sub(
            r'(pro\.menu\.usb\.\d+\.manufacturer=)([^\n]*)',
            rf'\1{NEW_MANUFACTURER_NAME}',
            content,
            flags=re.IGNORECASE
        )
        if content != content_before:
            modifications.append("Manufacturer Name")
        
        # Modify VID/PID if enabled
        if change_vid_pid and NEW_VID and NEW_PID:
            # Pattern: pro.vid.0=0x2341
            content_before = content
            content = re.sub(
                r'(pro\.vid\.\d+=)(0x[0-9A-Fa-f]+)',
                rf'\1{NEW_VID}',
                content,
                flags=re.IGNORECASE
            )
            if content != content_before:
                modifications.append(f"VID ({NEW_VID})")
            
            # Pattern: pro.pid.0=0x0037
            content_before = content
            content = re.sub(
                r'(pro\.pid\.\d+=)(0x[0-9A-Fa-f]+)',
                rf'\1{NEW_PID}',
                content,
                flags=re.IGNORECASE
            )
            if content != content_before:
                modifications.append(f"PID ({NEW_PID})")
        
        # Also modify any USB_PRODUCT or USB_MANUFACTURER definitions
        content_before = content
        content = re.sub(
            r'(USB_PRODUCT\s*=\s*")([^"]*)(")',
            rf'\1{NEW_PRODUCT_NAME}\3',
            content,
            flags=re.IGNORECASE
        )
        if content != content_before:
            modifications.append("USB_PRODUCT")
        
        content_before = content
        content = re.sub(
            r'(USB_MANUFACTURER\s*=\s*")([^"]*)(")',
            rf'\1{NEW_MANUFACTURER_NAME}\3',
            content,
            flags=re.IGNORECASE
        )
        if content != content_before:
            modifications.append("USB_MANUFACTURER")
        
        # Check if modified
        if content == original_content:
            print("[INFO] No changes needed - file may already be modified")
            # Show relevant lines
            lines = content.split('\n')
            print("\n[INFO] Current Pro Micro settings:")
            for i, line in enumerate(lines):
                if 'pro' in line.lower() and any(keyword in line.lower() for keyword in ['product', 'manufacturer', 'vid', 'pid']):
                    print(f"   Line {i+1}: {line.strip()}")
            return True
        
        # Write file
        with open(boards_txt_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"[✓] Modified: {boards_txt_path}")
        print(f"   Modifications: {', '.join(modifications)}")
        if change_vid_pid:
            print(f"   Product Name: {NEW_PRODUCT_NAME}")
            print(f"   Manufacturer: {NEW_MANUFACTURER_NAME}")
            print(f"   VID: {NEW_VID}")
            print(f"   PID: {NEW_PID}")
        else:
            print(f"   Product Name: {NEW_PRODUCT_NAME}")
            print(f"   Manufacturer: {NEW_MANUFACTURER_NAME}")
            print(f"   VID/PID: Not changed (disabled)")
        
        # Show modified lines
        lines = content.split('\n')
        print("\n[INFO] Modified lines:")
        for i, line in enumerate(lines):
            if 'pro' in line.lower() and any(keyword in line.lower() for keyword in [NEW_PRODUCT_NAME.lower(), NEW_MANUFACTURER_NAME.lower(), NEW_VID.lower() if change_vid_pid else '', NEW_PID.lower() if change_vid_pid else '']):
                print(f"   Line {i+1}: {line.strip()}")
        
        return True
        
    except Exception as e:
        print(f"[✗] Failed to modify {boards_txt_path}: {e}")
        import traceback
        traceback.print_exc()
        return False

def verify_modification(boards_txt_path, change_vid_pid=False):
    """Verify modification"""
    if not os.path.exists(boards_txt_path):
        return False
    
    try:
        with open(boards_txt_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Check if modified (flexible matching)
        has_product = NEW_PRODUCT_NAME in content
        has_manufacturer = NEW_MANUFACTURER_NAME in content
        
        # Check Pro Micro specific patterns
        pro_product_pattern = re.search(r'pro\.menu\.usb\.\d+\.product=' + re.escape(NEW_PRODUCT_NAME), content, re.IGNORECASE)
        pro_manufacturer_pattern = re.search(r'pro\.menu\.usb\.\d+\.manufacturer=' + re.escape(NEW_MANUFACTURER_NAME), content, re.IGNORECASE)
        
        result = (has_product and has_manufacturer) or (pro_product_pattern and pro_manufacturer_pattern)
        
        # Check VID/PID if enabled
        if change_vid_pid and NEW_VID and NEW_PID:
            has_vid = NEW_VID in content
            has_pid = NEW_PID in content
            pro_vid_pattern = re.search(r'pro\.vid\.\d+=' + re.escape(NEW_VID), content, re.IGNORECASE)
            pro_pid_pattern = re.search(r'pro\.pid\.\d+=' + re.escape(NEW_PID), content, re.IGNORECASE)
            result = result and ((has_vid and has_pid) or (pro_vid_pattern and pro_pid_pattern))
            if not result:
                print(f"[DEBUG] VID/PID verification:")
                print(f"   Has VID '{NEW_VID}': {has_vid}")
                print(f"   Has PID '{NEW_PID}': {has_pid}")
                print(f"   Pro VID pattern: {bool(pro_vid_pattern)}")
                print(f"   Pro PID pattern: {bool(pro_pid_pattern)}")
        
        if not result:
            print(f"[DEBUG] Verification details:")
            print(f"   Has product '{NEW_PRODUCT_NAME}': {has_product}")
            print(f"   Has manufacturer '{NEW_MANUFACTURER_NAME}': {has_manufacturer}")
            print(f"   Pro product pattern: {bool(pro_product_pattern)}")
            print(f"   Pro manufacturer pattern: {bool(pro_manufacturer_pattern)}")
        
        return result
        
    except Exception as e:
        print(f"[✗] Failed to verify: {e}")
        return False

def main():
    """Main function"""
    print("=" * 70)
    print("Arduino Phase 2 Implementation - Modify Device Name and VID/PID")
    print("=" * 70)
    print()
    
    # Check if VID/PID change is enabled
    if CHANGE_VID_PID:
        print("[INFO] VID/PID change: ENABLED")
        print(f"   New VID: {NEW_VID}")
        print(f"   New PID: {NEW_PID}")
        print()
        print("⚠️  WARNING: Changing VID/PID may cause driver issues!")
        print("⚠️  Only use valid, unregistered VID/PID combinations!")
        print()
    else:
        print("[INFO] VID/PID change: DISABLED (only changing device name)")
        print("   To enable VID/PID change, set CHANGE_VID_PID = True in script")
        print()
    
    # Find boards.txt
    print("[1/4] Finding boards.txt...")
    base_path, boards_txt_path = find_boards_txt()
    
    if not boards_txt_path:
        print("[✗] boards.txt not found!")
        print()
        print("Please install Arduino IDE or specify path manually.")
        print()
        print("Possible locations:")
        print("  - C:\\Program Files\\Arduino\\hardware\\arduino\\avr\\boards.txt")
        print("  - C:\\Users\\<YOUR_USER>\\AppData\\Local\\Arduino15\\packages\\arduino\\hardware\\avr\\<VERSION>\\boards.txt")
        return False
    
    print(f"[✓] Found boards.txt:")
    print(f"   Base path: {base_path}")
    print(f"   boards.txt: {boards_txt_path}")
    print()
    
    # Backup file
    print("[2/4] Backing up boards.txt...")
    if not backup_file(boards_txt_path):
        print("[✗] Failed to backup file!")
        return False
    print()
    
    # Modify file
    print("[3/4] Modifying boards.txt...")
    if not modify_boards_txt(boards_txt_path, change_vid_pid=CHANGE_VID_PID):
        print("[✗] Failed to modify file!")
        return False
    print()
    
    # Verify modification
    print("[4/4] Verifying modification...")
    if verify_modification(boards_txt_path, change_vid_pid=CHANGE_VID_PID):
        print("[✓] Modification verified!")
        print()
    else:
        print("[⚠️] Verification unclear - please check manually")
        print()
    
    # Instructions
    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print()
    print("1. Open Arduino IDE")
    print("2. File → Open: arduino_hid_keyboard\\arduino_hid_keyboard.ino")
    print("3. Tools → Board: Arduino Leonardo (Pro Micro uses Leonardo bootloader)")
    print("4. Tools → Port: COM13")
    print("5. Tools → USB Configuration: USB Keyboard (if available)")
    print("6. Sketch → Upload")
    print()
    print("7. Verify device name and VID/PID:")
    print("   - Device Manager → Keyboards")
    print("   - Should see 'USB Keyboard' (not 'Arduino Micro')")
    print("   - Check VID/PID in device properties")
    print("   - Or run: python check_arduino_device_name.py")
    print()
    print("=" * 70)
    print("IMPORTANT NOTES")
    print("=" * 70)
    print()
    print("⚠️  boards.txt will be restored when Arduino IDE updates")
    print("⚠️  You may need to run this script again after Arduino IDE updates")
    if CHANGE_VID_PID:
        print("⚠️  VID/PID change may cause driver issues - test carefully!")
        print("⚠️  Only use valid, unregistered VID/PID combinations!")
    print()
    print("✅ Backup saved at: " + boards_txt_path + BACKUP_SUFFIX)
    print()
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        if success:
            print("[✓] Phase 2 setup complete!")
        else:
            print("[✗] Phase 2 setup failed!")
            exit(1)
    except KeyboardInterrupt:
        print("\n\n[!] Interrupted by user.")
        exit(1)
    except Exception as e:
        print(f"\n[✗] Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
