"""
Host Sender - Mirror keyboard input từ Host đến VMware qua TCP
Nhận keyboard input thực và gửi qua TCP đến VMware receiver
"""

import ctypes
import ctypes.wintypes
import json
import os
import socket
import sys
import threading
import time
import tkinter as tk
import tkinter.font as tkfont
import winsound
from ctypes import wintypes
from typing import Any, Callable, Dict, List, Optional

# Windows API constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
HC_ACTION = 0
PM_REMOVE = 0x0001

# Compat: some Python builds lack wintypes.ULONG_PTR
if not hasattr(wintypes, "ULONG_PTR"):
    wintypes.ULONG_PTR = wintypes.WPARAM

# Ensure console can print UTF-8
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

# Virtual Key Codes mapping to Arduino key names
# Full keyboard layout support - all keys will be mirrored
VK_TO_KEY = {
    # Control keys
    0x08: "backspace",
    0x09: "tab",
    0x0D: "enter",
    0x10: "shift",
    0x11: "ctrl",
    0x12: "alt",
    0x14: "caps",
    0x1B: "esc",
    0x20: "space",
    # Navigation keys
    0x21: "pgup",
    0x22: "pgdn",
    0x23: "end",
    0x24: "home",
    0x25: "left",
    0x26: "up",
    0x27: "right",
    0x28: "down",
    0x2D: "insert",
    0x2E: "delete",
    # Numbers (top row)
    0x30: "0",
    0x31: "1",
    0x32: "2",
    0x33: "3",
    0x34: "4",
    0x35: "5",
    0x36: "6",
    0x37: "7",
    0x38: "8",
    0x39: "9",
    # Letters (A-Z)
    0x41: "a",
    0x42: "b",
    0x43: "c",
    0x44: "d",
    0x45: "e",
    0x46: "f",
    0x47: "g",
    0x48: "h",
    0x49: "i",
    0x4A: "j",
    0x4B: "k",
    0x4C: "l",
    0x4D: "m",
    0x4E: "n",
    0x4F: "o",
    0x50: "p",
    0x51: "q",
    0x52: "r",
    0x53: "s",
    0x54: "t",
    0x55: "u",
    0x56: "v",
    0x57: "w",
    0x58: "x",
    0x59: "y",
    0x5A: "z",
    # Function keys (F1-F12)
    0x70: "f1",
    0x71: "f2",
    0x72: "f3",
    0x73: "f4",
    0x74: "f5",
    0x75: "f6",
    0x76: "f7",
    0x77: "f8",
    0x78: "f9",
    0x79: "f10",
    0x7A: "f11",
    0x7B: "f12",
    # System keys (Windows, Menu)
    0x5B: "l_gui",
    0x5C: "r_gui",
    0x5D: "menu",
    # Special keys
    0x2C: "printscreen",
    0x91: "scroll",
    0x13: "pause",
    0x90: "numlock",
    # Right modifiers (map to left equivalents for Arduino compatibility)
    0xA0: "shift",  # VK_LSHIFT / VK_RSHIFT -> 'shift'
    0xA1: "shift",  # VK_RSHIFT
    0xA2: "ctrl",  # VK_LCONTROL / VK_RCONTROL -> 'ctrl'
    0xA3: "ctrl",  # VK_RCONTROL
    0xA4: "alt",  # VK_LMENU / VK_RMENU -> 'alt'
    0xA5: "alt",  # VK_RMENU
    # Numpad keys
    0x60: "np0",
    0x61: "np1",
    0x62: "np2",
    0x63: "np3",
    0x64: "np4",
    0x65: "np5",
    0x66: "np6",
    0x67: "np7",
    0x68: "np8",
    0x69: "np9",
    0x6A: "np_mul",
    0x6B: "np_add",
    0x6D: "np_sub",
    0x6E: "np_dec",
    0x6F: "np_div",
    # Special characters (punctuation)
    0xBA: "semicolon",
    0xBB: "equals",
    0xBC: "comma",
    0xBD: "minus",
    0xBE: "period",
    0xBF: "slash",
    0xC0: "grave",
    0xDB: "lbracket",
    0xDC: "backslash",
    0xDD: "rbracket",
    0xDE: "quote",
}


