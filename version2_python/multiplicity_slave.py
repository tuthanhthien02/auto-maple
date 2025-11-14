#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎮 Multiplicity Slave (Python Version)
Runs in VM, receives input from Master, applies desync/jitter/remap
"""

import socket
import threading
import time
import random
import ctypes
from ctypes import wintypes
import sys
from colorama import Fore, init

init(autoreset=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ⚙️ SETTINGS - EASY TO CUSTOMIZE!
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 🌐 TCP Server Port (Each VM uses different port!)
TCP_PORT = 7001  # VM1: 7001, VM2: 7002, VM3: 7003, ...
TCP_HOST = "0.0.0.0"  # Listen on all interfaces

# 1️⃣ DESYNC DELAY (Anti-detection timing randomization)
# IMPORTANT: Each VM should use DIFFERENT ranges!
# VM1: (0, 300), VM2: (100, 400), VM3: (200, 500), etc.
DESYNC_MIN = 0  # milliseconds
DESYNC_MAX = 500  # milliseconds
DISABLE_DESYNC = False  # Set to True to disable desync

# 2️⃣ ARROW KEYS JITTER (Movement smoothness)
ARROW_KEYS_USE_JITTER = True
JITTER_MIN = 5  # milliseconds
JITTER_MAX = 15  # milliseconds
USE_GAUSSIAN = True  # More human-like (bell curve distribution)

# 3️⃣ BEHAVIORAL PAUSE (Auto pause like human)
ENABLE_AUTO_PAUSE = True
PAUSE_INTERVAL_MIN = 20 * 60 * 1000  # 20 minutes (in ms)
PAUSE_INTERVAL_MAX = 60 * 60 * 1000  # 60 minutes (in ms)
PAUSE_DURATION_MIN = 1 * 60 * 1000  # 1 minute (in ms)
PAUSE_DURATION_MAX = 5 * 60 * 1000  # 5 minutes (in ms)

# 4️⃣ KEY REMAP (Game-specific key mapping)
# Master sends Q → Slave remaps to A and sends to game
KEY_REMAP = {
    "q": "a",
    "w": "w",
    "e": "e",
    "r": "r",
    "a": "a",
    "s": "s",
    "d": "d",
    "f": "f",
    # Arrow keys
    "up": "up",
    "down": "down",
    "left": "left",
    "right": "right",
    # Add more mappings as needed
}

# 🐛 DEBUG MODE
DEBUG_MODE = True
ENABLE_PERFORMANCE_MONITOR = True

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎹 WINDOWS VIRTUAL KEY CODES
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

VK_CODES = {
    # Letters
    "a": 0x41,
    "b": 0x42,
    "c": 0x43,
    "d": 0x44,
    "e": 0x45,
    "f": 0x46,
    "g": 0x47,
    "h": 0x48,
    "i": 0x49,
    "j": 0x4A,
    "k": 0x4B,
    "l": 0x4C,
    "m": 0x4D,
    "n": 0x4E,
    "o": 0x4F,
    "p": 0x50,
    "q": 0x51,
    "r": 0x52,
    "s": 0x53,
    "t": 0x54,
    "u": 0x55,
    "v": 0x56,
    "w": 0x57,
    "x": 0x58,
    "y": 0x59,
    "z": 0x5A,
    # Numbers
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
    # Arrow keys
    "up": 0x26,
    "down": 0x28,
    "left": 0x25,
    "right": 0x27,
    # Function keys
    "f1": 0x70,
    "f2": 0x71,
    "f3": 0x72,
    "f4": 0x73,
    "space": 0x20,
    "enter": 0x0D,
    "shift": 0x10,
    "ctrl": 0x11,
    "alt": 0x12,
    "tab": 0x09,
    "esc": 0x1B,
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎯 GLOBAL STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

script_enabled = True
is_paused = False
performance_stats = {
    "total_keypresses": 0,
    "avg_latency": 0,
    "total_desync_time": 0,
    "total_jitter_time": 0,
}

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔧 WINDOWS SendInput API (Low-level, undetectable!)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# Define structures
class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(wintypes.ULONG)),
    ]


class INPUT(ctypes.Structure):
    class _INPUT(ctypes.Union):
        _fields_ = [("ki", KEYBDINPUT)]

    _anonymous_ = ("_input",)
    _fields_ = [("type", wintypes.DWORD), ("_input", _INPUT)]


# Constants
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002


def send_key(vk_code, key_up=False):
    """Send key using Windows SendInput API (most undetectable method!)"""
    extra = ctypes.c_ulong(0)
    ii_ = INPUT()
    ii_.type = INPUT_KEYBOARD
    ii_.ki = KEYBDINPUT(
        wVk=vk_code,
        wScan=0,
        dwFlags=KEYEVENTF_KEYUP if key_up else 0,
        time=0,
        dwExtraInfo=ctypes.pointer(extra),
    )
    ctypes.windll.user32.SendInput(1, ctypes.byref(ii_), ctypes.sizeof(ii_))


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🎲 RANDOMIZATION HELPERS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def get_desync_delay():
    """Get random desync delay in milliseconds"""
    if DISABLE_DESYNC:
        return 0
    return random.uniform(DESYNC_MIN, DESYNC_MAX)


def get_jitter_delay():
    """Get random jitter delay in milliseconds"""
    if USE_GAUSSIAN:
        mean = (JITTER_MIN + JITTER_MAX) / 2
        std_dev = (JITTER_MAX - JITTER_MIN) / 6  # 99.7% within range
        delay = random.gauss(mean, std_dev)
        return max(JITTER_MIN, min(JITTER_MAX, delay))
    else:
        return random.uniform(JITTER_MIN, JITTER_MAX)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔽 PROCESS KEY DOWN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def process_key_down(key):
    """Process KEYDOWN command from Master"""
    global performance_stats, is_paused

    if not script_enabled or is_paused:
        return

    start_time = time.time()

    # Get target key from remap
    target_key = KEY_REMAP.get(key.lower(), key.lower())

    if DEBUG_MODE:
        print(f"{Fore.CYAN}[SLAVE] Key: {key} → {target_key}")

    # Apply desync delay
    desync = get_desync_delay()
    if desync > 0:
        time.sleep(desync / 1000.0)
        if ENABLE_PERFORMANCE_MONITOR:
            performance_stats["total_desync_time"] += desync

    # Apply jitter for arrow keys
    arrow_keys = ["up", "down", "left", "right"]
    if ARROW_KEYS_USE_JITTER and target_key in arrow_keys:
        jitter = get_jitter_delay()
        time.sleep(jitter / 1000.0)
        if ENABLE_PERFORMANCE_MONITOR:
            performance_stats["total_jitter_time"] += jitter

    # Send key down
    vk_code = VK_CODES.get(target_key)
    if vk_code:
        send_key(vk_code, key_up=False)

        if ENABLE_PERFORMANCE_MONITOR:
            performance_stats["total_keypresses"] += 1
            latency = (time.time() - start_time) * 1000
            performance_stats["avg_latency"] = (
                performance_stats["avg_latency"] + latency
            ) / 2

            if DEBUG_MODE:
                print(
                    f"{Fore.GREEN}✓ Sent {target_key} DOWN (latency: {latency:.1f}ms)"
                )
    else:
        print(f"{Fore.RED}✗ Unknown key: {target_key}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔼 PROCESS KEY UP
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def process_key_up(key):
    """Process KEYUP command from Master"""
    if not script_enabled or is_paused:
        return

    target_key = KEY_REMAP.get(key.lower(), key.lower())
    vk_code = VK_CODES.get(target_key)

    if vk_code:
        send_key(vk_code, key_up=True)
        if DEBUG_MODE:
            print(f"{Fore.GREEN}✓ Sent {target_key} UP")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🔌 TCP SERVER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def handle_client(client_socket, addr):
    """Handle incoming TCP connection from Master"""
    try:
        # Set socket timeout
        client_socket.settimeout(1.0)

        # Receive command
        data = client_socket.recv(1024).decode("utf-8").strip()

        if not data:
            return

        if DEBUG_MODE:
            print(f"{Fore.YELLOW}[SLAVE] Received: {data}")

        # Parse command: "KEYDOWN:q" or "KEYUP:q"
        parts = data.split(":", 1)
        if len(parts) != 2:
            return

        action, key = parts

        if action == "KEYDOWN":
            process_key_down(key)
        elif action == "KEYUP":
            process_key_up(key)
        else:
            print(f"{Fore.RED}✗ Unknown action: {action}")

    except socket.timeout:
        print(f"{Fore.RED}✗ Socket timeout")
    except Exception as e:
        print(f"{Fore.RED}✗ Error handling client: {e}")
    finally:
        client_socket.close()


def tcp_server():
    """TCP server - listens for commands from Master"""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((TCP_HOST, TCP_PORT))
        server_socket.listen(5)
        print(f"{Fore.GREEN}[SLAVE] TCP Server running on {TCP_HOST}:{TCP_PORT}")
        print(f"{Fore.CYAN}Waiting for Master commands...")

        while script_enabled:
            try:
                client_socket, addr = server_socket.accept()
                # Handle in separate thread for non-blocking
                threading.Thread(
                    target=handle_client, args=(client_socket, addr), daemon=True
                ).start()
            except KeyboardInterrupt:
                break

    except Exception as e:
        print(f"{Fore.RED}✗ Failed to start TCP server: {e}")
        sys.exit(1)
    finally:
        server_socket.close()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🤖 BEHAVIORAL PAUSE (Auto pause like human)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def schedule_pause():
    """Schedule next auto pause"""
    if not ENABLE_AUTO_PAUSE:
        return

    interval = random.uniform(PAUSE_INTERVAL_MIN, PAUSE_INTERVAL_MAX) / 1000.0
    threading.Timer(interval, start_pause).start()


def start_pause():
    """Start behavioral pause"""
    global is_paused
    is_paused = True
    duration = random.uniform(PAUSE_DURATION_MIN, PAUSE_DURATION_MAX) / 1000.0

    print(f"{Fore.YELLOW}[PAUSE] Auto pause for {duration / 60:.1f} minutes")

    threading.Timer(duration, end_pause).start()


def end_pause():
    """End behavioral pause"""
    global is_paused
    is_paused = False
    print(f"{Fore.GREEN}[RESUME] Pause ended")
    schedule_pause()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 📊 PERFORMANCE MONITOR
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def show_performance_stats():
    """Display performance statistics"""
    if not ENABLE_PERFORMANCE_MONITOR:
        return

    stats = performance_stats
    print(f"\n{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.GREEN}📊 PERFORMANCE STATS")
    print(f"{Fore.CYAN}{'=' * 60}")
    print(f"Total Keypresses: {stats['total_keypresses']}")
    print(f"Avg Latency: {stats['avg_latency']:.1f}ms")
    print(f"Total Desync Time: {stats['total_desync_time']:.0f}ms")
    print(f"Total Jitter Time: {stats['total_jitter_time']:.0f}ms")
    print(f"{Fore.CYAN}{'=' * 60}\n")

    # Schedule next display
    threading.Timer(60, show_performance_stats).start()


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# 🚀 MAIN
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


def main():
    """Main entry point"""
    print(f"{Fore.CYAN}{'=' * 60}")
    print(f"{Fore.GREEN}🎮 MULTIPLICITY SLAVE (Python Version)")
    print(f"{Fore.CYAN}{'=' * 60}")
    print(f"TCP Port: {TCP_PORT}")
    print(f"Desync Range: {DESYNC_MIN}-{DESYNC_MAX}ms")
    print(f"Jitter Range: {JITTER_MIN}-{JITTER_MAX}ms")
    print(f"Auto Pause: {'Enabled' if ENABLE_AUTO_PAUSE else 'Disabled'}")
    print(f"{Fore.CYAN}{'=' * 60}\n")

    # Start behavioral pause scheduler
    if ENABLE_AUTO_PAUSE:
        schedule_pause()

    # Start performance monitor
    if ENABLE_PERFORMANCE_MONITOR:
        threading.Timer(60, show_performance_stats).start()

    # Start TCP server (blocking)
    tcp_server()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}[SLAVE] Shutting down...")
        script_enabled = False
        sys.exit(0)
