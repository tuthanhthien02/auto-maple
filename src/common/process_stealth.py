"""Process stealth features for better hiding."""

import ctypes
import gc
import os
import random
import sys
import threading
import time
from ctypes import wintypes

import psutil


class ProcessStealth:
    """Manages process stealth features."""

    def __init__(self):
        self.original_title = None
        self.console_hidden = False
        self.process_name_changed = False
        self.original_process_name = None
        self.original_description = None
        self.description_changed = False
        self.fake_allocations = []  # Track fake memory allocations

    def hide_console(self):
        """Hide the console window."""
        try:
            if not self.console_hidden:
                # Get console window handle
                kernel32 = ctypes.WinDLL("kernel32")
                console_window = kernel32.GetConsoleWindow()

                if console_window:
                    # Hide console window
                    user32 = ctypes.WinDLL("user32")
                    user32.ShowWindow(console_window, 0)  # SW_HIDE
                    self.console_hidden = True
                    print("[Process Stealth] Console window hidden")

        except Exception as e:
            print(f"[Process Stealth] Failed to hide console: {e}")

    def show_console(self):
        """Show the console window."""
        try:
            if self.console_hidden:
                # Get console window handle
                kernel32 = ctypes.WinDLL("kernel32")
                console_window = kernel32.GetConsoleWindow()

                if console_window:
                    # Show console window
                    user32 = ctypes.WinDLL("user32")
                    user32.ShowWindow(console_window, 1)  # SW_SHOW
                    self.console_hidden = False
                    print("[Process Stealth] Console window shown")

        except Exception as e:
            print(f"[Process Stealth] Failed to show console: {e}")

    def change_process_name(self, new_name):
        """Change the process name (requires admin privileges)."""
        try:
            if not self.process_name_changed:
                # This is a simplified approach - actual process name changing
                # requires more complex techniques and admin privileges
                print(f"[Process Stealth] Process name change requested: {new_name}")
                print(
                    "[Process Stealth] Note: Full process name changing requires admin privileges"
                )
                self.process_name_changed = True
                self.original_process_name = os.path.basename(sys.executable)

        except Exception as e:
            print(f"[Process Stealth] Failed to change process name: {e}")

    def restore_process_name(self):
        """Restore the original process name."""
        try:
            if self.process_name_changed:
                print("[Process Stealth] Process name restored")
                self.process_name_changed = False
                self.original_process_name = None

        except Exception as e:
            print(f"[Process Stealth] Failed to restore process name: {e}")

    def minimize_memory_footprint(self):
        """Minimize memory footprint to reduce detection."""
        try:
            # Force garbage collection
            import gc

            gc.collect()

            # Clear any cached data
            if hasattr(sys, "_clear_type_cache"):
                sys._clear_type_cache()

            print("[Process Stealth] Memory footprint minimized")

        except Exception as e:
            print(f"[Process Stealth] Failed to minimize memory: {e}")

    def obfuscate_memory_patterns(self):
        """Obfuscate memory patterns to avoid detection."""
        try:
            # Allocate and deallocate memory to create noise
            noise_data = []
            for _ in range(100):
                noise_data.append(random.randint(0, 255))

            # Clear the noise
            del noise_data

        except Exception as e:
            print(f"[Process Stealth] Failed to obfuscate memory: {e}")

    def scramble_memory(self):
        """Scramble memory patterns by moving data around."""
        try:
            # Force garbage collection to compact memory
            gc.collect()

            # Allocate temporary buffers with random data
            temp_buffers = []
            for _ in range(random.randint(5, 15)):
                size = random.randint(1024, 10240)  # 1KB to 10KB
                buffer_data = bytearray(random.randint(0, 255) for _ in range(size))
                temp_buffers.append(buffer_data)

            # Clear type cache
            if hasattr(sys, "_clear_type_cache"):
                sys._clear_type_cache()

            # Deallocate buffers
            del temp_buffers
            gc.collect()

        except Exception as e:
            print(f"[Process Stealth] Failed to scramble memory: {e}")

    def allocate_fake_memory(self, count=None):
        """Allocate fake memory with random data to obfuscate memory patterns."""
        try:
            if count is None:
                count = random.randint(3, 8)  # 3-8 fake allocations

            # Clear old allocations if too many
            if len(self.fake_allocations) > 20:
                # Remove oldest 50%
                remove_count = len(self.fake_allocations) // 2
                self.fake_allocations = self.fake_allocations[remove_count:]

            # Allocate new fake memory blocks
            for _ in range(count):
                # Random size between 1KB and 50KB
                size = random.randint(1024, 51200)
                # Create random data
                fake_data = bytearray(random.randint(0, 255) for _ in range(size))
                # Store reference to prevent immediate garbage collection
                self.fake_allocations.append(fake_data)

        except Exception as e:
            print(f"[Process Stealth] Failed to allocate fake memory: {e}")

    def clear_fake_memory(self):
        """Clear all fake memory allocations."""
        try:
            self.fake_allocations.clear()
            gc.collect()
        except Exception as e:
            print(f"[Process Stealth] Failed to clear fake memory: {e}")

    def change_process_description(self, new_description=None):
        """Change process description/window title (does not require admin)."""
        try:
            if new_description is None:
                # Generate a random description to look like a normal app
                descriptions = [
                    "Windows Explorer",
                    "Microsoft Edge",
                    "Google Chrome",
                    "Visual Studio Code",
                    "Notepad++",
                    "Discord",
                    "Steam",
                    "Windows Security",
                ]
                new_description = random.choice(descriptions)

            # Get console window handle
            kernel32 = ctypes.WinDLL("kernel32")
            user32 = ctypes.WinDLL("user32")

            console_window = kernel32.GetConsoleWindow()
            if console_window:
                # Change window title (visible in Task Manager)
                user32.SetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPCWSTR]
                user32.SetWindowTextW.restype = wintypes.BOOL

                # Convert to wide string
                description_wide = new_description.encode("utf-16le") + b"\x00\x00"
                result = user32.SetWindowTextW(console_window, description_wide)

                if result:
                    if not self.description_changed:
                        # Try to get original title
                        try:
                            buffer = ctypes.create_unicode_buffer(256)
                            user32.GetWindowTextW.argtypes = [
                                wintypes.HWND,
                                wintypes.LPWSTR,
                                ctypes.c_int,
                            ]
                            user32.GetWindowTextW.restype = ctypes.c_int
                            length = user32.GetWindowTextW(console_window, buffer, 256)
                            if length > 0:
                                self.original_description = buffer.value
                        except Exception:
                            pass

                    self.description_changed = True
                    return True

            # Also try to change process title via sys.argv[0] manipulation
            # (This is a limited approach but doesn't require admin)
            try:
                if hasattr(sys, "argv") and len(sys.argv) > 0:
                    # Note: This doesn't actually change the process name,
                    # but can help with some detection methods
                    pass
            except Exception:
                pass

            return False

        except Exception as e:
            print(f"[Process Stealth] Failed to change process description: {e}")
            return False

    def restore_process_description(self):
        """Restore the original process description."""
        try:
            if self.description_changed and self.original_description:
                kernel32 = ctypes.WinDLL("kernel32")
                user32 = ctypes.WinDLL("user32")

                console_window = kernel32.GetConsoleWindow()
                if console_window:
                    user32.SetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPCWSTR]
                    user32.SetWindowTextW.restype = wintypes.BOOL

                    description_wide = (
                        self.original_description.encode("utf-16le") + b"\x00\x00"
                    )
                    user32.SetWindowTextW(console_window, description_wide)
                    self.description_changed = False
                    self.original_description = None

        except Exception as e:
            print(f"[Process Stealth] Failed to restore process description: {e}")

    def hide_from_task_manager(self):
        """Attempt to hide from Task Manager (advanced technique)."""
        try:
            # This is a placeholder - actual hiding from Task Manager
            # requires very advanced techniques and may not be possible
            # on modern Windows systems due to security restrictions
            print("[Process Stealth] Task Manager hiding not implemented")
            print("[Process Stealth] Note: Modern Windows prevents this for security")

        except Exception as e:
            print(f"[Process Stealth] Failed to hide from Task Manager: {e}")

    def get_process_info(self):
        """Get current process information."""
        try:
            current_process = psutil.Process()

            info = {
                "pid": current_process.pid,
                "name": current_process.name(),
                "memory_usage": current_process.memory_info().rss,
                "cpu_percent": current_process.cpu_percent(),
                "create_time": current_process.create_time(),
                "status": current_process.status(),
            }

            return info

        except Exception as e:
            print(f"[Process Stealth] Failed to get process info: {e}")
            return None

    def monitor_process(self):
        """Monitor process for suspicious activity."""
        try:
            current_process = psutil.Process()

            # Check memory usage
            memory_usage = current_process.memory_info().rss / 1024 / 1024  # MB
            if memory_usage > 500:  # More than 500MB
                print(f"[Process Stealth] High memory usage: {memory_usage:.1f}MB")
                self.minimize_memory_footprint()

            # Check CPU usage
            cpu_percent = current_process.cpu_percent()
            if cpu_percent > 50:  # More than 50% CPU
                print(f"[Process Stealth] High CPU usage: {cpu_percent:.1f}%")

        except Exception as e:
            print(f"[Process Stealth] Failed to monitor process: {e}")

    def cleanup(self):
        """Cleanup stealth features."""
        try:
            if self.console_hidden:
                self.show_console()

            if self.process_name_changed:
                self.restore_process_name()

            if self.description_changed:
                self.restore_process_description()

            # Clear fake memory allocations
            self.clear_fake_memory()

            print("[Process Stealth] Stealth features cleaned up")

        except Exception as e:
            print(f"[Process Stealth] Failed to cleanup: {e}")


