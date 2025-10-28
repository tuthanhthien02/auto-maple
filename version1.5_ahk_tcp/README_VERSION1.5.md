# 🎮 Version 1.5 - AutoHotkey + TCP Protocol (⚠️ Experimental)

## 📦 Folder Contents

This folder contains **Version 1.5** - An **experimental TCP implementation** using AutoHotkey.

---

## ⚠️ STATUS: EXPERIMENTAL / NOT WORKING YET

**Current Issues:**

-   ❌ TCP connection works but input not received by Slave
-   ❌ Requires debugging and fixes
-   ⚠️ **Use Version 1 (AHK) or Version 2 (Python) instead for production**

---

## 📂 File Structure

| File                                   | Purpose                           |
| -------------------------------------- | --------------------------------- |
| `multiplicity_jitter_DESYNC_SLAVE.ahk` | Slave script with TCP Server      |
| `compile_SLAVE_obfuscate.bat`          | Compile script (with obfuscation) |
| `setup_autostart_SLAVE.bat`            | Setup autostart on Windows        |
| `remove_autostart_SLAVE.bat`           | Remove from autostart             |
| `README_VERSION1.5.md`                 | This file                         |

**Note:** Master script is in **Version 2.0 (Python)** - `version2_python/multiplicity_master.py`

---

## 🎯 What is Version 1.5?

Version 1.5 is an **experimental hybrid** that combines:

-   ✅ **AutoHotkey** (from Version 1) - For low latency
-   ✅ **TCP Protocol** (from Version 2) - For better architecture
-   ❌ **Not working yet** - Still has bugs

### Why Version 1.5?

We wanted to get the **best of both worlds:**

-   AHK's low latency (~2-5ms)
-   TCP's clean architecture (no window focus issues)

**But it's not working yet!** 😅

---

## 🔧 Implementation Details

### Slave Script (TCP Server - AHK)

**Location:** `version1.5_ahk_tcp/multiplicity_jitter_DESYNC_SLAVE.ahk`

```ahk
- Uses WSAStartup() to init WinSock
- TCPListen() binds to port 7001
- TCPAccept() accepts connections
- TCPRecv() receives commands
- ProcessKeyDown() applies desync/jitter/remap
```

### Master Script (TCP Client - Python)

**Location:** `version2_python/multiplicity_master.py`

```python
- Uses Python's native socket library
- Broadcasts to multiple VMs via TCP
- Sends "KEYDOWN:q" format commands
- Thread-based parallel broadcasting
```

**This is Version 1.5's main issue:** AHK Slave (TCP) + Python Master (TCP) should work, but currently has bugs in the AHK TCP implementation.

---

## 🐛 Known Issues

### Issue #1: Input Not Received

**Symptom:**

-   Master sends "KEYDOWN:q" → Shows "✅ OK"
-   Slave shows: `[SLAVE] TCP Server running on port 7001`
-   But: No input received in VM

**Possible Causes:**

1. TCPRecv() blocking issue
2. Socket buffer problem
3. WinSock initialization timing
4. PostMessage vs SendInput conflict

### Issue #2: Port Already in Use

**Workaround:**

```cmd
netstat -ano | findstr :7001
taskkill /F /PID <PID>
```

---

## 🚀 How to Test (If you want to help debug)

### STEP 1: Compile & Run Slave in VM

```bash
# In version1.5_ahk_tcp folder:
1. Run: compile_SLAVE_obfuscate.bat
2. Copy SystemAudioService.exe to VM
3. Run in VM as Administrator
4. Should see: "[SLAVE] TCP Server running on port 7001"
```

### STEP 2: Run Python Master on Host

```bash
# In version2_python folder:
1. pip install -r requirements_multiplicity.txt
2. python multiplicity_master.py
3. Press Q
4. Check console output on both Master and Slave
```

### STEP 3: Debug

```
- Check tooltips on both Host and VM
- Look for error messages
- Verify TCP connection with: netstat -ano | findstr :7001
```

---

## 📊 Version Comparison

| Feature          | v1.0 (AHK)              | v1.5 (AHK+TCP)   | v2.0 (Python)    |
| ---------------- | ----------------------- | ---------------- | ---------------- |
| **Language**     | AutoHotkey              | AutoHotkey       | Python           |
| **Protocol**     | WinActivate + SendInput | TCP Sockets      | TCP Sockets      |
| **Latency**      | ~2-5ms ⭐⭐⭐⭐⭐       | ~5-10ms ⭐⭐⭐⭐ | ~5-15ms ⭐⭐⭐⭐ |
| **Window Focus** | ❌ Switches focus       | ✅ Background    | ✅ Background    |
| **Status**       | ✅ Working              | ❌ Broken        | ✅ Working       |
| **Recommended**  | ✅ YES                  | ❌ NO            | ✅ YES           |

---

## 🎯 Recommendations

### ✅ **For Production Use:**

-   **Use Version 1 (AHK)** - Proven, stable, low latency
    -   Location: `version1_ahk/`
    -   Status: ✅ Production-ready

### ✅ **For Modern Development:**

-   **Use Version 2 (Python)** - Clean, maintainable, working TCP
    -   Location: `version2_python/`
    -   Status: ✅ Production-ready

### ⚠️ **Avoid Version 1.5:**

-   Status: ❌ Experimental, not working
-   Only useful if you want to help debug

---

## 🔍 Why Did We Keep Version 1.5?

**Educational purposes:**

1. Shows TCP implementation attempt in AHK
2. Demonstrates WinSock API usage
3. Reference for future debugging
4. Learning material for hybrid approaches

**Historical record:**

-   We tried to combine AHK speed + TCP architecture
-   Hit technical issues with WinSock + AHK
-   Python version (v2.0) works better for TCP approach

---

## 🛠️ If You Want to Fix It

### Areas to Investigate:

1. **TCPRecv() blocking:**

    ```ahk
    ; Current implementation might block
    ; Need async/non-blocking recv
    ```

2. **Socket buffer size:**

    ```ahk
    ; Try larger buffers
    VarSetCapacity(buffer, 4096, 0)
    ```

3. **WinSock timing:**

    ```ahk
    ; Add delays after connect
    Sleep, 50
    ```

4. **Alternative: Use COM/WMI:**
    ```ahk
    ; Might be more reliable than raw WinSock
    ```

---

## 📚 Related Documentation

-   **Version 1 (Working AHK):** `../version1_ahk/README_VERSION1.md`
-   **Version 2 (Working Python):** `../version2_python/README_VERSION2.md`
-   **Project Structure:** `../README_PROJECT_STRUCTURE.md`

---

## 🎓 Lessons Learned

1. ✅ **AHK is great for SendInput** - Low latency, reliable
2. ✅ **Python is great for TCP** - Better socket library
3. ❌ **AHK + TCP = Tricky** - WinSock DLL calls are complex
4. 💡 **Hybrid not always better** - Stick to one language

**Conclusion:** Use Version 1 (pure AHK) or Version 2 (pure Python). Don't mix! 😊

---

**Created:** October 2025  
**Status:** ⚠️ Experimental / Not Working  
**Tested on:** Windows 10/11 + VMware Workstation  
**Recommendation:** Use Version 1 or Version 2 instead
