# 🎮 Auto-Maple Multiplicity Project Structure

## 📂 Directory Layout

```
auto-maple/
├── version1_ahk/              # Version 1.0 - Standalone AHK scripts
│   ├── multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk  # Standalone (customizable)
│   ├── multiplicity_jitter_DESYNC_STEALTH.ahk      # Standalone (stealth)
│   ├── compile_*.bat          # Compilation scripts
│   ├── *_GUIDE.md             # Documentation
│   └── README_VERSION1.md     # Version 1 README
│
├── version1.1_ahk_winactivate/  # Version 1.1 - Master-Slave (WinActivate)
│   ├── Master_Multi_VM_*.ahk  # Master scripts (Host)
│   ├── multiplicity_*_SLAVE_*.ahk  # Slave scripts (VM)
│   ├── compile_MASTER_*.bat   # Master compile scripts
│   ├── compile_SLAVE_*.bat    # Slave compile scripts
│   ├── README_MASTER_SLAVE.md
│   ├── MASTER_SLAVE_SETUP_GUIDE.md
│   └── README_VERSION1.1.md   # Version 1.1 README
│
├── version1.5_ahk_tcp/        # Version 1.5 - AHK Slave (TCP) + Python Master (⚠️ Experimental)
│   ├── multiplicity_jitter_DESYNC_SLAVE.ahk  # TCP Slave (AHK)
│   ├── compile_SLAVE_obfuscate.bat
│   ├── setup_autostart_SLAVE.bat
│   ├── remove_autostart_SLAVE.bat
│   └── README_VERSION1.5.md   # Experimental README
│   # Note: Master is in version2_python/multiplicity_master.py
│
├── version2_python/           # Version 2.0 - Python + TCP
│   ├── multiplicity_master.py
│   ├── multiplicity_slave.py
│   ├── requirements_multiplicity.txt
│   ├── PYTHON_SETUP_GUIDE.md
│   └── README_VERSION2.md
│
├── main.py                    # Original auto-maple bot
├── requirements.txt           # Bot dependencies
├── setup.py                   # Bot setup
│
├── src/                       # Bot source code
├── assets/                    # Bot assets
└── resources/                 # Bot resources
```

---

## 🎯 Four Versions Available

### 📦 Version 1.0 - Standalone AHK Scripts

-   **Location:** `version1_ahk/`
-   **Language:** AutoHotkey v1.1+
-   **Architecture:** Standalone (no Master-Slave)
-   **Protocol:** Direct SendInput (no broadcasting)
-   **Best for:** Single VM, simple setup, maximum customization
-   **Status:** ✅ Production-ready
-   **Anti-detection:** ⭐⭐⭐⭐⭐

**Key Scripts:**

-   `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` - Customizable standalone
-   `multiplicity_jitter_DESYNC_STEALTH.ahk` - Stealth standalone

**Documentation:**

-   `version1_ahk/README_VERSION1.md` - Full guide
-   `version1_ahk/QUICK_START_GUIDE.md` - Quick setup

---

### 📦 Version 1.1 - Master-Slave (WinActivate)

-   **Location:** `version1.1_ahk_winactivate/`
-   **Language:** AutoHotkey v1.1+
-   **Architecture:** Master (Host) → Slaves (VMs)
-   **Protocol:** WinActivate + ControlSend
-   **Best for:** Managing multiple VMs with centralized control
-   **Status:** ✅ Production-ready
-   **Anti-detection:** ⭐⭐⭐⭐⭐

**Key Scripts:**

-   `Master_Multi_VM_STEALTH.ahk` - Master (Host)
-   `multiplicity_jitter_DESYNC_SLAVE_STEALTH.ahk` - Slave (VM)

**Documentation:**

-   `version1.1_ahk_winactivate/README_VERSION1.1.md` - Version guide
-   `version1.1_ahk_winactivate/MASTER_SLAVE_SETUP_GUIDE.md` - Setup guide

---

### ⚠️ Version 1.5 - AHK Slave (TCP) + Python Master (Experimental)

-   **Location:** `version1.5_ahk_tcp/` (Slave) + `version2_python/` (Master)
-   **Language:** AutoHotkey (Slave) + Python (Master)
-   **Protocol:** TCP Sockets (WinSock DLL in AHK Slave)
-   **Architecture:** Hybrid - AHK TCP Server + Python TCP Client
-   **Best for:** Educational / Debugging
-   **Status:** ❌ Experimental - Not Working
-   **Anti-detection:** N/A

**Note:** This is an experimental version that combines AHK slave (for low latency) with Python master (for easy control). **Not recommended for production use!**

---

### 🐍 Version 2 - Python + TCP

-   **Location:** `version2_python/`
-   **Language:** Python 3.10+
-   **Protocol:** TCP Sockets (native Python)
-   **Best for:** Easier maintenance, cross-platform
-   **Status:** ✅ Production-ready
-   **Anti-detection:** ⭐⭐⭐⭐

**Key Scripts:**

-   `multiplicity_master.py` - Master (Host)
-   `multiplicity_slave.py` - Slave (VM)

**Documentation:**

-   `version2_python/PYTHON_SETUP_GUIDE.md` - Complete guide
-   `version2_python/README_VERSION2.md` - Full guide

---

## 🤔 Which Version to Choose?

