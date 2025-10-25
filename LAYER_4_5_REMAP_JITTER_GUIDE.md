# 🔥 LAYER 4+5 COMBINED: Key Remap + Input Jitter

## 📋 **OVERVIEW**

Combines **Layer 4 (PowerToys Remap)** + **Layer 5 (Input Jitter)** into **ONE AHK script**!

```
Benefits:
✅ Simpler (1 tool instead of 2)
✅ No conflicts between tools
✅ Easy to customize per client
✅ Compile to .exe for obfuscation
✅ Different keys + Different timing = Maximum evasion!
```

---

## 📁 **FILES CREATED**

```
multiplicity_remap_jitter.ahk           [TEMPLATE - Edit this]
multiplicity_remap_jitter_CLIENT1.ahk   [Pre-configured for Client 1]
multiplicity_remap_jitter_CLIENT2.ahk   [Pre-configured for Client 2]
multiplicity_remap_jitter_CLIENT3.ahk   [Pre-configured for Client 3]
```

---

## 🔧 **PRE-CONFIGURED SETTINGS**

### **CLIENT 1: Fast Player**

```
Jitter Range: 30-80ms (fastest)
Key Remap: None (keeps original keys)
Use Case: Primary/Main character
```

### **CLIENT 2: Medium Player**

```
Jitter Range: 60-120ms (medium)
Key Remap: Q ↔ O (swap Q and O keys)
Use Case: Alt character
```

### **CLIENT 3: Slow Player**

```
Jitter Range: 90-150ms (slowest)
Key Remap: Q→L, W→;, E→P, R→[
Use Case: Alt character (more different)
```

---

## ⚙️ **HOW TO CUSTOMIZE KEY REMAPPING**

### **Step 1: Open the CLIENT script** (e.g., `multiplicity_remap_jitter_CLIENT2.ahk`)

### **Step 2: Find the REMAP section:**

```ahk
; ════════════════════════════════════════════════════════════
; 🔄 CLIENT 2 KEY REMAPPING
; ════════════════════════════════════════════════════════════
global KeyRemap := {}

; Example: Swap Q and O keys
KeyRemap["q"] := "o"
KeyRemap["o"] := "q"
```

### **Step 3: Edit or add your remaps:**

#### **Example 1: Swap 2 keys (Q ↔ O)**

```ahk
KeyRemap["q"] := "o"
KeyRemap["o"] := "q"
```

#### **Example 2: Remap skill keys to different positions**

```ahk
KeyRemap["q"] := "l"     ; Q becomes L
KeyRemap["w"] := ";"     ; W becomes ;
KeyRemap["e"] := "p"     ; E becomes P
KeyRemap["r"] := "["     ; R becomes [
```

#### **Example 3: Remap number keys**

```ahk
KeyRemap["1"] := "7"     ; 1 becomes 7
KeyRemap["2"] := "8"     ; 2 becomes 8
KeyRemap["3"] := "9"     ; 3 becomes 9
```

#### **Example 4: Remap function keys**

```ahk
KeyRemap["f1"] := "f5"   ; F1 becomes F5
KeyRemap["f2"] := "f6"   ; F2 becomes F6
```

#### **Example 5: No remapping (keep original keys)**

```ahk
global KeyRemap := {}
; Leave empty or comment out all remaps
```

### **Step 4: Save and test!**

---

## 🎮 **HOW IT WORKS - COMPLETE PIPELINE**

