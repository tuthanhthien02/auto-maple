# 🚀 MASTER-SLAVE AHK SETUP GUIDE

## 📋 TỔNG QUAN

Hệ thống Master-Slave AHK cho phép bạn control **N VMs** từ 1 HOST machine giống Multiplicity 4, nhưng **FREE** và **STEALTH** hơn!

```
┌─────────────────────────────────────────────────────────┐
│                    HOST MACHINE                          │
│  ┌──────────────────────────────────────────────────┐  │
│  │  Master Script                                    │  │
│  │  • Nhận input từ keyboard                        │  │
│  │  • Broadcast đến tất cả VMs                      │  │
│  │  • Perfect anti-detection!                      │  │
│  └──────────────────────────────────────────────────┘  │
└────────────────┬────────────────┬────────────────────────┘
                 │                │
           ┌─────▼─────┐    ┌─────▼─────┐
           │   VM 1    │    │   VM 2    │
           │           │    │           │
           │  Slave 1  │    │  Slave 2  │
           │  Desync:  │    │  Desync:  │
           │  0-300ms  │    │  100-400ms│
           └───────────┘    └───────────┘
```

---

## ✅ YÊU CẦU

-   **Host**: Windows 10/11 với AutoHotkey v1.1+
-   **VMs**: VMware Workstation (hoặc VirtualBox)
-   **AHK Scripts**: Master_Multi_VM_EASY_CUSTOM.ahk (Host) + multiplicity_jitter_DESYNC_SLAVE.ahk (VMs)

---

## 🎯 SETUP WORKFLOW

### **STEP 1: Setup Master trên HOST** 🔧

**1.1. Tìm tên VM Windows:**

Cách 1 (Dễ nhất):

1. Chạy Master script
2. Ấn `Ctrl+Alt+L`
3. Copy tên VMs từ popup

Cách 2 (Manual):

1. Mở VM
2. Ấn `Alt+Tab` trên HOST
3. Xem tên window (vd: "Windows 10 x64 - VMware Workstation")
4. Copy CHÍNH XÁC tên đó

**1.2. Sửa Master script:**

Mở `Master_Multi_VM_EASY_CUSTOM.ahk` và uncomment + sửa tên VMs:

```ahk
global vmList := []  ; ⚠️ KHÔNG XÓA DÒNG NÀY!

; ━━━ Thêm VMs của bạn vào đây ━━━
vmList.Push("Windows 10 x64 - VMware Workstation")  ; VM 1
vmList.Push("Windows 10 Pro - VMware Workstation")  ; VM 2
vmList.Push("Windows 11 x64 - VMware Workstation")   ; VM 3
```

**1.3. Chạy Master script:**

```
Double-click Master_Multi_VM_EASY_CUSTOM.ahk
```

Startup message sẽ hiển thị:

```
⭐ INPUT MODE: HOST + VMs
• Keys sent to HOST (notepad/game)
• Keys broadcast to ALL VMs
```

---

### **STEP 2: Setup Slave trong MỖI VM** 🔧

**2.1. Copy Slave script vào VM:**

Copy `multiplicity_jitter_DESYNC_SLAVE.ahk` vào mỗi VM (vào desktop hoặc folder dễ tìm).

**2.2. Sửa DESYNC RANGE cho mỗi VM:**

Mở `multiplicity_jitter_DESYNC_SLAVE.ahk` và tìm 2 dòng này (line 189-190):

```ahk
global MinDesync := 0      ; ← SỬA!
global MaxDesync := 500    ; ← SỬA!
```

**Mỗi VM phải có DESYNC RANGE KHÁC NHAU!**

Copy & Paste từ table này:

```
VM1:  MinDesync = 0     MaxDesync = 300   (range: 0-300ms)
VM2:  MinDesync = 100   MaxDesync = 400   (range: 100-400ms)
VM3:  MinDesync = 200   MaxDesync = 500   (range: 200-500ms)
VM4:  MinDesync = 50    MaxDesync = 350   (range: 50-350ms)
VM5:  MinDesync = 150   MaxDesync = 450   (range: 150-450ms)
VM6:  MinDesync = 250   MaxDesync = 550   (range: 250-550ms)
VM7:  MinDesync = 80    MaxDesync = 380   (range: 80-380ms)
VM8:  MinDesync = 180   MaxDesync = 480   (range: 180-480ms)
VM9:  MinDesync = 120   MaxDesync = 420   (range: 120-420ms)
VM10: MinDesync = 220   MaxDesync = 520   (range: 220-520ms)
```

**Ví dụ cho VM1:**

```ahk
global MinDesync := 0      ; VM1: 0ms
global MaxDesync := 300    ; VM1: 300ms
```

**Ví dụ cho VM2:**

```ahk
global MinDesync := 100    ; VM2: 100ms
global MaxDesync := 400    ; VM2: 400ms
```

**⚠️ QUAN TRỌNG:**

-   ❌ **SAI**: Tất cả VMs dùng cùng range (0-500ms) → Anti-cheat phát hiện pattern!
-   ✅ **ĐÚNG**: Mỗi VM có range khác nhau → Perfect desync!

**2.3. Chạy Slave script trong VM:**

```
Double-click multiplicity_jitter_DESYNC_SLAVE.ahk
```

Hoặc compile thành EXE (optional):

```
Right-click → Compile Script
→ multiplicity_jitter_DESYNC_SLAVE.exe
```

**2.4. Repeat cho tất cả VMs:**

Mỗi VM cần:

-   Copy Slave script vào VM
-   Sửa DESYNC RANGE khác nhau
-   Chạy Slave script

---

### **STEP 3: Test!** 🧪

**3.1. Test HOST input:**

