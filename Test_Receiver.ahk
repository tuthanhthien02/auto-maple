; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🧪 TEST RECEIVER SCRIPT - Chạy trong VM
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; MỤC ĐÍCH: Nhận input từ Master script và hiển thị tooltip
; 
; HƯỚNG DẪN:
; 1. Copy file này vào VM
; 2. Chạy script này TRONG VM
; 3. Chạy Master_Test.ahk trên HOST
; 4. Ấn Q/W/E trên HOST
; 5. Kiểm tra VM có hiện tooltip "VM RECEIVED..." không
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#NoEnv
#SingleInstance Force
SetBatchLines, -1

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📊 STATISTICS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

global totalReceived := 0
global lastKey := "None"
global lastTime := ""

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎮 RECEIVE HOTKEYS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Receive Q
q::
{
    global totalReceived, lastKey, lastTime
    
    totalReceived++
    lastKey := "Q"
    lastTime := A_Hour ":" A_Min ":" A_Sec
    
    ; Show BIG tooltip
    ToolTip, ✅ VM RECEIVED Q!`n`nTotal Received: %totalReceived%`nLast Key: %lastKey%`nTime: %lastTime%, 100, 100, 1
    SetTimer, RemoveTooltip1, 3000
    
    ; Audio feedback
    SoundBeep, 1000, 150
    
    ; Optional: Send to game (for actual testing)
    ; SendInput, a
}
Return

; Receive W
w::
{
    global totalReceived, lastKey, lastTime
    
    totalReceived++
    lastKey := "W"
    lastTime := A_Hour ":" A_Min ":" A_Sec
    
    ToolTip, ✅ VM RECEIVED W!`n`nTotal Received: %totalReceived%`nLast Key: %lastKey%`nTime: %lastTime%, 100, 100, 1
    SetTimer, RemoveTooltip1, 3000
    SoundBeep, 1100, 150
}
Return

; Receive E
e::
{
    global totalReceived, lastKey, lastTime
    
    totalReceived++
    lastKey := "E"
    lastTime := A_Hour ":" A_Min ":" A_Sec
    
    ToolTip, ✅ VM RECEIVED E!`n`nTotal Received: %totalReceived%`nLast Key: %lastKey%`nTime: %lastTime%, 100, 100, 1
    SetTimer, RemoveTooltip1, 3000
    SoundBeep, 1200, 150
}
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🎛️ UTILITY HOTKEYS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Ctrl+Alt+S - Show Statistics
^!s::
{
    global totalReceived, lastKey, lastTime
    
    MsgBox, 64, RECEIVER STATISTICS, 
    (
    Total Keys Received: %totalReceived%
    Last Key: %lastKey%
    Last Time: %lastTime%
    
    Listening for: Q, W, E
    
    Utility:
    • Ctrl+Alt+S = Show stats
    • Ctrl+Alt+R = Reset stats
    • Ctrl+Alt+Q = Exit
    )
}
Return

; Ctrl+Alt+R - Reset Statistics
^!r::
{
    global totalReceived, lastKey, lastTime
    
    totalReceived := 0
    lastKey := "None"
    lastTime := ""
    
    ToolTip, 🔄 STATISTICS RESET!, 100, 100, 1
    SetTimer, RemoveTooltip1, 2000
    SoundBeep, 800, 200
}
Return

; Ctrl+Alt+Q - Exit
^!q::
{
    global totalReceived
    
    MsgBox, 64, Exiting, Receiver exiting...`n`nTotal keys received: %totalReceived%
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

ToolTip, TEST RECEIVER RUNNING!`nWaiting for input from Master...`nListening: Q, W, E`nCtrl+Alt+S for stats, 100, 100, 1
SetTimer, RemoveTooltip1, 5000
SoundBeep, 600, 200

