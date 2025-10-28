# 🚀 MASTER-SLAVE AHK SYSTEM

## 📋 TỔNG QUAN

Hệ thống **Master-Slave AHK** cho phép bạn control **N VMs** từ 1 HOST machine, giống Multiplicity 4 nhưng **FREE** và **STEALTH** hơn!

### **⭐ KEY FEATURES:**

✅ **Perfect Anti-Detection**: Desync delay khác nhau cho mỗi VM
✅ **Natural Host Input**: Host nhận input tự nhiên (không block)
✅ **Scalable**: Thêm bao nhiêu VMs cũng được
✅ **Zero Network**: Local ControlSend, không cần network
✅ **Low Latency**: < 1ms per keypress
✅ **Memory Efficient**: ~2-5 MB per script

---

## 📁 FILES STRUCTURE

```
auto-maple/
├── Master_Multi_VM_EASY_CUSTOM.ahk     ← Master script (chạy trên HOST)
├── multiplicity_jitter_DESYNC_SLAVE.ahk ← Slave script (chạy trong VMs)
├── MASTER_SLAVE_SETUP_GUIDE.md         ← Full setup guide
├── QUICK_START_GUIDE.md                ← Quick start guide
└── README_MASTER_SLAVE.md              ← This file
```

---

## 🎯 HOW IT WORKS

```
┌─────────────────────────────────────────────────────────┐
│              HOST MACHINE (Physical PC)                  │
│                                                          │
│  Keyboard → Master Script → Broadcast to VMs             │
│                                                          │
│  ⌨️ HOST INPUT:                                          │
│     Q key → [~q::] → BroadcastKeyAsync("q")              │
│            ↓                                              │
│     → Send to VMs (ControlSend)                          │
│     → Host input hoạt động tự nhiên                      │
└────────┬────────────────────────┬────────────────────────┘
         │                       │
    ┌────▼────┐            ┌────▼────┐
    │   VM1   │            │   VM2   │
    │         │            │         │
    │  Slave  │            │  Slave  │
    │  Delay: │            │  Delay: │
    │  0-300ms│            │100-400ms│
    └─────────┘            └─────────┘
```

---

## ⚡ QUICK START

### **1. Setup Master (HOST):**

```ahk
; Mở Master_Multi_VM_EASY_CUSTOM.ahk
; Sửa line 110-114:

vmList.Push("Windows 10 x64 - VMware Workstation")  ; VM 1
vmList.Push("Windows 10 Pro - VMware Workstation")  ; VM 2
vmList.Push("Windows 11 x64 - VMware Workstation") ; VM 3

; Chạy Master script
```

### **2. Setup Slave (MỖI VM):**

```ahk
; Mở multiplicity_jitter_DESYNC_SLAVE.ahk
; Sửa line 189-190 (MỖI VM KHÁC NHAU!):

VM1: global MinDesync := 0    ; VM1: 0ms
     global MaxDesync := 300   ; VM1: 300ms

VM2: global MinDesync := 100  ; VM2: 100ms
     global MaxDesync := 400   ; VM2: 400ms

VM3: global MinDesync := 200  ; VM3: 200ms
     global MaxDesync := 500   ; VM3: 500ms

; Chạy Slave script trong VM
```

### **3. Test:**

```
HOST: Mở Notepad → Ấn Q → Hiển thị "Q" ✅
VM1:  Nhận Q sau 0-300ms
VM2:  Nhận Q sau 100-400ms
VM3:  Nhận Q sau 200-500ms
```

---

## ⌨️ HOTKEYS

### **Master Script (HOST):**

| Hotkey       | Function                         |
| ------------ | -------------------------------- |
| `Ctrl+Alt+S` | Status Check (VM found/missing)  |
| `Ctrl+Alt+L` | List VMs (copy tên windows)      |
| `Ctrl+Alt+T` | Toggle Input Broadcasting ON/OFF |
| `Ctrl+Alt+D` | Toggle Debug Tooltip             |
| `Ctrl+Alt+B` | Toggle Beep Sound                |
| `Ctrl+Alt+P` | Performance Monitor              |
| `Ctrl+Alt+R` | Refresh VM Cache                 |
| `Ctrl+Alt+Q` | Exit Script                      |

### **Slave Script (VMs):**

| Hotkey       | Function             |
| ------------ | -------------------- |
| `Ctrl+Alt+T` | Toggle Script ON/OFF |
| `Ctrl+Alt+P` | Performance Monitor  |
| `Ctrl+Alt+R` | Reset Statistics     |
| `Ctrl+Alt+D` | Toggle Debug Mode    |

---

## 📊 TECHNICAL DETAILS

### **Master Script:**

-   **Input Method**: `~Key::` (prefix `~` = pass through, không block Host)
-   **Broadcast Method**: `ControlSend` (send to background VM windows)
-   **VM Detection**: Window title matching
-   **Performance**: VM Window Caching, Auto-Retry, Batch ControlSend

