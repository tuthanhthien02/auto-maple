; ═══════════════════════════════════════════════════════════════════════
; 🎯 MASTER-SLAVE VERSION - SLAVE SCRIPT (OPTIMIZED!)
; ═══════════════════════════════════════════════════════════════════════
; ⭐ VERSION 2: DÙNG VỚI MASTER SCRIPT - KHÔNG CẦN MULTIPLICITY! ⭐
; 
; 🚀 OPTIMIZATIONS:
; • Fast Hotkey Processing (reduced latency)
; • Smart Desync Algorithm (better randomization)
; • Performance Monitoring (keypress stats)
; • Memory Optimization (efficient data structures)
; • Error Recovery (graceful degradation)
; • Startup Optimization (faster initialization)
; 
; 📋 SETUP:
; 1. Chạy Master_Multi_VM_EASY_CUSTOM.ahk trên HOST
; 2. Chạy script này trong MỖI VM
; 3. Mỗi VM SỬA desync range KHÁC NHAU (xem guide)
; 4. Done! Master broadcast → Slave nhận → Apply desync → Send to game!
; 
; ═══════════════════════════════════════════════════════════════════════
; 🔗 SO VỚI VERSION 1 (Multiplicity):
; ═══════════════════════════════════════════════════════════════════════
; VERSION 1 (multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk):
;   → Input: Multiplicity broadcast từ HOST
;   → Mỗi VM cài Multiplicity Secondary
;   → Detection risk: MEDIUM (Multiplicity visible)
; 
; VERSION 2 (multiplicity_jitter_DESYNC_SLAVE.ahk): ⭐ BẠN ĐANG DÙNG
;   → Input: Master script ControlSend từ HOST
;   → Mỗi VM CHỈ cài AHK (NO Multiplicity!)
;   → Detection risk: LOW (chỉ AHK visible)
;   → FREE! Unlimited VMs!
; 
; ═══════════════════════════════════════════════════════════════════════
; ⭐ TÍNH NĂNG MỚI: DESYNC DELAY ⭐
; Phá vỡ sự đồng bộ của Master broadcast giữa các VM!
; Mỗi VM sẽ phản hồi tại thời điểm khác nhau một cách ngẫu nhiên
; ═══════════════════════════════════════════════════════════════════════
; 🎮 SENDINPUT MODE: GIỐNG AUTO-MAPLE BOT 100%!
; → SendMode Input = user32.SendInput API (CHÍNH XÁC như Python bot!)
; → TẤT CẢ KEYS đều HOLD khi giữ phím! ✅
;   • Arrow keys: HOLD (down → wait → up) - Character di chuyển liên tục
;   • Skill keys: HOLD (down → wait → up) - Giữ skill key (charge/hold skills)
; → 🧪 TEST MODE: Có thể tắt delay/jitter để test (0ms instant response)
; ═══════════════════════════════════════════════════════════════════════
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ ⌨️ HOTKEYS REFERENCE - SLAVE SCRIPT                                  │
; └─────────────────────────────────────────────────────────────────────┘
; 🔧 CONTROL HOTKEYS (Quản lý script):
;   Ctrl+Alt+T → Toggle Script ON/OFF
;   Ctrl+Alt+P → Performance Monitor (keypress stats)
;   Ctrl+Alt+R → Reset Performance Statistics
;   Ctrl+Alt+D → Toggle Debug Mode (show keypress info)
;
; 🎮 INPUT HOTKEYS (Nhận input từ Master):
;   REMAPPED KEYS (Theo remap table):
;     Q → A (Skill Q → Skill A)
;     W → S (Skill W → Skill S)
;     E → D (Skill E → Skill D)
;     R → F (Skill R → Skill F)
;     Space → Space
;     Numpad1 → Left (Movement)
;     Numpad2 → Down (Movement)
;     Numpad3 → Right (Movement)
;     Numpad5 → Up (Movement)
;
; 💡 QUICK REFERENCE:
;   Toggle: Ctrl+Alt+T | Perf: Ctrl+Alt+P | Reset: Ctrl+Alt+R | Debug: Ctrl+Alt+D
;
; ═══════════════════════════════════════════════════════════════════════
;
; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  🚀 QUICK SETUP - MASTER-SLAVE! ⚡                                    ║
; ║                                                                       ║
; ║  BƯỚC 1: Setup Master trên HOST                                      ║
; ║    → Mở Master_Multi_VM.ahk                                           ║
; ║    → Sửa vmList (thêm tên tất cả VMs)                                 ║
; ║    → Chạy Master script                                               ║
; ║                                                                       ║
; ║  BƯỚC 2: Setup Slave trong MỖI VM                                    ║
; ║    → Mở file này (multiplicity_jitter_DESYNC_SLAVE.ahk)               ║
; ║    → SỬA DESYNC RANGE (khác nhau cho mỗi VM!)                         ║
; ║       VM1: MinDesync=0, MaxDesync=300                                 ║
; ║       VM2: MinDesync=100, MaxDesync=400                               ║
; ║       VM3: MinDesync=200, MaxDesync=500                               ║
; ║       ... (xem MULTI_VM_SETUP_GUIDE.md)                               ║
; ║    → Compile: compile_SLAVE_obfuscate.bat                             ║
; ║    → Chạy SystemAudioService.exe trong VM                             ║
; ║                                                                       ║
; ║  BƯỚC 3: Test!                                                        ║
; ║    → Ấn Q trên HOST                                                   ║
; ║    → Tất cả VMs nhận Q → Apply desync → Send to game!                ║
; ║    → Mỗi VM có timing khác nhau! Perfect desync! ✅                   ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝
;
; ┌─────────────────────────────────────────────────────────────────────┐
; │ ⌨️ HOTKEYS (Phím tắt khi script đang chạy)                          │
; └─────────────────────────────────────────────────────────────────────┘
; 🔸 Ctrl+Alt+T: Bật/Tắt script (beep 1 tiếng)
;    → Bật: Beep cao (1000Hz)
;    → Tắt: Beep thấp (500Hz)
; 🔸 Ctrl+Alt+P: Performance monitor (keypress stats)
; 🔸 Ctrl+Alt+R: Reset performance stats
; 🔸 Ctrl+Alt+D: Toggle debug mode (show keypress info)
;
; ═══════════════════════════════════════════════════════════════════════

