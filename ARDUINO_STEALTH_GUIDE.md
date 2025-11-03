# 🥷 Hướng dẫn Full Stealth cho Arduino Pro Micro

## 📋 Tổng quan

Guide này hướng dẫn cách cải thiện stealth cho Arduino Pro Micro để trông giống một keyboard thật:

1. **Thay đổi VID/PID** - Mimic keyboard phổ biến
2. **Thay đổi USB Strings** - Manufacturer, Product, Serial
3. **Thay đổi KbType** - Từ Japanese (0x07) → US Standard (0x04)
4. **Thay đổi TotalKeys** - Từ 101 → 104 (US layout)

---

## ⚠️ QUAN TRỌNG - ĐỌC TRƯỚC KHI BẮT ĐẦU

### Risks:

1. **Sau khi đổi VID/PID:**

    - Arduino IDE có thể không nhận board → Cần ISP programmer để upload code mới
    - Bootloader cũng cần đổi VID/PID nếu muốn upload qua USB
    - Cần backup bootloader hiện tại

2. **Legal:**

    - Sử dụng VID của hãng khác có thể vi phạm điều khoản
    - Khuyến khích dùng VID tự sở hữu hoặc generic VID

3. **Irreversible:**
    - Một khi đổi VID/PID và upload, không thể upload code mới qua USB nếu không có ISP programmer

### Backup:

-   **Backup bootloader hiện tại** (nếu có thể)
-   **Backup USB core files** trước khi sửa
-   **Save Arduino sketch** hiện tại

---

## 📍 Tìm Arduino Core Files

### Windows - Arduino IDE Installation Paths:

**Option 1: Arduino IDE Installation (Common)**

```
C:\Program Files\Arduino\hardware\arduino\avr\
```

**Option 2: User AppData (Arduino 1.8.13+)**

```
C:\Users\<YOUR_USERNAME>\AppData\Local\Arduino15\packages\arduino\hardware\avr\<VERSION>\
```

**Option 3: Portable Installation**

```
<PORTABLE_PATH>\portable\packages\arduino\hardware\avr\<VERSION>\
```

### Files cần sửa:

```
hardware/arduino/avr/
├── boards.txt                                    ← VID/PID + board definition
├── cores/arduino/
│   ├── USBCore.cpp                              ← USB strings + HID descriptor
│   ├── USBCore.h                                ← USB definitions
│   ├── HID.cpp                                  ← HID keyboard descriptor
│   └── HID.h                                    ← HID definitions
```

---

## 🔧 STEP 1: Thay đổi VID/PID trong boards.txt

### 1.1. Tìm boards.txt

**Location:**

```
hardware/arduino/avr/boards.txt
```

### 1.2. Tìm dòng Pro Micro definition

Tìm section:

```ini
##############################################################

pro.menu.cpu.16MHzatmega32U4=ATmega32U4 (5V, 16 MHz)

##############################################################
```

### 1.3. Tìm dòng với `pro.vid` và `pro.pid`

Tìm dòng như:

```ini
pro.vid.0=0x2341
pro.pid.0=0x0036
```

### 1.4. Thay đổi VID/PID

**Option A: Microsoft Keyboard (Recommended - Common)**

```ini
pro.vid.0=0x045E    # Microsoft VID
pro.pid.0=0x0745    # Microsoft Keyboard (generic)
```

**Option B: Logitech Keyboard**

```ini
pro.vid.0=0x046D    # Logitech VID
pro.pid.0=0xC31C    # Logitech Keyboard (generic)
```

**Option C: Dell Keyboard**

```ini
pro.vid.0=0x413C    # Dell VID
pro.pid.0=0x2107    # Dell Keyboard (generic)
```

**Option D: Generic HID (Safe)**

```ini
pro.vid.0=0x03EB    # Atmel VID (generic, safe)
pro.pid.0=0x2041    # Generic HID Device
```

### 1.5. Lưu ý về bootloader VID/PID

Nếu có dòng `pro.bootloader.`:

```ini
pro.bootloader.vid=0x2341
pro.bootloader.pid=0x0036
```

**Cũng cần đổi:**

```ini
pro.bootloader.vid=0x045E    # Match với pro.vid.0
pro.bootloader.pid=0x0036    # Có thể giữ hoặc đổi
```

**⚠️ Warning:** Đổi bootloader VID/PID sẽ làm Arduino không nhận được qua USB để upload code. Cần ISP programmer sau này.

---

## 🔧 STEP 2: Thay đổi USB Strings

### 2.1. Tìm USBCore.cpp

**Location:**

```
hardware/arduino/avr/cores/arduino/USBCore.cpp
```

### 2.2. Tìm USB String Definitions