class ReceiverSession:
    """Manage a single VMware receiver connection."""

    def __init__(self, host, config: Dict[str, Any]):
        self.host = host
        self.name = (
            config.get("name")
            or f"{config.get('vmware_ip', '?')}:{config.get('vmware_port', 12345)}"
        )
        self.vmware_ip = config.get("vmware_ip")
        self.vmware_port = int(config.get("vmware_port", 12345))
        self.reconnect_interval = float(config.get("reconnect_interval", 1.0))
        self.forwarding_enabled = bool(config.get("forwarding_enabled", True))
        self.auto_connect = config.get("auto_connect", True)
        self.enable_logging = config.get("enable_logging", host.enable_logging)

        self.socket: Optional[socket.socket] = None
        self.connected = False
        self.connecting = False
        self.desired_connection = bool(self.auto_connect)
        self.running = True

        self.stats = {
            "total_sent": 0,
            "total_errors": 0,
            "total_reconnects": 0,
        }

        self._ui_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        self._lock = threading.Lock()
        self._loop_thread = threading.Thread(target=self._connection_loop, daemon=True)
        self._loop_thread.start()

    # ------------------------------------------------------------------ utils
    def _notify_ui(self):
        if self._ui_callback:
            state = self.get_state_snapshot()
            self.host.call_in_gui_thread(self._ui_callback, state)

    def register_ui_callback(self, callback: Callable[[Dict[str, Any]], None]):
        self._ui_callback = callback
        self._notify_ui()

    def get_state_snapshot(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "connected": self.connected,
            "connecting": self.connecting,
            "forwarding_enabled": self.forwarding_enabled,
            "desired_connection": self.desired_connection,
        }

    # ------------------------------------------------------------ loop/threads
    def _connection_loop(self):
        while self.running:
            if self.desired_connection and not self.connected and not self.connecting:
                self._attempt_connect()
            elif not self.desired_connection and self.connected:
                self._disconnect()
            time.sleep(self.reconnect_interval)

    def _attempt_connect(self):
        if not self.vmware_ip:
            self.host.log(f"[CONFIG] Receiver '{self.name}' missing vmware_ip")
            self.desired_connection = False
            self._notify_ui()
            return

        self.connecting = True
        self._notify_ui()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5.0)
            sock.connect((self.vmware_ip, self.vmware_port))
            sock.settimeout(None)
            with self._lock:
                self.socket = sock
                self.connected = True
                self.stats["total_reconnects"] += 1
            self.host.log(
                f"[{self.name}] Connected to {self.vmware_ip}:{self.vmware_port}"
            )
        except Exception as exc:
            self.host.log(f"[{self.name}] Connect error: {exc}")
            with self._lock:
                if self.socket:
                    try:
                        self.socket.close()
                    except Exception:
                        pass
                    self.socket = None
                self.connected = False
        finally:
            self.connecting = False
            self._notify_ui()

    def _disconnect(self):
        with self._lock:
            if self.socket:
                try:
                    self.socket.close()
                except Exception:
                    pass
            self.socket = None
            was_connected = self.connected
            self.connected = False
        if was_connected:
            self.host.log(f"[{self.name}] Disconnected")
        self._notify_ui()

    # ---------------------------------------------------------------- commands
    def toggle_connection(self):
        self.desired_connection = not self.desired_connection
        if not self.desired_connection:
            self._disconnect()
        self._notify_ui()

    def toggle_forwarding(self):
        self.forwarding_enabled = not self.forwarding_enabled
        self._notify_ui()

    def send_key(self, key: str, action: str) -> bool:
        with self._lock:
            sock = self.socket
        if not self.connected or sock is None:
            return False
        try:
            command = f"{action}:{key}\n"
            sock.sendall(command.encode("utf-8"))
            self.stats["total_sent"] += 1
            return True
        except Exception as exc:
            self.stats["total_errors"] += 1
            self.host.log(f"[{self.name}] Send error: {exc}")
            self.connected = False
            self._notify_ui()
            return False

    def send_command(self, text: str) -> bool:
        with self._lock:
            sock = self.socket
        if not self.connected or sock is None:
            self.host.log(f"[{self.name}] Cannot send '{text.strip()}': not connected")
            return False
        try:
            payload = f"{text.strip()}\n"
            sock.sendall(payload.encode("utf-8"))
            return True
        except Exception as exc:
            self.stats["total_errors"] += 1
            self.host.log(f"[{self.name}] Command send error: {exc}")
            self.connected = False
            self._notify_ui()
            return False

    def send_all_up(self):
        with self._lock:
            sock = self.socket
        if not self.connected or sock is None:
            return
        try:
            sock.sendall(b"all_up\n")
        except Exception:
            self.connected = False
            self._notify_ui()

    def stop(self):
        self.running = False
        self.desired_connection = False
        self._disconnect()
        if self._loop_thread.is_alive():
            self._loop_thread.join(timeout=1.0)

    def to_config(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "vmware_ip": self.vmware_ip,
            "vmware_port": self.vmware_port,
            "reconnect_interval": self.reconnect_interval,
            "forwarding_enabled": self.forwarding_enabled,
            "auto_connect": self.desired_connection,
        }


