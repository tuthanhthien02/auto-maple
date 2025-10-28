# 🎮 Multiplicity - Version Summary

## 📊 Quick Version Comparison

| Version | Language   | Architecture | Protocol    | Status        | Recommended |
| ------- | ---------- | ------------ | ----------- | ------------- | ----------- |
| **1.0** | AutoHotkey | Standalone   | SendInput   | ✅ Production | ✅ YES      |
| **1.1** | AutoHotkey | Master-Slave | WinActivate | ✅ Production | ✅ YES      |
| **1.5** | AHK+Python | Hybrid       | TCP Sockets | ❌ Broken     | ❌ NO       |
| **2.0** | Python     | Master-Slave | TCP Sockets | ✅ Production | ✅ YES      |

---

## 🎯 Version Details

### ✅ Version 1.0 - Standalone AHK Scripts

📁 **Location:** `version1_ahk/`

**Pros:**

-   ⚡ Lowest latency (~2-5ms)
-   🔒 Best anti-detection
-   💾 Smallest memory (~10MB)
-   ✅ Simple setup (no Master-Slave)
-   🎨 Easy to customize

**Cons:**

-   ⚠️ No centralized control
-   ⚠️ Each VM needs individual configuration
-   ⚠️ Windows only

**Best for:**

-   Single VM setup
-   Maximum customization needed
-   Simple deployment

**Files:**

-   `multiplicity_jitter_DESYNC_EASY_CUSTOM.ahk` - Customizable
-   `multiplicity_jitter_DESYNC_STEALTH.ahk` - Stealth version

---

### ✅ Version 1.1 - Master-Slave (WinActivate)

📁 **Location:** `version1.1_ahk_winactivate/`

**Pros:**

-   ⚡ Lowest latency (~2-5ms)
-   🔒 Best anti-detection
-   💾 Small memory (~10MB)
-   🎛️ Centralized control (1 Master → many Slaves)
-   ✅ Proven & stable

**Cons:**

-   ⚠️ Switches window focus (WinActivate)
-   ⚠️ Requires Master + Slave setup
-   ⚠️ Windows only

**Best for:**

-   Multiple VMs with centralized control
-   Gaming (MapleStory, MMOs)
-   Maximum performance with multi-VM

**Files:**

-   Master: `Master_Multi_VM_STEALTH.ahk`
-   Slave: `multiplicity_jitter_DESYNC_SLAVE_STEALTH.ahk`

---

### ⚠️ Version 1.5 - AHK Slave (TCP) + Python Master (Experimental)

📁 **Location:** `version1.5_ahk_tcp/`

**Status:** ❌ Not Working

**Architecture:**

-   **Slave (VM):** AutoHotkey with TCP Server (`multiplicity_jitter_DESYNC_SLAVE.ahk`)
-   **Master (Host):** Python with TCP Client (`version2_python/multiplicity_master.py`)

**Why it exists:**

-   Attempt to combine AHK slave (low latency) + Python master (easy maintenance)
-   Educational/debugging purposes
-   Historical record

**Known issues:**

-   TCP connection works but input not received by AHK Slave
-   WinSock DLL complexity in AHK
-   Socket buffer problems

**Recommendation:** ❌ **DO NOT USE** - Use v1.0 (pure AHK) or v2.0 (pure Python) instead

---

### ✅ Version 2.0 - Python + TCP

📁 **Location:** `version2_python/`

**Pros:**

-   📖 Easy to read & maintain
-   🌐 Cross-platform (Windows/Linux)
-   🔧 Better error handling
-   🎨 Colored console output
-   ✅ TCP works perfectly

**Cons:**

-   ⚠️ Higher latency (~5-15ms)
-   ⚠️ More memory (~50MB)
-   ⚠️ Requires Python runtime

**Best for:**

-   Long-term maintenance
-   Cross-platform deployment
-   Future AI/ML features
-   Team development

**Files:**

-   Master: `multiplicity_master.py`
-   Slave: `multiplicity_slave.py`

---

## 🤔 Which Version Should I Use?

### 🎮 For Gaming (MapleStory, MMOs):

```
✅ Use Version 1.0 (AutoHotkey)
   - Lowest latency
   - Best anti-detection
   - Proven stability
```

### 💻 For Development/Maintenance:

