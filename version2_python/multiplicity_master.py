#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 Multiplicity Master (Python Version)
Runs on Host, mirrors input to all VMs via TCP
"""

import socket
import threading
import time
from pynput import keyboard
from colorama import Fore, init
import sys

init(autoreset=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⚙️ SETTINGS - EASY TO CUSTOMIZE!
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🌐 VM Configuration (VM Name → TCP Port)
VM_PORTS = {
    "bishop": 7001,  # VM 1
    # "VM2": 7002,   # VM 2
    # "VM3": 7003,   # VM 3
    # Add more VMs as needed
}

VM_HOST = "127.0.0.1"  # Localhost (VMs run on same PC via VMware)

# 🎯 Broadcasting Configuration
BROADCASTING_ENABLED = True  # Toggle with Ctrl+Alt+T

# 🐛 DEBUG MODE
DEBUG_MODE = True
SHOW_DEBUG_TOOLTIP = True

# 📊 PERFORMANCE MONITORING
ENABLE_PERFORMANCE_MONITOR = True

# ⌨️ KEYS TO BROADCAST (lowercase)
KEYS_TO_BROADCAST = [
    "q",
    "w",
    "e",
    "r",
    "t",
    "y",
    "u",
    "i",
    "o",
    "p",
    "a",
    "s",
    "d",
    "f",
    "g",
    "h",
    "j",
    "k",
    "l",
    "z",
    "x",
    "c",
    "v",
    "b",
    "n",
    "m",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "0",
]

# Arrow keys (special handling)
ARROW_KEYS = ["up", "down", "left", "right"]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎯 GLOBAL STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

broadcasting_enabled = BROADCASTING_ENABLED
performance_stats = {
    "total_sent": 0,
    "total_success": 0,
    "total_failed": 0,
    "avg_latency": 0,
}

pressed_keys = set()  # Track currently pressed keys

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🌐 TCP CLIENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def send_tcp_command(host, port, command, timeout=0.5):
    """Send TCP command to Slave"""
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.settimeout(timeout)

        # Connect to Slave
        client_socket.connect((host, port))

        # Send command
        client_socket.sendall(command.encode("utf-8"))

        # Small delay to ensure transmission
        time.sleep(0.01)

        client_socket.close()
        return True

    except socket.timeout:
        if DEBUG_MODE:
            print(f"{Fore.RED}✗ Timeout connecting to {host}:{port}")
        return False
    except ConnectionRefusedError:
        if DEBUG_MODE:
            print(f"{Fore.RED}✗ Connection refused: {host}:{port}")
        return False
    except Exception as e:
        if DEBUG_MODE:
            print(f"{Fore.RED}✗ Error sending to {host}:{port}: {e}")
        return False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📡 BROADCAST KEY TO ALL VMs
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def broadcast_key(key, action="KEYDOWN"):
    """Broadcast key to all VMs"""
    global performance_stats, broadcasting_enabled

    if not broadcasting_enabled:
        return

    start_time = time.time()
    success_count = 0
    fail_count = 0

    command = f"{action}:{key}"

    # Send to all VMs in parallel
    threads = []
    results = []

    def send_to_vm(vm_name, port):
        result = send_tcp_command(VM_HOST, port, command)
        results.append((vm_name, result))

    for vm_name, port in VM_PORTS.items():
        thread = threading.Thread(target=send_to_vm, args=(vm_name, port), daemon=True)
        thread.start()
        threads.append(thread)

    # Wait for all threads to complete (with timeout)
    for thread in threads:
        thread.join(timeout=1.0)

    # Count results
    for vm_name, result in results:
        if result:
            success_count += 1
        else:
            fail_count += 1

    # Update performance stats
    if ENABLE_PERFORMANCE_MONITOR:
        performance_stats["total_sent"] += 1
        performance_stats["total_success"] += success_count
        performance_stats["total_failed"] += fail_count

        latency = (time.time() - start_time) * 1000
        performance_stats["avg_latency"] = (
            performance_stats["avg_latency"] + latency
        ) / 2

    # Debug output
    if DEBUG_MODE:
        total = len(VM_PORTS)
        status = (
            f"✅ {success_count}/{total}"
            if fail_count == 0
            else f"⚠️ {success_count}/{total} (Failed: {fail_count})"
        )
        print(f"{Fore.CYAN}[MASTER] {action}: {key} → {status} ({latency:.1f}ms)")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⌨️ KEYBOARD LISTENER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def on_key_press(key):
    """Handle key press event"""
    global pressed_keys

    try:
        # Get key name
        if hasattr(key, "char") and key.char:
            key_name = key.char.lower()
        elif hasattr(key, "name"):
            key_name = key.name.lower()
        else:
            return

        # Avoid duplicate key press events
        if key_name in pressed_keys:
            return

        pressed_keys.add(key_name)

        # Check if key should be broadcasted
        if key_name in KEYS_TO_BROADCAST or key_name in ARROW_KEYS:
            # Broadcast in separate thread to not block keyboard input
            threading.Thread(
                target=broadcast_key, args=(key_name, "KEYDOWN"), daemon=True
            ).start()

    except AttributeError:
        pass


def on_key_release(key):
    """Handle key release event"""
    global pressed_keys

    try:
        # Get key name
        if hasattr(key, "char") and key.char:
            key_name = key.char.lower()
        elif hasattr(key, "name"):
            key_name = key.name.lower()
        else:
            return

        # Remove from pressed keys
        pressed_keys.discard(key_name)

        # Check if key should be broadcasted
        if key_name in KEYS_TO_BROADCAST or key_name in ARROW_KEYS:
            # Broadcast in separate thread
            threading.Thread(
                target=broadcast_key, args=(key_name, "KEYUP"), daemon=True
            ).start()

    except AttributeError:
        pass


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎛️ HOTKEYS (Ctrl+Alt+...)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ctrl_pressed = False
alt_pressed = False


def check_hotkey(key):
    """Check for hotkey combinations"""
    global broadcasting_enabled, ctrl_pressed, alt_pressed

    # Track modifier keys
    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = True
    if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        alt_pressed = True

    # Check hotkeys
    if ctrl_pressed and alt_pressed:
        if hasattr(key, "char"):
            if key.char == "t" or key.char == "T":
                # Toggle broadcasting
                broadcasting_enabled = not broadcasting_enabled
                status = "ENABLED" if broadcasting_enabled else "DISABLED"
                print(f"\n{Fore.YELLOW}[MASTER] Broadcasting {status}\n")

            elif key.char == "s" or key.char == "S":
                # Show status
                show_status()

            elif key.char == "p" or key.char == "P":
                # Show performance
                show_performance()

            elif key.char == "q" or key.char == "Q":
                # Quit
                print(f"\n{Fore.YELLOW}[MASTER] Shutting down...")
                sys.exit(0)


def on_key_release_hotkey(key):
    """Reset modifier key state on release"""
    global ctrl_pressed, alt_pressed

    if key == keyboard.Key.ctrl_l or key == keyboard.Key.ctrl_r:
        ctrl_pressed = False
    if key == keyboard.Key.alt_l or key == keyboard.Key.alt_r:
        alt_pressed = False


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 STATUS & PERFORMANCE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def show_status():
    """Show current status"""
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.GREEN}📊 MASTER STATUS")
    print(f"{Fore.CYAN}{'=' * 60}")
    print(
        f"Broadcasting: {Fore.GREEN if broadcasting_enabled else Fore.RED}{'ENABLED' if broadcasting_enabled else 'DISABLED'}"
    )
    print(f"VMs configured: {len(VM_PORTS)}")
    for vm_name, port in VM_PORTS.items():
        print(f"  • {vm_name}: {VM_HOST}:{port}")
    print(f"{Fore.CYAN}{'=' * 60}\n")


def show_performance():
    """Show performance statistics"""
    stats = performance_stats
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.GREEN}📊 PERFORMANCE STATS")
    print(f"{Fore.CYAN}{'=' * 60}")
    print(f"Total Sent: {stats['total_sent']}")
    print(f"Success: {Fore.GREEN}{stats['total_success']}")
    print(f"Failed: {Fore.RED}{stats['total_failed']}")
    print(f"Avg Latency: {stats['avg_latency']:.1f}ms")
    if stats["total_sent"] > 0:
        success_rate = (
            stats["total_success"] / (stats["total_sent"] * len(VM_PORTS))
        ) * 100
        print(f"Success Rate: {success_rate:.1f}%")
    print(f"{Fore.CYAN}{'=' * 60}\n")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def main():
    """Main entry point"""
    print(f"{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.GREEN}🎮 MULTIPLICITY MASTER (Python Version)")
    print(f"{Fore.CYAN}{'=' * 60}")
    print(f"VMs configured: {len(VM_PORTS)}")
    for vm_name, port in VM_PORTS.items():
        print(f"  • {vm_name}: {VM_HOST}:{port}")
    print(f"\n{Fore.YELLOW}Hotkeys:")
    print("  Ctrl+Alt+T - Toggle Broadcasting")
    print("  Ctrl+Alt+S - Show Status")
    print("  Ctrl+Alt+P - Show Performance")
    print("  Ctrl+Alt+Q - Quit")
    print(f"{Fore.CYAN}{'=' * 60}\n")
    print(f"{Fore.GREEN}✓ Listening for keyboard input...")
    print(f"{Fore.GREEN}✓ Press any key to broadcast to VMs\n")

    # Start keyboard listener
    with keyboard.Listener(
        on_press=lambda k: (check_hotkey(k), on_key_press(k)),
        on_release=lambda k: (on_key_release_hotkey(k), on_key_release(k)),
    ) as listener:
        listener.join()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[MASTER] Shutting down...")
        sys.exit(0)
