# 🥷 Arduino Stealth Template - Code Changes

## 📋 Template cho các thay đổi cần thiết

### File 1: `boards.txt` - VID/PID Changes

**Location:** `hardware/arduino/avr/boards.txt`

**Find:**

```ini
pro.vid.0=0x2341
pro.pid.0=0x0036
pro.bootloader.vid=0x2341
pro.bootloader.pid=0x0036
```

**Replace with (Option A - Minimal, Safe):**

```ini
pro.vid.0=0x03EB              # Atmel VID (generic, safe)
pro.pid.0=0x2041              # Generic HID Device
pro.bootloader.vid=0x2341     # KEEP bootloader VID (để upload được)
pro.bootloader.pid=0x0036     # KEEP bootloader PID
```

**Replace with (Option B - Full Stealth):**

```ini
pro.vid.0=0x045E              # Microsoft VID
pro.pid.0=0x0745              # Microsoft Keyboard
pro.bootloader.vid=0x045E     # Đổi bootloader VID (cần ISP programmer sau này)
pro.bootloader.pid=0x0036     # Bootloader PID (có thể giữ)
```

---

### File 2: `USBCore.cpp` - USB Strings Changes

**Location:** `hardware/arduino/avr/cores/arduino/USBCore.cpp`

**Find:**

```cpp
#ifdef USB_PRODUCT
#define STRING_PRODUCT        USB_PRODUCT
#else
#define STRING_PRODUCT        "Arduino Leonardo"
#endif

#ifdef USB_MANUFACTURER
#define STRING_MANUFACTURER   USB_MANUFACTURER
#else
#define STRING_MANUFACTURER   "Arduino LLC"
#endif

#ifdef USB_SERIAL_PLACEHOLDER
#define STRING_SERIAL_PLACEHOLDER USB_SERIAL_PLACEHOLDER
#else
#define STRING_SERIAL_PLACEHOLDER "12345678901234567890"
#endif
```

**Replace with (Option A - Generic):**

```cpp
#ifdef USB_PRODUCT
#define STRING_PRODUCT        USB_PRODUCT
#else
#define STRING_PRODUCT        "USB Keyboard"
#endif

#ifdef USB_MANUFACTURER
#define STRING_MANUFACTURER   USB_MANUFACTURER
#else
#define STRING_MANUFACTURER   "Standard HID Keyboard"
#endif

#ifdef USB_SERIAL_PLACEHOLDER
#define STRING_SERIAL_PLACEHOLDER USB_SERIAL_PLACEHOLDER
#else
#define STRING_SERIAL_PLACEHOLDER "00000000000000000000"
#endif
```

**Replace with (Option B - Microsoft):**

```cpp
#define STRING_PRODUCT        "Microsoft USB Keyboard"
#define STRING_MANUFACTURER   "Microsoft Corp."
#define STRING_SERIAL_PLACEHOLDER "00000000000000000000"
```

**Replace with (Option C - Logitech):**

```cpp
#define STRING_PRODUCT        "Logitech USB Keyboard"
#define STRING_MANUFACTURER   "Logitech Inc."
#define STRING_SERIAL_PLACEHOLDER "00000000000000000000"
```

---

### File 3: `HID.cpp` - KbType & TotalKeys Changes

**Location:** `hardware/arduino/avr/cores/arduino/HID.cpp`

**Find HID Report Descriptor:**

```cpp
const u8 _hidReportDescriptor[] PROGMEM = {
    0x05, 0x01,        // Usage Page (Generic Desktop)
    0x09, 0x06,        // Usage (Keyboard)
    0xa1, 0x01,        // Collection (Application)
    // ... more bytes ...
    0x29, 0x65,        // Usage Maximum (0x65 = 101 keys)
    // ... more bytes ...
};
```

**Change TotalKeys (101 → 104):**

```cpp
// Find:
0x29, 0x65,        // Usage Maximum (0x65 = 101 keys)

// Replace with:
0x29, 0x68,        // Usage Maximum (0x68 = 104 keys - US Standard)
```

**Note về KbType:**

-   KbType được Windows determine từ HID usage page
-   Standard US keyboard usage → Windows sẽ detect là KbType 0x04
-   Đảm bảo HID descriptor dùng standard keyboard usage

---

## 📝 Quick Reference

### Common VID/PID Combinations:

```ini
# Generic (Safe)
VID=0x03EB, PID=0x2041

# Microsoft
VID=0x045E, PID=0x0745

# Logitech
VID=0x046D, PID=0xC31C

# Dell
VID=0x413C, PID=0x2107
```

### USB Strings:

```cpp
// Generic
STRING_PRODUCT = "USB Keyboard"
STRING_MANUFACTURER = "Standard HID Keyboard"
STRING_SERIAL = "00000000000000000000"

// Microsoft
STRING_PRODUCT = "Microsoft USB Keyboard"
STRING_MANUFACTURER = "Microsoft Corp."

// Logitech
STRING_PRODUCT = "Logitech USB Keyboard"
STRING_MANUFACTURER = "Logitech Inc."
```

### HID Descriptor Values:

```cpp
// TotalKeys: 101 (Japanese)
0x29, 0x65,        // Usage Maximum (101)

// TotalKeys: 104 (US Standard)
0x29, 0x68,        // Usage Maximum (104)

// KbType: 0x04 (US Standard) - Windows auto-detect từ HID usage
// KbType: 0x07 (Japanese) - Windows auto-detect nếu có Japanese usage
```

---

## ⚠️ Important Notes

1. **Backup trước khi sửa**
2. **Bootloader VID/PID:**
    - Giữ cũ → Vẫn upload được qua USB
    - Đổi → Cần ISP programmer sau này
3. **Strings:**
    - Tránh special characters
    - Tránh unicode (dùng ASCII)
4. **HID Descriptor:**
    - Dùng standard keyboard descriptor
    - Đổi TotalKeys: `0x65` (101) → `0x68` (104)

---

**Ready to implement?** Follow `ARDUINO_STEALTH_GUIDE.md` for step-by-step instructions!
