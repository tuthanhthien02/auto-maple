; ═══════════════════════════════════════════════════════════
; QUICK TEST - JITTER CỰC LỚN ĐỂ DỄ THẤY!
; ═══════════════════════════════════════════════════════════
; Test với delay 500-1000ms để dễ nhận biết!
; AUTO-ELEVATE TO ADMIN RIGHTS!
; ═══════════════════════════════════════════════════════════

#SingleInstance Force
#NoEnv
SetWorkingDir %A_ScriptDir%
Random, Seed, A_TickCount

; ════════════════════════════════════════════════════════════
; 🔒 AUTO-ELEVATE TO ADMIN (if not already)
; ════════════════════════════════════════════════════════════
if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

; ════ CẤU HÌNH TEST - DELAY CỰC LỚN ════
global MinJitter := 500   ; 500ms = 0.5 giây
global MaxJitter := 1000  ; 1000ms = 1 giây

MsgBox, 
(
✅ RUNNING AS ADMINISTRATOR!

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
    
    ; Send Q (using SendInput - works with admin!)
    SendInput, q
    return

; ════ EXIT HOTKEY ════
^+q::
    MsgBox, Thoát script test!
    ExitApp
    return


