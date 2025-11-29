"""
Mirror Input module: hooks hardware keyboard on host and forwards keys via TCP
to vmware_receiver.py (running inside VMware). Similar to host_sender.py but
integrated into Auto Maple workflow.
"""

import ctypes
import threading
import time
from typing import Dict, Optional

from ctypes import wintypes

from src.common.logger import get_logger
from src.common.tcp_key_client import TcpKeyClient

log = get_logger(__name__)

# Low-level keyboard hook constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
HC_ACTION = 0
PM_REMOVE = 0x0001

# Map VK codes to key strings (copied from host_sender)
VK_TO_KEY: Dict[int, str] = {
    0x08: "backspace",
    0x09: "tab",
    0x0D: "enter",
    0x10: "shift",
    0x11: "ctrl",
    0x12: "alt",
    0x14: "caps",
    0x1B: "esc",
    0x20: "space",
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
    0x2C: "printscreen",
    0x91: "scroll",
    0x13: "pause",
    0x90: "numlock",
    0xA0: "shift",
    0xA1: "shift",
    0xA2: "ctrl",
    0xA3: "ctrl",
    0xA4: "alt",
    0xA5: "alt",
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


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR),
    ]


class MirrorInput:
    """Manages hardware keyboard hook and forwarding to VMware."""

    def __init__(self):
        self.enabled = False
        self.block_original_input = False
        self.host = "127.0.0.1"
        self.port = 12345
        self.client: Optional[TcpKeyClient] = None
        self.hook = None
        self.hook_proc = None
        self.hook_thread: Optional[threading.Thread] = None
        self._hook_running = threading.Event()
        self._init_windows_api()
        self.key_states: Dict[str, bool] = {}
        self.lock = threading.Lock()
        self.last_error = ""
        self.connection_requested = False

    # ------------------------------------------------------------------ public
    def configure(self, host: str, port: int, block_input: bool):
        reconnect_needed = self.client is not None and (
            host != self.host or port != self.port
        )
        self.host = host
        self.port = port
        self.block_original_input = block_input
        if reconnect_needed:
            self.disconnect()
            if self.connection_requested:
                self.connect()

    def start(self):
        if self.enabled:
            return
        self.enabled = True
        self._hook_running.set()
        self.hook_thread = threading.Thread(target=self._hook_loop, daemon=True)
        self.hook_thread.start()
        log.info("Mirror input hook started (host=%s, port=%s)", self.host, self.port)

    def stop(self):
        if not self.enabled:
            return
        self.enabled = False
        self._hook_running.clear()
        if self.hook_thread and self.hook_thread.is_alive():
            self.hook_thread.join(timeout=1.0)
        self.hook_thread = None
        log.info("Mirror input hook stopped")

    def is_running(self):
        return self.enabled and self._hook_running.is_set()

    def connect(self):
        with self.lock:
            if self.client:
                self.connection_requested = True
                return True
            try:
                client = TcpKeyClient(self.host, self.port, auto_reconnect=True)
                client.start()
                self.client = client
                self.connection_requested = True
                log.info(
                    "Mirror input TCP connection requested (%s:%s)",
                    self.host,
                    self.port,
                )
                return True
            except Exception as exc:
                log.error("Mirror input: failed to start TCP client: %s", exc)
                self.client = None
                self.connection_requested = False
                return False

    def disconnect(self):
        with self.lock:
            client = self.client
            self.client = None
            self.connection_requested = False
        if client:
            try:
                client.send_all_up()
            except Exception:
                pass
            client.close()
            log.info("Mirror input TCP connection closed")

    def is_connected(self):
        with self.lock:
            client = self.client
        if not client:
            return False
        return bool(getattr(client, "connected", False))

    def shutdown(self):
        self.stop()
        self.disconnect()

    # ------------------------------------------------------------------ internals
    def _hook_loop(self):
        try:
            hook_proc = self.HOOKPROC(self._low_level_keyboard_proc)
            self.hook_proc = hook_proc
            module_handle = self.kernel32.GetModuleHandleW(None)
            self.hook = self.user32.SetWindowsHookExW(
                WH_KEYBOARD_LL, hook_proc, module_handle, 0
            )
            if not self.hook:
                error_code = ctypes.get_last_error()
                if error_code == 0:
                    error_code = self.kernel32.GetLastError()
                # Fallback attempt with hMod = None (some systems require)
                if error_code == 126:
                    self.hook = self.user32.SetWindowsHookExW(
                        WH_KEYBOARD_LL, hook_proc, 0, 0
                    )
                if not self.hook:
                    raise RuntimeError(f"SetWindowsHookEx failed ({error_code})")

            msg = wintypes.MSG()
            while self._hook_running.is_set():
                if self.user32.PeekMessageW(ctypes.byref(msg), 0, 0, 0, PM_REMOVE):
                    if msg.message == 0x0012:  # WM_QUIT
                        break
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageW(ctypes.byref(msg))
                else:
                    time.sleep(0.001)
        except Exception as exc:
            self.last_error = str(exc)
            log.error("Mirror input hook error: %s", exc, exc_info=True)
        finally:
            if self.hook:
                self.user32.UnhookWindowsHookEx(self.hook)
                self.hook = None
            self._hook_running.clear()
            self.enabled = False

    def _low_level_keyboard_proc(self, n_code, w_param, l_param):
        try:
            if n_code < HC_ACTION:
                result = self.user32.CallNextHookEx(self.hook, n_code, w_param, l_param)
                return result if result is not None else 0

            kb_data = ctypes.cast(
                ctypes.c_void_p(l_param), ctypes.POINTER(KBDLLHOOKSTRUCT)
            ).contents
            vk_code = kb_data.vkCode
            key_name = VK_TO_KEY.get(vk_code)

            if key_name:
                if w_param in (WM_KEYDOWN, WM_SYSKEYDOWN):
                    if self._update_key_state(key_name, True):
                        self._send_key("down", key_name)
                elif w_param in (WM_KEYUP, WM_SYSKEYUP):
                    if self._update_key_state(key_name, False):
                        self._send_key("up", key_name)
            if self.block_original_input and key_name:
                return 1
        except Exception as exc:
            log.debug("Mirror input hook exception: %s", exc)

        result = self.user32.CallNextHookEx(self.hook, n_code, w_param, l_param)
        return result if result is not None else 0

    # ------------------------------------------------------------------ helpers
    def _update_key_state(self, key: str, is_down: bool) -> bool:
        current = self.key_states.get(key, False)
        if is_down and current:
            return False
        if not is_down and not current:
            return False
        self.key_states[key] = is_down
        return True

    def _send_key(self, action: str, key: str):
        with self.lock:
            client = self.client
        if not client:
            return
        try:
            if action == "down":
                client.send_down(key)
            elif action == "up":
                client.send_up(key)
        except Exception as exc:
            log.debug("Mirror input send failed: %s", exc)

    def _init_windows_api(self):
        self.user32 = ctypes.WinDLL("user32", use_last_error=True)
        self.kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
        self.HOOKPROC = ctypes.WINFUNCTYPE(
            ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM
        )
        self.user32.PeekMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG),
            wintypes.HWND,
            wintypes.UINT,
            wintypes.UINT,
            wintypes.UINT,
        ]
        self.user32.PeekMessageW.restype = wintypes.BOOL
        self.user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
        self.user32.TranslateMessage.restype = wintypes.BOOL
        self.user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]
        try:
            lresult = wintypes.LRESULT
        except AttributeError:
            lresult = ctypes.c_long
        self.user32.DispatchMessageW.restype = lresult
        self.user32.CallNextHookEx.argtypes = [
            wintypes.HHOOK,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM,
        ]
        self.user32.CallNextHookEx.restype = ctypes.c_int
