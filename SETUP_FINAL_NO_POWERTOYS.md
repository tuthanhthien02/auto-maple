# 🎯 MULTIPLICITY JITTER - FINAL SETUP (NO POWERTOYS!)

## ✅ **ARCHITECTURE ĐƠN GIẢN NHẤT!**

```
HOST PC: Press Q, W, E, R...
    ↓
MULTIPLICITY 4: Broadcast to all VMs
    ↓         ↓         ↓
┌───────────────────────────────────┐
│  VM1       VM2       VM3          │
│  AHK       AHK       AHK          │
│  Q→P       Q→O       Q→I          │
│  30ms      60ms      90ms         │
│  ↓         ↓         ↓            │
│  GAME      GAME      GAME         │
│  gets P    gets O    gets I       │
└───────────────────────────────────┘
```

**Không cần PowerToys!** ✅  
**Chỉ cần AHK + In-game keybindings!** ✅

---

## 📦 **FILES SỬ DỤNG**

```
VM1: multiplicity_jitter_VM1.ahk  (Fast: 30-80ms)
VM2: multiplicity_jitter_VM2.ahk  (Medium: 60-120ms)
VM3: multiplicity_jitter_VM3.ahk  (Slow: 90-150ms)
```

---

## 🎮 **IN-GAME KEY MAPPINGS**

### **⚠️ CRITICAL: Mỗi VM PHẢI config keybindings KHÁC NHAU trong game!**

### **VM1 Keybindings:**

| Host Key     | AHK Converts To | Bind In-Game             |
| ------------ | --------------- | ------------------------ |
| Q            | P               | Skill 1 → **P**          |
| W            | [               | Skill 2 → **[**          |
| E            | ]               | Skill 3 → **]**          |
| R            | \               | Skill 4 → \*\*\*\*       |
| T            | -               | Skill 5 → **-**          |
| Y            | =               | Skill 6 → **=**          |
| U            | F10             | Skill 7 → **F10**        |
| I            | F11             | Skill 8 → **F11**        |
| O            | F12             | Skill 9 → **F12**        |
| P            | Home            | Skill 10 → **Home**      |
| Z            | End             | Alt Skill 1 → **End**    |
| X            | PgUp            | Alt Skill 2 → **PgUp**   |
| C            | PgDn            | Alt Skill 3 → **PgDn**   |
| V            | Insert          | Alt Skill 4 → **Insert** |
| B            | Delete          | Alt Skill 5 → **Delete** |
| **Numbers:** |
| 1            | Numpad1         | Potion 1 → **Numpad1**   |
| 2            | Numpad2         | Potion 2 → **Numpad2**   |
| 3            | Numpad3         | Potion 3 → **Numpad3**   |
| 4            | Numpad4         | Potion 4 → **Numpad4**   |
| 5            | Numpad5         | Potion 5 → **Numpad5**   |
| 6            | Numpad6         | Potion 6 → **Numpad6**   |
| 7            | Numpad7         | Potion 7 → **Numpad7**   |
| 8            | Numpad8         | Potion 8 → **Numpad8**   |
| 9            | Numpad9         | Potion 9 → **Numpad9**   |
| 0            | Numpad0         | Mount → **Numpad0**      |

---

### **VM2 Keybindings:**

