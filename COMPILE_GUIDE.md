# 🔧 COMPILE GUIDE - ANTI-DETECTION

## ✅ **WHY COMPILE?**

```
.ahk files:
  ❌ Easily detected by anti-cheat
  ❌ Can be read and analyzed
  ❌ Obvious it's an automation script

.exe files:
  ✅ Harder to detect
  ✅ Binary (can't be easily read)
  ✅ Can be renamed to look legitimate
  ✅ Better anti-detection!
```

---

## 🚀 **QUICK START (2 MINUTES):**

### **Option A: Simple Compile**

```bash
1. Double-click: compile_custom.bat

2. Wait for compilation...

3. Result: multiplicity_jitter_CUSTOM.exe ✅

4. Test: Double-click .exe → Should work like .ahk!

5. Use .exe instead of .ahk from now on!
```

---

### **Option B: Compile + Obfuscate (RECOMMENDED!)**

```bash
1. Double-click: compile_custom_obfuscate.bat

2. Choose obfuscated name:
   1. WindowsUpdateHelper.exe    ← BEST! ⭐
   2. SystemAudioService.exe
   3. DisplayManager.exe
   4. NetworkHelper.exe
   5. SecurityHelper.exe
   6. Custom name

3. Enter choice: 1 (recommended)

4. Wait for compilation...

5. Result: WindowsUpdateHelper.exe ✅

6. Test: Double-click → Works? ✅

7. Use this obfuscated .exe for farming!
```

**Why obfuscate?**

-   Anti-cheat sees "WindowsUpdateHelper.exe" → looks legitimate!
-   Much harder to detect than "multiplicity_jitter_CUSTOM.exe"

---

## 🎯 **DETAILED STEPS:**

### **STEP 1: Compile Script**

#### **Method 1: Using batch file (EASY):**

```bash
compile_custom.bat
```

Output: `multiplicity_jitter_CUSTOM.exe`

---

#### **Method 2: Using batch file with obfuscation (BEST!):**

```bash
compile_custom_obfuscate.bat
```

Choose name → Get obfuscated .exe!

---

#### **Method 3: Manual compile:**

```bash
"C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe" /in "multiplicity_jitter_CUSTOM.ahk" /out "multiplicity_jitter_CUSTOM.exe"
```

---

### **STEP 2: Test Compiled .exe**

```bash
1. Double-click the .exe

2. UAC prompt → Yes

3. Popup shows mappings ✅

4. Test in Notepad:
   Type: q w e r
   Shows: a s d f ✅

5. Works? → Next step!
```

---

### **STEP 3: Setup Autostart (Optional)**

```bash
1. Double-click: setup_autostart_custom.bat

2. Enter .exe filename: WindowsUpdateHelper.exe

3. Done! ✅

4. Script runs on Windows startup!
```

---

## 🎭 **OBFUSCATION NAMES:**

### **Recommended Names (Look Legitimate):**

| Name                      | Description                | Detection Risk  |
| ------------------------- | -------------------------- | --------------- |
| `WindowsUpdateHelper.exe` | Looks like Windows update  | Very Low ⭐⭐⭐ |
| `SystemAudioService.exe`  | Looks like audio driver    | Very Low ⭐⭐⭐ |
| `DisplayManager.exe`      | Looks like display driver  | Low ⭐⭐        |
| `NetworkHelper.exe`       | Looks like network utility | Low ⭐⭐        |
| `SecurityHelper.exe`      | Looks like security tool   | Medium ⭐       |

### **BAD Names (Avoid!):**

```
❌ multiplicity.exe       (obvious!)
❌ jitter.exe             (obvious!)
❌ bot.exe                (obvious!)
❌ auto.exe               (obvious!)
❌ remap.exe              (obvious!)
❌ macro.exe              (obvious!)
```

---

## 📊 **ANTI-DETECTION COMPARISON:**

| Method                        | Detection Risk | Setup Time |
| ----------------------------- | -------------- | ---------- |
| .ahk file (original)          | Very High ❌   | 0 min      |
| .exe (simple compile)         | Medium ⚠️      | 1 min      |
| .exe (obfuscated name)        | Low ✅         | 2 min      |
| .exe (obfuscated + autostart) | Very Low ✅✅  | 3 min      |

---

## ⚙️ **TECHNICAL DETAILS:**

### **What compilation does:**

```
1. Converts .ahk text → .exe binary
2. Embeds AHK runtime inside .exe
3. Makes script harder to analyze
4. Allows renaming without breaking
5. Can run without AHK installed
```

### **Compiler location:**

```
Default: C:\Program Files\AutoHotkey\Compiler\Ahk2Exe.exe
```

### **Compiler options:**

```bash
/in "input.ahk"      ← Source file
/out "output.exe"    ← Output file
/icon "icon.ico"     ← Custom icon (optional)
```

