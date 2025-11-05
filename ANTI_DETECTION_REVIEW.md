# 🛡️ Anti-Detection Codebase Review - Liệt Kê Điểm Cần Xem Xét

## 📋 Tổng Quan

Đây là review tổng hợp về các tính năng anti-detection trong codebase trước khi chạy bot. **KHÔNG IMPLEMENT**, chỉ liệt kê các điểm cần kiểm tra và cân nhắc.

---

## ✅ CÁC TÍNH NĂNG ĐÃ CÓ SẴN

### 1. **Anti-Detect Core** (`src/common/anti_detect.py`)

**Trạng thái:** ✅ Đã implement và ENABLED

**Tính năng:**

-   ✅ Timing randomization với Gaussian distribution
-   ✅ Pattern diversification (5% skip key, 2% add random key)
-   ✅ Memory optimization (cleanup mỗi 5 phút)
-   ✅ Human-like delays với variance multipliers
-   ✅ Typing pattern simulation
-   ❌ Behavioral simulation DISABLED (AFK, pauses, mistakes)
-   ❌ Typing mistakes DISABLED

**Điểm cần xem xét:**

-   ✅ Timing randomization đang hoạt động tốt
-   ✅ Pattern diversification có thể giúp tránh detection
-   ⚠️ Behavioral simulation đã TẮT hoàn toàn (có thể là tốt để tránh unexpected behavior)
-   ⚠️ Memory cleanup mỗi 5 phút có thể ảnh hưởng performance nếu quá thường xuyên

---

### 2. **Process Stealth** (`src/common/process_stealth.py`)

**Trạng thái:** ✅ Đã implement và ENABLED trong `bot.py` (line 79-82)

**Tính năng:**

-   ✅ Hide console window
-   ✅ Minimize memory footprint
-   ✅ Obfuscate memory patterns (tạo noise)
-   ✅ Process monitoring (check memory/CPU mỗi 30 giây)
-   ⚠️ Process name change - CHỈ là placeholder (không thực sự đổi tên)
-   ❌ Hide from Task Manager - KHÔNG implement (Windows security restrictions)

**Điểm cần xem xét:**

-   ✅ Console hiding hoạt động tốt
-   ✅ Memory minimization giúp giảm footprint
-   ⚠️ Process name change KHÔNG hoạt động (chỉ print message)
-   ⚠️ Memory obfuscation tạo noise nhưng có thể không hiệu quả với NGS
-   ⚠️ Process monitoring có thể spam logs nếu memory/CPU cao

---

### 3. **Screenshot Blocking** (`src/common/screenshot_blocker.py`)

**Trạng thái:** ❌ DISABLED trong `bot.py` (line 84-90 đã comment)

**Tính năng:**

-   ❌ Block Print Screen - KHÔNG implement (chỉ print message)
-   ❌ Block Snipping Tool - Có kill process nhưng cần quyền admin
-   ❌ Block third-party tools - Có kill process nhưng cần quyền admin
-   ❌ Window protection - KHÔNG implement
-   ❌ API hooking - KHÔNG implement (Windows PatchGuard ngăn cản)

**Điểm cần xem xét:**

-   ❌ Tính năng này **KHÔNG hoạt động** và đã bị DISABLE
-   ⚠️ Nếu enable, sẽ cần quyền admin để kill processes
-   ⚠️ API hooking KHÔNG thể implement trên Windows hiện đại
-   ✅ Tốt là đã disable để tránh conflicts

---

### 4. **Routine Randomization** (`src/common/routine_randomization.py`)

**Trạng thái:** ✅ Đã implement và ENABLED trong `bot.py` (line 76)

**Tính năng:**

-   ✅ Point selection randomization (10% skip probability)
-   ✅ Routine pattern variants (normal, reverse, floor1_only, floor2_only)
-   ✅ Variant switching (15% chance sau mỗi loop)
-   ✅ Minimum loops before switch (3 loops)
-   ✅ Never skip labels/jumps/transitions

**Điểm cần xem xét:**

-   ✅ Randomization giúp tránh pattern detection
-   ⚠️ Skip probability 10% có thể làm bot miss điểm quan trọng
-   ⚠️ Variant switching có thể làm bot behavior không nhất quán
-   ✅ An toàn là không skip labels/jumps/transitions

---

### 5. **Anti-Detect Config** (`src/common/anti_detect_config.py`)

