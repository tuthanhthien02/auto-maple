; ═══════════════════════════════════════════════════════════
; TEST: BLOCK KEY A, SEND KEY Q (Different keys!)
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

TEST LOGIC: Block KEY A → Send KEY Q

Test trong Notepad:
- Bấm A → Sẽ send "q" thay vì "a"
- Bấm S → Sẽ send "q" thay vì "s"
- Bấm D → Sẽ send "q" thay vì "d"
- Bấm F → Sẽ send "q" thay vì "f"

4 methods:
  A = SendInput`, q
  S = Send`, q
  D = SendInput`, {q}
  F = Send`, {q}

Press ESC to exit.
)

; Block A, Send Q with SendInput, q
a::
    ToolTip, [A blocked] Sending Q with SendInput`, q
    Sleep, 200
    SendInput, q
    Sleep, 500
    ToolTip
    return

; Block S, Send Q with Send, q
s::
    ToolTip, [S blocked] Sending Q with Send`, q
    Sleep, 200
    Send, q
    Sleep, 500
    ToolTip
    return

; Block D, Send Q with SendInput, {q}
d::
    ToolTip, [D blocked] Sending Q with SendInput`, {q}
    Sleep, 200
    SendInput, {q}
    Sleep, 500
    ToolTip
    return

; Block F, Send Q with Send, {q}
f::
    ToolTip, [F blocked] Sending Q with Send`, {q}
    Sleep, 200
    Send, {q}
    Sleep, 500
    ToolTip
    return

Esc::
    ExitApp

