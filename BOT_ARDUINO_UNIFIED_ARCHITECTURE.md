# 🤖 Bot → Arduino Unified Architecture

## 📋 Tổng quan

**Use Cases:**

1. **Host → VMware qua TCP** (Remote control từ Host sang VMware)
2. **Direct Serial** (Bot và Game cùng VMware)

**Architecture:**

```
Bot → Output Module → [TCP Mode | Serial Mode] → Arduino → USB HID → Game
```

---

## ✅ Đánh giá: HỢP LÝ

### **Ưu điểm:**

1. ✅ **Flexibility**: Support cả 2 use cases
2. ✅ **Scalability**: Có thể extend thêm modes sau
3. ✅ **Backward Compatible**: Có thể switch giữa modes
4. ✅ **Reuse Code**: Chia sẻ logic giữa 2 modes
5. ✅ **Better Testing**: Test cả 2 scenarios

### **Nhược điểm:**

1. ⚠️ **More Complex**: Cần manage 2 modes
2. ⚠️ **More Code**: Cần implement cả 2
3. ⚠️ **Config Complexity**: Cần config cho từng mode

**Verdict:** **✅ HỢP LÝ** - Flexibility quan trọng hơn complexity nhỏ!

---

## 🏗️ Proposed Unified Architecture

### **Architecture Diagram:**

```
┌─────────────────────────────────────────────────────────┐
│                    Auto-Maple Bot                       │
│                                                         │
│  Bot → vkeys.press() → OutputManager → [Mode Selector] │
└─────────────────────────────────────────────────────────┘
                        │
                        ▼
        ┌───────────────┴───────────────┐
        │                               │
        ▼                               ▼
┌───────────────┐            ┌─────────────────┐
│   TCP Mode    │            │  Serial Mode     │
│               │            │                 │
│ host_sender   │            │ Direct Serial   │
│   → TCP →     │            │   → Serial →    │
│ vmware_       │            │   Arduino       │
│ receiver      │            │                 │
└───────────────┘            └─────────────────┘
        │                               │
        └───────────────┬───────────────┘
                        ▼
                ┌─────────────┐
                │   Arduino   │
                │  Pro Micro  │
                └─────────────┘
                        │
                        ▼
                ┌─────────────┐
                │     Game    │
                └─────────────┘
```

---

## 🔧 Implementation Design

### **Option 1: Unified Output Module** (Recommended)

