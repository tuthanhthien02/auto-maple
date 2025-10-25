# 🎨 START HERE - CUSTOM REMAP VERSION!

## ✅ **NEW FILE: `multiplicity_jitter_CUSTOM.ahk`**

**CỰC KỲ DỄ CHỈNH SỬA!** Chỉ cần edit 1 table! 🚀

---

## 🆚 **SO SÁNH: OLD vs NEW**

### **❌ OLD WAY (Hard to edit):**

```ahk
; Host Q → VM1 sends P
$q::
    ApplyJitterAndSend("p")
    return

; Host W → VM1 sends [
$w::
    ApplyJitterAndSend("[")
    return

; Host E → VM1 sends ]
$e::
    ApplyJitterAndSend("]")
    return

; Need to edit 3 lines per mapping! 😰
; Need to know AHK syntax! 😰
```

---

### **✅ NEW WAY (Super easy!):**

```ahk
; 🎨 REMAP TABLE - EDIT HERE!
remap["q"] := "a"  ← Just change this!
remap["w"] := "s"  ← Just change this!
remap["e"] := "d"  ← Just change this!
remap["r"] := "f"  ← Just change this!

; ONE line per mapping! ✅
; No AHK knowledge needed! ✅
```

---

## 🎯 **CURRENT SETUP (Q W E R → A S D F):**

```
Host sends Q → Multiplicity → VM receives Q
                                  ↓
                             AHK blocks Q
                                  ↓
                           Jitter 30-80ms
                                  ↓
                              Send A
                                  ↓
                          Game receives A
```

**In-game keybinding:** Skill 1 → bind to **A** (not Q!)

---

## 🚀 **QUICK START (2 MINUTES):**

### **STEP 1: Run Script (30 sec)**

```bash
1. Double-click: multiplicity_jitter_CUSTOM.ahk

2. UAC prompt → Yes

3. Popup shows all mappings:
   q → a
   w → s
   e → d
   r → f
   ...

4. Click OK

5. Icon "H" in system tray ✅
```

---

### **STEP 2: Test in Notepad (30 sec)**

```bash
1. Open Notepad

2. Type: q w e r

3. EXPECTED: a s d f ✅

4. Works? → Next step!
```

---

### **STEP 3: Configure In-Game (1 min)**

```bash
In MapleStory:

1. ESC → Settings → Key Settings

2. Skill 1 → Click → Press A (not Q!)
   (Because Q now sends A!)

3. Skill 2 → Click → Press S (not W!)
   (Because W now sends S!)

4. Skill 3 → Click → Press D (not E!)
   (Because E now sends D!)

5. Skill 4 → Click → Press F (not R!)
   (Because R now sends F!)

6. Save → Test in game!
```

---

### **STEP 4: Test In-Game (30 sec)**

```bash
1. In MapleStory

2. Press Q on host → Skill 1 activates? ✅

3. Press W → Skill 2 activates? ✅

4. Press E → Skill 3 activates? ✅

5. Works? → READY TO FARM! 🎉
```

---

## 🎨 **CUSTOMIZE MAPPINGS:**

### **Want different keys? SUPER EASY:**

```bash
1. Right-click: multiplicity_jitter_CUSTOM.ahk
   → Edit Script

2. Find line ~50:
   remap["q"] := "a"

3. Change to whatever you want:
   remap["q"] := "p"  ← Now Q sends P!
   remap["q"] := "F1" ← Now Q sends F1!
   remap["q"] := "Home" ← Now Q sends Home!

4. Save (Ctrl+S)

5. Restart script:
   - Right-click H icon → Exit
   - Double-click script again

6. Test in Notepad → Works? → Use in game!
```

---

## 📋 **COMMON MAPPINGS:**

### **Option A: Q W E R → A S D F (Current):**

```ahk
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
```

In-game: Skill 1 → A, Skill 2 → S, Skill 3 → D, Skill 4 → F

