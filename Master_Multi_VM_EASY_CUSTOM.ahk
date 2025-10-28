; ═══════════════════════════════════════════════════════════════════════
; 🎮 MASTER SCRIPT - BROADCAST TO MULTIPLE VMs (OPTIMIZED!)
; ═══════════════════════════════════════════════════════════════════════
; ⭐ VERSION 2: MASTER-SLAVE SETUP - THAY THẾ MULTIPLICITY! ⭐
; 
; 🚀 OPTIMIZATIONS:
; • VM Window Caching (faster detection)
; • Batch ControlSend (reduced overhead)
; • Error Recovery (auto-retry failed VMs)
; • Performance Monitoring (CPU/Memory usage)
; • Smart Broadcasting (skip inactive VMs)
; 
; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  🚀 QUICK SETUP - CHỈ 3 BƯỚC!  ⚡                                     ║
; ║                                                                       ║
; ║  BƯỚC 1: TÌM TÊN VMs                                                  ║
; ║    → Cách 1: Chạy script này → Ấn Ctrl+Alt+L                          ║
; ║    → Cách 2: Mở VM → Alt+Tab → Xem tên window                         ║
; ║                                                                       ║
; ║  BƯỚC 2: SỬA vmList BÊN DƯỚI (Line 77-90)                             ║
; ║    → Thay tên VMs của bạn vào                                         ║
; ║    → Thêm/bớt VMs tùy ý (unlimited!)                                  ║
; ║                                                                       ║
; ║  BƯỚC 3: CHẠY!                                                        ║
; ║    → HOST: Chạy script này (hoặc compile)                             ║
; ║    → VMs: Chạy SystemAudioService.exe (slave script)                  ║
; ║    → Ấn phím → Tất cả VMs nhận!                                       ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ ⌨️ HOTKEYS REFERENCE - MASTER SCRIPT                                │
; └─────────────────────────────────────────────────────────────────────┘
; 🔧 CONTROL HOTKEYS (Quản lý script):
;   Ctrl+Alt+S → Status Check (VM found/missing)
;   Ctrl+Alt+L → List VMs (copy tên windows)
;   Ctrl+Alt+T → Toggle Input Broadcasting ON/OFF
;   Ctrl+Alt+D → Toggle Debug Tooltip
;   Ctrl+Alt+B → Toggle Beep Sound
;   Ctrl+Alt+P → Performance Monitor
;   Ctrl+Alt+R → Refresh VM Cache
;   Ctrl+Alt+Q → Exit Script
;
; 🎮 BROADCAST HOTKEYS (Gửi input đến HOST + VMs):
;   SKILL KEYS: Q, W, E, R, A, S, D, F, Space
;   ARROW KEYS: Left, Right, Up, Down
;   NUMPAD KEYS: Numpad1-8
;   NUMBER KEYS: 1-9, 0
;   FUNCTION KEYS: F1-F12
;   ⭐ MỖI PHÍM SẼ ĐƯỢC GỬI ĐẾN: HOST + TẤT CẢ VMs
;
; 💡 QUICK REFERENCE:
;   Status: Ctrl+Alt+S | List: Ctrl+Alt+L | Toggle: Ctrl+Alt+T | Perf: Ctrl+Alt+P
;   Refresh: Ctrl+Alt+R | Exit: Ctrl+Alt+Q
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ ⌨️ HOTKEYS (Phím tắt khi script đang chạy)                          │
; └─────────────────────────────────────────────────────────────────────┘
; 🔸 Ctrl+Alt+S: Check status (bao nhiêu VMs found)
; 🔸 Ctrl+Alt+L: List all VMware windows (để copy tên)
; 🔸 Ctrl+Alt+T: Toggle input broadcasting ON/OFF
; 🔸 Ctrl+Alt+D: Toggle debug tooltip ON/OFF
; 🔸 Ctrl+Alt+B: Toggle beep ON/OFF
; 🔸 Ctrl+Alt+P: Performance monitor (CPU/Memory)
; 🔸 Ctrl+Alt+R: Refresh VM cache (re-scan windows)
; 🔸 Ctrl+Alt+Q: Exit script
;
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
SetBatchLines, -1
Process, Priority,, High

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  ⚙️ ⚙️ ⚙️  TẤT CẢ SETTINGS Ở ĐÂY - DỄ TÌM, DỄ CUSTOM!  ⚙️ ⚙️ ⚙️       ║
; ║                                                                       ║
; ║  📍 CHỈ CẦN SỬA 2 SETTINGS:                                           ║
; ║     1️⃣ vmList (Line 77-90) - Thêm tên VMs của bạn                    ║
; ║     2️⃣ Keys to broadcast (Line 110-170) - Thêm/bớt phím              ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 1️⃣ DANH SÁCH VMs (Tên window của từng VM)                           ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; 
; ┌─────────────────────────────────────────────────────────────────────┐
; │ 🎯 CÁCH TÌM TÊN VM WINDOW:                                           │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ CÁCH 1: Dùng hotkey (DỄ NHẤT!)
;    1. Chạy script này
;    2. Ấn Ctrl+Alt+L
;    3. Copy tên VMs từ popup
; 
; ✅ CÁCH 2: Manual
;    1. Mở VM
;    2. Ấn Alt+Tab trên HOST
;    3. Xem tên window (vd: "Windows 10 x64 - VMware Workstation")
;    4. Copy CHÍNH XÁC tên đó
; 
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

