# 🎮 Version 1.1 - Master-Slave Architecture (WinActivate)

## 📦 Folder Contents

This folder contains **Version 1.1** - Master-Slave architecture using **WinActivate + ControlSend**.

---

## ⚙️ Architecture

```
┌─────────────────────────┐
│   HOST (Master)         │
│  Master_Multi_VM.ahk    │
│  WinActivate + Send     │
└─────────┬───────────────┘
          │ WinActivate
          │ ControlSend
          ▼
┌─────────────────────────┐
│   VM (Slave)            │
│  ...SLAVE_STEALTH.ahk   │
│  Receives + Processes   │
└─────────────────────────┘
```

---

## 📂 File Structure

### 🎯 Master Scripts (Host)

| File                             | Purpose                           |
| -------------------------------- | --------------------------------- |
| `Master_Multi_VM.ahk`            | Standard Master script            |
| `Master_Multi_VM_STEALTH.ahk`    | **[RECOMMENDED]** Stealth version |
| `Master_Multi_VM_OBFUSCATED.ahk` | Heavily obfuscated                |
| `Master_Test.ahk`                | Test script                       |

### 🎯 Slave Scripts (VM)

| File                                              | Purpose                         |
| ------------------------------------------------- | ------------------------------- |
| `multiplicity_jitter_DESYNC_SLAVE_STEALTH.ahk`    | **[RECOMMENDED]** Stealth Slave |
| `multiplicity_jitter_DESYNC_SLAVE_OBFUSCATED.ahk` | Heavily obfuscated Slave        |

### 🔨 Compilation Scripts

| File                            | Purpose                     |
| ------------------------------- | --------------------------- |
| `compile_MASTER_stealth.bat`    | Compile Master (stealth)    |
| `compile_MASTER_obfuscated.bat` | Compile Master (obfuscated) |
| `compile_SLAVE_stealth.bat`     | Compile Slave (stealth)     |
| `compile_SLAVE_obfuscated.bat`  | Compile Slave (obfuscated)  |

### 📖 Documentation

| File                          | Purpose               |
| ----------------------------- | --------------------- |
| `README_MASTER_SLAVE.md`      | Master-Slave overview |
| `MASTER_SLAVE_SETUP_GUIDE.md` | Complete setup guide  |
| `TEST_MASTER_SLAVE_GUIDE.md`  | Testing guide         |

---

## 🚀 Quick Start

### STEP 1: Edit VM Names in Master Script

Open `Master_Multi_VM_STEALTH.ahk` and edit VM list (around line 77):

```ahk
vmList := ["bishop", "cleric", "warrior"]  ; ← Your VM window titles
```

### STEP 2: Compile Scripts

**On Host:**

```bash
cd version1.1_ahk_winactivate
compile_MASTER_stealth.bat
# Output: Master_Multi_VM_STEALTH.exe
```

**For VMs:**

```bash
compile_SLAVE_stealth.bat
# Output: multiplicity_jitter_DESYNC_SLAVE_STEALTH.exe
```

### STEP 3: Run

1. **In each VM:** Run `multiplicity_jitter_DESYNC_SLAVE_STEALTH.exe`
2. **On Host:** Run `Master_Multi_VM_STEALTH.exe`
3. **Test:** Press any key on Host → All VMs receive!

---

## ✨ Key Features

### ✅ Master Script (Host):

-   🌐 **Broadcast to multiple VMs** via WinActivate + ControlSend
-   🔍 **VM Window Caching** for faster detection
-   ⚡ **Auto-retry** on failed broadcasts
-   📊 **Performance monitoring**
-   🎛️ **Hotkeys**: Ctrl+Alt+S (status), Ctrl+Alt+T (toggle)

### ✅ Slave Script (VM):

