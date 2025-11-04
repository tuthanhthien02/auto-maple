#!/usr/bin/bin/env python3
# -*- coding: utf-8 -*-
"""
Check LDPlayer Detection - Diagnostic tool for NGS detection
LDPlayer có thể trigger NGS detection khi chạy với admin rights
"""

import subprocess
import sys
import os

def check_ldplayer_processes():
    """Check for running LDPlayer processes"""
    print("=" * 60)
    print("LDPlayer Processes Check")
    print("=" * 60)
    print()
    
    # Common LDPlayer process names
    ldplayer_processes = [
        'LdVBoxHeadless.exe',
        'LdVBoxSVC.exe',
        'LdVBoxSDS.exe',
        'dnplayer.exe',
        'dnplayerconsole.exe',
        'dnservice.exe',
        'LdVBoxHeadless.exe',
        'LdVBoxSVC.exe',
        'LdVBoxSDS.exe',
        'LDPlayer.exe',
        'LDMultiPlayer.exe',
        'LDMultiPlayerConsole.exe',
        'LDMonitor.exe',
        'LDTool.exe',
        'LDUpdater.exe',
        'LDBox.exe'
    ]
    
    print("Checking for LDPlayer processes...")
    print()
    
    found_processes = []
    
    try:
        # Use tasklist on Windows
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        tasklist_output = result.stdout.lower()
        
        for process_name in ldplayer_processes:
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
            print("[OK] No LDPlayer processes found running")
            print()
        else:
            print(f"[WARN] Found {len(found_processes)} LDPlayer process(es)")
            print("[WARN] LDPlayer processes may trigger NGS detection!")
            print("[WARN] Especially when running with admin rights!")
            print()
            
    except Exception as e:
        print(f"[ERROR] Failed to check processes: {e}")
        print()
    
    return found_processes


