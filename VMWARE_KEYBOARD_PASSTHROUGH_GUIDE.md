# VMware Keyboard Pass-Through Guide

## 🔍 Có thể pass-through keyboard host vào VMware không?

**✅ CÓ** - Nhưng có **LIMITATIONS** quan trọng!

---

## 📋 Các Phương Pháp

### **Method 1: USB Pass-Through (Physical Keyboard)**

**Cách làm:**

1. **VMware Settings:**

    - VM → Settings → USB Controller
    - Chọn USB 2.0 hoặc USB 3.0 (tùy keyboard)

2. **Connect Keyboard:**

    - VM đang chạy → VM → Removable Devices → [Keyboard Name] → Connect (Disconnect from Host)

3. **Kết quả:**
    - Keyboard sẽ disconnect từ Host
    - Chỉ hoạt động trong VM
    - **Host mất keyboard!**

**⚠️ LIMITATIONS:**

-   ❌ Host không thể dùng keyboard khi VM đang dùng
-   ❌ Phải disconnect keyboard từ VM để dùng lại trên Host
-   ❌ Không phù hợp nếu cần dùng keyboard trên cả Host và VM

---

### **Method 2: Virtual USB Keyboard (Không khả thi)**

-   ❌ VMware không hỗ trợ virtual USB keyboard
-   ❌ Keyboard phải là hardware thật

---

### **Method 3: Arduino HID Keyboard (RECOMMENDED)** ⭐⭐⭐⭐⭐

**Setup hiện tại trong codebase:**

```
Host → TCP → VMware Receiver → Serial → Arduino HID → Game
```

**Benefits:**

-   ✅ **Host vẫn dùng keyboard bình thường**
-   ✅ **VM có Arduino HID riêng** (hardware thật, có VID/PID)
-   ✅ **Không bị NGS detect** (vì có VID/PID thật)
-   ✅ **Không phải disconnect/reconnect**

**Setup:**

1. **Arduino USB pass-through vào VM:**

    - VM → Settings → USB Controller
    - VM → Removable Devices → [Arduino] → Connect (Disconnect from Host)

2. **Chạy scripts:**

    - Host: `run_host_sender.bat`
    - VM: `run_vmware_receiver.bat`

3. **Kết quả:**
    - Host keyboard → Host script → TCP → VM script → Arduino → Game
    - ✅ Host vẫn dùng keyboard được
    - ✅ VM có Arduino HID riêng

---

## 🎯 So Sánh Các Phương Pháp

| Method               | Host Keyboard | VM Keyboard | NGS Detection | Difficulty |
| -------------------- | ------------- | ----------- | ------------- | ---------- |
| **USB Pass-Through** | ❌ Lost       | ✅ Works    | ⚠️ Medium     | ✅ Easy    |
| **Arduino HID**      | ✅ Works      | ✅ Works    | ✅ **LOW**    | ⚠️ Medium  |

---

## 🔧 Cách Pass-Through USB Keyboard (Nếu muốn thử)

### **Bước 1: Enable USB Controller trong VM**

1. VM đang **TẮT**
2. VM → Settings → Add → USB Controller
3. Chọn USB 2.0 hoặc USB 3.0
4. OK

### **Bước 2: Connect Keyboard**

1. **VM đang CHẠY**
2. VM → Removable Devices → [Your Keyboard] → **Connect (Disconnect from Host)**
3. Keyboard sẽ disconnect từ Host và connect vào VM

### **Bước 3: Disconnect (Khi cần dùng lại trên Host)**

1. VM → Removable Devices → [Your Keyboard] → **Disconnect (Connect to Host)**
2. Keyboard sẽ về lại Host

---

## ⚠️ Các Vấn Đề Có Thể Gặp

### **1. Keyboard không xuất hiện trong Removable Devices**

**Nguyên nhân:**

-   Keyboard là PS/2 (không phải USB)
-   USB Controller chưa được enable
-   VM chưa được cài đặt VMware Tools

**Fix:**

-   Chỉ USB keyboard mới pass-through được
-   Enable USB Controller trong VM Settings
-   Cài VMware Tools

### **2. Keyboard bị disconnect khi VM không focus**

**Nguyên nhân:**

-   VMware tự động disconnect USB khi VM không focus (tùy cấu hình)

**Fix:**

-   VM → Settings → USB Controller
-   Bỏ tick "Connect USB devices automatically when VM is powered on"
-   Tick "Connect USB devices automatically when VM is powered on" (nếu muốn auto-connect)

### **3. NGS Detection Risk**

**Vấn đề:**

-   Physical keyboard pass-through vào VM vẫn có thể bị detect nếu:
    -   Keyboard có VID/PID nhưng VMware traces vẫn có
    -   Kết hợp với VMware mouse = VM fingerprint

**Solution:**

-   ✅ **Dùng Arduino HID** (hardware riêng, không có VMware traces)

---

## 🎯 Recommendation

### **Use Arduino HID Keyboard** ⭐⭐⭐⭐⭐

**Tại sao:**

1. ✅ **Host vẫn dùng keyboard** - Không mất keyboard trên Host
2. ✅ **VM có Arduino riêng** - Hardware thật, có VID/PID
3. ✅ **Không bị NGS detect** - Không có VMware traces
4. ✅ **Đã có sẵn code** - Setup đơn giản với scripts có sẵn