### **Slave Script:**

-   **Input Method**: ControlSend nhận từ Master
-   **Output Method**: `SendInput` (user32.SendInput API)
-   **Desync**: Random delay với Gaussian distribution
-   **Jitter**: Small random variation (30-80ms)
-   **Features**: Key remapping, auto-pause, performance monitoring

---

## ⚠️ IMPORTANT NOTES

### **1. DESYNC RANGE - CRITICAL!**

❌ **SAI**: Tất cả VMs cùng range

```ahk
VM1: 0-500ms
VM2: 0-500ms  ← ANTI-CHEAT PHÁT HIỆN PATTERN!
VM3: 0-500ms
```

✅ **ĐÚNG**: Mỗi VM range khác nhau

```ahk
VM1: 0-300ms    ← Range 1
VM2: 100-400ms  ← Range 2 (overlap để tự nhiên)
VM3: 200-500ms  ← Range 3
```

### **2. VM WINDOW TITLE**

Phải CHÍNH XÁC giống window title trong VMware:

-   ✅ Dùng `Ctrl+Alt+L` để copy tên đúng
-   ❌ Không guess tên window

### **3. HOST INPUT**

Prefix `~` trong hotkeys cho phép input pass through:

```ahk
~q::BroadcastKeyAsync("q")  ← Host nhận Q tự nhiên
```

---

## 🔍 TROUBLESHOOTING

### **Problem: Host không xuất Q trong Notepad**

**Solution:**

-   Kiểm tra Master script đang chạy
-   Test với Notepad mở
-   Kiểm tra hotkeys có prefix `~`

### **Problem: VMs không nhận input**

**Solution:**

1. `Ctrl+Alt+S` trong Master → Check "Found: X"
2. Verify Slave script đang chạy trong VM
3. Verify VM window title đúng trong Master script
4. `Ctrl+Alt+R` để refresh VM cache

### **Problem: Tất cả VMs phản hồi cùng lúc**

**Solution:**

-   Kiểm tra DESYNC RANGE khác nhau cho mỗi VM
-   Test với Debug Mode (`Ctrl+Alt+D` trong Slave)
-   Verify Slave script settings

### **Problem: "Failed: X" trong tooltip**

**Solution:**

-   X VMs không tìm thấy window
-   `Ctrl+Alt+R` để refresh cache
-   Verify VM đang chạy
-   Check VM window title

---

## 💡 ADVANCED USAGE

### **Scale to N VMs:**

Chỉ cần thêm VM vào list:

```ahk
vmList.Push("VM100 - VMware Workstation")  ; Thêm VM 100
```

### **Disable specific VMs:**

Comment VM trong Master script:

```ahk
; vmList.Push("VM5 - VMware Workstation")  ; Temporary disable
```

### **Test HOST only:**

Comment tất cả VMs:

```ahk
; vmList.Push("Win10-VM1 - VMware Workstation")
; vmList.Push("Win10-VM2 - VMware Workstation")
```

---

## 📚 DOCUMENTATION

-   **`MASTER_SLAVE_SETUP_GUIDE.md`**: Full setup guide với chi tiết
-   **`QUICK_START_GUIDE.md`**: Quick start cho người mới
-   **`VERSION_COMPARISON.md`**: So sánh V1 (Multiplicity) vs V2 (Master-Slave)
-   **`FEATURE_CHECKLIST_V1_V2.md`**: Feature parity checklist

---

## 🎯 BENEFITS vs MULTIPLICITY 4

| Feature         | Multiplicity 4        | Master-Slave AHK |
| --------------- | --------------------- | ---------------- |
| **Cost**        | 💰 Paid               | ✅ FREE          |
| **Stealth**     | ⚠️ Visible in VMs     | ✅ Low detection |
| **Scalability** | ✅ Unlimited          | ✅ Unlimited     |
| **Setup**       | ⚠️ Install in each VM | ✅ No install    |
| **Desync**      | ❌ None               | ✅ Built-in      |
| **Flexibility** | ⚠️ Limited            | ✅ Full control  |

---

## 🆘 SUPPORT

Nếu gặp vấn đề:

1. Đọc Troubleshooting section
2. Check debug tooltip (`Ctrl+Alt+D`)
3. Check performance monitor (`Ctrl+Alt+P`)
4. Verify VM list (`Ctrl+Alt+L`)

---

## 📝 VERSION HISTORY

-   **V1**: Multiplicity-based (multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk)
-   **V2**: Master-Slave AHK (Master_Multi_VM_EASY_CUSTOM.ahk + multiplicity_jitter_DESYNC_SLAVE.ahk)

---

**🎉 ENJOY YOUR PERFECT MASTER-SLAVE SETUP! 🎉**
