"""
Host Sender - Mirror keyboard input từ Host đến VMware qua TCP
Nhận keyboard input thực và gửi qua TCP đến VMware receiver
"""
import socket
import json
import os
import sys
import time
import threading
import ctypes
import ctypes.wintypes
import winsound
from typing import Optional
from ctypes import wintypes

# Windows API constants
WH_KEYBOARD_LL = 13
WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101
WM_SYSKEYDOWN = 0x0104
WM_SYSKEYUP = 0x0105
HC_ACTION = 0
PM_REMOVE = 0x0001

# Compat: some Python builds lack wintypes.ULONG_PTR
if not hasattr(wintypes, 'ULONG_PTR'):
    wintypes.ULONG_PTR = wintypes.WPARAM

# Ensure console can print UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# Virtual Key Codes mapping to Arduino key names
# Full keyboard layout support - all keys will be mirrored
VK_TO_KEY = {
    # Control keys
    0x08: 'backspace', 0x09: 'tab', 0x0D: 'enter',
    0x10: 'shift', 0x11: 'ctrl', 0x12: 'alt',
    0x14: 'caps', 0x1B: 'esc', 0x20: 'space',
    
    # Navigation keys
    0x21: 'pgup', 0x22: 'pgdn', 0x23: 'end',
    0x24: 'home', 0x25: 'left', 0x26: 'up',
    0x27: 'right', 0x28: 'down', 0x2D: 'insert',
    0x2E: 'delete',
    
    # Numbers (top row)
    0x30: '0', 0x31: '1', 0x32: '2', 0x33: '3',
    0x34: '4', 0x35: '5', 0x36: '6', 0x37: '7',
    0x38: '8', 0x39: '9',
    
    # Letters (A-Z)
    0x41: 'a', 0x42: 'b', 0x43: 'c', 0x44: 'd',
    0x45: 'e', 0x46: 'f', 0x47: 'g', 0x48: 'h',
    0x49: 'i', 0x4A: 'j', 0x4B: 'k', 0x4C: 'l',
    0x4D: 'm', 0x4E: 'n', 0x4F: 'o', 0x50: 'p',
    0x51: 'q', 0x52: 'r', 0x53: 's', 0x54: 't',
    0x55: 'u', 0x56: 'v', 0x57: 'w', 0x58: 'x',
    0x59: 'y', 0x5A: 'z',
    
    # Function keys (F1-F12)
    0x70: 'f1', 0x71: 'f2', 0x72: 'f3', 0x73: 'f4',
    0x74: 'f5', 0x75: 'f6', 0x76: 'f7', 0x77: 'f8',
    0x78: 'f9', 0x79: 'f10', 0x7A: 'f11', 0x7B: 'f12',
    
    # System keys (Windows, Menu)
    0x5B: 'l_gui', 0x5C: 'r_gui', 0x5D: 'menu',
    
    # Special keys
    0x2C: 'printscreen', 0x91: 'scroll', 0x13: 'pause', 0x90: 'numlock',
    
    # Right modifiers (map to left equivalents for Arduino compatibility)
    0xA0: 'shift',    # VK_LSHIFT / VK_RSHIFT -> 'shift'
    0xA1: 'shift',    # VK_RSHIFT
    0xA2: 'ctrl',     # VK_LCONTROL / VK_RCONTROL -> 'ctrl'
    0xA3: 'ctrl',     # VK_RCONTROL
    0xA4: 'alt',      # VK_LMENU / VK_RMENU -> 'alt'
    0xA5: 'alt',      # VK_RMENU
    
    # Numpad keys
    0x60: 'np0', 0x61: 'np1', 0x62: 'np2', 0x63: 'np3',
    0x64: 'np4', 0x65: 'np5', 0x66: 'np6', 0x67: 'np7',
    0x68: 'np8', 0x69: 'np9',
    0x6A: 'np_mul', 0x6B: 'np_add', 0x6D: 'np_sub',
    0x6E: 'np_dec', 0x6F: 'np_div',
    
    # Numpad Enter (map to regular enter)
    0x0A: 'enter',   # VK_CLEAR (numpad clear/enter)
    
    # Special characters (punctuation)
    0xBA: 'semicolon', 0xBB: 'equals', 0xBC: 'comma',
    0xBD: 'minus', 0xBE: 'period', 0xBF: 'slash',
    0xC0: 'grave', 0xDB: 'lbracket', 0xDC: 'backslash',
    0xDD: 'rbracket', 0xDE: 'quote'
}


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR)
    ]


