; ═══════════════════════════════════════════════════════════════════════
; 🥷 MULTIPLICITY JITTER WITH DESYNC - STEALTH MODE
; ═══════════════════════════════════════════════════════════════════════
; ⭐ TÍNH NĂNG MỚI: DESYNC DELAY ⭐
; Phá vỡ sự đồng bộ của Multiplicity giữa các VM!
; Mỗi VM sẽ phản hồi tại thời điểm khác nhau một cách ngẫu nhiên
; ═══════════════════════════════════════════════════════════════════════
; 🥷 STEALTH MODE FEATURES:
; → NO TRAY ICON (Không hiện icon ở system tray)
; → NO VISIBLE WINDOW (Chạy ngầm hoàn toàn)
; → HOTKEY CHECK STATUS: Ctrl+Alt+S (kiểm tra script đang chạy)
; → HOTKEY EXIT: Ctrl+Alt+Q (thoát script)
; → STARTUP CONFIRMATION: Beep + Tooltip 1.5s khi script bắt đầu
; ═══════════════════════════════════════════════════════════════════════
; 🎮 SENDINPUT MODE: GIỐNG AUTO-MAPLE BOT 100%!
; → SendMode Input = user32.SendInput API (CHÍNH XÁC như Python bot!)
; → TẤT CẢ KEYS đều HOLD khi giữ phím! ✅
;   • Arrow keys: HOLD (down → wait → up) - Character di chuyển liên tục
;   • Skill keys: HOLD (down → wait → up) - Giữ skill key (charge/hold skills)
; → 🧪 TEST MODE: Có thể tắt delay/jitter để test (0ms instant response)
; ═══════════════════════════════════════════════════════════════════════
;
; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  🚀 CHẠY NGAY - KHÔNG CẦN CUSTOM! ⚡                                   ║
; ║                                                                       ║
; ║  ✅ ĐÃ CÓ SETTING MẶC ĐỊNH TỐI ƯU SẴN!                                ║
; ║                                                                       ║
; ║  Chỉ cần chạy: compile_STEALTH_obfuscate.bat                         ║
; ║  Xong! Test file .exe luôn                                            ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ 📋 TÓM TẮT SETTING MẶC ĐỊNH (Đang dùng gì?) ⭐                       │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ STEALTH MODE: BẬT (Không tray icon, chạy ngầm hoàn toàn)
; ✅ MỨC ĐỘ TRAINING: Trung bình (0-500ms desync) - 4-6 giờ/ngày
; ✅ BEHAVIORAL PAUSE: Vừa phải (3-5 phút pause 1 lần, 0.8-2.5s)
; ✅ ARROW KEYS JITTER: BẬT (30-580ms delay - Anti-detect tốt!)
; ✅ KEY REMAP: MapleStory (Q/W/E/R→A/S/D/F, Numpad→Arrow)
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ ⌨️ HOTKEYS (Phím tắt khi script đang chạy) - QUAN TRỌNG!            │
; └─────────────────────────────────────────────────────────────────────┘
; 🔸 Ctrl+Alt+T: Bật/Tắt script (beep + tooltip)
;    → Bật: Beep cao (1000Hz) + tooltip "ENABLED"
;    → Tắt: Beep thấp (500Hz) + tooltip "DISABLED"
;
; 🔸 Ctrl+Alt+S: Check status (kiểm tra script có đang chạy không)
;    → Hiện tooltip: Script status + Next pause time
;    → Tooltip tự tắt sau 3 giây
;
; 🔸 Ctrl+Alt+Q: Exit script (thoát hoàn toàn)
;    → Beep 2 tiếng → Script dừng
;    → PHẢI dùng hotkey này để thoát (vì không có tray icon!)
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ 🎯 MUỐN CUSTOM? (Chỉ 3 BƯỚC - Cực dễ!)                              │
; └─────────────────────────────────────────────────────────────────────┘
; 
; ━━━ BƯỚC 1: Kéo xuống Line 120 - TẤT CẢ SETTINGS Ở ĐÓ! ━━━
; 
; 🔍 Tìm phần "⚙️ ⚙️ ⚙️  TẤT CẢ SETTINGS Ở ĐÂY" (Line 120-330)
; 
; Có 4 SETTINGS ở gần nhau:
;   1️⃣ Mức độ training (Line 132): 1-2 giờ? 4-6 giờ? 8-10 giờ?
;   2️⃣ Arrow keys jitter (Line 207): Movement mượt hay giật?
;   3️⃣ Behavioral pause (Line 173): Pause nhiều hay ít?
;   4️⃣ Key remap (Line 246): Template MapleStory hay game khác?
; 
; ━━━ BƯỚC 2: Lưu file (Ctrl+S) ━━━
; 
; ━━━ BƯỚC 3: Chạy lại compile_STEALTH_obfuscate.bat ━━━
; 
; 🎉 XONG! File .exe mới đã có setting mới!
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ ❓ TROUBLESHOOTING (Gặp vấn đề?)                                    │
; └─────────────────────────────────────────────────────────────────────┘
; 
; ❌ VẤN ĐỀ: Không biết script có đang chạy không
;    ✅ GIẢI PHÁP: Nhấn Ctrl+Alt+S → Xem tooltip status
;    → Nếu hiện tooltip → Đang chạy!
;    → Nếu không hiện gì → Script chưa chạy hoặc đã tắt
;
; ❌ VẤN ĐỀ: Không thể thoát script (không có tray icon)
;    ✅ GIẢI PHÁP: Nhấn Ctrl+Alt+Q → Beep 2 tiếng → Script thoát
;    → Hoặc Task Manager → Tìm tên .exe → End task
;
; ❌ VẤN ĐỀ: Key chỉ nhích 1 chút, không hold được
;    ✅ GIẢI PHÁP: ĐÃ FIX! TẤT CẢ keys giờ HOLD được khi giữ!
;    → Giữ Numpad1 → Character di chuyển Left liên tục
;    → Giữ Q → Skill spam liên tục (nếu skill hỗ trợ hold)
;    → Nhả phím → Dừng ngay lập tức!
; 
; ❌ VẤN ĐỀ: Di chuyển bị giật
;    ✅ GIẢI PHÁP: ArrowKeysUseJitter đang = true, đổi sang false
;    → Xem hướng dẫn ở SETTING 2️⃣ (Line 207)
; 
; ❌ VẤN ĐỀ: Phím không hoạt động sau khi custom
;    ✅ GIẢI PHÁP: Kiểm tra lại:
;    → Có thêm ; vào template cũ chưa?
;    → Có bỏ ; ở ĐÚNG chỗ (đầu dòng remap["..."]) chưa?
;    → Đã compile lại chưa? (compile_STEALTH_obfuscate.bat)
; 
; ❌ VẤN ĐỀ: Compile bị lỗi
;    ✅ GIẢI PHÁP: Kiểm tra lại:
;    → Có XÓA dòng "global remap := {}" không? (KHÔNG ĐƯỢC XÓA!)
;    → Có sửa code ở phần "KHÔNG NÊN THAY ĐỔI" không?
;    → Thử revert lại (Ctrl+Z) và làm lại từ đầu
;
;
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
#NoTrayIcon  ; ← STEALTH: Không hiện tray icon!
#Persistent  ; ← STEALTH: Script chạy ngầm mãi mãi
#NoTrayIcon  ; ← DOUBLE STEALTH: Đảm bảo không có tray icon!
SetBatchLines, -1
Process, Priority,, High
SendMode Input  ; ← Dùng user32.SendInput GIỐNG auto-maple bot!

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  ⚙️ ⚙️ ⚙️  TẤT CẢ SETTINGS Ở ĐÂY - DỄ TÌM, DỄ CUSTOM!  ⚙️ ⚙️ ⚙️       ║
; ║                                                                       ║
; ║  📍 4 SETTINGS CHÍNH (Tất cả ở gần nhau!):                            ║
; ║     1️⃣ Mức độ training (Desync delay 0-500ms)                        ║
; ║     2️⃣ Arrow keys jitter (Movement mượt/giật?)                       ║
; ║     3️⃣ Behavioral pause (Auto pause giống người)                     ║
; ║     4️⃣ Key remap (Template game)                                     ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 1️⃣ MỨC ĐỘ TRAINING (Desync Delay - QUAN TRỌNG!)                    ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; ⚡ SETTING MẶC ĐỊNH: MỨC TRUNG BÌNH (0-500ms) - 4-6 giờ/ngày