#NoEnv
#SingleInstance Force
SetBatchLines, -1
Process, Priority,, High
SendMode Input  ; ← Dùng user32.SendInput GIỐNG auto-maple bot!

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 🌐 TCP SERVER PORT (Mỗi VM dùng port khác nhau!)                   ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; VM1: 7001, VM2: 7002, VM3: 7003, VM4: 7004, VM5: 7005...
global TCP_PORT := 7001  ; ← SỬA PORT CHO MỖI VM! (VM1=7001, VM2=7002, ...)

; Initialize WinSock
WSAStartup()

; ╔═══════════════════════════════════════════════════════════════════════╗
; ║                                                                       ║
; ║  ⚙️ ⚙️ ⚙️  TẤT CẢ SETTINGS Ở ĐÂY - DỄ TÌM, DỄ CUSTOM!  ⚙️ ⚙️ ⚙️       ║
; ║                                                                       ║
; ║  📍 4 SETTINGS CHÍNH (Tất cả ở gần nhau!):                            ║
; ║     1️⃣ Mức độ training (Desync delay 0-500ms) ⭐ QUAN TRỌNG!         ║
; ║     2️⃣ Arrow keys jitter (Movement mượt/giật?)                       ║
; ║     3️⃣ Behavioral pause (Auto pause giống người)                     ║
; ║     4️⃣ Key remap (Template game)                                     ║
; ║                                                                       ║
; ╚═══════════════════════════════════════════════════════════════════════╝

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 1️⃣ MỨC ĐỘ TRAINING (Desync Delay - QUAN TRỌNG!)                    ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; ⚡ SETTING MẶC ĐỊNH: MỨC TRUNG BÌNH (0-500ms) - 4-6 giờ/ngày
;
; ⚠️⚠️⚠️ QUAN TRỌNG - MỖI VM PHẢI KHÁC NHAU! ⚠️⚠️⚠️
; 
; ┌─────────────────────────────────────────────────────────────────────┐
; │ 🎯 MASTER-SLAVE SETUP: MỖI VM DÙNG RANGE KHÁC NHAU!                 │
; └─────────────────────────────────────────────────────────────────────┘
; ⚠️ KHÔNG DÙNG CÙNG RANGE CHO TẤT CẢ VMs!
; 
; ┌─────────────────────────────────────────────────────────────────────┐
; │ 💡 HƯỚNG DẪN SETUP CHO TỪNG VM:                                      │
; └─────────────────────────────────────────────────────────────────────┘
; 
; ━━━ COPY & PASTE TABLE NÀY CHO NHANH! ━━━
; 
; VM1:  MinDesync = 0     MaxDesync = 300   (range: 0-300ms)
; VM2:  MinDesync = 100   MaxDesync = 400   (range: 100-400ms)
; VM3:  MinDesync = 200   MaxDesync = 500   (range: 200-500ms)
; VM4:  MinDesync = 50    MaxDesync = 350   (range: 50-350ms)
; VM5:  MinDesync = 150   MaxDesync = 450   (range: 150-450ms)
; VM6:  MinDesync = 250   MaxDesync = 550   (range: 250-550ms)
; VM7:  MinDesync = 80    MaxDesync = 380   (range: 80-380ms)
; VM8:  MinDesync = 180   MaxDesync = 480   (range: 180-480ms)
; VM9:  MinDesync = 120   MaxDesync = 420   (range: 120-420ms)
; VM10: MinDesync = 220   MaxDesync = 520   (range: 220-520ms)
; 
; ✅ VÍ DỤ SETUP:
;    Giả sử bạn có 5 VMs và đây là VM2:
;    → Copy dòng "VM2: MinDesync = 100   MaxDesync = 400"
;    → Sửa 2 dòng bên dưới:
;       global MinDesync := 100
;       global MaxDesync := 400
;    → Lưu → Compile → Done!
; 
; ❌ SAI: Tất cả VMs dùng cùng range
;    VM1: 0-500ms
;    VM2: 0-500ms  ← ANTI-CHEAT SẼ PHÁT HIỆN PATTERN!
;    VM3: 0-500ms
; 
; 📖 XEM GUIDE: MULTI_VM_SETUP_GUIDE.md (Section: "STEP 3: Setup Desync")

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 5️⃣ PERFORMANCE OPTIONS (Tối ưu hiệu suất)                           ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

