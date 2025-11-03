# 🔍 SendInput vs Arduino Serial - So sánh chi tiết

## 📋 Tổng quan

Bot hiện tại hỗ trợ **2 cách output keyboard**:

1. **SendInput** (Simulate Key Press) - Default
2. **Arduino Serial** (Direct Serial) - Optional

---

## 🔧 Technical Differences

### **1. SendInput (Simulate Key Press)**

**Implementation:**

```python
# src/common/vkeys.py
user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
```

**How it works:**

-   **Windows API** (`SendInput`) được gọi trực tiếp từ Python
-   **Software-based simulation** của keyboard events
-   Input được inject vào Windows message queue
-   Game nhận input như từ một **virtual keyboard driver**

**Flow:**

```
Bot → Python → SendInput API → Windows Message Queue → Game
```

**Characteristics:**

-   ✅ **No hardware required**
-   ✅ **Fast latency** (~0.1-0.5ms)
-   ✅ **Simple setup**
-   ❌ **Software detection** - Dễ bị detect
-   ❌ **May be blocked** bởi một số games/anti-cheat

---

### **2. Arduino Serial (Direct Serial)**

**Implementation:**

```python
# src/common/output_arduino.py
self.serial.write(command.encode('utf-8'))
# Command: "down:a\n" or "up:a\n"
```

**How it works:**

-   **Serial communication** với Arduino Pro Micro qua COM port
-   Arduino nhận command qua Serial (text protocol)
-   Arduino **emulates USB HID keyboard** (hardware device)
-   Game nhận input như từ một **real hardware keyboard**

**Flow:**

```
Bot → Python → Serial (COM) → Arduino → USB HID → Game
```

**Characteristics:**

-   ✅ **Hardware-based** - Harder to detect
-   ✅ **Real keyboard device** - Works like physical keyboard
-   ✅ **Stealth** - Appears as genuine hardware
-   ❌ **Hardware required** (Arduino Pro Micro)
-   ❌ **Slightly higher latency** (~0.5-1ms)
-   ❌ **More complex setup**

---

## 📊 Chi tiết so sánh

| Feature                | SendInput           | Arduino Serial           |
| ---------------------- | ------------------- | ------------------------ |
| **Type**               | Software simulation | Hardware device          |
| **Latency**            | ~0.1-0.5ms          | ~0.5-1ms                 |
| **Stealth**            | Low ⚠️              | High ✅                  |
| **Hardware**           | None ✅             | Arduino needed           |
| **Setup**              | Simple ✅           | Medium                   |
| **Reliability**        | High ✅             | Medium                   |
| **Detection Risk**     | High ⚠️             | Low ✅                   |
| **Game Compatibility** | May be blocked      | Works like real keyboard |
| **Cost**               | Free ✅             | ~$5-10 (Arduino)         |
| **Maintenance**        | Low ✅              | Medium                   |

---

## 🔍 Technical Deep Dive

### **SendInput - How it works:**

```python
# vkeys.py
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002

# Create input structure
x = Input(
    type=INPUT_KEYBOARD,
    ki=KeyboardInput(
        wVk=KEY_MAP[key],  # Virtual key code
        dwFlags=0  # Key down
    )
)

# Send to Windows
user32.SendInput(1, ctypes.byref(x), ctypes.sizeof(x))
```

**Key Points:**

-   Uses **Virtual Key Codes** (VK codes)
-   Windows treats it as **synthetic input**
-   Some games can distinguish synthetic vs hardware input
-   Anti-cheat may flag as "programmatic input"

---

### **Arduino Serial - How it works:**

```python
# output_arduino.py
# Send command via Serial
command = f"down:{arduino_key}\n"
self.serial.write(command.encode('utf-8'))

# Arduino receives:
# "down:a\n"
```

**Arduino Code:**

```cpp
// arduino_hid_keyboard_tcp.ino
void processCommand(String cmd) {
    // Parse: "down:a" or "up:a"
    if (cmd.startsWith("down:")) {
        String key = cmd.substring(5);
        pressKey(key);
    } else if (cmd.startsWith("up:")) {
        String key = cmd.substring(3);
        releaseKey(key);
    }
}

void pressKey(String key) {
    uint8_t keyCode = getKeyCode(key);  // Map to HID keycode
    Keyboard.press(keyCode);  // USB HID library
}
```

**Key Points:**

-   Uses **USB HID protocol** (standard keyboard protocol)
-   Arduino appears as **real hardware keyboard** to OS
-   Game sees it as **genuine hardware input**
-   Anti-cheat sees a **physical USB device**

---

## 🎯 Detection Differences

### **SendInput Detection:**

**What games/anti-cheat see:**

-   ✅ **Software injection** vào message queue
-   ✅ **Virtual key codes** thay vì hardware scan codes
-   ✅ **Input flags** indicate synthetic input
-   ✅ **API call patterns** (SendInput sequence)

**Detection methods:**

-   Check if input comes from **hardware vs software**
-   Monitor **Windows API calls** (SendInput)
-   Analyze **input timing patterns**
-   Verify **keyboard device origin**

**Risk level:** ⚠️ **High**

---

### **Arduino Serial Detection:**

**What games/anti-cheat see:**

-   ✅ **USB HID device** (hardware keyboard)
-   ✅ **Real hardware scan codes**
-   ✅ **Standard USB protocol**
-   ✅ **Physical device presence**

**Detection methods:**

-   Very difficult - Arduino appears as **genuine hardware**
-   Would need to:
    -   Analyze **hardware VID/PID** (can be changed)
    -   Check **device driver signatures**
    -   Monitor **USB traffic patterns** (advanced)

**Risk level:** ✅ **Low** (with proper stealth config)

---

