"""
Simple keyboard hook to BLOCK Arduino simulate input only
Blocks Arduino input, allows hardware input to pass through
"""
import ctypes
import ctypes.wintypes
import time
import threading
import json
import os
import sys
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

# Virtual Key Codes mapping
VK_TO_KEY = {
    0x08: 'backspace', 0x09: 'tab', 0x0D: 'enter',
    0x10: 'shift', 0x11: 'ctrl', 0x12: 'alt',
    0x14: 'caps', 0x1B: 'esc', 0x20: 'space',
    0x21: 'pgup', 0x22: 'pgdn', 0x23: 'end',
    0x24: 'home', 0x25: 'left', 0x26: 'up',
    0x27: 'right', 0x28: 'down', 0x2D: 'insert',
    0x2E: 'delete',
    0x30: '0', 0x31: '1', 0x32: '2', 0x33: '3',
    0x34: '4', 0x35: '5', 0x36: '6', 0x37: '7',
    0x38: '8', 0x39: '9',
    0x41: 'a', 0x42: 'b', 0x43: 'c', 0x44: 'd',
    0x45: 'e', 0x46: 'f', 0x47: 'g', 0x48: 'h',
    0x49: 'i', 0x4A: 'j', 0x4B: 'k', 0x4C: 'l',
    0x4D: 'm', 0x4E: 'n', 0x4F: 'o', 0x50: 'p',
    0x51: 'q', 0x52: 'r', 0x53: 's', 0x54: 't',
    0x55: 'u', 0x56: 'v', 0x57: 'w', 0x58: 'x',
    0x59: 'y', 0x5A: 'z',
    0x70: 'f1', 0x71: 'f2', 0x72: 'f3', 0x73: 'f4',
    0x74: 'f5', 0x75: 'f6', 0x76: 'f7', 0x77: 'f8',
    0x78: 'f9', 0x79: 'f10', 0x7A: 'f11', 0x7B: 'f12',
    0x5B: 'l_gui', 0x5C: 'r_gui', 0x5D: 'menu',
    0x2C: 'printscreen', 0x91: 'scroll', 0x13: 'pause', 0x90: 'numlock',
    0x60: 'np0', 0x61: 'np1', 0x62: 'np2', 0x63: 'np3',
    0x64: 'np4', 0x65: 'np5', 0x66: 'np6', 0x67: 'np7',
    0x68: 'np8', 0x69: 'np9',
    0x6A: 'np_mul', 0x6B: 'np_add', 0x6D: 'np_sub',
    0x6E: 'np_dec', 0x6F: 'np_div',
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


class KeyboardBlockArduino:
    """Simple keyboard hook - BLOCK Arduino simulate input only"""
    
    def __init__(self, block_simulate_input=True, ignore_window_ms=200, enable_logging=False):
        self.hook = None
        self.running = False
        self.block_simulate_input = block_simulate_input
        self.ignore_window_ms = ignore_window_ms
        self.enable_logging = enable_logging
        
        # Track when we detect Arduino events (simulate input)
        # Track events we send to detect Arduino input loopback
        self.sent_events = {}  # {key_name: timestamp_ms}
        self.key_states = {}  # {key_name: (is_down, timestamp)}
        self.key_states_lock = threading.Lock()
        
        # Stats
        self.stats = {
            'total_events': 0,
            'arduino_blocked': 0,
            'hardware_allowed': 0
        }
        
        # Hotkeys
        self.VK_PGDN = 0x22  # Page Down -> toggle blocking
        self.VK_END = 0x23   # End -> exit
        
        # Config
        self.CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'keyboard_block_arduino.config.json')
        self._load_config()
        
        # Initialize Windows API
        self._init_windows_api()
    
    def _init_windows_api(self):
        """Initialize Windows API functions"""
        self.user32 = ctypes.windll.user32
        self.kernel32 = ctypes.windll.kernel32
        
        # Set up hook function signature
        HOOKPROC = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM
        )
        
        # Define SetWindowsHookExW
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
        self.user32.DispatchMessageW.restype = ctypes.LONG
    
    def _load_config(self):
        """Load config from JSON file"""
        try:
            if os.path.exists(self.CONFIG_PATH):
                with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    self.block_simulate_input = config.get('block_simulate_input', self.block_simulate_input)
                    self.ignore_window_ms = config.get('ignore_window_ms', self.ignore_window_ms)
                    self.enable_logging = config.get('enable_logging', self.enable_logging)
                    if self.enable_logging:
                        print(f"[CONFIG] Loaded: block_simulate_input={self.block_simulate_input}, "
                              f"ignore_window_ms={self.ignore_window_ms}")
        except Exception as e:
            if self.enable_logging:
                print(f"[CONFIG] Load error: {e}")
    
    def _save_config(self):
        """Save config to JSON file"""
        try:
            config = {
                'block_simulate_input': self.block_simulate_input,
                'ignore_window_ms': self.ignore_window_ms,
                'enable_logging': self.enable_logging
            }
            with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=4)
        except Exception as e:
            if self.enable_logging:
                print(f"[CONFIG] Save error: {e}")
    
    def _update_key_state(self, key_name, is_down):
        """Update key state and return True if state changed"""
        with self.key_states_lock:
            current_time = time.time()
            if is_down:
                if key_name in self.key_states and self.key_states[key_name][0]:
                    return False  # Already down
                self.key_states[key_name] = (True, current_time)
                return True
            else:
                if key_name in self.key_states and self.key_states[key_name][0]:
                    self.key_states[key_name] = (False, current_time)
                    return True
                return False  # Already up
    
    def _detect_arduino_event(self, key_name):
        """Detect if this event is from Arduino (simulate input)"""
        if not key_name:
            return False
        
        current_time_ms = int(time.perf_counter() * 1000)
        
        # Check if we recently detected this key (within ignore window)
        # This indicates Arduino input loopback
        if key_name in self.sent_events:
            time_since_sent = current_time_ms - self.sent_events[key_name]
            if time_since_sent < self.ignore_window_ms:
                return True
        
        # Fallback: Check if key was recently pressed and we have it in our state
        with self.key_states_lock:
            if key_name in self.key_states:
                state = self.key_states[key_name]
                is_down, timestamp = state[0], state[1]
                # If key was pressed very recently (within 500ms) and matches timing
                current_time_sec = current_time_ms / 1000.0
                if is_down and (current_time_sec - timestamp) < 0.5:
                    # This might be Arduino input - mark it
                    self.sent_events[key_name] = current_time_ms
                    return True
        
        return False
    
    def _mark_event_sent(self, key_name):
        """Mark that we detected this key (to detect Arduino loopback)"""
        if key_name:
            current_time_ms = int(time.perf_counter() * 1000)
            self.sent_events[key_name] = current_time_ms
    
    def _low_level_keyboard_proc(self, nCode, wParam, lParam):
        """Low-level keyboard hook procedure"""
        if nCode < HC_ACTION:
            return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)
        
        # Parse hook structure
        kbd = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
        vk_code = kbd.vkCode
        
        # Get key name
        key_name = VK_TO_KEY.get(vk_code)
        
        # Update stats
        self.stats['total_events'] += 1
        
        # Hotkey: Page Down -> toggle blocking
        if vk_code == self.VK_PGDN:
            if wParam == WM_KEYDOWN:
                self.block_simulate_input = not self.block_simulate_input
                print(f"\n[TOGGLE] Block simulate input: {self.block_simulate_input}")
                self._save_config()
                return 1  # Block hotkey itself
        
        # Hotkey: End -> exit
        if vk_code == self.VK_END:
            if wParam == WM_KEYDOWN:
                print("\n[EXIT] End key pressed - stopping...")
                self.running = False
                return 1  # Block hotkey itself
        
        # Detect Arduino events (simulate input)
        is_arduino_event = False
        if self.block_simulate_input:
            is_arduino_event = self._detect_arduino_event(key_name)
        
        # Update key state for hardware events
        if not is_arduino_event and key_name:
            if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
                self._update_key_state(key_name, True)
                self._mark_event_sent(key_name)  # Mark to detect loopback
            elif wParam in (WM_KEYUP, WM_SYSKEYUP):
                self._update_key_state(key_name, False)
        
        # Block Arduino events (simulate input), allow hardware input
        if self.block_simulate_input and is_arduino_event:
            self.stats['arduino_blocked'] += 1
            if self.enable_logging:
                print(f"[BLOCK] Arduino input blocked: {key_name}")
            return 1  # Block Arduino input
        
        # Allow hardware input to pass through
        self.stats['hardware_allowed'] += 1
        return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)
    
    def install_hook(self):
        """Install low-level keyboard hook"""
        HOOKPROC = ctypes.WINFUNCTYPE(
            ctypes.c_int,
            ctypes.c_int,
            wintypes.WPARAM,
            wintypes.LPARAM
        )
        
        self.hook_proc = HOOKPROC(self._low_level_keyboard_proc)
        hMod = self.kernel32.GetModuleHandleW(None)
        
        self.hook = self.user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            self.hook_proc,
            hMod,
            0
        )
        
        if not self.hook:
            error_code = self.kernel32.GetLastError()
            raise Exception(f"Failed to install hook. Error code: {error_code}")
        
        print(f"[HOOK] Keyboard hook installed (block_simulate_input={self.block_simulate_input})")
        print("[HOTKEYS] Page Down = toggle blocking, End = exit")
    
    def message_loop(self):
        """Windows message loop"""
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
        """Start blocking Arduino input"""
        try:
            self.install_hook()
            self.running = True
            
            print("\n[START] Blocking Arduino simulate input...")
            print("[INFO] Hardware input will pass through normally")
            print("[INFO] Press End to exit\n")
            
            self.message_loop()
        except KeyboardInterrupt:
            print("\n[INTERRUPT] Keyboard interrupt received")
        except Exception as e:
            print(f"\n[ERROR] Error in message loop: {e}")
            import traceback
            traceback.print_exc()
        finally:
            self.stop()
    
    def stop(self):
        """Stop and cleanup"""
        if self.hook:
            self.user32.UnhookWindowsHookEx(self.hook)
            self.hook = None
            print("[HOOK] Keyboard hook removed")
        
        # Print stats
        print("\n=== STATISTICS ===")
        print(f"Total events: {self.stats['total_events']}")
        print(f"Arduino blocked: {self.stats['arduino_blocked']}")
        print(f"Hardware allowed: {self.stats['hardware_allowed']}")
        
        # Save config
        self._save_config()


if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    block_input = True
    if len(sys.argv) > 1:
        block_input = sys.argv[1].lower() in ['true', '1', 'yes', 'on']
    
    ignore_window_ms = 200
    if len(sys.argv) > 2:
        ignore_window_ms = int(sys.argv[2])
    
    enable_logging = False
    if len(sys.argv) > 3:
        enable_logging = sys.argv[3].lower() in ['true', '1', 'yes', 'on']
    
    try:
        handler = KeyboardBlockArduino(
            block_simulate_input=block_input,
            ignore_window_ms=ignore_window_ms,
            enable_logging=enable_logging
        )
        handler.start()
    except Exception as e:
        import traceback
        print(f"\n=== INITIALIZATION ERROR ===")
        print(f"Error: {e}")
        print("\n=== Error Details ===")
        traceback.print_exc()
        print("\n=== End Error Details ===\n")
        input("Press Enter to close...")