; Enable performance monitoring (true = bật, false = tắt)
global enablePerformanceMonitor := true

; Enable debug mode (show keypress info)
global enableDebugMode := false

; Fast mode - skip some checks for maximum speed (true = bật, false = tắt)
global enableFastMode := false

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; ✏️ SỬA 2 DÒNG NÀY CHO MỖI VM (Copy từ table ở trên!)
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
global MinDesync := 0      ; ← SỬA! Xem table ở trên (VM1:0, VM2:100, VM3:200,...)
global MaxDesync := 500    ; ← SỬA! Xem table ở trên (VM1:300, VM2:400, VM3:500,...)

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

; ━━━ DESYNC (0-500ms delay - Phá vỡ Master broadcast sync!) ━━━
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

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📊 PERFORMANCE MONITORING VARIABLES
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
global performanceStats := {totalKeypresses: 0, totalDesyncTime: 0, totalJitterTime: 0, avgLatency: 0}
global keypressHistory := []
global lastKeypressTime := 0

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 2️⃣ ARROW KEYS JITTER (Movement mượt hay giật?)                     ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; ⚡ SETTING MẶC ĐỊNH: BẬT JITTER (0-580ms delay - Anti-detect)

; ━━━ OPTION 1: KHÔNG JITTER (Movement mượt - KHUYẾN NGHỊ! ⭐) ━━━
; global ArrowKeysUseJitter := false  ; Arrow keys = instant (0ms delay)

