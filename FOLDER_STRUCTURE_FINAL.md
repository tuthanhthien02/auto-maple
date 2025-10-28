# 🎮 Auto-Maple Multiplicity - Final Folder Structure

## 📊 QUICK OVERVIEW

```
auto-maple/
│
├── 📁 version1_ahk/              ← V1.0: Standalone Scripts ✅
├── 📁 version1.1_ahk_winactivate/ ← V1.1: Master-Slave (WinActivate) ✅
├── 📁 version1.5_ahk_tcp/        ← V1.5: Hybrid (Experimental) ⚠️
└── 📁 version2_python/           ← V2.0: Python (TCP) ✅
```

---

## 📂 DETAILED BREAKDOWN

### ✅ Version 1.0 - Standalone AHK Scripts

📁 **Location:** `version1_ahk/`

**What's inside:**

```
version1_ahk/
├── multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk  ⭐ RECOMMENDED
├── multiplicity_jitter_DESYNC_STEALTH.ahk
├── compile_EASY_CUSTOM*.bat
├── compile_STEALTH*.bat
├── setup_autostart_*.bat
└── README_VERSION1.md
```

**No Master/Slave files!** ✅  
All scripts are **standalone** - run directly in each VM.

---

### ✅ Version 1.1 - Master-Slave (WinActivate)

📁 **Location:** `version1.1_ahk_winactivate/`

**What's inside:**

```
version1.1_ahk_winactivate/
├── Master_Multi_VM_STEALTH.ahk                ⭐ Master (Host)
├── Master_Multi_VM_OBFUSCATED.ahk
├── Master_Multi_VM.ahk
├── multiplicity_jitter_DESYNC_SLAVE_STEALTH.ahk  ⭐ Slave (VM)
├── multiplicity_jitter_DESYNC_SLAVE_OBFUSCATED.ahk
├── compile_MASTER_*.bat
├── compile_SLAVE_*.bat
├── README_MASTER_SLAVE.md
├── MASTER_SLAVE_SETUP_GUIDE.md
└── README_VERSION1.1.md
```

**All Master/Slave files are here!** ✅  
Centralized control: 1 Master → Multiple Slaves

---

### ⚠️ Version 1.5 - Hybrid (Experimental)

📁 **Location:** `version1.5_ahk_tcp/`

**What's inside:**

```
version1.5_ahk_tcp/
├── multiplicity_jitter_DESYNC_SLAVE.ahk  (TCP Slave - AHK)
├── compile_SLAVE_obfuscate.bat
├── setup_autostart_SLAVE.bat
├── remove_autostart_SLAVE.bat
├── README_VERSION1.5.md
└── QUICK_REFERENCE.md
```

**Note:** Master is in `version2_python/multiplicity_master.py`  
**Status:** ❌ Not working - for educational purposes only

---

### ✅ Version 2.0 - Python (TCP)

📁 **Location:** `version2_python/`

**What's inside:**

```
version2_python/
├── multiplicity_master.py         ⭐ Master (Host)
├── multiplicity_slave.py          ⭐ Slave (VM)
├── requirements_multiplicity.txt
├── PYTHON_SETUP_GUIDE.md
└── README_VERSION2.md
```

**Pure Python implementation** ✅  
TCP-based Master-Slave with better error handling

---

## 🎯 WHICH VERSION TO USE?

### 🏆 Use Version 1.0 (Standalone) if:

```
✅ Simple setup (single VM)
✅ Maximum customization
✅ No Master-Slave complexity
✅ Just want it to work!
```

### 🏆 Use Version 1.1 (Master-Slave) if:

```
✅ Multiple VMs (centralized control)
✅ Need to manage many VMs from 1 PC
✅ Comfortable with WinActivate
✅ Maximum performance
```

### 🏆 Use Version 2.0 (Python) if:

```
✅ Want modern codebase
✅ Need cross-platform (Windows + Linux)
✅ Prefer Python over AHK
✅ TCP protocol benefits
```

### ❌ DON'T Use Version 1.5:

```
❌ Experimental, broken
⚠️ For educational purposes only
```

