# NGS Sensitive Processes Checker

## 📋 Mục Đích

Script để check và kill các process nhạy cảm có khả năng trigger NGS detection, bao gồm:

-   Virtual Machines (VMware, VirtualBox, LDPlayer, etc.)
-   Keyboard Hooks (keyboard_to_arduino, host_sender, etc.)
-   Automation Tools (AutoHotkey, etc.)
-   Debugging Tools (Cheat Engine, x64dbg, etc.)
-   Screen Capture Tools (OBS, Fraps, etc.)
-   Remote Desktop Tools (TeamViewer, AnyDesk, etc.)

---

## 🚀 Cách Sử Dụng

### **1. Check Processes (Không Kill)**

```bash
# Windows
check_ngs_processes.bat

# Hoặc Python trực tiếp
python check_ngs_processes.py
```

**Output:**

```
============================================================
NGS SENSITIVE PROCESSES SCAN REPORT
============================================================

⚠️  Found 3 sensitive process(es) that might trigger NGS detection:

📁 Vmware (2 process(es)):
----------------------------------------------------------------------
  • PID:   1234 | vmware.exe
    Path: C:\Program Files\VMware\VMware Workstation\vmware.exe
    Matched: vmware.exe

  • PID:   5678 | vmwareuser.exe
    Path: C:\Program Files\VMware\VMware Workstation\vmwareuser.exe
    Matched: vmwareuser.exe

📁 Keyboard Hooks (1 process(es)):
----------------------------------------------------------------------
  • PID:   9012 | python.exe
    Cmdline: python keyboard_to_arduino.py
    Matched: keyboard_to_arduino.py

============================================================
⚠️  WARNING: These processes might trigger NGS detection!
   Recommendation: Close these processes before starting game.
============================================================
```

---

### **2. Kill Processes (Với Confirmation)**

```bash
# Windows
kill_ngs_processes.bat

# Hoặc Python trực tiếp
python check_ngs_processes.py --kill
```

**Output:**

```
⚠️  WARNING: About to kill 3 process(es):
  • PID 1234: vmware.exe
  • PID 5678: vmwareuser.exe
  • PID 9012: python.exe

Continue? (yes/no): yes
✅ Killed PID 1234: vmware.exe
✅ Killed PID 5678: vmwareuser.exe
✅ Killed PID 9012: python.exe

✅ Killed 3 process(es).
```

---

### **3. Kill Tất Cả (Không Confirmation)**

```bash
python check_ngs_processes.py --kill-all
```

⚠️ **WARNING:** Sẽ kill tất cả processes mà không hỏi!

---

### **4. Kill Theo Category**

```bash
# Chỉ kill VMware processes
python check_ngs_processes.py --kill --category vmware

# Chỉ kill keyboard hooks
python check_ngs_processes.py --kill --category keyboard_hooks

# Chỉ kill VirtualBox
python check_ngs_processes.py --kill --category virtualbox
```

---

### **5. Brief Report (Không Chi Tiết)**

```bash
python check_ngs_processes.py --brief
```

**Output:**

```
============================================================
NGS SENSITIVE PROCESSES SCAN REPORT
============================================================

⚠️  Found 3 sensitive process(es) that might trigger NGS detection:

📁 Vmware (2 process(es)):
----------------------------------------------------------------------
  • PID:   1234 | vmware.exe
  • PID:   5678 | vmwareuser.exe

📁 Keyboard Hooks (1 process(es)):
----------------------------------------------------------------------
  • PID:   9012 | python.exe

============================================================
⚠️  WARNING: These processes might trigger NGS detection!
   Recommendation: Close these processes before starting game.
============================================================
```

---

### **6. List Categories**

```bash
python check_ngs_processes.py --list-categories
```

**Output:**

```
Available categories:
  • vmware
  • virtualbox
  • vbox
  • ldplayer
  • nox
  • bluestacks
  • memu
  • keyboard_hooks
  • automation
  • debugging
  • screen_capture
  • injection
  • remote
  • other
```

---

## 📁 Categories

### **Virtual Machines:**

-   `vmware` - VMware Workstation/Player
-   `virtualbox` - VirtualBox
-   `vbox` - VirtualBox (alternative)
-   `ldplayer` - LDPlayer emulator
-   `nox` - Nox emulator
-   `bluestacks` - BlueStacks emulator
-   `memu` - MEmu emulator

### **Keyboard Hooks:**

-   `keyboard_hooks` - Python scripts using keyboard hooks
    -   `keyboard_to_arduino.py`
    -   `keyboard_block_arduino.py`
    -   `host_sender.py`
    -   `vmware_receiver.py`

### **Automation:**

-   `automation` - Automation tools
    -   AutoHotkey

### **Debugging:**

-   `debugging` - Debugging/Reverse Engineering tools
    -   Cheat Engine
    -   x64dbg, x32dbg
    -   IDA Pro
    -   Wireshark, Fiddler

### **Screen Capture:**

-   `screen_capture` - Screen recording tools
    -   OBS
    -   Fraps, Bandicam
    -   Action!

### **Injection:**

-   `injection` - Process injection tools
    -   Process Hacker
    -   Process Explorer

### **Remote:**

-   `remote` - Remote desktop tools
    -   TeamViewer
    -   AnyDesk
    -   VNC

### **Other:**

-   `other` - Other suspicious tools
    -   Sandboxie

---

## ⚙️ Installation

### **1. Install Dependencies:**

```bash
pip install psutil
```

Hoặc nếu đã có `requirements.txt`:

```bash
pip install -r requirements.txt
```

### **2. Make Scripts Executable (Optional):**

```bash
# Windows - Already executable (.bat files)
# Linux/Mac:
chmod +x check_ngs_processes.py
```

---

## 🎯 Workflow Recommended

### **Before Starting Game:**

1. **Check processes:**

    ```bash
    check_ngs_processes.bat
    ```

2. **Kill processes nếu cần:**

    ```bash
    kill_ngs_processes.bat
    ```

3. **Start game**

### **After Closing Game:**

1. **Start bot (nếu cần)**

2. **Kill processes khi done:**
    ```bash
    kill_ngs_processes.bat
    ```

---

## ⚠️ Notes

1. **Kill processes có thể:**

    - Mất dữ liệu chưa save
    - Close các ứng dụng đang chạy
    - Cần admin privileges cho một số processes

2. **Python processes:**

    - Chỉ flag Python processes đang chạy keyboard hooks
    - Không flag các Python processes khác

3. **VMware/VirtualBox:**
    - Nếu đang dùng VM → KHÔNG kill
    - Chỉ kill khi không dùng VM

---

## 📝 Examples

### **Example 1: Check Before Game**

```bash
python check_ngs_processes.py
```

### **Example 2: Kill Keyboard Hooks Only**

```bash
python check_ngs_processes.py --kill --category keyboard_hooks
```

### **Example 3: Kill All Without Confirmation**

```bash
python check_ngs_processes.py --kill-all
```

---

## 🔧 Troubleshooting

### **Error: psutil not found**

```bash
pip install psutil
```

### **Error: Access Denied**

-   Run as Administrator
-   Some processes require admin privileges to kill

### **Error: Process not found**

-   Process đã được kill bởi process khác
-   Process đã tự động exit

---

## 📊 Summary

**Script này giúp:**

-   ✅ Check processes nhạy cảm
-   ✅ Kill processes có thể trigger NGS
-   ✅ Workflow dễ dàng trước khi start game

**Sử dụng:**

1. Check → Kill → Start game
2. Kill sau khi done