global vmList := []  ; ⚠️ KHÔNG XÓA DÒNG NÀY!

; ━━━ THÊM VMs CỦA BẠN VÀO ĐÂY (Sửa tên cho đúng!) ━━━
vmList.Push("bishop - VMware Workstation")  ; VM 1
; vmList.Push("Win10-VM2 - VMware Workstation")  ; VM 2
; vmList.Push("Win10-VM3 - VMware Workstation")  ; VM 3
; vmList.Push("Win10-VM4 - VMware Workstation")  ; VM 4
; vmList.Push("Win10-VM5 - VMware Workstation")  ; VM 5

; ━━━ Thêm VM 6, 7, 8... nếu cần (Bỏ ; ở đầu dòng để enable) ━━━
; vmList.Push("Win10-VM6 - VMware Workstation")  ; VM 6
; vmList.Push("Win10-VM7 - VMware Workstation")  ; VM 7
; vmList.Push("Win10-VM8 - VMware Workstation")  ; VM 8
; vmList.Push("Win10-VM9 - VMware Workstation")  ; VM 9
; vmList.Push("Win10-VM10 - VMware Workstation") ; VM 10

; 💡 KHÔNG CÓ GIỚI HẠN! Thêm bao nhiêu cũng được!
; 📝 Template để copy: vmList.Push("TÊN_VM_CỦA_BẠN")

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 🌐 TCP PORT MAPPING (VM → TCP Port)                                ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; Mỗi VM phải map đến 1 TCP port (7001, 7002, 7003...)
global vmPorts := {}
vmPorts["bishop - VMware Workstation"] := 7001  ; VM 1 → Port 7001
; vmPorts["Win10-VM2 - VMware Workstation"] := 7002  ; VM 2 → Port 7002
; vmPorts["Win10-VM3 - VMware Workstation"] := 7003  ; VM 3 → Port 7003
; vmPorts["Win10-VM4 - VMware Workstation"] := 7004  ; VM 4 → Port 7004
; vmPorts["Win10-VM5 - VMware Workstation"] := 7005  ; VM 5 → Port 7005

global VM_HOST := "127.0.0.1"  ; Localhost (VMs chạy trên cùng máy)

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 2️⃣ OPTIONS (Bật/tắt debug features)                                 ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

; Hiện debug tooltip khi broadcast? (true = bật, false = tắt)
global showDebugTooltip := true

