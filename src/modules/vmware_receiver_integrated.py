"""
VMware Receiver Integrated - TCP Server để nhận input từ Host và forward đến Arduino
Tích hợp vào GUI để dùng chung serial connection, tránh "Access is denied"

KHÔNG tạo serial connection riêng - sử dụng SharedArduinoConnection
"""

import ctypes
import ctypes.wintypes
import json
import os
import socket
import sys
import threading
import time
import winsound
from ctypes import wintypes

from src.common.logger import get_logger

log = get_logger(__name__)

# Windows API constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
HC_ACTION = 0
PM_REMOVE = 0x0001
PM_NOYIELD = 0x0002

# Compat: some Python builds lack wintypes.ULONG_PTR
if not hasattr(wintypes, "ULONG_PTR"):
    wintypes.ULONG_PTR = wintypes.WPARAM

# Ensure console can print UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    ]


class VMwareReceiverIntegrated:
    """
    TCP Server nhận commands từ Host và forward đến Arduino
    Sử dụng SharedArduinoConnection để tránh "Access is denied"
    """

    def __init__(
        self,
        server_port=12345,
        enable_hotkey_hook=False,
        enable_logging=False,
        key_mapping=None,
    ):
        """
        Initialize VMware Receiver Integrated

        Args:
            server_port: TCP server port (default: 12345)
            enable_hotkey_hook: Enable keyboard hook for End key hotkey (default: False)
            enable_logging: Enable debug logging (default: False)
            key_mapping: Key remapping dictionary (optional, will load from config if not provided)
        """
        log.info(
            "[VMwareReceiverIntegrated] Initializing VMware Receiver Integrated..."
        )
        log.info(
            f"[VMwareReceiverIntegrated] Server port: {server_port}, Hotkey hook: {enable_hotkey_hook}"
        )

        self.server_port = server_port
        self.enable_hotkey_hook = enable_hotkey_hook
        self.enable_logging = enable_logging

        # Use SharedArduinoConnection instead of creating serial connection
        from src.common.shared_arduino_connection import SharedArduinoConnection

        log.debug(
            "[VMwareReceiverIntegrated] Getting SharedArduinoConnection instance..."
        )
        self.shared_connection = SharedArduinoConnection.get_instance()
        arduino_connected = self.shared_connection.is_connected()
        log.info(
            f"[VMwareReceiverIntegrated] SharedArduinoConnection status: {'CONNECTED' if arduino_connected else 'DISCONNECTED'}"
        )

        # Key remapping (will sync with shared connection)
        self.key_mapping = key_mapping or {}
        self.remapping_enabled = True

        # Load config
        self.CONFIG_PATH = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "vmware_receiver.config.json",
        )
        self._load_config()

        # TCP server
        self.server_socket = None
        self.running = False
        self.client_socket = None
        self.client_address = None
        self.server_thread = None

        # Keyboard hook for hotkeys (OPTIONAL)
        self.hook = None
        self.user32 = None
        self.kernel32 = None
        self.VK_END = 0x23  # End key -> toggle remapping
        self.hook_thread = None

        # Stats (thread-safe with lock)
        self.stats = {
            "total_received": 0,
            "total_forwarded": 0,
            "total_errors": 0,
            "total_clients": 0,
            "total_remapped": 0,
        }
        self._stats_lock = threading.Lock()  # Bug fix: Thread safety for stats

        # Initialize Windows API for keyboard hook
        if self.enable_hotkey_hook:
            self._init_windows_api()

    def _load_config(self):
        """Load config from JSON file"""
        try:
            if os.path.exists(self.CONFIG_PATH):
                with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                    config = json.load(f)
                    self.server_port = config.get("server_port", self.server_port)
                    self.enable_logging = config.get(
                        "enable_logging", self.enable_logging
                    )
                    self.enable_hotkey_hook = config.get(
                        "enable_hotkey_hook", self.enable_hotkey_hook
                    )

                    # Load key remapping
                    key_mapping_config = config.get("key_mapping", {})
                    if key_mapping_config:
                        self.key_mapping = {
                            k.lower(): v.lower() for k, v in key_mapping_config.items()
                        }
                        if self.enable_logging:
                            log.info(
                                f"[CONFIG] Loaded key remapping: {len(self.key_mapping)} mappings"
                            )
                            for orig, mapped in self.key_mapping.items():
                                log.info(f"[CONFIG]   {orig} → {mapped}")
                    else:
                        self.key_mapping = {}

                    if self.enable_logging:
                        log.info(f"[CONFIG] Server port: {self.server_port}")
                        hook_status = (
                            "ENABLED"
                            if self.enable_hotkey_hook
                            else "DISABLED (recommended: zero delay)"
                        )
                        log.info(f"[CONFIG] Hotkey hook: {hook_status}")
        except Exception as e:
            if self.enable_logging:
                log.warning(f"[CONFIG] Load error: {e}")

    def _init_windows_api(self):
        """Initialize Windows API for keyboard hook"""
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32

        # Define SetWindowsHookExW signature
        HOOKPROC = ctypes.WINFUNCTYPE(
            ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM
        )

        self.user32.SetWindowsHookExW.argtypes = [
            ctypes.c_int,
            HOOKPROC,
            wintypes.HINSTANCE,
            wintypes.DWORD,
        ]
        self.user32.SetWindowsHookExW.restype = wintypes.HHOOK

        # Define CallNextHookEx
        self.user32.CallNextHookEx.argtypes = [
            wintypes.HHOOK,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self.user32.CallNextHookEx.restype = ctypes.c_int

        # Define UnhookWindowsHookEx
        self.user32.UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
        self.user32.UnhookWindowsHookEx.restype = wintypes.BOOL

        # Define GetModuleHandleW
        self.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        self.kernel32.GetModuleHandleW.restype = wintypes.HINSTANCE

        # Define PeekMessageW
        self.user32.PeekMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
            wintypes.UINT,
        ]
        self.user32.PeekMessageW.restype = wintypes.BOOL

        # Define TranslateMessage and DispatchMessageW
        self.user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
        self.user32.TranslateMessage.restype = wintypes.BOOL

        self.user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]

        # Define PostQuitMessage
        self.user32.PostQuitMessage.argtypes = [ctypes.c_int]
        self.user32.PostQuitMessage.restype = None

    def _low_level_keyboard_proc(self, nCode, wParam, lParam):
        """
        Low-level keyboard hook callback - ZERO DELAY for local input
        CRITICAL: This hook ONLY intercepts End key for hotkey
        ALL other keys pass through IMMEDIATELY
        """
        # Fast path 1: if not action code, pass through immediately
        if nCode < HC_ACTION:
            return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)

        # Parse structure to get vkCode
        kb_data = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk_code = kb_data.vkCode

        # Fast path 2: if NOT End key, pass through IMMEDIATELY
        if vk_code != self.VK_END:
            return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)

        # Only End key reaches here - handle hotkey
        if wParam == WM_KEYDOWN:
            self.shared_connection.toggle_remapping()
            self.remapping_enabled = self.shared_connection.remapping_enabled
            status = "ENABLED" if self.remapping_enabled else "DISABLED"
            log.info(f"[HOTKEY] End → Key remapping: {status}")
            if self.remapping_enabled:
                winsound.Beep(800, 150)  # ON - Higher pitch
            else:
                winsound.Beep(400, 150)  # OFF - Lower pitch
        return 1  # Block End key only

    def install_hook(self):
        """Install low-level keyboard hook"""
        if not self.enable_hotkey_hook:
            return False

        try:
            HOOKPROC = ctypes.WINFUNCTYPE(
                ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM
            )

            self.hook_proc = HOOKPROC(self._low_level_keyboard_proc)
            hMod = self.kernel32.GetModuleHandleW(None)
            self.hook = self.user32.SetWindowsHookExW(
                WH_KEYBOARD_LL, self.hook_proc, hMod, 0
            )

            if not self.hook:
                error_code = self.kernel32.GetLastError()
                log.error(
                    f"[ERROR] Failed to install keyboard hook. Error code: {error_code}"
                )
                return False

            return True
        except Exception as e:
            log.error(f"[ERROR] Hook installation error: {e}")
            return False

    def uninstall_hook(self):
        """Uninstall keyboard hook"""
        if self.hook:
            try:
                self.user32.UnhookWindowsHookEx(self.hook)
                self.hook = None
                self.hook_proc = None
            except Exception as e:
                log.error(f"[ERROR] Hook uninstallation error: {e}")

    def message_loop(self):
        """Windows message loop for keyboard hook"""
        msg = wintypes.MSG()
        try:
            while self.running:
                bRet = self.user32.PeekMessageW(
                    ctypes.byref(msg), None, 0, 0, PM_REMOVE | PM_NOYIELD
                )
                if bRet:
                    if msg.message == 0x0012:  # WM_QUIT
                        break
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageW(ctypes.byref(msg))
                else:
                    time.sleep(0)  # Yield to other threads
        except Exception as e:
            log.error(f"[ERROR] Keyboard hook message loop error: {e}")
        finally:
            # Bug fix: Ensure hook is uninstalled even if exception occurs
            log.debug(
                "[VMwareReceiverIntegrated] Cleaning up keyboard hook in message_loop..."
            )
            self.uninstall_hook()

    def send_key_to_arduino(self, key_name: str, action: str) -> bool:
        """
        Gửi command đến Arduino qua SharedArduinoConnection

        Args:
            key_name: Key name
            action: 'down' or 'up'

        Returns:
            True if sent successfully, False otherwise
        """
        try:
            result = self.shared_connection.send_command(action, key_name)
            # Bug fix: Thread-safe stats update
            with self._stats_lock:
                if result:
                    self.stats["total_forwarded"] += 1
                    if self.enable_logging:
                        log.debug(f"[FORWARD] {action}:{key_name} → Arduino")
                else:
                    self.stats["total_errors"] += 1
                    if self.enable_logging:
                        log.warning(f"[ERROR] Failed to forward: {action}:{key_name}")
            return result
        except Exception as e:
            log.error(f"[ERROR] Send error: {e}")
            # Bug fix: Thread-safe stats update
            with self._stats_lock:
                self.stats["total_errors"] += 1
            return False

    def send_all_up(self):
        """Gửi lệnh release tất cả keys đến Arduino"""
        self.shared_connection.send_all_up()
        if self.enable_logging:
            log.debug("[FORWARD] all_up")

    def handle_client(self, client_socket, client_address):
        """Xử lý client connection"""
        # Bug fix: Thread-safe client socket assignment
        with self._stats_lock:
            self.client_socket = client_socket
            self.client_address = client_address
            self.stats["total_clients"] += 1

        log.info(f"[CLIENT] ✓ Connected from {client_address[0]}:{client_address[1]}")

        try:
            buffer = ""
            while self.running:
                data = client_socket.recv(1024)
                if not data:
                    break

                buffer += data.decode("utf-8", errors="ignore")

                # Process complete commands (ending with \n)
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()

                    if line:
                        # Bug fix: Thread-safe stats update
                        with self._stats_lock:
                            self.stats["total_received"] += 1
                        if self.enable_logging:
                            log.debug(f"[RECEIVED] Command: {line}")
                        self.process_command(line)

        except Exception as e:
            if self.running:
                log.error(f"[ERROR] Client handler error: {e}")
            else:
                log.debug(
                    f"[CLIENT] Connection closed while shutting down: {client_address} ({e})"
                )
        finally:
            log.info(
                f"[CLIENT] ✗ Disconnected from {client_address[0]}:{client_address[1]}"
            )
            try:
                client_socket.close()
            except Exception:
                pass
            self.client_socket = None
            self.client_address = None

    def process_command(self, command: str):
        """
        Xử lý command từ Host
        Commands: "down:<key>", "up:<key>", "all_up"
        """
        command = command.strip()

        if not command:
            return

        if command == "all_up":
            self.send_all_up()
            return

        # Parse: "action:key"
        if ":" not in command:
            log.warning(f"[WARN] Invalid command format: {command}")
            return

        action, key_name = command.split(":", 1)
        action = action.strip().lower()
        key_name = key_name.strip().lower()

        if action in ("down", "up"):
            # Key remapping is handled by SharedArduinoConnection
            # Just forward the command
            result = self.send_key_to_arduino(key_name, action)
            if not result:
                log.warning(f"[PROCESS] ✗ Failed to forward: {action}:{key_name}")
        elif action == "command":
            self._handle_command_action(key_name)
        else:
            log.warning(f"[WARN] Unknown action: {action} (command: {command})")

    def _handle_command_action(self, command_name: str):
        if command_name == "toggle_bot":
            self._handle_remote_toggle()
        else:
            log.warning(f"[COMMAND] Unknown command: {command_name}")

    def _handle_remote_toggle(self):
        try:
            from src.modules.listener import Listener

            Listener.toggle_enabled()
            log.info("[COMMAND] Remote toggle executed via Listener.toggle_enabled()")
        except Exception as exc:
            log.warning(
                "[COMMAND] Listener.toggle_enabled() unavailable (%s); trying fallback",
                exc,
            )
            try:
                from src.common import config as global_config, utils

                global_config.enabled = not global_config.enabled
                utils.print_state()
                log.info("[COMMAND] Remote toggle executed via config fallback")
            except Exception as fallback_exc:
                log.error(
                    "[COMMAND] Remote toggle failed: %s",
                    fallback_exc,
                    exc_info=True,
                )

    def _server_loop(self):
        """TCP server loop (runs in background thread)"""
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(("0.0.0.0", self.server_port))
            self.server_socket.listen(5)
            self.server_socket.settimeout(
                1.0
            )  # Timeout for accept to check running flag

            log.info(f"[SERVER] ✓ TCP server started on port {self.server_port}")
            log.info("[SERVER] Listening for Host sender connection...")
            arduino_status = (
                "CONNECTED" if self.shared_connection.is_connected() else "DISCONNECTED"
            )
            log.info(f"[STATUS] Arduino: {arduino_status}")

            while self.running:
                try:
                    client_socket, client_address = self.server_socket.accept()
                    # Handle client in separate thread
                    # Bug fix: Thread-safe client socket check and close
                    old_client = None
                    with self._stats_lock:
                        if self.client_socket:
                            old_client = self.client_socket
                            self.client_socket = None
                            self.client_address = None
                    if old_client:
                        try:
                            old_client.close()
                        except Exception:
                            pass

                    client_thread = threading.Thread(
                        target=self.handle_client,
                        args=(client_socket, client_address),
                        daemon=True,
                    )
                    client_thread.start()

                except socket.timeout:
                    continue
                except Exception as e:
                    if self.running:
                        log.error(f"[ERROR] Accept error: {e}")
                    break

        except Exception as e:
            log.error(f"[ERROR] Server error: {e}")
            import traceback

            traceback.print_exc()
        finally:
            # Ensure resources are cleaned up if the loop exits unexpectedly
            self.stop_tcp_server()

    def start_tcp_server(self):
        """Start TCP server in background thread"""
        if self.running:
            log.warning("[VMwareReceiverIntegrated] TCP server is already running")
            return

        log.info("[VMwareReceiverIntegrated] Starting TCP server...")
        self.running = True

        # Install keyboard hook if enabled
        if self.enable_hotkey_hook:
            try:
                if self.install_hook():
                    log.info("[HOOK] ✓ Keyboard hook installed (hotkeys only)")
                    log.info("[HOTKEYS] End = toggle key remapping")
                    # Start message loop thread for keyboard hook
                    self.hook_thread = threading.Thread(
                        target=self.message_loop, daemon=True
                    )
                    self.hook_thread.start()
                else:
                    log.warning(
                        "[WARN] Failed to install keyboard hook (hotkeys disabled)"
                    )
            except Exception as e:
                log.warning(f"[WARN] Hook installation failed: {e}")
        else:
            log.info("[HOOK] ✓ Keyboard hook DISABLED (zero delay mode)")

        # Start TCP server in background thread
        self.server_thread = threading.Thread(target=self._server_loop, daemon=True)
        self.server_thread.start()

        log.info(
            f"[VMwareReceiverIntegrated] ✅ TCP server starting in background thread (port {self.server_port})..."
        )

    def stop_tcp_server(self):
        """Stop TCP server"""
        if not self.running:
            log.debug("[VMwareReceiverIntegrated] TCP server is not running")
            return

        log.info("[VMwareReceiverIntegrated] Stopping TCP server...")
        self.running = False

        # Uninstall keyboard hook
        log.debug("[VMwareReceiverIntegrated] Uninstalling keyboard hook...")
        self.uninstall_hook()

        # Close client connection (thread-safe)
        old_client = None
        with self._stats_lock:
            if self.client_socket:
                old_client = self.client_socket
                self.client_socket = None
                self.client_address = None
        if old_client:
            try:
                log.debug("[VMwareReceiverIntegrated] Closing client connection...")
                old_client.close()
            except Exception as e:
                log.debug(f"[VMwareReceiverIntegrated] Error closing client: {e}")

        # Close server socket
        if self.server_socket:
            try:
                log.debug("[VMwareReceiverIntegrated] Closing server socket...")
                self.server_socket.close()
            except Exception as e:
                log.debug(
                    f"[VMwareReceiverIntegrated] Error closing server socket: {e}"
                )
            self.server_socket = None

        log.info("[VMwareReceiverIntegrated] ✅ TCP server stopped")

    def is_running(self) -> bool:
        """Check if TCP server is running"""
        return self.running

    def get_stats(self) -> dict:
        """Get statistics (thread-safe)"""
        # Bug fix: Thread-safe stats access
        with self._stats_lock:
            return self.stats.copy()

    def print_stats(self):
        """Print statistics"""
        log.info("\n=== VMWARE RECEIVER STATISTICS ===")
        log.info(f"Arduino connected: {self.shared_connection.is_connected()}")
        log.info(f"Client connected: {self.client_socket is not None}")
        log.info(f"Total received: {self.stats['total_received']}")
        log.info(f"Total forwarded: {self.stats['total_forwarded']}")
        log.info(f"Total errors: {self.stats['total_errors']}")
        log.info(f"Total clients: {self.stats['total_clients']}")
