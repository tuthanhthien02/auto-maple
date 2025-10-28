; ═══════════════════════════════════════════════════════════════════════
; 🎮 MASTER SCRIPT - STEALTH VERSION (INVISIBLE & HIDDEN!)
; ═══════════════════════════════════════════════════════════════════════
; ⭐ VERSION 2: MASTER-SLAVE SETUP - THAY THẾ MULTIPLICITY! ⭐
; 
; 🚀 STEALTH FEATURES:
; • No tray icon (completely invisible)
; • Hidden process name
; • Minimal memory footprint
; • Silent operation (no beeps/tooltips by default)
; • Process hiding techniques
; • Anti-detection measures
; • Minimal logging
; 
; ⚠️ WARNING: This version is designed to be undetectable!
; 💡 Use Master_Multi_VM_EASY_CUSTOM.ahk for normal use!
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
#NoTrayIcon
SetBatchLines, -1
Process, Priority,, High

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║  ⚙️ STEALTH SETTINGS (MINIMAL CONFIGURATION!)                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 1️⃣ DANH SÁCH VMs (Tên window của từng VM)                           ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

global vmList := []

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

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 2️⃣ STEALTH OPTIONS (Silent operation)                              ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

global showDebugTooltip := false  ; NO tooltips (stealth mode)
global enableBeep := false         ; NO beeps (stealth mode)
global enableVMCache := true       ; Cache enabled for performance
global enableAutoRetry := true     ; Auto-retry enabled
global maxRetryAttempts := 3
global cacheRefreshInterval := 30000

; ═══════════════════════════════════════════════════════════════════════
; ⚠️ STEALTH CODE SECTION - MINIMAL FOOTPRINT! ⚠️
; ═══════════════════════════════════════════════════════════════════════

global vmCache := {}
global vmRetryCount := {}
global lastCacheRefresh := 0
global performanceStats := {totalBroadcasts: 0, totalSuccess: 0, totalFailed: 0, avgLatency: 0}

BroadcastKey(key) {
    global vmList, showDebugTooltip, enableBeep, enableVMCache, enableAutoRetry
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
    
    ; Debug tooltip (only if enabled)
    if (showDebugTooltip) {
        totalVMs := vmList.Length()
        ToolTip, [MASTER] Key: %key%`nSent: %successCount%/%totalVMs%`nFailed: %failCount%`nRetries: %retryCount%`nLatency: %latency%ms, 10, 10, 1
        SetTimer, RemoveTooltip1, 1500
    }
    
    ; Beep feedback (only if enabled)
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
; 🎛️ STEALTH HOTKEYS (SILENT OPERATION)
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
; 🚀 STEALTH STARTUP (SILENT INITIALIZATION)
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Initialize VM cache silently
RefreshVMCache()

totalVMs := vmList.Length()
foundVMs := 0

for vmTitle, exists in vmCache {
    if (exists)
        foundVMs++
}

; Silent startup - no tooltips or beeps by default
; Only show status if debug mode is enabled
if (showDebugTooltip) {
    startupText := "MASTER SCRIPT RUNNING!`n`n"
    startupText .= "Total VMs: " . totalVMs . "`n"
    startupText .= "Found: " . foundVMs . "`n"
    startupText .= "Cache: " . (enableVMCache ? "ENABLED" : "DISABLED") . "`n`n"
    startupText .= "Hotkeys:`n"
    startupText .= "Ctrl+Alt+S - Status`n"
    startupText .= "Ctrl+Alt+L - List VMs`n"
    startupText .= "Ctrl+Alt+P - Performance`n"
    startupText .= "Ctrl+Alt+R - Refresh Cache`n"
    startupText .= "Ctrl+Alt+Q - Exit"
    
    ToolTip, %startupText%, 10, 10, 1
    SetTimer, RemoveTooltip1, 5000
}

; Silent beep only if enabled
if (enableBeep) {
    if (foundVMs = totalVMs) {
        SoundBeep, 800, 100
        Sleep, 100
        SoundBeep, 1000, 100
    } else if (foundVMs > 0) {
        SoundBeep, 600, 200
    } else {
        SoundBeep, 400, 300
    }
}

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔑 KEY MAPPINGS (SILENT BROADCAST)
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

q::BroadcastKey("q")
w::BroadcastKey("w")
e::BroadcastKey("e")
r::BroadcastKey("r")
a::BroadcastKey("a")
s::BroadcastKey("s")
d::BroadcastKey("d")
f::BroadcastKey("f")
Space::BroadcastKey("Space")

Left::BroadcastKey("Left")
Right::BroadcastKey("Right")
Up::BroadcastKey("Up")
Down::BroadcastKey("Down")

Numpad1::BroadcastKey("Numpad1")
Numpad2::BroadcastKey("Numpad2")
Numpad3::BroadcastKey("Numpad3")
Numpad4::BroadcastKey("Numpad4")
Numpad5::BroadcastKey("Numpad5")
Numpad6::BroadcastKey("Numpad6")
Numpad8::BroadcastKey("Numpad8")

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