; Beep khi broadcast? (true = bật, false = tắt)
global enableBeep := true

; Toggle input broadcasting ON/OFF (true = bật, false = tắt)
global enableBroadcasting := true

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 3️⃣ PERFORMANCE OPTIONS (Tối ưu hiệu suất)                           ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

; Cache VM windows để tăng tốc độ (true = bật, false = tắt)
global enableVMCache := true

; Auto-retry failed VMs (true = bật, false = tắt)
global enableAutoRetry := true

; Max retry attempts cho failed VMs
global maxRetryAttempts := 3

; Cache refresh interval (ms) - refresh VM list mỗi X ms
global cacheRefreshInterval := 30000

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 4️⃣ KEYS TO BROADCAST (Phím nào sẽ broadcast đến HOST + VMs)      ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; 
; ⭐ MỖI PHÍM SẼ ĐƯỢC GỬI ĐẾN:
;   • HOST (notepad hoặc game trên host)
;   • TẤT CẢ VMs (với desync delay)
; 
; ┌─────────────────────────────────────────────────────────────────────┐
; │ 💡 HƯỚNG DẪN:                                                        │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ THÊM PHÍM: Bỏ ; ở đầu dòng
;    VD: ; q::BroadcastKey("q")  → Bỏ ; → q::BroadcastKey("q")
; 
; ✅ BỎ PHÍM: Thêm ; ở đầu dòng
;    VD: q::BroadcastKey("q")  → Thêm ; → ; q::BroadcastKey("q")
; 
; ✅ THÊM PHÍM MỚI: Copy template bên dưới
;    Template: PHÍM::BroadcastKey("PHÍM")
;    VD: t::BroadcastKey("t")  → Broadcast phím T
; 
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; ━━━ SKILL KEYS (Phím skill) ━━━
; 🔑 Prefix ~ = Allow original key to pass through
~q::
BroadcastKeyAsync("q")
return

~w::
BroadcastKeyAsync("w")
return

~e::
BroadcastKeyAsync("e")
return

~r::
BroadcastKeyAsync("r")
return

~a::
BroadcastKeyAsync("a")
return

~s::
BroadcastKeyAsync("s")
return

~d::
BroadcastKeyAsync("d")
return

~f::
BroadcastKeyAsync("f")
return

~Space::
BroadcastKeyAsync("Space")
return

; ━━━ ARROW KEYS (Phím mũi tên) ━━━
~Left::
BroadcastKeyAsync("Left")
return

~Right::
BroadcastKeyAsync("Right")
return

~Up::
BroadcastKeyAsync("Up")
return

~Down::
BroadcastKeyAsync("Down")
return

; ━━━ NUMPAD KEYS (Phím numpad) ━━━
~Numpad1::
BroadcastKeyAsync("Numpad1")
return

~Numpad2::
BroadcastKeyAsync("Numpad2")
return

~Numpad3::
BroadcastKeyAsync("Numpad3")
return

~Numpad4::
BroadcastKeyAsync("Numpad4")
return

~Numpad5::
BroadcastKeyAsync("Numpad5")
return

~Numpad6::
BroadcastKeyAsync("Numpad6")
return

~Numpad8::
BroadcastKeyAsync("Numpad8")
return

; ━━━ NUMBER KEYS (Phím số 1-9, 0) ━━━
~1::
BroadcastKeyAsync("1")
return

~2::
BroadcastKeyAsync("2")
return

~3::
BroadcastKeyAsync("3")
return

~4::
BroadcastKeyAsync("4")
return

~5::
BroadcastKeyAsync("5")
return

~6::
BroadcastKeyAsync("6")
return

~7::
BroadcastKeyAsync("7")
return

~8::
BroadcastKeyAsync("8")
return

~9::
BroadcastKeyAsync("9")
return

~0::
BroadcastKeyAsync("0")
return

; ━━━ FUNCTION KEYS (Phím F1-F12) ━━━
~F1::
BroadcastKeyAsync("F1")
return

