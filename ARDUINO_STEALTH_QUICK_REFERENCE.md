# 🎯 Arduino Hardware Input Stealth - Quick Reference

## 📊 **PHASE STATUS**

| Phase | Status | Priority | Time | Next Step |
|-------|--------|----------|------|-----------|
| **Phase 1** | ✅ DONE | ⭐⭐⭐⭐⭐ | 1-2h | - |
| **Phase 2** | ✅ DONE | ⭐⭐⭐⭐ | 2-4h | - |
| **Phase 3** | ⏳ PLAN | ⭐⭐⭐ | 1-3h | Increase Baud Rate |
| **Phase 4** | ⏳ PLAN | ⭐⭐⭐ | 2-4h | Timing Randomization |
| **Phase 5** | ⏳ PLAN | ⭐⭐ | 4-8h | Advanced (Optional) |

---

## 🚀 **NEXT STEPS (Priority Order)**

### **#1: Phase 3.1 - Increase Baud Rate** ⭐⭐⭐ **NEXT**

**Files:**
- `arduino_hid_keyboard/arduino_hid_keyboard.ino` (Line 72)
- `src/common/output_arduino.py` (Line 96, 190)

**Changes:**
```cpp
Serial.begin(921600);  // Arduino
```
```python
baudrate: int = 921600  # Python
```

**Time:** 30 phút
**Difficulty:** ⭐ Easy

---

### **#2: Phase 4.1 - Timing Randomization** ⭐⭐⭐

**Files:**
- `arduino_hid_keyboard/arduino_hid_keyboard.ino` (processCommand)
- `src/common/output_arduino.py` (already has, verify)

**Changes:**
```cpp
delayMicroseconds(random(1000, 10000));  // Arduino
```

**Time:** 2-3 giờ
**Difficulty:** ⭐⭐ Medium

---

### **#3: Phase 4.3 - Micro Pauses** ⭐⭐

**Files:**
- `arduino_hid_keyboard/arduino_hid_keyboard.ino` (processCommand)
- `src/common/output_arduino.py` (already has, verify)

**Changes:**
```cpp
delayMicroseconds(random(500, 2000));  // Arduino
```

**Time:** 1 giờ
**Difficulty:** ⭐ Easy

---

## 📋 **FILES TO MODIFY**

### **Arduino Files:**
- `arduino_hid_keyboard/arduino_hid_keyboard.ino`
  - Line 72: `Serial.begin(921600)`
  - `processCommand()`: Add timing randomization
  - `processCommand()`: Add micro pauses

### **Python Files:**
- `src/common/output_arduino.py`
  - Line 96: `baudrate: int = 921600`
  - Line 190: `serial.Serial(port, 921600)`
  - Already has timing randomization (verify)
  - Already has micro pauses (verify)

---

## ⚠️ **IMPORTANT NOTES**

### **1. Gaussian Distribution:**
- ⚠️ **NOT RECOMMENDED** - Có thể tạo ra patterns nhất quán
- ✅ Use uniform distribution thay vì Gaussian

### **2. Timing Randomization:**
- ✅ Python đã có timing randomization (via `_get_human_like_delay`)
- ⏳ Cần thêm trong Arduino

### **3. Micro Pauses:**
- ✅ Python đã có micro pauses (via `_get_micro_pause`)
- ⏳ Cần thêm trong Arduino

---

## 🎯 **RECOMMENDED ORDER**

1. ✅ **Phase 1: Basic Setup** - DONE
2. ✅ **Phase 2: Device Stealth** - DONE
3. ⏳ **Phase 3.1: Increase Baud Rate** - NEXT (30 phút)
4. ⏳ **Phase 4.1: Timing Randomization** - (2-3 giờ)
5. ⏳ **Phase 4.3: Micro Pauses** - (1 giờ)

**Total Time:** 3-4 giờ
**Result:** ✅ **Hardware Input Stealth** (Good)

---

**REMEMBER:** Bắt đầu từ Phase 3.1 (Increase Baud Rate)! ⭐