**Trạng thái:** ✅ Đã có config chi tiết

**Điểm cần xem xét:**

-   ✅ Timing randomization: ENABLED với Gaussian distribution
-   ❌ Behavioral simulation: DISABLED (AFK, pauses, mistakes)
-   ✅ Pattern diversification: ENABLED
-   ✅ Memory optimization: ENABLED
-   ✅ Mouse anti-detect: ENABLED (jitter, delays)
-   ✅ Keyboard anti-detect: ENABLED (micro pauses, variation)
-   ❌ Process stealth: DISABLED by default (requires admin)
-   ✅ Advanced features: ENABLED (human-like rhythm, time-based patterns)
-   ❌ Fatigue simulation: DISABLED
-   ❌ Learning adaptation: DISABLED

---

### 6. **VMware Stealth Checker** (`check_vmware_stealth.py`)

**Trạng thái:** ✅ Script check độc lập

**Tính năng:**

-   ✅ Check VMware processes
-   ✅ Check VMware registry keys
-   ✅ Check VMware services
-   ✅ Check VMware device drivers
-   ✅ Check hardware traces (VID/PID)
-   ✅ Check VM detection signatures

**Điểm cần xem xét:**

-   ✅ Script tốt để verify VM stealth trước khi chạy bot
-   ⚠️ Cần chạy TRƯỚC KHI start game để đảm bảo VM stealth
-   ⚠️ HIGH RISK issues = VMware processes/services đang chạy
-   ⚠️ LOW RISK warnings = Registry keys (không thể xóa được)

---

### 7. **NGS Process Checker** (`check_ngs_processes.py`)

**Trạng thái:** ✅ Script check độc lập

**Tính năng:**

-   ✅ Check sensitive processes (VM, keyboard hooks, automation tools)
-   ✅ Check registry for keyboard simulation
-   ✅ Kill processes (optional)
-   ✅ Category-based filtering

**Điểm cần xem xét:**

-   ✅ Script tốt để check processes TRƯỚC KHI start game
-   ⚠️ **QUAN TRỌNG:** Phải kill keyboard hooks TRƯỚC KHI start game
-   ⚠️ Python processes có thể bị detect nếu đang chạy keyboard hooks
-   ⚠️ Registry checks có thể phát hiện Scancode Map (key remapping)

---

## ⚠️ CÁC VẤN ĐỀ QUAN TRỌNG CẦN XEM XÉT

### 1. **Keyboard Hooks Detection** 🔴 HIGH PRIORITY

**Vấn đề:**

-   NGS có thể detect keyboard hooks ngay cả khi bot chưa chạy
-   Các scripts: `keyboard_to_arduino.py`, `keyboard_block_arduino.py`, `host_sender.py`, `vmware_receiver.py`

**Giải pháp:**

-   ✅ **BẮT BUỘC:** Kill tất cả keyboard hooks TRƯỚC KHI start game
-   ✅ Chạy `check_ngs_processes.bat` hoặc `kill_ngs_processes.bat`
-   ✅ Chỉ start bot SAU KHI game đã start hoàn toàn

**Workflow:**

```
1. Kill all processes → check_ngs_processes.bat
2. Start game (MapleStory)
3. Wait for game fully loaded
4. Start bot (ExplorerSettings.exe)
```

---

### 2. **VMware Stealth** 🔴 HIGH PRIORITY

**Vấn đề:**

-   VM có thể bị detect qua processes, services, hardware traces
-   ACPI keyboard (không có VID/PID) = VM signature
-   VMware mouse VID/PID = VM fingerprint

**Giải pháp:**

-   ✅ **BẮT BUỘC:** Chạy `check_vmware_stealth.py` TRƯỚC KHI start game
-   ✅ Disable VMware services (services.msc)
-   ✅ Disable VMware Tools features
-   ✅ **QUAN TRỌNG:** Dùng Arduino HID Keyboard (hardware thật, có VID/PID)
-   ✅ Pass-through physical mouse vào VM

**Workflow:**

```
1. Check VM stealth → check_vmware_stealth.bat
2. Fix HIGH RISK issues (disable services, kill processes)
3. Restart VM
4. Verify stealth again
5. Start game
```

---

### 3. **Process Stealth Limitations** 🟡 MEDIUM PRIORITY

**Vấn đề:**

