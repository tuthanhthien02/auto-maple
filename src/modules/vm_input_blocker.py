"""
VM Input Blocker - Block input từ VM hardware và force dùng Arduino
Sử dụng keyboard hook để block tất cả input từ VM hardware
Anti-detect: Random pass-through, timing variation, periodic pauses
"""
import ctypes
import ctypes.wintypes
import threading
import time
import random
from typing import Optional
from ctypes import wintypes
from src.common.logger import get_logger
from src.common import config

log = get_logger(__name__)

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


class KBDLLHOOKSTRUCT(ctypes.Structure):
    _fields_ = [
        ("vkCode", wintypes.DWORD),
        ("scanCode", wintypes.DWORD),
        ("flags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", wintypes.ULONG_PTR)
    ]


class VMInputBlocker:
    """
    Block input từ VM hardware bằng keyboard hook
    Tất cả input từ VM sẽ bị block, chỉ cho phép input từ Arduino
    """
    
    def __init__(self, enable_logging=False):
        """
        Initialize VM Input Blocker
        
        Args:
            enable_logging: Enable debug logging (default: False)
        """
        self.enable_logging = enable_logging
        self.blocking = False
        self.hook = None
        self.user32 = None
        self.kernel32 = None
        self.hook_thread = None
        self.hook_running = False
        
        # Whitelist keys (emergency keys that should NOT be blocked)
        # Ctrl+Alt+Del, Ctrl+Shift+Esc, etc.
        self.whitelist_vk_codes = {
            0x23,  # End key (for hotkeys)
            # Add more emergency keys if needed
        }
        
        # Anti-detect settings (không ảnh hưởng đến blocking - chỉ timing variation)
        self.enable_timing_variation = True  # Enable timing variation trong hook (0-0.5ms)
        # NOTE: Block 100% input từ VM hardware - không có random pass-through
        
        # Periodic pause settings (REMOVED - không cần vì không ảnh hưởng blocking)
        # NOTE: Periodic pauses đã được remove vì không cần thiết cho 100% blocking
        
        # Stats
        self.stats = {
            'total_blocked': 0,
            'total_passed': 0,  # Only whitelist keys pass through
        }
        
        # Initialize Windows API
        self._init_windows_api()
    
    def _init_windows_api(self):
        """Initialize Windows API for keyboard hook"""
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
        
        # Define PostQuitMessage
        self.user32.PostQuitMessage.argtypes = [ctypes.c_int]
        self.user32.PostQuitMessage.restype = None
    
    def _low_level_keyboard_proc(self, nCode, wParam, lParam):
        """
        Low-level keyboard hook callback
        Blocks 100% input from VM hardware (except whitelist keys only)
        
        CRITICAL: Return 1 = Block key, Return CallNextHookEx = Pass through
        - Whitelist keys (End key): Pass through
        - All other keys when blocking: Return 1 (100% block)
        
        Anti-detect: Timing variation (0-0.5ms) trong hook processing
        NOTE: Timing variation không ảnh hưởng blocking - vẫn block 100%
        """
        # Fast path: if not action code, pass through immediately
        if nCode < HC_ACTION:
            if self.hook is not None:
                return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)
            return 0  # Safe fallback if hook is None
        
        # Anti-detect: Timing variation trong hook processing (0-0.5ms)
        # NOTE: Delay này rất nhỏ và không ảnh hưởng đến blocking behavior
        if self.enable_timing_variation and self.blocking:
            time.sleep(random.uniform(0, 0.0005))
        
        # Parse structure to get vkCode (with error handling)
        try:
            if lParam is None:
                # Invalid lParam, pass through
                if self.hook is not None:
                    return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)
                return 0
            
            kb_data = ctypes.cast(lParam, ctypes.POINTER(KBDLLHOOKSTRUCT)).contents
            vk_code = kb_data.vkCode
        except (ValueError, TypeError, AttributeError) as e:
            # Invalid pointer or structure, pass through
            if self.enable_logging:
                log.debug(f"[VM_INPUT_BLOCKER] Error parsing keyboard data: {e}")
            if self.hook is not None:
                return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)
            return 0
        
        # Whitelist check: allow emergency keys ONLY
        if vk_code in self.whitelist_vk_codes:
            self.stats['total_passed'] += 1
            if self.hook is not None:
                return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)
            return 0
        
        # Block 100% all other keys from VM hardware
        if self.blocking:
            self.stats['total_blocked'] += 1
            if self.enable_logging:
                log.debug(f"[VM_INPUT_BLOCKER] Blocked key: VK={vk_code:02X}")
            # Return 1 to block the key - 100% blocking
            # This prevents the key from reaching the system
            return 1
        
        # If not blocking, pass through
        self.stats['total_passed'] += 1
        if self.hook is not None:
            return self.user32.CallNextHookEx(self.hook, nCode, wParam, lParam)
        return 0
    
    def install_hook(self):
        """Install low-level keyboard hook"""
        if self.hook is not None:
            log.warning("[VM_INPUT_BLOCKER] Hook already installed")
            return False
        
        log.info("[VM_INPUT_BLOCKER] Installing keyboard hook...")
        
        try:
            HOOKPROC = ctypes.WINFUNCTYPE(
                ctypes.c_int,
                ctypes.c_int,
                wintypes.WPARAM,
                wintypes.LPARAM
            )
            
            hook_proc = HOOKPROC(self._low_level_keyboard_proc)
            
            # Get module handle
            h_mod = self.kernel32.GetModuleHandleW(None)
            
            # Install hook
            self.hook = self.user32.SetWindowsHookExW(
                WH_KEYBOARD_LL,
                hook_proc,
                h_mod,
                0
            )
            
            if self.hook is None:
                log.error("[VM_INPUT_BLOCKER] Failed to install keyboard hook")
                return False
            
            log.info("[VM_INPUT_BLOCKER] ✅ Keyboard hook installed successfully")
            
            # Start message loop in separate thread
            self.hook_running = True
            self.hook_thread = threading.Thread(target=self._message_loop, daemon=True)
            self.hook_thread.start()
            
            return True
            
        except Exception as e:
            log.error(f"[VM_INPUT_BLOCKER] Error installing hook: {e}")
            return False
    
    def uninstall_hook(self):
        """Uninstall keyboard hook"""
        if self.hook is None:
            return
        
        try:
            # Stop message loop
            self.hook_running = False
            
            # Unhook
            if self.user32.UnhookWindowsHookEx(self.hook):
                log.info("[VM_INPUT_BLOCKER] ✅ Keyboard hook uninstalled")
            else:
                log.warning("[VM_INPUT_BLOCKER] Failed to uninstall hook")
            
            self.hook = None
            
            # Wait for thread to finish (with timeout)
            if self.hook_thread and self.hook_thread.is_alive():
                self.hook_thread.join(timeout=1.0)
            
        except Exception as e:
            log.error(f"[VM_INPUT_BLOCKER] Error uninstalling hook: {e}")
    
    def _message_loop(self):
        """Message loop for keyboard hook (must run in separate thread)"""
        msg = wintypes.MSG()
        
        while self.hook_running:
            try:
                # PeekMessageW returns BOOL (0 = FALSE, non-zero = TRUE)
                b_ret = self.user32.PeekMessageW(
                    ctypes.byref(msg),
                    None,
                    0,
                    0,
                    PM_REMOVE
                )
                
                # Check if message was retrieved (non-zero = TRUE)
                if b_ret != 0:
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageW(ctypes.byref(msg))
                else:
                    time.sleep(0.01)  # Small delay to prevent CPU spinning
                    
            except Exception as e:
                log.error(f"[VM_INPUT_BLOCKER] Error in message loop: {e}")
                import traceback
                log.error(f"[VM_INPUT_BLOCKER] Traceback: {traceback.format_exc()}")
                time.sleep(0.1)  # Wait before retrying
                # Don't exit on error - keep trying to process messages
    
    def start_blocking(self):
        """Start blocking VM input"""
        if not self.blocking:
            self.blocking = True
            log.info("[VM_INPUT_BLOCKER] ✅ Started blocking VM input")
    
    def stop_blocking(self):
        """Stop blocking VM input"""
        if self.blocking:
            self.blocking = False
            log.info("[VM_INPUT_BLOCKER] ✅ Stopped blocking VM input")
    
    def is_blocking(self):
        """Check if currently blocking"""
        return self.blocking
    
    def get_stats(self):
        """Get blocking statistics"""
        return self.stats.copy()

