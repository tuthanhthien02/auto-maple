# 📍 Vị trí file boards.txt - Thay đổi VID/PID

## ✅ File đã tìm thấy:

**Full Path:**

```
C:\Users\Thanh Thien\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6\boards.txt
```

**Short Path (từ AppData):**

```
%USERPROFILE%\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6\boards.txt
```

---

## ⚠️ QUAN TRỌNG - ĐỌC TRƯỚC KHI SỬA

### **Critical Warning:**

1. **Sau khi đổi VID/PID trong boards.txt:**

    - Lần upload đầu tiên vẫn dùng USB bình thường (bootloader cũ)
    - Sau khi upload, Arduino sẽ có VID/PID mới
    - **Lần upload tiếp theo:** Arduino IDE có thể không nhận board qua USB
    - **Cần ISP programmer** để upload code mới nếu không có bootloader với VID/PID mới

2. **Bootloader VID/PID:**

    - Nếu đổi `pro.bootloader.vid` → Bootloader sẽ có VID mới
    - **Hậu quả:** Không thể upload qua USB nữa → **Cần ISP programmer**
    - **Khuyến nghị:** Giữ bootloader VID/PID cũ nếu muốn vẫn upload được qua USB

3. **Irreversible:**
    - Một khi upload với VID/PID mới, không thể revert về cũ qua USB
    - Cần ISP programmer hoặc bootloader mới để upload lại

---

## 🔧 Cách mở và sửa file:

### Option 1: Mở trực tiếp từ File Explorer

1. Nhấn `Windows + R`
2. Paste: `%USERPROFILE%\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6`
3. Enter → Folder sẽ mở
4. Tìm file `boards.txt`
5. Right-click → **Open with** → Notepad++ hoặc VS Code

### Option 2: Copy path vào Editor

1. Copy path:
    ```
    C:\Users\Thanh Thien\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6\boards.txt
    ```
2. Mở VS Code hoặc Notepad++
3. File → Open → Paste path → Open

---

## 📝 Tìm Pro Micro / Leonardo Section

### Vấn đề:

**Pro Micro không có section riêng trong boards.txt** → Pro Micro dùng **Leonardo bootloader** (Caterina)

**Giải pháp:**

1. **Option A: Sửa USBCore.cpp (Đã có sẵn)** ✅ **RECOMMENDED**

    - File đã có override section ở dòng 24-30
    - Đơn giản hơn, không ảnh hưởng đến bootloader
    - Location: `USBCore.cpp` line 26, 30

2. **Option B: Sửa boards.txt cho Leonardo**

    - Tìm section `leonardo.vid.0` và `leonardo.pid.0`
    - Ảnh hưởng đến tất cả board dùng Leonardo bootloader

3. **Option C: Tạo section riêng cho Pro Micro**
    - Phức tạp hơn, cần hiểu Arduino board definition syntax

---

## ✏️ Option A: Sửa trong USBCore.cpp (Recommended)

**File Location:**

```
C:\Users\Thanh Thien\AppData\Local\Arduino15\packages\arduino\hardware\avr\1.8.6\cores\arduino\USBCore.cpp
```

**Current Code (Line 24-30):**

```cpp
// --- BEGIN: Override USB identity to mimic Logitech ---
#ifndef USB_VID
  #define USB_VID 0x046D    // Line 26: Logitech VID
#endif

#ifndef USB_PID
  #define USB_PID 0xC31C    // Line 30: Logitech PID
#endif
```

**Thay đổi:**

**Option A1 - Generic (Safe):**

```cpp
#ifndef USB_VID
  #define USB_VID 0x03EB    // Atmel VID (generic, safe)
#endif

#ifndef USB_PID
  #define USB_PID 0x2041    // Generic HID Device
#endif
```

**Option A2 - Microsoft (Common):**

```cpp
#ifndef USB_VID
  #define USB_VID 0x045E    // Microsoft VID
#endif

#ifndef USB_PID
  #define USB_PID 0x0745    // Microsoft Keyboard (generic)
#endif
```

**Option A3 - Logitech (Current):**

```cpp
#ifndef USB_VID
  #define USB_VID 0x046D    // Logitech VID (already set)
#endif

#ifndef USB_PID
  #define USB_PID 0xC31C    // Logitech PID (already set)
#endif
```

**Ưu điểm:**

-   ✅ Đơn giản, chỉ sửa 2 dòng
-   ✅ Không ảnh hưởng đến bootloader
-   ✅ Vẫn upload được qua USB sau khi upload lần đầu

---

## ✏️ Option B: Sửa trong boards.txt cho Leonardo

**Tìm section Leonardo trong boards.txt:**

Tìm dòng:

```ini
leonardo.vid.0=0x2341
leonardo.pid.0=0x0036
```

**Thay đổi:**

**Option B1 - Minimal (Giữ bootloader cũ):**

```ini
leonardo.vid.0=0x03EB        # Atmel VID (generic, safe)
leonardo.pid.0=0x2041        # Generic HID Device
# Giữ bootloader VID/PID cũ (nếu có)
# leonardo.bootloader.vid=0x2341    # KEEP OLD
# leonardo.bootloader.pid=0x0036    # KEEP OLD
```