-   Process name change KHÔNG hoạt động (chỉ placeholder)
-   Hide from Task Manager KHÔNG thể implement (Windows security)
-   Process monitoring có thể spam logs

**Giải pháp:**

-   ⚠️ Không thể thay đổi process name runtime (cần build-time với PyInstaller)
-   ⚠️ Process name đã được set là "ExplorerSettings.exe" trong build (đã tốt)
-   ✅ Console hiding hoạt động tốt
-   ✅ Memory minimization hoạt động tốt

---

### 4. **Screenshot Blocking Disabled** 🟢 LOW PRIORITY

**Vấn đề:**

-   Screenshot blocking đã bị DISABLE
-   Tính năng này KHÔNG hoạt động (API hooking không thể implement)

**Giải pháp:**

-   ✅ **OK** để disable vì không hoạt động
-   ⚠️ Không thể block screenshot tools trên Windows hiện đại
-   ✅ NGS không quan tâm screenshot blocking

---

### 5. **Behavioral Simulation Disabled** 🟢 LOW PRIORITY

**Vấn đề:**

-   AFK simulation DISABLED
-   Behavioral pauses DISABLED
-   Typing mistakes DISABLED

**Điểm cần xem xét:**

-   ✅ **OK** để disable vì có thể làm bot behavior không nhất quán
-   ⚠️ Nếu enable, có thể giúp tránh detection nhưng có thể gây issues
-   ✅ Timing randomization đã đủ tốt

---

### 6. **Routine Randomization** 🟡 MEDIUM PRIORITY

**Vấn đề:**

-   10% skip probability có thể làm bot miss điểm quan trọng
-   Variant switching có thể làm bot behavior không nhất quán

**Điểm cần xem xét:**

-   ✅ Randomization giúp tránh pattern detection
-   ⚠️ Cần test kỹ để đảm bảo bot không miss điểm quan trọng
-   ✅ An toàn là không skip labels/jumps/transitions

---

### 7. **Arduino HID Keyboard** 🔴 HIGH PRIORITY

**Vấn đề:**

-   VM keyboard (ACPI) không có VID/PID = VM signature
-   NGS có thể detect VM qua hardware traces

**Giải pháp:**

-   ✅ **BẮT BUỘC:** Dùng Arduino HID Keyboard (hardware thật, có VID/PID)
-   ✅ Pass-through USB Arduino vào VM
-   ✅ Bot dùng Arduino output thay vì VM keyboard

**Setup:**

```
1. Connect Arduino vào VM (USB pass-through)
2. Upload arduino_hid_keyboard.ino
3. Bot dùng Arduino output
```

---

## 📊 CHECKLIST TRƯỚC KHI CHẠY BOT

### **Phase 1: Pre-Game Setup** 🔴 CRITICAL

-   [ ] **1. Check VMware Stealth**

    -   [ ] Chạy `check_vmware_stealth.bat`
    -   [ ] Fix HIGH RISK issues (disable services, kill processes)
    -   [ ] Restart VM
    -   [ ] Verify stealth again (should be PASS)

-   [ ] **2. Check NGS Processes**

    -   [ ] Chạy `check_ngs_processes.bat`
    -   [ ] Kill tất cả sensitive processes
    -   [ ] Verify no keyboard hooks running
    -   [ ] Verify no Python processes running

-   [ ] **3. Setup Hardware Stealth**
    -   [ ] Connect Arduino HID Keyboard vào VM
    -   [ ] Upload `arduino_hid_keyboard.ino`
    -   [ ] Pass-through physical mouse vào VM
    -   [ ] Check RawInputViewer để verify hardware (no VMware traces)

---

### **Phase 2: Game Startup** 🟡 IMPORTANT

-   [ ] **4. Start Game**

    -   [ ] Start MapleStory
    -   [ ] Wait for game fully loaded
    -   [ ] Verify game running smoothly

-   [ ] **5. Start Bot**
    -   [ ] Start bot SAU KHI game đã start hoàn toàn
    -   [ ] Verify bot initializes correctly
    -   [ ] Verify process stealth enabled (console hidden)
    -   [ ] Verify anti-detect features initialized

---

### **Phase 3: Runtime Monitoring** 🟢 MONITORING

