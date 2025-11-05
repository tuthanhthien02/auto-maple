# VMware VID/PID Detection - NGS Risk Analysis

## 🔍 Phân Tích Hình Ảnh

### **Hardware Khoanh Đỏ (Keyboard):**

```
Handle: 0x0000000000010043
Interface: \\?\ACPI#PNP0303#4&1bd7f811&0#{884b96c3-56ef-11d1-bc8c-00a0c91405dd}
HID Type: 1 (RIM_TYPEKEYBOARD)
KbType: 0x07 (Japanese Keyboard)
```

**❌ KHÔNG CÓ VID/PID** - Vì đây là **ACPI device**, không phải USB device.

---

## ❓ Tại Sao Không Có VID/PID?

### **1. ACPI Device vs USB Device**

**ACPI Device (`ACPI#PNP0303`):**

-   ✅ Standard PS/2 keyboard (emulated by VMware)
-   ✅ Integrated vào firmware/BIOS của VM
-   ✅ **KHÔNG có VID/PID** (vì không phải USB device)
-   ✅ Common trong VM environments

**USB Device:**

-   ✅ Có VID/PID (Vendor ID / Product ID)
-   ✅ Example: `VID_0E0F&PID_0003` (VMware mouse)
-   ✅ Physical hardware thường có VID/PID

### **2. VMware Keyboard Emulation**

VMware emulates keyboard như **PS/2 keyboard** (legacy standard):

-   ✅ Không qua USB protocol
-   ✅ Không có VID/PID
-   ✅ Appears as ACPI device
-   ✅ **NGS có thể detect pattern này!**

---

## ⚠️ NGS Detection Risk

### **Tại Sao NGS Có Thể Detect:**

1. **ACPI Keyboard Pattern:**

    - ✅ Physical host thường dùng USB keyboard (có VID/PID)
    - ✅ VM thường dùng ACPI/PS/2 keyboard (không có VID/PID)
    - ✅ **Pattern này là signature của VM!**

2. **VMware Traces:**

    - ✅ Mouse devices có `VID_0E0F (VMware)` và `PID_0003 (VMware)`
    - ✅ `ACPI#VMW0003` string (VMware-specific)
    - ✅ **Kết hợp với ACPI keyboard = VM fingerprint!**

3. **NGS Detection Logic:**
    ```
    IF (keyboard has no VID/PID AND mouse has VMware VID/PID):
        → HIGH RISK: Virtual Machine detected
    ```

---

## ✅ Solutions

### **Solution 1: Dùng Arduino HID Keyboard** ⭐ RECOMMENDED

**Vấn đề:**

-   VM keyboard (ACPI) không có VID/PID → NGS detect

**Solution:**

-   Dùng **Arduino HID Keyboard** (hardware USB device)
-   Arduino có **VID/PID thật** (không phải VMware)
-   Input từ hardware thật → NGS không detect

**Setup:**

```
Game (in VM) → Arduino HID Keyboard (hardware USB) → Input
```

**Benefits:**

-   ✅ Hardware keyboard thật (có VID/PID)
-   ✅ NGS không detect VM traces
-   ✅ An toàn hơn nhiều

---

### **Solution 2: Pass-Through USB Keyboard**

**Vấn đề:**

-   VM keyboard là emulated (không có VID/PID)

**Solution:**

-   Pass-through physical USB keyboard vào VM
-   Physical keyboard có VID/PID thật
-   NGS sẽ không detect VM traces

**Setup:**

```
VMware Settings → USB Devices → Pass-through physical keyboard
```

**Benefits:**

-   ✅ Physical keyboard (có VID/PID)
-   ✅ NGS không detect VM traces
-   ⚠️ Cần physical keyboard thật

---

### **Solution 3: USB HID Emulation (Advanced)**

**Vấn đề:**

-   VM keyboard không có VID/PID

**Solution:**

-   Emulate USB HID keyboard trong VM
-   Tạo VID/PID giống hardware thật
-   ⚠️ **Rất phức tạp, có thể không work**

**Not Recommended:**

-   ❌ Phức tạp
-   ❌ Có thể không work
-   ❌ Vẫn có thể bị detect

---

## 🎯 Recommendation

### **Use Arduino HID Keyboard** ⭐⭐⭐⭐⭐

**Why:**

1. ✅ **Hardware thật** - Arduino có VID/PID thật
2. ✅ **Không có VM traces** - Input từ hardware, không từ VM emulation
3. ✅ **An toàn nhất** - NGS không detect VM traces
4. ✅ **Đã có sẵn** - Code đã support Arduino

**Setup:**

1. Connect Arduino vào VM (USB pass-through)
2. Upload `arduino_hid_keyboard.ino`
3. Bot dùng Arduino output (không dùng VM keyboard)

**Result:**

```
Game → Arduino HID (hardware USB, có VID/PID) → Input
✅ NGS không detect VM traces
```

---

## 📊 Comparison

| Method                    | Has VID/PID? | NGS Detection Risk | Difficulty |
| ------------------------- | ------------ | ------------------ | ---------- |
| **VM ACPI Keyboard**      | ❌ No        | ⚠️ **HIGH**        | ✅ Easy    |
| **Physical USB Keyboard** | ✅ Yes       | ✅ Low             | ⚠️ Medium  |
| **Arduino HID Keyboard**  | ✅ Yes       | ✅ **LOW**         | ✅ Easy    |

---

## ⚠️ Critical Notes

1. **ACPI Keyboard = VM Signature:**

    - Physical host thường dùng USB keyboard
    - VM thường dùng ACPI/PS/2 keyboard
    - NGS có thể detect pattern này

2. **VMware Traces:**

    - Mouse devices có VMware VID/PID
    - Keyboard không có VID/PID
    - **Kết hợp = VM fingerprint**

3. **Arduino HID = Best Solution:**
    - Hardware thật (có VID/PID)
    - Không có VM traces
    - An toàn nhất

---

## 🚀 Action Plan

### **Immediate:**

1. ✅ **Dùng Arduino HID Keyboard** (khuyến nghị)
2. ✅ Connect Arduino vào VM (USB pass-through)
3. ✅ Bot dùng Arduino output

### **Alternative:**

1. ⚠️ Pass-through physical USB keyboard vào VM
2. ⚠️ Không dùng VM emulated keyboard

---

## 📝 Summary

**Tại sao không có VID/PID:**

-   Keyboard là ACPI device (emulated by VMware), không phải USB device
-   ACPI devices không có VID/PID

**Có bị NGS detect không:**

-   ✅ **CÓ** - NGS có thể detect vì:
    -   ACPI keyboard pattern = VM signature
    -   Kết hợp với VMware mouse VID/PID = VM fingerprint

**Solution:**

-   ✅ **Dùng Arduino HID Keyboard** (hardware thật, có VID/PID)
-   ✅ An toàn nhất, không có VM traces