Tìm section như:

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

### 2.3. Thay đổi Strings

**Option A: Generic Keyboard (Recommended)**

```cpp
#define STRING_PRODUCT        "USB Keyboard"
#define STRING_MANUFACTURER   "Standard HID Keyboard"
#define STRING_SERIAL_PLACEHOLDER "00000000000000000000"
```

**Option B: Microsoft Keyboard**

```cpp
#define STRING_PRODUCT        "Microsoft USB Keyboard"
#define STRING_MANUFACTURER   "Microsoft Corp."
#define STRING_SERIAL_PLACEHOLDER "00000000000000000000"
```

**Option C: Logitech Keyboard**

```cpp
#define STRING_PRODUCT        "Logitech USB Keyboard"
#define STRING_MANUFACTURER   "Logitech Inc."
#define STRING_SERIAL_PLACEHOLDER "00000000000000000000"
```

**Option D: Dell Keyboard**

```cpp
#define STRING_PRODUCT        "Dell USB Keyboard"
#define STRING_MANUFACTURER   "Dell Inc."
#define STRING_SERIAL_PLACEHOLDER "00000000000000000000"
```

### 2.4. Tìm và sửa String Tables

Tìm array như:

```cpp
static const PROGMEM char string0[] = STRING_LANGUAGE;
static const PROGMEM char string1[] = STRING_MANUFACTURER;
static const PROGMEM char string2[] = STRING_PRODUCT;
static const PROGMEM char string3[] = STRING_SERIAL_PLACEHOLDER;
```

Strings này sẽ tự động dùng definitions ở trên, không cần sửa.

---

## 🔧 STEP 3: Thay đổi KbType (0x07 → 0x04)

### 3.1. Tìm HID Keyboard Descriptor

**Location:**

```
hardware/arduino/avr/cores/arduino/HID.cpp
```

### 3.2. Tìm HID Report Descriptor

Tìm section:

```cpp
const u8 HID_REPORT_DESCRIPTOR[] PROGMEM = {
    0x05, 0x01,        // Usage Page (Generic Desktop Ctrls)
    0x09, 0x06,        // Usage (Keyboard)
    0xa1, 0x01,        // Collection (Application)
    // ... more bytes ...
};
```

### 3.3. Tìm KbType Byte

KbType thường ở trong HID descriptor, nhưng **Arduino HID library không expose KbType trực tiếp**.

**Windows nhận KbType từ USB device descriptor**, không phải HID descriptor.

### 3.4. Cách đổi KbType (Phức tạp hơn)

**Option A: Dùng Raw HID Library (Custom)**

Thay vì `Keyboard.h`, dùng custom HID library với descriptor tùy chỉnh:

```cpp
// Custom HID descriptor with US Keyboard (0x04)
const u8 KeyboardReportDescriptor[] = {
    0x05, 0x01,        // Usage Page (Generic Desktop)
    0x09, 0x06,        // Usage (Keyboard)
    0xa1, 0x01,        // Collection (Application)
    0x85, 0x01,        // Report ID (1)
    // ... HID descriptor ...
};

// Set keyboard type in descriptor
// Note: KbType is determined by Windows based on HID usage, not directly set
```

**Option B: Modify Arduino Core (Advanced)**

Cần modify USB device descriptor trong `USBCore.cpp`:

-   Tìm USB device descriptor structure
-   Modify `bDeviceClass`, `bDeviceSubClass`, `bDeviceProtocol`
-   Hoặc dùng custom HID report descriptor

**⚠️ Note:** KbType được Windows xác định từ HID usage page/usage, không phải từ một byte cụ thể. Để đổi KbType:

-   Dùng standard HID keyboard descriptor (US layout)
-   Windows sẽ tự detect là US Keyboard (0x04) thay vì Japanese (0x07)

### 3.5. Verify HID Descriptor

HID descriptor chuẩn cho US Keyboard:

```cpp
// Standard US Keyboard HID Descriptor
const u8 KeyboardReportDescriptor[] = {
    0x05, 0x01,        // Usage Page (Generic Desktop)
    0x09, 0x06,        // Usage (Keyboard)
    0xa1, 0x01,        // Collection (Application)
    0x85, 0x01,        // Report ID
    0x05, 0x07,        // Usage Page (Key Codes)
    0x19, 0xe0,        // Usage Minimum (0xE0 = Left Control)
    0x29, 0xe7,        // Usage Maximum (0xE7 = Right GUI)
    0x15, 0x00,        // Logical Minimum (0)
    0x25, 0x01,        // Logical Maximum (1)
    0x75, 0x01,        // Report Size (1)
    0x95, 0x08,        // Report Count (8 = 8 modifier keys)
    0x81, 0x02,        // Input (Data,Var,Abs,NWrp,Lin,Pref,NNul,Bit)
    0x95, 0x01,        // Report Count (1)
    0x75, 0x08,        // Report Size (8)
    0x81, 0x01,        // Input (Const) - Reserved byte
    0x95, 0x06,        // Report Count (6)
    0x75, 0x08,        // Report Size (8)
    0x15, 0x00,        // Logical Minimum (0)
    0x25, 0x65,        // Logical Maximum (101 keys)
    0x05, 0x07,        // Usage Page (Key Codes)
    0x19, 0x00,        // Usage Minimum (0)
    0x29, 0x65,        // Usage Maximum (101)
    0x81, 0x00,        // Input (Data,Array,Abs)
    0xc0,              // End Collection
};
```

