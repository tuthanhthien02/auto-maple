# 🚨 URGENT: Fix NGS Hacking Detected (0xD2020201) - Tránh Ban

## ⚠️ CẢNH BÁO NGHIÊM TRỌNG

**Lỗi này sẽ dẫn đến BAN sau 1 giờ nếu không fix!**

**Error Code:** `0xD2020201`  
**Nguyên nhân:** NGS phát hiện keyboard hooks, automation tools, hoặc processes đáng ngờ **TRƯỚC KHI hoặc TRONG KHI** game đang chạy.

---

## 🔴 NGUYÊN NHÂN CHÍNH

### **1. Keyboard Hooks Đang Chạy** ⚠️ CRITICAL

**Các scripts có keyboard hooks:**

-   `keyboard_to_arduino.py` - **Keyboard hook**
-   `keyboard_block_arduino.py` - **Keyboard hook**
-   `host_sender.py` - **Keyboard hook**
-   `vmware_receiver.py` - **Keyboard hook**

**Vấn đề:**

-   NGS **PHÁT HIỆN** keyboard hooks ngay cả khi bot chưa chạy
-   Hooks đang chạy trong background → NGS detect → Crash game → Ban

### **2. Python Processes Đang Chạy** ⚠️ HIGH RISK

-   Python processes có thể bị NGS scan
-   Processes từ lần chạy trước không được kill
-   NGS có thể detect Python processes và scan project folder

### **3. Bot Process Đang Chạy** ⚠️ HIGH RISK

-   `ExplorerSettings.exe` đang chạy khi start game
-   NGS scan process → detect bot → crash

### **4. VMware Traces** ⚠️ MEDIUM RISK (nếu đang dùng VM)

-   VMware processes/services đang chạy
-   Hardware traces (ACPI keyboard, VMware mouse)

---

## ✅ GIẢI PHÁP KHẮC PHỤC NGAY

### **BƯỚC 1: Kill TẤT CẢ Processes TRƯỚC KHI Start Game** 🔴 CRITICAL

**Chạy script tự động:**

```bash
kill_all_before_game.bat
```

**Hoặc manual:**

```bash
REM Kill Python processes
taskkill /F /IM python.exe
taskkill /F /IM pythonw.exe

REM Kill bot
taskkill /F /IM ExplorerSettings.exe

REM Kill AutoHotkey
taskkill /F /IM autohotkey.exe
taskkill /F /IM autohotkeyu64.exe

REM Verify
tasklist | findstr /I "python ExplorerSettings autohotkey"
```

### **BƯỚC 2: Verify Không Có Processes**

**Check processes đang chạy:**

```bash
check_ngs_processes.bat
```

**Nếu có processes → Kill tất cả:**

```bash
kill_ngs_processes.bat
```

### **BƯỚC 3: Start Game ĐÚNG CÁCH**

**Workflow ĐÚNG:**

```
1. ✅ Kill ALL processes (kill_all_before_game.bat)
2. ✅ Verify no processes (check_ngs_processes.bat)
3. ✅ Start MapleStory
4. ✅ Wait for game FULLY loaded (character select screen)
5. ✅ Start bot (ExplorerSettings.exe) SAU KHI game loaded
```

**Workflow SAI (SẼ BỊ DETECT):**

```
❌ Start bot → Start game (SAI!)
❌ Start game → Immediately start bot (SAI!)
❌ Start game khi có keyboard hooks đang chạy (SAI!)
```

### **BƯỚC 4: Stop Bot ĐÚNG CÁCH**

**Khi muốn dừng:**

```
1. Press Insert (stop bot)
2. Close bot GUI
3. Kill ALL processes (kill_all_before_game.bat)
4. Close game
```

---

## 🛡️ WORKFLOW AN TOÀN (NÊN LÀM)

### **Mỗi Lần Chơi:**

```batch
REM 1. Kill ALL processes
kill_all_before_game.bat

REM 2. Verify
check_ngs_processes.bat

REM 3. Start game
REM (Double-click MapleStory shortcut)

REM 4. WAIT for game fully loaded
REM (Character select screen visible)

REM 5. Start bot
REM (Double-click ExplorerSettings.exe)
```

### **Khi Dừng Chơi:**

```batch
REM 1. Press Insert (stop bot)
REM 2. Close bot GUI
REM 3. Kill ALL processes
kill_all_before_game.bat

REM 4. Close game
```

---

## 🚨 QUAN TRỌNG NHẤT

### **NGUYÊN TẮC VÀNG:**

1. **KHÔNG BAO GIỜ** start bot trước khi start game
2. **KHÔNG BAO GIỜ** để keyboard hooks chạy khi không cần
3. **LUÔN** kill tất cả processes TRƯỚC KHI start game
4. **LUÔN** verify không có processes trước khi start game
5. **LUÔN** start bot SAU KHI game đã fully loaded
6. **NÊN COMPILE BOT** - Bot chưa compile (Python script) có thể bị NGS detect như automation tool

