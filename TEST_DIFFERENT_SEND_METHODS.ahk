; ═══════════════════════════════════════════════════════════
; TEST DIFFERENT SEND METHODS
; ═══════════════════════════════════════════════════════════

#SingleInstance Force

MsgBox, 
(
TEST DIFFERENT SEND METHODS

Bấm các phím khác nhau để test:

Q = Send, q
W = Send, {q}
E = SendInput, q
R = SendPlay, q

Mở Notepad và test!
Phím nào làm Q xuất hiện = phím đó hoạt động!

Press ESC to exit.
)

q::
    ToolTip, Method 1: Send`, q
    Sleep, 500
    Send, q
    ToolTip
    return

w::
    ToolTip, Method 2: Send`, {q}
    Sleep, 500
    Send, {q}
    ToolTip
    return

e::
    ToolTip, Method 3: SendInput`, q
    Sleep, 500
    SendInput, q
    ToolTip
    return

r::
    ToolTip, Method 4: SendPlay`, q
    Sleep, 500
    SendPlay, q
    ToolTip
    return

Esc::
    ExitApp

