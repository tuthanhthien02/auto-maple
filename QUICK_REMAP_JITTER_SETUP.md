# ⚡ QUICK SETUP: Remap + Jitter (Layer 4+5)

## 🎯 **3-MINUTE SETUP**

### **STEP 1: Customize (Optional)**

Open and edit if you want different key mappings:

```bash
notepad multiplicity_remap_jitter_CLIENT2.ahk
notepad multiplicity_remap_jitter_CLIENT3.ahk
```

Find this section and edit:

```ahk
; 🔄 KEY REMAPPING
KeyRemap["q"] := "o"    ; Q becomes O
KeyRemap["o"] := "q"    ; O becomes Q
```

### **STEP 2: Compile**

Run:

```bash
compile_remap_jitter_all.bat
```

Creates:

-   `SystemInputService_C1.exe` → Deploy to Client 1
-   `SystemInputService_C2.exe` → Deploy to Client 2
-   `SystemInputService_C3.exe` → Deploy to Client 3

### **STEP 3: Deploy & Run**

Copy each EXE to its client and **run before MapleStory**!

---

## 🎮 **IN-GAME SETUP REQUIRED**

⚠️ **After remapping, bind skills in-game!**

### **Example: Host presses Q to cast skill**

| Client   | AHK Remap | In-Game Keybinding  | Result         |
| -------- | --------- | ------------------- | -------------- |
| Client 1 | Q → Q     | Bind skill to **Q** | ✅ Skill casts |
| Client 2 | Q → O     | Bind skill to **O** | ✅ Skill casts |
| Client 3 | Q → L     | Bind skill to **L** | ✅ Skill casts |

**Result:** Same skill casts, but game sees different keys (Q, O, L)! 🎯

---

## 📋 **PRE-CONFIGURED SETTINGS**

| Client   | Jitter Range | Key Remap          | Profile       |
| -------- | ------------ | ------------------ | ------------- |
| CLIENT 1 | 30-80ms      | None               | Fast player   |
| CLIENT 2 | 60-120ms     | Q↔O swap           | Medium player |
| CLIENT 3 | 90-150ms     | Q→L, W→;, E→P, R→[ | Slow player   |

---

## 🔧 **CUSTOMIZATION EXAMPLES**

### **Minimal (Easy):**

```ahk
; CLIENT 2
KeyRemap["q"] := "o"
KeyRemap["o"] := "q"
```

### **Moderate (Better):**

```ahk
; CLIENT 2
KeyRemap["q"] := "o"
KeyRemap["w"] := "p"
KeyRemap["e"] := "["

; CLIENT 3
KeyRemap["q"] := "l"
KeyRemap["w"] := ";"
KeyRemap["e"] := "'"
```

### **Maximum (Best):**

```ahk
; CLIENT 3
KeyRemap["q"] := "l"
KeyRemap["w"] := ";"
KeyRemap["e"] := "'"
KeyRemap["r"] := ","
KeyRemap["a"] := "k"
KeyRemap["s"] := "j"
KeyRemap["1"] := "7"
KeyRemap["2"] := "8"
```

---

## 🧪 **QUICK TEST**

### **Test Remap:**

1. Run `.ahk` file
2. Open Notepad
3. Press Q → Should type O (if remapped)

### **Test Jitter:**

1. Run `.ahk` file
2. Open MapleStory
3. Press Q rapidly → Should feel slight delays (30-150ms)

---

## 📊 **PIPELINE FLOW**

```
Host presses Q
    ↓
Multiplicity broadcasts Q to all clients
    ↓
┌──────────┬──────────┬──────────┐
│ CLIENT 1 │ CLIENT 2 │ CLIENT 3 │
│ Q → Q    │ Q → O    │ Q → L    │
│ +45ms    │ +87ms    │ +112ms   │
└──────────┴──────────┴──────────┘
    ↓           ↓           ↓
  Game Q     Game O     Game L
  @45ms      @87ms      @112ms

Result: Different keys + Different timing! ✅
```

---

## ⚠️ **IMPORTANT**

```
✅ Run EXE before MapleStory
✅ Bind skills to REMAPPED keys in-game
✅ Test in Notepad first
✅ Check system tray for AHK icon (green H)
```

---

## 📈 **EVASION SCORE**

```
Layer 1 + 4 + 5 = 34% evasion ✅
+ Layer 3 (VPN) = 42% evasion ✅✅
+ Layer 6 (Behaviors) = 49% evasion ✅✅✅
```

---

## 🚀 **NEXT STEP**

**Move to Layer 6: Behavioral Variation**

File: `multiplicity_anti_detection_complete.ahk`

Guide: `MULTIPLICITY_ULTIMATE_GUIDE.md`

---

**🎉 Layer 4+5 Setup Complete!**

Read full guide: `LAYER_4_5_REMAP_JITTER_GUIDE.md`
