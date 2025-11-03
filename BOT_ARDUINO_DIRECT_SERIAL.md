# 🤖 Bot → Arduino Direct Serial Pipeline

## 📋 Tổng quan

**Scenario:**

-   Bot chạy trên VMware
-   Game chạy trên VMware (cùng VM)
-   Không cần latency requirement
-   Có Arduino hardware

**Architecture:**

```
Bot (Python) → Serial → Arduino → USB HID → Game
```

**Latency:** ~0.5-1ms (không có network overhead)

---

## ✅ ƯU ĐIỂM - So với TCP Pipeline

### **1. Lower Latency** ⚡

-   ✅ **Direct Serial**: ~0.5-1ms (vs ~2ms với TCP)
-   ✅ **No Network Overhead**: Không cần TCP
-   ✅ **Simpler Path**: Bot → Serial → Arduino → Game

### **2. Simpler Setup** 🔧

-   ✅ **No Network Config**: Không cần IP, port
-   ✅ **No TCP Scripts**: Không cần host_sender.py, vmware_receiver.py
-   ✅ **Direct Connection**: Serial trực tiếp từ bot
-   ✅ **Fewer Components**: Ít moving parts = ít failure points

### **3. Better Reliability** 🛡️

-   ✅ **No Network Dependency**: Không lo TCP drop
-   ✅ **Local Only**: Serial USB = reliable
-   ✅ **Fewer Failure Points**: Bot → Serial → Arduino

### **4. Easier Integration** 💻

-   ✅ **Simple Module**: Chỉ cần 1 module mới
-   ✅ **No Network Logic**: Không cần reconnect, health checks
-   ✅ **Straightforward**: Serial read/write only

---

## 🏗️ Proposed Architecture

### **Option 1: Direct Serial Module** (Recommended)

```python
# src/common/output_arduino.py
import serial
import time
from src.common.logger import get_logger

log = get_logger(__name__)

class ArduinoOutput:
    def __init__(self, com_port=None, baudrate=115200):
        self.serial = None
        self.com_port = com_port
        self.baudrate = baudrate
        self.connected = False
        self._connect()

    def _connect(self):
        """Auto-detect hoặc connect to Arduino"""
        if self.com_port:
            # Use specified port
            ports_to_try = [self.com_port]
        else:
            # Auto-detect Arduino
            ports_to_try = self._find_arduino_ports()

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
                log.info(f"Connected to Arduino on {port}")
                return
            except Exception as e:
                log.warning(f"Failed to connect to {port}: {e}")
                continue

        log.error("Failed to connect to Arduino")
        self.connected = False

    def _find_arduino_ports(self):
        """Find potential Arduino COM ports"""
        import serial.tools.list_ports
        ports = []
        for port in serial.tools.list_ports.comports():
            ports.append(port.device)
        return ports

    def send_command(self, action, key):
        """Send command to Arduino: 'down:a\\n' or 'up:a\\n'"""
        if not self.connected or not self.serial:
            return False

        try:
            command = f"{action}:{key}\n"
            self.serial.write(command.encode('utf-8'))
            return True
        except Exception as e:
            log.error(f"Failed to send command: {e}")
            self.connected = False
            # Try reconnect
            self._connect()
            return False

    def press(self, key, n, down_time=0.05, up_time=0.1):
        """Press key N times with timing"""
        from src.common import utils

        if not utils.run_if_enabled(lambda: None):
            return

        key = key.lower()

        for i in range(n):
            # Key down
            self.send_command('down', key)
            time.sleep(down_time)

            # Key up
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

    def release_all(self):
        """Release all keys (emergency)"""
        if self.connected:
            try:
                self.serial.write(b"all_up\n")
            except:
                pass
```

---

## 🔌 Integration với Bot

### **Step 1: Update vkeys.py**

```python
# src/common/vkeys.py

# At top of file
from src.common import config

# Arduino output (lazy import)
_arduino_output = None

def _get_arduino_output():
    """Get or create Arduino output instance"""
    global _arduino_output
    if _arduino_output is None and config.use_arduino:
        try:
            from src.common.output_arduino import ArduinoOutput
            _arduino_output = ArduinoOutput(
                com_port=config.arduino_com_port,
                baudrate=config.arduino_baudrate
            )
        except Exception as e:
            log.warning(f"Failed to initialize Arduino output: {e}")
            _arduino_output = False  # Mark as unavailable
    return _arduino_output

# Modify press() function
@utils.run_if_enabled
def press(key, n, down_time=0.05, up_time=0.1):
    """Press key - uses Arduino if enabled, otherwise SendInput"""

    # Check if Arduino is enabled and available
    if config.use_arduino:
        arduino = _get_arduino_output()
        if arduino and arduino.connected:
            # Use Arduino
            arduino.press(key, n, down_time, up_time)
            return

    # Fallback to SendInput (current method)
    _press_sendinput(key, n, down_time, up_time)

# Rename current press to _press_sendinput
def _press_sendinput(key, n, down_time=0.05, up_time=0.1):
    """Original SendInput implementation"""
    # ... existing code ...

# Similar for key_down() and key_up()
def key_down(key):
    if config.use_arduino:
        arduino = _get_arduino_output()
        if arduino and arduino.connected:
            arduino.key_down(key)
            return

    # Fallback to SendInput
    _key_down_sendinput(key)

def key_up(key):
    if config.use_arduino:
        arduino = _get_arduino_output()
        if arduino and arduino.connected:
            arduino.key_up(key)
            return

    # Fallback to SendInput
    _key_up_sendinput(key)
```

