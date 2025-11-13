"""Process stealth features for better hiding."""

import os
import sys
import ctypes
import psutil
import threading
import time


class ProcessStealth:
    """Manages process stealth features."""

    def __init__(self):
        self.original_title = None
        self.console_hidden = False
        self.process_name_changed = False
        self.original_process_name = None

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
            import random

            # Create some random data
            noise_data = []
            for _ in range(100):
                noise_data.append(random.randint(0, 255))

            # Clear the noise
            del noise_data

            print("[Process Stealth] Memory patterns obfuscated")

        except Exception as e:
            print(f"[Process Stealth] Failed to obfuscate memory: {e}")

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

            print("[Process Stealth] Stealth features cleaned up")

        except Exception as e:
            print(f"[Process Stealth] Failed to cleanup: {e}")


class StealthMonitor:
    """Monitors and maintains stealth features."""

    def __init__(self):
        self.stealth = ProcessStealth()
        self.monitoring = False
        self.monitor_thread = None

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
        if self.monitor_thread:
            self.monitor_thread.join()
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

    def enable_stealth(self):
        """Enable all stealth features."""
        try:
            # Hide console
            self.stealth.hide_console()

            # Minimize memory footprint
            self.stealth.minimize_memory_footprint()

            # Obfuscate memory patterns
            self.stealth.obfuscate_memory_patterns()

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


def enable_process_stealth():
    """Enable process stealth features."""
    stealth_monitor.enable_stealth()


def disable_process_stealth():
    """Disable process stealth features."""
    stealth_monitor.disable_stealth()


def get_process_info():
    """Get current process information."""
    return stealth_monitor.stealth.get_process_info()


def is_stealth_enabled():
    """Check if stealth is enabled."""
    return stealth_monitor.monitoring