; ┌─────────────────────────────────────────────────────────────────────┐
; │ 🎚️ CHỌN MỨC ĐỘ TRAINING (Bỏ ; ở 2 DÒNG bạn muốn dùng)              │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ CÁCH DÙNG: Bỏ dấu ; ở ĐẦU 2 DÒNG (MinDesync và MaxDesync)
; ⚠️ CHỈ BỎ ; Ở 1 MỨC ĐỘ, THÊM ; VÀO CÁC MỨC KHÁC!
; 
; 📝 VÍ DỤ: Đổi từ MỨC TRUNG BÌNH → MỨC NẶNG (8-10 giờ/ngày)
;    BƯỚC 1: THÊM ; vào 2 dòng 110-111 (Mức trung bình)
;    BƯỚC 2: BỎ ; ở 2 dòng 114-115 (Mức nặng)
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

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 🧪 TEST MODE: TẮT DESYNC/JITTER (Chỉ dùng để test!)                ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; ⚠️ Chỉ bật khi test! BẮT BUỘC TẮT khi training thật!
; 💡 TẬP RIÊNG TỪNG FEATURE để test dễ hơn!

; ━━━ DESYNC (0-500ms delay - Phá vỡ Multiplicity sync!) ━━━
global DISABLE_DESYNC := false  ; ⭐ false = BẬT (khuyến nghị!)
; global DISABLE_DESYNC := true   ; ⚠️ true = TẮT (test mode!)