-   [ ] **6. Monitor Bot**

    -   [ ] Monitor memory usage (should be < 500MB)
    -   [ ] Monitor CPU usage (should be < 50%)
    -   [ ] Check logs for any warnings/errors
    -   [ ] Verify routine randomization working

-   [ ] **7. Monitor Game**
    -   [ ] Monitor game performance
    -   [ ] Watch for any NGS warnings/errors
    -   [ ] Verify input from Arduino (not VM keyboard)

---

### **Phase 4: Cleanup** 🟡 IMPORTANT

-   [ ] **8. Stop Bot**

    -   [ ] Stop bot gracefully (Press Insert)
    -   [ ] Close bot GUI
    -   [ ] Verify bot process stopped

-   [ ] **9. Cleanup Processes**

    -   [ ] Chạy `kill_ngs_processes.bat`
    -   [ ] Verify no Python processes running
    -   [ ] Verify no keyboard hooks running

-   [ ] **10. Close Game**
    -   [ ] Close MapleStory
    -   [ ] Verify all processes cleaned up

---

## 🎯 KHUYẾN NGHỊ

### **Must Do (Before Running Bot):**

1. ✅ **Check VMware Stealth** - Đảm bảo VM không bị detect
2. ✅ **Kill Keyboard Hooks** - Tránh NGS detection
3. ✅ **Setup Arduino HID** - Hardware thật, không có VM traces
4. ✅ **Verify Processes** - Không có sensitive processes running

### **Should Do:**

1. ✅ **Test Routine Randomization** - Đảm bảo không miss điểm quan trọng
2. ✅ **Monitor Memory/CPU** - Đảm bảo bot không tốn quá nhiều resources
3. ✅ **Check Logs** - Monitor warnings/errors

### **Nice to Have:**

1. ✅ **Process Stealth** - Đã enable, console hiding hoạt động tốt
2. ✅ **Memory Optimization** - Đã enable, cleanup mỗi 5 phút
3. ✅ **Timing Randomization** - Đã enable, hoạt động tốt

---

## ⚠️ CÁC ĐIỂM CẦN LƯU Ý

### **1. Workflow Quan Trọng:**

```
❌ KHÔNG: Start bot → Start game
✅ ĐÚNG: Kill processes → Start game → Start bot
```

### **2. Keyboard Hooks:**

```
❌ KHÔNG: Để keyboard hooks chạy khi start game
✅ ĐÚNG: Kill tất cả hooks TRƯỚC KHI start game
```

### **3. VMware Stealth:**

```
❌ KHÔNG: Để VMware processes/services chạy
✅ ĐÚNG: Disable services, kill processes TRƯỚC KHI start game
```

### **4. Hardware Stealth:**

```
❌ KHÔNG: Dùng VM keyboard (ACPI, không có VID/PID)
✅ ĐÚNG: Dùng Arduino HID Keyboard (hardware thật, có VID/PID)
```

---

## 📝 SUMMARY

### **Tính Năng Hoạt Động Tốt:**

-   ✅ Timing randomization (ENABLED)
-   ✅ Pattern diversification (ENABLED)
-   ✅ Memory optimization (ENABLED)
-   ✅ Process stealth - Console hiding (ENABLED)
-   ✅ Routine randomization (ENABLED)
-   ✅ Mouse/Keyboard anti-detect (ENABLED)

### **Tính Năng Không Hoạt Động:**

-   ❌ Screenshot blocking (DISABLED, không hoạt động)
-   ❌ Process name change (placeholder only)
-   ❌ Hide from Task Manager (không thể implement)
-   ❌ Behavioral simulation (DISABLED by design)

### **Tính Năng Cần Setup Thủ Công:**

-   ⚠️ VMware stealth (cần disable services, kill processes)
-   ⚠️ Keyboard hooks cleanup (cần kill processes)
-   ⚠️ Arduino HID Keyboard (cần setup hardware)

---

## 🚀 NEXT STEPS

1. **Review checklist** ở trên
2. **Chạy các scripts check** để verify stealth
3. **Fix các HIGH RISK issues** nếu có
4. **Setup hardware** (Arduino HID Keyboard)
5. **Test bot** với game để verify không bị detect
6. **Monitor** bot runtime để đảm bảo stability

---

**Note:** Tất cả các điểm trên đều cần được kiểm tra và verify TRƯỚC KHI chạy bot trong production. Đặc biệt quan trọng là VMware stealth và keyboard hooks cleanup.
