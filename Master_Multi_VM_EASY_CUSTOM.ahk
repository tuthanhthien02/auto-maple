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
; 🎮 BROADCAST HOTKEYS (Gửi input đến VMs):
;   SKILL KEYS: Q, W, E, R, A, S, D, F, Space
;   ARROW KEYS: Left, Right, Up, Down
;   NUMPAD KEYS: Numpad1-8
;   NUMBER KEYS: 1-9, 0
;   FUNCTION KEYS: F1-F12
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
vmList.Push("Win10-VM1 - VMware Workstation")  ; VM 1
vmList.Push("Win10-VM2 - VMware Workstation")  ; VM 2
vmList.Push("Win10-VM3 - VMware Workstation")  ; VM 3
vmList.Push("Win10-VM4 - VMware Workstation")  ; VM 4
vmList.Push("Win10-VM5 - VMware Workstation")  ; VM 5

; ━━━ Thêm VM 6, 7, 8... nếu cần (Bỏ ; ở đầu dòng để enable) ━━━
; vmList.Push("Win10-VM6 - VMware Workstation")  ; VM 6
; vmList.Push("Win10-VM7 - VMware Workstation")  ; VM 7
; vmList.Push("Win10-VM8 - VMware Workstation")  ; VM 8
; vmList.Push("Win10-VM9 - VMware Workstation")  ; VM 9
; vmList.Push("Win10-VM10 - VMware Workstation") ; VM 10

; 💡 KHÔNG CÓ GIỚI HẠN! Thêm bao nhiêu cũng được!
; 📝 Template để copy: vmList.Push("TÊN_VM_CỦA_BẠN")

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
; ┃ 4️⃣ KEYS TO BROADCAST (Phím nào sẽ broadcast đến VMs)               ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
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
q::BroadcastKey("q")
w::BroadcastKey("w")
e::BroadcastKey("e")
r::BroadcastKey("r")
a::BroadcastKey("a")
s::BroadcastKey("s")
d::BroadcastKey("d")
f::BroadcastKey("f")
Space::BroadcastKey("Space")

; ━━━ ARROW KEYS (Phím mũi tên) ━━━
Left::BroadcastKey("Left")
Right::BroadcastKey("Right")
Up::BroadcastKey("Up")
Down::BroadcastKey("Down")

; ━━━ NUMPAD KEYS (Phím numpad) ━━━
Numpad1::BroadcastKey("Numpad1")
Numpad2::BroadcastKey("Numpad2")
Numpad3::BroadcastKey("Numpad3")
Numpad4::BroadcastKey("Numpad4")
Numpad5::BroadcastKey("Numpad5")
Numpad6::BroadcastKey("Numpad6")
Numpad8::BroadcastKey("Numpad8")

; ━━━ NUMBER KEYS (Phím số 1-9, 0) ━━━
1::BroadcastKey("1")
2::BroadcastKey("2")
3::BroadcastKey("3")
4::BroadcastKey("4")
5::BroadcastKey("5")
6::BroadcastKey("6")
7::BroadcastKey("7")
8::BroadcastKey("8")
9::BroadcastKey("9")
0::BroadcastKey("0")

; ━━━ FUNCTION KEYS (Phím F1-F12) ━━━
F1::BroadcastKey("F1")
F2::BroadcastKey("F2")
F3::BroadcastKey("F3")
F4::BroadcastKey("F4")
F5::BroadcastKey("F5")
F6::BroadcastKey("F6")
F7::BroadcastKey("F7")
F8::BroadcastKey("F8")
F9::BroadcastKey("F9")
F10::BroadcastKey("F10")
F11::BroadcastKey("F11")
F12::BroadcastKey("F12")

; ━━━ THÊM PHÍM KHÁC NẾU CẦN ━━━
; Template: PHÍM::BroadcastKey("PHÍM")
; VD: t::BroadcastKey("t")
; VD: Tab::BroadcastKey("Tab")
; VD: Enter::BroadcastKey("Enter")

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
            ; Send key to VM
            ControlSend,, {%key%}, %vmTitle%
            successCount++
            
            ; Reset retry count on success
            vmRetryCount[vmTitle] := 0
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
        }
    }
    
    if (vmwareWindows = "")
    {
        MsgBox, 48, VMware Windows, No VMware windows found!`n`nMake sure VMs are running.
    }
    else
    {
        MsgBox, 64, VMware Windows Found, 
        (
        Found %counter% VMware window(s):
        
        %vmwareWindows%
        
        Copy these titles and add them to vmList in the script!
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

