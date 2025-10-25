; ═══════════════════════════════════════════════════════════
; QUICK TEST - JITTER CỰC LỚN ĐỂ DỄ THẤY!
; ═══════════════════════════════════════════════════════════
; Test với delay 500-1000ms để dễ nhận biết!
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount

; ════ CẤU HÌNH TEST - DELAY CỰC LỚN ════
global MinJitter := 500   ; 500ms = 0.5 giây
global MaxJitter := 1000  ; 1000ms = 1 giây

MsgBox, 
(
🧪 TEST JITTER SCRIPT - CỰC DỄ THẤY!

Delay: 500-1000ms (0.5-1 giây)

HƯỚNG DẪN:
1. Mở Notepad
2. Bấm Q nhiều lần nhanh nhanh
3. Sẽ thấy delay RÕ RÀNG giữa mỗi lần Q xuất hiện!

Nếu thấy delay → Script hoạt động! ✅
Nếu KHÔNG thấy delay → Script lỗi! ❌

Press CTRL+SHIFT+Q to exit.
)

; ════ CHỈ INTERCEPT Q ĐỂ TEST ════
q::
    ; Delay cực lớn
    Random, jitter, %MinJitter%, %MaxJitter%
    Sleep, %jitter%
    
    ; Send Q (using SendInput for reliability)
    SendInput, q
    return

; ════ EXIT HOTKEY ════
^+q::
    MsgBox, Thoát script test!
    ExitApp
    return

