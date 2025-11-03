"""
Arduino Serial Output Module - Direct Serial communication với Arduino Pro Micro
Hỗ trợ bot output qua Arduino USB HID keyboard thay vì SendInput
"""
import serial
import serial.tools.list_ports
import time
from typing import Optional
from src.common.logger import get_logger

log = get_logger(__name__)

# Key mapping: vkeys key names → Arduino key names
# Reference: arduino_hid_keyboard_tcp.ino keyMap[]
VKEYS_TO_ARDUINO = {
    # Letters (same)
    'a': 'a', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'e', 'f': 'f',
    'g': 'g', 'h': 'h', 'i': 'i', 'j': 'j', 'k': 'k', 'l': 'l',
    'm': 'm', 'n': 'n', 'o': 'o', 'p': 'p', 'q': 'q', 'r': 'r',
    's': 's', 't': 't', 'u': 'u', 'v': 'v', 'w': 'w', 'x': 'x',
    'y': 'y', 'z': 'z',
    
    # Numbers (same)
    '0': '0', '1': '1', '2': '2', '3': '3', '4': '4',
    '5': '5', '6': '6', '7': '7', '8': '8', '9': '9',
    
    # Control keys - map to Arduino key names (Arduino uses 'shift', 'ctrl', 'alt' not 'lshift', 'lctrl', 'lalt')
    'shift': 'shift',       # Arduino keyMap uses 'shift' not 'lshift'
    'ctrl': 'ctrl',         # Arduino keyMap uses 'ctrl' not 'lctrl'
    'alt': 'alt',           # Arduino keyMap uses 'alt' not 'lalt'
    'space': 'space',
    'enter': 'enter',
    'backspace': 'backspace',
    'esc': 'esc',
    'tab': 'tab',
    'caps lock': 'caps',
    'caps': 'caps',
    
    # Navigation keys
    'page up': 'pgup',
    'page down': 'pgdn',
    'pgup': 'pgup',
    'pgdn': 'pgdn',
    'end': 'end',
    'home': 'home',
    'insert': 'insert',
    'delete': 'delete',
    
    # Arrow keys (same)
    'left': 'left',
    'right': 'right',
    'up': 'up',
    'down': 'down',
    
    # Function keys (same)
    'f1': 'f1', 'f2': 'f2', 'f3': 'f3', 'f4': 'f4',
    'f5': 'f5', 'f6': 'f6', 'f7': 'f7', 'f8': 'f8',
    'f9': 'f9', 'f10': 'f10', 'f11': 'f11', 'f12': 'f12',
    
    # Special keys
    'num lock': 'numlock',
    'numlock': 'numlock',
    'scroll lock': 'scroll',
    'scroll': 'scroll',
    'pause': 'pause',
    'menu': 'menu',
    'printscreen': 'printscreen',
    'print screen': 'printscreen',
    
    # Special characters (from vkeys.py)
    ';': 'semicolon',
    '=': 'equals',
    ',': 'comma',
    '-': 'minus',
    '.': 'period',
    '/': 'slash',
    '`': 'grave',
    '[': 'lbracket',
    '\\': 'backslash',
    ']': 'rbracket',
    "'": 'quote',
    '"': 'quote',
}


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
        
        Args:
            com_port: COM port của Arduino (None = auto-detect)
            baudrate: Serial baudrate (default: 115200)
            key_mapping: Key remapping dictionary (e.g., {'a': 'rbracket', 'w': 'lbracket'})
            remapping_enabled: Enable/disable key remapping (default: True)
        """
        self.serial: Optional[serial.Serial] = None
        self.com_port = com_port
        self.baudrate = baudrate
        self.connected = False
        
        # Key remapping for game customization
        self.key_mapping = key_mapping or {}  # Key remapping: {'original': 'mapped'}
        self.remapping_enabled = remapping_enabled  # Toggle for key remapping
        
        # Statistics
        self.stats = {
            'total_remapped': 0  # Count of remapped keys
        }
        
        # Load remapping from config if not provided
        if not self.key_mapping:
            try:
                from src.common import config
                if hasattr(config, 'arduino_key_mapping') and config.arduino_key_mapping:
                    self.key_mapping = {k.lower(): v.lower() for k, v in config.arduino_key_mapping.items()}
                    log.info(f"Loaded key remapping from config: {len(self.key_mapping)} mappings")
                if hasattr(config, 'arduino_remapping_enabled'):
                    self.remapping_enabled = config.arduino_remapping_enabled
            except Exception as e:
                log.warning(f"Failed to load remapping config: {e}")
        
        # Try connect on initialization
        self._connect()
        
        # Log remapping status
        if self.key_mapping:
            log.info(f"Key remapping: {len(self.key_mapping)} mappings, Status: {'ENABLED' if self.remapping_enabled else 'DISABLED'}")
            for orig, mapped in self.key_mapping.items():
                log.debug(f"  {orig} → {mapped}")
    
    def _find_arduino_ports(self) -> list:
        """
        Tìm tất cả COM ports có thể là Arduino
        
        Returns:
            List of COM port names
        """
        ports = []
        try:
            for port in serial.tools.list_ports.comports():
                ports.append(port.device)
                # Log port info for debugging
                log.debug(f"Found COM port: {port.device} - {port.description}")
        except Exception as e:
            log.warning(f"Failed to list COM ports: {e}")
        
        return ports
    
    def _connect(self) -> bool:
        """
        Kết nối đến Arduino qua Serial
        
        Returns:
            True nếu kết nối thành công, False nếu thất bại
        """
        if self.serial and self.serial.is_open:
            # Already connected
            return True
        
        # Determine ports to try
        if self.com_port:
            # Use specified port
            ports_to_try = [self.com_port]
            log.info(f"Attempting to connect to specified COM port: {self.com_port}")
        else:
            # Auto-detect: try all available ports
            ports_to_try = self._find_arduino_ports()
            log.info(f"Auto-detecting Arduino COM port from {len(ports_to_try)} available ports")
        
        if not ports_to_try:
            log.error("No COM ports found")
            self.connected = False
            return False
        
        # Try each port
        for port in ports_to_try:
            try:
                log.debug(f"Trying to connect to {port}...")
                self.serial = serial.Serial(
                    port,
                    self.baudrate,
                    timeout=0.1,
                    write_timeout=0.1,
                    inter_byte_timeout=0.01
                )
                
                # Wait for Arduino to initialize
                time.sleep(0.5)
                
                # Flush any existing data
                self.serial.flush()
                
                self.connected = True
                self.com_port = port
                log.info(f"✅ Successfully connected to Arduino on {port} (baudrate: {self.baudrate})")
                return True
                
            except serial.SerialException as e:
                log.debug(f"Failed to connect to {port}: {e}")
                continue
            except Exception as e:
                log.warning(f"Unexpected error connecting to {port}: {e}")
                continue
        
        # Failed to connect to all ports
        log.error(f"❌ Failed to connect to Arduino on any of {len(ports_to_try)} ports")
        self.connected = False
        return False
    
    def _map_key(self, key: str) -> str:
        """
        Map vkeys key name sang Arduino key name
        
        Args:
            key: vkeys key name (lowercase)
        
        Returns:
            Arduino key name, hoặc original key nếu không có mapping
        """
        key_lower = key.lower()
        
        # Step 1: Apply key remapping (game customization) if enabled
        if self.remapping_enabled and self.key_mapping:
            original_key = key_lower
            if key_lower in self.key_mapping:
                key_lower = self.key_mapping[key_lower]
                self.stats['total_remapped'] += 1
                log.debug(f"Key remapping: '{original_key}' → '{key_lower}'")
        
        # Step 2: Map vkeys key name to Arduino key name (system mapping)
        arduino_key = VKEYS_TO_ARDUINO.get(key_lower, key_lower)
        
        # Log mapping for debugging
        if arduino_key != key_lower:
            log.debug(f"Key mapping: '{key_lower}' → '{arduino_key}'")
        
        return arduino_key
    
    def toggle_remapping(self):
        """
        Toggle key remapping on/off
        """
        self.remapping_enabled = not self.remapping_enabled
        status = "ENABLED" if self.remapping_enabled else "DISABLED"
        log.info(f"Key remapping: {status}")
    
    def set_remapping(self, enabled: bool):
        """
        Set key remapping enabled/disabled
        
        Args:
            enabled: True to enable remapping, False to disable
        """
        self.remapping_enabled = enabled
        status = "ENABLED" if self.remapping_enabled else "DISABLED"
        log.info(f"Key remapping: {status}")
    
    def send_command(self, action: str, key: str = None) -> bool:
        """
        Gửi command đến Arduino: 'down:a\n' hoặc 'up:a\n'
        
        Args:
            action: 'down', 'up', hoặc 'all_up'
            key: Key name (chỉ dùng cho 'down' và 'up', có thể None cho 'all_up')
        
        Returns:
            True nếu gửi thành công, False nếu thất bại
        """
        # Validate input
        if action not in ['down', 'up', 'all_up']:
            log.warning(f"Invalid action: {action}")
            return False
        
        if action != 'all_up' and (not key or not key.strip()):
            log.warning(f"Key required for action '{action}'")
            return False
        
        if not self.connected or not self.serial or not self.serial.is_open:
            # Try reconnect
            if not self._connect():
                return False
            # If reconnect successful, continue to send command
        
        try:
            # Handle special command
            if action == 'all_up':
                command = "all_up\n"
            else:
                # Map key name
                arduino_key = self._map_key(key)
                command = f"{action}:{arduino_key}\n"
            
            # Send command
            self.serial.write(command.encode('utf-8'))
            self.serial.flush()  # Ensure command is sent immediately
            
            log.debug(f"Sent command: {command.strip()}")
            return True
            
        except serial.SerialException as e:
            log.error(f"Serial error sending command: {e}")
            self.connected = False
            # Try reconnect
            self._connect()
            return False
        except Exception as e:
            log.error(f"Unexpected error sending command: {e}")
            return False
    
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
        key = key.lower()
        self.send_command('down', key)
    
    def key_up(self, key: str):
        """
        Release key
        
        Args:
            key: Key name
        """
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
        if self.connected and self.serial and self.serial.is_open:
            try:
                self.serial.write(b"all_up\n")
                self.serial.flush()
                log.debug("Sent command: all_up")
            except Exception as e:
                log.error(f"Failed to send all_up command: {e}")
    
    def disconnect(self):
        """
        Disconnect from Arduino
        """
        if self.serial and self.serial.is_open:
            try:
                # Release all keys before disconnecting
                self.release_all()
                time.sleep(0.1)
                
                # Close serial connection
                self.serial.close()
                log.info("Disconnected from Arduino")
            except Exception as e:
                log.error(f"Error disconnecting from Arduino: {e}")
            finally:
                self.connected = False
                self.serial = None
    
    def __del__(self):
        """Cleanup on deletion"""
        self.disconnect()