**Setup:**

```
1. Arduino USB pass-through vào VM
2. Host: run_host_sender.bat
3. VM: run_vmware_receiver.bat
4. Done!
```

---

## 📝 Summary

**Có thể pass-through keyboard host vào VMware không?**

-   ✅ **CÓ** - Nhưng Host sẽ mất keyboard
-   ⚠️ **KHÔNG RECOMMENDED** - Vì Host không thể dùng keyboard

**Solution tốt nhất:**

-   ✅ **Arduino HID Keyboard** - Host vẫn dùng keyboard, VM có Arduino riêng
-   ✅ **Đã có sẵn code** - Setup đơn giản
-   ✅ **An toàn nhất** - Không bị NGS detect

---

## 🔗 Related Files

-   `host_sender.py` - Host script gửi input qua TCP
-   `vmware_receiver.py` - VM script nhận input và forward đến Arduino
-   `arduino_hid_keyboard.ino` - Arduino HID keyboard code
-   `TCP_SETUP.md` - Chi tiết setup TCP connection

---

---

## 💻 Laptop Users - Special Instructions

### **⚠️ Laptop Keyboard KHÔNG THỂ Pass-Through**

**Tại sao:**

-   ❌ Laptop keyboard là **built-in keyboard** (gắn liền với mainboard)
-   ❌ Không phải USB device → Không xuất hiện trong VMware Removable Devices
-   ❌ VMware chỉ pass-through được **USB devices** (không phải built-in devices)

**Solution:**

✅ **BẮT BUỘC dùng Arduino HID Keyboard** - Đây là giải pháp DUY NHẤT cho laptop!

---

### **Setup cho Laptop:**

#### **Option 1: Dùng Arduino HID (RECOMMENDED)** ⭐⭐⭐⭐⭐

**Setup:**

1. **Mua Arduino Leonardo/Micro/Pro Micro** (có HID support)
2. **Upload code:**
    - Upload `arduino_hid_keyboard.ino` lên Arduino
3. **Connect Arduino vào laptop:**
    - Cắm Arduino vào USB port của laptop
4. **Pass-through Arduino vào VM:**
    - VM → Removable Devices → [Arduino] → Connect (Disconnect from Host)
5. **Chạy scripts:**
    - Laptop (Host): `run_host_sender.bat`
    - VM: `run_vmware_receiver.bat`

**Kết quả:**

```
Laptop Keyboard → host_sender.py → TCP → vmware_receiver.py → Arduino HID → Game
```

**Benefits:**

-   ✅ **Laptop keyboard vẫn hoạt động bình thường** trên Host
-   ✅ **VM có Arduino HID riêng** (hardware thật, có VID/PID)
-   ✅ **Không bị NGS detect** (vì có VID/PID thật, không có VMware traces)
-   ✅ **Không cần external USB keyboard**

---

#### **Option 2: Dùng External USB Keyboard + Pass-Through** ⚠️ NOT RECOMMENDED

**Nếu bạn có external USB keyboard:**

1. Connect external USB keyboard vào laptop
2. Pass-through external keyboard vào VM
3. **⚠️ Laptop keyboard vẫn hoạt động trên Host** (vì là built-in)
4. **⚠️ External keyboard sẽ disconnect từ Host và chỉ hoạt động trong VM**

**Hạn chế:**

-   ❌ Cần external USB keyboard (tốn tiền)
-   ❌ External keyboard sẽ disconnect từ Host khi pass-through vào VM
-   ⚠️ Vẫn có NGS detection risk (VMware traces)

**Không khuyến nghị** - Tốt hơn là dùng Arduino HID!

---

### **Laptop Setup Summary:**

| Method                          | Laptop Keyboard | VM Keyboard               | NGS Risk   | Cost    |
| ------------------------------- | --------------- | ------------------------- | ---------- | ------- |
| **Arduino HID**                 | ✅ Works        | ✅ Works                  | ✅ **LOW** | ~$5-10  |
| **External USB + Pass-Through** | ✅ Works        | ⚠️ Works (lost from Host) | ⚠️ Medium  | ~$20-50 |

---

### **Recommendation cho Laptop:**

**✅ Dùng Arduino HID Keyboard** - Giải pháp tốt nhất!

**Lý do:**

1. ✅ **Không cần external keyboard** - Laptop keyboard vẫn hoạt động
2. ✅ **Rẻ hơn** - Arduino chỉ ~$5-10 vs USB keyboard ~$20-50
3. ✅ **An toàn hơn** - Không bị NGS detect
4. ✅ **Đã có sẵn code** - Setup đơn giản

---

## 💡 Tips

1. **Nếu chỉ test:** Có thể pass-through keyboard vào VM
2. **Nếu production:** Dùng Arduino HID (setup hiện tại)
3. **Nếu Host không cần keyboard:** Có thể pass-through keyboard vào VM
4. **Nếu Host vẫn cần keyboard:** **BẮT BUỘC dùng Arduino HID**
5. **Nếu dùng laptop:** **BẮT BUỘC dùng Arduino HID** (laptop keyboard không thể pass-through)