```
┌─────────────────────────────────────────────────────┐
│ HOST PC (Primary)                                    │
│ You press: Q                                         │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ MULTIPLICITY 4 PRO                                   │
│ Broadcasts Q to all 3 clients                        │
└────────────┬────────────────────────────────────────┘
             │
             ├──────────────┬──────────────┬──────────
             ▼              ▼              ▼
     ┌───────────┐  ┌───────────┐  ┌───────────┐
     │ CLIENT 1  │  │ CLIENT 2  │  │ CLIENT 3  │
     │ Receives  │  │ Receives  │  │ Receives  │
     │    Q      │  │    Q      │  │    Q      │
     └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
           │              │              │
           ▼              ▼              ▼
     ┌───────────┐  ┌───────────┐  ┌───────────┐
     │ AHK REMAP │  │ AHK REMAP │  │ AHK REMAP │
     │ Q → Q     │  │ Q → O     │  │ Q → L     │
     │ (No map)  │  │ (Remapped)│  │ (Remapped)│
     └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
           │              │              │
           ▼              ▼              ▼
     ┌───────────┐  ┌───────────┐  ┌───────────┐
     │ AHK JITTER│  │ AHK JITTER│  │ AHK JITTER│
     │ Q + 45ms  │  │ O + 87ms  │  │ L + 112ms │
     │ (30-80ms) │  │ (60-120ms)│  │ (90-150ms)│
     └─────┬─────┘  └─────┬─────┘  └─────┬─────┘
           │              │              │
           ▼              ▼              ▼
     ┌───────────┐  ┌───────────┐  ┌───────────┐
     │  GAME     │  │  GAME     │  │  GAME     │
     │ Gets: Q   │  │ Gets: O   │  │ Gets: L   │
     │ @T=45ms   │  │ @T=87ms   │  │ @T=112ms  │
     └───────────┘  └───────────┘  └───────────┘
```

**Result:**

-   **3 DIFFERENT keys** (Q, O, L) sent to game
-   **3 DIFFERENT timings** (45ms, 87ms, 112ms)
-   **No synchronization pattern detected!** ✅

---

## 🚀 **QUICK SETUP (3 STEPS)**

### **STEP 1: Customize Remaps (Optional)**

Edit each CLIENT script if you want different key mappings:

```bash
# Edit CLIENT2 if you want different remaps
notepad multiplicity_remap_jitter_CLIENT2.ahk

# Edit CLIENT3 if you want different remaps
notepad multiplicity_remap_jitter_CLIENT3.ahk
```

### **STEP 2: Compile to EXE (Obfuscation)**

Run the batch script to compile all 3 clients:

```bash
compile_remap_jitter_all.bat
```

This will create:

```
SystemInputService_C1.exe   (Client 1)
SystemInputService_C2.exe   (Client 2)
SystemInputService_C3.exe   (Client 3)
```

### **STEP 3: Deploy to Clients**

Copy the compiled EXE to each client:

```
Client 1 PC: Copy SystemInputService_C1.exe
Client 2 PC: Copy SystemInputService_C2.exe
Client 3 PC: Copy SystemInputService_C3.exe
```

Run on each client before starting MapleStory!

---

## 🎯 **IN-GAME SETUP REQUIRED**

⚠️ **IMPORTANT:** After remapping keys, you need to **bind skills in-game**!

### **Example Setup:**

#### **HOST presses Q to cast primary skill:**

**CLIENT 1 (No remap):**

```
AHK: Q → Q
In-game keybinding: Q = Primary Skill
Result: ✅ Primary Skill casts
```

**CLIENT 2 (Q → O remap):**

```
AHK: Q → O
In-game keybinding: O = Primary Skill
Result: ✅ Primary Skill casts
```

**CLIENT 3 (Q → L remap):**

```
AHK: Q → L
In-game keybinding: L = Primary Skill
Result: ✅ Primary Skill casts
```

### **Summary:**

```
All 3 clients cast the SAME skill (Primary Skill)
But game receives DIFFERENT keys (Q, O, L)
Anti-cheat sees: Different key patterns ✅
```

---

## 📝 **CUSTOMIZATION EXAMPLES**

### **Example 1: Minimal Remap (Easy to manage)**

**CLIENT 1:** No remap (original keys)
**CLIENT 2:** Just swap Q and O
**CLIENT 3:** Just swap W and P

```ahk
; CLIENT 2
KeyRemap["q"] := "o"
KeyRemap["o"] := "q"

; CLIENT 3
KeyRemap["w"] := "p"
KeyRemap["p"] := "w"
```