---

## 🔧 STEP 4: Thay đổi TotalKeys (101 → 104)

### 4.1. Tìm HID Report Count

Trong HID descriptor, tìm dòng:

```cpp
0x29, 0x65,        // Usage Maximum (0x65 = 101 keys)
```

### 4.2. Đổi thành 104 keys

```cpp
0x29, 0x68,        // Usage Maximum (0x68 = 104 keys)
```

### 4.3. Verify TotalKeys

**US Standard Layout:**

-   104 keys = Standard US full-size keyboard
-   101 keys = Japanese/International layout

---

## 📝 STEP 5: Implementation Guide

### 5.1. Backup Files

```bash
# Backup boards.txt
cp boards.txt boards.txt.backup

# Backup USBCore.cpp
cp cores/arduino/USBCore.cpp cores/arduino/USBCore.cpp.backup

# Backup HID.cpp
cp cores/arduino/HID.cpp cores/arduino/HID.cpp.backup
```

### 5.2. Thực hiện Changes

**1. Edit boards.txt:**

-   Tìm `pro.vid.0=` và `pro.pid.0=`
-   Đổi sang VID/PID mong muốn (ví dụ: Microsoft 0x045E)

**2. Edit USBCore.cpp:**

-   Tìm `STRING_MANUFACTURER`
-   Tìm `STRING_PRODUCT`
-   Tìm `STRING_SERIAL_PLACEHOLDER`
-   Đổi thành strings mong muốn

**3. Edit HID.cpp (nếu cần):**

-   Verify HID descriptor là standard US keyboard
-   Đổi `Usage Maximum` từ `0x65` (101) → `0x68` (104)

### 5.3. Compile và Upload

**⚠️ CRITICAL:** Sau khi đổi VID/PID, lần upload đầu tiên vẫn dùng USB bình thường. Nhưng sau khi upload, Arduino sẽ có VID/PID mới, và lần upload tiếp theo có thể cần ISP programmer.

**Steps:**

1. Close Arduino IDE
2. Make all changes
3. Restart Arduino IDE
4. Select board: **Tools → Board → Arduino Leonardo** (hoặc Pro Micro)
5. **Upload sketch lần cuối qua USB** (vẫn dùng bootloader cũ)
6. After upload, Arduino sẽ có VID/PID mới
7. **Next uploads:** Có thể cần ISP programmer

---

## 🎯 Recommended Settings (Example)

### Minimal Stealth (Safe - Không đổi bootloader):

```ini
# boards.txt
pro.vid.0=0x03EB        # Atmel VID (generic, safe)
pro.pid.0=0x2041        # Generic HID Device
pro.bootloader.vid=0x2341    # Giữ bootloader cũ (để upload được)
pro.bootloader.pid=0x0036    # Giữ bootloader cũ
```

```cpp
// USBCore.cpp
#define STRING_PRODUCT        "USB Keyboard"
#define STRING_MANUFACTURER   "Standard HID Keyboard"
#define STRING_SERIAL_PLACEHOLDER "00000000000000000000"
```

**KbType:** Dùng standard HID descriptor (Windows sẽ detect US keyboard)

**TotalKeys:** Đổi HID descriptor `0x29, 0x65` → `0x29, 0x68` (101 → 104)

### Full Stealth (Advanced - Đổi cả bootloader):

```ini
# boards.txt
pro.vid.0=0x045E        # Microsoft VID
pro.pid.0=0x0745        # Microsoft Keyboard
pro.bootloader.vid=0x045E   # Đổi bootloader cũng
pro.bootloader.pid=0x0036   # Giữ PID hoặc đổi
```

```cpp
// USBCore.cpp
#define STRING_PRODUCT        "Microsoft USB Keyboard"
#define STRING_MANUFACTURER   "Microsoft Corp."
#define STRING_SERIAL_PLACEHOLDER "00000000000000000000"
```

