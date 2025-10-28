# 🧪 TEST MASTER-SLAVE AHK SETUP - QUICK START GUIDE

## 🎯 MỤC ĐÍCH

Test xem `ControlSend` từ HOST → VM có hoạt động không.

**Nếu test THÀNH CÔNG:**

-   ✅ Bạn có thể dùng AHK Master-Slave thay cho Multiplicity!
-   ✅ Detection risk: LOW! 🟢
-   ✅ FREE!
-   ✅ NO Multiplicity needed!

**Nếu test THẤT BẠI:**

-   ❌ `ControlSend` không work với setup của bạn
-   → Thử Input Director (free alternative)
-   → Hoặc tiếp tục Multiplicity + obfuscate

---

## 📋 CHUẨN BỊ

### **Cần có:**

1. ✅ HOST machine (máy chính)
2. ✅ VMware Workstation với ít nhất 1 VM
3. ✅ AutoHotkey đã cài trên cả HOST và VM
4. ✅ 2 files:
    - `Master_Test.ahk` (chạy trên HOST)
    - `Test_Receiver.ahk` (chạy trong VM)

---

## 🚀 STEP-BY-STEP TEST

### **STEP 1: Tìm VM Window Title**

**Cách 1: Dùng Alt+Tab**

1. Mở VM của bạn
2. Ấn `Alt+Tab` trên HOST
3. Xem tên window VM (ví dụ: "Windows 10 x64 - VMware Workstation")
4. Copy tên chính xác!

**Cách 2: Dùng Master_Test.ahk**

1. Chạy `Master_Test.ahk` trên HOST
2. Ấn `Ctrl+Alt+L`
3. Sẽ hiện list tất cả VMware windows
4. Copy tên window

---

### **STEP 2: Sửa Master_Test.ahk**

1. Mở `Master_Test.ahk` bằng text editor
2. Tìm dòng:

```ahk
global vmWindowTitle := "Windows 10 x64 - VMware Workstation"
```

3. SỬA thành tên VM của bạn (phải chính xác 100%!)

**Ví dụ:**

```ahk
; Nếu VM của bạn tên "Win10-Test - VMware Workstation"
global vmWindowTitle := "Win10-Test - VMware Workstation"

; Nếu VM tên "Ubuntu 22.04 - VMware Workstation"
global vmWindowTitle := "Ubuntu 22.04 - VMware Workstation"
```

4. Save file

---

### **STEP 3: Copy Test_Receiver.ahk vào VM**

**Cách 1: Copy-Paste qua Shared Folder**

1. Enable Shared Folders trong VMware
2. Copy `Test_Receiver.ahk` vào shared folder
3. Access từ VM

**Cách 2: Copy-Paste qua clipboard**

1. Mở `Test_Receiver.ahk` trên HOST
2. Copy toàn bộ nội dung
3. Paste vào Notepad trong VM
4. Save as `Test_Receiver.ahk` trong VM

**Cách 3: Network Share**

1. Share folder từ HOST
2. Access từ VM
3. Copy file

---

### **STEP 4: Chạy Scripts**

**Thứ tự quan trọng:**

1. **TRONG VM:** Chạy `Test_Receiver.ahk` TRƯỚC

    - Double-click `Test_Receiver.ahk` trong VM
    - Sẽ thấy tooltip: "TEST RECEIVER RUNNING!"
    - Nghe tiếng beep

2. **TRÊN HOST:** Chạy `Master_Test.ahk` SAU
    - Double-click `Master_Test.ahk` trên HOST
    - Sẽ thấy tooltip: "MASTER TEST SCRIPT RUNNING!"
    - Nghe tiếng beep

---

### **STEP 5: Test Input**

**Trên HOST, ấn các phím:**

1. Ấn `Q`

    - HOST sẽ hiện: "[HOST] Sent Q to VM"
    - VM phải hiện: "✅ VM RECEIVED Q!"
    - Nghe 2 tiếng beep (1 từ HOST, 1 từ VM)

2. Ấn `W`

    - HOST: "[HOST] Sent W to VM"
    - VM: "✅ VM RECEIVED W!"

3. Ấn `E`
    - HOST: "[HOST] Sent E to VM"
    - VM: "✅ VM RECEIVED E!"

---

## ✅ KẾT QUẢ TEST

### **THÀNH CÔNG! ✅**

**Nếu thấy:**

-   ✅ VM hiện tooltip "VM RECEIVED Q/W/E!"
-   ✅ Nghe beep từ cả HOST và VM
-   ✅ Statistics trong VM tăng lên

**→ MASTER-SLAVE WORKS! 🎉**

**Next steps:**

1. Deploy full Master-Slave scripts
2. Thay thế Multiplicity
3. Giảm detection risk!

---

### **THẤT BẠI! ❌**

**Nếu thấy:**

-   ❌ VM KHÔNG hiện tooltip
-   ❌ Chỉ nghe beep từ HOST
-   ❌ Statistics trong VM = 0

**→ CONTROLSEND KHÔNG WORK!**

**Troubleshooting:**

#### **Issue 1: VM Window Not Found**

**Triệu chứng:**

-   HOST hiện: "[ERROR] VM Window Not Found!"

**Giải pháp:**

1. Ấn `Ctrl+Alt+L` trong Master script
2. Xem list VMware windows
3. Copy CHÍNH XÁC tên window
4. Sửa lại `vmWindowTitle` trong Master script
5. Restart Master script

---

#### **Issue 2: ControlSend Blocked by VMware**

**Triệu chứng:**

-   VM window found
-   HOST gửi OK
-   VM KHÔNG nhận

**Giải pháp:**

**A. Check VMware Settings:**

