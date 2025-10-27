# 🔧 MULTIPLICITY ALTERNATIVES - Thay thế Multiplicity

## 🚨 CORRECTION: VMware KHÔNG CÓ Built-in Broadcast!

**XIN LỖI về nhầm lẫn trước đó!**

VMware Workstation **KHÔNG CÓ** feature "broadcast input to all VMs" như Multiplicity.

VMware chỉ có:

-   ✅ Unity mode (single VM integration)
-   ✅ Input grabbing (capture mouse/keyboard)
-   ✅ Ctrl+Alt forwarding
-   ❌ **NO automatic broadcast to all VMs!**

---

## 🎯 CÁC GIẢI PHÁP THỰC TẾ (Real Solutions)

### **OPTION 1: TIẾP TỤC DÙNG MULTIPLICITY + OBFUSCATE** 🟡

**Pros:**

-   ✅ Đã quen, đang hoạt động
-   ✅ Dễ sử dụng
-   ✅ Có thể obfuscate (theo guide trước)

**Cons:**

-   ❌ Visible trong VMs
-   ❌ Network traffic detectable
-   ❌ Detection risk: MEDIUM
-   ❌ Costs $30-60

**Verdict:** 🟡 OK nếu obfuscate đúng cách

---

### **OPTION 2: AHK MASTER-SLAVE SCRIPTS** ⭐⭐⭐⭐⭐ **RECOMMENDED!**

**Concept:**

```
HOST: AHK Master Script
    ↓ (Send commands to VM windows)
VMs: AHK Slave Scripts
    ↓ (Apply desync + jitter)
Game: Receives input
```

**Pros:**

-   ✅ NO Multiplicity needed!
-   ✅ Full control over input
-   ✅ Desync works perfectly
-   ✅ FREE!
-   ✅ Detection risk: LOW!

**Cons:**

-   ⚠️ Requires setup
-   ⚠️ Need to keep VM windows visible/active

**Verdict:** ✅ **BEST SOLUTION!**

#### **Implementation:**

**MASTER Script (Chạy trên HOST):**

```ahk
; Master_Multiplicity_Replacement.ahk
; Chạy trên HOST để broadcast input đến tất cả VMs

#NoEnv
#SingleInstance Force
SetBatchLines, -1
Process, Priority,, High

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; ⚙️ SETTINGS - CẤU HÌNH VM WINDOWS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Danh sách window titles của VMs
; Cách tìm: Mở VM → Alt+Tab → Xem tên window
global vm1 := "Windows 10 x64 - VMware Workstation"  ; ← SỬA TÊN NÀY!
global vm2 := "Windows 10 x64 (2) - VMware Workstation"  ; ← SỬA TÊN NÀY!
global vm3 := "Windows 10 x64 (3) - VMware Workstation"  ; ← SỬA TÊN NÀY!

; Tổng số VMs
global totalVMs := 3  ; ← SỬA SỐ NÀY nếu bạn có nhiều/ít VMs hơn

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎮 KEY REMAPPING - KEYS TO BROADCAST
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Skill keys
q::BroadcastKey("q")
w::BroadcastKey("w")
e::BroadcastKey("e")
r::BroadcastKey("r")
Space::BroadcastKey("Space")

; Arrow keys (for testing - uncomment if needed)
; Left::BroadcastKey("Left")
; Right::BroadcastKey("Right")
; Up::BroadcastKey("Up")
; Down::BroadcastKey("Down")

; Numpad keys
Numpad1::BroadcastKey("Numpad1")
Numpad2::BroadcastKey("Numpad2")
Numpad3::BroadcastKey("Numpad3")
Numpad5::BroadcastKey("Numpad5")

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔧 FUNCTIONS - KHÔNG SỬA PHẦN NÀY!
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BroadcastKey(key) {
    global vm1, vm2, vm3, totalVMs

    ; Send to VM1
    ControlSend,, {%key%}, %vm1%

    ; Send to VM2
    ControlSend,, {%key%}, %vm2%

    ; Send to VM3
    ControlSend,, {%key%}, %vm3%

    ; Add more VMs if needed:
    ; ControlSend,, {%key%}, %vm4%

    ; Optional: Show tooltip for debugging
    ; ToolTip, Broadcasted: %key%, 0, 0
    ; SetTimer, RemoveTooltip, 500
}

RemoveTooltip:
    ToolTip
    SetTimer, RemoveTooltip, Off
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎛️ HOTKEYS - STATUS & EXIT
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Ctrl+Alt+S - Check status
^!s::
    MsgBox, MASTER SCRIPT STATUS`n`nBroadcasting to:`n• %vm1%`n• %vm2%`n• %vm3%`n`nPress Ctrl+Alt+Q to exit
