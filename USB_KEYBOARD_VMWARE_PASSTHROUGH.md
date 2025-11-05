# USB Keyboard Pass-Through vào VMware - Step by Step Guide

## 📋 Tổng Quan

Nếu bạn có **USB keyboard rời**, bạn có thể pass-through nó vào VMware. Khi pass-through:

-   ✅ Keyboard sẽ hoạt động trong VM
-   ⚠️ Keyboard sẽ **disconnect từ Host** (Host mất keyboard)
-   ✅ **Laptop keyboard vẫn hoạt động** trên Host (nếu dùng laptop)

---

## 🔧 Setup Step-by-Step

### **Bước 1: Enable USB Controller trong VM**

1. **VM đang TẮT** (nếu đang chạy thì Shutdown)
2. Mở VMware Workstation
3. Chọn VM của bạn
4. Click **Settings** (hoặc chuột phải → Settings)
5. Trong tab **Hardware**, click **Add...**
6. Chọn **USB Controller**
7. Chọn **USB 2.0** hoặc **USB 3.0** (tùy keyboard của bạn)
    - Nếu không chắc, chọn USB 2.0 (tương thích tốt hơn)
8. Click **Finish**
9. Click **OK** để đóng Settings

---

### **Bước 2: Connect Keyboard vào VM**

1. **Connect USB keyboard vào laptop/PC** (nếu chưa cắm)
2. **Start VM** (Power On)
3. **Đợi VM boot xong** (đến desktop)
4. Trong VMware menu bar, click **VM** → **Removable Devices**
5. Tìm keyboard của bạn trong danh sách (ví dụ: "USB Keyboard", "Logitech Keyboard", ...)
6. Click vào keyboard → **Connect (Disconnect from Host)**
7. VM sẽ hiển thị notification: "USB device connected"

**✅ Xong!** Keyboard giờ chỉ hoạt động trong VM.

---

### **Bước 3: Test Keyboard trong VM**

1. Click vào VM window để focus vào VM
2. Mở Notepad hoặc bất kỳ app nào trong VM
3. Gõ phím → Keyboard sẽ hoạt động!
4. **Lưu ý:** Keyboard sẽ KHÔNG hoạt động trên Host nữa

---

### **Bước 4: Disconnect Keyboard (Khi cần dùng lại trên Host)**

**Cách 1: Disconnect từ VM Menu**

1. VM → Removable Devices → [Your Keyboard] → **Disconnect (Connect to Host)**
2. Keyboard sẽ về lại Host

**Cách 2: Disconnect từ System Tray (VMware Tools)**

1. Click vào VMware icon trong system tray của VM
2. Click vào keyboard → Disconnect

---

## ⚠️ Important Notes

### **1. Keyboard sẽ disconnect từ Host**

-   ❌ Host sẽ **mất keyboard** khi VM đang dùng
-   ✅ **Laptop keyboard vẫn hoạt động** trên Host (nếu dùng laptop)
-   ⚠️ Phải disconnect từ VM để dùng lại trên Host

### **2. Auto-Connect Settings**

**Cấu hình để keyboard tự động connect khi VM start:**

1. VM → Settings → USB Controller
2. Tick **"Connect USB devices automatically when VM is powered on"**
3. Chọn keyboard trong list → **Always connect to this virtual machine**

**Lưu ý:** Sau khi set "Always connect", keyboard sẽ **TỰ ĐỘNG disconnect từ Host** khi VM start!

### **3. Keyboard không xuất hiện trong Removable Devices?**

**Nguyên nhân:**

-   ❌ Keyboard là PS/2 (không phải USB)
-   ❌ USB Controller chưa được enable
-   ❌ VMware Tools chưa được cài đặt

**Fix:**

1. **Kiểm tra keyboard là USB:**

    - Windows: Device Manager → Keyboards → Phải có "USB" trong tên
    - Nếu là PS/2 → Không thể pass-through

2. **Enable USB Controller:**

    - Xem lại Bước 1

3. **Cài VMware Tools:**
    - VM → Install VMware Tools
    - Hoặc VM → Settings → Options → VMware Tools → Install

---

## 🎯 Use Cases

### **Case 1: Desktop PC**

**Setup:**

-   Desktop PC có keyboard rời
-   Pass-through keyboard vào VM

**Kết quả:**

-   ❌ Host mất keyboard (phải dùng mouse để disconnect)
-   ✅ VM có keyboard

**⚠️ Vấn đề:**