class HostSender:
    """Mirror keyboard input từ Host đến VMware qua TCP"""
    
    def __init__(self, vmware_ip: str = None, vmware_port: int = 12345, 
                 reconnect_interval: float = 1.0, enable_logging: bool = False,
                 block_original_input: bool = False, forwarding_enabled: bool = True):
        self.vmware_ip = vmware_ip
        self.vmware_port = vmware_port
        self.reconnect_interval = reconnect_interval
        self.enable_logging = enable_logging
        self.block_original_input = block_original_input
        self.forwarding_enabled = forwarding_enabled
        
        self.socket: Optional[socket.socket] = None
        self.connected = False
        self.running = False
        
        # Keyboard hook
        self.hook = None
        self.user32 = None
        self.kernel32 = None
        
        # Key state tracking
        self.key_states = {}
        self.key_states_lock = threading.Lock()
        
        # Hotkeys
        self.VK_PGDN = 0x22  # Page Down -> toggle blocking
        self.VK_PGUP = 0x21  # Page Up -> toggle forwarding
        # VK_END removed - now handled by receiver for toggle remapping
        self.VK_HOME = 0x24  # Home -> show stats
        
        # Stats
        self.stats = {
            'total_hardware_keys': 0,
            'total_sent': 0,
            'total_errors': 0,
            'total_reconnects': 0,
            'total_unmapped': 0
        }
        
        # Config
        self.CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'host_sender.config.json')
        self._load_config()
        
        # Initialize Windows API
        self._init_windows_api()
        
        # Auto-reconnect thread
        self.reconnect_thread = None
    
    def _init_windows_api(self):
        """Initialize Windows API"""
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # Define SetWindowsHookExW signature
        HOOKPROC = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM
        )
        
        self.user32.SetWindowsHookExW.argtypes = [
            ctypes.c_int,
            HOOKPROC,
            wintypes.HINSTANCE,
            wintypes.DWORD
        ]
        self.user32.SetWindowsHookExW.restype = wintypes.HHOOK
        
        # Define CallNextHookEx
        self.user32.CallNextHookEx.argtypes = [
            wintypes.HHOOK,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM
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
            wintypes.UINT
        ]
        self.user32.PeekMessageW.restype = wintypes.BOOL
        
        # Define TranslateMessage and DispatchMessageW
        self.user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
        self.user32.TranslateMessage.restype = wintypes.BOOL
        
        self.user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]
        # DispatchMessageW.restype not set (returns default c_long on Windows)
        
        # Define PostQuitMessage
        self.user32.PostQuitMessage.argtypes = [ctypes.c_int]
        self.user32.PostQuitMessage.restype = None
        
        # Store hook proc type for later use
        self.HOOKPROC = HOOKPROC
    
    def _load_config(self):
        """Load config from JSON file"""
        try:
            if os.path.exists(self.CONFIG_PATH):
                with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.vmware_ip = config.get('vmware_ip', self.vmware_ip)
                    self.vmware_port = config.get('vmware_port', self.vmware_port)
                    self.reconnect_interval = config.get('reconnect_interval', self.reconnect_interval)
                    self.enable_logging = config.get('enable_logging', self.enable_logging)
                    self.block_original_input = config.get('block_original_input', self.block_original_input)
                    self.forwarding_enabled = config.get('forwarding_enabled', self.forwarding_enabled)
                    if self.enable_logging:
                        print(f"[CONFIG] Loaded: vmware_ip={self.vmware_ip}, "
                              f"vmware_port={self.vmware_port}, block_input={self.block_original_input}")
        except Exception as e:
            if self.enable_logging:
                print(f"[CONFIG] Load error: {e}")
    
    def _save_config(self):
        """Save config to JSON file"""
        try:
            config = {
                'vmware_ip': self.vmware_ip,
                'vmware_port': self.vmware_port,
                'reconnect_interval': self.reconnect_interval,
                'enable_logging': self.enable_logging,
                'block_original_input': self.block_original_input,
                'forwarding_enabled': self.forwarding_enabled
            }
            with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            if self.enable_logging:
                print(f"[CONFIG] Save error: {e}")
    
    def _update_key_state(self, key_name: str, is_down: bool) -> bool:
        """Update key state và return True nếu state changed"""
        with self.key_states_lock:
            if is_down:
                if key_name in self.key_states and self.key_states[key_name]:
                    return False  # Already down
                self.key_states[key_name] = True
                return True
            else:
                if key_name in self.key_states and self.key_states[key_name]:
                    self.key_states[key_name] = False
                    return True
                return False  # Already up
    
    def _low_level_keyboard_proc(self, nCode, wParam, lParam):
        """Low-level keyboard hook callback - capture keyboard input"""
        if nCode >= HC_ACTION:
            kb_data = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk_code = kb_data.vkCode
            
            # Hotkeys - MUST be checked BEFORE mapping to key names
            # This ensures hotkeys are not forwarded and are handled immediately
            if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
                if vk_code == self.VK_PGDN:
                    # Toggle block original input
                    self.block_original_input = not self.block_original_input
                    status = "ON (BLOCK)" if self.block_original_input else "OFF (PASS)"
                    print(f"[HOTKEY] PageDown → Block original input: {status}")
                    # Beep: High pitch for ON, Low pitch for OFF
                    if self.block_original_input:
                        winsound.Beep(800, 150)  # ON - Higher pitch
                    else:
                        winsound.Beep(400, 150)  # OFF - Lower pitch
                    self._save_config()
                    return 1  # Block hotkey - prevent forwarding
                elif vk_code == self.VK_PGUP:
                    # Toggle forwarding (mirror input on/off)
                    self.forwarding_enabled = not self.forwarding_enabled
                    status = "ENABLED" if self.forwarding_enabled else "DISABLED"
                    print(f"[HOTKEY] PageUp → Mirror input: {status}")
                    # Beep: High pitch for ON, Low pitch for OFF
                    if self.forwarding_enabled:
                        winsound.Beep(784, 333)  # G5 - Mirror ON
                    else:
                        winsound.Beep(523, 333)  # C5 - Mirror OFF
                    self._save_config()
                    return 1  # Block hotkey - prevent forwarding
                # End key removed - now handled by receiver for toggle remapping
                elif vk_code == self.VK_HOME:
                    # Show statistics
                    self._print_statistics()
                    winsound.Beep(600, 100)  # Quick beep for stats
                    return 1  # Block hotkey
            
            # Map VK code to key name
            key_name = VK_TO_KEY.get(vk_code)
            
            # Track hardware keyboard events
            if wParam in (WM_KEYDOWN, WM_KEYUP, WM_SYSKEYDOWN, WM_SYSKEYUP):
                self.stats['total_hardware_keys'] += 1
            
            # Process hardware input - forward via TCP (MIRROR mode)
            # ALWAYS forward ALL keys to receiver (full keyboard mirroring)
            # Backspace, Space, Alt, F1-F12, Arrow keys, and ALL other keys are mirrored
            if key_name and self.forwarding_enabled:
                if wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN:
                    if self._update_key_state(key_name, True):
                        success = self.send_key(key_name, 'down')
                        if success:
                            self.stats['total_sent'] += 1
                        else:
                            self.stats['total_errors'] += 1
                elif wParam == WM_KEYUP or wParam == WM_SYSKEYUP:
                    if self._update_key_state(key_name, False):
                        success = self.send_key(key_name, 'up')
                        if success:
                            self.stats['total_sent'] += 1
                        else:
                            self.stats['total_errors'] += 1
            elif not key_name:
                self.stats['total_unmapped'] += 1
                if self.enable_logging:
                    print(f"[WARNING] Unmapped key: VK 0x{vk_code:02X}")
            
            # ALWAYS allow original input to pass through (MIRROR mode)
            # Input is forwarded to VMware receiver AND passed through to Host
            # Set block_original_input=True in config if you want to block original input
            if self.block_original_input:
                return 1  # Block hardware input (only if explicitly enabled)
        
        # Allow input to pass through (default behavior - MIRROR mode)
        return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)
    
    def _print_statistics(self):
        """Print statistics"""
        print(f"\n{'='*50}")
        print("=== STATISTICS ===")
        print(f"{'='*50}")
        print(f"Connection: {'CONNECTED' if self.connected else 'DISCONNECTED'}")
        print(f"Hardware keys captured: {self.stats['total_hardware_keys']}")
        print(f"Total sent: {self.stats['total_sent']}")
        print(f"Total errors: {self.stats['total_errors']}")
        print(f"Total reconnects: {self.stats['total_reconnects']}")
        print(f"Unmapped keys: {self.stats['total_unmapped']}")
        if self.stats['total_hardware_keys'] > 0:
            sent_rate = (self.stats['total_sent'] / self.stats['total_hardware_keys'] * 100)
            print(f"Sent rate: {sent_rate:.1f}%")
        print(f"{'='*50}\n")
    
    def connect(self) -> bool:
        """Kết nối đến VMware receiver"""
        if not self.vmware_ip:
            print("[ERROR] VMware IP not set. Please configure vmware_ip in config file.")
            return False
        
        try:
            print(f"[CONNECT] Connecting to {self.vmware_ip}:{self.vmware_port}...")
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(5.0)  # 5s timeout for connect
            self.socket.connect((self.vmware_ip, self.vmware_port))
            self.socket.settimeout(None)  # No timeout after connect
            self.connected = True
            
            print(f"[CONNECT] ✓ Connected successfully to {self.vmware_ip}:{self.vmware_port}")
            return True
        except socket.timeout:
            print(f"[ERROR] Connection timeout to {self.vmware_ip}:{self.vmware_port}")
            print("[ERROR] Check if VMware receiver is running and firewall allows connection")
            self.connected = False
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            return False
        except Exception as e:
            print(f"[ERROR] Failed to connect to {self.vmware_ip}:{self.vmware_port}: {e}")
            print(f"[ERROR] Error type: {type(e).__name__}")
            self.connected = False
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            return False
    
    def disconnect(self):
        """Ngắt kết nối"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        print("[DISCONNECT] Disconnected from VMware")
    
    def _auto_reconnect_loop(self):
        """Auto-reconnect thread"""
        while self.running:
            if not self.connected:
                print(f"[RECONNECT] Attempting to reconnect... (next try in {self.reconnect_interval}s)")
                if self.connect():
                    self.stats['total_reconnects'] += 1
                    print(f"[RECONNECT] ✓ Reconnected successfully (total reconnects: {self.stats['total_reconnects']})")
            time.sleep(self.reconnect_interval)
    
    def send_key(self, key: str, action: str) -> bool:
        """
        Gửi key command đến VMware
        Args:
            key: Tên phím (vd: 'a', 'space', 'ctrl')
            action: 'down' hoặc 'up'
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.connected or not self.socket:
            if self.enable_logging:
                print(f"[ERROR] Not connected: {action}:{key}")
            return False
        
        try:
            command = f"{action}:{key}\n"
            bytes_sent = self.socket.send(command.encode('utf-8'))
            
            if bytes_sent == 0:
                if self.enable_logging:
                    print(f"[ERROR] Failed to send: {action}:{key}")
                self.connected = False
                return False
            
            self.stats['total_sent'] += 1
            if self.enable_logging:
                print(f"[SEND] {action}:{key} ({bytes_sent} bytes) → VMware")
            return True
            
        except Exception as e:
            print(f"[ERROR] Send error: {e}")
            self.connected = False
            self.stats['total_errors'] += 1
            return False
    
    def send_all_up(self) -> bool:
        """Gửi lệnh release tất cả keys"""
        if not self.connected or not self.socket:
            if self.enable_logging:
                print("[ERROR] Not connected: all_up")
            return False
        
        try:
            command = "all_up\n"
            bytes_sent = self.socket.send(command.encode('utf-8'))
            
            if bytes_sent == 0:
                if self.enable_logging:
                    print("[ERROR] Failed to send: all_up")
                self.connected = False
                return False
            
            self.stats['total_sent'] += 1
            if self.enable_logging:
                print(f"[SEND] all_up ({bytes_sent} bytes)")
            return True
            
        except Exception as e:
            print(f"[ERROR] Send error: {e}")
            self.connected = False
            self.stats['total_errors'] += 1
            return False
    
    def install_hook(self):
        """Install keyboard hook"""
        # Create hook proc callback (must store to prevent garbage collection)
        self.hook_proc = self.HOOKPROC(self._low_level_keyboard_proc)
        hMod = self.kernel32.GetModuleHandleW(None)
        
        self.hook = self.user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            self.hook_proc,
            hMod,
            0
        )
        
        if not self.hook:
            error_code = self.kernel32.GetLastError()
            raise Exception(f"Failed to install keyboard hook. Error code: {error_code}")
        
        print("[HOOK] Keyboard hook installed")
    
    def message_loop(self):
        """Windows message loop for keyboard hook"""
        msg = wintypes.MSG()
        
        while self.running:
            ret = self.user32.PeekMessageW(
                ctypes.byref(msg),
                None,
                0,
                0,
                PM_REMOVE
            )
            
            if ret:
                if msg.message == 0x0012:  # WM_QUIT
                    break
                else:
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageW(ctypes.byref(msg))
            else:
                time.sleep(0)  # Yield to other threads
    
    def start(self):
        """Bắt đầu sender với keyboard hook và auto-reconnect"""
        if not self.vmware_ip:
            print("[ERROR] VMware IP not configured. Please set vmware_ip in config file.")
            input("\nPress Enter to close...")
            return
        
        self.running = True
        
        print(f"\n[CONFIG] VMware IP: {self.vmware_ip}")
        print(f"[CONFIG] VMware Port: {self.vmware_port}")
        print(f"[CONFIG] Reconnect Interval: {self.reconnect_interval}s")
        print(f"[CONFIG] Block original input: {self.block_original_input} (MIRROR mode: forward + allow through)")
        print(f"[CONFIG] Forwarding enabled: {self.forwarding_enabled}")
        print(f"[CONFIG] Logging: {self.enable_logging}")
        
        # Initial connect
        print(f"\n[CONNECT] Attempting to connect to {self.vmware_ip}:{self.vmware_port}...")
        if not self.connect():
            print(f"[WARN] Initial connection failed. Auto-reconnect will attempt every {self.reconnect_interval}s")
        
        # Start auto-reconnect thread
        self.reconnect_thread = threading.Thread(target=self._auto_reconnect_loop, daemon=True)
        self.reconnect_thread.start()
        
        # Install keyboard hook
        try:
            self.install_hook()
            print("[START] Host sender started - mirroring keyboard input to VMware")
            print(f"[STATUS] Connection: {'CONNECTED' if self.connected else 'DISCONNECTED'}")
            print(f"[HOTKEYS] PageDown = toggle blocking, PageUp = toggle forwarding, Home = stats")
            print(f"[STATUS] Press Ctrl+C to exit\n")
            
            # Start message loop
            self.message_loop()
        except Exception as e:
            print(f"[ERROR] Failed to install keyboard hook: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop()
    
    def stop(self):
        """Dừng sender"""
        self.running = False
        
        # Remove keyboard hook
        if self.hook:
            self.user32.UnhookWindowsHookEx(self.hook)
            self.hook = None
            print("[HOOK] Keyboard hook removed")
        
        if self.reconnect_thread and self.reconnect_thread.is_alive():
            self.reconnect_thread.join(timeout=2.0)
        
        self.disconnect()
        
        # Release all keys
        if self.connected:
            self.send_all_up()
        
        # Print stats
        self._print_statistics()
        
        # Save config
        self._save_config()
    
    def print_stats(self):
        """Print statistics"""
        print("\n=== STATISTICS ===")
        print(f"Connected: {self.connected}")
        print(f"Total sent: {self.stats['total_sent']}")
        print(f"Total errors: {self.stats['total_errors']}")
        print(f"Total reconnects: {self.stats['total_reconnects']}")


# Example usage
if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    vmware_ip = None
    if len(sys.argv) > 1:
        vmware_ip = sys.argv[1]
    
    vmware_port = 12345
    if len(sys.argv) > 2:
        vmware_port = int(sys.argv[2])
    
    enable_logging = False
    if len(sys.argv) > 3:
        enable_logging = sys.argv[3].lower() in ['true', '1', 'yes', 'on']
    
    try:
        sender = HostSender(vmware_ip=vmware_ip, vmware_port=vmware_port, enable_logging=enable_logging)
        sender.start()
        
    except KeyboardInterrupt:
        print("\n[INTERRUPT] Keyboard interrupt received")
        if 'sender' in locals():
            sender.stop()
        print("[EXIT] Shutting down...")
    except Exception as e:
        import traceback
        print(f"\n{'='*50}")
        print(f"=== INITIALIZATION ERROR ===")
        print(f"{'='*50}")
        print(f"Error: {e}")
        print(f"Error type: {type(e).__name__}")
        print(f"\n=== Error Details ===")
        traceback.print_exc()
        print(f"=== End Error Details ===\n")
        print(f"{'='*50}\n")
        input("Press Enter to close...")