-   ⏱️ **Desync delay** (0-500ms randomized)
-   🎲 **Jitter** for arrow keys (Gaussian distribution)
-   🤖 **Auto pause** (20-60min intervals)
-   🎹 **Key remapping** (Q→A, W→S, etc.)
-   🔧 **SendInput API** (undetectable)

---

## 🎯 When to Use Version 1.1?

**Choose Version 1.1 if:**

-   ✅ You want centralized control (1 Master → many Slaves)
-   ✅ You need to manage multiple VMs easily
-   ✅ You're comfortable with WinActivate (switches focus)
-   ✅ Maximum performance is priority

**DON'T use if:**

-   ❌ You want background operation (use Version 1.0 standalone)
-   ❌ You need TCP protocol (use Version 2.0 Python)
-   ❌ Window focus switching is annoying (use Version 1.0)

---

## 📊 Version 1.1 vs Other Versions

| Feature          | v1.0 (Standalone) | v1.1 (Master-Slave) | v2.0 (Python)      |
| ---------------- | ----------------- | ------------------- | ------------------ |
| **Architecture** | Single script     | Master → Slaves     | Master ↔ Slaves    |
| **Protocol**     | None              | WinActivate         | TCP Sockets        |
| **Latency**      | ~2-5ms ⭐⭐⭐⭐⭐ | ~2-5ms ⭐⭐⭐⭐⭐   | ~5-15ms ⭐⭐⭐⭐   |
| **Window Focus** | ❌ Switches       | ❌ Switches         | ✅ Background      |
| **Control**      | Individual        | Centralized ⭐      | Centralized ⭐     |
| **Setup**        | Simple            | Medium              | Medium             |
| **Recommended**  | ✅ For solo use   | ✅ For multi-VM     | ✅ For development |

---

## 🐛 Troubleshooting

### ❌ Master can't find VM windows

```
1. Press Ctrl+Alt+L in Master → Lists all windows
2. Copy EXACT window title to vmList
3. Make sure VM is running before Master
```

### ❌ Slave not receiving input

```
1. Check Slave is running in VM
2. Check VM window title matches Master's vmList
3. Run both scripts as Administrator
```

### ❌ Input only works when VM is focused

```
This is expected with WinActivate!
Use Version 1.0 (standalone) or Version 2.0 (Python TCP) for background operation.
```

---

## 🎛️ Hotkeys Reference

### Master Hotkeys:

| Hotkey       | Action                          |
| ------------ | ------------------------------- |
| `Ctrl+Alt+S` | Status Check (VM found/missing) |
| `Ctrl+Alt+L` | List all windows (copy names)   |
| `Ctrl+Alt+T` | Toggle broadcasting ON/OFF      |
| `Ctrl+Alt+P` | Performance monitor             |
| `Ctrl+Alt+Q` | Exit script                     |

### Slave Hotkeys:

| Hotkey       | Action               |
| ------------ | -------------------- |
| `Ctrl+Alt+T` | Toggle script ON/OFF |
| `Ctrl+Alt+P` | Performance stats    |
| `Ctrl+Alt+R` | Reset statistics     |

---

## 📚 Documentation

For detailed setup:

-   `MASTER_SLAVE_SETUP_GUIDE.md` - Complete setup guide
-   `README_MASTER_SLAVE.md` - Architecture overview
-   `TEST_MASTER_SLAVE_GUIDE.md` - Testing procedures

For comparison:

-   `../README_PROJECT_STRUCTURE.md` - Project overview
-   `../VERSION_SUMMARY.md` - Version comparison

---

## 🔗 Related Versions

-   **Version 1.0** (`../version1_ahk/`) - Standalone scripts (no Master-Slave)
-   **Version 1.5** (`../version1.5_ahk_tcp/`) - Experimental TCP (broken)
-   **Version 2.0** (`../version2_python/`) - Python TCP (working)

---

**Created:** October 2025  
**Status:** ✅ Production-ready  
**Tested on:** Windows 10/11 + VMware Workstation  
**Best for:** Managing multiple VMs with centralized control