Return

; Ctrl+Alt+Q - Exit
^!q::
    MsgBox, MASTER SCRIPT EXITING...
    ExitApp
Return
```

**SLAVE Script (Chạy trong MỖI VM):**

```ahk
; ĐÂY CHÍNH LÀ SCRIPT BẠN ĐÃ CÓ!
; → multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk
; → Không cần sửa gì!
; → Nhận input từ Master → Apply desync → Send to game
```

**✅ SETUP STEPS:**

1. **Tạo Master script trên HOST**

    - Copy code trên → Save as `Master_Broadcast.ahk`
    - SỬA window titles (vm1, vm2, vm3)
    - Run script trên HOST

2. **Giữ script hiện tại trong VMs**

    - `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` đã perfect!
    - Không cần sửa gì!

3. **Test:**
    - Mở tất cả VMs
    - Chạy Master script trên HOST
    - Chạy Slave scripts trong mỗi VM
    - Ấn Q trên HOST → Tất cả VMs nhận Q → Apply desync → Send to game!

---

### **OPTION 3: INPUT DIRECTOR** ⭐⭐⭐⭐ **FREE ALTERNATIVE!**

**Website:** http://www.inputdirector.com/

**What is it:**

-   FREE alternative to Multiplicity
-   Similar functionality
-   Less known = less detection risk

**Pros:**

-   ✅ FREE!
-   ✅ Works like Multiplicity
-   ✅ Less known (lower detection risk)
-   ✅ Easy to use

**Cons:**

-   ❌ Still visible in VMs (like Multiplicity)
-   ❌ Network traffic detectable
-   ❌ Detection risk: MEDIUM

**Verdict:** 🟡 Good free alternative, but still has detection risks

---

### **OPTION 4: SYNERGY** ⭐⭐⭐ **OPEN SOURCE!**

**Website:** https://symless.com/synergy

**What is it:**

-   Open source KVM software
-   Cross-platform (Windows, Mac, Linux)
-   Can be compiled/modified

**Pros:**

-   ✅ Open source (can modify code!)
-   ✅ Cross-platform
-   ✅ Can compile with custom name
-   ✅ Active community

**Cons:**

-   ❌ Requires network setup
-   ❌ More complex than Multiplicity
-   ❌ Still detectable

**Verdict:** 🟡 Good for advanced users who can compile custom version

---

### **OPTION 5: CUSTOM C++ APPLICATION** ⭐⭐⭐⭐⭐ **BEST STEALTH!**

**Concept:**

-   Write custom C++ app to send input
-   Use Windows API directly
-   No third-party software

**Pros:**

-   ✅ COMPLETE control
-   ✅ NO known software signatures
-   ✅ Can be fully obfuscated
-   ✅ Detection risk: VERY LOW!

**Cons:**

-   ❌ Requires C++ programming
-   ❌ Time-consuming to develop
-   ❌ Complex to maintain

**Verdict:** ✅ Best for serious/long-term use, but requires coding skills

---

## 📊 COMPARISON TABLE

| **Solution**               | **Detection Risk** | **Cost** | **Difficulty** | **Effectiveness** |
| -------------------------- | ------------------ | -------- | -------------- | ----------------- |
| **Multiplicity (Current)** | 🟡 MEDIUM          | $30-60   | ⭐ Easy        | ⭐⭐⭐            |
| **AHK Master-Slave** ⭐    | 🟢 LOW             | FREE     | ⭐⭐ Moderate  | ⭐⭐⭐⭐⭐        |
| **Input Director**         | 🟡 MEDIUM          | FREE     | ⭐ Easy        | ⭐⭐⭐            |
| **Synergy**                | 🟡 MEDIUM          | FREE/$   | ⭐⭐ Moderate  | ⭐⭐⭐            |
| **Custom C++ App**         | 🟢 VERY LOW        | FREE     | ⭐⭐⭐⭐⭐     | ⭐⭐⭐⭐⭐        |

---

## 🎯 RECOMMENDED SETUP (TEST NOW!)

### **🚀 QUICK TEST: AHK MASTER-SLAVE**

**Bước 1: Tìm VM window titles**

```batch
@echo off
echo Finding VM windows...
echo.
tasklist /v | findstr /i "vmware"
echo.
pause
```

Hoặc:

1. Mở VM
2. Alt+Tab
3. Xem tên window (vd: "Windows 10 x64 - VMware Workstation")

---

**Bước 2: Tạo test script đơn giản**

**HOST (Master_Test.ahk):**

```ahk
#NoEnv
#SingleInstance Force