### **KIỂM TRA TRƯỚC MỖI LẦN CHƠI:**

```bash
# Check processes
tasklist | findstr /I "python ExplorerSettings autohotkey"

# Nếu có output → KHÔNG start game!
# Kill tất cả trước:
kill_all_before_game.bat
```

---

## 📋 CHECKLIST TRƯỚC MỖI LẦN CHƠI

### **Before Starting Game:**

-   [ ] **1. Kill ALL processes**

    ```bash
    kill_all_before_game.bat
    ```

-   [ ] **2. Verify no processes**

    ```bash
    tasklist | findstr /I "python ExplorerSettings autohotkey"
    ```

    Output phải **RỖNG**!

-   [ ] **3. Check keyboard hooks**

    ```bash
    check_ngs_processes.bat --check-registry
    ```

-   [ ] **4. Start game**

    -   Double-click MapleStory shortcut
    -   **WAIT** for game fully loaded

-   [ ] **5. Start bot SAU KHI game loaded**
    -   Double-click ExplorerSettings.exe
    -   Verify bot initialized correctly

### **After Closing Game:**

-   [ ] **1. Stop bot**

    -   Press Insert
    -   Close bot GUI

-   [ ] **2. Kill ALL processes**

    ```bash
    kill_all_before_game.bat
    ```

-   [ ] **3. Close game**
    -   Close MapleStory

---

## 🔧 NẾU VẪN BỊ DETECT

### **Additional Checks:**

1. **Check Registry:**

```bash
check_ngs_processes.bat --check-registry
```

2. **Rename Folder:**

```
auto-maple → ExplorerSettings
```

3. **Move Folder:**

```
C:\Users\...\auto-maple
→ C:\Program Files\ExplorerSettings
```

4. **Check VMware Stealth (nếu dùng VM):**

```bash
check_vmware_stealth.bat
```

5. **Disable VMware Services:**

```bash
fix_vmware_stealth.bat
```

---

## ⚠️ KHÔNG BAO GIỜ LÀM

1. ❌ **KHÔNG** start bot trước khi start game
2. ❌ **KHÔNG** để keyboard hooks chạy khi không cần
3. ❌ **KHÔNG** start game khi có Python processes đang chạy
4. ❌ **KHÔNG** start game khi có bot process đang chạy
5. ❌ **KHÔNG** để AutoHotkey scripts chạy
6. ❌ **KHÔNG** để debugging tools chạy
7. ❌ **KHÔNG** để VMware processes/services chạy (nếu dùng VM)

---

## 🎯 TÓM TẮT

**Nguyên nhân chính:** Keyboard hooks và processes đang chạy khi start game

**Fix ngay:**

1. ✅ Kill ALL processes TRƯỚC KHI start game
2. ✅ Verify không có processes
3. ✅ Start game
4. ✅ WAIT for game fully loaded
5. ✅ Start bot SAU KHI game loaded

**Quan trọng nhất:**

-   ✅ **LUÔN** kill processes trước khi start game
-   ✅ **KHÔNG BAO GIỜ** start bot trước khi start game
-   ✅ **LUÔN** verify không có processes

---

## 📝 SCRIPT TỰ ĐỘNG

Đã tạo các scripts để tự động kill tất cả processes:

### **Scripts Available:**

1. **`kill_all_before_game.bat`** - Kill processes trước khi start game
2. **`kill_all_before_bot.bat`** - Kill processes trước khi start bot (NEW)
3. **`kill_ngs_processes.bat`** - Kill processes với Python script (NEW)
4. **`kill_ngs_processes.py`** - Python script kill processes (NEW)

**Cách dùng:**

```batch
REM Option 1: Before starting game
kill_all_before_game.bat

REM Option 2: Before starting bot (recommended)
kill_all_before_bot.bat

REM Option 3: Using Python script directly
python kill_ngs_processes.py
```

**Workflow:**

1. Double-click `kill_all_before_bot.bat`
2. Verify output: "READY TO START BOT"
3. Start game
4. Wait for game fully loaded
5. Start bot (ExplorerSettings.exe if compiled, or python main.py if not compiled)

---

## ⚠️ **BOT CHƯA COMPILE - NGS DETECTION RISK**

**Bot chưa compile (Python script) có thể bị NGS detect:**

-   ⚠️ **Process name:** `python.exe` → NGS có thể detect như automation tool
-   ⚠️ **Command line:** `python main.py` → NGS có thể scan project folder
-   ⚠️ **Project folder:** NGS có thể scan và detect `.py` files

**Khuyến nghị:**

1. ✅ **Compile bot** để giảm detection risk
2. ✅ **Use compiled executable** (`ExplorerSettings.exe`) thay vì Python script
3. ✅ **Kill Python processes** trước khi start bot

**Xem chi tiết:** `BOT_COMPILE_NGS_RISK.md`

---

**REMEMBER:** Nếu không fix, game sẽ bị ban sau 1 giờ! ⚠️
