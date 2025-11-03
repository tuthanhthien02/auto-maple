"""
Keyboard Hook để nhận input từ Multiplicity và forward qua Arduino Pro Micro
"""
import ctypes
import ctypes.wintypes
import serial
import serial.tools.list_ports
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

# Ensure console can print UTF-8 without errors (Windows cp1252 consoles)
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except Exception:
    pass

# Virtual Key Codes mapping to Arduino key names
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
    
    # System / modifiers
    0x5B: 'l_gui',      # Left Windows (GUI)
    0x5C: 'r_gui',      # Right Windows (GUI)
    0x5D: 'menu',       # Application/Menu key
    0x2C: 'printscreen',
    0x91: 'scroll',
    0x13: 'pause',
    0x90: 'numlock',

    # Numpad (map name; Arduino có thể fallback sang hàng số)
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


class KeyboardToArduino:
    def __init__(self, com_port=None, baudrate=9600, block_original_input=True, 
                 stuck_key_timeout=10.0, enable_logging=False):
        self.serial = None
        self.hook = None
        self.running = False
        self.com_port = com_port
        self.baudrate = baudrate
        self.block_original_input = block_original_input  # Block input gốc để chỉ forward qua Arduino
        self.stuck_key_timeout = stuck_key_timeout  # Timeout để auto-release stuck keys (giây)
        self.enable_logging = enable_logging  # Log key events để debug
        
        # Key state tracking: {key_name: (is_down: bool, down_timestamp: float)}
        self.key_states = {}
        self.key_states_lock = threading.Lock()  # Thread-safe access
        
        # Stuck key monitor thread
        self.stuck_key_monitor_thread = None

        # Runtime toggles
        self.forwarding_enabled = True  # Toggle forward to Arduino on/off

        # Safety hotkeys (VK codes)
        self.VK_PGDN = 0x22        # Page Down -> toggle blocking
        self.VK_PGUP = 0x21        # Page Up   -> toggle forwarding
        self.VK_END = 0x23         # End       -> exit
        
        # Config persistence
        self.CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'keyboard_to_arduino.config.json')
        self._load_config()
        
        # Initialize Windows API (must be called before using user32/kernel32)
        self._init_windows_api()

    def _print_status(self):
        block_status = "ON (BLOCK)" if self.block_original_input else "OFF (PASS)"
        fwd_status = "ENABLED" if self.forwarding_enabled else "DISABLED"
        print(f"[STATUS] Block original input: {block_status} | Forwarding: {fwd_status}")

    def _load_config(self):
        try:
            if os.path.exists(self.CONFIG_PATH):
                with open(self.CONFIG_PATH, 'r', encoding='utf-8') as f:
                    cfg = json.load(f)
                # Only set if provided (keep constructor defaults/CLI otherwise)
                self.com_port = cfg.get('com_port', self.com_port)
                self.baudrate = cfg.get('baudrate', self.baudrate)
                self.block_original_input = cfg.get('block_original_input', self.block_original_input)
                self.forwarding_enabled = cfg.get('forwarding_enabled', self.forwarding_enabled)
                self.stuck_key_timeout = cfg.get('stuck_key_timeout', self.stuck_key_timeout)
                self.enable_logging = cfg.get('enable_logging', self.enable_logging)
        except Exception as e:
            print(f"[CONFIG] Lỗi load cấu hình: {e}")

    def _init_windows_api(self):
        """Initialize Windows API libraries and function signatures"""
        # Load Windows API
        self.user32 = ctypes.WinDLL('user32', use_last_error=True)
        self.kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        
        # Define function signatures
        self.user32.SetWindowsHookExW.argtypes = [
            ctypes.c_int, ctypes.c_void_p, wintypes.HINSTANCE, wintypes.DWORD
        ]
        self.user32.SetWindowsHookExW.restype = wintypes.HHOOK
        
        self.user32.CallNextHookEx.argtypes = [
            wintypes.HHOOK, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM
        ]
        self.user32.CallNextHookEx.restype = ctypes.c_int
        
        self.user32.UnhookWindowsHookEx.argtypes = [wintypes.HHOOK]
        self.user32.UnhookWindowsHookEx.restype = wintypes.BOOL
        
        self.user32.GetMessageW.argtypes = [
            ctypes.POINTER(wintypes.MSG), wintypes.HWND, wintypes.UINT, wintypes.UINT
        ]
        self.user32.GetMessageW.restype = wintypes.BOOL
        
        self.user32.TranslateMessage.argtypes = [ctypes.POINTER(wintypes.MSG)]
        self.user32.DispatchMessageW.argtypes = [ctypes.POINTER(wintypes.MSG)]
        
        # PostQuitMessage signature
        self.user32.PostQuitMessage.argtypes = [ctypes.c_int]
        self.user32.PostQuitMessage.restype = None
        
        # GetModuleHandleW signature
        self.kernel32.GetModuleHandleW.argtypes = [wintypes.LPCWSTR]
        self.kernel32.GetModuleHandleW.restype = wintypes.HINSTANCE
        
        # GetLastError signature
        self.kernel32.GetLastError.argtypes = []
        self.kernel32.GetLastError.restype = wintypes.DWORD
        
        # FormatMessageW signature for error message formatting
        self.kernel32.FormatMessageW.argtypes = [
            wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD,
            ctypes.POINTER(wintypes.LPWSTR), wintypes.DWORD, ctypes.c_void_p
        ]
        self.kernel32.FormatMessageW.restype = wintypes.DWORD
        
        # LocalFree signature
        self.kernel32.LocalFree.argtypes = [ctypes.c_void_p]
        self.kernel32.LocalFree.restype = ctypes.c_void_p
        
        # Hook callback type
        HOOKPROC = ctypes.WINFUNCTYPE(
            ctypes.c_int, ctypes.c_int, wintypes.WPARAM, wintypes.LPARAM
        )
        self.hook_proc = HOOKPROC(self.low_level_keyboard_proc)
    
    def _save_config(self):
        try:
            cfg = {
                'com_port': self.com_port,
                'baudrate': self.baudrate,
                'block_original_input': self.block_original_input,
                'forwarding_enabled': self.forwarding_enabled,
                'stuck_key_timeout': self.stuck_key_timeout,
                'enable_logging': self.enable_logging,
            }
            with open(self.CONFIG_PATH, 'w', encoding='utf-8') as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[CONFIG] Lỗi lưu cấu hình: {e}")
    
    def find_arduino_port(self):
        """Tự động tìm Arduino Pro Micro port"""
        ports = serial.tools.list_ports.comports()
        for port in ports:
            # Arduino Pro Micro thường có VID:PID hoặc description
            if 'arduino' in port.description.lower() or \
               'pro micro' in port.description.lower() or \
               'USB Serial' in port.description:
                return port.device
        # Nếu không tìm thấy, list tất cả ports
        print("Không tìm thấy Arduino tự động. Các COM ports có sẵn:")
        for port in ports:
            print(f"  - {port.device}: {port.description}")
        return None
    
    def connect_arduino(self):
        """Kết nối với Arduino"""
        if not self.com_port:
            self.com_port = self.find_arduino_port()
        
        if not self.com_port:
            raise RuntimeError("Không tìm thấy Arduino. Vui lòng chỉ định COM port.")
        
        try:
            self.serial = serial.Serial(self.com_port, self.baudrate, timeout=1)
            time.sleep(2)  # Đợi Arduino khởi động
            print(f"Đã kết nối với Arduino tại {self.com_port}")
            # Đồng bộ trạng thái: release tất cả keys trên Arduino
            self.send_all_up()
            return True
        except Exception as e:
            print(f"Lỗi kết nối Arduino: {e}")
            return False
    
    def send_key_to_arduino(self, key_name, action):
        """
        Gửi command đến Arduino
        Format: <action>:<key>\n
        action: 'down' hoặc 'up'
        key: tên phím
        """
        if not self.serial or not self.serial.is_open:
            return
        
        try:
            command = f"{action}:{key_name}\n"
            self.serial.write(command.encode('utf-8'))
            
            if self.enable_logging:
                print(f"[LOG] Sent: {action}:{key_name}")
        except Exception as e:
            print(f"Lỗi gửi command: {e}")
            # Nếu lỗi, release key để tránh stuck
            self._release_key_safe(key_name)
            # Thử reconnect
            self._reconnect_loop()

    def send_all_up(self):
        try:
            if self.serial and self.serial.is_open:
                self.serial.write(b"all_up\n")
                if self.enable_logging:
                    print("[LOG] Sent: all_up")
        except Exception as e:
            print(f"Lỗi gửi all_up: {e}")
            self._reconnect_loop()

    def _reconnect_loop(self, retry_delay=2.0):
        """Thử reconnect Arduino cho đến khi thành công hoặc script dừng"""
        if not self.running:
            return
        print("[RECONNECT] Mất kết nối Arduino. Đang thử reconnect...")
        # Đóng cổng cũ nếu còn mở
        try:
            if self.serial:
                self.serial.close()
        except Exception:
            pass
        self.serial = None
        
        while self.running and self.serial is None:
            try:
                # Giữ nguyên self.com_port, self.baudrate; nếu com_port None, thử auto-detect
                if not self.com_port:
                    self.com_port = self.find_arduino_port()
                if not self.com_port:
                    print("[RECONNECT] Chưa tìm thấy COM port, sẽ thử lại...")
                    time.sleep(retry_delay)
                    continue
                
                self.serial = serial.Serial(self.com_port, self.baudrate, timeout=1)
                time.sleep(2)
                print(f"[RECONNECT] Đã kết nối lại Arduino tại {self.com_port}")
                # Đồng bộ trạng thái sau reconnect
                self.send_all_up()
                self._print_status()
            except Exception as e:
                print(f"[RECONNECT] Lỗi reconnect: {e}. Thử lại sau {retry_delay}s...")
                self.serial = None
                time.sleep(retry_delay)
    
    def _update_key_state(self, key_name, is_down):
        """Update key state và timestamp (thread-safe)"""
        with self.key_states_lock:
            current_time = time.time()
            if is_down:
                # Key down: check duplicate prevention
                if key_name in self.key_states and self.key_states[key_name][0]:
                    # Key đã đang down, skip duplicate
                    if self.enable_logging:
                        print(f"[LOG] Duplicate key down ignored: {key_name}")
                    return False
                # Set key down với timestamp
                self.key_states[key_name] = (True, current_time)
                return True
            else:
                # Key up: check nếu key đang down
                if key_name in self.key_states and self.key_states[key_name][0]:
                    self.key_states[key_name] = (False, current_time)
                    return True
                else:
                    # Key không đang down, có thể là duplicate key up
                    if self.enable_logging:
                        print(f"[LOG] Duplicate key up ignored: {key_name}")
                    return False
    
    def _release_key_safe(self, key_name):
        """Release key an toàn (thread-safe)"""
        with self.key_states_lock:
            if key_name in self.key_states and self.key_states[key_name][0]:
                self.key_states[key_name] = (False, time.time())
                try:
                    if self.serial and self.serial.is_open:
                        command = f"up:{key_name}\n"
                        self.serial.write(command.encode('utf-8'))
                        if self.enable_logging:
                            print(f"[LOG] Force released: {key_name}")
                except Exception:
                    pass
    
    def low_level_keyboard_proc(self, nCode, wParam, lParam):
        """Low-level keyboard hook callback"""
        if nCode >= HC_ACTION:
            # Extract keyboard data
            kb_data = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk_code = kb_data.vkCode
            
            # Safety hotkeys (handle immediately, do NOT forward to Arduino)
            if wParam in (WM_KEYDOWN, WM_SYSKEYDOWN):
                if vk_code == self.VK_PGDN:
                    # Toggle block_original_input
                    self.block_original_input = not self.block_original_input
                    status = "ON (BLOCK)" if self.block_original_input else "OFF (PASS)"
                    print(f"[HOTKEY] PageDown → Block original input: {status}")
                    self._print_status()
                    self._save_config()
                    return 1  # consume
                elif vk_code == self.VK_PGUP:
                    # Toggle forwarding
                    self.forwarding_enabled = not self.forwarding_enabled
                    status = "ENABLED" if self.forwarding_enabled else "DISABLED"
                    print(f"[HOTKEY] PageUp → Forwarding: {status}")
                    self._print_status()
                    self._save_config()
                    return 1  # consume
                elif vk_code == self.VK_END:
                    print("[HOTKEY] End → Exit requested")
                    # Post quit and stop
                    self.running = False
                    self.user32.PostQuitMessage(0)
                    self._save_config()
                    return 1  # consume

            # Map VK code to key name
            key_name = VK_TO_KEY.get(vk_code)
            
            if key_name:
                # Check if key down or up
                if wParam == WM_KEYDOWN or wParam == WM_SYSKEYDOWN:
                    # Key down event - check duplicate và update state
                    if self._update_key_state(key_name, True) and self.forwarding_enabled:
                        # Chỉ gửi nếu không phải duplicate
                        self.send_key_to_arduino(key_name, 'down')
                elif wParam == WM_KEYUP or wParam == WM_SYSKEYUP:
                    # Key up event - update state và gửi
                    if self._update_key_state(key_name, False) and self.forwarding_enabled:
                        # Chỉ gửi nếu key đang down
                        self.send_key_to_arduino(key_name, 'up')
                
                # QUAN TRỌNG: Block input gốc để game chỉ nhận input từ Arduino
                # Return 1 để block, return CallNextHookEx để allow
                if self.block_original_input:
                    return 1  # Block input gốc - game sẽ chỉ nhận từ Arduino
        
        # Allow input (nếu không block) hoặc cho phép các input không được map
        if not self.block_original_input:
            return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)
        else:
            return 1  # Block tất cả input đã được forward
    
    def install_hook(self):
        """Cài đặt keyboard hook"""
        # Get module handle
        module_handle = self.kernel32.GetModuleHandleW(None)
        if not module_handle:
            error_code = self.kernel32.GetLastError()
            raise RuntimeError(f"Không thể lấy module handle. Mã lỗi Windows: {error_code}")
        
        # Install hook
        self.hook = self.user32.SetWindowsHookExW(
            WH_KEYBOARD_LL,
            self.hook_proc,
            module_handle,
            0
        )
        
        if not self.hook:
            error_code = self.kernel32.GetLastError()
            error_msg = self._get_windows_error_message(error_code)
            raise RuntimeError(
                f"Không thể cài đặt keyboard hook.\n"
                f"Mã lỗi Windows: {error_code}\n"
                f"Chi tiết: {error_msg}\n"
                f"Lưu ý: Keyboard hook yêu cầu quyền Administrator."
            )
        
        print("Keyboard hook đã được cài đặt")
    
    def _get_windows_error_message(self, error_code):
        """Lấy thông báo lỗi Windows bằng FormatMessageW"""
        FORMAT_MESSAGE_FROM_SYSTEM = 0x00001000
        FORMAT_MESSAGE_IGNORE_INSERTS = 0x00000200
        FORMAT_MESSAGE_ALLOCATE_BUFFER = 0x00000100
        
        # Try using FormatMessageW với buffer tự cấp phát
        buffer_size = 256
        buffer = ctypes.create_unicode_buffer(buffer_size)
        
        flags = FORMAT_MESSAGE_FROM_SYSTEM | FORMAT_MESSAGE_IGNORE_INSERTS
        
        result = self.kernel32.FormatMessageW(
            flags,
            None,
            error_code,
            0,  # Language ID (0 = system default)
            buffer,
            buffer_size,
            None
        )
        
        if result:
            message = buffer.value.strip()
            if message:
                return message
        
        # Fallback: Common error codes mapping
        error_messages = {
            5: "Access Denied - Cần chạy với quyền Administrator",
            87: "Invalid Parameter",
            142: "Cannot set nonlocal hook without a module handle",
            0: "No error (success)",
        }
        
        return error_messages.get(error_code, "Unknown error {}".format(error_code))
    
    def _monitor_stuck_keys(self):
        """Monitor thread để phát hiện và auto-release stuck keys"""
        while self.running:
            try:
                current_time = time.time()
                stuck_keys = []
                
                with self.key_states_lock:
                    for key_name, (is_down, down_timestamp) in self.key_states.items():
                        if is_down:
                            # Key đang down, check timeout
                            elapsed = current_time - down_timestamp
                            if elapsed > self.stuck_key_timeout:
                                stuck_keys.append(key_name)
                
                # Release stuck keys
                for key_name in stuck_keys:
                    print(f"[WARNING] Auto-releasing stuck key: {key_name} (held for {self.stuck_key_timeout}s)")
                    self._release_key_safe(key_name)
                
                # Sleep 1 giây trước khi check lại
                time.sleep(1.0)
                
            except Exception as e:
                if self.enable_logging:
                    print(f"[ERROR] Stuck key monitor error: {e}")
                time.sleep(1.0)
    
    def message_loop(self):
        """Windows message loop"""
        msg = wintypes.MSG()
        
        while self.running:
            ret = self.user32.GetMessageW(
                ctypes.byref(msg),
                None,
                0,
                0
            )
            
            if ret == 0:  # WM_QUIT
                break
            elif ret == -1:  # Error
                print("Lỗi trong message loop")
                break
            else:
                self.user32.TranslateMessage(ctypes.byref(msg))
                self.user32.DispatchMessageW(ctypes.byref(msg))
    
    def start(self):
        """Bắt đầu hook và forward input"""
        # Kết nối Arduino (retry vô hạn cho đến khi thành công hoặc user thoát)
        while self.running is False:
            # ensure flag reset before connect
            break
        while True:
            if self.connect_arduino():
                break
            print("[START] Kết nối Arduino thất bại. Thử lại sau 2s...")
            time.sleep(2.0)
        
        try:
            self.install_hook()
            self.running = True
            
            # Start stuck key monitor thread
            self.stuck_key_monitor_thread = threading.Thread(
                target=self._monitor_stuck_keys,
                daemon=True
            )
            self.stuck_key_monitor_thread.start()
            
            if self.block_original_input:
                print("Đã bắt đầu nhận input từ Multiplicity và forward qua Arduino...")
                print("[WARNING] Input gốc đã bị BLOCK - Game chỉ nhận input từ Arduino")
                print("[WARNING] Bàn phím thật của máy này cũng sẽ bị block")
            else:
                print("Đã bắt đầu nhận input từ Multiplicity và forward qua Arduino...")
                print("[INFO] Input gốc vẫn được forward - Game có thể nhận cả 2 nguồn")
            print(f"[INFO] Stuck key auto-release: {self.stuck_key_timeout}s timeout")
            self._print_status()
            print("Nhấn Ctrl+C để dừng")
            
            # Run message loop in main thread
            self.message_loop()
            
        except KeyboardInterrupt:
            print("\nĐang dừng...")
        except Exception as e:
            import traceback
            print(f"Lỗi: {e}")
            print("\n=== Chi tiết lỗi ===")
            traceback.print_exc()
            print("\n=== Kết thúc chi tiết lỗi ===\n")
            # Pause để người dùng có thể xem lỗi
            input("Nhấn Enter để đóng...")
        finally:
            self.stop()
    
    def stop(self):
        """Dừng hook và đóng kết nối"""
        self.running = False
        
        # Cleanup: Release tất cả keys đang down (và trên Arduino)
        print("Đang cleanup và release tất cả keys...")
        with self.key_states_lock:
            keys_to_release = [
                key_name for key_name, (is_down, _) in self.key_states.items()
                if is_down
            ]
        
        for key_name in keys_to_release:
            self._release_key_safe(key_name)
            if self.enable_logging:
                print(f"[CLEANUP] Released: {key_name}")
        
        if keys_to_release:
            print(f"Đã release {len(keys_to_release)} key(s) đang down")

        # Gửi all_up xuống Arduino lần cuối
        self.send_all_up()
        
        # Đợi stuck key monitor thread dừng
        if self.stuck_key_monitor_thread and self.stuck_key_monitor_thread.is_alive():
            self.stuck_key_monitor_thread.join(timeout=2.0)
        
        if self.hook:
            self.user32.UnhookWindowsHookEx(self.hook)
            self.hook = None
            print("Keyboard hook đã được gỡ bỏ")
        
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Đã đóng kết nối Arduino")
        
        # Clear key states
        with self.key_states_lock:
            self.key_states.clear()


