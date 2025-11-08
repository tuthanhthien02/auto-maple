# 🎯 Arduino Phase 2 Implementation - Device Stealth

## 📋 **PHASE 2: DEVICE STEALTH IMPLEMENTATION**

### **Step 2.1: Change Arduino Device Name**
### **Step 2.2: Change Arduino VID/PID (Optional)**

---

## 🔧 **METHOD 1: MODIFY ARDUINO CORE FILES** (RECOMMENDED)

### **Step 1: Tìm Arduino Core Files**

**Chạy script:**
```batch
python find_arduino_core.py
```

**Hoặc tìm thủ công:**
- `C:\Program Files\Arduino\hardware\arduino\avr\`
- `C:\Users\<YOUR_USER>\AppData\Local\Arduino15\packages\arduino\hardware\avr\`

---

### **Step 2: Modify USBCore.cpp**

**File cần sửa:** `cores/arduino/USBCore.cpp`

**Tìm dòng:**
```cpp
#define STRING_PRODUCT        L"Arduino Micro"
#define STRING_MANUFACTURER   L"Arduino LLC"
```

**Thay đổi thành:**
```cpp
#define STRING_PRODUCT        L"USB Keyboard"
#define STRING_MANUFACTURER   L"Generic"
```

**Hoặc:**
```cpp
#define STRING_PRODUCT        L"HID Keyboard"
#define STRING_MANUFACTURER   L"Standard"
```

---

### **Step 3: Modify boards.txt (Optional - Change VID/PID)**

**File cần sửa:** `boards.txt`

**Tìm dòng:**
```ini
pro.menu.usb.0.name=USB Keyboard
pro.menu.usb.0.vid.0=0x2341
pro.menu.usb.0.pid.0=0x0037
```

**Thay đổi thành:**
```ini
pro.menu.usb.0.name=USB Keyboard
pro.menu.usb.0.vid.0=0x046D  # Logitech VID (example)
pro.menu.usb.0.pid.0=0xC077  # Generic keyboard PID (example)
```

**Lưu ý:** VID/PID phải là valid USB IDs. Không dùng VID/PID đã được đăng ký bởi nhà sản xuất khác.

---

### **Step 4: Upload Firmware**

1. **Mở Arduino IDE**
2. **Select Board:** Tools → Board → Arduino Leonardo (Pro Micro uses Leonardo bootloader)
3. **Select Port:** Tools → Port → COM13
4. **Upload:** Sketch → Upload

---

## 🔧 **METHOD 2: SCRIPT TỰ ĐỘNG** (EASIER)

### **Step 1: Chạy Script**

**Script sẽ:**
1. Tìm Arduino core files
2. Backup files gốc
3. Modify device name
4. Hướng dẫn upload firmware

```batch
python modify_arduino_device_name.py
```

---

## 📝 **MANUAL STEPS**

### **Step 1: Backup Core Files**

```batch
# Backup USBCore.cpp
copy "C:\Program Files\Arduino\hardware\arduino\avr\cores\arduino\USBCore.cpp" "USBCore.cpp.backup"
```

---

### **Step 2: Modify USBCore.cpp**

**Mở file:** `C:\Program Files\Arduino\hardware\arduino\avr\cores\arduino\USBCore.cpp`

**Tìm và thay đổi:**

**Before:**
```cpp
#define STRING_PRODUCT        L"Arduino Micro"
#define STRING_MANUFACTURER   L"Arduino LLC"
```

**After:**
```cpp
#define STRING_PRODUCT        L"USB Keyboard"
#define STRING_MANUFACTURER   L"Generic"
```

---

### **Step 3: Upload Firmware**

1. **Mở Arduino IDE**
2. **File → Open:** `arduino_hid_keyboard\arduino_hid_keyboard.ino`
3. **Tools → Board:** Arduino Leonardo
4. **Tools → Port:** COM13
5. **Sketch → Upload**

---

## ✅ **VERIFY DEVICE NAME**

### **Step 1: Check Device Manager**

1. **Windows + X → Device Manager**
2. **Keyboards → Tìm device mới**
3. **Right-click → Properties → Details**
4. **Property:** Device description
5. **Value:** Should be "USB Keyboard" (not "Arduino Micro")

---

### **Step 2: Check Raw Input Devices**

**Chạy script:**
```python
python check_arduino_device_name.py
```

**Hoặc check manual:**
```python
import win32api
# Check device name
```

---

## 🎯 **EXPECTED RESULTS**

### **Before Phase 2:**
- Device Name: "Arduino Micro"
- Manufacturer: "Arduino LLC"
- VID/PID: 0x2341 / 0x0037 (Arduino)

### **After Phase 2:**
- Device Name: "USB Keyboard"
- Manufacturer: "Generic"
- VID/PID: 0x046D / 0xC077 (Logitech - example) or unchanged

---

## ⚠️ **IMPORTANT NOTES**

### **1. Backup Files:**
- ✅ **ALWAYS backup** core files trước khi modify
- ✅ Core files sẽ bị restore khi update Arduino IDE

### **2. Arduino IDE Updates:**
- ⚠️ **Core files sẽ bị restore** khi update Arduino IDE
- ✅ Cần modify lại sau mỗi lần update

### **3. VID/PID:**
- ⚠️ **Không dùng VID/PID đã được đăng ký** bởi nhà sản xuất khác
- ✅ Có thể dùng generic VID/PID hoặc giữ nguyên Arduino VID/PID

---

## 🚀 **QUICK START**

### **Option 1: Manual (Recommended)**

1. **Backup core files**
2. **Modify USBCore.cpp**
3. **Upload firmware to COM13**
4. **Verify device name**

### **Option 2: Script (Easier)**

1. **Chạy script:** `python modify_arduino_device_name.py`
2. **Follow instructions**
3. **Upload firmware to COM13**
4. **Verify device name**

---

**REMEMBER:** Phase 2 giảm detection risk đáng kể bằng cách change device name! ⭐