-   Nếu Host không có keyboard backup → Khó disconnect keyboard từ VM!

**Solution:**

-   ✅ Dùng **Arduino HID** thay vì pass-through keyboard (Host vẫn dùng keyboard được)

---

### **Case 2: Laptop + USB Keyboard**

**Setup:**

-   Laptop có keyboard rời
-   Pass-through keyboard vào VM

**Kết quả:**

-   ✅ **Laptop keyboard vẫn hoạt động** trên Host
-   ✅ VM có USB keyboard

**✅ Tốt!** Vì Host vẫn có keyboard (laptop keyboard).

---

### **Case 3: Game Bot (NGS Detection)**

**Setup:**

-   Pass-through keyboard vào VM để chơi game

**⚠️ NGS Detection Risk:**

-   ⚠️ Keyboard có VID/PID thật → **Tốt**
-   ⚠️ Nhưng VMware traces vẫn có (mouse, system) → **Có thể bị detect**
-   ⚠️ Kết hợp với VMware mouse = VM fingerprint

**Recommendation:**

-   ✅ **Tốt hơn:** Dùng **Arduino HID Keyboard** (hardware riêng, không có VMware traces)

---

## 🔄 Comparison: USB Keyboard Pass-Through vs Arduino HID

| Feature           | USB Keyboard Pass-Through             | Arduino HID |
| ----------------- | ------------------------------------- | ----------- |
| **Host Keyboard** | ❌ Lost (Desktop) / ✅ Works (Laptop) | ✅ Works    |
| **VM Keyboard**   | ✅ Works                              | ✅ Works    |
| **NGS Detection** | ⚠️ Medium (VMware traces)             | ✅ **LOW**  |
| **Cost**          | Free (nếu đã có)                      | ~$5-10      |
| **Setup**         | ✅ Easy                               | ⚠️ Medium   |

---

## 💡 Tips

### **Tip 1: Disconnect Keyboard từ VM trước khi Shutdown**

-   Nếu bạn shutdown VM mà keyboard vẫn connect → Keyboard sẽ về Host khi VM tắt
-   Nhưng tốt hơn là disconnect thủ công để tránh conflict

### **Tip 2: Dùng Shortcut để Disconnect**

-   VMware có thể set shortcut để disconnect USB devices
-   VM → Settings → Keyboard → Shortcuts

### **Tip 3: Nếu Host mất keyboard (Desktop PC)**

**Cách disconnect keyboard từ Host:**

1. **Dùng Remote Desktop** (nếu có)
2. **Dùng PowerShell/Terminal** (nếu có SSH)
3. **Dùng VMware menu** trên Host (nếu VMware đang chạy)
4. **Restart VM** (keyboard sẽ về Host khi VM tắt)

**⚠️ Cẩn thận:** Nếu Host không có keyboard backup → Khó disconnect!

---

## 🎯 Recommendation

### **Nếu dùng Laptop:**

-   ✅ **OK** - Pass-through USB keyboard vào VM
-   ✅ Laptop keyboard vẫn hoạt động trên Host
-   ⚠️ Vẫn có NGS detection risk (nhưng ít hơn VM emulated keyboard)

### **Nếu dùng Desktop PC:**

-   ⚠️ **Cẩn thận** - Host sẽ mất keyboard
-   ✅ **Nên dùng Arduino HID** thay vì pass-through keyboard
-   ✅ Host vẫn dùng keyboard được

### **Nếu lo về NGS Detection:**

-   ✅ **BẮT BUỘC dùng Arduino HID** - An toàn nhất!

---

## 📝 Summary

**Pass-through USB keyboard vào VMware:**

1. ✅ **Enable USB Controller** trong VM Settings
2. ✅ **Connect keyboard** từ VM → Removable Devices
3. ✅ **Keyboard sẽ disconnect từ Host** và chỉ hoạt động trong VM
4. ✅ **Laptop keyboard vẫn hoạt động** trên Host (nếu dùng laptop)

**Khi nào nên dùng:**

-   ✅ Dùng laptop + USB keyboard → OK
-   ⚠️ Dùng desktop PC → Cẩn thận (Host mất keyboard)
-   ⚠️ Lo về NGS detection → Nên dùng Arduino HID

---

## 🔗 Related Files

-   `VMWARE_KEYBOARD_PASSTHROUGH_GUIDE.md` - General guide
-   `host_sender.py` - Alternative: TCP-based input (không cần pass-through)
-   `vmware_receiver.py` - Alternative: Arduino HID setup