**Option B2 - Full (Đổi cả bootloader):**

```ini
leonardo.vid.0=0x045E        # Microsoft VID
leonardo.pid.0=0x0745        # Microsoft Keyboard
leonardo.bootloader.vid=0x045E   # Đổi bootloader VID (cần ISP programmer)
leonardo.bootloader.pid=0x0036   # Bootloader PID
```

**⚠️ Warning Option B2:**

-   Sau khi đổi bootloader VID/PID, không thể upload qua USB nữa
-   Cần ISP programmer để upload code mới

---

## 📋 Quick Reference - VID/PID Options

| Vendor              | VID    | PID    | Notes                       |
| ------------------- | ------ | ------ | --------------------------- |
| **Atmel (Generic)** | 0x03EB | 0x2041 | ✅ Safe, generic HID device |
| **Microsoft**       | 0x045E | 0x0745 | Common keyboard             |
| **Logitech**        | 0x046D | 0xC31C | Common keyboard (current)   |
| **Dell**            | 0x413C | 0x2107 | Common keyboard             |
| **Arduino**         | 0x2341 | 0x0036 | Original (detectable)       |

---

## 🎯 Recommended Approach

### Minimal Stealth (Safe):

1. **Sửa USBCore.cpp** (Line 26, 30):

    ```cpp
    #define USB_VID 0x03EB    // Atmel (generic)
    #define USB_PID 0x2041    // Generic HID
    ```

2. **Không sửa boards.txt**

    - Bootloader giữ nguyên → Vẫn upload được qua USB

3. **Kết quả:**
    - ✅ Application có VID/PID mới
    - ✅ Bootloader vẫn có VID/PID cũ
    - ✅ Vẫn upload được qua USB

### Full Stealth (Advanced):

1. **Sửa USBCore.cpp** (Line 26, 30)
2. **Sửa boards.txt** (Leonardo section)
3. **Cảnh báo:** Cần ISP programmer sau này

---

## ⚠️ Lưu ý quan trọng

### 1. Backup trước khi sửa:

```bash
# Backup boards.txt
copy boards.txt boards.txt.backup

# Backup USBCore.cpp (nếu sửa)
copy cores\arduino\USBCore.cpp cores\arduino\USBCore.cpp.backup
```

### 2. Sau khi sửa:

1. **Close Arduino IDE** (nếu đang mở)
2. **Restart Arduino IDE**
3. **Upload sketch lần cuối qua USB** (vẫn dùng bootloader cũ)
4. **After upload:** Arduino sẽ có VID/PID mới
5. **Next uploads:**
    - Nếu giữ bootloader cũ → Vẫn upload được
    - Nếu đổi bootloader → Cần ISP programmer

### 3. Verify:

1. **Device Manager:**

    - Right-click Arduino → Properties → Details → Hardware Ids
    - Check VID/PID → Sẽ là VID/PID mới

2. **RawInputViewer:**
    - Check VID/PID trong device properties

---

## 🔍 Tìm Leonardo Section trong boards.txt

### Method 1: Search trong Editor

1. Mở `boards.txt` trong VS Code hoặc Notepad++
2. Press `Ctrl+F`
3. Search: `leonardo.vid`
4. Tìm dòng `leonardo.vid.0=` và `leonardo.pid.0=`

### Method 2: Command Line

```powershell
Select-String -Path "boards.txt" -Pattern "leonardo\.(vid|pid)"
```

---

## 📝 Step-by-Step Guide

### Step 1: Backup

1. Backup `boards.txt` → `boards.txt.backup`
2. Backup `USBCore.cpp` → `USBCore.cpp.backup` (nếu sửa)

### Step 2: Chọn phương pháp

**Khuyến nghị:** **Option A (Sửa USBCore.cpp)** - Đơn giản và an toàn hơn

### Step 3: Sửa USBCore.cpp

1. Mở `USBCore.cpp`
2. Tìm dòng 26 (`USB_VID`) và 30 (`USB_PID`)
3. Đổi thành VID/PID mong muốn
4. Save

### Step 4: (Optional) Sửa boards.txt

Chỉ làm nếu cần Full Stealth:

1. Mở `boards.txt`
2. Tìm section Leonardo
3. Tìm `leonardo.vid.0=` và `leonardo.pid.0=`
4. Đổi thành VID/PID mong muốn
5. **Nếu đổi bootloader VID/PID:** Cảnh báo về ISP programmer
6. Save

### Step 5: Restart & Upload

1. Close Arduino IDE
2. Restart Arduino IDE
3. Upload sketch
4. Verify VID/PID trong Device Manager

---

## 💡 Tips

1. **Bắt đầu với USBCore.cpp:**

    - Đơn giản hơn
    - An toàn hơn (không ảnh hưởng bootloader)
    - Vẫn đạt được mục tiêu stealth

2. **Nếu cần Full Stealth:**

    - Đổi cả boards.txt
    - Backup bootloader trước
    - Có ISP programmer sẵn

3. **Testing:**
    - Test trên nhiều máy Windows
    - Verify trong Device Manager
    - Verify trong RawInputViewer

---

**Next Step:** Chọn phương pháp và sửa file tương ứng!
