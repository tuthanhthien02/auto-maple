; ═══════════════════════════════════════════════════════════
; DEBUG SCRIPT - CHECK IF SCRIPT IS INTERCEPTING KEYS
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%

MsgBox, 
(
DEBUG SCRIPT RUNNING!

Khi bạn bấm Q:
- Script sẽ hiện popup "Q detected!"
- Popup sẽ tự đóng sau 1 giây
- Nếu thấy popup → Script đang intercept được Q ✅
- Nếu KHÔNG thấy popup → Script KHÔNG intercept được Q ❌

Hãy thử bấm Q ngay bây giờ!

Press CTRL+SHIFT+Q to exit script.
)

; Counter
global QCount := 0

q::
    QCount++
    
    ; Show tooltip instead of MsgBox
    ToolTip, Q DETECTED! (Count: %QCount%)
    
    ; Auto-hide tooltip after 1 second
    SetTimer, RemoveToolTip, 1000
    
    ; Block Q completely (no Send)
    return

RemoveToolTip:
    SetTimer, RemoveToolTip, Off
    ToolTip
    return

^+q::
    MsgBox, Total Q presses: %QCount%
    ExitApp
    return

