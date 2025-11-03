# 🎮 Arduino Key Remapping Guide

## 📋 Tổng quan

Arduino Serial Output hỗ trợ **key remapping** cho game customization, tương tự như `vmware_receiver.py`.

**Vị trí remapping:** `src/common/output_arduino.py` → `_map_key()` method

---

## 🔧 Configuration

### **1. Config File (`src/common/config.py`):**

```python
# Key remapping for game customization
arduino_key_mapping = {
    'a': 'rbracket',   # Press 'a' → outputs ']'
    'w': 'lbracket',   # Press 'w' → outputs '['
    'e': 'p'          # Press 'e' → outputs 'p'
}

# Enable/disable key remapping
arduino_remapping_enabled = True
```

### **2. Runtime Configuration:**

```python
from src.common import config

# Set remapping
config.arduino_key_mapping = {'a': 'rbracket', 'w': 'lbracket'}
config.arduino_remapping_enabled = True

# Restart bot to apply changes
```

---

## 🎯 Key Remapping Location

### **Location: `src/common/output_arduino.py`**

**Method:** `_map_key(key: str) -> str`

**Flow:**

```python
def _map_key(self, key: str) -> str:
    key_lower = key.lower()

    # Step 1: Apply key remapping (game customization) if enabled
    if self.remapping_enabled and self.key_mapping:
        if key_lower in self.key_mapping:
            key_lower = self.key_mapping[key_lower]  # Remap: 'a' → 'rbracket'

    # Step 2: Map vkeys key name to Arduino key name (system mapping)
    arduino_key = VKEYS_TO_ARDUINO.get(key_lower, key_lower)  # 'rbracket' → 'rbracket'

    return arduino_key
```

**Process:**

1. **Key remapping** (game customization) - `'a'` → `'rbracket'`
2. **System mapping** (vkeys → Arduino) - `'rbracket'` → `'rbracket'` (already correct)

---

## ✅ Toggle Remapping

### **1. Runtime Toggle:**

```python
from src.common.output_arduino import ArduinoSerialOutput

arduino = ArduinoSerialOutput()

# Toggle remapping on/off
arduino.toggle_remapping()  # Toggle

# Set remapping enabled/disabled
arduino.set_remapping(True)   # Enable
arduino.set_remapping(False)  # Disable
```

### **2. Config Toggle:**

```python
from src.common import config

# Enable/disable remapping
config.arduino_remapping_enabled = True   # Enable
config.arduino_remapping_enabled = False  # Disable

# Restart bot to apply changes
```

### **3. Hotkey Toggle (Future Enhancement):**

Có thể thêm hotkey để toggle remapping tương tự `vmware_receiver.py` (End key), nhưng hiện tại **chưa implement** vì bot không có keyboard hook.

**Future option:**

-   Add keyboard hook trong bot để listen hotkey
-   Hoặc use GUI toggle button

---

## 📊 Usage Examples

### **Example 1: Basic Remapping**

**Config:**

```python
# src/common/config.py
arduino_key_mapping = {
    'a': 'rbracket',   # a → ]
    'w': 'lbracket',   # w → [
    'e': 'p'          # e → p
}
arduino_remapping_enabled = True
```

**Result:**

-   Bot calls `vkeys.press('a', 1)` → Arduino outputs `']'`
-   Bot calls `vkeys.press('w', 1)` → Arduino outputs `'['`
-   Bot calls `vkeys.press('e', 1)` → Arduino outputs `'p'`

---

### **Example 2: Toggle Remapping**

**Runtime:**

```python
from src.common import vkeys

# Press 'a' with remapping enabled (a → ])
vkeys.press('a', 1)

# Disable remapping
arduino = _get_arduino_output()
if arduino:
    arduino.set_remapping(False)

# Press 'a' without remapping (a → a)
vkeys.press('a', 1)

# Enable remapping again
if arduino:
    arduino.set_remapping(True)
```