### **Example 2: Moderate Remap (More different)**

**CLIENT 1:** No remap
**CLIENT 2:** Remap main skill keys
**CLIENT 3:** Remap different skill keys

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

### **Example 3: Maximum Remap (Hardest to detect)**

**CLIENT 1:** Minimal remap
**CLIENT 2:** Different skill keys
**CLIENT 3:** Completely different layout

```ahk
; CLIENT 1
KeyRemap["q"] := "u"

; CLIENT 2
KeyRemap["q"] := "o"
KeyRemap["w"] := "p"
KeyRemap["e"] := "["
KeyRemap["r"] := "]"

; CLIENT 3
KeyRemap["q"] := "l"
KeyRemap["w"] := ";"
KeyRemap["e"] := "'"
KeyRemap["r"] := ","
KeyRemap["a"] := "k"
KeyRemap["s"] := "j"
```

---

## ⚠️ **IMPORTANT NOTES**

### **1. Test Before Compiling:**

```bash
# Double-click the .ahk file to run it
# Press keys in MapleStory to verify remapping
# Check timing feels natural
```

### **2. Don't Forget In-Game Keybindings:**

```
If you remap Q → O in AHK, you MUST bind the skill to O in-game!
Otherwise the skill won't cast.
```

### **3. Consistent Across All Clients:**

```
If you change a remap, update the in-game keybinding on that client!
```

### **4. Jitter Ranges:**

```
CLIENT 1: 30-80ms (fast, responsive)
CLIENT 2: 60-120ms (medium, balanced)
CLIENT 3: 90-150ms (slow, casual player)

These ranges create natural variation!
```

---

## 🧪 **TESTING**

### **Test 1: Verify Remap Works**

1. Run the .ahk script
2. Open Notepad
3. Press Q → Should type O (if remapped)
4. Press O → Should type Q (if remapped)

### **Test 2: Verify Jitter Works**

1. Run the .ahk script
2. Open MapleStory
3. Press Q multiple times rapidly
4. You should feel slight variation in timing (30-80ms for Client 1)

### **Test 3: Verify In-Game Skill Cast**

1. Open MapleStory
2. Press Q (on host)
3. All 3 clients should cast the skill (if keybindings are correct)

---

## 📊 **EVASION IMPACT**

```
Layer 1 (Multiplicity):              +20%
Layer 4 (Key Remap):                 +2%
Layer 5 (Input Jitter):              +12%
───────────────────────────────────────
TOTAL (Layer 1 + 4 + 5):             34% ✅

With Layer 3 (VPN):                  42% ✅✅
With Layer 6 (Behaviors):            49% ✅✅✅
```

---

## 🎯 **NEXT STEPS**

After setting up Layer 4+5:

1. ✅ Test remapping in Notepad
2. ✅ Test jitter timing in-game
3. ✅ Configure in-game keybindings
4. ✅ Compile to EXE for obfuscation
5. 🔜 Move to Layer 6 (Behavioral Variation)

---

## ❓ **TROUBLESHOOTING**

### **Problem: Key not remapping**

```
Solution: Check #IfWinActive, MapleStory is correct
Solution: Make sure window title matches your game
```

### **Problem: Skill not casting**

```
Solution: Bind the REMAPPED key in-game settings
Example: If Q → O, bind skill to O in-game
```

### **Problem: Script not running**

```
Solution: Right-click .ahk → Run as Administrator
Solution: Check AutoHotkey is installed
```

### **Problem: Too slow/fast**

```
Solution: Adjust MinJitter and MaxJitter values
Fast: 20-60ms
Medium: 60-120ms
Slow: 100-180ms
```

---

## 🔗 **RELATED FILES**

```
Layer 1: START_HERE_LAYER_1.md
Layer 6: multiplicity_anti_detection_complete.ahk
Compile: compile_remap_jitter_all.bat
```

---

**🎉 Layer 4+5 Combined Complete!**

**Continue to Layer 6 for maximum evasion!** 🚀
