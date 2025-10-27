# 🚀 QUICK START GUIDE - VERSION 2 (Master-Slave)

## 🎯 **1 HOST → N SLAVES - SETUP NHANH CHỈ 5 PHÚT!**

```
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  🖥️  HOST (1 máy)                                                │
│      ↓                                                           │
│      Master_Multi_VM_EASY_CUSTOM.ahk                             │
│      ↓                                                           │
│      Broadcast Input                                             │
│      ↓                                                           │
│  ┌───┴───┬───────┬───────┬───────┬───────┐                      │
│  ↓       ↓       ↓       ↓       ↓       ↓                      │
│  VM1     VM2     VM3     VM4     VM5    ... VMN                 │
│  ↓       ↓       ↓       ↓       ↓       ↓                      │
│  Slave   Slave   Slave   Slave   Slave  ... Slave               │
│  0-300ms 100-400 200-500 50-350  150-450 ... (unique!)          │
│                                                                  │
│  🎯 MỖI VM APPLY DESYNC KHÁC NHAU → PHẢN HỒI KHÁC THỜI ĐIỂM!    │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 📋 **FILES CẦN DÙNG:**

### **📂 Trên HOST (1 lần setup):**

-   ✅ `Master_Multi_VM_EASY_CUSTOM.ahk` - Master script
-   ✅ `compile_MASTER_obfuscate.bat` - Compile master

### **📂 Trong MỖI VM (setup N lần):**

-   ✅ `multiplicity_jitter_DESYNC_SLAVE.ahk` - Slave script
-   ✅ `compile_SLAVE_obfuscate.bat` - Compile slave

---

## 🔑 **KEY POINTS - ĐỌC TRƯỚC KHI SETUP:**

```
┌──────────────────────────────────────────────────────────────────┐
│  ✅ GIỐNG NHAU CHO TẤT CẢ VMs (Copy Same File):                  │
│     • Slave script file (.ahk)                                   │
│     • Tất cả settings TRỪ Desync Range                           │
│     • Compile batch file                                         │
│                                                                  │
│  ⚠️  KHÁC NHAU CHO MỖI VM (MUST BE UNIQUE!):                     │
│     • MinDesync value (0, 100, 200, 50, 150, ...)               │
│     • MaxDesync value (300, 400, 500, 350, 450, ...)            │
│                                                                  │
│  ⭐ CỐT LÕI: Chỉ cần sửa 2 số (MinDesync, MaxDesync) mỗi VM!     │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🚀 **SETUP 3 BƯỚC:**

### **BƯỚC 1: Setup Master (HOST) - 2 phút**

```
1. Mở Master_Multi_VM_EASY_CUSTOM.ahk

2. TÌM TÊN VMs (chọn 1 cách):
   Cách 1: Chạy script → Ctrl+Alt+L → Copy tên VMs
   Cách 2: Mở VM → Alt+Tab → Note lại tên

3. SỬA vmList (Line 77-90):
   vmList.Push("Win10-VM1 - VMware Workstation")  ; VM 1
   vmList.Push("Win10-VM2 - VMware Workstation")  ; VM 2
   vmList.Push("Win10-VM3 - VMware Workstation")  ; VM 3
   ... (thêm tên VMs của bạn)

4. LƯU FILE (Ctrl+S)

5. COMPILE (tùy chọn):
   → Chạy compile_MASTER_obfuscate.bat
   → Output: WindowsTaskScheduler.exe
```

---

### **BƯỚC 2: Setup Slave (MỖI VM) - 3 phút x N VMs**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  🎯 WORKFLOW: LẶP LẠI CHO MỖI VM (VM1 → VM2 → VM3 → ... VMN) ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌──────────────────────────────────────────────────────────────┐
│  📋 DESYNC TABLE - COPY & PASTE CHO NHANH!                   │
└──────────────────────────────────────────────────────────────┘

