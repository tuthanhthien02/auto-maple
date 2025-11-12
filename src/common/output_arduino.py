"""
Arduino Serial Output Module - Direct Serial communication với Arduino Pro Micro
Hỗ trợ bot output qua Arduino USB HID keyboard thay vì SendInput

NOTE: Sử dụng SharedArduinoConnection để tránh "Access is denied" khi chạy cùng với VMware receiver
"""
import serial
import time
from typing import Optional
from src.common.logger import get_logger

log = get_logger(__name__)


class ArduinoSerialOutput:
    """
    Arduino Serial Output - Direct Serial communication với Arduino Pro Micro
    
    Sử dụng Serial protocol giống TCP version:
    - "down:a\n" - Press key 'a'
    - "up:a\n" - Release key 'a'
    - "all_up\n" - Release all keys
    """
    
    def __init__(self, com_port: Optional[str] = None, baudrate: int = 115200, 
                 key_mapping: Optional[dict] = None, remapping_enabled: bool = True):
        """
        Initialize Arduino Serial Output
        
        NOTE: Sử dụng SharedArduinoConnection để tránh conflict với VMware receiver
        
        Args:
            com_port: COM port của Arduino (None = auto-detect)
            baudrate: Serial baudrate (default: 115200)
            key_mapping: Key remapping dictionary (e.g., {'a': 'rbracket', 'w': 'lbracket'})
            remapping_enabled: Enable/disable key remapping (default: True)
        """
        # Use shared connection instead of creating new serial connection
        from src.common.shared_arduino_connection import SharedArduinoConnection
        
        self.shared_connection = SharedArduinoConnection.get_instance(
            com_port=com_port,
            baudrate=baudrate,
            key_mapping=key_mapping,
            remapping_enabled=remapping_enabled
        )
        
        # Store for backward compatibility
        self.com_port = self.shared_connection.com_port
        self.baudrate = self.shared_connection.baudrate
        self.key_mapping = self.shared_connection.key_mapping
        self.remapping_enabled = self.shared_connection.remapping_enabled
        
        # Statistics (sync from shared connection stats)
        self.stats = {
            'total_remapped': self.shared_connection.stats.get('total_remapped', 0)
        }
        
        # Backward compatibility: expose serial property
        self.serial = self.shared_connection.get_serial()
        self.connected = self.shared_connection.is_connected()
        
        log.info("[ArduinoSerialOutput] ✅ Initialized using SharedArduinoConnection")
        log.info(f"[ArduinoSerialOutput] Connection status: {'CONNECTED' if self.connected else 'DISCONNECTED'}")
        if self.connected:
            log.info(f"[ArduinoSerialOutput] COM Port: {self.com_port}, Baudrate: {self.baudrate}")
    
    # Removed _find_arduino_ports, _connect, _map_key - now handled by SharedArduinoConnection
    
    def toggle_remapping(self):
        """
        Toggle key remapping on/off
        """
        self.shared_connection.toggle_remapping()
        self.remapping_enabled = self.shared_connection.remapping_enabled
    
    def set_remapping(self, enabled: bool):
        """
        Set key remapping enabled/disabled
        
        Args:
            enabled: True to enable remapping, False to disable
        """
        self.shared_connection.set_remapping(enabled)
        self.remapping_enabled = self.shared_connection.remapping_enabled
    
    def send_command(self, action: str, key: str = None) -> bool:
        """
        Gửi command đến Arduino: 'down:a\n' hoặc 'up:a\n'
        Sử dụng SharedArduinoConnection (thread-safe)
        
        Args:
            action: 'down', 'up', hoặc 'all_up'
            key: Key name (chỉ dùng cho 'down' và 'up', có thể None cho 'all_up')
        
        Returns:
            True nếu gửi thành công, False nếu thất bại
        """
        # Update connected status from shared connection
        old_connected = self.connected
        self.connected = self.shared_connection.is_connected()
        self.serial = self.shared_connection.get_serial()
        
        # Log connection status change
        if old_connected != self.connected:
            log.info(f"[ArduinoSerialOutput] Connection status changed: {'CONNECTED' if self.connected else 'DISCONNECTED'}")
        
        if not self.connected:
            log.debug(f"[ArduinoSerialOutput] Not connected, cannot send command: {action}:{key if key else 'all_up'}")
            return False
        
        # Forward to shared connection
        result = self.shared_connection.send_command(action, key)
        if not result:
            log.debug(f"[ArduinoSerialOutput] Failed to send command: {action}:{key if key else 'all_up'}")
        return result
    
    def press(self, key: str, n: int = 1, down_time: float = 0.05, up_time: float = 0.1):
        """
        Press key N times với timing (giống SendInput)
        Includes advanced anti-detect timing randomization.
        
        Args:
            key: Key name
            n: Number of times to press
            down_time: Duration to hold key down (seconds)
            up_time: Duration between presses (seconds)
        """
        from src.common import config
        
        # Check if bot is enabled (same as vkeys.press())
        if not config.enabled:
            return
        
        # Update connected status
        self.connected = self.shared_connection.is_connected()
        if not self.connected:
            return
        
        key = key.lower()
        
        # Import timing functions from vkeys for consistency
        try:
            from src.common.vkeys import _get_human_like_delay, _get_micro_pause
            use_timing_randomization = True
        except ImportError:
            # Fallback if vkeys not available
            use_timing_randomization = False
        
        for i in range(n):
            # Advanced timing randomization (same as SendInput)
            if use_timing_randomization:
                down_delay = _get_human_like_delay(down_time, 'down')
                up_delay = _get_human_like_delay(up_time, 'up')
            else:
                # Fallback: simple timing without randomization
                down_delay = down_time
                up_delay = up_time
            
            # Key down
            self.send_command('down', key)
            time.sleep(down_delay)
            
            # Key up
            self.send_command('up', key)
            
            # Wait between presses (if multiple presses)
            if i < n - 1:
                time.sleep(up_delay)
                
                # Add micro-pauses between rapid key presses (same as SendInput)
                if n > 1 and use_timing_randomization:
                    micro_pause = _get_micro_pause()
                    time.sleep(micro_pause)
    
    def key_down(self, key: str):
        """
        Hold key down
        
        Args:
            key: Key name
        """
        # Update connected status
        self.connected = self.shared_connection.is_connected()
        if not self.connected:
            return
        
        key = key.lower()
        self.send_command('down', key)
    
    def key_up(self, key: str):
        """
        Release key
        
        Args:
            key: Key name
        """
        # Update connected status
        self.connected = self.shared_connection.is_connected()
        if not self.connected:
            return
        
        key = key.lower()
        self.send_command('up', key)
    
    def press_with_behavioral_pause(self, key: str, n: int = 1, down_time: float = 0.05, up_time: float = 0.1):
        """
        Enhanced press function with pattern variation (giống SendInput)
        
        Args:
            key: Key name
            n: Number of times to press
            down_time: Duration to hold key down (seconds)
            up_time: Duration between presses (seconds)
        """
        from src.common import config
        from random import uniform
        
        # Check if bot is enabled
        if not config.enabled:
            return
        
        key = key.lower()
        
        # Import timing functions from vkeys for consistency
        try:
            from src.common.vkeys import _get_human_like_delay, _get_micro_pause, _get_input_pattern_variation
            use_timing_randomization = True
        except ImportError:
            # Fallback if vkeys not available
            use_timing_randomization = False
            # Fallback implementation
            def _get_input_pattern_variation():
                return uniform(0.8, 1.2)
        
        for i in range(n):
            # Apply input pattern variation (same as SendInput)
            if use_timing_randomization:
                variation = _get_input_pattern_variation()
                adjusted_down_time = down_time * variation
                adjusted_up_time = up_time * variation
                
                # Advanced timing randomization
                down_delay = _get_human_like_delay(adjusted_down_time, 'down')
                up_delay = _get_human_like_delay(adjusted_up_time, 'up')
            else:
                # Fallback: simple timing without randomization
                down_delay = down_time
                up_delay = up_time
            
            # Key down
            self.send_command('down', key)
            time.sleep(down_delay)
            
            # Key up
            self.send_command('up', key)
            time.sleep(up_delay)
            
            # Add micro-pauses between rapid key presses (same as SendInput)
            if i < n - 1 and n > 1:
                if use_timing_randomization:
                    micro_pause = _get_micro_pause()
                    time.sleep(micro_pause)
    
    def press_sequence_with_variation(self, keys: list, delays: list = None):
        """
        Presses a sequence of keys with human-like variations (giống SendInput)
        
        Args:
            keys: List of keys to press in sequence
            delays: Optional list of delays between keys
        """
        from src.common import config
        
        # Check if bot is enabled
        if not config.enabled:
            return
        
        # Import timing functions from vkeys for consistency
        try:
            from src.common.vkeys import _get_human_like_delay
            use_timing_randomization = True
        except ImportError:
            use_timing_randomization = False
        
        # Generate delays if not provided
        if delays is None:
            if use_timing_randomization:
                delays = [_get_human_like_delay(0.1, 'micro') for _ in range(len(keys) - 1)]
            else:
                delays = [0.1] * (len(keys) - 1)
        
        for i, key in enumerate(keys):
            # Press key with variation (uses press_with_behavioral_pause internally)
            self.press_with_behavioral_pause(key, 1)
            
            # Add delay between keys
            if i < len(keys) - 1:
                delay = delays[i] if i < len(delays) else (0.1 if not use_timing_randomization else _get_human_like_delay(0.1, 'micro'))
                time.sleep(delay)
    
    def simulate_human_typing(self, text: str, base_delay: float = 0.1):
        """
        Simulates human typing with realistic timing variations (giống SendInput)
        
        Args:
            text: Text to type
            base_delay: Base delay between keystrokes (seconds)
        """
        from src.common import config
        
        # Check if bot is enabled
        if not config.enabled:
            return
        
        # Import timing functions from vkeys for consistency
        try:
            from src.common.vkeys import _get_human_like_delay
            use_timing_randomization = True
        except ImportError:
            use_timing_randomization = False
        
        for char in text:
            if char == ' ':
                # Space key
                self.press_with_behavioral_pause('space', 1)
            elif char.isupper():
                # Uppercase: shift + key
                self.key_down('shift')
                if use_timing_randomization:
                    time.sleep(_get_human_like_delay(0.01, 'micro'))
                else:
                    time.sleep(0.01)
                
                self.key_down(char.lower())
                if use_timing_randomization:
                    time.sleep(_get_human_like_delay(0.05, 'down'))
                else:
                    time.sleep(0.05)
                
                self.key_up(char.lower())
                if use_timing_randomization:
                    time.sleep(_get_human_like_delay(0.01, 'micro'))
                else:
                    time.sleep(0.01)
                
                self.key_up('shift')
            else:
                # Lowercase: regular key
                self.press_with_behavioral_pause(char.lower(), 1)
            
            # Variable delay between characters
            if use_timing_randomization:
                char_delay = _get_human_like_delay(base_delay, 'micro')
            else:
                char_delay = base_delay
            time.sleep(char_delay)
    
    def release_all(self):
        """
        Release all keys (emergency cleanup)
        """
        self.shared_connection.send_all_up()
    
    def disconnect(self):
        """
        Disconnect from Arduino
        NOTE: Shared connection will remain open if other components are using it
        """
        # Don't disconnect shared connection - other components might be using it
        # Just update local state
        self.connected = False
        self.serial = None
        log.debug("ArduinoSerialOutput disconnected (shared connection remains active)")
    
    def __del__(self):
        """Cleanup on deletion"""
        # Don't disconnect shared connection - just clear local references
        self.disconnect()

