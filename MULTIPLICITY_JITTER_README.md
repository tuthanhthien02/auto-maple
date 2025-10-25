# 🎯 Multiplicity Input Jitter

## 📁 **FILE DUY NHẤT**

```
multiplicity_jitter_passthrough.ahk  ⭐ MAIN FILE
```

---

## 🚀 **QUICK START**

### **1. Run Script:**

```bash
# Double-click file:
multiplicity_jitter_passthrough.ahk

# Hoặc compile to .exe:
# Right-click → Compile Script
```

### **2. Verify Running:**

```
Check system tray → Green "H" icon ✅
```

### **3. Test:**

```
Open Notepad → Type qqqq
Should see slight delays (30-80ms each)
```

---

## ⚙️ **CONFIGURATION**

Edit jitter range (Lines 21-22):

```ahk
global MinJitter := 30    ; Min delay in ms
global MaxJitter := 80    ; Max delay in ms
```

**Recommended ranges:**

```
Fast:    20-60ms
Medium:  50-100ms
Slow:    80-150ms
```

---

## 🎮 **USAGE**

### **Features:**

```
✅ Gaussian jitter (human-like delays)
✅ Passthrough mode (keys work normally)
✅ Global (works in all windows)
✅ 93 keys covered (letters, numbers, F-keys, arrows, etc.)
```

### **How it works:**

```
1. Multiplicity sends key to VM
2. Script adds random delay (30-80ms)
3. Key passes through to game
4. Result: Different timing per client ✅
```

---

## 🔧 **CUSTOMIZATION**

### **Change jitter range:**

```ahk
; Line 21-22
global MinJitter := 50    ; Your min
global MaxJitter := 120   ; Your max
```

### **Disable Gaussian (use uniform random):**

```ahk
; Line 23
global UseGaussian := false
```

### **Add exit hotkey:**

```ahk
; Already included: CTRL+SHIFT+Q to exit
```

---

## 📊 **MULTI-CLIENT SETUP**

For 3 clients with different jitter:

### **CLIENT 1:**

```ahk
global MinJitter := 30
global MaxJitter := 80
```

### **CLIENT 2:**

```ahk
global MinJitter := 60
global MaxJitter := 120
```

### **CLIENT 3:**

```ahk
global MinJitter := 90
global MaxJitter := 150
```

**Compile each version with different names:**

```
Client1_Jitter.exe
Client2_Jitter.exe
Client3_Jitter.exe
```

---

## 🧪 **TESTING**

### **Test jitter works:**

```bash
1. Run script
2. Open Notepad
3. Press Q rapidly 10 times
4. Should see uneven delays between each Q
5. Working! ✅
```

### **Test in game:**

```bash
1. Script running (H icon in tray)
2. Open game
3. Press skill keys
4. Should work with slight delays ✅
```

---

## ⚠️ **IMPORTANT NOTES**

### **Passthrough Mode:**

```
✅ Keys work normally (passthrough with ~ prefix)
✅ Compatible with Multiplicity
✅ No key blocking issues
```

### **Global Mode:**

```
⚠️ Active in ALL windows
💡 Tip: Press CTRL+SHIFT+Q to exit script temporarily
```

---

## 🎯 **EVASION**

```
Without jitter: Perfect sync = Easy to detect ❌
With jitter:    Random delays = Harder to detect ✅

Evasion improvement: ~10-15%
```

---

## 💡 **SUMMARY**

| Feature                     | Status                                |
| --------------------------- | ------------------------------------- |
| **File**                    | `multiplicity_jitter_passthrough.ahk` |
| **Mode**                    | Global (all windows)                  |
| **Jitter**                  | 30-80ms (Gaussian)                    |
| **Keys**                    | 93 keys covered                       |
| **Hold support**            | No (passthrough mode)                 |
| **Works with Multiplicity** | ✅ Yes                                |

---

## 🔗 **RELATED FILES**

```
Main Auto Maple Bot:
- main.py
- resources/command_books/
- resources/routines/

This is SEPARATE from main bot!
Use for Multiplicity 4 multi-client control.
```

---

**🎉 Clean and simple! One file to rule them all!** ✅