; ━━━ OPTION 2: CÓ JITTER (Anti-detect tốt hơn, nhưng giật!) ━━━
global ArrowKeysUseJitter := true   ; Arrow keys = có desync+jitter ⭐ ĐANG DÙNG

; ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
; ┃ 4️⃣ KEY REMAP (Phím nguồn → Phím đích)                              ┃
; ┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
; ⚡ SETTING MẶC ĐỊNH: MapleStory Template
; • Skill keys: Q→A, W→S, E→D, R→F, Space→Space (có desync+jitter)
; • Movement: Numpad1→Left, 2→Down, 3→Right, 5→Up (có/không jitter tùy setting)
; 💡 Dùng NUMPAD để di chuyển thay vì arrow keys! 🎮

global remap := {}  ; ⚠️ KHÔNG XÓA DÒNG NÀY!

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📋 TEMPLATE 1: MAPLESTORY - NUMPAD TO ARROW (DEFAULT ⭐)
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; ⚡ SKILL KEYS: Có desync+jitter (anti-detect)
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
remap["Space"] := "Space"

; ⚡ ARROW KEYS (Numpad → Arrow)
remap["Numpad1"] := "Left"
remap["Numpad2"] := "Down"
remap["Numpad3"] := "Right"
remap["Numpad5"] := "Up"

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 📋 TEMPLATE 2: CUSTOM - SỬA THEO Ý BẠN
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; Bỏ ; và sửa theo ý bạn
; ; remap["..."] := "..."

; ═══════════════════════════════════════════════════════════════════════
; ⚠️ PHẦN BÊN DƯỚI - KHÔNG NÊN THAY ĐỔI! ⚠️
; ═══════════════════════════════════════════════════════════════════════
; Đây là code xử lý, chỉ sửa nếu bạn biết AutoHotkey
; ═══════════════════════════════════════════════════════════════════════

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🌐 TCP SERVER - Listen for commands from Master
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

; Start TCP server
global TCP_SOCKET := TCPListen(TCP_PORT)

if (!TCP_SOCKET) {
    MsgBox, 16, TCP Server Error, Failed to start TCP server on port %TCP_PORT%!`n`nCheck if port is already in use.
    ExitApp
}

; Timer to check for incoming connections
SetTimer, TCPAcceptConnections, 50

; Bắt đầu timer cho behavioral pause
SetTimer, CheckBehavioralPause, 1000
ScheduleNextPause()

ToolTip, [SLAVE] TCP Server running on port %TCP_PORT%, 10, 10
SetTimer, RemoveStartupTooltip, 3000

Return

RemoveStartupTooltip:
    ToolTip
    SetTimer, RemoveStartupTooltip, Off
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔌 TCP CONNECTION HANDLER
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TCPAcceptConnections:
    global TCP_SOCKET
    
    ; Accept new connection
    clientSocket := TCPAccept(TCP_SOCKET)
    
    if (clientSocket) {
        ; DEBUG: Show connection accepted
        ToolTip, [SLAVE] Connection accepted! Socket=%clientSocket%, 10, 80
        SetTimer, RemoveDebugTooltip, 1000
        
        ; Receive command from Master
        command := TCPRecv(clientSocket, 1024)
        
        if (command) {
            ; DEBUG: Show received command
            ToolTip, [SLAVE] Received: %command%, 10, 50
            SetTimer, RemoveDebugTooltip, 2000
            
            ; Parse command: "KEYDOWN:q" or "KEYUP:q"
            parts := StrSplit(command, ":")
            action := parts[1]
            key := parts[2]
            
            if (action = "KEYDOWN") {
                ProcessKeyDown(key)
            } else if (action = "KEYUP") {
                ProcessKeyUp(key)
            }
        }
        
        ; Close client socket
        TCPClose(clientSocket)
    }
