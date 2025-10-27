; ═══════════════════════════════════════════════════════════════════════
; 🎯 MULTIPLICITY JITTER WITH DESYNC - PHIÊN BẢN CỰC KỲ DỄ CUSTOM
; ═══════════════════════════════════════════════════════════════════════
; ⭐ TÍNH NĂNG MỚI: DESYNC DELAY ⭐
; Phá vỡ sự đồng bộ của Multiplicity giữa các VM!
; Mỗi VM sẽ phản hồi tại thời điểm khác nhau một cách ngẫu nhiên
; ═══════════════════════════════════════════════════════════════════════
; 🎮 SENDINPUT MODE: GIỐNG AUTO-MAPLE BOT 100%!
; → SendMode Input = user32.SendInput API (CHÍNH XÁC như Python bot!)
; → Arrow keys: Left/Right/Up/Down (instant, 0ms delay!) ✅ WORK!
; → Skill keys: SendInput + desync (0-500ms) + jitter (30-80ms)
; → HOLD keys: down → sleep 40-70ms → up (giống auto-maple!)
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
; ╚═══════════════════════════════════════════════════════════════════════╝
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ 📋 TÓM TẮT SETTING MẶC ĐỊNH (Đang dùng gì?) ⭐                       │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ MỨC ĐỘ TRAINING: Trung bình (0-500ms desync) - 4-6 giờ/ngày
; ✅ BEHAVIORAL PAUSE: Vừa phải (3-5 phút pause 1 lần, 0.8-2.5s)
; ✅ ARROW KEYS JITTER: TẮT (0ms delay - Movement mượt!)
; ✅ KEY REMAP: MapleStory (Q/W/E/R→A/S/D/F, Numpad→Arrow)
; ✅ HOTKEYS: Ctrl+Alt+T (toggle on/off)
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ 🎯 MUỐN CUSTOM? (Chỉ 3 BƯỚC - Cực dễ!)                              │
; └─────────────────────────────────────────────────────────────────────┘
; 
; ━━━ BƯỚC 1: Chọn setting muốn thay đổi (kéo xuống section tương ứng) ━━━
; 
;   📌 PHẦN 1 (Line 46): Mức độ training (training nhiều/ít?)
;      → BỎ ; ở mức muốn dùng (1-2 giờ/4-6 giờ/8-10 giờ...)
;      → THÊM ; vào mức hiện tại
; 
;   📌 PHẦN 1.5 (Line 120): Arrow keys có jitter không? (mượt hay giật?)
;      → BỎ ; ở dòng "global ArrowKeysUseJitter := true/false"
;      → THÊM ; vào dòng còn lại
; 
;   📌 PHẦN 2 (Line 145): Template game (MapleStory/Khác?)
;      → BỎ ; ở tất cả dòng remap["..."] của template muốn dùng
;      → THÊM ; vào tất cả dòng remap["..."] của template cũ
; 
; ━━━ BƯỚC 2: Lưu file (Ctrl+S) ━━━
; 
; ━━━ BƯỚC 3: Chạy lại compile_EASY_CUSTOM_obfuscate.bat ━━━
; 
; 🎉 XONG! File .exe mới đã có setting mới!
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ ⌨️ HOTKEYS (Phím tắt khi script đang chạy)                          │
; └─────────────────────────────────────────────────────────────────────┘
; 🔸 Ctrl+Alt+T: Bật/Tắt script (beep 1 tiếng)
;    → Bật: Beep cao (1000Hz)
;    → Tắt: Beep thấp (500Hz)
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ ❓ TROUBLESHOOTING (Gặp vấn đề?)                                    │
; └─────────────────────────────────────────────────────────────────────┘
; 
; ❌ VẤN ĐỀ: Arrow keys không di chuyển trong game
;    ✅ GIẢI PHÁP: Dùng NUMPAD (1/2/3/5) thay vì arrow keys
;    → Numpad đã remap sẵn sang arrow keys trong Template 1
; 
; ❌ VẤN ĐỀ: Di chuyển bị giật
;    ✅ GIẢI PHÁP: ArrowKeysUseJitter đang = true, đổi sang false
;    → Xem hướng dẫn ở PHẦN 1.5 (Line 155)
; 
; ❌ VẤN ĐỀ: Phím không hoạt động sau khi custom
;    ✅ GIẢI PHÁP: Kiểm tra lại:
;    → Có thêm ; vào template cũ chưa?
;    → Có bỏ ; ở ĐÚNG chỗ (đầu dòng remap["..."]) chưa?
;    → Đã compile lại chưa? (compile_EASY_CUSTOM_obfuscate.bat)
; 
; ❌ VẤN ĐỀ: Compile bị lỗi
;    ✅ GIẢI PHÁP: Kiểm tra lại:
;    → Có XÓA dòng "global remap := {}" không? (KHÔNG ĐƯỢC XÓA!)
;    → Có sửa code ở phần "KHÔNG NÊN THAY ĐỔI" không?
;    → Thử revert lại (Ctrl+Z) và làm lại từ đầu
; 
; ❌ VẤN ĐỀ: Không biết script có đang chạy không
;    ✅ GIẢI PHÁP: Nhấn Ctrl+Alt+T → Nghe beep → Đang chạy!
;
;
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
SetBatchLines, -1
Process, Priority,, High
SendMode Input  ; ← Dùng user32.SendInput GIỐNG auto-maple bot!

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
; 
; 📝 VÍ DỤ: Đổi từ MỨC TRUNG BÌNH → MỨC NẶNG (8-10 giờ/ngày)
;    BƯỚC 1: THÊM ; vào 2 dòng 95-96 (Mức trung bình)
;    BƯỚC 2: BỎ ; ở 2 dòng 99-100 (Mức nặng)
;    BƯỚC 3: Lưu → Compile → Xong!

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
; ║  📝 PHẦN 1.5: ARROW KEYS JITTER (Mượt hay Giật?)                     ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ ⚡ ARROW KEYS JITTER SETTING (Dễ dàng bật/tắt!)                     │
; └─────────────────────────────────────────────────────────────────────┘
; 
; 📊 SO SÁNH 2 OPTIONS:
; ┌──────────────────┬─────────────────┬──────────────────────┐
; │   OPTION         │   DELAY         │   KHI NÀO DÙNG       │
; ├──────────────────┼─────────────────┼──────────────────────┤
; │ 1. KHÔNG JITTER  │ 0ms (instant)   │ Movement mượt ⭐      │
; │ 2. CÓ JITTER     │ 30-580ms random │ Anti-detect tốt hơn  │
; └──────────────────┴─────────────────┴──────────────────────┘
; 
; 💡 ĐỀ XUẤT: Dùng OPTION 1 (false) cho tới khi bị detect, rồi đổi OPTION 2 (true)
; 
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; ✅ CÁCH ĐỔI TỪ OPTION 1 → OPTION 2 (3 BƯỚC - Cực dễ!):
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 
; BƯỚC 1: THÊM ; vào đầu dòng 164 (Option 1 hiện tại)
;    TRƯỚC: global ArrowKeysUseJitter := false
;    SAU:   ; global ArrowKeysUseJitter := false
; 
; BƯỚC 2: BỎ ; ở đầu dòng 168 (Option 2)
;    TRƯỚC: ; global ArrowKeysUseJitter := true
;    SAU:   global ArrowKeysUseJitter := true
; 
; BƯỚC 3: Lưu file → Compile lại → Xong!
; 
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; ━━━ OPTION 1: KHÔNG JITTER (Movement mượt - KHUYẾN NGHỊ! ⭐) ━━━
global ArrowKeysUseJitter := false  ; Arrow keys = instant (0ms delay)
; ✅ Ưu điểm: Di chuyển mượt mà, không giật
; ⚠️ Nhược điểm: Có thể bị detect (instant response)