---

## ⚙️ Configuration

### **Add to settings.py**

```python
# src/common/settings.py

class Settings:
    def __init__(self):
        # ... existing settings ...

        # Arduino output settings
        self.arduino = SettingsSection(
            use_arduino=BooleanVar(value=False),
            com_port=StringVar(value=None),  # None = auto-detect
            baudrate=IntVar(value=115200)
        )
```

### **Or add to config.py**

```python
# src/common/config.py

# Add to Config class or as module-level config
arduino_config = {
    'use_arduino': False,
    'com_port': None,  # Auto-detect if None
    'baudrate': 115200
}
```

---

## 📊 Key Mapping

### **Map vkeys keys → Arduino key names**

```python
# src/common/output_arduino.py

# Key mapping: vkeys key names → Arduino key names
KEY_MAPPING = {
    # Letters (same)
    'a': 'a', 'b': 'b', 'c': 'c', # ... etc

    # Numbers (same)
    '0': '0', '1': '1', # ... etc

    # Control keys
    'space': 'space',
    'shift': 'lshift',  # Arduino expects 'lshift'
    'ctrl': 'lctrl',
    'alt': 'lalt',
    'backspace': 'backspace',
    'enter': 'enter',
    'esc': 'esc',

    # Arrow keys
    'left': 'left',
    'right': 'right',
    'up': 'up',
    'down': 'down',

    # Function keys
    'f1': 'f1', 'f2': 'f2', # ... etc
}

def _map_key(self, key):
    """Map vkeys key name to Arduino key name"""
    return KEY_MAPPING.get(key.lower(), key.lower())
```

---

## 🚀 Implementation Steps

### **Phase 1: Basic Integration**

1. ✅ Create `src/common/output_arduino.py`
2. ✅ Add config options (`use_arduino`, `com_port`, `baudrate`)
3. ✅ Update `vkeys.py` với hybrid mode
4. ✅ Test với simple commands
5. ✅ Verify Arduino receives commands

### **Phase 2: Full Integration**

1. ✅ Map all keys correctly
2. ✅ Test với real routines
3. ✅ Handle errors gracefully
4. ✅ Add auto-reconnect logic
5. ✅ Test với real game

### **Phase 3: Optimization**

1. ✅ Fine-tune timing nếu cần
2. ✅ Optimize serial write
3. ✅ Add connection health checks
4. ✅ Performance testing

---

## 🔧 Technical Details

### **Serial Communication**

```python
# Example serial communication
serial.write(b"down:a\n")  # Press 'a'
time.sleep(0.05)
serial.write(b"up:a\n")    # Release 'a'
```

**Protocol:** Same as TCP version (`action:key\n`)

### **Auto-Detection**

```python
# Find Arduino port
import serial.tools.list_ports

for port in serial.tools.list_ports.comports():
    if 'arduino' in port.description.lower() or \
       'ch340' in port.description.lower() or \
       'ch341' in port.description.lower():
        # Potential Arduino port
        pass
```

### **Error Handling**

```python
try:
    serial.write(command.encode('utf-8'))
except serial.SerialException:
    # Port disconnected, try reconnect
    self._connect()
except Exception as e:
    log.error(f"Serial error: {e}")
    # Fallback to SendInput
    return False
```

---

## 📋 Comparison: Direct Serial vs TCP

| Feature         | Direct Serial         | TCP Pipeline             |
| --------------- | --------------------- | ------------------------ |
| **Latency**     | ~0.5-1ms ✅           | ~1.5-2ms                 |
| **Setup**       | Simple ✅             | Complex                  |
| **Components**  | 1 module ✅           | 2 scripts                |
| **Network**     | No ✅                 | Required                 |
| **Reliability** | High ✅               | Medium                   |
| **Use Case**    | Bot + Game same VM ✅ | Bot + Game different VMs |

---

## ✅ Benefits cho Use Case của bạn

### **Bot + Game cùng VMware:**

1. ✅ **No Network Overhead**: Không cần TCP
2. ✅ **Simpler Setup**: Chỉ cần 1 module
3. ✅ **Lower Latency**: ~0.5-1ms (vs ~2ms)
4. ✅ **Better Reliability**: Serial USB = stable
5. ✅ **Easy Integration**: Thêm vào bot code
6. ✅ **Same Stealth**: Vẫn là Arduino HID (hardware keyboard)

---

## 🎯 Final Recommendation

**✅ HỢP LÝ & TỐI ƯU cho use case của bạn:**

-   ✅ **Direct Serial** thay vì TCP
-   ✅ **Simple Integration** với bot
-   ✅ **Lower Latency** than TCP
-   ✅ **Same Stealth** benefits
-   ✅ **Easier to maintain**

**Implementation Priority:**

1. Create `output_arduino.py` module
2. Integrate với `vkeys.py` (hybrid mode)
3. Add config options
4. Test với real game

---

**Ready to implement?** 🚀