**⚠️ Warning:** Sau khi đổi bootloader VID/PID, không thể upload qua USB nữa → Cần ISP programmer.

---

## 🔍 Verification sau khi đổi

### 1. Device Manager

**Windows:**

1. Mở **Device Manager**
2. Tìm **Keyboards**
3. Check device name → Sẽ hiển thị strings mới
4. Right-click → **Properties → Details → Hardware Ids**
5. Check VID/PID → Sẽ là VID/PID mới

### 2. RawInputViewer

1. Mở RawInputViewer
2. Check device properties:
    - **KbType:** Nên là `0x04` (US Keyboard) thay vì `0x07` (Japanese)
    - **TotalKeys:** Nên là `104` thay vì `101`
    - **Manufacturer:** Sẽ là string mới
    - **Product:** Sẽ là string mới

### 3. USB Descriptor Tool

Dùng **USBDeview** hoặc **USB Device Viewer** để check:

-   VID/PID
-   Manufacturer String
-   Product String
-   Serial Number

---

## ⚠️ Troubleshooting

### Problem: Arduino IDE không nhận board sau khi đổi VID/PID

**Solution:**

1. Dùng ISP programmer để upload code mới
2. Hoặc revert bootloader VID/PID (giữ `pro.bootloader.vid=0x2341`)
3. Chỉ đổi application VID/PID (`pro.vid.0`)

### Problem: Windows không nhận device

**Solution:**

1. Check VID/PID có hợp lệ không
2. Check USB strings có special characters không
3. Uninstall driver cũ → Reconnect Arduino

### Problem: KbType vẫn là 0x07

**Solution:**

1. KbType được Windows determine từ HID usage
2. Đảm bảo HID descriptor dùng standard US keyboard usage
3. Có thể cần custom HID library thay vì `Keyboard.h`

### Problem: TotalKeys vẫn là 101

**Solution:**

1. Check HID descriptor `Usage Maximum` byte
2. Đổi `0x29, 0x65` → `0x29, 0x68` (101 → 104)
3. Recompile và reupload

---

## 📚 References

### Common VID/PID:

| Vendor    | VID    | PID (Example) | Notes                 |
| --------- | ------ | ------------- | --------------------- |
| Arduino   | 0x2341 | 0x0036        | Original (detectable) |
| Atmel     | 0x03EB | 0x2041        | Generic (safe)        |
| Microsoft | 0x045E | 0x0745        | Common keyboard       |
| Logitech  | 0x046D | 0xC31C        | Common keyboard       |
| Dell      | 0x413C | 0x2107        | Common keyboard       |

### Keyboard Types (KbType):

| Type     | Value | Description          |
| -------- | ----- | -------------------- |
| US       | 0x04  | US Standard Keyboard |
| Japanese | 0x07  | Japanese Keyboard    |
| Generic  | 0x51  | Generic HID Keyboard |

### TotalKeys:

| Layout        | Keys | Usage Maximum |
| ------------- | ---- | ------------- |
| US Standard   | 104  | 0x68          |
| Japanese      | 101  | 0x65          |
| International | 102  | 0x66          |

---

## ✅ Checklist

Trước khi implement:

-   [ ] Backup tất cả files cần sửa
-   [ ] Backup bootloader (nếu có thể)
-   [ ] Backup Arduino sketch hiện tại
-   [ ] Hiểu rõ risks (không thể upload qua USB sau khi đổi bootloader VID/PID)
-   [ ] Có ISP programmer (nếu cần)

Sau khi implement:

-   [ ] Verify VID/PID trong Device Manager
-   [ ] Verify strings trong Device Manager
-   [ ] Verify KbType trong RawInputViewer
-   [ ] Verify TotalKeys trong RawInputViewer
-   [ ] Test Arduino vẫn hoạt động bình thường
-   [ ] Test upload code mới (nếu không đổi bootloader VID/PID)

---

## 💡 Tips

1. **Bắt đầu với Minimal Stealth:**

    - Chỉ đổi strings và HID descriptor
    - Không đổi bootloader VID/PID
    - Vẫn upload được qua USB

2. **Nếu cần Full Stealth:**

    - Đổi tất cả, kể cả bootloader
    - Backup bootloader trước
    - Có ISP programmer sẵn

3. **Testing:**

    - Test trên nhiều máy Windows
    - Test với RawInputViewer
    - Test với Device Manager

4. **Legal:**
    - Khuyến khích dùng generic VID (Atmel 0x03EB)
    - Tránh dùng VID của hãng lớn nếu không có permission

---

**Lưu ý:** Guide này chỉ để tham khảo. Việc modify Arduino core có thể gây issues. Hãy backup và test kỹ trước khi deploy!
