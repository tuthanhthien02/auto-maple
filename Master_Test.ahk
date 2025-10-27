; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🧪 MASTER TEST SCRIPT - Chạy trên HOST
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; MỤC ĐÍCH: Test xem ControlSend từ HOST đến VM có hoạt động không
; 
; HƯỚNG DẪN:
; 1. Mở VM của bạn
; 2. Tìm window title: Alt+Tab và xem tên window VM
; 3. SỬA biến "vmWindowTitle" bên dưới
; 4. Chạy Test_Receiver.ahk trong VM
; 5. Chạy script này trên HOST
; 6. Ấn Q hoặc W trên HOST
; 7. Kiểm tra VM có hiện tooltip "VM RECEIVED..." không
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#NoEnv
#SingleInstance Force
SetBatchLines, -1

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; ⚙️ SETTINGS - SỬA PHẦN NÀY!
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Tên window của VM (PHẢI SỬA!)
; Ví dụ:
; - "Windows 10 x64 - VMware Workstation"
; - "Win10-VM1 - VMware Workstation"
; - "Ubuntu - VMware Workstation"
global vmWindowTitle := "Windows 10 x64 - VMware Workstation"  ; ← SỬA TÊN NÀY!

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎮 TEST HOTKEYS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Test key Q
q::
{
    global vmWindowTitle
    
    ; Check if VM window exists
    IfWinExist, %vmWindowTitle%
    {
        ; Send Q to VM
        ControlSend,, q, %vmWindowTitle%
        
        ; Show confirmation on HOST
        ToolTip, [HOST] Sent Q to VM, 10, 10, 1
        SetTimer, RemoveTooltip1, 2000
        
        ; Beep for audio feedback
        SoundBeep, 500, 100
    }
    else
    {
        ; VM window not found!
        ToolTip, [ERROR] VM Window Not Found!`nWindow Title: %vmWindowTitle%, 10, 10, 1
        SetTimer, RemoveTooltip1, 3000
        SoundBeep, 1000, 300
    }
}
Return

; Test key W
w::
{
    global vmWindowTitle
    
    IfWinExist, %vmWindowTitle%
    {
        ControlSend,, w, %vmWindowTitle%
        ToolTip, [HOST] Sent W to VM, 10, 10, 1
        SetTimer, RemoveTooltip1, 2000
        SoundBeep, 600, 100
    }
    else
    {
        ToolTip, [ERROR] VM Window Not Found!, 10, 10, 1
        SetTimer, RemoveTooltip1, 3000
        SoundBeep, 1000, 300
    }
}
Return

; Test key E
e::
{
    global vmWindowTitle
    
    IfWinExist, %vmWindowTitle%
    {
        ControlSend,, e, %vmWindowTitle%
        ToolTip, [HOST] Sent E to VM, 10, 10, 1
        SetTimer, RemoveTooltip1, 2000
        SoundBeep, 700, 100
    }
    else
    {
        ToolTip, [ERROR] VM Window Not Found!, 10, 10, 1
        SetTimer, RemoveTooltip1, 3000
        SoundBeep, 1000, 300
    }
}
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎛️ UTILITY HOTKEYS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Ctrl+Alt+S - Check Status
^!s::
{
    global vmWindowTitle
    
    IfWinExist, %vmWindowTitle%
    {
        status := "VM FOUND!"
        color := "Green"
    }
    else
    {
        status := "VM NOT FOUND!"
        color := "Red"
    }
    
    MsgBox, 64, MASTER TEST STATUS, 
    (
    Window Title: %vmWindowTitle%
    
    Status: %status%
    
    Test Keys:
    • Press Q, W, or E to test
    
    Utility:
    • Ctrl+Alt+S = Check status
    • Ctrl+Alt+L = List all VMware windows
    • Ctrl+Alt+Q = Exit
    )
}
Return

; Ctrl+Alt+L - List all VMware windows
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
        MsgBox, 48, VMware Windows, No VMware windows found!`n`nMake sure VM is running.
    }
    else
    {
        MsgBox, 64, VMware Windows Found, 
        (
        Found %counter% VMware window(s):
        
        %vmwareWindows%
        
        Copy the exact title and paste it into the script!
        )
    }
}
Return

; Ctrl+Alt+Q - Exit
^!q::
{
    MsgBox, 64, Exiting, Master Test Script exiting...
    ExitApp
}
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔧 HELPER FUNCTIONS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

RemoveTooltip1:
    ToolTip,,, 1
    SetTimer, RemoveTooltip1, Off
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🚀 STARTUP MESSAGE
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

ToolTip, MASTER TEST SCRIPT RUNNING!`nPress Q/W/E to test`nCtrl+Alt+S for status`nCtrl+Alt+L to list VMs, 10, 10, 1
SetTimer, RemoveTooltip1, 5000
SoundBeep, 800, 200

