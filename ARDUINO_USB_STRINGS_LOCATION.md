# 📍 Vị trí file USBCore.cpp - Thay đổi USB Strings

## ✅ File đã tìm thấy:

**Full Path:**

```
C:\Users\Thanh Thien\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6\cores\arduino\USBCore.cpp
```

**Short Path (từ AppData):**

```
%USERPROFILE%\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6\cores\arduino\USBCore.cpp
```

---

## 🔧 Cách mở và sửa file:

### Option 1: Mở trực tiếp từ File Explorer

1. Nhấn `Windows + R`
2. Paste: `%USERPROFILE%\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6\cores\arduino`
3. Enter → Folder sẽ mở
4. Tìm file `USBCore.cpp`
5. Right-click → **Open with** → Notepad++ hoặc VS Code

### Option 2: Copy path vào Editor

1. Copy path:
    ```
    C:\Users\Thanh Thien\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6\cores\arduino\USBCore.cpp
    ```
2. Mở VS Code hoặc Notepad++
3. File → Open → Paste path → Open

---

## 📝 Dòng cần sửa trong USBCore.cpp:

### Current Status:

File hiện tại **ĐÃ CÓ** code override ở **dòng 24-40**:

```cpp
// --- BEGIN: Override USB identity to mimic Logitech ---
#ifndef USB_VID
  #define USB_VID 0x046D
#endif

#ifndef USB_PID
  #define USB_PID 0xC31C
#endif

#ifndef USB_MANUFACTURER
  #define USB_MANUFACTURER "Logitech"
#endif

#ifndef USB_PRODUCT
  #define USB_PRODUCT "Logitech Gaming Keyboard"
#endif
// --- END: Override USB identity ---
```

### Các dòng khác cần check:

**Dòng 68:**

```cpp
const u8 STRING_PRODUCT[] PROGMEM = USB_PRODUCT;
```

**Dòng 85:**

```cpp
const u8 STRING_MANUFACTURER[] PROGMEM = USB_MANUFACTURER;
```

**Dòng 64-66 (fallback):**

```cpp
#ifndef USB_PRODUCT
#define USB_PRODUCT     "USB IO Board"
#endif
```

**Dòng 70-83 (manufacturer logic):**

```cpp
#if USB_VID == 0x2341
  #define USB_MANUFACTURER "Arduino LLC"
#elif USB_VID == 0x1b4f
  #define USB_MANUFACTURER "SparkFun"
#elif !defined(USB_MANUFACTURER)
  #define USB_MANUFACTURER "Unknown"
#endif
```

---

## ✏️ Cách sửa USB Strings:

### Step 1: Backup file

1. Copy file `USBCore.cpp` → `USBCore.cpp.backup`

### Step 2: Sửa dòng 24-40 (Override section)

**Thay đổi từ:**

```cpp
#ifndef USB_MANUFACTURER
  #define USB_MANUFACTURER "Logitech"
#endif

#ifndef USB_PRODUCT
  #define USB_PRODUCT "Logitech Gaming Keyboard"
#endif
```

**Thành (Option A - Generic):**

```cpp
#ifndef USB_MANUFACTURER
  #define USB_MANUFACTURER "Standard HID Keyboard"
#endif

#ifndef USB_PRODUCT
  #define USB_PRODUCT "USB Keyboard"
#endif
```

**Hoặc (Option B - Microsoft):**

```cpp
#ifndef USB_MANUFACTURER
  #define USB_MANUFACTURER "Microsoft Corp."
#endif

#ifndef USB_PRODUCT
  #define USB_PRODUCT "Microsoft USB Keyboard"
#endif
```

### Step 3: Tìm và sửa STRING_SERIAL_PLACEHOLDER (nếu có)

Tìm dòng có `STRING_SERIAL` hoặc `ISERIAL` và đổi nếu cần.

---

## 📋 Quick Reference - Dòng số cần sửa:

Dựa vào file hiện tại:

| Purpose              | Dòng | Current Value                | Change To                                          |
| -------------------- | ---- | ---------------------------- | -------------------------------------------------- |
| **Manufacturer**     | 34   | `"Logitech"`                 | `"Standard HID Keyboard"` hoặc `"Microsoft Corp."` |
| **Product**          | 38   | `"Logitech Gaming Keyboard"` | `"USB Keyboard"` hoặc `"Microsoft USB Keyboard"`   |
| **Fallback Product** | 65   | `"USB IO Board"`             | `"USB Keyboard"` (optional)                        |

---

## ⚠️ Lưu ý:

1. **File đang dùng Logitech VID/PID:**

    - Line 26: `USB_VID = 0x046D` (Logitech)
    - Line 30: `USB_PID = 0xC31C` (Logitech)

    Nếu muốn đổi VID/PID, sửa dòng 26 và 30.

2. **Sau khi sửa:**

    - Save file
    - **Close Arduino IDE** (nếu đang mở)
    - **Restart Arduino IDE**
    - Recompile sketch để áp dụng changes

3. **Verify:**
    - Upload sketch lên Arduino
    - Mở Device Manager
    - Check device name → Sẽ hiển thị strings mới

---

## 🔍 Tìm Serial String:

Nếu cần đổi Serial Number, tìm trong file:

```cpp
#define ISERIAL "12345678901234567890"
```

Hoặc tìm pattern:

-   `STRING_SERIAL`
-   `ISERIAL`
-   Serial placeholder

---

**Next Step:** Sau khi sửa, restart Arduino IDE và recompile sketch!