---

## 📊 COMPARISON TABLE

| Feature             | v1.0 Standalone   | v1.1 Master-Slave | v2.0 Python     |
| ------------------- | ----------------- | ----------------- | --------------- |
| **Architecture**    | Standalone        | Master → Slaves   | Master ↔ Slaves |
| **Protocol**        | None              | WinActivate       | TCP             |
| **Latency**         | 2-5ms ⭐⭐⭐⭐⭐  | 2-5ms ⭐⭐⭐⭐⭐  | 5-15ms ⭐⭐⭐⭐ |
| **Setup**           | Simple ⭐⭐⭐⭐⭐ | Medium ⭐⭐⭐     | Medium ⭐⭐⭐   |
| **Centralized**     | ❌                | ✅                | ✅              |
| **Multi-VM**        | Manual            | Easy ⭐⭐⭐⭐⭐   | Easy ⭐⭐⭐⭐⭐ |
| **Customization**   | High ⭐⭐⭐⭐⭐   | Medium ⭐⭐⭐     | High ⭐⭐⭐⭐⭐ |
| **Maintainability** | Medium ⭐⭐⭐     | Medium ⭐⭐⭐     | High ⭐⭐⭐⭐⭐ |

---

## 🚀 QUICK START GUIDE

### Version 1.0 (Standalone):

```bash
cd version1_ahk
# Edit: multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk
# Run: compile_EASY_CUSTOM.bat
# Deploy to each VM individually
```

### Version 1.1 (Master-Slave):

```bash
cd version1.1_ahk_winactivate
# HOST: Edit Master_Multi_VM_STEALTH.ahk (VM names)
# HOST: Run compile_MASTER_stealth.bat
# VM: Run compile_SLAVE_stealth.bat
# Deploy Master.exe to Host, Slave.exe to VMs
```

### Version 2.0 (Python):

```bash
cd version2_python
pip install -r requirements_multiplicity.txt
# HOST: python multiplicity_master.py
# VM: python multiplicity_slave.py
```

---

## 📚 DOCUMENTATION

| Version  | Main README                                       | Setup Guide                   |
| -------- | ------------------------------------------------- | ----------------------------- |
| **v1.0** | `version1_ahk/README_VERSION1.md`                 | `QUICK_START_GUIDE.md`        |
| **v1.1** | `version1.1_ahk_winactivate/README_VERSION1.1.md` | `MASTER_SLAVE_SETUP_GUIDE.md` |
| **v1.5** | `version1.5_ahk_tcp/README_VERSION1.5.md`         | N/A (broken)                  |
| **v2.0** | `version2_python/README_VERSION2.md`              | `PYTHON_SETUP_GUIDE.md`       |

---

## ✅ VERIFICATION CHECKLIST

### ✅ Version 1.0 (version1_ahk/):

-   [x] No Master files
-   [x] No Slave files
-   [x] Only standalone scripts
-   [x] EASY_CUSTOM.ahk ✓
-   [x] STEALTH.ahk ✓

### ✅ Version 1.1 (version1.1_ahk_winactivate/):

-   [x] All Master files moved
-   [x] All Slave files moved
-   [x] Master-Slave guides included
-   [x] Compile scripts for both

### ✅ Version 1.5 (version1.5_ahk_tcp/):

-   [x] Only TCP Slave (AHK)
-   [x] Master is in v2.0 Python
-   [x] Marked as experimental

### ✅ Version 2.0 (version2_python/):

-   [x] Python Master + Slave
-   [x] Requirements file
-   [x] Setup guides

---

## 🎓 FINAL NOTES

1. **Version 1.0** = Standalone (no Master-Slave) ✅
2. **Version 1.1** = Master-Slave (WinActivate) ✅
3. **Version 1.5** = Experimental hybrid ❌
4. **Version 2.0** = Python TCP implementation ✅

**All folders are now clearly separated!** 🎉

---

**Last Updated:** October 2025  
**Structure Status:** ✅ Final and Clean  
**No Master/Slave files in version1_ahk:** ✅ Confirmed
