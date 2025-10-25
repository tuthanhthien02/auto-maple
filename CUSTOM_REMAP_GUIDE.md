# 🎨 CUSTOM REMAP GUIDE - DỄ DÀNG CHỈNH SỬA!

## ✅ **FILE MỚI: `multiplicity_jitter_CUSTOM.ahk`**

Script này **CỰC KỲ DỄ CUSTOM!**

Chỉ cần edit **REMAP TABLE** - không cần biết code AHK! ✨

---

## 🎯 **CURRENT MAPPINGS (Q W E R → A S D F):**

```ahk
remap["q"] := "a"  ← Q sends A
remap["w"] := "s"  ← W sends S
remap["e"] := "d"  ← E sends D
remap["r"] := "f"  ← R sends F
```

---

## 📝 **CÁCH EDIT:**

### **1. MỞ FILE:**

```
Right-click: multiplicity_jitter_CUSTOM.ahk
→ Edit Script (or open in Notepad)
```

---

### **2. TÌM SECTION "REMAP TABLE" (Line ~43):**

```ahk
; ═══════════════════════════════════════════════════════════
; 🎨 REMAP TABLE - EDIT HERE TO CHANGE MAPPINGS!
; ═══════════════════════════════════════════════════════════

global remap := {}

; MAIN KEYS (Q W E R → A S D F)
remap["q"] := "a"  ← EDIT THIS LINE!
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
```

---

### **3. THAY ĐỔI THEO Ý BẠN:**

#### **Example 1: Change Q → P instead of A:**

```ahk
Before:
  remap["q"] := "a"

After:
  remap["q"] := "p"  ← Changed!
```

---

#### **Example 2: Add new mapping (F → V):**

```ahk
remap["f"] := "v"  ← Add this line!
```

---

#### **Example 3: Remove a mapping (comment out):**

```ahk
Before:
  remap["z"] := "m"

After:
  ; remap["z"] := "m"  ← Commented out, Z not remapped
```

---

#### **Example 4: Remap to F-keys:**

```ahk
remap["q"] := "F1"
remap["w"] := "F2"
remap["e"] := "F3"
remap["r"] := "F4"
```

---

#### **Example 5: Remap to special keys:**

```ahk
remap["q"] := "Home"
remap["w"] := "End"
remap["e"] := "PgUp"
remap["r"] := "PgDn"
remap["t"] := "Insert"
remap["y"] := "Delete"
```

---

## 📚 **AVAILABLE KEY NAMES:**

### **Letters:**

```
a b c d e f g h i j k l m n o p q r s t u v w x y z
```

### **Numbers:**

```
0 1 2 3 4 5 6 7 8 9
```

### **Numpad:**

```
Numpad0 Numpad1 Numpad2 ... Numpad9
NumpadAdd (+)
NumpadSub (-)
NumpadMult (*)
NumpadDiv (/)
NumpadDot (.)
NumpadEnter
```

### **Function Keys:**

```
F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12
```

### **Special Keys:**

```
Home End PgUp PgDn Insert Delete
Left Right Up Down
Space Enter Tab Backspace Escape
```

### **Symbols:**

```
; ' , . / [ ] \ - =
` (backtick - use `` in AHK)
```

---

## ⚙️ **CHANGE JITTER SETTINGS:**

Edit lines 38-39:

```ahk
global MinJitter := 30  ← Change minimum delay
global MaxJitter := 80  ← Change maximum delay
```

**Examples:**

```ahk
; Fast (almost instant)
global MinJitter := 10
global MaxJitter := 30

; Medium (balanced)
global MinJitter := 30
global MaxJitter := 80

; Slow (more human-like)
global MinJitter := 80
global MaxJitter := 150

; Very slow (testing)
global MinJitter := 200
global MaxJitter := 500
```

---

## 🔄 **APPLY CHANGES:**

```bash
1. Edit script (change remap table)

2. SAVE file (Ctrl+S)

3. CLOSE old script:
   Right-click H icon → Exit

4. RUN new version:
   Double-click multiplicity_jitter_CUSTOM.ahk

5. Popup shows NEW mappings ✅