---

## 🧪 **TESTING:**

### **Test 1: Basic Functionality**

```bash
1. Run .exe (double-click)
2. Popup shows mappings? ✅
3. Test in Notepad (q → a)? ✅
4. Icon "H" in system tray? ✅
```

---

### **Test 2: Remap Working**

```bash
1. Open Notepad
2. Type: q w e r
3. Shows: a s d f ✅
```

---

### **Test 3: Jitter Working**

```bash
1. Open Notepad
2. Type: q w e r (quickly)
3. Letters appear with slight delay? ✅
4. Not all at once? ✅
```

---

### **Test 4: Exit Hotkey**

```bash
1. Press: Ctrl+Shift+Q
2. Popup: "Exiting..."? ✅
3. Script stops? ✅
4. Icon "H" disappears? ✅
```

---

## 🚀 **AUTOSTART SETUP:**

### **Why autostart?**

```
✅ Script runs automatically on boot
✅ No need to manually start
✅ Always active when farming
✅ Survives restarts
```

---

### **How to setup:**

```bash
1. Run: setup_autostart_custom.bat

2. Choose .exe: WindowsUpdateHelper.exe

3. Done! ✅

Registry entry created:
  Location: HKCU\Software\Microsoft\Windows\CurrentVersion\Run
  Name: WindowsJitterService
  Value: "C:\path\to\WindowsUpdateHelper.exe"
```

---

### **How to remove:**

```bash
1. Run: remove_autostart_custom.bat

2. Done! Autostart removed ✅
```

---

## ⚠️ **IMPORTANT NOTES:**

### **1. Keep source .ahk file:**

```
Keep: multiplicity_jitter_CUSTOM.ahk
Why:  If you want to change mappings later!

Workflow:
  1. Edit .ahk file
  2. Recompile to .exe
  3. Use new .exe
```

---

### **2. Antivirus false positive:**

```
Some antivirus may flag compiled AHK scripts!

If blocked:
  1. Add exception in antivirus
  2. Whitelist the .exe file
  3. OR use different obfuscated name
```

---

### **3. Update mappings:**

```
To change mappings:
  1. Edit .ahk file (change remap table)
  2. Recompile (run compile script again)
  3. Replace old .exe with new one
  4. If autostart: Update registry entry
```

---

### **4. Multiple VMs:**

```
For multiple VMs with different mappings:

VM1:
  1. Edit .ahk → Set VM1 mappings
  2. Compile as: WindowsUpdateHelper.exe
  3. Copy to VM1

VM2:
  1. Edit .ahk → Set VM2 mappings
  2. Compile as: SystemAudioService.exe
  3. Copy to VM2

VM3:
  1. Edit .ahk → Set VM3 mappings
  2. Compile as: DisplayManager.exe
  3. Copy to VM3
```

---

## 📋 **COMPLETE WORKFLOW:**

```
┌──────────────────────────────────────┐
│ 1. Edit .ahk file                    │
│    (Change remap table)              │
│         ↓                            │
│ 2. Compile with obfuscation          │
│    (compile_custom_obfuscate.bat)    │
│         ↓                            │
│ 3. Choose legitimate name            │
│    (WindowsUpdateHelper.exe)         │
│         ↓                            │
│ 4. Test .exe                         │
│    (Notepad: q → a)                  │
│         ↓                            │
│ 5. Setup autostart                   │
│    (setup_autostart_custom.bat)      │
│         ↓                            │
│ 6. Reboot and verify                 │
│    (Check if auto-runs)              │
│         ↓                            │
│ 7. Use in game! 🎉                   │
└──────────────────────────────────────┘
```

Total time: ~5 minutes per VM!

---

## 💡 **PRO TIPS:**

```
✅ Use obfuscated names (WindowsUpdateHelper.exe)
✅ Setup autostart for convenience
✅ Keep backup of working .ahk file
✅ Test in Notepad before game
✅ Different names per VM (avoid detection)
✅ Recompile after changing mappings
✅ Add antivirus exception if needed
```

---

## 🎉 **YOU'RE READY!**

```
╔════════════════════════════════════════════════════╗
║                                                    ║
║   🔧 COMPILE COMPLETE! 🔧                         ║
║                                                    ║
║   ✅ .ahk → .exe (harder to detect)               ║
║   ✅ Obfuscated name (looks legitimate)           ║
║   ✅ Autostart (runs on boot)                     ║
║   ✅ Ready for farming! 🚀                        ║
║                                                    ║
║   Detection risk: VERY LOW! ✅✅                  ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

---

**🚀 START: Run `compile_custom_obfuscate.bat`!**

**🎭 NAME: Choose `WindowsUpdateHelper.exe`!**

**🔧 AUTOSTART: Run `setup_autostart_custom.bat`!**

**🎉 FARM: Start farming safely!** ✨