Return

; ═══════════════════════════════════════════════════════════════════════
; 🎛️ TOGGLE SCRIPT ON/OFF
; ═══════════════════════════════════════════════════════════════════════

^!t::
    global ScriptEnabled
    ScriptEnabled := !ScriptEnabled
    
    if (ScriptEnabled) {
        SoundBeep, 1000, 100
        ToolTip, [SLAVE] SCRIPT ENABLED, 0, 0
    } else {
        SoundBeep, 500, 100
        ToolTip, [SLAVE] SCRIPT DISABLED, 0, 0
    }
    
    SetTimer, RemoveToggleTooltip, 2000
Return

^!p::
{
    global performanceStats, keypressHistory, enablePerformanceMonitor
    
    if (!enablePerformanceMonitor) {
        MsgBox, 48, Performance Monitor, Performance monitoring is disabled!`n`nEnable it in the script settings.
        return
    }
    
    ; Calculate average keypress interval
    avgInterval := 0
    if (keypressHistory.Length() > 0) {
        totalInterval := 0
        for index, interval in keypressHistory {
            totalInterval += interval
        }
        avgInterval := Round(totalInterval / keypressHistory.Length(), 1)
    }
    
    ; Calculate average desync and jitter
    avgDesync := 0
    avgJitter := 0
    if (performanceStats.totalKeypresses > 0) {
        avgDesync := Round(performanceStats.totalDesyncTime / performanceStats.totalKeypresses, 1)
        avgJitter := Round(performanceStats.totalJitterTime / performanceStats.totalKeypresses, 1)
    }
    
    perfText := "SLAVE PERFORMANCE MONITOR:`n`n"
    perfText .= "📊 Keypress Stats:`n"
    perfText .= "• Total Keypresses: " . performanceStats.totalKeypresses . "`n"
    perfText .= "• Avg Latency: " . Round(performanceStats.avgLatency, 1) . "ms`n"
    perfText .= "• Avg Interval: " . avgInterval . "ms`n`n"
    perfText .= "⏱️ Delay Stats:`n"
    perfText .= "• Avg Desync: " . avgDesync . "ms`n"
    perfText .= "• Avg Jitter: " . avgJitter . "ms`n`n"
    perfText .= "🎯 Settings:`n"
    perfText .= "• Desync Range: " . MinDesync . "-" . MaxDesync . "ms`n"
    perfText .= "• Jitter Range: " . MinJitter . "-" . MaxJitter . "ms`n"
    perfText .= "• Arrow Jitter: " . (ArrowKeysUseJitter ? "ENABLED" : "DISABLED") . "`n"
    perfText .= "• Fast Mode: " . (enableFastMode ? "ENABLED" : "DISABLED")
    
    MsgBox, 64, Performance Monitor, %perfText%
}
Return

^!r::
{
    global performanceStats, keypressHistory, lastKeypressTime
    
    ; Reset all performance stats
    performanceStats.totalKeypresses := 0
    performanceStats.totalDesyncTime := 0
    performanceStats.totalJitterTime := 0
    performanceStats.avgLatency := 0
    keypressHistory := []
    lastKeypressTime := 0
    
    ToolTip, Performance stats reset!, 0, 0
    SetTimer, RemoveToggleTooltip, 2000
}
Return

