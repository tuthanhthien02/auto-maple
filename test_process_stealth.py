"""Test script to verify Process Stealth features are working."""

import time
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from src.common.process_stealth import (
    enable_process_stealth,
    get_stealth_status,
    get_process_info,
    is_stealth_enabled,
)
from src.common.logger import get_logger

log = get_logger(__name__)


def test_stealth_features():
    """Test all Process Stealth features."""
    print("=" * 60)
    print("Process Stealth Test Script")
    print("=" * 60)
    print()

    # Test 1: Check initial status
    print("1. Initial Status:")
    print(f"   Stealth enabled: {is_stealth_enabled()}")
    print()

    # Test 2: Enable stealth
    print("2. Enabling Process Stealth...")
    try:
        enable_process_stealth()
        print("   ✓ Process Stealth enabled successfully")
    except Exception as e:
        print(f"   ✗ Failed to enable: {e}")
        return
    print()

    # Wait a moment for initialization
    time.sleep(1)

    # Test 3: Check status after enabling
    print("3. Status after enabling:")
    status = get_stealth_status()
    print(f"   Enabled: {status['enabled']}")
    print(f"   Console hidden: {status['console_hidden']}")
    print(f"   Description changed: {status['description_changed']}")
    if status["description_changed"]:
        print(f"   Original description: {status['original_description']}")
    print(f"   Memory scrambling: {status['memory_scrambling_enabled']}")
    print(f"   Fake allocations: {status['fake_allocations_count']}")
    print()

    # Test 4: Check process info
    print("4. Process Information:")
    process_info = get_process_info()
    if process_info:
        print(f"   PID: {process_info['pid']}")
        print(f"   Name: {process_info['name']}")
        print(f"   Memory: {process_info['memory_usage'] / 1024 / 1024:.2f} MB")
        print(f"   CPU: {process_info['cpu_percent']:.2f}%")
    print()

    # Test 5: Check window title (if console is visible)
    print("5. Window Title Check:")
    try:
        import ctypes
        from ctypes import wintypes

        kernel32 = ctypes.WinDLL("kernel32")
        user32 = ctypes.WinDLL("user32")

        console_window = kernel32.GetConsoleWindow()
        if console_window:
            buffer = ctypes.create_unicode_buffer(256)
            user32.GetWindowTextW.argtypes = [
                wintypes.HWND,
                wintypes.LPWSTR,
                ctypes.c_int,
            ]
            user32.GetWindowTextW.restype = ctypes.c_int
            length = user32.GetWindowTextW(console_window, buffer, 256)
            if length > 0:
                print(f"   Current window title: {buffer.value}")
            else:
                print("   Window title: (empty or console hidden)")
        else:
            print("   No console window found")
    except Exception as e:
        print(f"   Could not check window title: {e}")
    print()

    # Test 6: Monitor for a few seconds
    print("6. Monitoring (5 seconds)...")
    print("   (Check logs for memory scrambling and other activities)")
    for i in range(5):
        time.sleep(1)
        status = get_stealth_status()
        print(f"   [{i+1}s] Fake allocations: {status['fake_allocations_count']}")
    print()

    # Test 7: Final status
    print("7. Final Status:")
    status = get_stealth_status()
    print(f"   Enabled: {status['enabled']}")
    print(f"   Console hidden: {status['console_hidden']}")
    print(f"   Description changed: {status['description_changed']}")
    print(f"   Memory scrambling: {status['memory_scrambling_enabled']}")
    print(f"   Fake allocations: {status['fake_allocations_count']}")
    print()

    print("=" * 60)
    print("Test completed!")
    print("=" * 60)
    print()
    print("To disable stealth, run:")
    print("  disable_process_stealth()")
    print()
    print("Or check logs in: logs/auto_maple.log")


if __name__ == "__main__":
    test_stealth_features()
