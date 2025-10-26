; ═══════════════════════════════════════════════════════════════════════
; 🎯 AUTO PAUSE ONLY - SCRIPT ĐƠN GIẢN
; ═══════════════════════════════════════════════════════════════════════
; ⭐ CHỈ CÓ AUTO PAUSE - Không có remap, desync, jitter
; Tự động pause ngẫu nhiên để giả lập hành vi người thật
; ═══════════════════════════════════════════════════════════════════════
;
; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  🚀 CHẠY NGAY - ĐÃ CÓ SETTING MẶC ĐỊNH! ⚡                            ║
; ║                                                                       ║
; ║  ✅ SETTING MẶC ĐỊNH: PAUSE VỪA PHẢI (3-5 phút)                       ║
; ║                                                                       ║
; ║  Chỉ cần chạy: compile_auto_pause_obfuscate.bat                      ║
; ║  Xong! Test file .exe luôn                                            ║
; ║                                                                       ║
; ║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
; ║                                                                       ║
; ║  📝 MUỐN CUSTOM? (OPTIONAL)                                           ║
; ║     Kéo xuống phần "CẤU HÌNH PAUSE" để thay đổi                      ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝
;
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
SetBatchLines, -1
Process, Priority,, High
#Persistent

; ═══════════════════════════════════════════════════════════════════════
; 🔒 STEALTH MODE - KHÔNG CÓ TRAY ICON
; ═══════════════════════════════════════════════════════════════════════
; Hotkeys:
;   Ctrl+Alt+S → Show status (xem next pause khi nào)
;   Ctrl+Alt+Q → Quit script
; ═══════════════════════════════════════════════════════════════════════

; Ẩn tray icon hoàn toàn
Menu, Tray, NoIcon

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  ⚙️ CẤU HÌNH PAUSE (OPTIONAL - Đã có mặc định VỪA PHẢI)              ║
; ║                                                                       ║
; ║  ⚡ SETTING MẶC ĐỊNH: PAUSE VỪA PHẢI (3-5 phút)                       ║
; ║  💡 Nếu muốn đổi, bỏ ; ở mức khác, thêm ; vào mức hiện tại           ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┌─────────────────────────────────────────────────────────────────────┐
; │ ⏸️ CHỌN MỨC ĐỘ PAUSE (Bỏ ; ở 4 DÒNG bạn muốn dùng)                 │
; └─────────────────────────────────────────────────────────────────────┘
; ⚡ SETTING MẶC ĐỊNH: PAUSE VỪA PHẢI (3-5 phút, pause 0.8-2.5 giây)
; ✅ CÁCH ĐỔI: Bỏ dấu ; ở ĐẦU 4 DÒNG của mức khác, thêm ; vào mức hiện tại
; ⚠️ CHỈ BỎ ; Ở 1 MỨC ĐỘ!

; ━━━ PAUSE THƯỜNG XUYÊN (Pause nhiều, an toàn) ━━━
; global MinPauseInterval := 120000
; global MaxPauseInterval := 180000
; global MinPauseDuration := 1000
; global MaxPauseDuration := 3000

; ━━━ PAUSE VỪA PHẢI (Cân bằng - KHUYẾN NGHỊ! ⭐) ━━━
global MinPauseInterval := 8000
global MaxPauseInterval := 8000
global MinPauseDuration := 800
global MaxPauseDuration := 2500

; ━━━ QUICK TEST MODE (Pause mỗi 10-20 giây để test - ĐỂ TEST!) ━━━
; global MinPauseInterval := 10000
; global MaxPauseInterval := 20000
; global MinPauseDuration := 2000
; global MaxPauseDuration := 4000

; ━━━ PAUSE ÍT (Pause ít, rủi ro cao hơn) ━━━
; global MinPauseInterval := 300000
; global MaxPauseInterval := 600000
; global MinPauseDuration := 500
; global MaxPauseDuration := 2000

; ━━━ KHÔNG PAUSE (Rất rủi ro - KHÔNG KHUYẾN NGHỊ!) ━━━
; global MinPauseInterval := 999999999
; global MaxPauseInterval := 999999999
; global MinPauseDuration := 1
; global MaxPauseDuration := 1

global IsPaused := false  ; ⚠️ KHÔNG SỬA DÒNG NÀY!

; ═══════════════════════════════════════════════════════════════════════
; ⚠️ PHẦN BÊN DƯỚI - KHÔNG NÊN THAY ĐỔI! ⚠️
; ═══════════════════════════════════════════════════════════════════════
; Đây là code xử lý, chỉ sửa nếu bạn biết AutoHotkey
; ═══════════════════════════════════════════════════════════════════════

; Start timer for behavioral pause
SetTimer, CheckBehavioralPause, 1000
ScheduleNextPause()

; Startup notification
ToolTip, AUTO PAUSE STARTED (Stealth Mode), 0, 0
SetTimer, RemoveStartupTooltip, 3000

Return

RemoveStartupTooltip:
    ToolTip
    SetTimer, RemoveStartupTooltip, Off
Return

; ═══════════════════════════════════════════════════════════════════════
; ⌨️ HOTKEYS
; ═══════════════════════════════════════════════════════════════════════

; Ctrl+Alt+S - Show Status
^!s::
    global NextPauseTime
    timeLeft := (NextPauseTime - A_TickCount) / 1000
    if (timeLeft < 0)
        timeLeft := 0
    
    minutes := Floor(timeLeft / 60)
    seconds := Floor(Mod(timeLeft, 60))
    
    ToolTip, RUNNING | Next pause in: %minutes%m %seconds%s, 0, 0
    SetTimer, RemoveStatusTooltip, 2000
Return

RemoveStatusTooltip:
    ToolTip
    SetTimer, RemoveStatusTooltip, Off
Return

; Ctrl+Alt+Q - Quit Script
^!q::
    ToolTip, EXITING..., 0, 0
    Sleep, 500
    ExitApp
Return

; ═══════════════════════════════════════════════════════════════════════
; ⏸️ HỆ THỐNG BEHAVIORAL PAUSE
; ═══════════════════════════════════════════════════════════════════════

CheckBehavioralPause:
    if (A_TickCount >= NextPauseTime && !IsPaused) {
        StartBehavioralPause()
    }
Return

StartBehavioralPause() {
    global IsPaused, MinPauseDuration, MaxPauseDuration
    IsPaused := true
    
    ; BLOCK ALL INPUT
    BlockInput, On
    
    ; Show tooltip during pause
    Random, duration, %MinPauseDuration%, %MaxPauseDuration%
    ToolTip, BLOCKED! PAUSE: %duration%ms, 0, 0
    
    SetTimer, EndBehavioralPause, %duration%
}

EndBehavioralPause:
    global IsPaused
    IsPaused := false
    
    ; UNBLOCK INPUT
    BlockInput, Off
    
    ToolTip  ; Hide tooltip
    SetTimer, EndBehavioralPause, Off
    ScheduleNextPause()
Return

ScheduleNextPause() {
    global NextPauseTime, MinPauseInterval, MaxPauseInterval
    Random, interval, %MinPauseInterval%, %MaxPauseInterval%
    NextPauseTime := A_TickCount + interval
}

; ═══════════════════════════════════════════════════════════════════════
; 💡 THÔNG TIN SCRIPT
; ═══════════════════════════════════════════════════════════════════════
; Script này chỉ tạo pause ngẫu nhiên, KHÔNG can thiệp vào phím bấm
; Mục đích: Tạo hành vi giống người thật khi training
; ═══════════════════════════════════════════════════════════════════════