6. Test in Notepad or keytest.vn!
```

---

## 🧪 **TEST YOUR MAPPINGS:**

```bash
1. Open Notepad

2. Enable Multiplicity broadcast

3. Type: Q W E R

4. EXPECTED:
   Notepad: a s d f ✅
   (or whatever you configured!)

5. If correct → Test in game!
```

---

## 📋 **COMPLETE EXAMPLES:**

### **Example A: QWER → ASDF (Current):**

```ahk
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"
```

---

### **Example B: QWER → 1234:**

```ahk
remap["q"] := "1"
remap["w"] := "2"
remap["e"] := "3"
remap["r"] := "4"
```

---

### **Example C: QWER → UIOP:**

```ahk
remap["q"] := "u"
remap["w"] := "i"
remap["e"] := "o"
remap["r"] := "p"
```

---

### **Example D: QWER → F1-F4:**

```ahk
remap["q"] := "F1"
remap["w"] := "F2"
remap["e"] := "F3"
remap["r"] := "F4"
```

---

### **Example E: Skills + Potions:**

```ahk
; Skills (QWER → ASDF)
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"

; Potions (1234 → Numpad)
remap["1"] := "Numpad1"
remap["2"] := "Numpad2"
remap["3"] := "Numpad3"
remap["4"] := "Numpad4"

; Mount (Space → F12)
remap["Space"] := "F12"
```

---

## ⚠️ **IMPORTANT NOTES:**

### **1. Use lowercase for input keys:**

```ahk
✅ remap["q"] := "a"
❌ remap["Q"] := "a"  (wrong!)
```

---

### **2. Output keys can be any case:**

```ahk
✅ remap["q"] := "A"  (works, same as "a")
✅ remap["q"] := "a"  (works)
```

---

### **3. Backtick needs double ``:**

```ahk
✅ remap["y"] := "``"  (correct!)
❌ remap["y"] := "`"   (wrong!)
```

---

### **4. Don't remap to same key:**

```ahk
❌ remap["q"] := "q"  (pointless, causes issues)
```

If you don't want to remap a key, just don't add it to the table!

---

### **5. Arrow keys NOT remapped by default:**

```
Arrow keys, Space, Ctrl, Alt, Shift: Work normally!
Only keys in remap table are affected.
```

To remap arrow keys:

```ahk
remap["Up"] := "w"
remap["Down"] := "s"
remap["Left"] := "a"
remap["Right"] := "d"
```

---

## 🎯 **QUICK WORKFLOW:**

```
1. Edit: Open multiplicity_jitter_CUSTOM.ahk
2. Find: "REMAP TABLE" section (line ~43)
3. Change: remap["q"] := "a" to whatever you want
4. Add: New lines for new mappings
5. Remove: Comment out with ; or delete line
6. Save: Ctrl+S
7. Restart: Close old script, run new one
8. Test: Notepad → Type keys → See output
9. Play: Use in game!
```

---

## 💡 **PRO TIPS:**

```
✅ Keep a backup of working config
✅ Test in Notepad first, then game
✅ Start with few mappings, add more later
✅ Use consistent pattern (e.g., all F-keys, all Numpad)
✅ Comment your mappings for clarity:

remap["q"] := "a"  ; Skill 1 - Teleport
remap["w"] := "s"  ; Skill 2 - Buff
remap["e"] := "d"  ; Skill 3 - Attack
```

---

## 🎉 **YOU'RE READY!**

```
╔════════════════════════════════════════╗
║                                        ║
║  🎨 EASIEST REMAP SCRIPT EVER! 🎨     ║
║                                        ║
║  ✅ Edit remap table only             ║
║  ✅ No AHK knowledge needed           ║
║  ✅ Add/remove mappings easily        ║
║  ✅ See all mappings in popup         ║
║  ✅ Auto-generates hotkeys            ║
║                                        ║
║  Just edit, save, restart! 🚀         ║
║                                        ║
╚════════════════════════════════════════╝
```

---

**📖 File: `multiplicity_jitter_CUSTOM.ahk`**

**🎨 Edit the REMAP TABLE and you're done!** ✨