VM1:   MinDesync = 0     MaxDesync = 300   (range: 0-300ms)
VM2:   MinDesync = 100   MaxDesync = 400   (range: 100-400ms)
VM3:   MinDesync = 200   MaxDesync = 500   (range: 200-500ms)
VM4:   MinDesync = 50    MaxDesync = 350   (range: 50-350ms)
VM5:   MinDesync = 150   MaxDesync = 450   (range: 150-450ms)
VM6:   MinDesync = 250   MaxDesync = 550   (range: 250-550ms)
VM7:   MinDesync = 80    MaxDesync = 380   (range: 80-380ms)
VM8:   MinDesync = 180   MaxDesync = 480   (range: 180-480ms)
VM9:   MinDesync = 120   MaxDesync = 420   (range: 120-420ms)
VM10:  MinDesync = 220   MaxDesync = 520   (range: 220-520ms)

💡 Có nhiều hơn 10 VMs? Dùng công thức:
   VM(N): MinDesync = (N-1)*100 + random(0-50)
          MaxDesync = MinDesync + 300

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📝 CHO MỖI VM, LÀM THEO 5 BƯỚC SAU:

1️⃣  Copy multiplicity_jitter_DESYNC_SLAVE.ahk vào VM

2️⃣  Mở file → Tìm dòng 139-140 (hoặc Ctrl+G → nhập 139)

3️⃣  SỬA 2 DÒNG (copy từ table ở trên theo số VM):

    ┌─ VÍ DỤ CHO VM1: ─────────────────────┐
    │ global MinDesync := 0                │
    │ global MaxDesync := 300              │
    └──────────────────────────────────────┘

    ┌─ VÍ DỤ CHO VM2: ─────────────────────┐
    │ global MinDesync := 100              │
    │ global MaxDesync := 400              │
    └──────────────────────────────────────┘

    ┌─ VÍ DỤ CHO VM3: ─────────────────────┐
    │ global MinDesync := 200              │
    │ global MaxDesync := 500              │
    └──────────────────────────────────────┘

4️⃣  LƯU FILE (Ctrl+S)

5️⃣  COMPILE:
    → Chạy compile_SLAVE_obfuscate.bat
    → Output: SystemAudioService.exe

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ DONE MỘT VM? → LẶP LẠI CHO VM TIẾP THEO!
   (Nhớ thay đổi MinDesync/MaxDesync theo table!)

⚠️  CRITICAL: MỖI VM PHẢI DÙNG RANGE KHÁC NHAU!
   ❌ SAI: VM1=0-300, VM2=0-300, VM3=0-300 (trùng nhau!)
   ✅ ĐÚNG: VM1=0-300, VM2=100-400, VM3=200-500 (khác nhau!)
```

---

### **BƯỚC 3: CHẠY & TEST! - 1 phút**

```
1. TRONG MỖI VM:
   → Chạy SystemAudioService.exe
   → Nghe beep = thành công!

2. TRÊN HOST:
   → Chạy WindowsTaskScheduler.exe (hoặc Master script)
   → Nghe beep = thành công!
   → Ấn Ctrl+Alt+S để check status

3. TEST:
   → Ấn Q trên HOST
   → Xem tất cả VMs có nhận không
   → Mỗi VM sẽ delay khác nhau (desync!)
