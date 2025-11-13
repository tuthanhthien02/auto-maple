"""
Shared Arduino Connection - Singleton class để quản lý serial connection
Đảm bảo chỉ có một serial connection duy nhất được sử dụng bởi cả bot và TCP server
"""

import serial
import serial.tools.list_ports
import threading
import time
import os
import json
from typing import List, Optional
from src.common.logger import get_logger
from src.common.serial_obfuscation import SerialObfuscator

log = get_logger(__name__)

# Key mapping: vkeys key names → Arduino key names (same as output_arduino.py)
VKEYS_TO_ARDUINO = {
    # Letters (same)
    "a": "a",
    "b": "b",
    "c": "c",
    "d": "d",
    "e": "e",
    "f": "f",
    "g": "g",
    "h": "h",
    "i": "i",
    "j": "j",
    "k": "k",
    "l": "l",
    "m": "m",
    "n": "n",
    "o": "o",
    "p": "p",
    "q": "q",
    "r": "r",
    "s": "s",
    "t": "t",
    "u": "u",
    "v": "v",
    "w": "w",
    "x": "x",
    "y": "y",
    "z": "z",
    # Numbers (same)
    "0": "0",
    "1": "1",
    "2": "2",
    "3": "3",
    "4": "4",
    "5": "5",
    "6": "6",
    "7": "7",
    "8": "8",
    "9": "9",
    # Control keys
    "shift": "shift",
    "ctrl": "ctrl",
    "alt": "alt",
    "space": "space",
    "enter": "enter",
    "backspace": "backspace",
    "esc": "esc",
    "tab": "tab",
    "caps lock": "caps",
    "caps": "caps",
    # Navigation keys
    "page up": "pgup",
    "page down": "pgdn",
    "pgup": "pgup",
    "pgdn": "pgdn",
    "end": "end",
    "home": "home",
    "insert": "insert",
    "delete": "delete",
    # Arrow keys
    "left": "left",
    "right": "right",
    "up": "up",
    "down": "down",
    # Function keys
    "f1": "f1",
    "f2": "f2",
    "f3": "f3",
    "f4": "f4",
    "f5": "f5",
    "f6": "f6",
    "f7": "f7",
    "f8": "f8",
    "f9": "f9",
    "f10": "f10",
    "f11": "f11",
    "f12": "f12",
    # Special keys
    "num lock": "numlock",
    "numlock": "numlock",
    "scroll lock": "scroll",
    "scroll": "scroll",
    "pause": "pause",
    "menu": "menu",
    "printscreen": "printscreen",
    "print screen": "printscreen",
    # Special characters
    ";": "semicolon",
    "=": "equals",
    ",": "comma",
    "-": "minus",
    ".": "period",
    "/": "slash",
    "`": "grave",
    "[": "lbracket",
    "\\": "backslash",
    "]": "rbracket",
    "'": "quote",
    '"': "quote",
}