## ⚡ Performance Comparison

### **Latency:**

**SendInput:**

```
Python call → Windows API → Message queue → Game
Time: ~0.1-0.5ms
```

**Arduino Serial:**

```
Python call → Serial write → Arduino → USB HID → Game
Time: ~0.5-1ms
```

**Difference:** Arduino có latency cao hơn ~0.4-0.5ms do:

-   Serial communication overhead (~0.1-0.2ms)
-   Arduino processing time (~0.1-0.2ms)
-   USB HID protocol overhead (~0.1-0.2ms)

**Note:** Với bot gaming, difference này **không đáng kể** (< 1ms).

---

### **Throughput:**

**SendInput:**

-   ✅ **High throughput** - No hardware limit
-   ✅ Can send thousands of inputs/second

**Arduino Serial:**

-   ✅ **Medium throughput** - Limited by Serial baudrate (115200 baud)
-   ✅ ~1000-2000 commands/second (đủ cho bot)

---

## 🔒 Stealth Comparison

### **SendInput Stealth:**

**Vulnerabilities:**

1. **Software injection detection**
    - Games can detect SendInput API calls
    - Anti-cheat monitors Windows API usage
2. **Input pattern detection**
    - Synthetic input có timing patterns khác hardware
    - Missing hardware scan codes
3. **Device origin detection**
    - Input không đến từ physical device
    - No USB device signature

**Mitigation:**

-   ❌ **Limited options** - Vẫn là software injection
-   ❌ Có thể thêm **timing randomization** (bot đã có)
-   ❌ Vẫn dễ bị detect với advanced anti-cheat

---

### **Arduino Serial Stealth:**

**Advantages:**

1. **Hardware device**
    - Arduino appears as **real USB keyboard**
    - OS treats it as **physical hardware**
2. **Standard protocol**
    - Uses **USB HID** (industry standard)
    - Same protocol như real keyboards
3. **Device signature**
    - Can modify **VID/PID** (Vendor/Product ID)
    - Can change **USB strings** (manufacturer name)
    - Can adjust **KbType** và **TotalKeys**

**Mitigation:**

-   ✅ **Hardware-based** - Rất khó detect
-   ✅ Có thể **customize device signature**
-   ✅ **Stealth guide** đã có sẵn (`ARDUINO_STEALTH_GUIDE.md`)

---

## 🎮 Game Compatibility

### **SendInput:**

**Works with:**

-   ✅ Most games (older games)
-   ✅ Games không có anti-cheat
-   ✅ Games cho phép programmatic input

**Blocked by:**

-   ❌ Games với **advanced anti-cheat** (EAC, BattlEye)
-   ❌ Games detect **synthetic input**
-   ❌ Games require **hardware input only**

---

### **Arduino Serial:**

**Works with:**

-   ✅ **All games** (appears as real keyboard)
-   ✅ Games với **anti-cheat** (hardware device)
-   ✅ Games require **hardware input**
-   ✅ **Any game** that accepts keyboard input

**Blocked by:**

-   ❌ None (appears as genuine hardware)

---

## 💡 Use Cases

### **When to use SendInput:**

1. ✅ **Development/Testing**
    - No hardware required
    - Faster iteration
2. ✅ **Games without anti-cheat**
    - Simple games
    - Older games
3. ✅ **Low stealth requirement**
    - Private servers
    - Single-player games

---

### **When to use Arduino Serial:**

1. ✅ **Production/Live use**
    - Maximum stealth
    - Anti-cheat protection
2. ✅ **Games with anti-cheat**
    - EAC, BattlEye, etc.
    - Competitive games
3. ✅ **Long-term usage**
    - Reduced detection risk
    - Hardware investment worth it

---

## 🔄 Hybrid Mode (Current Implementation)

Bot hiện tại hỗ trợ **hybrid mode**:

```python
# src/common/vkeys.py
def press(key, n, down_time=0.05, up_time=0.1):
    # Check if Arduino is enabled and available
    arduino = _get_arduino_output()
    if arduino and arduino.connected:
        # Use Arduino (stealth)
        arduino.press(key, n, down_time, up_time)
        return

    # Fallback to SendInput (reliable)
    _press_sendinput(key, n, down_time, up_time)
```

**Benefits:**

-   ✅ **Automatic fallback** if Arduino unavailable
-   ✅ **Easy switching** via config (`use_arduino = True/False`)
-   ✅ **Best of both worlds** - Stealth when needed, reliability always

---

## 📋 Summary

### **Key Differences:**

1. **Stealth:**

    - **SendInput:** Software simulation → **Dễ detect**
    - **Arduino:** Hardware device → **Khó detect**

2. **Latency:**

    - **SendInput:** ~0.1-0.5ms (faster)
    - **Arduino:** ~0.5-1ms (slightly slower)

3. **Setup:**

    - **SendInput:** No setup (ready to use)
    - **Arduino:** Requires hardware + setup

4. **Reliability:**

    - **SendInput:** High (no hardware dependency)
    - **Arduino:** Medium (depends on hardware)

5. **Compatibility:**
    - **SendInput:** Most games (may be blocked)
    - **Arduino:** All games (appears as real hardware)

---

## ✅ Recommendation

**Use SendInput when:**

-   ✅ Development/testing
-   ✅ Games without anti-cheat
-   ✅ Quick testing/prototyping

**Use Arduino Serial when:**

-   ✅ Production/live use
-   ✅ Games with anti-cheat
-   ✅ Maximum stealth required
-   ✅ Long-term usage

**Current Implementation:**

-   ✅ **Hybrid mode** - Best of both worlds
-   ✅ Easy switching via config
-   ✅ Automatic fallback

---

**Ready to use!** 🚀
