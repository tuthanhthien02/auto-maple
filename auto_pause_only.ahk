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
global MinPauseInterval := 180000
global MaxPauseInterval := 300000
global MinPauseDuration := 800
global MaxPauseDuration := 2500

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

; Bắt đầu timer cho behavioral pause
SetTimer, CheckBehavioralPause, 1000
ScheduleNextPause()

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
    
    ; Hiển thị tooltip khi pause
    Random, duration, %MinPauseDuration%, %MaxPauseDuration%
    ToolTip, ⏸️ PAUSE: %duration%ms, 0, 0
    
    SetTimer, EndBehavioralPause, %duration%
}

EndBehavioralPause:
    global IsPaused
    IsPaused := false
    ToolTip  ; Ẩn tooltip
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

