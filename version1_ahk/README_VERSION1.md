# 🎮 Version 1 - AutoHotkey (AHK) Scripts

## 📦 Folder Contents

This folder contains **Version 1** of the Multiplicity project, implemented using **AutoHotkey (AHK)**.

---

## 📂 File Structure

### 🎯 Main Scripts

| File                                              | Purpose                                                    |
| ------------------------------------------------- | ---------------------------------------------------------- |
| `Master_Multi_VM_EASY_CUSTOM.ahk`                 | **[RECOMMENDED]** Master script (Host) - Easy to customize |
| `multiplicity_jitter_DESYNC_SLAVE.ahk`            | **[RECOMMENDED]** Slave script (VM) - Full features        |
| `Master_Multi_VM_STEALTH.ahk`                     | Master script with obfuscation                             |
| `multiplicity_jitter_DESYNC_SLAVE_STEALTH.ahk`    | Slave script with obfuscation                              |
| `Master_Multi_VM_OBFUSCATED.ahk`                  | Heavily obfuscated Master                                  |
| `multiplicity_jitter_DESYNC_SLAVE_OBFUSCATED.ahk` | Heavily obfuscated Slave                                   |

### 📖 Documentation

| File                                | Content                      |
| ----------------------------------- | ---------------------------- |
| `QUICK_START_GUIDE.md`              | Quick setup for beginners    |
| `MASTER_SLAVE_SETUP_GUIDE.md`       | Complete setup instructions  |
| `MULTI_VM_SETUP_GUIDE.md`           | Multi-VM configuration guide |
| `HOTKEYS_REFERENCE_GUIDE.md`        | All hotkeys reference        |
| `OBFUSCATE_STEALTH_GUIDE.md`        | Obfuscation & stealth guide  |
| `MULTIPLICITY_OBFUSCATION_GUIDE.md` | Advanced obfuscation         |
| `README_MASTER_SLAVE.md`            | Master-Slave architecture    |
| `EASY_CUSTOM_GUIDE.txt`             | Easy customization tips      |

### 🔨 Compilation Scripts

| File                            | Purpose                     |
| ------------------------------- | --------------------------- |
| `compile_EASY_CUSTOM.bat`       | Compile EASY_CUSTOM scripts |
| `compile_MASTER_stealth.bat`    | Compile Master (stealth)    |
| `compile_SLAVE_stealth.bat`     | Compile Slave (stealth)     |
| `compile_MASTER_obfuscated.bat` | Compile Master (obfuscated) |
| `compile_SLAVE_obfuscated.bat`  | Compile Slave (obfuscated)  |
| `COMPILE_MAC_DINH_NGAY.bat`     | **Quick compile (default)** |

### ⚙️ Autostart Scripts

| File                              | Purpose                            |
| --------------------------------- | ---------------------------------- |
| `setup_autostart_EASY_CUSTOM.bat` | Add EASY_CUSTOM to Windows startup |
| `setup_autostart_SLAVE.bat`       | Add Slave to Windows startup       |
| `setup_autostart_STEALTH.bat`     | Add Stealth version to startup     |
| `setup_autostart_auto_pause.bat`  | Add auto pause to startup          |
| `remove_autostart_*.bat`          | Remove from Windows startup        |

---

## 🚀 Quick Start

### For Beginners (Recommended):

1. **Read:** `QUICK_START_GUIDE.md`
2. **Setup Master on Host:** Run `Master_Multi_VM_EASY_CUSTOM.ahk`
3. **Setup Slave in VM:** Run `multiplicity_jitter_DESYNC_SLAVE.ahk`
4. **Test:** Press Q on Host → See "a" in VM Notepad ✅

### For Advanced Users:

1. **Read:** `MASTER_SLAVE_SETUP_GUIDE.md`
2. **Customize:** Edit scripts for your game
3. **Compile:** Use `COMPILE_MAC_DINH_NGAY.bat`
4. **Deploy:** Use autostart scripts for convenience

---

## ✨ Key Features

### ✅ Master Script (Host):