---

### **Example 3: Command Book with Remapping**

**Command Book:**

```python
# resources/command_books/kanna.py
from src.common.vkeys import press

class Key:
    JUMP = 'space'      # Will be remapped if config.arduino_key_mapping['space'] exists
    TELEPORT = 'e'      # Will be remapped if config.arduino_key_mapping['e'] exists
```

**Config:**

```python
arduino_key_mapping = {
    'e': 'p'  # Teleport key 'e' → outputs 'p'
}
```

**Result:**

-   `press(Key.TELEPORT, 1)` → Arduino outputs `'p'` (remapped)
-   Remapping works automatically với tất cả bot functions!

---

## 🔑 Supported Arduino Key Names

**Remapping sử dụng Arduino key names:**

-   Letters: `'a'`, `'b'`, `'c'`, ... `'z'`
-   Numbers: `'0'`, `'1'`, ... `'9'`
-   Control: `'shift'`, `'ctrl'`, `'alt'`, `'space'`, `'enter'`, `'backspace'`, `'esc'`, `'tab'`, `'caps'`
-   Navigation: `'pgup'`, `'pgdn'`, `'end'`, `'home'`, `'insert'`, `'delete'`
-   Arrows: `'left'`, `'right'`, `'up'`, `'down'`
-   Function: `'f1'`, `'f2'`, ... `'f12'`
-   Special chars: `'semicolon'`, `'equals'`, `'comma'`, `'minus'`, `'period'`, `'slash'`, `'grave'`, `'lbracket'`, `'backslash'`, `'rbracket'`, `'quote'`

**Xem `src/common/output_arduino.py` → `VKEYS_TO_ARDUINO` dictionary để xem full list.**

---

## 📋 Statistics

**Remapping statistics:**

```python
from src.common.output_arduino import ArduinoSerialOutput

arduino = ArduinoSerialOutput()
print(f"Total remapped: {arduino.stats['total_remapped']}")
```

**Logs:**

-   `[INFO] Key remapping: 3 mappings, Status: ENABLED`
-   `[DEBUG] Key remapping: 'a' → 'rbracket'`
-   `[INFO] Key remapping: ENABLED` (when toggled)

---

## ⚠️ Important Notes

### **1. Remapping vs System Mapping:**

**Remapping (game customization):**

-   `'a'` → `'rbracket'` (game-specific)

**System mapping (vkeys → Arduino):**

-   `'shift'` → `'shift'` (system requirement)
-   `'page up'` → `'pgup'` (system requirement)

**Order:**

1. Remapping applied first (game customization)
2. System mapping applied second (vkeys → Arduino)

---

### **2. Key Names:**

**Use Arduino key names trong remapping:**

-   ✅ `'rbracket'` (correct)
-   ❌ `']'` (wrong - Arduino doesn't have `']'` in keyMap)

---

### **3. Remapping Persistence:**

**Config-based remapping:**

-   Loaded on initialization
-   Persists until bot restart
-   Can be changed via `config.arduino_key_mapping`

**Runtime remapping:**

-   Can be toggled via `arduino.toggle_remapping()`
-   Can be changed via `arduino.set_remapping(True/False)`
-   Changes persist until bot restart

---

## ✅ Summary

**Remapping location:**

-   ✅ `src/common/output_arduino.py` → `_map_key()` method
-   ✅ `src/common/config.py` → `arduino_key_mapping` config

**Toggle remapping:**

-   ✅ `arduino.toggle_remapping()` - Toggle on/off
-   ✅ `arduino.set_remapping(True/False)` - Set enabled/disabled
-   ✅ `config.arduino_remapping_enabled` - Config-based

**Usage:**

-   ✅ Works với tất cả bot functions (`press()`, `key_down()`, `key_up()`)
-   ✅ Works với Command Books và Routines
-   ✅ Automatic - không cần code changes

---

**Ready to use!** 🚀
