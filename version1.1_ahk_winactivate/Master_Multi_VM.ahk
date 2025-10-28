; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎮 MASTER SCRIPT - MULTIPLE VMs BROADCAST
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; MỤC ĐÍCH: Broadcast input từ HOST đến TẤT CẢ VMs
; 
; HƯỚNG DẪN:
; 1. Tìm window titles của TẤT CẢ VMs
; 2. Sửa phần SETTINGS bên dưới
; 3. Chạy multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk trong MỖI VM
; 4. Chạy script này trên HOST
; 5. Ấn phím → Tất cả VMs nhận → Mỗi VM apply desync riêng!
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#NoEnv
#SingleInstance Force
SetBatchLines, -1
Process, Priority,, High

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; ⚙️ SETTINGS - SỬA PHẦN NÀY!
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Danh sách window titles của VMs
; Cách tìm: Mở VM → Alt+Tab → Xem tên window
; Hoặc: Chạy script này → Ấn Ctrl+Alt+L

global vmList := []

; ━━━ THÊM VMs CỦA BẠN VÀO ĐÂY! ━━━
; Ví dụ cho 5 VMs:
vmList.Push("Win10-VM1 - VMware Workstation")  ; VM 1
vmList.Push("Win10-VM2 - VMware Workstation")  ; VM 2
vmList.Push("Win10-VM3 - VMware Workstation")  ; VM 3
vmList.Push("Win10-VM4 - VMware Workstation")  ; VM 4
vmList.Push("Win10-VM5 - VMware Workstation")  ; VM 5

; Thêm VM 6, 7, 8... nếu cần:
; vmList.Push("Win10-VM6 - VMware Workstation")
; vmList.Push("Win10-VM7 - VMware Workstation")
; vmList.Push("Win10-VM8 - VMware Workstation")
; vmList.Push("Win10-VM9 - VMware Workstation")
; vmList.Push("Win10-VM10 - VMware Workstation")

; KHÔNG CÓ GIỚI HẠN! Thêm bao nhiêu cũng được!

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔧 OPTIONS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Hiện debug tooltip khi broadcast? (true/false)
global showDebugTooltip := true

; Beep khi broadcast? (true/false)
global enableBeep := true

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎮 KEY REMAPPING - KEYS TO BROADCAST
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Skill keys
q::BroadcastKey("q")
w::BroadcastKey("w")
e::BroadcastKey("e")
r::BroadcastKey("r")
a::BroadcastKey("a")
s::BroadcastKey("s")
d::BroadcastKey("d")
f::BroadcastKey("f")
Space::BroadcastKey("Space")

; Arrow keys
Left::BroadcastKey("Left")
Right::BroadcastKey("Right")
Up::BroadcastKey("Up")
Down::BroadcastKey("Down")

; Numpad keys (for movement)
Numpad1::BroadcastKey("Numpad1")
Numpad2::BroadcastKey("Numpad2")
Numpad3::BroadcastKey("Numpad3")
Numpad4::BroadcastKey("Numpad4")
Numpad5::BroadcastKey("Numpad5")
Numpad6::BroadcastKey("Numpad6")
Numpad8::BroadcastKey("Numpad8")

; Number keys (1-9, 0)
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

; Function keys (F1-F12)
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

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔧 BROADCAST FUNCTION
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BroadcastKey(key) {
    global vmList, showDebugTooltip, enableBeep
    
    ; Count successful sends
    successCount := 0
    failCount := 0
    
    ; Broadcast to ALL VMs
    for index, vmTitle in vmList {
        IfWinExist, %vmTitle%
        {
            ; Send to this VM
            ControlSend,, {%key%}, %vmTitle%
            successCount++
        }
        else
        {
            ; VM not found
            failCount++
        }
    }
    
    ; Show debug info
    if (showDebugTooltip) {
        totalVMs := vmList.Length()
        ToolTip, [MASTER] Broadcasted: %key%`nSent: %successCount%/%totalVMs%`nFailed: %failCount%, 10, 10, 1
        SetTimer, RemoveTooltip1, 1000
    }
    
    ; Audio feedback
    if (enableBeep) {
        if (failCount = 0) {
            ; All success - happy beep
            SoundBeep, 800, 50
        } else {
            ; Some failed - warning beep
            SoundBeep, 1200, 100
        }
    }
}

RemoveTooltip1:
    ToolTip,,, 1
    SetTimer, RemoveTooltip1, Off
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎛️ UTILITY HOTKEYS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Ctrl+Alt+S - Check Status
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

; Ctrl+Alt+L - List All VMware Windows
^!l::
{
    vmwareWindows := ""
    counter := 0
    
    ; Enumerate all windows
    WinGet, windowList, List
    
    Loop, %windowList%
    {
        windowID := windowList%A_Index%
        WinGetTitle, windowTitle, ahk_id %windowID%
        
        ; Check if window title contains "VMware"
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

; Ctrl+Alt+D - Toggle Debug Tooltip
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

; Ctrl+Alt+B - Toggle Beep
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

; Ctrl+Alt+Q - Exit
^!q::
{
    global vmList
    totalVMs := vmList.Length()
    
    MsgBox, 64, Exiting, Master script exiting...`n`nBroadcasted to %totalVMs% VMs
    ExitApp
}
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🚀 STARTUP MESSAGE
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Count VMs on startup
totalVMs := vmList.Length()
foundVMs := 0

for index, vmTitle in vmList {
    IfWinExist, %vmTitle%
    {
        foundVMs++
    }
}

; Show startup message
ToolTip, MASTER SCRIPT RUNNING!`n`nTotal VMs: %totalVMs%`nFound: %foundVMs%`n`nHotkeys:`nCtrl+Alt+S - Status`nCtrl+Alt+L - List VMs`nCtrl+Alt+Q - Exit, 10, 10, 1
SetTimer, RemoveTooltip1, 5000

; Startup beep
if (foundVMs = totalVMs) {
    ; All VMs found - happy beep
    SoundBeep, 800, 100
    Sleep, 100
    SoundBeep, 1000, 100
} else {
    ; Some VMs missing - warning beep
    SoundBeep, 600, 200
}

