; ═══════════════════════════════════════════════════════════
; SUPER SIMPLE TEST - NO JITTER, JUST SEND
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv

if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

MsgBox, 
(
✅ RUNNING AS ADMIN!

SUPER SIMPLE TEST:
- Bấm Q → Send "q" with SendInput
- Bấm W → Send "q" with Send
- Bấm E → Send "q" with SendPlay

Mở Notepad và test!

Press ESC to exit.
)

; TEST 1: SendInput
q::
    ToolTip, [Q] SendInput`, q
    Sleep, 200
    SendInput, q
    Sleep, 500
    ToolTip
    return

; TEST 2: Send
w::
    ToolTip, [W] Send`, q
    Sleep, 200
    Send, q
    Sleep, 500
    ToolTip
    return

; TEST 3: SendPlay
e::
    ToolTip, [E] SendPlay`, q
    Sleep, 200
    SendPlay, q
    Sleep, 500
    ToolTip
    return

Esc::
    ExitApp