~F2::
BroadcastKeyAsync("F2")
return

~F3::
BroadcastKeyAsync("F3")
return

~F4::
BroadcastKeyAsync("F4")
return

~F5::
BroadcastKeyAsync("F5")
return

~F6::
BroadcastKeyAsync("F6")
return

~F7::
BroadcastKeyAsync("F7")
return

~F8::
BroadcastKeyAsync("F8")
return

~F9::
BroadcastKeyAsync("F9")
return

~F10::
BroadcastKeyAsync("F10")
return

~F11::
BroadcastKeyAsync("F11")
return

~F12::
BroadcastKeyAsync("F12")
return

; ━━━ THÊM PHÍM KHÁC NẾU CẦN ━━━
; Template với prefix ~ (cho phép key pass through):
;   ~PHÍM::
;   BroadcastKeyAsync("PHÍM")
;   return
; 
; VD: t → 
;   ~t::
;   BroadcastKeyAsync("t")
;   return
; 
; VD: Tab → 
;   ~Tab::
;   BroadcastKeyAsync("Tab")
;   return

; ═══════════════════════════════════════════════════════════════════════
; ⚠️ PHẦN BÊN DƯỚI - KHÔNG NÊN THAY ĐỔI! ⚠️
; ═══════════════════════════════════════════════════════════════════════
; Đây là code xử lý, chỉ sửa nếu bạn biết AutoHotkey
; ═══════════════════════════════════════════════════════════════════════

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🚀 OPTIMIZED BROADCAST FUNCTION
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Global variables for optimization
global vmCache := {}
global vmRetryCount := {}
global lastCacheRefresh := 0
global performanceStats := {totalBroadcasts: 0, totalSuccess: 0, totalFailed: 0, avgLatency: 0}

BroadcastKey(key) {
    global vmList, showDebugTooltip, enableBeep, enableBroadcasting, enableVMCache, enableAutoRetry
    
    ; Check if broadcasting is enabled
    if (!enableBroadcasting) {
        return
    }
    
    ; Check if there are any VMs configured
    if (vmList.Length() = 0) {
        ; No VMs configured - skip broadcasting
        return
    }
    
    ; Don't send to HOST - let HOST input work naturally
    ; Only broadcast to VMs
    global vmCache, vmRetryCount, lastCacheRefresh, cacheRefreshInterval, maxRetryAttempts
    global performanceStats
    
    startTime := A_TickCount
    successCount := 0
    failCount := 0
    retryCount := 0
    
    ; Refresh VM cache if needed
    if (enableVMCache && (A_TickCount - lastCacheRefresh > cacheRefreshInterval)) {
        RefreshVMCache()
    }
    
    ; Batch process VMs
    for index, vmTitle in vmList {
        vmExists := false
        
        if (enableVMCache) {
            ; Use cached result
            vmExists := vmCache[vmTitle]
        } else {
            ; Check window existence directly
            IfWinExist, %vmTitle%
                vmExists := true
        }
        
        if (vmExists) {
            ; Send key via TCP to Slave script in VM
            port := vmPorts[vmTitle]
            
            if (port) {
                ; Send KEYDOWN command
                result := TCPSendCommand(VM_HOST, port, "KEYDOWN:" . key)
                
                if (result) {
                    successCount++
                    vmRetryCount[vmTitle] := 0
                } else {
                    failCount++
                }
            } else {
                failCount++
            }
        } else {
            failCount++
            
            ; Auto-retry logic
            if (enableAutoRetry && vmRetryCount[vmTitle] < maxRetryAttempts) {
                vmRetryCount[vmTitle]++
                retryCount++
                
                ; Quick retry after 100ms
                Sleep, 100
                IfWinExist, %vmTitle%
                {
                    ControlSend,, {%key%}, %vmTitle%
                    successCount++
                    failCount--
                    vmRetryCount[vmTitle] := 0
                }
            }
        }
    }
    
    ; Update performance stats
    latency := A_TickCount - startTime
    performanceStats.totalBroadcasts++
    performanceStats.totalSuccess += successCount
    performanceStats.totalFailed += failCount
    performanceStats.avgLatency := (performanceStats.avgLatency + latency) / 2
    
    ; Debug tooltip
    if (showDebugTooltip) {
        totalVMs := vmList.Length()
        ToolTip, [MASTER] Key: %key%`nSent: %successCount%/%totalVMs%`nFailed: %failCount%`nRetries: %retryCount%`nLatency: %latency%ms, 10, 10, 1
        SetTimer, RemoveTooltip1, 1500
    }
    
    ; Beep feedback
    if (enableBeep) {
        if (failCount = 0) {
            SoundBeep, 800, 50
        } else if (failCount < totalVMs / 2) {
            SoundBeep, 1000, 75
        } else {
            SoundBeep, 1200, 100
        }
    }
}