```

---

## 📊 **SO SÁNH SETTINGS:**

### **Master Script Settings:**

| **Setting**       | **Location** | **Mô tả**                              |
| ----------------- | ------------ | -------------------------------------- |
| vmList            | Line 77-90   | Tên VMs (QUAN TRỌNG!)                  |
| showDebugTooltip  | Line 104     | Hiện tooltip (true/false)              |
| enableBeep        | Line 107     | Beep (true/false)                      |
| Keys to broadcast | Line 110-170 | Phím nào sẽ broadcast (thêm/bớt tùy ý) |

### **Slave Script Settings:**

| **Setting**        | **Location** | **Mô tả**                               |
| ------------------ | ------------ | --------------------------------------- |
| MinDesync          | Line 139     | Desync min (KHÁC NHAU MỖI VM! ⭐)       |
| MaxDesync          | Line 140     | Desync max (KHÁC NHAU MỖI VM! ⭐)       |
| ArrowKeysUseJitter | Line 243     | Arrow keys có jitter không (true/false) |
| MinPauseInterval   | Line 186     | Behavioral pause interval               |
| remap              | Line 273-287 | Key remap (Q→A, Numpad→Arrow, etc)      |

---

## 💡 **TIPS & TRICKS - 1 HOST to N SLAVES:**

### **1️⃣ Tìm VM Window Title Nhanh (Cho MASTER):**

```
┌──────────────────────────────────────────────────────────────┐
│  CÁCH DỄ NHẤT:                                               │
│  1. Chạy Master script                                       │
│  2. Ấn Ctrl+Alt+L                                            │
│  3. Popup hiện TẤT CẢ VMware windows                         │
│  4. Copy → Paste vào vmList (Line 74-90)                     │
│                                                              │
│  💡 Tự động detect! Không cần manual tìm tên!                │
└──────────────────────────────────────────────────────────────┘
```

---

### **2️⃣ Scale lên N VMs Dễ Dàng:**

```
┌──────────────────────────────────────────────────────────────┐
│  MASTER (HOST):                                              │
│  → Thêm VM: vmList.Push("NEW-VM-NAME")                       │
│  → Bỏ VM:   ; vmList.Push("OLD-VM-NAME")  (thêm ; ở đầu)    │
│  → Location: Line 74-90                                      │
│                                                              │
│  SLAVE (TRONG MỖI VM):                                       │
│  → Chỉ cần sửa 2 số: MinDesync, MaxDesync                   │
│  → Dùng table ở BƯỚC 2 để chọn range                         │
│  → Location: Line 139-140                                    │
│                                                              │
│  💡 UNLIMITED VMs! Không giới hạn số lượng!                  │
└──────────────────────────────────────────────────────────────┘
```

---

### **3️⃣ Công Thức Desync Range Cho N VMs:**

```
┌──────────────────────────────────────────────────────────────┐
│  CÔNG THỨC ĐƠN GIẢN:                                         │
│                                                              │
│  VM(N):  MinDesync = (N-1) * 100 + random(0-50)             │
│          MaxDesync = MinDesync + 300                         │
│                                                              │
│  VÍ DỤ:                                                      │
│  • VM1:  Min=0,   Max=300    (0*100+0=0)                    │
│  • VM2:  Min=100, Max=400    (1*100+0=100)                  │
│  • VM3:  Min=200, Max=500    (2*100+0=200)                  │
│  • VM4:  Min=50,  Max=350    (0*100+50=50)                  │
│  • VM5:  Min=150, Max=450    (1*100+50=150)                 │
│  • VM6:  Min=250, Max=550    (2*100+50=250)                 │
│  ...                                                         │
│  • VM20: Min=420, Max=720    (19*100+20=1920→420)           │
│  • VM50: Min=1200,Max=1500   (49*100+random)                │
│                                                              │
│  💡 RULE: Mỗi VM cách nhau ít nhất 50ms!                     │
└──────────────────────────────────────────────────────────────┘
```

---

### **4️⃣ Thêm/Bớt Keys Broadcast (MASTER):**

```
┌──────────────────────────────────────────────────────────────┐
│  Location: Master script Line 110-170                        │
│                                                              │
│  THÊM KEY MỚI:                                               │
│  → Template: KEY::BroadcastKey("KEY")                        │
│  → VD: t::BroadcastKey("t")                                  │
│  → VD: Tab::BroadcastKey("Tab")                              │
│                                                              │
│  BỎ KEY:                                                     │
│  → Thêm ; ở đầu dòng                                         │
│  → VD: ; q::BroadcastKey("q")                                │
│                                                              │
│  💡 Slave sẽ tự động nhận keys mới từ Master!                │
└──────────────────────────────────────────────────────────────┘
```

---

### **5️⃣ Check Status Khi Running (1→N):**

```
┌──────────────────────────────────────────────────────────────┐
│  🖥️  MASTER (HOST):                                          │
│     Ctrl+Alt+S → Status (bao nhiêu VMs found/missing)        │
│     Ctrl+Alt+L → List all VMware windows                     │
│     Ctrl+Alt+D → Toggle debug tooltip                        │
│     Ctrl+Alt+B → Toggle beep                                 │
│     Ctrl+Alt+Q → Exit                                        │
│                                                              │
│  💻 SLAVE (MỖI VM):                                          │
│     Ctrl+Alt+T → Toggle ON/OFF script                        │
│                                                              │
│  💡 Check Master status để verify TẤT CẢ VMs đã connect!     │
└──────────────────────────────────────────────────────────────┘
```

---

## ❓ **TROUBLESHOOTING:**

### **Issue 1: Master không tìm thấy VMs**

**Triệu chứng:**

-   Ấn Ctrl+Alt+S → "Found: 0/5"

**Giải pháp:**

1. Ấn Ctrl+Alt+L để xem list VMs
2. So sánh với vmList trong script
3. Phải CHÍNH XÁC 100% (case-sensitive!)
4. Sửa lại vmList → Restart Master script

---

### **Issue 2: VMs không nhận input**

**Triệu chứng:**

-   Master broadcast OK
-   Slave script đang chạy
-   VM không nhận key

**Giải pháp:**

1. Check Slave script có chạy không (Ctrl+Alt+T để toggle)
2. Check remap table có key đó không
3. Check IsPaused (có thể đang pause)
4. Restart Slave script

---

### **Issue 3: Tất cả VMs cùng timing**

**Triệu chứng:**

-   Tất cả VMs phản hồi đồng thời

**Giải pháp:**

1. **QUAN TRỌNG:** Mỗi VM phải có desync range KHÁC NHAU!
2. Check MinDesync và MaxDesync trong mỗi VM
3. Phải khác nhau ít nhất 50-100ms
4. Xem table ở BƯỚC 2

---

### **Issue 4: Compile lỗi**

**Triệu chứng:**

-   Batch file báo lỗi

**Giải pháp:**

1. Check AutoHotkey đã cài chưa
2. Check đường dẫn compiler (Line 10 trong batch file)
3. Check syntax trong AHK script (có lỗi không)
4. Thử compile manual bằng Ahk2Exe GUI

---

## 🎉 **DONE!**

```
┌────────────────────────────────────────────┐
│                                            │
│  ✅ MASTER-SLAVE SETUP COMPLETE!           │
│                                            │
│  • FREE (no Multiplicity cost!)            │
│  • Unlimited VMs                           │
│  • Lower detection risk                    │
│  • Per-VM desync                           │
│  • Full control                            │
│                                            │
└────────────────────────────────────────────┘
```

---

## 📖 **NEXT STEPS:**

1. ✅ Test với 1-2 VMs trước
2. ✅ Verify desync works (mỗi VM delay khác nhau)
3. ✅ Scale lên all VMs
4. ✅ Setup autostart (optional):
    - HOST: Tạo shortcut WindowsTaskScheduler.exe vào Startup folder
    - VMs: Chạy setup_autostart_SLAVE.bat

---

## 📖 **QUICK REFERENCE - 1 HOST to N SLAVES:**

```
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃  📝 CUSTOMIZATION CHEAT SHEET                                ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛

