# 🎨 KEY REMAP EXAMPLES - Visual Guide

## 📋 **COMMON REMAP PATTERNS**

---

## 🎯 **PATTERN 1: SIMPLE SWAP (Easiest)**

### **Use Case:** Minimal changes, easy to remember

### **CLIENT 1: No Remap**

```ahk
global KeyRemap := {}
# Keep everything default
```

### **CLIENT 2: Swap Q and O**

```ahk
KeyRemap["q"] := "o"
KeyRemap["o"] := "q"
```

### **CLIENT 3: Swap W and P**

```ahk
KeyRemap["w"] := "p"
KeyRemap["p"] := "w"
```

### **Visual:**

```
HOST PRESSES:  Q    W    E    R
                ↓    ↓    ↓    ↓
CLIENT 1:      Q    W    E    R  (No change)
CLIENT 2:      O    W    E    R  (Q→O)
CLIENT 3:      Q    P    E    R  (W→P)
```

### **In-Game Keybindings:**

| Skill           | CLIENT 1 | CLIENT 2 | CLIENT 3 |
| --------------- | -------- | -------- | -------- |
| Primary Attack  | Q        | **O**    | Q        |
| Secondary Skill | W        | W        | **P**    |
| Buff            | E        | E        | E        |
| Ultimate        | R        | R        | R        |

---

## 🎯 **PATTERN 2: SKILL ROW REMAP (Moderate)**

### **Use Case:** Main attack keys different on each client

### **CLIENT 1: Minimal**

```ahk
KeyRemap["q"] := "u"
```

### **CLIENT 2: Shift Right**

```ahk
KeyRemap["q"] := "o"
KeyRemap["w"] := "p"
KeyRemap["e"] := "["
```

### **CLIENT 3: Different Row**

```ahk
KeyRemap["q"] := "l"
KeyRemap["w"] := ";"
KeyRemap["e"] := "'"
```

### **Visual:**

```
HOST PRESSES:  Q    W    E
                ↓    ↓    ↓
CLIENT 1:      U    W    E
CLIENT 2:      O    P    [
CLIENT 3:      L    ;    '
```

### **Keyboard Layout:**

```
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│ Q  │ W  │ E  │ R  │ T  │ Y  │ U  │ I  │ O  │ P  │
│ C1 │    │    │    │    │    │C1→│    │C2→│    │
└────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
┌────┬────┬────┬────┬────┬────┬────┬────┬────┬────┐
│ A  │ S  │ D  │ F  │ G  │ H  │ J  │ K  │ L  │ ;  │
│    │    │    │    │    │    │    │    │C3→│C3→│
└────┴────┴────┴────┴────┴────┴────┴────┴────┴────┘
```

---

## 🎯 **PATTERN 3: FULL SKILLS REMAP (Maximum)**

### **Use Case:** Maximum differentiation, hardest to detect

### **CLIENT 1: Minimal**

```ahk
KeyRemap["q"] := "i"
KeyRemap["e"] := "u"
```

### **CLIENT 2: Upper Right**

```ahk
KeyRemap["q"] := "o"
KeyRemap["w"] := "p"
KeyRemap["e"] := "["
KeyRemap["r"] := "]"
KeyRemap["a"] := "l"
KeyRemap["s"] := ";"
```

### **CLIENT 3: Lower Right**

```ahk
KeyRemap["q"] := "l"
KeyRemap["w"] := ";"
KeyRemap["e"] := "'"
KeyRemap["r"] := "/"
KeyRemap["a"] := "k"
KeyRemap["s"] := "j"
KeyRemap["d"] := "h"
```

### **Visual:**

```
HOST PRESSES:  Q    W    E    R    A    S    D
                ↓    ↓    ↓    ↓    ↓    ↓    ↓
CLIENT 1:      I    W    U    R    A    S    D
CLIENT 2:      O    P    [    ]    L    ;    D
CLIENT 3:      L    ;    '    /    K    J    H
```

---

## 🎯 **PATTERN 4: NUMBER KEYS REMAP**

### **Use Case:** Potion/buff hotkeys different

### **CLIENT 1: Default**

```ahk
# No remap
```

### **CLIENT 2: Shift +3**

```ahk
KeyRemap["1"] := "4"
KeyRemap["2"] := "5"
KeyRemap["3"] := "6"
```

### **CLIENT 3: Shift +6**

```ahk
KeyRemap["1"] := "7"
KeyRemap["2"] := "8"
KeyRemap["3"] := "9"
```

### **Visual:**

```
HOST PRESSES:  1    2    3
                ↓    ↓    ↓
CLIENT 1:      1    2    3  (No change)
CLIENT 2:      4    5    6  (Shift +3)
CLIENT 3:      7    8    9  (Shift +6)
```

---

## 🎯 **PATTERN 5: FUNCTION KEYS REMAP**

### **Use Case:** Buff keys different on each client

### **CLIENT 1: Default**

```ahk
# No remap
```

### **CLIENT 2: Shift +2**

```ahk
KeyRemap["f1"] := "f3"
KeyRemap["f2"] := "f4"
```

### **CLIENT 3: Shift +4**

```ahk
KeyRemap["f1"] := "f5"
KeyRemap["f2"] := "f6"
```