---

### **Option B: Q W E R → 1 2 3 4:**

```ahk
remap["q"] := "1"
remap["w"] := "2"
remap["e"] := "3"
remap["r"] := "4"
```

In-game: Skill 1 → 1, Skill 2 → 2, Skill 3 → 3, Skill 4 → 4

---

### **Option C: Q W E R → F1 F2 F3 F4:**

```ahk
remap["q"] := "F1"
remap["w"] := "F2"
remap["e"] := "F3"
remap["r"] := "F4"
```

In-game: Skill 1 → F1, Skill 2 → F2, Skill 3 → F3, Skill 4 → F4

---

### **Option D: Q W E R → U I O P:**

```ahk
remap["q"] := "u"
remap["w"] := "i"
remap["e"] := "o"
remap["r"] := "p"
```

In-game: Skill 1 → U, Skill 2 → I, Skill 3 → O, Skill 4 → P

---

## ⚙️ **CHANGE JITTER (DELAY):**

Edit lines 38-39:

```ahk
global MinJitter := 30  ← Minimum delay (ms)
global MaxJitter := 80  ← Maximum delay (ms)
```

**Examples:**

```ahk
; Fast (almost instant)
MinJitter := 10
MaxJitter := 30

; Medium (current)
MinJitter := 30
MaxJitter := 80

; Slow (more human)
MinJitter := 80
MaxJitter := 150

; Testing (very obvious delay)
MinJitter := 200
MaxJitter := 500
```

---

## 🎯 **KEY FEATURES:**

```
✅ Edit ONE table for all mappings
✅ Add new mapping: Just add one line!
✅ Remove mapping: Delete or comment out (;)
✅ Change mapping: Just edit the output key!
✅ No AHK knowledge needed
✅ Popup shows all mappings on startup
✅ Auto-generates hotkeys from table
✅ Still has jitter (30-80ms Gaussian)
✅ Still has $ prefix (no chain remap)
✅ Auto-elevates to admin
```

---

## 📚 **DOCUMENTATION:**

```
START_HERE_CUSTOM.md  ← This file (quick start)
CUSTOM_REMAP_GUIDE.md ← Full guide with examples
multiplicity_jitter_CUSTOM.ahk ← The script!
```

---

## 🎉 **YOU'RE READY!**

```
╔════════════════════════════════════════════════╗
║                                                ║
║  🎨 EASIEST MULTIPLICITY JITTER EVER! 🎨      ║
║                                                ║
║  ✅ Run: Double-click script                  ║
║  ✅ Test: Notepad (q w e r → a s d f)        ║
║  ✅ Config: In-game keybindings to A S D F    ║
║  ✅ Play: Host press Q, game gets A!          ║
║                                                ║
║  Want different keys?                          ║
║  → Edit remap table (1 line per key!)         ║
║  → Save, restart, done! 🚀                    ║
║                                                ║
╚════════════════════════════════════════════════╝
```

---

## 🔄 **EDIT → SAVE → RESTART WORKFLOW:**

```bash
┌─────────────────────────────────────┐
│ 1. Edit remap table                 │
│    remap["q"] := "a"                │
│         ↓                           │
│ 2. Save (Ctrl+S)                    │
│         ↓                           │
│ 3. Close script (H icon → Exit)    │
│         ↓                           │
│ 4. Run script (double-click)        │
│         ↓                           │
│ 5. Popup shows new mappings ✅      │
│         ↓                           │
│ 6. Test in Notepad                  │
│         ↓                           │
│ 7. Use in game! 🎉                  │
└─────────────────────────────────────┘
```

**Total time: 30 seconds to change mappings!** ⚡

---

**🚀 Start: Double-click `multiplicity_jitter_CUSTOM.ahk`!**

**🎨 Customize: Edit remap table anytime!** ✨

**📖 More info: Read `CUSTOM_REMAP_GUIDE.md`!** 📚