def check_ldplayer_services():
    """Check for running LDPlayer services"""
    print("=" * 60)
    print("LDPlayer Services Check")
    print("=" * 60)
    print()
    
    ldplayer_services = [
        'LdVBoxSVC',
        'LdVBoxSDS',
        'LDPlayerService',
        'dnservice',
        'LDPlayerService',
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
                        found_services.append(service_name)
                        print(f"[FOUND] {service_name} - RUNNING")
                        print(f"  Status: {status_result.stdout.split('STATE')[1].split('\\n')[0].strip()}")
                        print()
                except:
                    pass
        
        if not found_services:
            print("[OK] No LDPlayer services found running")
            print()
        else:
            print(f"[WARN] Found {len(found_services)} LDPlayer service(s) running")
            print("[WARN] LDPlayer services may trigger NGS detection!")
            print()
            
    except Exception as e:
        print(f"[ERROR] Failed to check services: {e}")
        print()
    
    return found_services


def check_virtualbox_processes():
    """Check for VirtualBox processes (LDPlayer uses VirtualBox)"""
    print("=" * 60)
    print("VirtualBox Processes Check (LDPlayer uses VirtualBox)")
    print("=" * 60)
    print()
    
    vbox_processes = [
        'VBoxHeadless.exe',
        'VBoxSVC.exe',
        'VBoxSDS.exe',
        'VBoxNetDHCP.exe',
        'VBoxNetNAT.exe',
        'VirtualBox.exe'
    ]
    
    print("Checking for VirtualBox processes...")
    print()
    
    found_processes = []
    
    try:
        result = subprocess.run(['tasklist'], capture_output=True, text=True)
        tasklist_output = result.stdout.lower()
        
        for process_name in vbox_processes:
            if process_name.lower() in tasklist_output:
                lines = result.stdout.split('\n')
                for line in lines:
                    if process_name.lower() in line.lower():
                        found_processes.append(line.strip())
                        print(f"[FOUND] {process_name}")
                        print(f"  Details: {line.strip()}")
                        print()
        
        if not found_processes:
            print("[OK] No VirtualBox processes found running")
            print()
        else:
            print(f"[WARN] Found {len(found_processes)} VirtualBox process(es)")
            print("[WARN] VirtualBox processes may trigger NGS detection!")
            print("[WARN] LDPlayer uses VirtualBox internally!")
            print()
            
    except Exception as e:
        print(f"[ERROR] Failed to check processes: {e}")
        print()
    
    return found_processes


def check_admin_processes():
    """Check for processes running with admin rights"""
    print("=" * 60)
    print("Processes Running with Admin Rights")
    print("=" * 60)
    print()
    
    print("Checking for elevated processes...")
    print()
    
    try:
        # Use wmic to check elevated processes
        result = subprocess.run(['wmic', 'process', 'where', 'executablepath!=""', 'get', 
                               'name,executablepath,processid', '/format:list'], 
                              capture_output=True, text=True, timeout=10)
        
        # Check for LDPlayer processes
        ldplayer_keywords = ['ldplayer', 'ldvbox', 'dnplayer', 'virtualbox']
        elevated_processes = []
        
        lines = result.stdout.split('\n')
        current_process = {}
        for line in lines:
            line = line.strip()
            if line.startswith('Name='):
                current_process['name'] = line.split('=', 1)[1]
            elif line.startswith('ExecutablePath='):
                current_process['path'] = line.split('=', 1)[1]
            elif line.startswith('ProcessId='):
                current_process['pid'] = line.split('=', 1)[1]
                
                # Check if it's LDPlayer or VirtualBox related
                name_lower = current_process.get('name', '').lower()
                path_lower = current_process.get('path', '').lower()
                
                for keyword in ldplayer_keywords:
                    if keyword in name_lower or keyword in path_lower:
                        elevated_processes.append(current_process.copy())
                        print(f"[FOUND] {current_process.get('name', 'Unknown')} (PID: {current_process.get('pid', 'Unknown')})")
                        print(f"  Path: {current_process.get('path', 'Unknown')}")
                        print()
                current_process = {}
        
        if not elevated_processes:
            print("[OK] No LDPlayer/VirtualBox processes found with elevated rights")
            print()
        else:
            print(f"[WARN] Found {len(elevated_processes)} LDPlayer/VirtualBox process(es)")
            print("[WARN] Running with admin rights may trigger NGS detection!")
            print()
            
    except subprocess.TimeoutExpired:
        print("[TIMEOUT] Process check took too long, skipping...")
        print()
    except Exception as e:
        print(f"[ERROR] Failed to check elevated processes: {e}")
        print("[INFO] May need admin rights to check")
        print()
    
    return []


def main():
    """Main function"""
    print("\n" + "=" * 60)
    print("LDPlayer Detection Diagnostic Tool")
    print("For NGS (Nexon Game Security) Detection Troubleshooting")
    print("=" * 60)
    print()
    print("[INFO] LDPlayer chạy với admin rights có thể trigger NGS detection!")
    print("[INFO] LDPlayer sử dụng VirtualBox internally - cũng có thể bị detect!")
    print()
    
    ldplayer_processes = check_ldplayer_processes()
    ldplayer_services = check_ldplayer_services()
    vbox_processes = check_virtualbox_processes()
    check_admin_processes()
    
    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)
    print()
    
    total_findings = len(ldplayer_processes) + len(ldplayer_services) + len(vbox_processes)
    
    if total_findings == 0:
        print("[OK] No LDPlayer/VirtualBox components detected!")
        print("[OK] Your system should be safe from LDPlayer-related NGS detection")
    else:
        print(f"[WARN] Found {total_findings} LDPlayer/VirtualBox component(s) that may trigger NGS detection")
        print()
        print("⚠️ CRITICAL FINDINGS:")
        print("  - LDPlayer uses VirtualBox internally")
        print("  - Running LDPlayer with admin rights increases detection risk")
        print("  - NGS may detect LDPlayer/VirtualBox processes")
        print()
        print("Recommendations:")
        print("1. Stop LDPlayer before playing MapleStory")
        print("2. Do NOT run LDPlayer with admin rights when playing game")
        print("3. Stop LDPlayer services: LdVBoxSVC, LdVBoxSDS")
        print("4. Use 'stop_ldplayer_for_game.bat' script")
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

