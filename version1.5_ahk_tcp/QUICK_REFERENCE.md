# 🎮 Version 1.5 - Quick Reference

## ⚠️ STATUS: EXPERIMENTAL - NOT WORKING

**DO NOT USE IN PRODUCTION!** Use Version 1.0 or Version 2.0 instead.

---

## 📦 What's in This Folder?

### ✅ Available Files:

-   `multiplicity_jitter_DESYNC_SLAVE.ahk` - TCP Slave (AHK)
-   `compile_SLAVE_obfuscate.bat` - Compile to SystemAudioService.exe
-   `setup_autostart_SLAVE.bat` - Add to Windows startup
-   `remove_autostart_SLAVE.bat` - Remove from startup

### ❌ What's NOT Here (Use Version 2):

-   **Master script** → Use `version2_python/multiplicity_master.py`
-   **Master compile** → Run with Python directly

---

## 🏗️ Architecture

```
┌─────────────────────────┐
│   HOST (Master)         │
│  Python TCP Client      │
│  version2_python/       │
│  multiplicity_master.py │
└─────────┬───────────────┘
          │ TCP (port 7001)
          │ Sends "KEYDOWN:q"
          ▼
┌─────────────────────────┐
│   VM (Slave)            │
│  AHK TCP Server         │
│  version1.5_ahk_tcp/    │
│  ...SLAVE.ahk           │
└─────────────────────────┘
```

---

## 🚀 Quick Setup (For Debugging Only)

### On VM (Slave):

```bash
1. Run: compile_SLAVE_obfuscate.bat
2. Output: SystemAudioService.exe
3. Run SystemAudioService.exe as Admin
4. Should show tooltip: "TCP Server running on port 7001"
```

### On Host (Master):

```bash
cd version2_python
pip install -r requirements_multiplicity.txt
python multiplicity_master.py
```

### Test:

```
Press Q on Host → Should send to VM (but doesn't work yet!)
```

---

## 🐛 Known Issues

### Issue: Input Not Received

-   Master sends command ✅
-   Slave receives connection ✅
-   Slave DOESN'T process input ❌

**Root Cause:** WinSock DLL complexity in AHK

---

## 🎯 Recommendations

### ✅ **For Gaming (Production):**

Use **Version 1.0** - Pure AHK (WinActivate)

```
Location: version1_ahk/
Status: ✅ Working
```

### ✅ **For Development:**

Use **Version 2.0** - Pure Python (TCP)

```
Location: version2_python/
Status: ✅ Working
```

### ❌ **Avoid Version 1.5:**

```
Status: ❌ Broken
Purpose: Educational only
```

---

## 📚 Full Documentation

-   `README_VERSION1.5.md` - Detailed explanation
-   `../README_PROJECT_STRUCTURE.md` - Project overview
-   `../VERSION_SUMMARY.md` - Version comparison

---

**TL;DR:** This version doesn't work. Use v1.0 (AHK) or v2.0 (Python) instead! 🚀
