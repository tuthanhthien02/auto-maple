; ═══════════════════════════════════════════════════════════
; TEST ALL SEND METHODS - COMPREHENSIVE
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#InstallKeybdHook
SetKeyDelay, -1

MsgBox, 
(
TEST ALL SEND METHODS

Mở Notepad và test các phím:

1 = Send`, q
2 = Send`, {q}
3 = SendInput`, q
4 = SendInput`, {q}
5 = SendPlay`, q
6 = SendPlay`, {q}
7 = SendEvent`, q
8 = SendRaw`, q

Phím nào làm Q xuất hiện = method đó hoạt động!

Press ESC to exit.
)

1::
    ToolTip, Method 1: Send`, q
    Sleep, 300
    Send, q
    Sleep, 500
    ToolTip
    return

2::
    ToolTip, Method 2: Send`, {q}
    Sleep, 300
    Send, {q}
    Sleep, 500
    ToolTip
    return

3::
    ToolTip, Method 3: SendInput`, q
    Sleep, 300
    SendInput, q
    Sleep, 500
    ToolTip
    return

4::
    ToolTip, Method 4: SendInput`, {q}
    Sleep, 300
    SendInput, {q}
    Sleep, 500
    ToolTip
    return

5::
    ToolTip, Method 5: SendPlay`, q
    Sleep, 300
    SendPlay, q
    Sleep, 500
    ToolTip
    return

6::
    ToolTip, Method 6: SendPlay`, {q}
    Sleep, 300
    SendPlay, {q}
    Sleep, 500
    ToolTip
    return

7::
    ToolTip, Method 7: SendEvent`, q
    Sleep, 300
    SendEvent, q
    Sleep, 500
    ToolTip
    return

8::
    ToolTip, Method 8: SendRaw`, q
    Sleep, 300
    SendRaw, q
    Sleep, 500
    ToolTip
    return

Esc::
    ExitApp


