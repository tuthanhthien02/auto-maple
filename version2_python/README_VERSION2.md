# 🐍 Version 2 - Python Implementation

## 📦 Folder Contents

This folder contains **Version 2** of the Multiplicity project, implemented using **Python 3.10+**.

---

## 📂 File Structure

| File                            | Purpose                                                    |
| ------------------------------- | ---------------------------------------------------------- |
| `multiplicity_master.py`        | Master script (Host) - Keyboard listener & TCP broadcaster |
| `multiplicity_slave.py`         | Slave script (VM) - TCP server & input processor           |
| `requirements_multiplicity.txt` | Python dependencies (pynput, colorama, etc.)               |
| `PYTHON_SETUP_GUIDE.md`         | Complete setup & configuration guide                       |
| `README_VERSION2.md`            | This file                                                  |

---

## 🚀 Quick Start

### STEP 1: Install Dependencies

```bash
cd version2_python
pip install -r requirements_multiplicity.txt
```

### STEP 2: Run Slave in VM

```bash
# In VM "bishop":
python multiplicity_slave.py

# Output:
# ============================================================
# 🎮 MULTIPLICITY SLAVE (Python Version)
# ============================================================
# TCP Port: 7001
# Desync Range: 0-500ms
# Jitter Range: 5-15ms
# Auto Pause: Enabled
# ============================================================
#
# [SLAVE] TCP Server running on 0.0.0.0:7001
# Waiting for Master commands...
```

### STEP 3: Run Master on Host

```bash
# On HOST:
python multiplicity_master.py

# Output:
# ============================================================
# 🎮 MULTIPLICITY MASTER (Python Version)
# ============================================================
# VMs configured: 1
#   • bishop: 127.0.0.1:7001
#
# Hotkeys:
#   Ctrl+Alt+T - Toggle Broadcasting
#   Ctrl+Alt+S - Show Status
#   Ctrl+Alt+P - Show Performance
#   Ctrl+Alt+Q - Quit
# ============================================================
#
# ✓ Listening for keyboard input...
# ✓ Press any key to broadcast to VMs
```

### STEP 4: Test!

1. Open Notepad in VM
2. Press `Q` on Host
3. See console output:
    ```
    [MASTER] KEYDOWN: q → ✅ 1/1 (2.5ms)
    [SLAVE] Received: KEYDOWN:q
    [SLAVE] Key: q → a
    ✓ Sent a DOWN (latency: 125.3ms)
    ```
4. Notepad shows "a" ✅

---

## ⚙️ Configuration

### 🔧 Slave Settings (multiplicity_slave.py)

```python
# Line 22: TCP Port (each VM uses different port)
TCP_PORT = 7001  # VM1: 7001, VM2: 7002, VM3: 7003

# Line 27-30: Desync delay (IMPORTANT: Each VM different!)
DESYNC_MIN = 0      # milliseconds
DESYNC_MAX = 500    # milliseconds

# Line 33-36: Arrow keys jitter
ARROW_KEYS_USE_JITTER = True
JITTER_MIN = 5
JITTER_MAX = 15
USE_GAUSSIAN = True  # Bell curve distribution

# Line 39-43: Auto pause (like human)
ENABLE_AUTO_PAUSE = True
PAUSE_INTERVAL_MIN = 20 * 60 * 1000  # 20 minutes
PAUSE_INTERVAL_MAX = 60 * 60 * 1000  # 60 minutes

# Line 46-62: Key remap (game-specific)
KEY_REMAP = {
    'q': 'a',  # Master sends Q → Slave sends A
    'w': 'w',
    'e': 'e',
    # Add more mappings...
}
```

### 🔧 Master Settings (multiplicity_master.py)

```python
# Line 20-25: VM configuration
VM_PORTS = {
    "bishop": 7001,  # VM 1
    "VM2": 7002,     # VM 2 (uncomment to enable)
    # Add more VMs as needed
}

# Line 27: VM Host (localhost for VMware on same PC)
VM_HOST = "127.0.0.1"

# Line 30: Enable/disable broadcasting
BROADCASTING_ENABLED = True

# Line 39-43: Keys to broadcast
KEYS_TO_BROADCAST = [
    'q', 'w', 'e', 'r', 't', ...
]

# Line 46: Arrow keys
ARROW_KEYS = ['up', 'down', 'left', 'right']
```

---

## 🎮 Hotkeys (Master)

| Hotkey       | Action                     |
| ------------ | -------------------------- |
| `Ctrl+Alt+T` | Toggle broadcasting ON/OFF |
| `Ctrl+Alt+S` | Show status (VMs, ports)   |
| `Ctrl+Alt+P` | Show performance stats     |
| `Ctrl+Alt+Q` | Quit                       |

---

## ✨ Key Features

### ✅ Master Script (Host):

-   ⌨️ **Keyboard listener** (pynput) - Non-blocking
-   🌐 **TCP Client** - Parallel broadcast to all VMs
-   🎛️ **Hotkeys** - Ctrl+Alt+... for control
-   📊 **Performance monitoring** - Success rate, latency
-   🐛 **Debug mode** - Colored console output
-   ⚡ **Threading** - Non-blocking operations

### ✅ Slave Script (VM):

-   🌐 **TCP Server** - Listens for Master commands
-   ⏱️ **Desync delay** - 0-500ms randomized (configurable)
-   🎲 **Jitter** - Gaussian distribution for arrow keys
-   🤖 **Auto pause** - 20-60min intervals (human-like)
-   🎹 **Key remapping** - Q→A, etc. (game-specific)
-   🔧 **Windows SendInput API** - ctypes (undetectable)
-   📊 **Performance stats** - Auto-display every 60s
-   🐛 **Colored output** - Green/Red/Yellow status