if __name__ == "__main__":
    import sys
    
    # Parse command line arguments
    # Usage: python keyboard_to_arduino.py [COM_PORT] [BAUDRATE] [BLOCK_INPUT] [STUCK_KEY_TIMEOUT] [ENABLE_LOGGING]
    com_port = None
    if len(sys.argv) > 1:
        com_port = sys.argv[1]
    
    baudrate = 115200
    if len(sys.argv) > 2:
        baudrate = int(sys.argv[2])
    
    # Block original input by default (để game chỉ nhận từ Arduino)
    block_input = True
    if len(sys.argv) > 3:
        block_input = sys.argv[3].lower() in ['true', '1', 'yes', 'on']
    
    # Stuck key timeout (giây)
    stuck_key_timeout = 10.0
    if len(sys.argv) > 4:
        stuck_key_timeout = float(sys.argv[4])
    
    # Enable logging
    enable_logging = False
    if len(sys.argv) > 5:
        enable_logging = sys.argv[5].lower() in ['true', '1', 'yes', 'on']
    
    # Create and start
    try:
        handler = KeyboardToArduino(
            com_port=com_port, 
            baudrate=baudrate,
            block_original_input=block_input,
            stuck_key_timeout=stuck_key_timeout,
            enable_logging=enable_logging
        )
        handler.start()
    except Exception as e:
        import traceback
        print(f"\n=== LỖI KHỞI TẠO ===")
        print(f"Lỗi: {e}")
        print("\n=== Chi tiết lỗi ===")
        traceback.print_exc()
        print("\n=== Kết thúc chi tiết lỗi ===\n")
        # Pause để người dùng có thể xem lỗi
        input("Nhấn Enter để đóng...")

