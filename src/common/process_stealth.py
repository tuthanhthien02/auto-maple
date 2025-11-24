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

from src.common.logger import get_logger

log = get_logger(__name__)
DEFAULT_PROCESS_NAME = "explorer.exe"
DEFAULT_FAKE_PROCESS_DESC = "File Explorer"
DEFAULT_DESCRIPTION_FALLBACK = "Windows Explorer"


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
        self._fake_mem_lock = threading.Lock()  # Thread safety for fake_allocations
        base_identity_pool = [
            (DEFAULT_PROCESS_NAME, DEFAULT_FAKE_PROCESS_DESC),
            ("chrome.exe", "Google Chrome"),
            ("msedge.exe", "Microsoft Edge"),
            ("Code.exe", "Visual Studio Code"),
            ("notepad.exe", "Notepad"),
            ("Discord.exe", "Discord"),
            ("Steam.exe", "Steam Client Bootstrapper"),
            ("Teams.exe", "Microsoft Teams"),
            ("Spotify.exe", "Spotify"),
            ("AcroRd32.exe", "Adobe Acrobat"),
            ("WinRAR.exe", "WinRAR"),
            ("7zFM.exe", "7-Zip File Manager"),
            ("vlc.exe", "VLC media player"),
            ("paintdotnet.exe", "Paint.NET"),
            ("Calculator.exe", "Calculator"),
            ("wmplayer.exe", "Windows Media Player"),
            ("svchost.exe", "Service Host"),
            ("dwm.exe", "Desktop Window Manager"),
            ("winlogon.exe", "Windows Logon Application"),
            ("csrss.exe", "Client Server Runtime Process"),
        ]
        self._identity_pool = base_identity_pool
        identity_descriptions = [desc for _, desc in base_identity_pool]
        extra_descriptions = [
            "Notepad++",
            "Windows Security",
            "Windows Update",
            "Windows Defender",
            "Adobe Reader",
            DEFAULT_DESCRIPTION_FALLBACK,
        ]
        merged = identity_descriptions + extra_descriptions
        # Preserve order while removing duplicates
        self._description_pool = list(dict.fromkeys(merged))

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
                    log.info("[Process Stealth] Console window hidden")

        except Exception as e:
            log.error("[Process Stealth] Failed to hide console: %s", e)

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
                    log.info("[Process Stealth] Console window shown")

        except Exception as e:
            log.error("[Process Stealth] Failed to show console: %s", e)

    def _select_random_identity(self):
        """Pick a random (process_name, description) tuple from system or fallback."""
        current_proc = os.path.basename(sys.executable).lower()
        candidates = []
        try:
            for proc in psutil.process_iter(["name"]):
                name = proc.info.get("name")
                if not name:
                    continue
                lname = name.lower()
                if not lname.endswith(".exe"):
                    continue
                if lname == current_proc:
                    continue
                candidates.append((name, name.replace(".exe", "")))
        except Exception:
            candidates = []

        if candidates:
            return random.choice(candidates)
        return random.choice(self._identity_pool)

    def _resolve_process_identity(self, requested_name, randomize):
        if requested_name:
            return requested_name, requested_name.replace(".exe", "")
        if randomize:
            return self._select_random_identity()
        return DEFAULT_PROCESS_NAME, DEFAULT_FAKE_PROCESS_DESC

    def _resolve_description(self, requested_description, randomize):
        if requested_description:
            return requested_description
        if randomize:
            return random.choice(self._description_pool)
        return DEFAULT_DESCRIPTION_FALLBACK

    def _cache_original_description(self, user32, console_window):
        if self.description_changed:
            return
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

    def _set_console_description(self, description):
        kernel32 = ctypes.WinDLL("kernel32")
        user32 = ctypes.WinDLL("user32")
        console_window = kernel32.GetConsoleWindow()
        if not console_window:
            return False

        user32.SetWindowTextW.argtypes = [wintypes.HWND, ctypes.c_wchar_p]
        user32.SetWindowTextW.restype = wintypes.BOOL
        result = user32.SetWindowTextW(console_window, description)
        if result:
            self._cache_original_description(user32, console_window)
            return True

        log.warning("[Process Stealth] SetWindowTextW returned False (may need admin)")
        return False

    def _attempt_sysargv_spoof(self):
        try:
            if hasattr(sys, "argv") and len(sys.argv) > 0:
                # Placeholder for additional spoofing if needed
                pass
        except Exception:
            pass

    def change_process_name(self, new_name=None, randomize=True):
        """Change the process name with randomization support.

        Args:
            new_name: Specific process name to use (if None, will randomize)
            randomize: If True, randomly select from pool of common process names

        Note: Actual process name changing requires admin privileges and complex techniques.
        This function primarily changes the window title/description which is more accessible.
        """
        try:
            if self.process_name_changed:
                return

            selected_name, selected_description = self._resolve_process_identity(
                new_name, randomize
            )

            log.info(
                "[Process Stealth] Process name change requested: %s", selected_name
            )
            log.info(
                "[Process Stealth] Note: Full process name changing requires admin privileges"
            )
            self.process_name_changed = True
            self.original_process_name = os.path.basename(sys.executable)

            if randomize and not self.description_changed:
                description = selected_description or selected_name.replace(".exe", "")
                self.change_process_description(description, randomize=False)

        except Exception as e:
            log.error("[Process Stealth] Failed to change process name: %s", e)

    def restore_process_name(self):
        """Restore the original process name."""
        try:
            if self.process_name_changed:
                log.info("[Process Stealth] Process name restored")
                self.process_name_changed = False
                self.original_process_name = None

        except Exception as e:
            log.error("[Process Stealth] Failed to restore process name: %s", e)

    def minimize_memory_footprint(self):
        """Minimize memory footprint to reduce detection."""
        try:
            # Optimization: Multiple GC passes for better cleanup
            gc.collect(0)  # Collect generation 0
            gc.collect(1)  # Collect generation 1
            gc.collect(2)  # Collect generation 2 (full collection)
            gc.collect()  # Final pass

            # Clear any cached data
            if hasattr(sys, "_clear_type_cache"):
                sys._clear_type_cache()

            # Optimization: Clear module-level caches if possible
            # Bug fix: Only invalidate caches if safe (not during critical operations)
            try:
                import importlib

                # Clear importlib cache
                # Note: invalidate_caches() is safe to call, it only clears import cache
                # and doesn't affect already-loaded modules
                if hasattr(importlib, "invalidate_caches"):
                    importlib.invalidate_caches()
            except Exception:
                pass  # Ignore if not available

            log.debug("[Process Stealth] Memory footprint minimized")

        except Exception as e:
            log.error("[Process Stealth] Failed to minimize memory: %s", e)

    def obfuscate_memory_patterns(self):
        """Obfuscate memory patterns to avoid detection."""
        try:
            # Optimization: Create more substantial noise to be more effective
            # Allocate multiple buffers with random data (10-20 buffers, 1-5KB each)
            # Bug fix: Limit total memory allocation to prevent excessive memory usage
            max_total_memory = 100 * 1024  # Max 100KB total
            noise_buffers = []
            buffer_count = random.randint(10, 20)
            total_allocated = 0

            for _ in range(buffer_count):
                if total_allocated >= max_total_memory:
                    break  # Stop if we've allocated enough
                size = random.randint(1024, 5120)  # 1KB to 5KB
                # Bug fix: Ensure we don't exceed max_total_memory
                remaining = max_total_memory - total_allocated
                if size > remaining:
                    size = remaining
                if size <= 0:
                    break

                noise_data = bytearray(random.randint(0, 255) for _ in range(size))
                noise_buffers.append(noise_data)
                total_allocated += size

            # Clear the noise
            # Bug fix: Explicitly delete each buffer before clearing list
            for buffer in noise_buffers:
                del buffer
            del noise_buffers
            gc.collect()  # Force GC to actually free memory

        except Exception as e:
            log.error("[Process Stealth] Failed to obfuscate memory: %s", e)

    def scramble_memory(self):
        """Scramble memory patterns by moving data around."""
        try:
            # Optimization: Multiple GC passes before scrambling
            gc.collect(0)
            gc.collect(1)
            gc.collect(2)

            # Optimization: Allocate more substantial temporary buffers with random data
            # Use larger buffers (5-20 buffers, 5-50KB each) for better obfuscation
            # Bug fix: Limit total memory allocation to prevent excessive memory usage
            max_total_memory = 500 * 1024  # Max 500KB total
            temp_buffers = []
            buffer_count = random.randint(5, 20)
            total_allocated = 0

            for _ in range(buffer_count):
                if total_allocated >= max_total_memory:
                    break  # Stop if we've allocated enough
                size = random.randint(
                    5120, 51200
                )  # 5KB to 50KB (increased from 1-10KB)
                # Bug fix: Ensure we don't exceed max_total_memory
                remaining = max_total_memory - total_allocated
                if size > remaining:
                    size = remaining
                if size <= 0:
                    break

                buffer_data = bytearray(random.randint(0, 255) for _ in range(size))
                temp_buffers.append(buffer_data)
                total_allocated += size

            # Optimization: Clear type cache and module cache
            if hasattr(sys, "_clear_type_cache"):
                sys._clear_type_cache()

            # Bug fix: Only invalidate caches if safe
            try:
                import importlib

                if hasattr(importlib, "invalidate_caches"):
                    importlib.invalidate_caches()
            except Exception:
                pass

            # Optimization: Explicitly delete each buffer before clearing list
            for buffer in temp_buffers:
                del buffer
            del temp_buffers

            # Optimization: Multiple GC passes after scrambling
            gc.collect(0)
            gc.collect(1)
            gc.collect(2)
            gc.collect()  # Final pass

        except Exception as e:
            log.error("[Process Stealth] Failed to scramble memory: %s", e)

    def allocate_fake_memory(self, count=None):
        """Allocate fake memory with random data to obfuscate memory patterns."""
        try:
            if count is None:
                count = random.randint(3, 8)  # 3-8 fake allocations

            # Thread-safe: Clear old allocations if too many
            with self._fake_mem_lock:
                if len(self.fake_allocations) > 20:
                    # Remove oldest 50%
                    remove_count = len(self.fake_allocations) // 2
                    self.fake_allocations = self.fake_allocations[remove_count:]

            # Allocate new fake memory blocks (thread-safe)
            with self._fake_mem_lock:
                for _ in range(count):
                    # Random size between 1KB and 50KB
                    size = random.randint(1024, 51200)
                    # Create random data
                    fake_data = bytearray(random.randint(0, 255) for _ in range(size))
                    # Store reference to prevent immediate garbage collection
                    self.fake_allocations.append(fake_data)

        except Exception as e:
            log.error("[Process Stealth] Failed to allocate fake memory: %s", e)

    def clear_fake_memory(self):
        """Clear all fake memory allocations."""
        try:
            with self._fake_mem_lock:
                # Optimization: Explicitly delete each allocation before clearing list
                # Bug fix: Create a copy of the list to avoid modifying while iterating
                allocations_to_clear = list(self.fake_allocations)
                for allocation in allocations_to_clear:
                    try:
                        del allocation
                    except Exception:
                        pass  # Ignore errors when deleting individual allocations
                self.fake_allocations.clear()
            # Force multiple GC passes to ensure memory is actually freed
            gc.collect()
            gc.collect()  # Second pass for better cleanup
        except Exception as e:
            log.error("[Process Stealth] Failed to clear fake memory: %s", e)

    def change_process_description(self, new_description=None, randomize=True):
        """Change process description/window title (does not require admin).

        Args:
            new_description: Specific description to use (if None, will randomize)
            randomize: If True, randomly select from pool of common app names
        """
        try:
            description = self._resolve_description(new_description, randomize)
            if self._set_console_description(description):
                self.description_changed = True
                log.info(
                    "[Process Stealth] Process description changed to: %s",
                    description,
                )
                return True

            self._attempt_sysargv_spoof()
            return False

        except Exception as e:
            log.error("[Process Stealth] Failed to change process description: %s", e)
            return False

    def restore_process_description(self):
        """Restore the original process description."""
        try:
            if self.description_changed and self.original_description:
                kernel32 = ctypes.WinDLL("kernel32")
                user32 = ctypes.WinDLL("user32")

                console_window = kernel32.GetConsoleWindow()
                if console_window:
                    user32.SetWindowTextW.argtypes = [wintypes.HWND, ctypes.c_wchar_p]
                    user32.SetWindowTextW.restype = wintypes.BOOL

                    user32.SetWindowTextW(console_window, self.original_description)
                    self.description_changed = False
                    self.original_description = None

        except Exception as e:
            log.error("[Process Stealth] Failed to restore process description: %s", e)

    def hide_from_task_manager(self):
        """Attempt to hide from Task Manager (advanced technique)."""
        try:
            # This is a placeholder - actual hiding from Task Manager
            # requires very advanced techniques and may not be possible
            # on modern Windows systems due to security restrictions
            log.info("[Process Stealth] Task Manager hiding not implemented")
            log.info(
                "[Process Stealth] Note: Modern Windows prevents this for security"
            )

        except Exception as e:
            log.error("[Process Stealth] Failed to hide from Task Manager: %s", e)

    def get_process_info(self):
        """Get current process information."""
        try:
            current_process = psutil.Process()

            info = {
                "pid": current_process.pid,
                "name": current_process.name(),
                "memory_usage": current_process.memory_info().rss,
                "cpu_percent": current_process.cpu_percent(interval=0.1),
                "create_time": current_process.create_time(),
                "status": current_process.status(),
            }

            return info

        except Exception as e:
            log.error("[Process Stealth] Failed to get process info: %s", e)
            return None

    def monitor_process(self):
        """Monitor process for suspicious activity."""
        try:
            current_process = psutil.Process()

            # Check memory usage
            memory_usage = current_process.memory_info().rss / 1024 / 1024  # MB
            if memory_usage > 500:  # More than 500MB
                log.warning("[Process Stealth] High memory usage: %.1fMB", memory_usage)
                self.minimize_memory_footprint()

            # Check CPU usage (need interval for accurate reading)
            cpu_percent = current_process.cpu_percent(interval=0.1)
            if cpu_percent > 50:  # More than 50% CPU
                log.warning("[Process Stealth] High CPU usage: %.1f%%", cpu_percent)

        except Exception as e:
            log.error("[Process Stealth] Failed to monitor process: %s", e)

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

            log.info("[Process Stealth] Stealth features cleaned up")

        except Exception as e:
            log.error("[Process Stealth] Failed to cleanup: %s", e)


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
            log.info("[Stealth Monitor] Started monitoring")

    def stop_monitoring(self):
        """Stop stealth monitoring."""
        self.monitoring = False
        self.memory_scramble_enabled = False
        if self.monitor_thread:
            self.monitor_thread.join()
        if self.memory_scramble_thread:
            self.memory_scramble_thread.join()
        log.info("[Stealth Monitor] Stopped monitoring")

    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.monitoring:
            try:
                self.stealth.monitor_process()
                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                log.error("[Stealth Monitor] Error: %s", e, exc_info=True)
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
                log.error(
                    "[Stealth Monitor] Memory scramble error: %s", e, exc_info=True
                )
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
            log.info(
                "[Stealth Monitor] Started periodic memory scrambling "
                "(%d-%d minutes)",
                interval_min // 60,
                interval_max // 60,
            )

    def stop_memory_scrambling(self):
        """Stop periodic memory scrambling thread."""
        self.memory_scramble_enabled = False
        if self.memory_scramble_thread:
            self.memory_scramble_thread.join(timeout=5)
        log.info("[Stealth Monitor] Stopped periodic memory scrambling")

    def enable_stealth(
        self,
        change_description=True,
        randomize_process_name=True,
        enable_memory_scrambling=True,
        enable_fake_allocations=True,
    ):
        """Enable all stealth features.

        Args:
            change_description: Change process description/window title (default: True)
            randomize_process_name: Randomize process name/description (default: True)
            enable_memory_scrambling: Enable periodic memory scrambling (default: True)
            enable_fake_allocations: Allocate fake memory with random data (default: True)
        """
        try:
            # Hide console
            self.stealth.hide_console()

            # Change process name (with randomization)
            if randomize_process_name:
                self.stealth.change_process_name(randomize=True)

            # Change process description (doesn't require admin)
            if change_description:
                self.stealth.change_process_description(
                    randomize=randomize_process_name
                )

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

            log.info("[Stealth Monitor] All stealth features enabled")
            log.info(
                "[Stealth Monitor] Features: console_hidden=%s, description_changed=%s, "
                "memory_scrambling=%s, fake_allocations=%d",
                self.stealth.console_hidden,
                self.stealth.description_changed,
                self.memory_scramble_enabled,
                len(self.stealth.fake_allocations),
            )

        except Exception as e:
            log.error(
                "[Stealth Monitor] Failed to enable stealth: %s", e, exc_info=True
            )

    def disable_stealth(self):
        """Disable all stealth features."""
        try:
            # Stop monitoring
            self.stop_monitoring()

            # Cleanup stealth features
            self.stealth.cleanup()

            log.info("[Stealth Monitor] All stealth features disabled")

        except Exception as e:
            log.error(
                "[Stealth Monitor] Failed to disable stealth: %s", e, exc_info=True
            )