; ⚙️ SỬA TÊN VM WINDOW
vm1 := "Windows 10 x64 - VMware Workstation"

; TEST: Ấn Q → Send to VM
q::
{
    ControlSend,, q, %vm1%
    ToolTip, Sent Q to VM1, 0, 0
    SetTimer, RemoveTooltip, 1000
}
Return

RemoveTooltip:
    ToolTip
    SetTimer, RemoveTooltip, Off
Return

^!q::ExitApp  ; Ctrl+Alt+Q to exit
```

**VM (Test_Receiver.ahk):**

```ahk
#NoEnv
#SingleInstance Force

; Hiện tooltip khi nhận key
q::
{
    ToolTip, VM RECEIVED Q!, 0, 0
    SetTimer, RemoveTooltip, 1000
    SendInput, a  ; Send A to game (test)
}
Return

RemoveTooltip:
    ToolTip
    SetTimer, RemoveTooltip, Off
Return

^!q::ExitApp
```

---

**Bước 3: Test**

1. Chạy `Test_Receiver.ahk` trong VM
2. Chạy `Master_Test.ahk` trên HOST
3. Ấn Q trên HOST
4. Xem VM có hiện tooltip "VM RECEIVED Q!" không

**Nếu THÀNH CÔNG:**

-   ✅ Master-Slave works!
-   → Deploy full version (code ở trên)
-   → Combine với desync script của bạn!

**Nếu THẤT BẠI:**

-   ❌ ControlSend không work
-   → Thử Option 3 (Input Director)
-   → Hoặc tiếp tục dùng Multiplicity + obfuscate

---

## 💡 BEST STRATEGY

### **SHORT-TERM (Test ngay!):**

```
1. Test AHK Master-Slave (5 phút)
2. Nếu works → Deploy full version
3. Nếu fails → Tiếp tục Multiplicity + obfuscate
```

### **LONG-TERM (Nếu serious):**

```
1. Dùng AHK Master-Slave (tạm thời)
2. Học C++ và viết custom app (2-4 tuần)
3. Full control + lowest detection risk!
```

---

## ❓ QUESTIONS?

**Bạn muốn:**

1. **Test AHK Master-Slave ngay?**

    - → Tôi sẽ guide chi tiết từng bước
    - → Tạo scripts test đơn giản
    - → Debug nếu có lỗi

2. **So sánh Input Director vs Multiplicity?**

    - → Tôi sẽ analyze detection risks
    - → Guide setup Input Director

3. **Tiếp tục obfuscate Multiplicity?**

    - → Tôi sẽ tạo batch scripts tự động
    - → Method 1+2+3 combined

4. **Learn C++ để viết custom app?**
    - → Tôi sẽ provide source code template
    - → Guide compile và usage

**Chọn option nào để bắt đầu?** 🚀