### **Visual:**

```
HOST PRESSES:  F1   F2
                ↓    ↓
CLIENT 1:      F1   F2  (No change)
CLIENT 2:      F3   F4  (Shift +2)
CLIENT 3:      F5   F6  (Shift +4)
```

---

## 🎯 **PATTERN 6: MIXED REMAP (Recommended)**

### **Best balance of safety and ease of use**

### **CLIENT 1: Minimal (Fast Player)**

```ahk
KeyRemap["q"] := "u"
```

### **CLIENT 2: Moderate (Medium Player)**

```ahk
# Skills
KeyRemap["q"] := "o"
KeyRemap["e"] := "["

# Potions
KeyRemap["1"] := "5"
KeyRemap["2"] := "6"
```

### **CLIENT 3: Maximum (Slow Player)**

```ahk
# Skills
KeyRemap["q"] := "l"
KeyRemap["w"] := ";"
KeyRemap["e"] := "'"

# Potions
KeyRemap["1"] := "7"
KeyRemap["2"] := "8"

# Buffs
KeyRemap["f1"] := "f5"
```

### **Summary Table:**

| Key | CLIENT 1 | CLIENT 2 | CLIENT 3 | Anti-Cheat Sees     |
| --- | -------- | -------- | -------- | ------------------- |
| Q   | U        | O        | L        | 3 different keys ✅ |
| W   | W        | W        | ;        | 2 different keys ✅ |
| E   | E        | [        | '        | 3 different keys ✅ |
| 1   | 1        | 5        | 7        | 3 different keys ✅ |
| 2   | 2        | 6        | 8        | 3 different keys ✅ |
| F1  | F1       | F1       | F5       | 2 different keys ✅ |

---

## 📝 **HOW TO CHOOSE YOUR PATTERN**

### **Easy (Pattern 1-2):**

```
✅ Simple to remember
✅ Easy to set up in-game
✅ Still effective
⚠️ Less differentiation
```

### **Moderate (Pattern 3-4):**

```
✅ Good balance
✅ More differentiation
✅ Manageable complexity
⚠️ Need careful in-game setup
```

### **Maximum (Pattern 5-6):**

```
✅ Maximum evasion
✅ Very different patterns
⚠️ Complex to set up
⚠️ Easy to make mistakes
```

---

## 🎯 **RECOMMENDED FOR BEGINNERS**

Start with **PATTERN 6 (Mixed Remap)**:

-   Easy enough to manage
-   Effective enough for safety
-   Good balance!

---

## 🧪 **TEST YOUR REMAP**

### **Step 1: Test in Notepad**

```
1. Run .ahk script
2. Open Notepad
3. Press Q → Should type remapped key
4. Press all remapped keys to verify
```

### **Step 2: Test in MapleStory (Training Map)**

```
1. Go to safe training map
2. Test each skill key
3. Verify skills cast correctly
4. Check timing feels natural
```

### **Step 3: Verify All 3 Clients**

```
1. Host presses Q
2. All 3 clients should cast same skill
3. Check game receives different keys (Q, O, L)
4. Success! ✅
```

---

## ⚠️ **COMMON MISTAKES**

### **❌ Mistake 1: Forgot to update in-game keybindings**

```
Problem: Skill doesn't cast on CLIENT 2/3
Solution: Bind skill to REMAPPED key in-game
```

### **❌ Mistake 2: Same remap on multiple clients**

```
Problem: Defeats the purpose!
Solution: Each client should have DIFFERENT remaps
```

### **❌ Mistake 3: Circular remap conflicts**

```
Problem: Q→O and O→Q on SAME client won't work right
Solution: Test in Notepad first!
```

### **❌ Mistake 4: Remapped to non-existent keys**

```
Problem: Can't bind in-game
Solution: Use standard keyboard keys only
```

---

## 🚀 **QUICK START TEMPLATE**

Copy this to your CLIENT scripts:

```ahk
; ═══════════════════════════════════════════════════════════
; CLIENT X CUSTOM REMAPS
; ═══════════════════════════════════════════════════════════

global KeyRemap := {}

; ──────────────────────────────────────────────────────────
; SKILL KEYS (QWER)
; ──────────────────────────────────────────────────────────
KeyRemap["q"] := "o"   ; Primary attack
KeyRemap["w"] := "p"   ; Secondary skill
KeyRemap["e"] := "["   ; Third skill
; KeyRemap["r"] := "]" ; Ultimate

; ──────────────────────────────────────────────────────────
; POTION KEYS (123)
; ──────────────────────────────────────────────────────────
KeyRemap["1"] := "5"   ; HP potion
KeyRemap["2"] := "6"   ; MP potion
; KeyRemap["3"] := "7" ; Buff potion

; ──────────────────────────────────────────────────────────
; BUFF KEYS (F1-F4)
; ──────────────────────────────────────────────────────────
; KeyRemap["f1"] := "f5"
; KeyRemap["f2"] := "f6"

; ──────────────────────────────────────────────────────────
; ADD MORE REMAPS HERE
; ──────────────────────────────────────────────────────────
```

---

**🎉 Choose your pattern and customize!**

Full guide: `LAYER_4_5_REMAP_JITTER_GUIDE.md`