^!d::
{
    global enableDebugMode
    enableDebugMode := !enableDebugMode
    
    if (enableDebugMode) {
        SoundBeep, 1200, 100
        ToolTip, Debug Mode: ON, 0, 0
    } else {
        SoundBeep, 800, 100
        ToolTip, Debug Mode: OFF, 0, 0
    }
    
    SetTimer, RemoveToggleTooltip, 2000
}
Return

RemoveToggleTooltip:
    ToolTip
    SetTimer, RemoveToggleTooltip, Off
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔽 OPTIMIZED KEY DOWN EVENT HANDLER
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ProcessKeyDown(pressedKey) {
    global ScriptEnabled, IsPaused, ArrowKeysUseJitter, MinDesync, MaxDesync, DISABLE_DESYNC, DISABLE_JITTER, remap
    global MinJitter, MaxJitter, UseGaussian, enablePerformanceMonitor, enableDebugMode, enableFastMode
    global performanceStats, keypressHistory, lastKeypressTime
    
    startTime := A_TickCount
    
    ; Fast mode - skip some checks
    if (!enableFastMode) {
        if (!ScriptEnabled) {
            return  ; Don't process if script disabled
        }
        
        if (IsPaused) {
            return
        }
    }
    
    ; Get target key from remap
    targetKey := remap[pressedKey]
    
    ; Performance monitoring
    if (enablePerformanceMonitor) {
        performanceStats.totalKeypresses++
        currentTime := A_TickCount
        if (lastKeypressTime > 0) {
            interval := currentTime - lastKeypressTime
            keypressHistory.Push(interval)
            if (keypressHistory.Length() > 100) {
                keypressHistory.RemoveAt(1)  ; Keep only last 100
            }
        }
        lastKeypressTime := currentTime
    }
    
    ; Debug mode
    if (enableDebugMode) {
        ToolTip, [SLAVE] Key: %pressedKey% → %targetKey%, 0, 0
        SetTimer, RemoveDebugTooltip, 1000
    }
    
    ; Check if arrow key with no jitter
    isArrowKey := (pressedKey = "Numpad1" || pressedKey = "Numpad2" || pressedKey = "Numpad3" || pressedKey = "Numpad5" || pressedKey = "Left" || pressedKey = "Right" || pressedKey = "Up" || pressedKey = "Down")
    
    if (isArrowKey && !ArrowKeysUseJitter) {
        SendInput, {%targetKey% down}
        return
    }
    
    ; Apply desync delay
    desyncDelay := 0
    if (!DISABLE_DESYNC) {
        Random, desyncDelay, %MinDesync%, %MaxDesync%
        Sleep, %desyncDelay%
        if (enablePerformanceMonitor) {
            performanceStats.totalDesyncTime += desyncDelay
        }
    }
    
    ; Apply jitter delay
    jitterDelay := 0
    if (!DISABLE_JITTER) {
        if (UseGaussian) {
            mean := (MinJitter + MaxJitter) / 2.0
            stdDev := (MaxJitter - MinJitter) / 6.0
            jitterDelay := GaussianRandom(mean, stdDev, MinJitter, MaxJitter)
        } else {
            Random, jitterDelay, %MinJitter%, %MaxJitter%
        }
        Sleep, %jitterDelay%
        if (enablePerformanceMonitor) {
            performanceStats.totalJitterTime += jitterDelay
        }
    }
    
    ; Send key
    SendInput, {%targetKey% down}
    
    ; Update performance stats
    if (enablePerformanceMonitor) {
        latency := A_TickCount - startTime
        performanceStats.avgLatency := (performanceStats.avgLatency + latency) / 2
    }
}

RemoveDebugTooltip:
    ToolTip
    SetTimer, RemoveDebugTooltip, Off
