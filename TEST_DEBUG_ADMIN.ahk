; ═══════════════════════════════════════════════════════════
; DEBUG TEST - WITH TOOLTIPS TO SEE EVERYTHING!
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount

; 🔒 AUTO-ELEVATE TO ADMIN
if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

; ════ CẤU HÌNH ════
global MinJitter := 500
global MaxJitter := 1000

MsgBox, 
(
✅ DEBUG TEST - RUNNING AS ADMIN!

Test với nhiều methods:
- Q = SendInput`, q
- W = Send`, q  
- E = SendInput`, {q}
- R = Send`, {q}

Bấm từng phím trong Notepad và xem tooltips!

Press ESC to exit.
)

; ════ TEST SENDPUT, q ════
q::
    ToolTip, [Q] Step 1: Key pressed!, 100, 100
    Sleep, 100
    
    Random, jitter, %MinJitter%, %MaxJitter%
    ToolTip, [Q] Step 2: Sleeping %jitter%ms..., 100, 100
    Sleep, %jitter%
    
    ToolTip, [Q] Step 3: Sending "SendInput`, q"..., 100, 100
    Sleep, 100
    SendInput, q
    
    ToolTip, [Q] Step 4: DONE! Q should appear now!, 100, 100
    Sleep, 1000
    ToolTip
    return

; ════ TEST SEND, q ════
w::
    ToolTip, [W] Step 1: Key pressed!, 100, 100
    Sleep, 100
    
    Random, jitter, %MinJitter%, %MaxJitter%
    ToolTip, [W] Step 2: Sleeping %jitter%ms..., 100, 100
    Sleep, %jitter%
    
    ToolTip, [W] Step 3: Sending "Send`, q"..., 100, 100
    Sleep, 100
    Send, q
    
    ToolTip, [W] Step 4: DONE! Q should appear now!, 100, 100
    Sleep, 1000
    ToolTip
    return

; ════ TEST SENDINPUT, {q} ════
e::
    ToolTip, [E] Step 1: Key pressed!, 100, 100
    Sleep, 100
    
    Random, jitter, %MinJitter%, %MaxJitter%
    ToolTip, [E] Step 2: Sleeping %jitter%ms..., 100, 100
    Sleep, %jitter%
    
    ToolTip, [E] Step 3: Sending "SendInput`, {q}"..., 100, 100
    Sleep, 100
    SendInput, {q}
    
    ToolTip, [E] Step 4: DONE! Q should appear now!, 100, 100
    Sleep, 1000
    ToolTip
    return

; ════ TEST SEND, {q} ════
r::
    ToolTip, [R] Step 1: Key pressed!, 100, 100
    Sleep, 100
    
    Random, jitter, %MinJitter%, %MaxJitter%
    ToolTip, [R] Step 2: Sleeping %jitter%ms..., 100, 100
    Sleep, %jitter%
    
    ToolTip, [R] Step 3: Sending "Send`, {q}"..., 100, 100
    Sleep, 100
    Send, {q}
    
    ToolTip, [R] Step 4: DONE! Q should appear now!, 100, 100
    Sleep, 1000
    ToolTip
    return

; ════ EXIT ════
Esc::
    MsgBox, Exiting debug test...
    ExitApp
    return