┌──────────────────────────────────────────────────────────────┐
│  🖥️  MASTER SCRIPT (Setup 1 lần trên HOST):                  │
└──────────────────────────────────────────────────────────────┘

File: Master_Multi_VM_EASY_CUSTOM.ahk

┌────────────┬──────────┬─────────────────────────────────────┐
│ Setting    │ Location │ Mô tả                               │
├────────────┼──────────┼─────────────────────────────────────┤
│ vmList     │ 74-90    │ Tên VMs (thêm/bớt VMs ở đây)        │
│ Keys       │ 110-170  │ Phím broadcast (thêm/bớt keys)      │
│ Tooltip    │ 104      │ showDebugTooltip (true/false)       │
│ Beep       │ 107      │ enableBeep (true/false)             │
└────────────┴──────────┴─────────────────────────────────────┘

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────────────────────────────────────────────────┐
│  💻 SLAVE SCRIPT (Setup N lần, 1 cho mỗi VM):                │
└──────────────────────────────────────────────────────────────┘

File: multiplicity_jitter_DESYNC_SLAVE.ahk

┌─────────────────┬──────────┬──────────────────────────────┐
│ Setting         │ Location │ Mô tả                        │
├─────────────────┼──────────┼──────────────────────────────┤
│ MinDesync ⭐    │ 139      │ KHÁC NHAU MỖI VM! (0-2000)   │
│ MaxDesync ⭐    │ 140      │ KHÁC NHAU MỖI VM! (300-2300) │
│ ArrowJitter     │ 243      │ true/false (movement)        │
│ PauseInterval   │ 186-189  │ Behavioral pause (min-max)   │
│ Remap Table     │ 273-287  │ Key remap (Q→A, Numpad, etc) │
│ DISABLE_DESYNC  │ 152      │ Test mode (true/false)       │
│ DISABLE_JITTER  │ 153      │ Test mode (true/false)       │
└─────────────────┴──────────┴──────────────────────────────┘