; ━━━ OPTION 2: CÓ JITTER (Anti-detect tốt hơn, nhưng giật!) ━━━
; global ArrowKeysUseJitter := true   ; Arrow keys = có desync+jitter
; ✅ Ưu điểm: Anti-detect tốt hơn (random timing)
; ⚠️ Nhược điểm: Di chuyển hơi giật (delay 30-580ms)

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  📝 PHẦN 2: KEY REMAP (OPTIONAL - Đã có mặc định) ✏️                  ║
; ║                                                                       ║
; ║  ⚡ SETTING MẶC ĐỊNH: NUMPAD MOVEMENT                                 ║
; ║     Skill keys: Q→A, W→S, E→D, R→F, Space (desync+jitter)            ║
; ║     Movement: Numpad1→Left, 2→Down, 3→Right, 5→Up (instant!)        ║
; ║                                                                       ║
; ║  💡 Dùng NUMPAD để di chuyển thay vì arrow keys! 🎮                   ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┌─────────────────────────────────────────────────────────────────────┐
; │ 🎮 CHỌN TEMPLATE GAME (Bỏ ; ở template bạn muốn dùng)               │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ CÁCH DÙNG: Bỏ dấu ; ở ĐẦU CÁC DÒNG của 1 template
; ⚠️ CHỈ BỎ ; Ở 1 TEMPLATE, THÊM ; VÀO CÁC TEMPLATE KHÁC!
; 
; 📝 VÍ DỤ: Đổi từ TEMPLATE 1 → TEMPLATE 2 (Không remap)
;    BƯỚC 1: THÊM ; vào TẤT CẢ dòng remap["..."] của Template 1 (dòng 199-214)
;    BƯỚC 2: BỎ ; ở TẤT CẢ dòng remap["..."] của Template 2 (dòng 221-229)
;    BƯỚC 3: Lưu → Compile → Xong!