| Host Key     | AHK Converts To | Bind In-Game                  |
| ------------ | --------------- | ----------------------------- |
| Q            | O               | Skill 1 → **O**               |
| W            | K               | Skill 2 → **K**               |
| E            | L               | Skill 3 → **L**               |
| R            | ;               | Skill 4 → **;**               |
| T            | '               | Skill 5 → **'**               |
| Y            | `               | Skill 6 → **`**               |
| U            | ,               | Skill 7 → **,**               |
| I            | .               | Skill 8 → **.**               |
| O            | /               | Skill 9 → **/**               |
| P            | Numpad+         | Skill 10 → **Numpad+**        |
| Z            | Numpad-         | Alt Skill 1 → **Numpad-**     |
| X            | Numpad\*        | Alt Skill 2 → **Numpad\***    |
| C            | Numpad/         | Alt Skill 3 → **Numpad/**     |
| V            | NumpadDot       | Alt Skill 4 → **Numpad.**     |
| B            | NumpadEnter     | Alt Skill 5 → **NumpadEnter** |
| **Numbers:** |
| 1            | F1              | Potion 1 → **F1**             |
| 2            | F2              | Potion 2 → **F2**             |
| 3            | F3              | Potion 3 → **F3**             |
| 4            | F4              | Potion 4 → **F4**             |
| 5            | F5              | Potion 5 → **F5**             |
| 6            | F6              | Potion 6 → **F6**             |
| 7            | F7              | Potion 7 → **F7**             |
| 8            | F8              | Potion 8 → **F8**             |
| 9            | F9              | Potion 9 → **F9**             |
| 0            | F10             | Mount → **F10**               |

---

### **VM3 Keybindings:**

| Host Key     | AHK Converts To | Bind In-Game                  |
| ------------ | --------------- | ----------------------------- |
| Q            | I               | Skill 1 → **I**               |
| W            | U               | Skill 2 → **U**               |
| E            | Y               | Skill 3 → **Y**               |
| R            | T               | Skill 4 → **T**               |
| T            | G               | Skill 5 → **G**               |
| Y            | H               | Skill 6 → **H**               |
| U            | J               | Skill 7 → **J**               |
| I            | K               | Skill 8 → **K**               |
| O            | M               | Skill 9 → **M**               |
| P            | N               | Skill 10 → **N**              |
| Z            | B               | Alt Skill 1 → **B**           |
| X            | V               | Alt Skill 2 → **V**           |
| C            | Left            | Alt Skill 3 → **Left Arrow**  |
| V            | Right           | Alt Skill 4 → **Right Arrow** |
| B            | Up              | Alt Skill 5 → **Up Arrow**    |
| **Numbers:** |
| 1            | 6               | Potion 1 → **6**              |
| 2            | 7               | Potion 2 → **7**              |
| 3            | 8               | Potion 3 → **8**              |
| 4            | 9               | Potion 4 → **9**              |
| 5            | 0               | Potion 5 → **0**              |
| 6            | 1               | Potion 6 → **1**              |
| 7            | 2               | Potion 7 → **2**              |
| 8            | 3               | Potion 8 → **3**              |
| 9            | 4               | Potion 9 → **4**              |
| 0            | 5               | Mount → **5**                 |

---

## 🚀 **SETUP STEPS**

### **STEP 1: Deploy AHK Scripts** ⏱️ 5 phút

```bash
VM1:
  1. Copy multiplicity_jitter_VM1.ahk
  2. Double-click → UAC → Yes
  3. Popup shows mappings → OK
  4. Icon "H" in system tray ✅

VM2:
  1. Copy multiplicity_jitter_VM2.ahk
  2. Double-click → UAC → Yes
  3. Popup shows mappings → OK
  4. Icon "H" in system tray ✅

VM3:
  1. Copy multiplicity_jitter_VM3.ahk
  2. Double-click → UAC → Yes
  3. Popup shows mappings → OK
  4. Icon "H" in system tray ✅
```

---

### **STEP 2: Configure In-Game Keybindings** ⏱️ 15 phút PER VM

```bash
In MapleStory (mỗi VM):

1. Press ESC → Settings → Key Settings

2. Configure theo table ở trên:

VM1:
  Skill 1: Change to P
  Skill 2: Change to [
  Skill 3: Change to ]
  Skill 4: Change to \
  Potion 1: Change to Numpad1
  Potion 2: Change to Numpad2
  ... (theo table)

VM2:
  Skill 1: Change to O
  Skill 2: Change to K
  Skill 3: Change to L
  Skill 4: Change to ;
  Potion 1: Change to F1
  Potion 2: Change to F2
  ... (theo table)

VM3:
  Skill 1: Change to I
  Skill 2: Change to U
  Skill 3: Change to Y
  Skill 4: Change to T
  Potion 1: Change to 6
  Potion 2: Change to 7
  ... (theo table)

3. Save settings

4. Test: Verify skills respond correctly
```

---

### **STEP 3: Test Pipeline** ⏱️ 5 phút

```bash
TEST IN NOTEPAD FIRST:

1. All VMs: Open Notepad

2. Multiplicity: Enable broadcast

3. HOST: Type "QWER" quickly

4. EXPECTED:
   VM1 Notepad: P [ ] \
   VM2 Notepad: O K L ;
   VM3 Notepad: I U Y T

   → Different keys! ✅

5. Observe delays (jitter):
   VM1: Fastest (30-80ms)
   VM2: Medium (60-120ms)
   VM3: Slowest (90-150ms)

   → Different timing! ✅

6. If YES → Test in game!
```

---

### **STEP 4: Test In-Game** ⏱️ 10 phút

```bash
1. All VMs: In MapleStory

2. HOST: Press Q (Skill 1)

3. EXPECTED:
   VM1: Skill 1 activates (got P)
   VM2: Skill 1 activates (got O)
   VM3: Skill 1 activates (got I)

   → All skills work! ✅
   → Different timing! ✅

4. Test all keys:
   HOST: Q W E R 1 2 3

   All VMs: Skills and potions work? ✅

5. If YES → READY TO FARM! 🎉
```

---

## 📊 **HOW IT WORKS**

```
Example: Host presses Q

HOST:
  User presses Q
  ↓
MULTIPLICITY:
  Broadcasts Q to all VMs at T=0ms
  ↓         ↓         ↓
VM1:       VM2:       VM3:
Q arrives  Q arrives  Q arrives
  ↓          ↓          ↓
AHK:       AHK:       AHK:
Block Q    Block Q    Block Q
Wait 47ms  Wait 83ms  Wait 118ms (random Gaussian)
Send P     Send O     Send I
  ↓          ↓          ↓
GAME:      GAME:      GAME:
T=47ms     T=83ms     T=118ms
Receives P Receives O Receives I
Skill 1!   Skill 1!   Skill 1!

RESULT:
  ✅ All characters use Skill 1
  ✅ But at DIFFERENT times!
  ✅ VM1: 47ms, VM2: 83ms, VM3: 118ms
  ✅ NOT synchronized!
  ✅ Anti-detection working! 🎉
```

---

## 🎯 **ADVANTAGES**

```
✅ NO PowerToys needed! (simpler!)
✅ Only AHK scripts (easy to manage)
✅ Each VM has DIFFERENT in-game keybindings
   → Extra anti-detection layer! ✅✅
✅ Jitter still working (30-80ms, 60-120ms, 90-150ms)
✅ Different "player personality" per VM
✅ Harder to detect than synchronized input!
```

---

## ⚠️ **IMPORTANT NOTES**

### **Arrow Keys, Space, Ctrl, Alt, Shift:**

```
⚠️ KHÔNG remap các keys này!
→ Để nguyên để di chuyển, jump, etc.

AHK scripts KHÔNG block:
  - Arrow keys (Up, Down, Left, Right)
  - Space (Jump)
  - Alt (Skill modifier)
  - Ctrl (Skill modifier)
  - Shift (Skill modifier)
  - Enter, Tab, ESC

→ These keys work normally! ✅
```

---

## 🎮 **IN-GAME SETUP TIPS**

### **MapleStory Key Settings:**

```
1. Open game settings

2. Key Configuration tab

3. Click on skill slot

4. Press NEW key (e.g., P for VM1, O for VM2)

5. Repeat for all skills/potions

6. Save and test!

⚠️ Make sure EACH VM has DIFFERENT bindings!
```

---

## 📈 **EXPECTED RESULTS**

### **With This Setup:**

```
✅ Different keys per VM (P, O, I...)
✅ Different timing per VM (47ms, 83ms, 118ms)
✅ Different jitter ranges (30-80, 60-120, 90-150ms)
✅ Gaussian distribution (more human-like)

Anti-cheat sees:
  "3 different players"
  "Different keybindings"
  "Different reaction times"
  "Different playstyles"

  → Much harder to detect! ✅
```

---

## 🔧 **CUSTOMIZATION**

### **Change Jitter Ranges:**

Edit AHK scripts:

```ahk
VM1: Lines 30-31:
  global MinJitter := 30  ← Change this
  global MaxJitter := 80  ← Change this

VM2: Lines 30-31:
  global MinJitter := 60
  global MaxJitter := 120

VM3: Lines 30-31:
  global MinJitter := 90
  global MaxJitter := 150
```

### **Change Key Mappings:**

Edit AHK scripts:

```ahk
VM1 example:
  q::
    ApplyJitterAndSend("p")  ← Change "p" to another key

Then update in-game keybindings to match!
```

---

## 🐛 **TROUBLESHOOTING**

### **Issue: Skills don't activate**

```
Problem: Host press Q, nothing happens in game
Fix:
  1. Check AHK script running (icon "H" in tray)
  2. Test in Notepad: Q → P/O/I?
  3. Check in-game keybindings match AHK output
  4. VM1 game: Skill 1 bound to P?
  5. VM2 game: Skill 1 bound to O?
  6. VM3 game: Skill 1 bound to I?
```

---

### **Issue: All VMs use same skill**

```
Problem: All VMs have same in-game keybindings
Fix:
  ⚠️ MUST configure DIFFERENT keybindings per VM!

  VM1: Skill 1 = P
  VM2: Skill 1 = O  (NOT P!)
  VM3: Skill 1 = I  (NOT P or O!)
```

---

### **Issue: No jitter/delay visible**

```
Problem: All VMs respond instantly
Fix:
  1. Test in Notepad (easier to see delay)
  2. Increase jitter ranges for testing
  3. VM1: 100-200ms (temporary)
  4. Verify delay now visible
  5. Reduce back to 30-80ms for gameplay
```

---

## 🎊 **READY TO USE!**

```
╔════════════════════════════════════════════════════╗
║                                                    ║
║   🎉 SIMPLEST SOLUTION - NO POWERTOYS! 🎉         ║
║                                                    ║
║   ✅ AHK scripts with remap + jitter              ║
║   ✅ Different keys per VM                        ║
║   ✅ Different timing per VM                      ║
║   ✅ In-game keybindings DIFFERENT per VM         ║
║   ✅ Extra anti-detection layer!                  ║
║                                                    ║
║   Easier to setup than PowerToys approach! 🚀     ║
║                                                    ║
╚════════════════════════════════════════════════════╝
```

---

**🚀 START: Deploy multiplicity_jitter_VM1/2/3.ahk!**

**Then configure in-game keybindings per VM!** ✨

**Total setup time: ~45 minutes (15 min per VM for keybindings)** ⚡