| Criteria              | Version 1 (AHK)   | Version 2 (Python)       |
| --------------------- | ----------------- | ------------------------ |
| **Latency**           | ~2-5ms ⭐⭐⭐⭐⭐ | ~5-15ms ⭐⭐⭐⭐         |
| **Memory Usage**      | ~10MB ⭐⭐⭐⭐⭐  | ~50MB ⭐⭐⭐             |
| **Easy to Read**      | ⭐⭐⭐            | ⭐⭐⭐⭐⭐               |
| **Easy to Customize** | ⭐⭐⭐            | ⭐⭐⭐⭐⭐               |
| **Error Handling**    | ⭐⭐              | ⭐⭐⭐⭐⭐               |
| **Cross-platform**    | Windows only      | Windows/Linux ⭐⭐⭐⭐⭐ |
| **Anti-detection**    | ⭐⭐⭐⭐⭐        | ⭐⭐⭐⭐                 |
| **Compilation Size**  | ~1-2MB ⭐⭐⭐⭐⭐ | ~20-30MB ⭐⭐⭐          |

### 🎯 Recommendations:

**Choose Version 1 (AHK) if:**

-   ✅ You need lowest latency (< 5ms)
-   ✅ You only use Windows
-   ✅ Maximum anti-detection is priority
-   ✅ Smallest memory footprint needed

**Choose Version 2 (Python) if:**

-   ✅ You want easier code maintenance
-   ✅ You need cross-platform support
-   ✅ You plan to add AI/ML features
-   ✅ You're comfortable with Python
-   ✅ Latency < 15ms is acceptable

---

## 🚀 Quick Start

### Version 1 (AHK):

```bash
# 1. Navigate to Version 1 folder
cd version1_ahk

# 2. Read setup guide
# Open: QUICK_START_GUIDE.md

# 3. Run Master on Host
# Double-click: Master_Multi_VM_EASY_CUSTOM.ahk

# 4. Run Slave in VM
# Double-click: multiplicity_jitter_DESYNC_SLAVE.ahk
```

### Version 2 (Python):

```bash
# 1. Install dependencies
pip install -r requirements_multiplicity.txt

# 2. Read setup guide
# Open: PYTHON_SETUP_GUIDE.md

# 3. Run Master on Host
python multiplicity_master.py

# 4. Run Slave in VM
python multiplicity_slave.py
```

---

## 📊 Feature Comparison

| Feature             | Version 1 (AHK) | Version 2 (Python) |
| ------------------- | --------------- | ------------------ |
| TCP Broadcasting    | ✅              | ✅                 |
| Desync Delay        | ✅ 0-500ms      | ✅ 0-500ms         |
| Jitter (Arrow keys) | ✅ Gaussian     | ✅ Gaussian        |
| Auto Pause          | ✅ 20-60min     | ✅ 20-60min        |
| Key Remapping       | ✅              | ✅                 |
| Performance Monitor | ✅              | ✅                 |
| Debug Mode          | ✅              | ✅ Colored output  |
| Hotkeys             | ✅ Ctrl+Alt+... | ✅ Ctrl+Alt+...    |
| Obfuscation         | ✅ Built-in     | ❌ Manual          |
| Colored Console     | ❌              | ✅                 |
| Error Logging       | Basic           | Advanced           |

---

## 🔧 Configuration

### Common Settings (Both Versions):

```
TCP Port Mapping:
  VM1 → Port 7001
  VM2 → Port 7002
  VM3 → Port 7003
  ...

Desync Ranges (MUST be different per VM):
  VM1: 0-300ms
  VM2: 100-400ms
  VM3: 200-500ms
  VM4: 300-600ms

Key Remapping Example:
  Q → A  (Master sends Q, Slave sends A)
  W → W  (No remap)
  E → E  (No remap)
```

---

## 🐛 Troubleshooting

### Both Versions:

**❌ Connection refused:**

```
1. Check Slave is running
2. Verify port 7001 is open
3. Check Windows Firewall
4. Run as Administrator
```

**❌ Input not working:**

```
1. Test with Notepad first
2. Check key remap mapping
3. Verify desync delay isn't too high
4. Check game anti-cheat compatibility
```

### Version 1 (AHK) Specific:

**❌ AHK not installed:**

```
Download from: https://www.autohotkey.com/
Install v1.1.33+
```

### Version 2 (Python) Specific:

**❌ Module not found:**

```bash
pip install -r requirements_multiplicity.txt
```

---

## 📁 Additional Files

| File                           | Purpose                                             |
| ------------------------------ | --------------------------------------------------- |
| `main.py`                      | Original auto-maple bot (unrelated to multiplicity) |
| `README.md`                    | Main project README                                 |
| `DETECTION_RISK_ANALYSIS.md`   | Anti-detection analysis                             |
| `VERSION_COMPARISON.md`        | Detailed version comparison                         |
| `MULTIPLICITY_ALTERNATIVES.md` | Alternative solutions                               |

---

## 🎯 Migration Guide

### From Version 1 → Version 2:

1. ✅ Install Python 3.10+
2. ✅ Install dependencies: `pip install -r requirements_multiplicity.txt`
3. ✅ Copy settings from AHK scripts to Python configs
4. ✅ Test with 1 VM first
5. ✅ Gradually migrate other VMs

### Settings Mapping:

| AHK Variable              | Python Variable     |
| ------------------------- | ------------------- |
| `global TCP_PORT := 7001` | `TCP_PORT = 7001`   |
| `global MinDesync := 0`   | `DESYNC_MIN = 0`    |
| `global MaxDesync := 500` | `DESYNC_MAX = 500`  |
| `global MinJitter := 5`   | `JITTER_MIN = 5`    |
| `global remap := {...}`   | `KEY_REMAP = {...}` |

---

## 📞 Support

-   **Documentation:** See guide files in each version folder
-   **Issues:** Check troubleshooting sections
-   **Questions:** Review comparison tables above

---

**Last Updated:** October 2025  
**Project Status:** ✅ Both versions production-ready  
**Tested on:** Windows 10/11 + VMware Workstation
