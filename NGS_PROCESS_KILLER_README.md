# 🛡️ NGS Process Killer - Kill Processes Trước Khi Chạy Bot

## 📋 **TỔNG QUAN**

Scripts để kill tất cả processes có thể trigger NGS detection **TRƯỚC KHI** start bot.

**Mục đích:** Tránh NGS detection bằng cách kill các processes đáng ngờ trước khi start bot.

---

## 🚀 **SCRIPTS CÓ SẴN**

### **1. `kill_ngs_processes.py`** ⭐ RECOMMENDED

**Python script** kill tất cả sensitive processes.

**Features:**

-   ✅ Scan và kill tất cả sensitive processes
-   ✅ Kill theo category (vmware, keyboard_hooks, etc.)
-   ✅ Verify không có processes còn lại
-   ✅ Detailed reporting

**Usage:**

```bash
# Kill all processes
python kill_ngs_processes.py

# Kill by category
python kill_ngs_processes.py --category keyboard_hooks

# Check only (no kill)
python kill_ngs_processes.py --check-only

# List categories
python kill_ngs_processes.py --list-categories
```

---

### **2. `kill_ngs_processes.bat`**

**Batch script wrapper** cho `kill_ngs_processes.py`.

**Usage:**

```batch
kill_ngs_processes.bat
```

**Features:**

-   ✅ Auto-run Python script
-   ✅ Fallback method nếu Python script fail
-   ✅ Verification

---

### **3. `kill_all_before_bot.bat`** ⭐ RECOMMENDED

**Batch script** kill processes trước khi start bot.

**Usage:**

```batch
kill_all_before_bot.bat
```

**Features:**

-   ✅ Kill tất cả sensitive processes
-   ✅ Verify không có processes còn lại
-   ✅ Workflow instructions

---

### **4. `kill_all_before_game.bat`**

**Batch script** kill processes trước khi start game.

**Usage:**

```batch
kill_all_before_game.bat
```

**Features:**

-   ✅ Kill tất cả sensitive processes
-   ✅ Verify không có processes còn lại
-   ✅ Workflow instructions

---

## 📋 **PROCESSES ĐƯỢC KILL**

### **Categories:**

1. **VM Processes:**

    - VMware (`vmware.exe`, `vmwaretray.exe`, etc.)
    - VirtualBox (`virtualbox.exe`, `vboxsvc.exe`, etc.)
    - LDPlayer, Nox, BlueStacks, MEmu

2. **Keyboard Hooks:**

    - `keyboard_to_arduino.py`
    - `keyboard_block_arduino.py`
    - `host_sender.py`
    - `vmware_receiver.py`
    - `python.exe` (nếu chạy keyboard hooks)

3. **Automation Tools:**

    - AutoHotkey (`autohotkey.exe`, `ahk.exe`)
    - Key remapping tools
    - Virtual keyboard tools

4. **Debugging Tools:**

    - Cheat Engine (`cheatengine.exe`)
    - Debuggers (`x64dbg.exe`, `ollydbg.exe`, etc.)
    - IDA Pro (`ida.exe`, `ida64.exe`)

5. **Other:**
    - Screen capture tools
    - Process injection tools
    - Remote desktop tools

---

## 🎯 **WORKFLOW**

### **Before Starting Bot:**

```batch
REM Step 1: Kill all processes
kill_all_before_bot.bat

REM Step 2: Verify no processes
python check_ngs_processes.py --brief

REM Step 3: Start game
REM (Double-click MapleStory shortcut)

REM Step 4: Wait for game fully loaded
REM (Character select screen visible)

REM Step 5: Start bot
REM (Double-click ExplorerSettings.exe if compiled)
REM (Or: python main.py if not compiled)
```

---

## ⚠️ **QUAN TRỌNG**

### **Bot Chưa Compile:**

-   ⚠️ **Process name:** `python.exe` → NGS có thể detect
-   ⚠️ **Command line:** `python main.py` → NGS có thể scan project folder
-   ⚠️ **Project folder:** NGS có thể scan và detect `.py` files

**Khuyến nghị:**

1. ✅ **Compile bot** để giảm detection risk
2. ✅ **Use compiled executable** (`ExplorerSettings.exe`)
3. ✅ **Kill Python processes** trước khi start bot

**Xem chi tiết:** `BOT_COMPILE_NGS_RISK.md`

---

## 🔧 **ADVANCED USAGE**

### **Kill by Category:**

```bash
# Kill only VMware processes
python kill_ngs_processes.py --category vmware

# Kill only keyboard hooks
python kill_ngs_processes.py --category keyboard_hooks

# Kill only automation tools
python kill_ngs_processes.py --category automation
```

### **Check Only:**

```bash
# Check without killing
python kill_ngs_processes.py --check-only

# Brief report
python check_ngs_processes.py --brief
```

---

## 📊 **OUTPUT EXAMPLE**

```
======================================================================
NGS PROCESS KILLER - Killing ALL sensitive processes
======================================================================

[1/3] Scanning for sensitive processes...
⚠️  Found 3 sensitive process(es):
   • keyboard_hooks: 1 process(es)
   • automation: 2 process(es)

[2/3] Killing 3 process(es)...

   Killing PID   1234: python.exe (keyboard_hooks)
   ✅ Killed PID 1234: python.exe
   Killing PID   5678: autohotkey.exe (automation)
   ✅ Killed PID 5678: autohotkey.exe
   Killing PID   9012: autohotkeyu64.exe (automation)
   ✅ Killed PID 9012: autohotkeyu64.exe

[3/3] Kill summary:
   ✅ Killed: 3
   ❌ Failed: 0

Verifying no sensitive processes remain...
✅ All sensitive processes killed successfully!

======================================================================
✅ READY TO START BOT
======================================================================

Safe to start bot now.
```

---

## 🚨 **TROUBLESHOOTING**

### **Some Processes Fail to Kill:**

**Nguyên nhân:**

-   Không có quyền Administrator
-   Process đang được protect bởi system

**Giải pháp:**

1. Run script as Administrator
2. Kill processes manually từ Task Manager
3. Restart computer nếu cần

### **Python Script Not Found:**

**Nguyên nhân:**

-   `check_ngs_processes.py` không có trong cùng folder

**Giải pháp:**

1. Đảm bảo `check_ngs_processes.py` trong cùng folder
2. Hoặc dùng batch script fallback method

---

## 📝 **RELATED DOCUMENTS**

-   `URGENT_NGS_FIX.md` - Hướng dẫn fix NGS detection
-   `BOT_COMPILE_NGS_RISK.md` - Phân tích bot chưa compile
-   `ARDUINO_DETECTION_RISK.md` - Phân tích Arduino detection risk
-   `check_ngs_processes.py` - Script check processes

---

## ✅ **CHECKLIST**

### **Before Starting Bot:**

-   [ ] Kill all processes (`kill_all_before_bot.bat`)
-   [ ] Verify no processes (`check_ngs_processes.py --brief`)
-   [ ] Start game
-   [ ] Wait for game fully loaded
-   [ ] Start bot (compiled executable recommended)

---

**REMEMBER:** Luôn kill processes trước khi start bot để tránh NGS detection! ⚠️