```
✅ Use Version 2.0 (Python)
   - Easier to modify
   - Better error messages
   - Cross-platform
```

### 🔬 For Learning/Debugging:

```
⚠️ Check Version 1.5 (but don't use in production!)
   - See TCP + AHK attempt
   - Learn from mistakes
```

---

## 📈 Performance Comparison

| Metric           | v1.0 (AHK)  | v1.5 (AHK+TCP) | v2.0 (Python) |
| ---------------- | ----------- | -------------- | ------------- |
| **Latency**      | ~2-5ms      | N/A (broken)   | ~5-15ms       |
| **Memory**       | ~10MB       | N/A            | ~50MB         |
| **CPU Usage**    | <1%         | N/A            | ~2-5%         |
| **Reliability**  | ⭐⭐⭐⭐⭐  | ❌             | ⭐⭐⭐⭐⭐    |
| **Window Focus** | ❌ Switches | ✅ Background  | ✅ Background |

---

## 🔧 Feature Comparison

| Feature           | v1.0 | v1.5        | v2.0      |
| ----------------- | ---- | ----------- | --------- |
| Desync Delay      | ✅   | ✅          | ✅        |
| Jitter            | ✅   | ✅          | ✅        |
| Auto Pause        | ✅   | ✅          | ✅        |
| Key Remap         | ✅   | ✅          | ✅        |
| TCP Protocol      | ❌   | ❌ (broken) | ✅        |
| Colored Output    | ❌   | ❌          | ✅        |
| Hotkeys           | ✅   | ✅          | ✅        |
| Performance Stats | ✅   | ✅          | ✅        |
| Obfuscation       | ✅   | ❌          | ⚠️ Manual |

---

## 🚀 Quick Start by Version

### Version 1.0 (AHK):

```bash
cd version1_ahk
# Read: QUICK_START_GUIDE.md
# Run: Master_Multi_VM_STEALTH.ahk (Host)
# Run: multiplicity_jitter_DESYNC_SLAVE_STEALTH.ahk (VM)
```

### Version 1.5 (Don't use!):

```bash
# ⚠️ Skip this version - it doesn't work!
# Use v1.0 or v2.0 instead
```

### Version 2.0 (Python):

```bash
cd version2_python
pip install -r requirements_multiplicity.txt
python multiplicity_master.py  # Host
python multiplicity_slave.py   # VM
```

---

## 📚 Documentation Links

| Version  | Main README                               | Quick Start             | Full Guide                    |
| -------- | ----------------------------------------- | ----------------------- | ----------------------------- |
| **v1.0** | `version1_ahk/README_VERSION1.md`         | `QUICK_START_GUIDE.md`  | `MASTER_SLAVE_SETUP_GUIDE.md` |
| **v1.5** | `version1.5_ahk_tcp/README_VERSION1.5.md` | N/A                     | N/A                           |
| **v2.0** | `version2_python/README_VERSION2.md`      | `PYTHON_SETUP_GUIDE.md` | `PYTHON_SETUP_GUIDE.md`       |

---

## 🎓 Version History

### v1.0 - Initial Release

-   Pure AutoHotkey
-   WinActivate + SendInput
-   Proven stability
-   ✅ Production-ready

### v1.5 - TCP Experiment

-   Attempted AHK + TCP hybrid
-   WinSock DLL implementation
-   ❌ Failed due to complexity
-   Kept for educational purposes

### v2.0 - Python Rewrite

-   Full Python implementation
-   Native TCP sockets
-   Clean architecture
-   ✅ Production-ready

---

## 💡 Lessons Learned

1. **AHK is great for SendInput** - Keep it simple
2. **Python is great for TCP** - Use right tool for the job
3. **Don't mix languages unnecessarily** - Hybrid = complex
4. **TCP works better in Python** - Native socket library

---

## 🎯 Final Recommendations

### ✅ Production Use:

-   **Version 1.0** - For gaming, max performance
-   **Version 2.0** - For development, maintenance

### ❌ Avoid:

-   **Version 1.5** - Experimental, broken

### 📖 For Learning:

-   Study v1.0 for AHK techniques
-   Study v2.0 for TCP architecture
-   Study v1.5 for what NOT to do 😊

---

**Last Updated:** October 2025  
**Current Versions:** v1.0 (AHK) ✅ | v1.5 (AHK+TCP) ❌ | v2.0 (Python) ✅