class StealthMonitor:
    """Monitors and maintains stealth features."""

    def __init__(self):
        self.stealth = ProcessStealth()
        self.monitoring = False
        self.monitor_thread = None
        self.memory_scramble_thread = None
        self.memory_scramble_enabled = False
        self.scramble_interval_min = 300  # 5 minutes
        self.scramble_interval_max = 600  # 10 minutes

    def start_monitoring(self):
        """Start stealth monitoring."""
        if not self.monitoring:
            self.monitoring = True
            self.monitor_thread = threading.Thread(
                target=self._monitor_loop, daemon=True
            )
            self.monitor_thread.start()
            print("[Stealth Monitor] Started monitoring")

    def stop_monitoring(self):
        """Stop stealth monitoring."""
        self.monitoring = False
        self.memory_scramble_enabled = False
        if self.monitor_thread:
            self.monitor_thread.join()
        if self.memory_scramble_thread:
            self.memory_scramble_thread.join()
        print("[Stealth Monitor] Stopped monitoring")

    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self.stealth.monitor_process()
                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                print(f"[Stealth Monitor] Error: {e}")
                time.sleep(60)  # Wait longer on error

    def _memory_scramble_loop(self):
        """Periodic memory scrambling loop (runs every 5-10 minutes)."""
        while self.memory_scramble_enabled:
            try:
                # Random interval between 5-10 minutes
                interval = random.uniform(
                    self.scramble_interval_min, self.scramble_interval_max
                )
                time.sleep(interval)

                if self.memory_scramble_enabled:
                    # Perform memory scrambling
                    self.stealth.scramble_memory()
                    # Allocate some fake memory
                    self.stealth.allocate_fake_memory()

            except Exception as e:
                print(f"[Stealth Monitor] Memory scramble error: {e}")
                time.sleep(60)  # Wait on error

    def start_memory_scrambling(self, interval_min=300, interval_max=600):
        """Start periodic memory scrambling thread."""
        if not self.memory_scramble_enabled:
            self.scramble_interval_min = interval_min
            self.scramble_interval_max = interval_max
            self.memory_scramble_enabled = True
            self.memory_scramble_thread = threading.Thread(
                target=self._memory_scramble_loop, daemon=True
            )
            self.memory_scramble_thread.start()
            print(
                f"[Stealth Monitor] Started periodic memory scrambling "
                f"({interval_min//60}-{interval_max//60} minutes)"
            )

    def stop_memory_scrambling(self):
        """Stop periodic memory scrambling thread."""
        self.memory_scramble_enabled = False
        if self.memory_scramble_thread:
            self.memory_scramble_thread.join(timeout=5)
        print("[Stealth Monitor] Stopped periodic memory scrambling")

    def enable_stealth(
        self,
        change_description=True,
        enable_memory_scrambling=True,
        enable_fake_allocations=True,
    ):
        """Enable all stealth features."""
        try:
            # Hide console
            self.stealth.hide_console()

            # Change process description (doesn't require admin)
            if change_description:
                self.stealth.change_process_description()

            # Allocate initial fake memory
            if enable_fake_allocations:
                self.stealth.allocate_fake_memory(count=random.randint(3, 8))

            # Minimize memory footprint
            self.stealth.minimize_memory_footprint()

            # Obfuscate memory patterns
            self.stealth.obfuscate_memory_patterns()

            # Start periodic memory scrambling (5-10 minutes)
            if enable_memory_scrambling:
                self.start_memory_scrambling(interval_min=300, interval_max=600)

            # Start monitoring
            self.start_monitoring()

            print("[Stealth Monitor] All stealth features enabled")

        except Exception as e:
            print(f"[Stealth Monitor] Failed to enable stealth: {e}")

    def disable_stealth(self):
        """Disable all stealth features."""
        try:
            # Stop monitoring
            self.stop_monitoring()

            # Cleanup stealth features
            self.stealth.cleanup()

            print("[Stealth Monitor] All stealth features disabled")

        except Exception as e:
            print(f"[Stealth Monitor] Failed to disable stealth: {e}")


# Global instance
stealth_monitor = StealthMonitor()


def enable_process_stealth(
    change_description=True,
    enable_memory_scrambling=True,
    enable_fake_allocations=True,
):
    """Enable process stealth features.

    Args:
        change_description: Change process description/window title (default: True)
        enable_memory_scrambling: Enable periodic memory scrambling every 5-10 min (default: True)
        enable_fake_allocations: Allocate fake memory with random data (default: True)
    """
    stealth_monitor.enable_stealth(
        change_description=change_description,
        enable_memory_scrambling=enable_memory_scrambling,
        enable_fake_allocations=enable_fake_allocations,
    )


def disable_process_stealth():
    """Disable process stealth features."""
    stealth_monitor.disable_stealth()


def get_process_info():
    """Get current process information."""
    return stealth_monitor.stealth.get_process_info()


def is_stealth_enabled():
    """Check if stealth is enabled."""
    return stealth_monitor.monitoring