class ReceiverRow(tk.Frame):
    """GUI row for a receiver session."""

    def __init__(self, master, session: ReceiverSession):
        super().__init__(master, bd=1, relief=tk.GROOVE, padx=8, pady=6)
        self.session = session
        self.label = tk.Label(self, text=session.name, font=("Segoe UI", 10, "bold"))
        self.label.grid(row=0, column=0, sticky="w", padx=(0, 10))

        self.toggle_bot_btn = tk.Button(
            self,
            text="Toggle Bot",
            bg="#2563eb",
            fg="white",
            width=12,
            command=self._on_toggle_bot,
        )
        self.toggle_bot_btn.grid(row=0, column=1, padx=4)

        self.mirror_btn = tk.Button(
            self,
            text="Mirror ON",
            bg="#16a34a",
            fg="white",
            width=12,
            command=self._on_toggle_mirror,
        )
        self.mirror_btn.grid(row=0, column=2, padx=4)

        self.connect_btn = tk.Button(
            self,
            text="Connect",
            bg="#dc2626",
            fg="white",
            width=14,
            command=self._on_toggle_connection,
        )
        self.connect_btn.grid(row=0, column=3, padx=4)

        self.status_label = tk.Label(self, text="", fg="gray")
        self.status_label.grid(row=1, column=0, columnspan=4, sticky="w", pady=(4, 0))

        session.register_ui_callback(self.update_state)

    def update_state(self, state: Dict[str, Any]):
        forwarding = state.get("forwarding_enabled", False)
        connected = state.get("connected", False)
        connecting = state.get("connecting", False)
        desired = state.get("desired_connection", False)

        self.mirror_btn.configure(
            text="Mirror ON" if forwarding else "Mirror OFF",
            bg="#16a34a" if forwarding else "#f97316",
        )

        if connecting:
            self.connect_btn.configure(
                text="Connecting...", state=tk.DISABLED, bg="#facc15"
            )
        else:
            self.connect_btn.configure(
                text="Disconnect" if connected else "Connect",
                state=tk.NORMAL,
                bg="#16a34a" if connected else "#dc2626",
            )

        if connected:
            status = "Connected"
        elif connecting:
            status = "Connecting..."
        else:
            status = "Disconnected"
        status += " | Mirror ON" if forwarding else " | Mirror OFF"
        status += " | Auto" if desired else " | Manual"
        self.status_label.configure(text=status)

    def _on_toggle_bot(self):
        if not self.session.send_command("command:toggle_bot"):
            print(f"[TOGGLE] Failed to trigger toggle on {self.session.name}.")

    def _on_toggle_mirror(self):
        self.session.toggle_forwarding()

    def _on_toggle_connection(self):
        self.session.toggle_connection()


def configure_high_dpi_scaling(widget: tk.Misc, scale: float = 1.4) -> None:
    """Best-effort DPI awareness & font scaling for high-resolution displays."""
    try:
        if sys.platform.startswith("win"):
            ctypes.windll.shcore.SetProcessDpiAwareness(2)
    except Exception:
        pass

    try:
        widget.tk.call("tk", "scaling", scale)
    except tk.TclError:
        pass

    try:
        for name in (
            "TkDefaultFont",
            "TkTextFont",
            "TkFixedFont",
            "TkMenuFont",
            "TkHeadingFont",
            "TkTooltipFont",
        ):
            try:
                font = tkfont.nametofont(name)
                font.configure(size=max(10, int(font.cget("size") * scale / 1.1)))
            except tk.TclError:
                continue
    except Exception:
        pass