1. HOST: Mở Notepad
2. HOST: Ấn `Q`
3. HOST: Notepad hiển thị "Q" ✅

**3.2. Test VM broadcasting:**

1. HOST: Mở game trên HOST
2. VM1: Mở game trên VM1
3. VM2: Mở game trên VM2
4. HOST: Ấn `Q`
5. HOST: Character cast skill Q ✅
6. VM1: Character cast skill Q (sau 0-300ms) ✅
7. VM2: Character cast skill Q (sau 100-400ms) ✅

**3.3. Check Master status:**

Ấn `Ctrl+Alt+S` trên HOST:

```
📊 STATUS CHECK:
Total VMs: 3
Found: 3
Broadcasting: ENABLED
✅ All VMs connected!
```

---

## 🎮 USAGE GUIDE

### **HOTKEYS - MASTER SCRIPT:**

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

### **HOTKEYS - SLAVE SCRIPT:**

| Hotkey       | Function                               |
| ------------ | -------------------------------------- |
| `Ctrl+Alt+T` | Toggle Script ON/OFF                   |
| `Ctrl+Alt+P` | Performance Monitor (keypress stats)   |
| `Ctrl+Alt+R` | Reset Performance Statistics           |
| `Ctrl+Alt+D` | Toggle Debug Mode (show keypress info) |

### **INPUT FLOW:**

```
HOST Keyboard Input (Q)
    ↓
Master Script (~q::)
    ↓ (BroadcastKeyAsync("q"))
    ├─→ VM1: ControlSend(Q) → Slave1 nhận Q → Delay 0-300ms → SendInput(Q)
    ├─→ VM2: ControlSend(Q) → Slave2 nhận Q → Delay 100-400ms → SendInput(Q)
    └─→ VM3: ControlSend(Q) → Slave3 nhận Q → Delay 200-500ms → SendInput(Q)
```

---

## 🔍 TROUBLESHOOTING

### **Problem: Host input không xuất hiện**

**Solution:**

-   Kiểm tra Master script đang chạy
-   Đảm bảo hotkeys có prefix `~` (không block input)
-   Test với Notepad trước

### **Problem: VMs không nhận input**

**Solution:**

1. Kiểm tra Master script: Ấn `Ctrl+Alt+S`
    - Nếu "Found: 0" → VM list sai, ấn `Ctrl+Alt+L` để copy tên đúng
2. Kiểm tra Slave script đang chạy trong VM
3. Kiểm tra VM window title đúng trong Master script

### **Problem: Tất cả VMs phản hồi cùng lúc**

**Solution:**

-   Đảm bảo mỗi VM có DESYNC RANGE khác nhau
-   Kiểm tra Slave script settings trong mỗi VM
-   Test với Debug Mode (`Ctrl+Alt+D` trong Slave)

### **Problem: "Failed: X" trong tooltip**

**Solution:**

-   X VMs không tìm thấy window
-   Refresh VM cache: Ấn `Ctrl+Alt+R`
-   Kiểm tra VM đang chạy
-   Kiểm tra VM window title đúng

---

## 💡 TIPS & TRICKS

### **1. Scale to N VMs:**

Chỉ cần thêm VM vào `vmList`:

```ahk
vmList.Push("VM20 - VMware Workstation")  ; Thêm VM 20
```

### **2. Disable specific VMs:**

Comment VM trong Master script:

```ahk
; vmList.Push("VM5 - VMware Workstation")  ; Temporary disable
```

### **3. Test HOST only:**

Comment tất cả VMs trong Master script:

```ahk
; vmList.Push("Win10-VM1 - VMware Workstation")
; vmList.Push("Win10-VM2 - VMware Workstation")
```

### **4. Compile to EXE:**

Master: Right-click → Compile Script → `Master_Multi_VM.exe`
Slave: Right-click → Compile Script → `multiplicity_jitter_DESYNC_SLAVE.exe`

### **5. Stealth Mode:**

Sử dụng các file compile với tên stealth:

-   Master: `WindowsTaskScheduler.exe`
-   Slave: `SystemAudioService.exe`

---

## 📊 PERFORMANCE

### **Master Script:**

-   Latency: < 1ms per keypress
-   CPU: < 1% idle
-   Memory: ~2-5 MB

### **Slave Script:**

-   Latency: Desync range (0-500ms)
-   CPU: < 1% idle
-   Memory: ~2-5 MB

### **Network:**

-   Không cần network (local ControlSend)
-   Không cần port forwarding
-   Perfect for local VMs

---

## 🎯 KEY BENEFITS

✅ **FREE**: Không cần Multiplicity license
✅ **STEALTH**: Chỉ AHK visible trong VMs
✅ **SCALABLE**: Thêm bao nhiêu VMs cũng được
✅ **FLEXIBLE**: Customize desync range cho mỗi VM
✅ **PERFORMANCE**: Low latency, low CPU usage
✅ **RELIABLE**: Auto-retry on failed broadcasts

---

## 📚 RELATED FILES

-   `Master_Multi_VM_EASY_CUSTOM.ahk` - Master script (Host)
-   `multiplicity_jitter_DESYNC_SLAVE.ahk` - Slave script (VMs)
-   `QUICK_START_GUIDE.md` - Quick setup guide
-   `MULTI_VM_SETUP_GUIDE.md` - Multi-VM setup guide
-   `VERSION_COMPARISON.md` - V1 vs V2 comparison

---

## 🆘 SUPPORT

Nếu gặp vấn đề:

1. Đọc Troubleshooting section
2. Check debug tooltip (`Ctrl+Alt+D`)
3. Check performance monitor (`Ctrl+Alt+P`)
4. Verify VM list (`Ctrl+Alt+L`)

---

**🎉 ENJOY YOUR PERFECT MASTER-SLAVE SETUP! 🎉**