; ━━━ JITTER (30-80ms delay - Làm timing không đều!) ━━━
global DISABLE_JITTER := false  ; ⭐ false = BẬT (khuyến nghị!)
; global DISABLE_JITTER := true   ; ⚠️ true = TẮT (test mode!)

; 📊 CÁC TỔ HỢP:
; • false + false = BẬT CẢ 2 (0-580ms delay) - KHUYẾN NGHỊ! ⭐
; • false + true  = CHỈ DESYNC (0-500ms delay) - Test jitter
; • true + false  = CHỈ JITTER (30-80ms delay) - Test desync
; • true + true   = TẮT CẢ 2 (0ms instant!) - Test hold key

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 3️⃣ BEHAVIORAL PAUSE (Auto pause giống người thật)                  ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; ⚡ SETTING MẶC ĐỊNH: PAUSE VỪA PHẢI (3-5 phút, pause 0.8-2.5s)

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

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 2️⃣ ARROW KEYS JITTER (Movement mượt hay giật?)                     ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; ⚡ SETTING MẶC ĐỊNH: BẬT JITTER (0-500ms delay - Anti-detect)
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
; BƯỚC 1: THÊM ; vào đầu dòng 179 (Option 1 hiện tại)
;    TRƯỚC: global ArrowKeysUseJitter := false
;    SAU:   ; global ArrowKeysUseJitter := false
; 
; BƯỚC 2: BỎ ; ở đầu dòng 183 (Option 2)
;    TRƯỚC: ; global ArrowKeysUseJitter := true
;    SAU:   global ArrowKeysUseJitter := true
; 
; BƯỚC 3: Lưu file → Compile lại → Xong!
; 
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; ━━━ OPTION 1: KHÔNG JITTER (Movement mượt - KHUYẾN NGHỊ! ⭐) ━━━
; global ArrowKeysUseJitter := false  ; Arrow keys = instant (0ms delay)
; ✅ Ưu điểm: Di chuyển mượt mà, không giật
; ⚠️ Nhược điểm: Có thể bị detect (instant response)