# Global instance
stealth_monitor = StealthMonitor()


def enable_process_stealth(
    change_description=True,
    randomize_process_name=True,
    enable_memory_scrambling=True,
    enable_fake_allocations=True,
):
    """Enable process stealth features.

    Args:
        change_description: Change process description/window title (default: True)
        randomize_process_name: Randomize process name/description (default: True)
        enable_memory_scrambling: Enable periodic memory scrambling every 5-10 min (default: True)
        enable_fake_allocations: Allocate fake memory with random data (default: True)
    """
    stealth_monitor.enable_stealth(
        change_description=change_description,
        randomize_process_name=randomize_process_name,
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


def get_stealth_status():
    """Get detailed status of all stealth features.

    Returns:
        dict: Dictionary containing status of all stealth features
    """
    status = {
        "enabled": stealth_monitor.monitoring,
        "console_hidden": stealth_monitor.stealth.console_hidden,
        "description_changed": stealth_monitor.stealth.description_changed,
        "original_description": stealth_monitor.stealth.original_description,
        "memory_scrambling_enabled": stealth_monitor.memory_scramble_enabled,
        "fake_allocations_count": len(stealth_monitor.stealth.fake_allocations),
        "process_info": stealth_monitor.stealth.get_process_info(),
    }
    return status