-   🌐 TCP broadcasting to multiple VMs
-   ⌨️ Hotkey support (Ctrl+Alt+...)
-   📊 Performance monitoring
-   🔧 VM caching for speed
-   ⚡ Auto-retry on failure

### ✅ Slave Script (VM):

-   🌐 TCP server (listens for Master commands)
-   ⏱️ **Desync delay** (0-500ms randomized)
-   🎲 **Jitter** for arrow keys (Gaussian distribution)
-   🤖 **Auto pause** (20-60min intervals like human)
-   🎹 **Key remapping** (Q→A, etc.)
-   🔧 Windows SendInput API (undetectable)

---

## 🎯 Which Script to Use?

| Use Case                     | Master                            | Slave                                             |
| ---------------------------- | --------------------------------- | ------------------------------------------------- |
| **Beginner / Testing**       | `Master_Multi_VM_EASY_CUSTOM.ahk` | `multiplicity_jitter_DESYNC_SLAVE.ahk`            |
| **Production / Anti-detect** | `Master_Multi_VM_STEALTH.ahk`     | `multiplicity_jitter_DESYNC_SLAVE_STEALTH.ahk`    |
| **Maximum Security**         | `Master_Multi_VM_OBFUSCATED.ahk`  | `multiplicity_jitter_DESYNC_SLAVE_OBFUSCATED.ahk` |

---

## 📊 Version 1 vs Version 2 (Python)

| Feature             | Version 1 (AHK)   | Version 2 (Python)       |
| ------------------- | ----------------- | ------------------------ |
| **Language**        | AutoHotkey        | Python 3.10+             |
| **Latency**         | ~2-5ms ⭐⭐⭐⭐⭐ | ~5-15ms ⭐⭐⭐⭐         |
| **Memory**          | ~10MB ⭐⭐⭐⭐⭐  | ~50MB ⭐⭐⭐             |
| **Readability**     | Medium ⭐⭐⭐     | High ⭐⭐⭐⭐⭐          |
| **Maintainability** | Medium ⭐⭐⭐     | High ⭐⭐⭐⭐⭐          |
| **Error Handling**  | Basic ⭐⭐        | Advanced ⭐⭐⭐⭐⭐      |
| **Cross-platform**  | Windows only      | Windows/Linux ⭐⭐⭐⭐⭐ |
| **Anti-detection**  | High ⭐⭐⭐⭐     | Medium ⭐⭐⭐            |

**Recommendation:**

-   Use **Version 1 (AHK)** for maximum performance and anti-detection
-   Use **Version 2 (Python)** for easier maintenance and extensibility

---

## 🐛 Troubleshooting

### ❌ AHK script not running

```
1. Install AutoHotkey v1.1+ from: https://www.autohotkey.com/
2. Right-click script → "Run as Administrator"
```

### ❌ TCP connection failed

```
1. Check Firewall in VM
2. Verify port 7001 is not blocked
3. Run both scripts as Administrator
```

### ❌ Input not mirrored to VM

```
1. Check VM window title in Master script
2. Verify TCP_PORT matches (Master ↔ Slave)
3. Test with Notepad first before game
```

---

## 📌 Important Notes

1. ⚠️ **Each VM must use a DIFFERENT desync range!**

    - VM1: 0-300ms
    - VM2: 100-400ms
    - VM3: 200-500ms

2. ⚠️ **TCP ports must be unique per VM!**

    - VM1: 7001
    - VM2: 7002
    - VM3: 7003

3. ⚠️ **Run scripts as Administrator** for best compatibility!

4. ✅ **Test with Notepad first** before using in game!

---

## 🎯 Next Steps

1. ✅ Read `QUICK_START_GUIDE.md`
2. ✅ Test basic setup (1 Master + 1 Slave)
3. ✅ Customize settings for your game
4. ✅ Add more VMs if needed
5. ✅ Consider migrating to Version 2 (Python) for easier maintenance

---

## 🔗 Related

-   **Version 2 (Python)**: See `../` directory for Python version
-   **Setup Guide**: See `PYTHON_SETUP_GUIDE.md` in parent directory

---

**Created:** October 2025  
**Status:** ✅ Production-ready  
**Tested on:** Windows 10/11 + VMware Workstation