global remap := {}  ; ⚠️ KHÔNG XÓA DÒNG NÀY!

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📋 TEMPLATE 1: MAPLESTORY - NUMPAD TO ARROW (TEST! ⭐)
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; ⚡ SKILL KEYS: Có desync+jitter (anti-detect)
; Phím skill: Q W E R → A S D F
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
; Phím nhảy (có desync+jitter)
remap["Space"] := "Space"

; ⚡ ARROW KEYS (Numpad1/2/3/5 → Left/Down/Right/Up)
; → Jitter: Tùy thuộc ArrowKeysUseJitter setting (line 126)
; → Nếu ArrowKeysUseJitter = false → instant (0ms, mượt!)
; → Nếu ArrowKeysUseJitter = true → có desync+jitter (giật!)
remap["Numpad1"] := "Left"   ; Numpad1 → Left
remap["Numpad2"] := "Down"   ; Numpad2 → Down
remap["Numpad3"] := "Right"  ; Numpad3 → Right
remap["Numpad5"] := "Up"     ; Numpad5 → Up

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📋 TEMPLATE 2: KHÔNG REMAP - CHỈ DESYNC + JITTER CHO SKILL KEYS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; Bỏ ; nếu bạn KHÔNG muốn remap, CHỈ cần desync + jitter
; ; remap["q"] := "q"
; ; remap["w"] := "w"
; ; remap["e"] := "e"
; ; remap["r"] := "r"
; ; remap["Space"] := "Space"
; ; remap["Left"] := "Left"
; ; remap["Right"] := "Right"
; ; remap["Up"] := "Up"
; ; remap["Down"] := "Down"

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
    global ScriptEnabled, IsPaused, ArrowKeysUseJitter
    
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
    
    ; ⚡ CHECK ARROW KEYS (Numpad hoặc Arrow keys)
    isArrowKey := (pressedKey = "Numpad1" || pressedKey = "Numpad2" || pressedKey = "Numpad3" || pressedKey = "Numpad5" || pressedKey = "Left" || pressedKey = "Right" || pressedKey = "Up" || pressedKey = "Down")
    
    ; ⚡ ARROW KEYS: Check setting
    if (isArrowKey && !ArrowKeysUseJitter) {
        ; INSTANT: Không jitter (mượt mà!)
        SendInput, {%targetKey%}
        return
    }
    
    ; ⚡ SKILL KEYS hoặc ARROW KEYS VỚI JITTER: Áp dụng desync + jitter
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
    
    ; BƯỚC 3: GỬI PHÍM (HOLD như auto-maple bot!)
    ; Key down
    SendInput, {%key% down}
    ; Hold time: 40-70ms (giống auto-maple: 0.05s * (0.8-1.2))
    Random, holdTime, 40, 70
    Sleep, %holdTime%
    ; Key up
    SendInput, {%key% up}
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