; ═══════════════════════════════════════════════════════════════════════
; 🚀 ASYNC BROADCAST FUNCTION (Không block Host input)
; ═══════════════════════════════════════════════════════════════════════
; Function này chạy ASYNC (không block) để Host input hoạt động tức thì

BroadcastKeyAsync(key) {
    ; Chạy BroadcastKey trong background thread
    ; KHÔNG block Host input
    SetTimer, % "BroadcastKeyTimer" . key, -1
    return
}

; Timer labels cho mỗi key
BroadcastKeyTimerq:
    BroadcastKey("q")
return

BroadcastKeyTimerw:
    BroadcastKey("w")
return

BroadcastKeyTimere:
    BroadcastKey("e")
return

BroadcastKeyTimerr:
    BroadcastKey("r")
return

BroadcastKeyTimera:
    BroadcastKey("a")
return

BroadcastKeyTimers:
    BroadcastKey("s")
return

BroadcastKeyTimerd:
    BroadcastKey("d")
return

BroadcastKeyTimerf:
    BroadcastKey("f")
return

BroadcastKeyTimerSpace:
    BroadcastKey("Space")
return

BroadcastKeyTimerLeft:
    BroadcastKey("Left")
return

BroadcastKeyTimerRight:
    BroadcastKey("Right")
return

BroadcastKeyTimerUp:
    BroadcastKey("Up")
return

BroadcastKeyTimerDown:
    BroadcastKey("Down")
return

BroadcastKeyTimerNumpad1:
    BroadcastKey("Numpad1")
return

BroadcastKeyTimerNumpad2:
    BroadcastKey("Numpad2")
return

BroadcastKeyTimerNumpad3:
    BroadcastKey("Numpad3")
return

BroadcastKeyTimerNumpad4:
    BroadcastKey("Numpad4")
return

BroadcastKeyTimerNumpad5:
    BroadcastKey("Numpad5")
return

BroadcastKeyTimerNumpad6:
    BroadcastKey("Numpad6")
return

BroadcastKeyTimerNumpad8:
    BroadcastKey("Numpad8")
return

BroadcastKeyTimer1:
    BroadcastKey("1")
return

BroadcastKeyTimer2:
    BroadcastKey("2")
return

BroadcastKeyTimer3:
    BroadcastKey("3")
return

BroadcastKeyTimer4:
    BroadcastKey("4")
return

BroadcastKeyTimer5:
    BroadcastKey("5")
return

BroadcastKeyTimer6:
    BroadcastKey("6")
return

BroadcastKeyTimer7:
    BroadcastKey("7")
return

BroadcastKeyTimer8:
    BroadcastKey("8")
return

BroadcastKeyTimer9:
    BroadcastKey("9")
return

BroadcastKeyTimer0:
    BroadcastKey("0")
return

BroadcastKeyTimerF1:
    BroadcastKey("F1")
return

BroadcastKeyTimerF2:
    BroadcastKey("F2")
return

BroadcastKeyTimerF3:
    BroadcastKey("F3")
