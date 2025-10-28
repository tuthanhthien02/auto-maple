# 🐍 Multiplicity Python Version - Setup Guide

## 📦 Installation

### BƯỚC 1: Install Python (if not installed)

```bash
# Download Python 3.10+ from: https://www.python.org/downloads/
# ⚠️ CHECK "Add Python to PATH" during installation!
```

### BƯỚC 2: Install Dependencies

```bash
# Trên HOST:
cd "C:\Users\Thanh Thien\Desktop\New folder\auto-maple"
pip install -r requirements_multiplicity.txt

# Trong VM (copy folder vào VM trước):
cd path\to\auto-maple
pip install -r requirements_multiplicity.txt
```

---

## 🚀 Running the Scripts

### BƯỚC 1: Run Slave in VM

```bash
# Trong VM "bishop":
cd path\to\auto-maple
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

### BƯỚC 2: Run Master on Host

```bash
# Trên HOST:
cd "C:\Users\Thanh Thien\Desktop\New folder\auto-maple"
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

### BƯỚC 3: Test!

```
1. Mở Notepad trong VM "bishop"
2. Trên HOST, ấn Q
3. Xem console output:
   [MASTER] KEYDOWN: q → ✅ 1/1 (2.5ms)
   [SLAVE] Received: KEYDOWN:q
   [SLAVE] Key: q → a
   ✓ Sent a DOWN (latency: 125.3ms)
4. Notepad trong VM hiện chữ "a" ✅
```

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

# Line 39-43: Auto pause (like human)
ENABLE_AUTO_PAUSE = True
PAUSE_INTERVAL_MIN = 20 * 60 * 1000  # 20 minutes
PAUSE_INTERVAL_MAX = 60 * 60 * 1000  # 60 minutes

# Line 46-62: Key remap (game-specific)
KEY_REMAP = {
    'q': 'a',  # Master sends Q → Slave sends A
    'w': 'w',
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
    'q', 'w', 'e', 'r', ...
]
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

## 🐛 Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'pynput'"

```bash
pip install pynput
```

### ❌ Slave: "Address already in use"

```bash
# Port 7001 đang được dùng, kill process:
netstat -ano | findstr :7001
taskkill /F /PID <PID_NUMBER>
```

### ❌ Master: "Connection refused"

```
1. Kiểm tra Slave có đang chạy không
2. Kiểm tra Firewall trong VM
3. Kiểm tra port mapping đúng chưa
```

### ❌ Input không hiện trong game

```
1. Kiểm tra KEY_REMAP mapping
2. Kiểm tra game có cần Run as Admin không
3. Kiểm tra anti-cheat có block không
```

---

## 📊 Performance Monitoring

### Master Performance

```
Ctrl+Alt+P → Show stats:
Total Sent: 1234
Success: 1230
Failed: 4
Avg Latency: 2.5ms
Success Rate: 99.7%
```

### Slave Performance

```
Auto-display every 60 seconds:
Total Keypresses: 5678
Avg Latency: 125.3ms
Total Desync Time: 1234567ms
Total Jitter Time: 45678ms
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

# multiplicity_slave.py (in each VM)
# VM1: TCP_PORT = 7001
# VM2: TCP_PORT = 7002
# VM3: TCP_PORT = 7003
# VM4: TCP_PORT = 7004
```

### 🎲 Different Desync Ranges per VM

```python
# VM1 (bishop): DESYNC_MIN=0,   DESYNC_MAX=300
# VM2 (cleric): DESYNC_MIN=100, DESYNC_MAX=400
# VM3 (warrior): DESYNC_MIN=200, DESYNC_MAX=500
# VM4 (mage):   DESYNC_MIN=300, DESYNC_MAX=600
```

---

## ✅ Advantages over AHK Version

1. ✅ **Easier to read & maintain** - Python syntax is clearer
2. ✅ **Better error handling** - try/except blocks
3. ✅ **Cross-platform** - Works on Windows/Linux (with minor changes)
4. ✅ **Better logging** - Colored console output (colorama)
5. ✅ **Easier to extend** - Add AI/ML features later
6. ✅ **Package management** - pip install vs manual DLLs

---

## 📌 Next Steps

1. ✅ Test basic setup (1 VM)
2. ✅ Add more VMs (edit VM_PORTS)
3. ✅ Customize key remapping (KEY_REMAP)
4. ✅ Tune desync/jitter for your game
5. ✅ Monitor performance (Ctrl+Alt+P)
6. 🎯 Profit! 🚀
