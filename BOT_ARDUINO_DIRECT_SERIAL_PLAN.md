# 🤖 Bot Arduino Direct Serial - Implementation Plan

## 📋 Tổng quan

**Goal:** Thêm Direct Serial support cho bot mà không thay đổi TCP pipeline hiện tại.

**Current State:**

-   ✅ TCP pipeline đã có: `host_sender.py`, `vmware_receiver.py` (không touch)
-   ✅ Bot hiện tại dùng `vkeys.py` với SendInput
-   ✅ Cần thêm Direct Serial mode cho bot

**Target State:**

-   ✅ Bot có thể dùng Direct Serial hoặc SendInput
-   ✅ TCP pipeline vẫn hoạt động bình thường (không đổi)
-   ✅ Config-based selection giữa SendInput và Serial

---

## 🎯 Objectives

### **Primary:**

1. Tạo `ArduinoSerialOutput` module cho Direct Serial
2. Integrate với `vkeys.py` (hybrid mode)
3. Auto-detect Arduino COM port
4. Key mapping từ vkeys → Arduino
5. Error handling & auto-reconnect

### **Secondary:**

1. Config options cho Serial mode
2. Logging & debugging
3. Performance optimization
4. Backward compatibility (SendInput fallback)

---

## 🏗️ Architecture Design

### **New Components:**

```
src/common/
├── output_arduino.py          [NEW] Arduino Serial output module
├── vkeys.py                   [MODIFY] Add hybrid mode
├── config.py                  [MODIFY] Add config options
└── settings.py                [MODIFY] Add GUI settings (optional)
```

### **Data Flow:**

```
Bot → vkeys.press() → Check config.use_arduino
                        │
                        ├─ YES → ArduinoSerialOutput → Serial → Arduino → USB HID → Game
                        │
                        └─ NO  → SendInput (current) → Windows → Game
```

---

## 📝 Implementation Steps

### **Phase 1: Core Module** (Priority: High)

#### **Step 1.1: Create `src/common/output_arduino.py`**

**Components:**

-   `ArduinoSerialOutput` class
    -   `__init__(com_port, baudrate)`
    -   `_connect()` - Auto-detect Arduino
    -   `_find_arduino_ports()` - List COM ports
    -   `send_command(action, key)` - Send "down:a\n" or "up:a\n"
    -   `press(key, n, down_time, up_time)` - Press key N times
    -   `key_down(key)` - Hold key
    -   `key_up(key)` - Release key
    -   `release_all()` - Emergency release all keys

**Key Mapping:**

-   Map vkeys key names → Arduino key names
-   Support full keyboard layout
-   Handle special keys (shift, ctrl, alt, arrows, F-keys)

**Error Handling:**

-   Auto-reconnect on serial error
-   Log errors
-   Fallback to SendInput if Arduino unavailable

**Estimated:** ~200-300 lines

---

#### **Step 1.2: Key Mapping Table**

**Mapping Strategy:**

-   Use `arduino_hid_keyboard_tcp.ino` key names as reference
-   Map vkeys `KEY_MAP` → Arduino key names
-   Handle differences:
    -   vkeys: `'shift'` → Arduino: `'lshift'`
    -   vkeys: `'ctrl'` → Arduino: `'lctrl'`
    -   vkeys: `'alt'` → Arduino: `'lalt'`
    -   Letters/Numbers: Same
    -   Arrows: Same (`'left'`, `'right'`, `'up'`, `'down'`)
    -   F-keys: Same (`'f1'` → `'f1'`)

**Implementation:**

```python
VKEYS_TO_ARDUINO = {
    # Letters (same)
    'a': 'a', 'b': 'b', ..., 'z': 'z',

    # Numbers (same)
    '0': '0', '1': '1', ..., '9': '9',

    # Control keys
    'shift': 'lshift',
    'ctrl': 'lctrl',
    'alt': 'lalt',
    'space': 'space',
    'enter': 'enter',
    'backspace': 'backspace',
    'esc': 'esc',

    # Arrow keys
    'left': 'left',
    'right': 'right',
    'up': 'up',
    'down': 'down',

    # Function keys
    'f1': 'f1', ..., 'f12': 'f12',

    # ... full mapping
}
```

---

### **Phase 2: Integration** (Priority: High)