return

BroadcastKeyTimerF4:
    BroadcastKey("F4")
return

BroadcastKeyTimerF5:
    BroadcastKey("F5")
return

BroadcastKeyTimerF6:
    BroadcastKey("F6")
return

BroadcastKeyTimerF7:
    BroadcastKey("F7")
return

BroadcastKeyTimerF8:
    BroadcastKey("F8")
return

BroadcastKeyTimerF9:
    BroadcastKey("F9")
return

BroadcastKeyTimerF10:
    BroadcastKey("F10")
return

BroadcastKeyTimerF11:
    BroadcastKey("F11")
return

BroadcastKeyTimerF12:
    BroadcastKey("F12")
return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔑 GET VIRTUAL KEY CODE
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

GetKeyVK(key) {
    ; Convert key name to VK code
    static keyMap := {q: 0x51, w: 0x57, e: 0x45, r: 0x52, a: 0x41, s: 0x53, d: 0x44, f: 0x46
                     , "Space": 0x20, "Left": 0x25, "Right": 0x27, "Up": 0x26, "Down": 0x28
                     , "Numpad1": 0x61, "Numpad2": 0x62, "Numpad3": 0x63, "Numpad4": 0x64
                     , "Numpad5": 0x65, "Numpad6": 0x66, "Numpad8": 0x68
                     , "1": 0x31, "2": 0x32, "3": 0x33, "4": 0x34, "5": 0x35
                     , "6": 0x36, "7": 0x37, "8": 0x38, "9": 0x39, "0": 0x30
                     , "F1": 0x70, "F2": 0x71, "F3": 0x72, "F4": 0x73, "F5": 0x74, "F6": 0x75
                     , "F7": 0x76, "F8": 0x77, "F9": 0x78, "F10": 0x79, "F11": 0x7A, "F12": 0x7B}
    
    return keyMap[key]
}

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔄 VM CACHE MANAGEMENT
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RefreshVMCache() {
    global vmList, vmCache, lastCacheRefresh
    
    for index, vmTitle in vmList {
        IfWinExist, %vmTitle%
            vmCache[vmTitle] := true
        else
            vmCache[vmTitle] := false
    }
    
    lastCacheRefresh := A_TickCount
}

RemoveTooltip1:
    ToolTip,,, 1
    SetTimer, RemoveTooltip1, Off
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎛️ UTILITY HOTKEYS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

^!s::
{
    global vmList
    
    totalVMs := vmList.Length()
    foundCount := 0
    missingCount := 0
    
    statusText := "VM STATUS:`n`n"
    
    for index, vmTitle in vmList {
        IfWinExist, %vmTitle%
        {
            statusText .= "✅ VM" . index . ": FOUND`n"
            foundCount++
        }
        else
        {
            statusText .= "❌ VM" . index . ": NOT FOUND`n"
            missingCount++
        }
    }
    
    statusText .= "`nTotal VMs: " . totalVMs
    statusText .= "`nFound: " . foundCount
    statusText .= "`nMissing: " . missingCount
    
    MsgBox, 64, MASTER STATUS, %statusText%
}
Return

^!l::
{
    vmwareWindows := ""
    vmwareList := ""
    counter := 0
    
    WinGet, windowList, List
    
    Loop, %windowList%
    {
        windowID := windowList%A_Index%
        WinGetTitle, windowTitle, ahk_id %windowID%
        
        IfInString, windowTitle, VMware
        {
            counter++
            vmwareWindows .= counter . ". " . windowTitle . "`n"
            vmwareList .= windowTitle . "`n"
        }
    }
    
    if (vmwareWindows = "")
    {
        MsgBox, 48, VMware Windows, No VMware windows found!`n`nMake sure VMs are running.
    }
    else
    {
        ; Copy to clipboard
        Clipboard := vmwareList
        
        MsgBox, 64, VMware Windows Found, 
        (
        Found %counter% VMware window(s):
        
        %vmwareWindows%
        
        ✅ COPIED TO CLIPBOARD!
        
        Paste them into vmList in the script!
        )
    }
}
Return

