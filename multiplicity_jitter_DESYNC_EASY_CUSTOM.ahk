; ═══════════════════════════════════════════════════════════════════════
; 🎯 MULTIPLICITY JITTER WITH DESYNC - PHIÊN BẢN CỰC KỲ DỄ CUSTOM
; ═══════════════════════════════════════════════════════════════════════
; ⭐ TÍNH NĂNG MỚI: DESYNC DELAY ⭐
; Phá vỡ sự đồng bộ của Multiplicity giữa các VM!
; Mỗi VM sẽ phản hồi tại thời điểm khác nhau một cách ngẫu nhiên
; ═══════════════════════════════════════════════════════════════════════
; 🎮 ARROW KEYS: HARDWARE PASSTHROUGH (KHÔNG QUA AHK!)
; → Game MapleStory BLOCK hoàn toàn software input cho movement!
; → Arrow keys: Multiplicity → Game trực tiếp (hardware input)
; → Skill keys: AHK với desync (0-500ms) + jitter (30-80ms)
; ═══════════════════════════════════════════════════════════════════════
;
; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  🚀 CHẠY NGAY - KHÔNG CẦN CUSTOM! ⚡                                   ║
; ║                                                                       ║
; ║  ✅ ĐÃ CÓ SETTING MẶC ĐỊNH TỐI ƯU SẴN!                                ║
; ║                                                                       ║
; ║  Chỉ cần chạy: compile_EASY_CUSTOM_obfuscate.bat                     ║
; ║  Xong! Test file .exe luôn                                            ║
; ║                                                                       ║
; ║  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  ║
; ║                                                                       ║
; ║  📝 MUỐN CUSTOM? (OPTIONAL - Không bắt buộc!)                         ║
; ║                                                                       ║
; ║  1️⃣ Kéo xuống PHẦN 1 → Chọn mức độ training khác nếu muốn           ║
; ║     (Hiện tại: MỨC TRUNG BÌNH - Tốt cho 4-6 giờ/ngày)                ║
; ║                                                                       ║
; ║  2️⃣ Kéo xuống PHẦN 2 → Chọn template game khác nếu muốn             ║
; ║     (Hiện tại: TEMPLATE MAPLESTORY - Phù hợp hầu hết game)           ║
; ║                                                                       ║
; ║  3️⃣ Lưu file → Chạy compile_EASY_CUSTOM_obfuscate.bat lại           ║
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
; ║  📝 PHẦN 1: MỨC ĐỘ TRAINING (OPTIONAL - Đã có mặc định) ✏️            ║
; ║                                                                       ║
; ║  ⚡ SETTING MẶC ĐỊNH: MỨC TRUNG BÌNH (4-6 giờ/ngày)                   ║
; ║  💡 Nếu muốn đổi, bỏ ; ở mức khác, thêm ; vào mức hiện tại           ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┌─────────────────────────────────────────────────────────────────────┐
; │ 🎚️ CHỌN MỨC ĐỘ TRAINING (Bỏ ; ở 2 DÒNG bạn muốn dùng)              │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ CÁCH DÙNG: Bỏ dấu ; ở ĐẦU 2 DÒNG (MinDesync và MaxDesync)
; ⚠️ CHỈ BỎ ; Ở 1 MỨC ĐỘ, THÊM ; VÀO CÁC MỨC KHÁC!

; ━━━ MỨC NHẸ (1-2 giờ/ngày) - An toàn nhất ━━━
; global MinDesync := 0
; global MaxDesync := 300

; ━━━ MỨC TRUNG BÌNH (4-6 giờ/ngày) - Cân bằng (KHUYẾN NGHỊ! ⭐) ━━━
global MinDesync := 0
global MaxDesync := 500

; ━━━ MỨC NẶNG (8-10 giờ/ngày) - Mạo hiểm hơn ━━━
; global MinDesync := 100
; global MaxDesync := 800

; ━━━ MỨC CỰC NẶNG (12+ giờ/ngày) - Rất mạo hiểm ━━━
; global MinDesync := 200
; global MaxDesync := 1000

; ═══════════════════════════════════════════════════════════════════════
; ⚙️ CẤU HÌNH JITTER - ⚠️ KHÔNG NÊN THAY ĐỔI! ⚠️
; ═══════════════════════════════════════════════════════════════════════
; Phần này đã tối ưu, KHÔNG NÊN thay đổi trừ khi bạn biết rõ mình đang làm gì
; ═══════════════════════════════════════════════════════════════════════
global MinJitter := 30     ; Jitter tối thiểu (ms) - KHÔNG THAY ĐỔI
global MaxJitter := 80     ; Jitter tối đa (ms) - KHÔNG THAY ĐỔI
global UseGaussian := true ; Dùng phân phối Gaussian - KHÔNG THAY ĐỔI