---

## 🐛 Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'pynput'"

```bash
pip install pynput
# or
pip install -r requirements_multiplicity.txt
```

### ❌ Slave: "Address already in use"

```bash
# Port 7001 already in use, kill process:
# Windows:
netstat -ano | findstr :7001
taskkill /F /PID <PID_NUMBER>

# Linux:
lsof -i :7001
kill -9 <PID>
```

### ❌ Master: "Connection refused"

```
1. Check Slave is running in VM
2. Check Firewall in VM (allow port 7001)
3. Verify port mapping: Master VM_PORTS matches Slave TCP_PORT
4. Test with telnet: telnet 127.0.0.1 7001
```

### ❌ Input not appearing in game

```
1. Check KEY_REMAP mapping
2. Run game as Administrator
3. Check if anti-cheat blocks SendInput
4. Test with Notepad first
```

---

## 📊 Performance Monitoring

### Master Performance (Ctrl+Alt+P)

```
============================================================
📊 PERFORMANCE STATS
============================================================
Total Sent: 1234
Success: 1230
Failed: 4
Avg Latency: 2.5ms
Success Rate: 99.7%
============================================================
```

### Slave Performance (Auto-display every 60s)

```
============================================================
📊 PERFORMANCE STATS
============================================================
Total Keypresses: 5678
Avg Latency: 125.3ms
Total Desync Time: 1234567ms
Total Jitter Time: 45678ms
============================================================
```

---

## 🚀 Advanced Features

### 🎯 Multi-VM Setup

```python
# multiplicity_master.py
VM_PORTS = {
    "bishop": 7001,
    "cleric": 7002,
    "warrior": 7003,
    "mage": 7004,
}
```

In each VM, set different ports:

```python
# VM1 (bishop): TCP_PORT = 7001
# VM2 (cleric): TCP_PORT = 7002
# VM3 (warrior): TCP_PORT = 7003
# VM4 (mage): TCP_PORT = 7004
```

### 🎲 Different Desync Ranges per VM

**IMPORTANT:** Each VM must use different ranges!

```python
# VM1 (bishop):
DESYNC_MIN = 0
DESYNC_MAX = 300

# VM2 (cleric):
DESYNC_MIN = 100
DESYNC_MAX = 400

# VM3 (warrior):
DESYNC_MIN = 200
DESYNC_MAX = 500

# VM4 (mage):
DESYNC_MIN = 300
DESYNC_MAX = 600
```

---

## ✅ Advantages over AHK Version

1. ✅ **Easier to read & maintain** - Python syntax is clearer
2. ✅ **Better error handling** - try/except blocks with detailed messages
3. ✅ **Cross-platform** - Works on Windows/Linux (with minor changes)
4. ✅ **Better logging** - Colored console output (colorama)
5. ✅ **Easier to extend** - Add AI/ML features later
6. ✅ **Package management** - pip install vs manual DLLs
7. ✅ **Better debugging** - Print statements, logging module
8. ✅ **Modern syntax** - List comprehensions, f-strings, type hints

---

## ⚠️ Disadvantages vs AHK

1. ⚠️ **Higher latency** - ~5-15ms vs ~2-5ms (AHK)
2. ⚠️ **Higher memory** - ~50MB vs ~10MB (AHK)
3. ⚠️ **More dependencies** - Requires Python + packages
4. ⚠️ **Slightly more detectable** - Python DLLs in memory
5. ⚠️ **Larger compiled size** - ~20-30MB vs ~1-2MB (AHK)

**BUT:** For TCP-based VM broadcasting, these disadvantages are negligible!

---

## 🎯 When to Use Version 2 (Python)

**Choose Python if:**

-   ✅ You want easier code maintenance
-   ✅ You need cross-platform support (Windows + Linux VMs)
-   ✅ You plan to add AI/ML features
-   ✅ You're comfortable with Python
-   ✅ Latency < 15ms is acceptable for your use case
-   ✅ You want better error messages and debugging

**Choose AHK (Version 1) if:**

-   ✅ You need absolute minimum latency (< 5ms)
-   ✅ You only use Windows
-   ✅ Maximum anti-detection is critical
-   ✅ Smallest memory footprint is needed

---

## 📌 Important Notes

1. ⚠️ **Each VM must use DIFFERENT desync ranges!**
2. ⚠️ **TCP ports must be unique per VM!**
3. ⚠️ **Test with Notepad before using in game!**
4. ✅ **Run scripts as normal user** (Admin not required for Python)

---

## 📚 Documentation

For detailed setup instructions, see:

-   `PYTHON_SETUP_GUIDE.md` - Complete guide
-   `../README_PROJECT_STRUCTURE.md` - Project overview
-   `../version1_ahk/README_VERSION1.md` - AHK version comparison

---

## 🔗 Dependencies

```
pynput>=1.7.6          # Keyboard listener
keyboard>=0.13.5       # Alternative keyboard library
pyautogui>=0.9.54      # GUI automation (backup)
psutil>=5.9.0          # Process monitoring
colorama>=0.4.6        # Colored console output
```

Install all:

```bash
pip install -r requirements_multiplicity.txt
```

---

**Created:** October 2025  
**Status:** ✅ Production-ready  
**Tested on:** Windows 10/11 + VMware Workstation  
**Python Version:** 3.10+