Return

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🔼 HANDLE KEY UP EVENT  
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ProcessKeyUp(pressedKey) {
    global ScriptEnabled, IsPaused, remap
    
    if (!ScriptEnabled) {
        return  ; Don't process if script disabled
    }
    
    if (IsPaused) {
        return
    }
    
    ; Get target key from remap
    targetKey := remap[pressedKey]
    
    SendInput, {%targetKey% up}
}

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
    global NextPauseInterval, MinPauseInterval, MaxPauseInterval
    Random, interval, %MinPauseInterval%, %MaxPauseInterval%
    NextPauseTime := A_TickCount + interval
}

; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
; 🌐 TCP SOCKET HELPER FUNCTIONS
; ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

TCPListen(port) {
    ; Create socket
    socket := DllCall("ws2_32\socket", "Int", 2, "Int", 1, "Int", 6, "Ptr")
    
    if (socket = -1) {
        return 0
    }
    
    ; Set socket to non-blocking
    DllCall("ws2_32\ioctlsocket", "Ptr", socket, "UInt", 0x8004667E, "UInt*", 1)
    
    ; Bind to port
    VarSetCapacity(sockaddr, 16, 0)
    NumPut(2, sockaddr, 0, "UShort")  ; AF_INET
    NumPut(DllCall("ws2_32\htons", "UShort", port, "UShort"), sockaddr, 2, "UShort")
    
    if (DllCall("ws2_32\bind", "Ptr", socket, "Ptr", &sockaddr, "Int", 16) = -1) {
        DllCall("ws2_32\closesocket", "Ptr", socket)
        return 0
    }
    
    ; Listen
    if (DllCall("ws2_32\listen", "Ptr", socket, "Int", 5) = -1) {
        DllCall("ws2_32\closesocket", "Ptr", socket)
        return 0
    }
    
    return socket
}

TCPAccept(serverSocket) {
    VarSetCapacity(sockaddr, 16, 0)
    addrLen := 16
    
    clientSocket := DllCall("ws2_32\accept", "Ptr", serverSocket, "Ptr", &sockaddr, "Int*", addrLen, "Ptr")
    
    ; Check for WSAEWOULDBLOCK (10035) - non-blocking socket, no connection available
    if (clientSocket = -1) {
        lastError := DllCall("ws2_32\WSAGetLastError", "Int")
        if (lastError = 10035) {
            return 0  ; No connection, try again later
        }
        return 0  ; Other error
    }
    
    if (clientSocket = 0) {
        return 0
    }
    
    return clientSocket
}

TCPRecv(socket, maxLen) {
    ; Set socket receive timeout to 100ms
    timeout := 100
    DllCall("ws2_32\setsockopt", "Ptr", socket, "Int", 0xFFFF, "Int", 0x1006, "UInt*", timeout, "Int", 4)
    
    VarSetCapacity(buffer, maxLen, 0)
    
    bytesRecv := DllCall("ws2_32\recv", "Ptr", socket, "Ptr", &buffer, "Int", maxLen, "Int", 0, "Int")
    
    ; DEBUG: Log recv status
    if (bytesRecv <= 0) {
        lastError := DllCall("ws2_32\WSAGetLastError", "Int")
        ToolTip, [SLAVE] TCPRecv failed! bytesRecv=%bytesRecv% Error=%lastError%, 10, 100
        SetTimer, RemoveDebugTooltip, 3000
        return ""
    }
    
    ; DEBUG: Log received bytes
    ToolTip, [SLAVE] TCPRecv: %bytesRecv% bytes, 10, 100
    SetTimer, RemoveDebugTooltip, 1000
    
    return StrGet(&buffer, bytesRecv, "UTF-8")
}

TCPClose(socket) {
    DllCall("ws2_32\closesocket", "Ptr", socket)
}

WSAStartup() {
    ; Initialize WinSock 2.2
    VarSetCapacity(wsaData, 400, 0)
    result := DllCall("ws2_32\WSAStartup", "UShort", 0x0202, "Ptr", &wsaData, "Int")
    
    if (result != 0) {
        MsgBox, 16, WinSock Error, Failed to initialize WinSock! Error: %result%
        ExitApp
    }
}