; ┌─────────────────────────────────────────────────────────────────────┐
; │ ⏸️ MỨC ĐỘ PAUSE (OPTIONAL - Đã có mặc định VỪA PHẢI)               │
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
global ScriptEnabled := true  ; ⚠️ KHÔNG SỬA DÒNG NÀY! (Toggle control)

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  📝 PHẦN 2: KEY REMAP (OPTIONAL - Đã có mặc định) ✏️                  ║
; ║                                                                       ║
; ║  ⚡ SETTING MẶC ĐỊNH: TEMPLATE MAPLESTORY                             ║
; ║     Skill keys: Q→A, W→S, E→D, R→F, Space (desync+jitter)            ║
; ║     Arrow keys: KHÔNG có trong AHK (hardware passthrough!)           ║
; ║                                                                       ║
; ║  💡 Game BLOCK software input cho movement! Arrow = hardware only!    ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┌─────────────────────────────────────────────────────────────────────┐
; │ 🎮 CHỌN TEMPLATE GAME (Bỏ ; ở template bạn muốn dùng)               │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ CÁCH DÙNG: Bỏ dấu ; ở ĐẦU CÁC DÒNG của 1 template
; ⚠️ CHỈ BỎ ; Ở 1 TEMPLATE, THÊM ; VÀO CÁC TEMPLATE KHÁC!

global remap := {}  ; ⚠️ KHÔNG XÓA DÒNG NÀY!

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📋 TEMPLATE 1: MAPLESTORY - SKILL KEYS ONLY (KHUYẾN NGHỊ! ⭐)
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; ⚡ SKILL KEYS: Có desync+jitter (anti-detect)
; Phím skill: Q W E R → A S D F
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
; Phím nhảy (có desync+jitter)
remap["Space"] := "Space"
; ⚠️ ARROW KEYS: BỎ KHỎI AHK HOÀN TOÀN!
; → Game MapleStory BLOCK software input cho movement!
; → Chỉ chấp nhận hardware input từ Multiplicity!
; → Để Multiplicity broadcast trực tiếp (hardware-level)

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📋 TEMPLATE 2: KHÔNG REMAP - CHỈ DESYNC + JITTER CHO SKILL KEYS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; Bỏ ; nếu bạn KHÔNG muốn remap, CHỈ cần desync + jitter
; ; remap["q"] := "q"
; ; remap["w"] := "w"
; ; remap["e"] := "e"
; ; remap["r"] := "r"
; ; remap["Space"] := "Space"
; ⚠️ ARROW KEYS: KHÔNG THÊM VÀO! (Game block software input)

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📋 TEMPLATE 3: CUSTOM - TỰ CHỈNH SỬA
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; Bỏ ; và sửa theo ý bạn
; ; remap["q"] := "..."  ; ← Thay ... bằng phím bạn muốn
; ; remap["w"] := "..."
; ; remap["e"] := "..."
; ; remap["r"] := "..."

; ┌─────────────────────────────────────────────────────────────────────┐
; │ 📚 TEMPLATE COPY-PASTE (Copy dòng này khi cần thêm phím mới)        │
; └─────────────────────────────────────────────────────────────────────┘
; remap["PHÍM_NGUỒN"] := "PHÍM_ĐÍCH"

; ┌─────────────────────────────────────────────────────────────────────┐
; │ 💡 HƯỚNG DẪN CHI TIẾT                                                │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ THÊM PHÍM MỚI: Copy dòng template, sửa tên phím
;    VD: remap["t"] := "g"  → Ấn T sẽ gửi G
;
; ✅ XÓA PHÍM: Thêm ; ở đầu dòng
;    VD: ; remap["q"] := "a"  → Phím Q không còn remap
;
; ✅ SỬA PHÍM: Thay đổi phím đích
;    VD: remap["q"] := "z"  → Ấn Q sẽ gửi Z (thay vì A)
;
; ⚠️ CHÚ Ý:
; - Viết CHỮ THƯỜNG: "q" (đúng) không phải "Q" (sai)
; - Arrow keys: "Left", "Right", "Up", "Down" (viết HOA chữ cái đầu)
; - Space: "Space" (viết HOA chữ S)
; - Các phím đặc biệt: "Enter", "Tab", "Escape", "Backspace"