; ━━━ OPTION 2: CÓ JITTER (Anti-detect tốt hơn, nhưng giật!) ━━━
global ArrowKeysUseJitter := true   ; Arrow keys = có desync+jitter ⭐ ĐANG DÙNG
; ✅ Ưu điểm: Anti-detect tốt hơn (random timing)
; ⚠️ Nhược điểm: Delay 0-500ms KHI ẤN XUỐNG (hơi lag khi bắt đầu di chuyển)

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 4️⃣ KEY REMAP (Phím nguồn → Phím đích)                              ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; ⚡ SETTING MẶC ĐỊNH: MapleStory Template
; • Skill keys: Q→A, W→S, E→D, R→F, Space→Space (có desync+jitter)
; • Movement: Numpad1→Left, 2→Down, 3→Right, 5→Up (có/không jitter tùy setting)
; 💡 Dùng NUMPAD để di chuyển thay vì arrow keys! 🎮

; ┌─────────────────────────────────────────────────────────────────────┐
; │ 🎮 CHỌN TEMPLATE GAME (Bỏ ; ở template bạn muốn dùng)               │
; └─────────────────────────────────────────────────────────────────────┘
; ✅ CÁCH DÙNG: Bỏ dấu ; ở ĐẦU CÁC DÒNG của 1 template
; ⚠️ CHỈ BỎ ; Ở 1 TEMPLATE, THÊM ; VÀO CÁC TEMPLATE KHÁC!
; 
; 📝 VÍ DỤ: Đổi từ TEMPLATE 1 → TEMPLATE 2 (Không remap)
;    BƯỚC 1: THÊM ; vào TẤT CẢ dòng remap["..."] của Template 1 (dòng 214-229)
;    BƯỚC 2: BỎ ; ở TẤT CẢ dòng remap["..."] của Template 2 (dòng 236-244)
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
; → Jitter: Tùy thuộc ArrowKeysUseJitter setting (line 141)
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

; ━━━ STARTUP CONFIRMATION ━━━
; STEALTH MODE: No beep, no tooltip - completely silent!
; SoundBeep, 800, 100
; ToolTip, STEALTH SCRIPT STARTED`nCtrl+Alt+S = Status`nCtrl+Alt+Q = Exit, 0, 0
; SetTimer, RemoveStartupTooltip, 1500
; Return

; RemoveStartupTooltip:
;     ToolTip
;     SetTimer, RemoveStartupTooltip, Off
; Return

; ━━━ REWRITE: Tạo hotkeys DOWN và UP riêng biệt! ━━━
; Tự động tạo hotkeys DOWN và UP cho mỗi key
For sourceKey, targetKey in remap {
    ; DOWN event
    Hotkey, $%sourceKey%, HandleKeyDown
    ; UP event  
    Hotkey, $%sourceKey% up, HandleKeyUp
}

; Bắt đầu timer cho behavioral pause
SetTimer, CheckBehavioralPause, 1000
ScheduleNextPause()

Return

; ═══════════════════════════════════════════════════════════════════════
; 🎛️ STEALTH HOTKEYS
; ═══════════════════════════════════════════════════════════════════════

; ━━━ Ctrl+Alt+T - Toggle script ON/OFF ━━━
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

; ━━━ Ctrl+Alt+S - Check status (NEW!) ━━━
^!s::
    global ScriptEnabled, IsPaused, NextPauseTime
    
    ; Tính thời gian còn lại đến lần pause kế tiếp
    remainingMs := NextPauseTime - A_TickCount
    if (remainingMs < 0) {
        remainingMs := 0
    }
    remainingSec := Floor(remainingMs / 1000)
    remainingMin := Floor(remainingSec / 60)
    remainingSec := Mod(remainingSec, 60)
    
    ; Xây dựng status message
    statusMsg := "=== STEALTH SCRIPT STATUS ===`n`n"
    
    if (ScriptEnabled) {
        statusMsg .= "State: ENABLED`n"
    } else {
        statusMsg .= "State: DISABLED (Passthrough mode)`n"
    }
    
    if (IsPaused) {
        statusMsg .= "Pause: ACTIVE (blocking input now!)`n"
    } else {
        statusMsg .= "Pause: NOT ACTIVE`n"
    }
    
    statusMsg .= "Next pause: " . remainingMin . "m " . remainingSec . "s`n`n"
    statusMsg .= "Ctrl+Alt+T = Toggle ON/OFF`n"
    statusMsg .= "Ctrl+Alt+Q = Exit script"
    
    SoundBeep, 600, 50
    ToolTip, %statusMsg%, 0, 0
    SetTimer, RemoveStatusTooltip, 3000
