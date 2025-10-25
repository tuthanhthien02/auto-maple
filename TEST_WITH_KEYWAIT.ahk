; ═══════════════════════════════════════════════════════════
; TEST: Use KeyWait before sending (Block same key)
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetKeyDelay, 10, 10

if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

MsgBox, 
(
✅ RUNNING AS ADMIN!

TEST với KeyWait + SetKeyDelay:

Try blocking Q và sending Q lại
Nhưng dùng KeyWait để chờ Q được release!

Bấm Q trong Notepad → Xem Q có xuất hiện không

Press ESC to exit.
)

q::
    ToolTip, [Q] Step 1: Key pressed
    Sleep, 100
    
    ToolTip, [Q] Step 2: Waiting for key release...
    KeyWait, q           ; Wait for Q to be released
    Sleep, 100
    
    ToolTip, [Q] Step 3: Key released! Sending Q...
    Sleep, 100
    Send, q              ; Try Send
    
    ToolTip, [Q] Step 4: DONE!
    Sleep, 1000
    ToolTip
    return

w::
    ToolTip, [W] Step 1: Key pressed
    Sleep, 100
    
    ToolTip, [W] Step 2: Waiting for key release...
    KeyWait, w
    Sleep, 100
    
    ToolTip, [W] Step 3: Key released! Sending Q...
    Sleep, 100
    SendInput, q         ; Try SendInput
    
    ToolTip, [W] Step 4: DONE!
    Sleep, 1000
    ToolTip
    return

Esc::
    ExitApp

