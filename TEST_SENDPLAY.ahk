; ═══════════════════════════════════════════════════════════
; TEST SENDPLAY - Most Compatible Method
; ═══════════════════════════════════════════════════════════

#SingleInstance Force

MsgBox, 
(
TEST SENDPLAY METHOD

SendPlay is the MOST COMPATIBLE method.
It simulates keys at driver level.

Test in Notepad:
Press Q → Should see Q after 1 second

Press ESC to exit.
)

q::
    ToolTip, SendPlay sending Q in 1s...
    Sleep, 1000
    SendPlay, q
    ToolTip, Done!
    Sleep, 500
    ToolTip
    return

Esc::
    ExitApp