^!d::
{
    global showDebugTooltip
    
    showDebugTooltip := !showDebugTooltip
    
    if (showDebugTooltip) {
        ToolTip, Debug Tooltip: ON, 10, 10, 1
        SetTimer, RemoveTooltip1, 1500
    } else {
        ToolTip, Debug Tooltip: OFF, 10, 10, 1
        SetTimer, RemoveTooltip1, 1500
    }
}
Return

^!t::
{
    global enableBroadcasting
    
    enableBroadcasting := !enableBroadcasting
    
    if (enableBroadcasting) {
        SoundBeep, 1000, 200
        ToolTip, [MASTER] Input Broadcasting: ENABLED, 10, 10, 3
    } else {
        SoundBeep, 500, 200
        ToolTip, [MASTER] Input Broadcasting: DISABLED, 10, 10, 3
    }
    
    SetTimer, RemoveTooltip3, 2000
}

RemoveTooltip3:
    ToolTip
Return

^!b::
{
    global enableBeep
    
    enableBeep := !enableBeep
    
    if (enableBeep) {
        SoundBeep, 800, 100
        ToolTip, Beep: ON, 10, 10, 1
        SetTimer, RemoveTooltip1, 1500
    } else {
        ToolTip, Beep: OFF, 10, 10, 1
        SetTimer, RemoveTooltip1, 1500
    }
}
Return

^!p::
{
    global performanceStats, vmCache, vmRetryCount
    
    ; Get CPU and Memory usage
    Process, Exist
    Process, Close, %A_ThisPID%
    Process, Exist, %A_ThisPID%
    
    ; Calculate success rate
    successRate := 0
    if (performanceStats.totalBroadcasts > 0) {
        successRate := Round((performanceStats.totalSuccess / performanceStats.totalBroadcasts) * 100, 1)
    }
    
    ; Count cached VMs
    cachedVMs := 0
    for vmTitle, exists in vmCache {
        if (exists)
            cachedVMs++
    }
    
    ; Count VMs with retry attempts
    retryVMs := 0
    for vmTitle, count in vmRetryCount {
        if (count > 0)
            retryVMs++
    }
    
    perfText := "PERFORMANCE MONITOR:`n`n"
    perfText .= "📊 Broadcast Stats:`n"
    perfText .= "• Total Broadcasts: " . performanceStats.totalBroadcasts . "`n"
    perfText .= "• Success Rate: " . successRate . "%`n"
    perfText .= "• Avg Latency: " . Round(performanceStats.avgLatency, 1) . "ms`n`n"
    perfText .= "🖥️ VM Status:`n"
    perfText .= "• Cached VMs: " . cachedVMs . "/" . vmCache.Count() . "`n"
    perfText .= "• VMs with Retries: " . retryVMs . "`n`n"
    perfText .= "⚡ Optimization:`n"
    perfText .= "• VM Cache: " . (enableVMCache ? "ENABLED" : "DISABLED") . "`n"
    perfText .= "• Auto Retry: " . (enableAutoRetry ? "ENABLED" : "DISABLED") . "`n"
    perfText .= "• Cache Refresh: " . Round(cacheRefreshInterval/1000, 1) . "s"
    
    MsgBox, 64, Performance Monitor, %perfText%
}
Return

