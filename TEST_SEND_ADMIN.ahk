; ═══════════════════════════════════════════════════════════
; TEST WITH ADMIN CHECK
; ═══════════════════════════════════════════════════════════

#SingleInstance Force

; Check if running as admin
if not A_IsAdmin
{
    MsgBox, 
    (
    ⚠️ NOT RUNNING AS ADMIN!
    
    This might be why Q is not appearing!
    
    Solution:
    1. Right-click this script
    2. Run as Administrator
    3. Test again
    
    Click OK to try running anyway...
    )
}
else
{
    MsgBox, ✅ Running as Administrator!
}

MsgBox, Test in Notepad. Press Q.

q::
    ToolTip, Sending Q...
    Sleep, 500
    SendInput, q
    ToolTip
    return

Esc::
    ExitApp