```python
# src/common/output_arduino.py

from enum import Enum
from src.common.logger import get_logger

log = get_logger(__name__)

class OutputMode(Enum):
    """Output mode enumeration"""
    SENDINPUT = "sendinput"      # Current method
    ARDUINO_SERIAL = "serial"    # Direct Serial
    ARDUINO_TCP = "tcp"          # TCP Network

class ArduinoOutputManager:
    """Unified Arduino output manager"""

    def __init__(self, mode, config=None):
        self.mode = OutputMode(mode) if isinstance(mode, str) else mode
        self.config = config or {}
        self.output = None
        self.connected = False
        self._init_output()

    def _init_output(self):
        """Initialize output based on mode"""
        try:
            if self.mode == OutputMode.ARDUINO_SERIAL:
                self.output = ArduinoSerialOutput(
                    com_port=self.config.get('com_port'),
                    baudrate=self.config.get('baudrate', 115200)
                )
            elif self.mode == OutputMode.ARDUINO_TCP:
                self.output = ArduinoTCPOutput(
                    vmware_ip=self.config.get('vmware_ip'),
                    vmware_port=self.config.get('vmware_port', 12345)
                )
            elif self.mode == OutputMode.SENDINPUT:
                # Use existing SendInput (no output object needed)
                self.output = None
                self.connected = True
            else:
                raise ValueError(f"Unknown output mode: {self.mode}")

            self.connected = self.output is None or self.output.connected

        except Exception as e:
            log.error(f"Failed to initialize output mode {self.mode}: {e}")
            self.connected = False

    def press(self, key, n, down_time=0.05, up_time=0.1):
        """Press key - unified interface"""
        if self.mode == OutputMode.SENDINPUT:
            # Use existing SendInput
            from src.common.vkeys import _press_sendinput
            _press_sendinput(key, n, down_time, up_time)
        elif self.output and self.connected:
            self.output.press(key, n, down_time, up_time)

    def key_down(self, key):
        """Hold key down"""
        if self.mode == OutputMode.SENDINPUT:
            from src.common.vkeys import _key_down_sendinput
            _key_down_sendinput(key)
        elif self.output and self.connected:
            self.output.key_down(key)

    def key_up(self, key):
        """Release key"""
        if self.mode == OutputMode.SENDINPUT:
            from src.common.vkeys import _key_up_sendinput
            _key_up_sendinput(key)
        elif self.output and self.connected:
            self.output.key_up(key)


class ArduinoSerialOutput:
    """Direct Serial output (Bot + Game cùng VM)"""

    def __init__(self, com_port=None, baudrate=115200):
        import serial
        import serial.tools.list_ports
        import time

        self.com_port = com_port
        self.baudrate = baudrate
        self.serial = None
        self.connected = False
        self._connect()

    def _connect(self):
        """Auto-detect hoặc connect to Arduino"""
        import serial
        import serial.tools.list_ports
        import time

        if self.com_port:
            ports_to_try = [self.com_port]
        else:
            # Auto-detect Arduino
            ports_to_try = [p.device for p in serial.tools.list_ports.comports()]

        for port in ports_to_try:
            try:
                self.serial = serial.Serial(
                    port,
                    self.baudrate,
                    timeout=0.1,
                    write_timeout=0.1
                )
                time.sleep(0.5)  # Wait for Arduino init
                self.connected = True
                log.info(f"Connected to Arduino via Serial on {port}")
                return
            except Exception as e:
                log.warning(f"Failed to connect to {port}: {e}")
                continue

        log.error("Failed to connect to Arduino via Serial")
        self.connected = False

    def send_command(self, action, key):
        """Send command to Arduino: 'down:a\\n' or 'up:a\\n'"""
        if not self.connected or not self.serial:
            return False

        try:
            command = f"{action}:{key}\n"
            self.serial.write(command.encode('utf-8'))
            return True
        except Exception as e:
            log.error(f"Failed to send serial command: {e}")
            self.connected = False
            self._connect()  # Try reconnect
            return False

    def press(self, key, n, down_time=0.05, up_time=0.1):
        """Press key N times"""
        import time
        from src.common import utils

        if not utils.run_if_enabled(lambda: None):
            return

        key = key.lower()

        for i in range(n):
            self.send_command('down', key)
            time.sleep(down_time)
            self.send_command('up', key)
            time.sleep(up_time)

    def key_down(self, key):
        """Hold key down"""
        key = key.lower()
        self.send_command('down', key)

    def key_up(self, key):
        """Release key"""
        key = key.lower()
        self.send_command('up', key)


class ArduinoTCPOutput:
    """TCP Network output (Host → VMware)"""

    def __init__(self, vmware_ip, vmware_port=12345):
        # Import host_sender logic
        try:
            from host_sender import HostSender

            self.sender = HostSender(
                vmware_ip=vmware_ip,
                vmware_port=vmware_port
            )
            self.sender.start()

            # Wait for connection
            import time
            max_wait = 5.0  # 5 seconds
            wait_time = 0
            while wait_time < max_wait and not self.sender.connected:
                time.sleep(0.1)
                wait_time += 0.1

            if self.sender.connected:
                self.connected = True
                log.info(f"Connected to VMware via TCP at {vmware_ip}:{vmware_port}")
            else:
                self.connected = False
                log.error(f"Failed to connect to VMware via TCP")

        except Exception as e:
            log.error(f"Failed to initialize TCP output: {e}")
            self.connected = False
            self.sender = None

    def press(self, key, n, down_time=0.05, up_time=0.1):
        """Press key N times"""
        import time
        from src.common import utils

        if not utils.run_if_enabled(lambda: None):
            return

        if not self.connected or not self.sender:
            return

        key = key.lower()

        for i in range(n):
            self.sender.send_key(key, 'down')
            time.sleep(down_time)
            self.sender.send_key(key, 'up')
            time.sleep(up_time)

    def key_down(self, key):
        """Hold key down"""
        if self.connected and self.sender:
            key = key.lower()
            self.sender.send_key(key, 'down')

    def key_up(self, key):
        """Release key"""
        if self.connected and self.sender:
            key = key.lower()
            self.sender.send_key(key, 'up')

    def stop(self):
        """Stop TCP connection"""
        if self.sender:
            self.sender.stop()
```

---

## 🔌 Integration với Bot

### **Update vkeys.py**

```python
# src/common/vkeys.py

from src.common import config
from src.common.output_arduino import ArduinoOutputManager, OutputMode

# Global output manager
_output_manager = None

def _get_output_manager():
    """Get or create output manager instance"""
    global _output_manager

    if _output_manager is None:
        # Determine mode from config
        mode = config.get('output_mode', 'sendinput')  # Default: SendInput

        # Build config based on mode
        output_config = {}

        if mode == 'serial':
            output_config = {
                'com_port': config.get('arduino_com_port'),
                'baudrate': config.get('arduino_baudrate', 115200)
            }
        elif mode == 'tcp':
            output_config = {
                'vmware_ip': config.get('arduino_vmware_ip'),
                'vmware_port': config.get('arduino_vmware_port', 12345)
            }

        try:
            _output_manager = ArduinoOutputManager(mode=mode, config=output_config)
        except Exception as e:
            log.warning(f"Failed to initialize output manager: {e}")
            _output_manager = None

    return _output_manager

# Modify press() function
@utils.run_if_enabled
def press(key, n, down_time=0.05, up_time=0.1):
    """Press key - unified interface"""

    manager = _get_output_manager()
    if manager:
        manager.press(key, n, down_time, up_time)
    else:
        # Fallback to SendInput
        _press_sendinput(key, n, down_time, up_time)

# Similar for key_down() and key_up()
def key_down(key):
    manager = _get_output_manager()
    if manager:
        manager.key_down(key)
    else:
        _key_down_sendinput(key)

def key_up(key):
    manager = _get_output_manager()
    if manager:
        manager.key_up(key)
    else:
        _key_up_sendinput(key)
```