#### **Step 2.1: Update `src/common/vkeys.py`**

**Changes:**

1. Add config check at top of file
2. Modify `press()` function:
    - Check `config.use_arduino`
    - If enabled and Arduino available → use Arduino
    - Else → use SendInput (current)
3. Modify `key_down()` function (same logic)
4. Modify `key_up()` function (same logic)
5. Rename current implementations to `_press_sendinput()`, etc.

**Code Structure:**

```python
# At top
from src.common import config

# Lazy import Arduino output
_arduino_output = None

def _get_arduino_output():
    """Get or create Arduino output instance"""
    global _arduino_output
    if _arduino_output is None and config.use_arduino:
        try:
            from src.common.output_arduino import ArduinoSerialOutput
            _arduino_output = ArduinoSerialOutput(
                com_port=config.arduino_com_port,
                baudrate=config.arduino_baudrate
            )
        except Exception as e:
            log.warning(f"Failed to initialize Arduino: {e}")
            _arduino_output = False
    return _arduino_output

# Modify press()
@utils.run_if_enabled
def press(key, n, down_time=0.05, up_time=0.1):
    """Press key - Arduino or SendInput"""
    if config.use_arduino:
        arduino = _get_arduino_output()
        if arduino and arduino.connected:
            arduino.press(key, n, down_time, up_time)
            return

    # Fallback to SendInput
    _press_sendinput(key, n, down_time, up_time)

# Rename current implementation
def _press_sendinput(key, n, down_time=0.05, up_time=0.1):
    """Original SendInput implementation"""
    # ... existing code ...
```

**Estimated:** ~50-100 lines modified

---

#### **Step 2.2: Update `src/common/config.py`**

**Add config variables:**

```python
# Arduino Serial output config
use_arduino = False  # Enable/disable Arduino output
arduino_com_port = None  # None = auto-detect, or "COM13"
arduino_baudrate = 115200  # Serial baudrate
```

**Estimated:** ~5-10 lines

---

### **Phase 3: Configuration** (Priority: Medium)

#### **Step 3.1: Config File Support** (Optional)

**Add `arduino_serial.config.json`:**

```json
{
    "use_arduino": false,
    "com_port": null,
    "baudrate": 115200
}
```

**Or integrate vào existing config system**

---

#### **Step 3.2: GUI Settings** (Optional)

**Add to `src/common/settings.py`:**

```python
self.arduino = SettingsSection(
    use_arduino=BooleanVar(value=False),
    com_port=StringVar(value=None),
    baudrate=IntVar(value=115200)
)
```

**Estimated:** ~20-30 lines

---

### **Phase 4: Testing & Optimization** (Priority: Medium)

#### **Step 4.1: Unit Testing**

**Test Cases:**

1. ✅ Arduino connection (auto-detect)
2. ✅ Key mapping (all keys)
3. ✅ `press()` function
4. ✅ `key_down()` / `key_up()` functions
5. ✅ Error handling (disconnect, reconnect)
6. ✅ Fallback to SendInput

---

#### **Step 4.2: Integration Testing**

**Test Cases:**

1. ✅ Bot với Serial mode enabled
2. ✅ Bot với Serial mode disabled (SendInput)
3. ✅ Switch between modes
4. ✅ Real routine execution
5. ✅ Error recovery

---

#### **Step 4.3: Performance Testing**

**Metrics:**

-   Latency measurement (Serial vs SendInput)
-   Throughput (keys/second)
-   Error rate
-   Resource usage

---

## 📊 File Structure

### **New Files:**

```
src/common/
└── output_arduino.py          [NEW] ~250-300 lines
```

### **Modified Files:**

```
src/common/
├── vkeys.py                   [MODIFY] ~50-100 lines
├── config.py                  [MODIFY] ~5-10 lines
└── settings.py                [MODIFY] ~20-30 lines (optional)
```

### **Total Changes:**

-   **New:** ~1 file (~250-300 lines)
-   **Modified:** ~2-3 files (~75-140 lines)
-   **Total:** ~325-440 lines

---

## 🔧 Technical Details

### **1. Serial Communication**

**Protocol:** Same as TCP version

```
"down:a\n"    - Press 'a'
"up:a\n"      - Release 'a'
"all_up\n"    - Release all keys
```

**Library:** `pyserial`

**Settings:**