class SharedArduinoConnection:
    """
    Singleton class để quản lý shared serial connection đến Arduino
    Thread-safe với lock để đảm bảo không conflict khi gửi commands
    """

    _instance = None
    _lock = threading.Lock()
    _init_lock = threading.Lock()
    _last_reuse_log = 0.0

    def __new__(cls, *args, **kwargs):
        """Singleton pattern - chỉ tạo một instance"""
        if cls._instance is None:
            with cls._init_lock:
                if cls._instance is None:
                    cls._instance = super(SharedArduinoConnection, cls).__new__(cls)
        return cls._instance

    def __init__(
        self,
        com_port: Optional[str] = None,
        baudrate: int = 115200,
        key_mapping: Optional[dict] = None,
        remapping_enabled: bool = True,
    ):
        """
        Initialize shared Arduino connection

        Args:
            com_port: COM port của Arduino (None = auto-detect)
            baudrate: Serial baudrate (default: 115200)
            key_mapping: Key remapping dictionary (e.g., {'a': 'rbracket', 'w': 'lbracket'})
            remapping_enabled: Enable/disable key remapping (default: True)
        """
        # Chỉ init một lần (singleton)
        if hasattr(self, "_initialized"):
            now = time.time()
            if now - self.__class__._last_reuse_log >= 60:
                log.debug(
                    "[SharedArduinoConnection] Instance already initialized, reusing existing"
                )
                self.__class__._last_reuse_log = now
            return

        log.info("[SharedArduinoConnection] Initializing shared Arduino connection...")
        self._initialized = True
        self.__class__._last_reuse_log = time.time()
        self.serial: Optional[serial.Serial] = None
        self.com_port = com_port
        self.baudrate = baudrate
        self.connected = False
        self._send_lock = threading.Lock()  # Lock cho send_command()

        # Key remapping for game customization
        self.key_mapping = key_mapping or {}
        self.remapping_enabled = remapping_enabled
        self.obfuscator = None
        self.obfuscation_enabled = True

        # Statistics
        self.stats = {"total_sent": 0, "total_errors": 0, "total_remapped": 0}

        # Load config from vmware_receiver.config.json if exists
        self._load_config()

        # Load remapping from config if not provided
        if not self.key_mapping:
            try:
                from src.common import config

                if (
                    hasattr(config, "arduino_key_mapping")
                    and config.arduino_key_mapping
                ):
                    self.key_mapping = {
                        k.lower(): v.lower()
                        for k, v in config.arduino_key_mapping.items()
                    }
                    log.info(
                        f"Loaded key remapping from config: {len(self.key_mapping)} mappings"
                    )
                if hasattr(config, "arduino_remapping_enabled"):
                    self.remapping_enabled = config.arduino_remapping_enabled
                self.obfuscation_enabled = getattr(
                    config, "arduino_obfuscation_enabled", True
                )
            except Exception as e:
                log.debug(f"Failed to load remapping from config: {e}")

        # Phase 5: Device Stealth - Raw Input API Bypass
        self.device_stealth = None
        try:
            from src.common.device_stealth import get_device_stealth

            self.device_stealth = get_device_stealth(enabled=True)
            log.debug("Device Stealth initialized (Phase 5: Advanced Stealth)")
        except Exception as e:
            log.debug(f"Device Stealth not available: {e}")

        # Try connect on initialization
        log.info("[SharedArduinoConnection] Attempting initial connection...")
        connection_result = self._connect()
        if connection_result:
            log.info("[SharedArduinoConnection] ✅ Initial connection successful")
        else:
            log.warning(
                "[SharedArduinoConnection] ⚠️ Initial connection failed, will retry on first command"
            )

        # Log remapping status
        if self.key_mapping:
            log.info(
                f"[SharedArduinoConnection] Key remapping: {len(self.key_mapping)} mappings, Status: {'ENABLED' if self.remapping_enabled else 'DISABLED'}"
            )
        else:
            log.debug("[SharedArduinoConnection] No key remapping configured")

    def _load_config(self):
        """Load config from vmware_receiver.config.json"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            "vmware_receiver.config.json",
        )
        try:
            if os.path.exists(config_path):
                with open(config_path, "r", encoding="utf-8") as f:
                    config_data = json.load(f)
                    # Load COM port and baudrate if not provided
                    if self.com_port is None:
                        self.com_port = config_data.get("com_port", None)
                    if self.baudrate == 115200:  # Only use config if default
                        self.baudrate = config_data.get("baudrate", 115200)

                    # Load key remapping (only if not already provided)
                    key_mapping_config = config_data.get("key_mapping", {})
                    if key_mapping_config and not self.key_mapping:
                        self.key_mapping = {
                            k.lower(): v.lower() for k, v in key_mapping_config.items()
                        }
                        log.debug(
                            f"Loaded key remapping from vmware_receiver.config.json: {len(self.key_mapping)} mappings"
                        )

                    # Load remapping enabled status
                    if "remapping_enabled" in config_data:
                        self.remapping_enabled = config_data.get(
                            "remapping_enabled", True
                        )

                    if "obfuscation_enabled" in config_data:
                        self.obfuscation_enabled = config_data.get(
                            "obfuscation_enabled", True
                        )
        except Exception as e:
            log.debug(f"Failed to load vmware_receiver.config.json: {e}")

    def _find_arduino_ports(self) -> list:
        """Tìm tất cả COM ports có thể là Arduino"""
        ports = []
        try:
            for port in serial.tools.list_ports.comports():
                ports.append(port.device)
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
            self.connected = True
            return True

        # Determine ports to try
        if self.com_port:
            ports_to_try = [self.com_port]
            log.info(f"Attempting to connect to specified COM port: {self.com_port}")
        else:
            # Auto-detect: try all available ports
            ports_to_try = self._find_arduino_ports()
            log.info(
                f"Auto-detecting Arduino COM port from {len(ports_to_try)} available ports"
            )

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
                    inter_byte_timeout=0.01,
                )

                # Wait for Arduino to initialize
                time.sleep(0.5)

                # Flush any existing data
                self.serial.flush()

                self.connected = True
                self.com_port = port

                # Log successful connection
                device_stealth_status = (
                    "Enabled"
                    if (
                        self.device_stealth
                        and getattr(self.device_stealth, "enabled", False)
                    )
                    else "Disabled"
                )

                log.info("=" * 60)
                log.info("✅ SHARED ARDUINO CONNECTION SUCCESSFUL")
                log.info(f"   Port: {port}")
                log.info(f"   Baudrate: {self.baudrate}")
                log.info(f"   Device Stealth: {device_stealth_status}")
                log.info(
                    f"   Key Remapping: {'Enabled' if self.remapping_enabled else 'Disabled'}"
                )
                if self.key_mapping:
                    log.info(f"   Remapping Keys: {len(self.key_mapping)} mappings")
                log.info(
                    f"   Serial Obfuscation: {'Enabled' if self.obfuscation_enabled else 'Disabled'}"
                )
                log.info("=" * 60)

                self._initialize_obfuscator()

                return True

            except serial.SerialException as e:
                error_str = str(e)
                # Check if port is already in use (Access is denied)
                if "Access is denied" in error_str or "being used" in error_str.lower():
                    log.warning(f"Port {port} is already in use by another process")
                    log.warning(
                        "This should not happen with shared connection. Continuing..."
                    )
                    # Try to continue anyway (maybe we can reuse existing connection)
                    continue
                log.debug(f"Failed to connect to {port}: {e}")
                continue
            except Exception as e:
                log.warning(f"Unexpected error connecting to {port}: {e}")
                continue

        # Failed to connect to all ports
        log.error(
            f"❌ Failed to connect to Arduino on any of {len(ports_to_try)} ports"
        )
        self.connected = False
        return False

    def _map_key(self, key: str) -> str:
        """
        Map vkeys key name sang Arduino key name
        Applies key remapping if enabled

        Args:
            key: vkeys key name (lowercase)

        Returns:
            Arduino key name
        """
        key_lower = key.lower()

        # Step 1: Apply key remapping (game customization) if enabled
        if self.remapping_enabled and self.key_mapping:
            original_key = key_lower
            if key_lower in self.key_mapping:
                key_lower = self.key_mapping[key_lower]
                self.stats["total_remapped"] += 1
                log.debug(f"Key remapping: '{original_key}' → '{key_lower}'")

        # Step 2: Map vkeys key name to Arduino key name (system mapping)
        arduino_key = VKEYS_TO_ARDUINO.get(key_lower, key_lower)

        return arduino_key

    def _initialize_obfuscator(self):
        """Prepare obfuscator instance."""
        if self.obfuscator is None:
            self.obfuscator = SerialObfuscator(enabled=self.obfuscation_enabled)
        else:
            self.obfuscator.enabled = self.obfuscation_enabled
            self.obfuscator.reset()

        if self.obfuscation_enabled:
            log.debug("[SharedArduinoConnection] Serial obfuscation enabled")
        else:
            log.debug("[SharedArduinoConnection] Serial obfuscation disabled")

    def _encode_for_serial(
        self, action: str, arduino_key: Optional[str]
    ) -> List[bytes]:
        """
        Encode command vào frame (obfuscated hoặc ASCII).
        """
        command_key = arduino_key if arduino_key is not None else None

        if not self.obfuscator:
            self._initialize_obfuscator()

        try:
            return self.obfuscator.encode_command(action, command_key)
        except Exception as exc:
            log.error(f"[SharedArduinoConnection] Serial obfuscation error: {exc}")
            # Fallback to ASCII
            return [self._build_plain_command(action, command_key)]

    @staticmethod
    def _build_plain_command(action: str, arduino_key: Optional[str]) -> bytes:
        if action == "all_up":
            return b"all_up\n"
        if not arduino_key:
            raise ValueError("arduino_key is required for %s" % action)
        return f"{action}:{arduino_key}\n".encode("utf-8")

    def send_command(self, action: str, key: str = None) -> bool:
        """
        Gửi command đến Arduino: 'down:a\n' hoặc 'up:a\n' hoặc 'all_up\n'
        Thread-safe với lock

        Args:
            action: 'down', 'up', hoặc 'all_up'
            key: Key name (chỉ dùng cho 'down' và 'up', có thể None cho 'all_up')

        Returns:
            True nếu gửi thành công, False nếu thất bại
        """
        # Validate input
        if action not in ["down", "up", "all_up"]:
            log.warning(f"[SharedArduinoConnection] Invalid action: {action}")
            return False

        if action != "all_up" and (not key or not key.strip()):
            log.warning(f"[SharedArduinoConnection] Key required for action '{action}'")
            return False

        # Thread-safe send
        log.debug(
            f"[SharedArduinoConnection] Sending command: {action}:{key if key else 'all_up'}"
        )
        with self._send_lock:
            if not self.connected or not self.serial or not self.serial.is_open:
                # Try reconnect
                if not self._connect():
                    return False
                # If reconnect successful, continue to send command

            try:
                # Map key name (except for all_up)
                arduino_key = None
                if action != "all_up":
                    arduino_key = self._map_key(key)

                frames = self._encode_for_serial(action, arduino_key)

                # Phase 5: Device Fingerprinting Bypass - Add random timing variation
                import random

                for frame in frames:
                    random_delay = random.uniform(0.0001, 0.002)  # 0.1-2ms
                    time.sleep(random_delay)

                    self.serial.write(frame)
                    self.serial.flush()  # Ensure command is sent immediately

                # Phase 5: Device Stealth - Monitor device properties
                if self.device_stealth:
                    try:
                        devices = self.device_stealth.get_raw_input_devices()
                        arduino_devices = [
                            d for d in devices if d.get("is_arduino", False)
                        ]
                        if arduino_devices:
                            for device in arduino_devices:
                                self.device_stealth.spoof_device_properties(
                                    device["handle"], spoofed_name="USB Keyboard"
                                )
                    except Exception as e:
                        log.debug(f"Device stealth monitoring error: {e}")

                self.stats["total_sent"] += 1
                log.debug(
                    f"[SharedArduinoConnection] ✅ Sent command: {action}:{arduino_key if arduino_key else 'all_up'}"
                )
                return True

            except serial.SerialException as e:
                log.error(
                    f"[SharedArduinoConnection] ❌ Serial error sending command: {e}"
                )
                self.connected = False
                self.stats["total_errors"] += 1
                # Try reconnect
                log.info("[SharedArduinoConnection] Attempting to reconnect...")
                reconnect_result = self._connect()
                if reconnect_result:
                    log.info("[SharedArduinoConnection] ✅ Reconnected successfully")
                else:
                    log.warning("[SharedArduinoConnection] ⚠️ Reconnection failed")
                return False
            except Exception as e:
                log.error(
                    f"[SharedArduinoConnection] ❌ Unexpected error sending command: {e}"
                )
                self.stats["total_errors"] += 1
                return False

    def send_all_up(self) -> bool:
        """Release all keys (emergency cleanup)"""
        return self.send_command("all_up")

    def is_connected(self) -> bool:
        """Check if connected"""
        return self.connected and self.serial and self.serial.is_open

    def get_serial(self) -> Optional[serial.Serial]:
        """
        Get serial.Serial object (for backward compatibility)
        WARNING: Direct access to serial is not thread-safe!
        Use send_command() instead.
        """
        return self.serial if self.is_connected() else None

    def toggle_remapping(self):
        """Toggle key remapping on/off"""
        self.remapping_enabled = not self.remapping_enabled
        status = "ENABLED" if self.remapping_enabled else "DISABLED"
        log.info(f"[SharedArduinoConnection] Key remapping toggled: {status}")

    def set_remapping(self, enabled: bool):
        """Set key remapping enabled/disabled"""
        old_status = "ENABLED" if self.remapping_enabled else "DISABLED"
        self.remapping_enabled = enabled
        new_status = "ENABLED" if self.remapping_enabled else "DISABLED"
        log.info(
            f"[SharedArduinoConnection] Key remapping changed: {old_status} → {new_status}"
        )

    def disconnect(self):
        """Disconnect from Arduino"""
        log.info("[SharedArduinoConnection] Disconnecting from Arduino...")
        with self._send_lock:
            if self.serial and self.serial.is_open:
                try:
                    # Release all keys before disconnecting (send directly, don't call send_all_up to avoid deadlock)
                    log.debug(
                        "[SharedArduinoConnection] Releasing all keys before disconnect..."
                    )
                    try:
                        self.serial.write(b"all_up\n")
                        self.serial.flush()
                        time.sleep(0.1)
                    except Exception as e:
                        log.debug(
                            f"[SharedArduinoConnection] Error sending all_up during disconnect: {e}"
                        )

                    # Close serial connection
                    self.serial.close()
                    log.info("[SharedArduinoConnection] ✅ Disconnected from Arduino")
                except Exception as e:
                    log.error(
                        f"[SharedArduinoConnection] ❌ Error disconnecting from Arduino: {e}"
                    )
                finally:
                    self.connected = False
                    self.serial = None
            else:
                log.debug(
                    "[SharedArduinoConnection] No active connection to disconnect"
                )

    def get_stats(self) -> dict:
        """Get statistics"""
        return self.stats.copy()

    @classmethod
    def get_instance(
        cls,
        com_port: Optional[str] = None,
        baudrate: int = 115200,
        key_mapping: Optional[dict] = None,
        remapping_enabled: bool = True,
    ):
        """
        Get or create singleton instance

        Args:
            com_port: COM port (only used if instance doesn't exist)
            baudrate: Baudrate (only used if instance doesn't exist)
            key_mapping: Key mapping (only used if instance doesn't exist)
            remapping_enabled: Remapping enabled (only used if instance doesn't exist)

        Returns:
            SharedArduinoConnection instance
        """
        if cls._instance is None:
            cls._instance = cls(
                com_port=com_port,
                baudrate=baudrate,
                key_mapping=key_mapping,
                remapping_enabled=remapping_enabled,
            )
        return cls._instance