⭐ = CRITICAL! PHẢI KHÁC NHAU CHO MỖI VM!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────────────────────────────────────────────────┐
│  🎯 DESYNC QUICK LOOKUP TABLE (COPY & PASTE):                │
└──────────────────────────────────────────────────────────────┘

VM1:  global MinDesync := 0    | global MaxDesync := 300
VM2:  global MinDesync := 100  | global MaxDesync := 400
VM3:  global MinDesync := 200  | global MaxDesync := 500
VM4:  global MinDesync := 50   | global MaxDesync := 350
VM5:  global MinDesync := 150  | global MaxDesync := 450
VM6:  global MinDesync := 250  | global MaxDesync := 550
VM7:  global MinDesync := 80   | global MaxDesync := 380
VM8:  global MinDesync := 180  | global MaxDesync := 480
VM9:  global MinDesync := 120  | global MaxDesync := 420
VM10: global MinDesync := 220  | global MaxDesync := 520

Formula cho VM > 10:
  MinDesync = (N-1) * 100 + random(0-50)
  MaxDesync = MinDesync + 300

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────────────────────────────────────────────────┐
│  ⌨️  HOTKEYS (Khi scripts đang chạy):                        │
└──────────────────────────────────────────────────────────────┘

MASTER (HOST):
  • Ctrl+Alt+S → Status (N/N VMs found?)
  • Ctrl+Alt+L → List VMware windows (auto-detect tên VMs!)
  • Ctrl+Alt+D → Toggle debug tooltip
  • Ctrl+Alt+B → Toggle beep
  • Ctrl+Alt+Q → Exit

SLAVE (VMs):
  • Ctrl+Alt+T → Toggle ON/OFF script

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

┌──────────────────────────────────────────────────────────────┐
│  🚀 WORKFLOW TÓM TẮT:                                        │
└──────────────────────────────────────────────────────────────┘

1. Setup Master (1 lần):
   → Sửa vmList (thêm tên VMs)
   → Compile (optional)
   → Chạy!

2. Setup Slave (N lần):
   → Copy file vào VM
   → Sửa MinDesync/MaxDesync (KHÁC NHAU MỖI VM!)
   → Compile
   → Chạy!

3. Test:
   → Master: Ctrl+Alt+S (check status)
   → Ấn phím → Tất cả VMs nhận → Mỗi VM delay khác nhau!

✅ DONE! FREE, Unlimited VMs, Lower detection risk!
```

---

**XEM CHI TIẾT:**

-   `MULTI_VM_SETUP_GUIDE.md` - Full setup guide
-   `VERSION_COMPARISON.md` - V1 vs V2 comparison
-   `FEATURE_CHECKLIST_V1_V2.md` - Feature parity check

**GOOD LUCK! 🚀**