-   Baudrate: 115200
-   Timeout: 0.1s
-   Write timeout: 0.1s

---

### **2. Auto-Detection**

**Strategy:**

1. If `com_port` specified → use that port
2. Else → scan all COM ports
3. Try connect to each port
4. First successful connection = Arduino

**Port Detection:**

```python
import serial.tools.list_ports

ports = [p.device for p in serial.tools.list_ports.comports()]
# Try each port until success
```

---

### **3. Error Handling**

**Error Types:**

1. **SerialException** (port disconnected)

    - Try reconnect
    - Fallback to SendInput after N retries

2. **Write Timeout**

    - Log warning
    - Continue (skip command)

3. **Connection Failed**
    - Log error
    - Mark Arduino unavailable
    - Fallback to SendInput

**Reconnect Logic:**

-   Auto-reconnect on error
-   Max retries: 3
-   Retry delay: 1s

---

### **4. Key Mapping**

**Reference:**

-   Arduino code: `arduino_hid_keyboard_tcp.ino` keyMap[]
-   vkeys code: `src/common/vkeys.py` KEY_MAP

**Mapping Rules:**

-   Letters: Same ('a' → 'a')
-   Numbers: Same ('0' → '0')
-   Modifiers: vkeys generic → Arduino specific
    -   'shift' → 'lshift'
    -   'ctrl' → 'lctrl'
    -   'alt' → 'lalt'
-   Arrows: Same ('left' → 'left')
-   F-keys: Same ('f1' → 'f1')

---

## 📋 Implementation Checklist

### **Phase 1: Core Module**

-   [ ] Create `src/common/output_arduino.py`
-   [ ] Implement `ArduinoSerialOutput` class
-   [ ] Implement auto-detection
-   [ ] Implement key mapping
-   [ ] Implement error handling
-   [ ] Add logging

### **Phase 2: Integration**

-   [ ] Update `vkeys.py` with hybrid mode
-   [ ] Add config variables
-   [ ] Test hybrid mode
-   [ ] Test fallback to SendInput

### **Phase 3: Configuration**

-   [ ] Add config file support (optional)
-   [ ] Add GUI settings (optional)
-   [ ] Test config loading

### **Phase 4: Testing**

-   [ ] Unit tests
-   [ ] Integration tests
-   [ ] Performance tests
-   [ ] Real game tests

---

## ⚠️ Risks & Mitigations

### **Risk 1: Serial Port Conflicts**

**Issue:** Port already in use
**Mitigation:** Check port availability, handle gracefully

### **Risk 2: Key Mapping Errors**

**Issue:** Wrong keys sent to Arduino
**Mitigation:** Comprehensive mapping table, test all keys

### **Risk 3: Performance Impact**

**Issue:** Serial slower than SendInput
**Mitigation:** Optimize serial writes, test latency

### **Risk 4: Error Recovery**

**Issue:** Arduino disconnects during use
**Mitigation:** Auto-reconnect, fallback to SendInput

---

## 🎯 Success Criteria

### **Functional:**

-   ✅ Bot can use Direct Serial mode
-   ✅ Auto-detect Arduino COM port
-   ✅ All keys work correctly
-   ✅ Fallback to SendInput works
-   ✅ Error handling works

### **Performance:**

-   ✅ Latency acceptable (~0.5-1ms)
-   ✅ No performance degradation vs SendInput
-   ✅ Stable under load

### **Compatibility:**

-   ✅ Backward compatible (SendInput still works)
-   ✅ TCP pipeline unchanged
-   ✅ Config-based selection

---

## 📅 Timeline Estimate

### **Phase 1:** 2-3 hours

-   Core module implementation
-   Key mapping
-   Error handling

### **Phase 2:** 1-2 hours

-   Integration với vkeys.py
-   Config setup
-   Basic testing

### **Phase 3:** 1 hour (optional)

-   Config file support
-   GUI settings

### **Phase 4:** 2-3 hours

-   Testing
-   Bug fixes
-   Optimization

**Total:** ~6-9 hours

---

## 🚀 Next Steps

1. **Review plan** với team/user
2. **Create `output_arduino.py`** module
3. **Integrate với `vkeys.py`**
4. **Test với real Arduino**
5. **Deploy & monitor**

---

**Ready to start?** 🎯