; ═══════════════════════════════════════════════════════════════════════
; ⚠️ PHẦN BÊN DƯỚI - KHÔNG NÊN THAY ĐỔI! ⚠️
; ═══════════════════════════════════════════════════════════════════════
; Đây là code xử lý, chỉ sửa nếu bạn biết AutoHotkey
; ═══════════════════════════════════════════════════════════════════════

; Tự động tạo hotkeys từ bảng remap
For sourceKey, targetKey in remap {
    Hotkey, $%sourceKey%, HandleKey
}

; Bắt đầu timer cho behavioral pause
SetTimer, CheckBehavioralPause, 1000
ScheduleNextPause()

Return

; ═══════════════════════════════════════════════════════════════════════
; 🎛️ TOGGLE SCRIPT ON/OFF
; ═══════════════════════════════════════════════════════════════════════

; Ctrl+Alt+T - Toggle script ON/OFF
^!t::
    global ScriptEnabled
    ScriptEnabled := !ScriptEnabled
    
    if (ScriptEnabled) {
        SoundBeep, 1000, 100
        ToolTip, SCRIPT ENABLED, 0, 0
    } else {
        SoundBeep, 500, 100
        ToolTip, SCRIPT DISABLED (Passthrough mode), 0, 0
    }
    
    SetTimer, RemoveToggleTooltip, 2000
Return

RemoveToggleTooltip:
    ToolTip
    SetTimer, RemoveToggleTooltip, Off
Return

; Xử lý phím
HandleKey:
    global ScriptEnabled, IsPaused
    
    ; Nếu script bị tắt, passthrough phím gốc
    if (!ScriptEnabled) {
        pressedKey := StrReplace(A_ThisHotkey, "$", "")
        SendInput, {%pressedKey%}
        return
    }
    
    ; Kiểm tra xem có đang pause không
    if (IsPaused) {
        return ; Block input khi đang pause
    }
    
    ; Lấy phím được ấn
    pressedKey := StrReplace(A_ThisHotkey, "$", "")
    
    ; Lấy phím đích từ bảng remap
    targetKey := remap[pressedKey]
    
    ; Áp dụng desync + jitter và gửi
    ApplyDesyncJitterAndSend(targetKey)
Return

; Hàm áp dụng desync + jitter
ApplyDesyncJitterAndSend(key) {
    global MinDesync, MaxDesync, MinJitter, MaxJitter, UseGaussian
    
    ; BƯỚC 1: DESYNC DELAY
    Random, desyncDelay, %MinDesync%, %MaxDesync%
    Sleep, %desyncDelay%
    
    ; BƯỚC 2: JITTER DELAY
    if (UseGaussian) {
        mean := (MinJitter + MaxJitter) / 2.0
        stdDev := (MaxJitter - MinJitter) / 6.0
        jitter := GaussianRandom(mean, stdDev, MinJitter, MaxJitter)
    } else {
        Random, jitter, %MinJitter%, %MaxJitter%
    }
    Sleep, %jitter%
    
    ; BƯỚC 3: GỬI PHÍM
    SendInput, {%key%}
}

; Hàm tạo số ngẫu nhiên Gaussian
GaussianRandom(mean, stdDev, min, max) {
    Random, u1, 0.0, 1.0
    Random, u2, 0.0, 1.0
    z := Sqrt(-2 * Ln(u1)) * Cos(2 * 3.14159265359 * u2)
    value := mean + z * stdDev
    if (value < min)
        value := min
    if (value > max)
        value := max
    return Round(value)
}

; Hệ thống behavioral pause
CheckBehavioralPause:
    if (A_TickCount >= NextPauseTime && !IsPaused) {
        StartBehavioralPause()
    }
Return

StartBehavioralPause() {
    global IsPaused, MinPauseDuration, MaxPauseDuration
    IsPaused := true
    Random, duration, %MinPauseDuration%, %MaxPauseDuration%
    SetTimer, EndBehavioralPause, %duration%
}

EndBehavioralPause:
    global IsPaused
    IsPaused := false
    SetTimer, EndBehavioralPause, Off
    ScheduleNextPause()
Return

ScheduleNextPause() {
    global NextPauseTime, MinPauseInterval, MaxPauseInterval
    Random, interval, %MinPauseInterval%, %MaxPauseInterval%
    NextPauseTime := A_TickCount + interval
}