```
VMware → Edit → Preferences → Input
✅ Check: "Grab keyboard and mouse input on mouse click"
✅ Uncheck: "Hide mouse cursor on key input from mouse or keyboard"
```

**B. Try Different SendMode:**

Edit `Master_Test.ahk`, thay:

```ahk
ControlSend,, q, %vmWindowTitle%
```

Thành:

```ahk
; Method 1: SendEvent
SendMode, Event
ControlSend,, q, %vmWindowTitle%

; Method 2: PostMessage (nếu Method 1 fail)
PostMessage, 0x100, 0x51, 0,, %vmWindowTitle%  ; 0x51 = Q key

; Method 3: Direct Send (VM phải active)
WinActivate, %vmWindowTitle%
Send, q
```

**C. VM Input Settings:**

Trong VM:

1. Disable "Enhanced Keyboard" trong VMware Tools
2. Restart VM
3. Test lại

---

#### **Issue 3: AHK Script Không Nhận**

**Triệu chứng:**

-   ControlSend works
-   Nhưng AHK script trong VM không trigger

**Giải pháp:**

Edit `Test_Receiver.ahk`, thay hotkey prefix:

```ahk
; Original
q::
{
    ...
}

; Try with ~ prefix (passthrough)
~q::
{
    ...
}

; Try with $ prefix (block)
$q::
{
    ...
}
```

---

## 🔧 UTILITY HOTKEYS

### **Master_Test.ahk (HOST):**

| **Hotkey**   | **Function**            |
| ------------ | ----------------------- |
| `Q, W, E`    | Send test keys to VM    |
| `Ctrl+Alt+S` | Check status            |
| `Ctrl+Alt+L` | List all VMware windows |
| `Ctrl+Alt+Q` | Exit                    |

### **Test_Receiver.ahk (VM):**

| **Hotkey**   | **Function**          |
| ------------ | --------------------- |
| `Q, W, E`    | Receive and show keys |
| `Ctrl+Alt+S` | Show statistics       |
| `Ctrl+Alt+R` | Reset statistics      |
| `Ctrl+Alt+Q` | Exit                  |

---

## 📊 EXPECTED OUTPUT

### **Successful Test:**

```
HOST:
  [Ấn Q]
  → Tooltip: "[HOST] Sent Q to VM"
  → Beep: 500 Hz

VM:
  → Tooltip: "✅ VM RECEIVED Q!"
             Total Received: 1
             Last Key: Q
             Time: 14:23:45
  → Beep: 1000 Hz
```

---

## 🎯 NEXT STEPS

### **Nếu Test THÀNH CÔNG:**

1. **Deploy Full Scripts:**

    - Xem `MULTIPLICITY_ALTERNATIVES.md`
    - Section: "OPTION 2: AHK MASTER-SLAVE SCRIPTS"
    - Có full Master và Slave scripts

2. **Combine với Desync:**

    - Master script → Broadcast to VMs
    - Slave script = `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk`
    - Mỗi VM có desync khác nhau!

3. **Uninstall Multiplicity:**
    - Không cần Multiplicity nữa!
    - Save $30-60
    - Reduce detection risk!

---

### **Nếu Test THẤT BẠI:**

1. **Try Input Director:**

    - FREE alternative to Multiplicity
    - Download: http://www.inputdirector.com/
    - Setup tương tự Multiplicity

2. **Obfuscate Multiplicity:**

    - Xem `MULTIPLICITY_OBFUSCATION_GUIDE.md`
    - Method 1+2+3
    - Detection risk: MEDIUM 🟡

3. **Learn Advanced Methods:**
    - Custom C++ app (long-term)
    - Process injection
    - Kernel-level hooks

---

## 💡 TIPS & TRICKS

### **Multiple VMs:**

Nếu muốn test nhiều VMs cùng lúc:

```ahk
; Master_Test.ahk
global vm1 := "Win10-1 - VMware Workstation"
global vm2 := "Win10-2 - VMware Workstation"
global vm3 := "Win10-3 - VMware Workstation"

q::
{
    ControlSend,, q, %vm1%
    ControlSend,, q, %vm2%
    ControlSend,, q, %vm3%
    ToolTip, Sent Q to all VMs!, 10, 10
    SetTimer, RemoveTooltip, 1000
}
```

---

### **Performance:**

Nếu muốn fast broadcasting:

```ahk
SetBatchLines, -1  ; No delay between lines
Process, Priority,, High  ; High priority
#MaxThreadsPerHotkey 10  ; Allow multiple threads
```

---

### **Debug Mode:**

Nếu muốn xem chi tiết:

```ahk
; Master script
q::
{
    startTime := A_TickCount
    ControlSend,, q, %vmWindowTitle%
    endTime := A_TickCount

    latency := endTime - startTime
    ToolTip, Sent Q`nLatency: %latency% ms, 10, 10
}
```

---

## ❓ FAQ

### **Q: VM phải active/visible không?**

**A:** Không! `ControlSend` works ngay cả khi VM minimized hoặc in background.

---

### **Q: Có thể send mouse clicks không?**

**A:** Có! Dùng `ControlClick`:

```ahk
ControlClick, x100 y200, %vmWindowTitle%
```

---

### **Q: Performance có tốt không?**

**A:** Rất tốt! Latency < 10ms trong hầu hết trường hợp.

---

### **Q: Có conflict với Multiplicity không?**

**A:** Không! Có thể chạy song song để compare.

---

### **Q: Có thể dùng với game fullscreen không?**

**A:** Có, nhưng VM phải ở windowed hoặc windowed fullscreen mode.

---

## 🎉 GOOD LUCK!

**Happy testing! 🚀**

**Nếu có vấn đề, cho tôi biết:**

1. Error message (nếu có)
2. VM window title (exact)
3. VMware version
4. AHK version

Tôi sẽ debug và fix! 💪