---

## ⚙️ Configuration

### **Option 1: Add to config.py**

```python
# src/common/config.py

# Add output configuration
output_config = {
    'output_mode': 'sendinput',  # 'sendinput', 'serial', 'tcp'

    # Serial mode config (khi mode='serial')
    'arduino_com_port': None,  # Auto-detect if None
    'arduino_baudrate': 115200,

    # TCP mode config (khi mode='tcp')
    'arduino_vmware_ip': '192.168.1.100',
    'arduino_vmware_port': 12345
}
```

### **Option 2: Add to settings.py**

```python
# src/common/settings.py

class Settings:
    def __init__(self):
        # ... existing settings ...

        # Output mode settings
        self.output = SettingsSection(
            mode=StringVar(value='sendinput'),  # 'sendinput', 'serial', 'tcp'

            # Serial mode
            arduino_com_port=StringVar(value=None),
            arduino_baudrate=IntVar(value=115200),

            # TCP mode
            arduino_vmware_ip=StringVar(value='192.168.1.100'),
            arduino_vmware_port=IntVar(value=12345)
        )
```

---

## 📊 Use Case Mapping

### **Use Case 1: Host → VMware qua TCP**

**Setup:**

```python
output_config = {
    'output_mode': 'tcp',
    'arduino_vmware_ip': '192.168.1.100',
    'arduino_vmware_port': 12345
}
```

**Requirements:**

-   ✅ Bot chạy trên Host
-   ✅ Game chạy trên VMware
-   ✅ VMware có `vmware_receiver.py` đang chạy
-   ✅ Arduino kết nối vào VMware

**Flow:**

```
Bot (Host) → TCP → vmware_receiver.py → Serial → Arduino → USB HID → Game
```

---

### **Use Case 2: Direct Serial**

**Setup:**

```python
output_config = {
    'output_mode': 'serial',
    'arduino_com_port': None,  # Auto-detect
    'arduino_baudrate': 115200
}
```

**Requirements:**

-   ✅ Bot chạy trên VMware
-   ✅ Game chạy trên VMware (cùng VM)
-   ✅ Arduino kết nối vào VMware

**Flow:**

```
Bot (VMware) → Serial → Arduino → USB HID → Game
```

---

## 🎯 Benefits

### **1. Flexibility** ✅

-   Support cả 2 use cases
-   Easy switch giữa modes
-   Config-based selection

### **2. Code Reuse** ✅

-   Unified interface (`press()`, `key_down()`, `key_up()`)
-   Shared logic (key mapping, timing)
-   Easy to extend

### **3. Backward Compatible** ✅

-   Default: SendInput (existing behavior)
-   Fallback nếu Arduino unavailable
-   No breaking changes

### **4. Maintainability** ✅

-   Single module for all output modes
-   Clear separation of concerns
-   Easy to test

---

## 🚀 Implementation Plan

### **Phase 1: Core Module**

1. ✅ Create `src/common/output_arduino.py`
2. ✅ Implement `ArduinoOutputManager`
3. ✅ Implement `ArduinoSerialOutput`
4. ✅ Implement `ArduinoTCPOutput`
5. ✅ Add `OutputMode` enum

### **Phase 2: Integration**

1. ✅ Update `vkeys.py` với unified interface
2. ✅ Add config options
3. ✅ Test với SendInput mode (backward compatible)
4. ✅ Test Serial mode
5. ✅ Test TCP mode

### **Phase 3: Testing & Optimization**

1. ✅ Test với real game (Serial mode)
2. ✅ Test với real game (TCP mode)
3. ✅ Optimize latency
4. ✅ Add error handling
5. ✅ Performance testing

---

## 📋 Configuration Examples

### **Example 1: Use Direct Serial**

```python
# config.py hoặc settings
output_config = {
    'output_mode': 'serial',
    'arduino_com_port': None,  # Auto-detect
    'arduino_baudrate': 115200
}
```

### **Example 2: Use TCP Network**

```python
# config.py hoặc settings
output_config = {
    'output_mode': 'tcp',
    'arduino_vmware_ip': '192.168.1.100',
    'arduino_vmware_port': 12345
}
```

### **Example 3: Use SendInput (Default)**

```python
# config.py hoặc settings
output_config = {
    'output_mode': 'sendinput'
}
```

---

## ✅ Final Verdict

**✅ HỢP LÝ & TỐI ƯU:**

1. ✅ **Support cả 2 use cases** - Flexibility cao
2. ✅ **Unified Architecture** - Dễ maintain
3. ✅ **Backward Compatible** - Không breaking changes
4. ✅ **Easy to Extend** - Có thể thêm modes sau
5. ✅ **Code Reuse** - Shared logic

**Recommendation:** **Implement Unified Architecture** 🚀

---

**Ready to implement?** 🎯