Return

RemoveStatusTooltip:
    ToolTip
    SetTimer, RemoveStatusTooltip, Off
Return

; ━━━ Ctrl+Alt+Q - Exit script (NEW!) ━━━
^!q::
    SoundBeep, 1000, 150
    Sleep, 100
    SoundBeep, 800, 150
    ToolTip, STEALTH SCRIPT EXITING..., 0, 0
    Sleep, 500
    ExitApp
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔽 HANDLE KEY DOWN EVENT
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HandleKeyDown:
    global ScriptEnabled, IsPaused, ArrowKeysUseJitter, MinDesync, MaxDesync, DISABLE_DESYNC, DISABLE_JITTER, remap
    global MinJitter, MaxJitter, UseGaussian
    
    ; Nếu script bị tắt, passthrough phím gốc
    if (!ScriptEnabled) {
        pressedKey := StrReplace(A_ThisHotkey, "$", "")
        pressedKey := StrReplace(pressedKey, " up", "")  ; Remove " up" if exists
        SendInput, {%pressedKey% down}
        return
    }
    
    ; Kiểm tra xem có đang pause không
    if (IsPaused) {
        return ; Block input khi đang pause
    }
    
    ; Lấy phím được ấn
    pressedKey := StrReplace(A_ThisHotkey, "$", "")
    pressedKey := StrReplace(pressedKey, " up", "")  ; Remove " up" if exists
    
    ; Lấy phím đích từ bảng remap
    targetKey := remap[pressedKey]
    
    ; ⚡ CHECK ARROW KEYS (Numpad hoặc Arrow keys)
    isArrowKey := (pressedKey = "Numpad1" || pressedKey = "Numpad2" || pressedKey = "Numpad3" || pressedKey = "Numpad5" || pressedKey = "Left" || pressedKey = "Right" || pressedKey = "Up" || pressedKey = "Down")
    
    ; ━━━ ARROW KEYS INSTANT (nếu ArrowKeysUseJitter = false) ━━━
    if (isArrowKey && !ArrowKeysUseJitter) {
        ; INSTANT: Send DOWN ngay lập tức (0ms delay)
        SendInput, {%targetKey% down}
        return
    }
    
    ; ━━━ TẤT CẢ KEYS (ARROW + SKILL): DÙNG LOGIC GIỐNG NHAU! ━━━
    
    ; BƯỚC 1: DESYNC (nếu không disable)
    if (!DISABLE_DESYNC) {
        Random, desyncDelay, %MinDesync%, %MaxDesync%
        Sleep, %desyncDelay%
    }
    
    ; BƯỚC 2: JITTER (nếu không disable)
    if (!DISABLE_JITTER) {
        if (UseGaussian) {
            mean := (MinJitter + MaxJitter) / 2.0
            stdDev := (MaxJitter - MinJitter) / 6.0
            jitter := GaussianRandom(mean, stdDev, MinJitter, MaxJitter)
        } else {
            Random, jitter, %MinJitter%, %MaxJitter%
        }
        Sleep, %jitter%
    }
    
    ; BƯỚC 3: Send target key DOWN
    SendInput, {%targetKey% down}
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔼 HANDLE KEY UP EVENT  
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HandleKeyUp:
    global ScriptEnabled, IsPaused, remap
    
    ; Nếu script bị tắt, passthrough
    if (!ScriptEnabled) {
        pressedKey := StrReplace(A_ThisHotkey, "$", "")
        pressedKey := StrReplace(pressedKey, " up", "")
        SendInput, {%pressedKey% up}
        return
    }
    
    ; Nếu đang pause, bỏ qua
    if (IsPaused) {
        return
    }
    
    ; Lấy phím được nhả
    pressedKey := StrReplace(A_ThisHotkey, "$", "")
    pressedKey := StrReplace(pressedKey, " up", "")
    
    ; Lấy phím đích
    targetKey := remap[pressedKey]
    
    ; Send target key UP (NGAY LẬP TỨC - KHÔNG DELAY!)
    SendInput, {%targetKey% up}
Return

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