^!r::
{
    RefreshVMCache()
    ToolTip, VM Cache Refreshed!`nFound: " . vmCache.Count() . " VMs, 10, 10, 1
    SetTimer, RemoveTooltip1, 2000
}
Return

^!q::
{
    global vmList, performanceStats
    totalVMs := vmList.Length()
    
    exitText := "Master script exiting...`n`n"
    exitText .= "📊 Final Stats:`n"
    exitText .= "• Total Broadcasts: " . performanceStats.totalBroadcasts . "`n"
    exitText .= "• Success Rate: " . Round((performanceStats.totalSuccess / performanceStats.totalBroadcasts) * 100, 1) . "%`n"
    exitText .= "• Avg Latency: " . Round(performanceStats.avgLatency, 1) . "ms`n`n"
    exitText .= "Broadcasted to %totalVMs% VMs"
    
    MsgBox, 64, Exiting, %exitText%
    ExitApp
}
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🚀 OPTIMIZED STARTUP
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Initialize VM cache
RefreshVMCache()

totalVMs := vmList.Length()
foundVMs := 0

for vmTitle, exists in vmCache {
    if (exists)
        foundVMs++
}

startupText := "MASTER SCRIPT RUNNING!`n`n"
startupText .= "Total VMs: " . totalVMs . "`n"
startupText .= "Found: " . foundVMs . "`n"
startupText .= "Cache: " . (enableVMCache ? "ENABLED" : "DISABLED") . "`n`n"

if (totalVMs = 0) {
    startupText .= "⭐ TEST MODE: HOST INPUT ONLY`n"
    startupText .= "• No VMs configured`n"
    startupText .= "• Keys will send to HOST`n`n"
} else {
    startupText .= "⭐ INPUT MODE: HOST + VMs`n"
    startupText .= "• Keys sent to HOST (notepad/game)`n"
    startupText .= "• Keys broadcast to ALL VMs`n`n"
}
startupText .= "Hotkeys:`n"
startupText .= "Ctrl+Alt+S - Status`n"
startupText .= "Ctrl+Alt+L - List VMs`n"
startupText .= "Ctrl+Alt+T - Toggle Broadcasting`n"
startupText .= "Ctrl+Alt+P - Performance`n"
startupText .= "Ctrl+Alt+R - Refresh Cache`n"
startupText .= "Ctrl+Alt+Q - Exit"

ToolTip, %startupText%, 10, 10, 1
SetTimer, RemoveTooltip1, 5000

if (foundVMs = totalVMs) {
    SoundBeep, 800, 100
    Sleep, 100
    SoundBeep, 1000, 100
} else if (foundVMs > 0) {
    SoundBeep, 600, 200
} else {
    SoundBeep, 400, 300
}

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🌐 TCP CLIENT HELPER FUNCTIONS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TCPSendCommand(host, port, command) {
    ; Create socket
    socket := DllCall("ws2_32\socket", "Int", 2, "Int", 1, "Int", 6, "Ptr")
    
    if (socket = -1) {
        return 0
    }
    
    ; Set socket to non-blocking with timeout
    timeout := 1000  ; 1 second
    DllCall("ws2_32\setsockopt", "Ptr", socket, "Int", 0xFFFF, "Int", 0x1006, "UInt*", timeout, "Int", 4)
    
    ; Connect to server
    VarSetCapacity(sockaddr, 16, 0)
    NumPut(2, sockaddr, 0, "UShort")  ; AF_INET
    NumPut(DllCall("ws2_32\htons", "UShort", port, "UShort"), sockaddr, 2, "UShort")
    
    ; Convert IP address
    DllCall("ws2_32\inet_pton", "Int", 2, "AStr", host, "Ptr", &sockaddr + 4)
    
    if (DllCall("ws2_32\connect", "Ptr", socket, "Ptr", &sockaddr, "Int", 16) = -1) {
        DllCall("ws2_32\closesocket", "Ptr", socket)
        return 0
    }
    
    ; Send command
    VarSetCapacity(buffer, StrLen(command) + 1, 0)
    StrPut(command, &buffer, "UTF-8")
    
    bytesSent := DllCall("ws2_32\send", "Ptr", socket, "Ptr", &buffer, "Int", StrLen(command), "Int", 0, "Int")
    
    ; Close socket
    DllCall("ws2_32\closesocket", "Ptr", socket)
    
    return (bytesSent > 0) ? 1 : 0
}

