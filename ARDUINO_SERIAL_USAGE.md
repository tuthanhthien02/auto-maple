# 🤖 Arduino Serial Output - Usage Guide

## 📋 Tổng quan

Bot có thể dùng **Direct Serial** để output qua Arduino USB HID keyboard thay vì SendInput.

**Architecture:**

```
Bot → ArduinoSerialOutput → Serial → Arduino → USB HID → Game
```

---

## ⚙️ Configuration

### **Enable Arduino Serial Output:**

Sửa file `src/common/config.py`:

```python
# Enable Arduino output
use_arduino = True

# Arduino Serial port (None = auto-detect, hoặc chỉ định: "COM13")
arduino_com_port = None  # Auto-detect

# Arduino Serial baudrate
arduino_baudrate = 115200
```

**Hoặc runtime (trong code):**

```python
from src.common import config

config.use_arduino = True
config.arduino_com_port = None  # Auto-detect
config.arduino_baudrate = 115200
```

---

## 🔧 Setup

### **1. Upload Arduino Code**

Đảm bảo Arduino đã upload code:

-   `arduino_hid_keyboard_tcp/arduino_hid_keyboard_tcp.ino`
-   Code này support cả TCP và Serial protocol

### **2. Connect Arduino**

-   Kết nối Arduino Pro Micro vào VMware
-   Arduino sẽ hiện như COM port trong Device Manager

### **3. Enable trong Bot**

Sửa `config.py`:

```python
use_arduino = True
```

---

## 🚀 Usage

### **Automatic (Hybrid Mode):**

Bot tự động chọn Arduino hoặc SendInput dựa vào config:

```python
from src.common import vkeys

# Nếu use_arduino = True và Arduino connected → dùng Arduino
# Nếu use_arduino = False hoặc Arduino unavailable → dùng SendInput
vkeys.press('a', 1)
vkeys.key_down('w')
vkeys.key_up('w')
```

### **Manual (Direct Access):**

```python
from src.common.output_arduino import ArduinoSerialOutput

# Create instance
arduino = ArduinoSerialOutput(com_port=None, baudrate=115200)

# Use Arduino
arduino.press('a', 1)
arduino.key_down('w')
arduino.key_up('w')

# Cleanup
arduino.disconnect()
```

---

## 📊 Key Mapping

Bot tự động map vkeys key names → Arduino key names:

**Examples:**

-   `'a'` → `'a'` (same)
-   `'shift'` → `'lshift'` (Arduino expects specific)
-   `'ctrl'` → `'lctrl'`
-   `'alt'` → `'lalt'`
-   `'space'` → `'space'` (same)
-   `'left'` → `'left'` (same)
-   `'f1'` → `'f1'` (same)

**Full mapping:** Xem `src/common/output_arduino.py` → `VKEYS_TO_ARDUINO`

---

## 🔍 Auto-Detection

### **How it works:**

1. Nếu `arduino_com_port = None` → Bot tự động scan tất cả COM ports
2. Try connect từng port cho đến khi thành công
3. Port đầu tiên connect được = Arduino

### **Log Messages:**

```
INFO: Auto-detecting Arduino COM port from 3 available ports
DEBUG: Trying to connect to COM3...
DEBUG: Trying to connect to COM13...
INFO: ✅ Successfully connected to Arduino on COM13 (baudrate: 115200)
```

---

## ⚠️ Error Handling

### **Connection Failed:**

Nếu Arduino không connect được:

-   Bot tự động fallback về SendInput
-   Log warning: `"Arduino output enabled but connection failed, falling back to SendInput"`

### **Serial Error:**

Nếu Serial connection bị lỗi trong runtime:

-   Bot tự động try reconnect
-   Nếu reconnect thành công → tiếp tục dùng Arduino
-   Nếu reconnect thất bại → fallback về SendInput

### **Disconnect:**

```python
# Emergency release all keys
arduino.release_all()

# Disconnect
arduino.disconnect()
```

---

## 📋 Troubleshooting

### **Problem: Arduino không connect**

**Check:**

1. Arduino đã upload code chưa?
2. Arduino đã connect vào VMware chưa?
3. COM port có đúng không?
4. Baudrate có match không? (default: 115200)

**Solution:**

```python
# Specify COM port manually
config.arduino_com_port = "COM13"
```

### **Problem: Keys không work**

**Check:**

1. Arduino code có đúng không?
2. Key mapping có đúng không?
3. Serial connection có stable không?

**Solution:**

-   Check logs để xem commands có được gửi không
-   Test với Serial Monitor trực tiếp

### **Problem: Latency cao**

**Check:**

1. Baudrate có đúng không? (115200)
2. Serial buffer có bị đầy không?

**Solution:**

-   Tăng baudrate (nếu Arduino support)
-   Check serial write timeout

---

## 🔄 Switch Between Modes

### **Enable Arduino:**

```python
from src.common import config
config.use_arduino = True
```

### **Disable Arduino (use SendInput):**

```python
from src.common import config
config.use_arduino = False
```

**Note:** Cần restart bot để apply changes.

---

## 📊 Comparison

| Feature         | SendInput  | Arduino Serial |
| --------------- | ---------- | -------------- |
| **Latency**     | ~0.1-0.5ms | ~0.5-1ms       |
| **Stealth**     | Low ⚠️     | High ✅        |
| **Hardware**    | None ✅    | Arduino needed |
| **Setup**       | Simple ✅  | Medium         |
| **Reliability** | High ✅    | Medium         |

---

## ✅ Checklist

### **Before Use:**

-   [ ] Arduino code đã upload (`arduino_hid_keyboard_tcp.ino`)
-   [ ] Arduino connected vào VMware
-   [ ] COM port available (check Device Manager)
-   [ ] Config `use_arduino = True`
-   [ ] Bot restarted sau khi đổi config

### **During Use:**

-   [ ] Check logs để verify Arduino connection
-   [ ] Test với simple commands trước
-   [ ] Monitor serial connection status
-   [ ] Verify keys work correctly

---

## 🎯 Quick Start

1. **Upload Arduino code** → `arduino_hid_keyboard_tcp.ino`
2. **Connect Arduino** → VMware
3. **Edit config** → `src/common/config.py`:
    ```python
    use_arduino = True
    arduino_com_port = None  # Auto-detect
    ```
4. **Start bot** → Bot sẽ auto-detect Arduino
5. **Test** → Bot sẽ dùng Arduino cho keyboard output

---

**Ready to use!** 🚀
