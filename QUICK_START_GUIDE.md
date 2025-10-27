# ⚡ QUICK START GUIDE - MASTER-SLAVE AHK

## 🎯 3 BƯỚC SETUP NHANH

### **BƯỚC 1: MASTER trên HOST** 🔧

**1.1. Tìm tên VM:**

```
Chạy Master script → Ấn Ctrl+Alt+L → Copy tên VMs
```

**1.2. Sửa Master script:**

```ahk
vmList.Push("Windows 10 x64 - VMware Workstation")  ; VM 1
vmList.Push("Windows 10 Pro - VMware Workstation")  ; VM 2
```

**1.3. Chạy:**

```
Double-click Master_Multi_VM_EASY_CUSTOM.ahk
```

---

### **BƯỚC 2: SLAVE trong MỖI VM** 🔧

**2.1. Copy Slave script vào VM**

**2.2. Sửa DESYNC RANGE (MỖI VM KHÁC NHAU!):**

```ahk
global MinDesync := 0      ; VM1: 0, VM2: 100, VM3: 200, ...
global MaxDesync := 300    ; VM1: 300, VM2: 400, VM3: 500, ...
```

**📋 DESYNC TABLE (Copy & Paste):**

```
VM1:  MinDesync = 0     MaxDesync = 300
VM2:  MinDesync = 100   MaxDesync = 400
VM3:  MinDesync = 200   MaxDesync = 500
VM4:  MinDesync = 50    MaxDesync = 350
VM5:  MinDesync = 150   MaxDesync = 450
```

**2.3. Chạy Slave script trong VM**

---

### **BƯỚC 3: TEST!** 🧪

```
1. HOST: Mở Notepad → Ấn Q → Hiển thị "Q" ✅
2. VM1: Mở game → HOST ấn Q → VM1 nhận Q (với delay) ✅
3. VM2: Mở game → HOST ấn Q → VM2 nhận Q (với delay) ✅
```

---

## ⌨️ HOTKEYS QUAN TRỌNG

| Script     | Hotkey       | Function            |
| ---------- | ------------ | ------------------- |
| **Master** | `Ctrl+Alt+S` | Status Check        |
| **Master** | `Ctrl+Alt+L` | List VMs            |
| **Master** | `Ctrl+Alt+T` | Toggle Broadcasting |
| **Master** | `Ctrl+Alt+Q` | Exit                |
| **Slave**  | `Ctrl+Alt+T` | Toggle ON/OFF       |
| **Slave**  | `Ctrl+Alt+D` | Debug Mode          |

---

## ⚠️ LƯU Ý QUAN TRỌNG

### **1. DESYNC RANGE**

❌ **SAI**: Tất cả VMs cùng range (0-500ms)
✅ **ĐÚNG**: Mỗi VM range khác nhau

### **2. VM WINDOW TITLE**

✅ Phải CHÍNH XÁC giống trong VMware
✅ Copy từ `Ctrl+Alt+L` để chắc chắn

### **3. HOST INPUT**

✅ Host nhận input tự nhiên (prefix `~`)
✅ Không bị block như Multiplicity 4

---

## 🔍 TROUBLESHOOTING

| Problem               | Solution                                            |
| --------------------- | --------------------------------------------------- |
| Host không xuất Q     | Kiểm tra Master đang chạy, test với Notepad         |
| VMs không nhận input  | `Ctrl+Alt+S` check status, verify Slave đang chạy   |
| VMs phản hồi cùng lúc | Kiểm tra DESYNC RANGE khác nhau                     |
| "Failed: X"           | Refresh cache (`Ctrl+Alt+R`), check VM window title |

---

## 📚 CHI TIẾT

Xem `MASTER_SLAVE_SETUP_GUIDE.md` để biết chi tiết!

---

**🎉 SETUP XONG! HOST ẤN PHÍM → TẤT CẢ VMs NHẬN! 🎉**