class HostSenderGUI(tk.Tk):
    """Simple Tkinter GUI to manage multiple VMware receivers."""

    def __init__(self, host, sessions: List[ReceiverSession]):
        super().__init__()
        configure_high_dpi_scaling(self)
        self.host = host
        self.sessions = sessions
        self.title("Host Sender - Multi VMware Controller")
        self.geometry("620x{}".format(max(140, 100 + len(sessions) * 80)))
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        header = tk.Label(
            self,
            text="VMware Receivers",
            font=("Segoe UI", 12, "bold"),
        )
        header.pack(pady=(10, 6))

        container = tk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        for session in sessions:
            row = ReceiverRow(container, session)
            row.pack(fill="x", pady=4)

    def _on_close(self):
        self.host.stop()
        self.destroy()


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    ]


class HostSender:
    """Mirror hardware input to multiple VMware receivers with GUI control."""

    def __init__(
        self,
        vmware_ip: str = None,
        vmware_port: int = 12345,
        reconnect_interval: float = 1.0,
        enable_logging: bool = False,
        block_original_input: bool = False,
        forwarding_enabled: bool = True,
    ):
        self.cli_override_ip = vmware_ip
        self.cli_override_port = vmware_port
        self.cli_override_reconnect = reconnect_interval

        self.enable_logging = enable_logging
        self.block_original_input = block_original_input
        self.global_forwarding_enabled = forwarding_enabled

        self.sessions: List[ReceiverSession] = []
        self.receiver_configs: List[Dict[str, Any]] = []
        self.running = False
        self.gui_root: Optional[HostSenderGUI] = None

        # Keyboard hook
        self.hook = None
        self.user32 = None
        self.kernel32 = None
        self.hook_thread: Optional[threading.Thread] = None
        self._hook_running = threading.Event()

        # Key state tracking
        self.key_states = {}
        self.key_states_lock = threading.Lock()

        # Hotkeys
        self.VK_PGDN = 0x22  # Page Down -> toggle blocking
        self.VK_PGUP = 0x21  # Page Up -> toggle global forwarding
        self.VK_HOME = 0x24  # Home -> show stats

        # Stats
        self.stats = {
            "total_hardware_keys": 0,
            "total_unmapped": 0,
        }

        # Config
        self.CONFIG_PATH = os.path.join(
            os.path.dirname(__file__), "host_sender.config.json"
        )
        self._config_snapshot: Dict[str, Any] = {}
        self._load_config()
        self._create_sessions()

        # Initialize Windows API / hook definitions
        self._init_windows_api()

    # ------------------------------------------------------------------ Config
    def log(self, message: str):
        if self.enable_logging:
            print(message)

    def call_in_gui_thread(self, func: Callable, *args, **kwargs):
        if self.gui_root and self.gui_root.winfo_exists():
            self.gui_root.after(0, lambda: func(*args, **kwargs))

    def _create_sessions(self):
        self.sessions = []
        for cfg in self.receiver_configs:
            session = ReceiverSession(self, cfg)
            self.sessions.append(session)

    def _load_config(self):
        data: Dict[str, Any] = {}
        if os.path.exists(self.CONFIG_PATH):
            try:
                with open(self.CONFIG_PATH, "r", encoding="utf-8") as f:
                    data = json.load(f)
            except Exception as exc:
                print(f"[CONFIG] Failed to parse {self.CONFIG_PATH}: {exc}")

        settings = data.get("settings", {})
        self.enable_logging = settings.get("enable_logging", self.enable_logging)
        self.block_original_input = settings.get(
            "block_original_input", self.block_original_input
        )
        self.global_forwarding_enabled = settings.get(
            "forwarding_enabled", self.global_forwarding_enabled
        )

        receivers = data.get("receivers")
        if not isinstance(receivers, list):
            # Back-compat: single receiver format
            legacy_entry = {
                "name": data.get("name"),
                "vmware_ip": data.get("vmware_ip"),
                "vmware_port": data.get("vmware_port", self.cli_override_port or 12345),
                "reconnect_interval": data.get(
                    "reconnect_interval", self.cli_override_reconnect or 1.0
                ),
                "forwarding_enabled": data.get("forwarding_enabled", True),
                "auto_connect": True,
            }
            receivers = [legacy_entry] if legacy_entry.get("vmware_ip") else []

        if self.cli_override_ip:
            override = {
                "name": receivers[0].get("name") if receivers else "Receiver 1",
                "vmware_ip": self.cli_override_ip,
                "vmware_port": self.cli_override_port,
                "reconnect_interval": self.cli_override_reconnect,
                "forwarding_enabled": True,
                "auto_connect": True,
            }
            if receivers:
                receivers[0].update(
                    {k: v for k, v in override.items() if v is not None}
                )
            else:
                receivers.append(override)

        self.receiver_configs = receivers or []
        self._config_snapshot = {
            "settings": {
                "enable_logging": self.enable_logging,
                "block_original_input": self.block_original_input,
                "forwarding_enabled": self.global_forwarding_enabled,
            },
            "receivers": self.receiver_configs,
        }

    def _save_config(self):
        payload = {
            "settings": {
                "enable_logging": self.enable_logging,
                "block_original_input": self.block_original_input,
                "forwarding_enabled": self.global_forwarding_enabled,
            },
            "receivers": [session.to_config() for session in self.sessions],
        }
        if payload == self._config_snapshot:
            return
        try:
            with open(self.CONFIG_PATH, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=4)
            self._config_snapshot = payload
        except Exception as exc:
            print(f"[CONFIG] Save error: {exc}")

    # ------------------------------------------------------------- Hook/WinAPI
    def _init_windows_api(self):
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
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

        self.user32.CallNextHookEx.argtypes = [
            wintypes.HHOOK,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self.user32.CallNextHookEx.restype = ctypes.c_int

        self.user32.UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
        self.user32.UnhookWindowsHookEx.restype = wintypes.BOOL

        self.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        self.kernel32.GetModuleHandleW.restype = wintypes.HINSTANCE

        self.user32.PeekMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
            wintypes.UINT,
        ]
        self.user32.PeekMessageW.restype = wintypes.BOOL
        self.user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
        self.user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]

        self.user32.PostQuitMessage.argtypes = [ctypes.c_int]
        self.user32.PostQuitMessage.restype = None
        self.HOOKPROC = HOOKPROC

    def _install_hook(self):
        self.hook_proc = self.HOOKPROC(self._low_level_keyboard_proc)
        module_handle = self.kernel32.GetModuleHandleW(None)
        self.hook = self.user32.SetWindowsHookExW(
            WH_KEYBOARD_LL, self.hook_proc, module_handle, 0
        )
        if not self.hook:
            error_code = self.kernel32.GetLastError()
            raise RuntimeError(
                f"Failed to install keyboard hook. Error code: {error_code}"
            )
        print("[HOOK] Keyboard hook installed")

    def _hook_loop(self):
        try:
            self._install_hook()
        except Exception as exc:
            print(f"[HOOK] Failed to install keyboard hook: {exc}")
            return

        msg = wintypes.MSG()
        while self._hook_running.is_set():
            ret = self.user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, PM_REMOVE)
            if ret:
                if msg.message == 0x0012:  # WM_QUIT
                    break
                self.user32.TranslateMessage(ctypes.byref(msg))
                self.user32.DispatchMessageW(ctypes.byref(msg))
            else:
                time.sleep(0.001)

        if self.hook:
            self.user32.UnhookWindowsHookEx(self.hook)
            self.hook = None
            print("[HOOK] Keyboard hook removed")

    # ----------------------------------------------------------- Input routing
    def _update_key_state(self, key_name: str, is_down: bool) -> bool:
        with self.key_states_lock:
            current = self.key_states.get(key_name, False)
            if is_down and current:
                return False
            if not is_down and not current:
                return False
            self.key_states[key_name] = is_down
            return True

    def _broadcast_key(self, key: str, action: str):
        if not self.global_forwarding_enabled:
            return
        for session in self.sessions:
            if session.forwarding_enabled:
                session.send_key(key, action)

    def _broadcast_all_up(self):
        for session in self.sessions:
            session.send_all_up()

    def _handle_hotkey(self, vk_code: int) -> bool:
        if vk_code == self.VK_PGDN:
            self.block_original_input = not self.block_original_input
            status = "BLOCK" if self.block_original_input else "PASS"
            print(f"[HOTKEY] PageDown → Block original input: {status}")
            winsound.Beep(800 if self.block_original_input else 400, 150)
            self._save_config()
            return True
        return False

    def _track_hardware_event(self, message: int):
        if message in (WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, WM_SYSKEYUP):
            self.stats["total_hardware_keys"] += 1

    def _forward_key(self, key_name: str, message: int):
        if not self.global_forwarding_enabled:
            return
        if message in (WM_KEYDOWN, WM_SYSKEYDOWN):
            if self._update_key_state(key_name, True):
                self._broadcast_key(key_name, "down")
        if message in (WM_KEYUP, WM_SYSKEYUP):
            if self._update_key_state(key_name, False):
                self._broadcast_key(key_name, "up")

    def _low_level_keyboard_proc(self, n_code, w_param, l_param):
        if n_code >= HC_ACTION:
            kb_data = ctypes.cast(l_param, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk_code = kb_data.vkCode

            if w_param in (WM_KEYDOWN, WM_SYSKEYDOWN) and self._handle_hotkey(vk_code):
                return 1

            key_name = VK_TO_KEY.get(vk_code)
            self._track_hardware_event(w_param)

            if key_name:
                self._forward_key(key_name, w_param)
            elif not key_name:
                self.stats["total_unmapped"] += 1
                self.log(f"[WARNING] Unmapped key: VK 0x{vk_code:02X}")

            if self.block_original_input:
                return 1

        return self.user32.CallNextHookEx(self.hook, n_code, w_param, l_param)

    def _print_statistics(self):
        print(f"\n{'=' * 50}")
        print("=== HOST SENDER STATS ===")
        print(f"Hardware keys captured: {self.stats['total_hardware_keys']}")
        print(f"Unmapped keys: {self.stats['total_unmapped']}")
        for session in self.sessions:
            state = "Connected" if session.connected else "Disconnected"
            print(
                f"- {session.name}: {state}, sent={session.stats['total_sent']}, "
                f"errors={session.stats['total_errors']}, reconnects={session.stats['total_reconnects']}"
            )
        print(f"{'=' * 50}\n")

    # ---------------------------------------------------------------- Lifecycle
    def start(self):
        if not self.sessions:
            print(
                "[WARN] No receivers configured. Update host_sender.config.json to add entries."
            )

        self.running = True
        self._hook_running.set()
        self.hook_thread = threading.Thread(target=self._hook_loop, daemon=True)
        self.hook_thread.start()

        print(
            "[START] Host sender running. Hotkeys: PageDown=Block input, PageUp=Toggle mirror, Home=Stats"
        )

        try:
            self.gui_root = HostSenderGUI(self, self.sessions)
            self.gui_root.mainloop()
        finally:
            self.stop()

    def stop(self):
        if not self.running:
            return
        self.running = False
        self._hook_running.clear()
        if self.hook_thread and self.hook_thread.is_alive():
            self.hook_thread.join(timeout=2.0)

        for session in self.sessions:
            session.stop()
        self._broadcast_all_up()
        self._save_config()
        if self.gui_root and self.gui_root.winfo_exists():
            self.gui_root.after(0, self.gui_root.destroy)
        print("[STOP] Host sender stopped.")

    # ------------------------------------------------------------ CLI helpers
    def run_cli(self):
        try:
            self.start()
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Keyboard interrupt received")
            self.stop()


def main():
    vmware_ip = None
    vmware_port = 12345
    enable_logging = False

    if len(sys.argv) > 1:
        vmware_ip = sys.argv[1]
    if len(sys.argv) > 2:
        vmware_port = int(sys.argv[2])
    if len(sys.argv) > 3:
        enable_logging = sys.argv[3].lower() in {"true", "1", "yes", "on"}

        sender = HostSender(
            vmware_ip=vmware_ip, vmware_port=vmware_port, enable_logging=enable_logging
        )
    sender.run_cli()


if __name__ == "__main__":
    main()
