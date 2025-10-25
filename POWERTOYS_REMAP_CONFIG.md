# 🎯 POWERTOYS KEYBOARD REMAP - CONFIGURATION GUIDE

## 📋 **OVERVIEW**

**Purpose:** Remap keys on HOST PC so Multiplicity broadcasts DIFFERENT keys to VMs, where AHK scripts convert them back with jitter!

```
HOST:      Q → A (PowerToys remap)
Multipl:   Broadcasts A
VMs:       A (block) → Q (send with jitter)
Game:      Receives Q with different timing! ✅
```

---

## 📥 **STEP 1: INSTALL POWERTOYS**

### **Download:**
```
https://github.com/microsoft/PowerToys/releases

Or:
  Microsoft Store → Search "PowerToys" → Install
```

### **Install:**
```
1. Download PowerToysSetup.exe
2. Run installer
3. Follow wizard
4. Launch PowerToys
```

---

## ⚙️ **STEP 2: OPEN KEYBOARD MANAGER**

```
1. PowerToys icon in system tray (right-click)
2. Click "Settings"
3. Left sidebar → "Keyboard Manager"
4. Enable "Enable Keyboard Manager"
5. Click "Remap a key"
```

---

## 🎹 **STEP 3: CONFIGURE KEY REMAPPING**

### **Core Game Keys (QWERTY layout):**

Click "Add key remapping" for EACH mapping below:

| Original Key | Maps To | Purpose |
|--------------|---------|---------|
| `Q` | `A` | Skill 1 |
| `W` | `S` | Skill 2 / Forward |
| `E` | `D` | Skill 3 |
| `R` | `F` | Skill 4 |
| `T` | `G` | Skill 5 |
| `Y` | `H` | Skill 6 |
| `U` | `J` | Skill 7 |
| `I` | `K` | Skill 8 |
| `O` | `L` | Skill 9 |
| `P` | `;` (Semicolon) | Skill 10 |
| `Z` | `X` | Alt skill 1 |
| `C` | `V` | Alt skill 2 |
| `B` | `N` | Alt skill 3 |
| `M` | `,` (Comma) | Alt skill 4 |

### **Number Keys (1-9):**

| Original Key | Maps To | Purpose |
|--------------|---------|---------|
| `1` | `F1` | Potion 1 |
| `2` | `F2` | Potion 2 |
| `3` | `F3` | Potion 3 |
| `4` | `F4` | Potion 4 |
| `5` | `F5` | Potion 5 |
| `6` | `F6` | Potion 6 |
| `7` | `F7` | Potion 7 |
| `8` | `F8` | Potion 8 |
| `9` | `F9` | Potion 9 |

### **⚠️ IMPORTANT NOTES:**

```
- Chỉ remap keys BẠN DÙNG trong game!
- Arrow keys, Space, Alt, Ctrl, Shift KHÔNG remap (để nguyên)
- Nếu game không dùng key nào, KHÔNG cần remap key đó
```

---

## 🖼️ **VISUAL GUIDE**

### **PowerToys Keyboard Manager Interface:**

```
╔══════════════════════════════════════════════════════════╗
║ Keyboard Manager                                         ║
║                                                          ║
║ ✅ Enable Keyboard Manager                               ║
║                                                          ║
║ [Remap a key]    [Remap a shortcut]                     ║
╚══════════════════════════════════════════════════════════╝

Click "Remap a key" →

╔══════════════════════════════════════════════════════════╗
║ Remap keys                                               ║
║                                                          ║
║ Key:           To send:                          [X]     ║
║ ┌──────┐       ┌──────┐                                  ║
║ │  Q   │   →   │  A   │                                  ║
║ └──────┘       └──────┘                                  ║
║                                                          ║
║ [ + Add key remapping ]                                  ║
║                                                          ║
║ [OK]  [Cancel]                                           ║
╚══════════════════════════════════════════════════════════╝

Repeat for all keys!
```

---

## ✅ **STEP 4: TEST REMAPPING**

### **Quick Test:**

```bash
1. Open Notepad

2. Type on keyboard:
   Q W E R T Y U I O P
   
3. Should see in Notepad:
   A S D F G H J K L ;
   
4. If YES → Remapping working! ✅
   If NO → Check PowerToys settings
```

---

## 🧪 **STEP 5: TEST WITH MULTIPLICITY**

### **Test broadcast:**

```bash
1. HOST: PowerToys remapping enabled ✅

2. ALL VMs: Open Notepad

3. Multiplicity: Enable broadcast mode

4. HOST: Type "QWER"

5. VMs should receive: "ASDF" (remapped keys!)

6. If YES → Ready for AHK jitter scripts! ✅
```

---

## 🚀 **STEP 6: DEPLOY AHK SCRIPTS TO VMS**

### **Copy scripts:**

```
VM1: multiplicity_jitter_REMAP_CLIENT1.ahk  (30-80ms)
VM2: multiplicity_jitter_REMAP_CLIENT2.ahk  (60-120ms)
VM3: multiplicity_jitter_REMAP_CLIENT3.ahk  (90-150ms)
```

### **Run scripts:**

```bash
1. Double-click script on each VM
2. UAC → Click Yes
3. Popup confirms running
4. Script now intercepts remapped keys!
```

---

## 🎯 **FULL PIPELINE TEST**

### **Test in Notepad:**

```bash
SETUP:
  - HOST: PowerToys remap Q→A
  - Multiplicity: Broadcast enabled
  - VM1: multiplicity_jitter_REMAP_CLIENT1.ahk running
  - VM2: multiplicity_jitter_REMAP_CLIENT2.ahk running
  - VM3: multiplicity_jitter_REMAP_CLIENT3.ahk running
  - All VMs: Notepad open

ACTION:
  - HOST: Bấm Q nhiều lần nhanh nhanh

EXPECTED RESULT:
  - VM1: Q xuất hiện với delay ~50ms
  - VM2: Q xuất hiện với delay ~90ms
  - VM3: Q xuất hiện với delay ~120ms
  - Different timing! ✅

If YES → READY FOR GAME! 🎉
```

---

## 📊 **COMPLETE MAPPING TABLE**

### **Recommended Mappings:**

```
┌─────────────────────────────────────────────────────┐
│ HOST KEY → MULTIPLICITY → VM RECEIVES → GAME GETS  │
├─────────────────────────────────────────────────────┤
│    Q     →     A        →      A       →    Q      │
│    W     →     S        →      S       →    W      │
│    E     →     D        →      D       →    E      │
│    R     →     F        →      F       →    R      │
│    T     →     G        →      G       →    T      │
│    Y     →     H        →      H       →    Y      │
│    U     →     J        →      J       →    U      │
│    I     →     K        →      K       →    I      │
│    O     →     L        →      L       →    O      │
│    P     →     ;        →      ;       →    P      │
│    Z     →     X        →      X       →    Z      │
│    C     →     V        →      V       →    C      │
│    B     →     N        →      N       →    B      │
│    M     →     ,        →      ,       →    M      │
│    1     →    F1        →     F1       →    1      │
│    2     →    F2        →     F2       →    2      │
│    3     →    F3        →     F3       →    3      │
│    4     →    F4        →     F4       →    4      │
│    5     →    F5        →     F5       →    5      │
│    6     →    F6        →     F6       →    6      │
│    7     →    F7        →     F7       →    7      │
│    8     →    F8        →     F8       →    8      │
│    9     →    F9        →     F9       →    9      │
└─────────────────────────────────────────────────────┘

Jitter applied between "VM RECEIVES" → "GAME GETS"!
```

---

## 🛠️ **TROUBLESHOOTING**

### **Issue 1: Remapping không work**

```
Problem: Bấm Q vẫn thấy Q thay vì A
Fix:
  1. Check PowerToys icon in system tray
  2. Right-click → Settings
  3. Keyboard Manager → Verify "Enable" is ON
  4. Check remap list, verify Q→A exists
  5. Try restart PowerToys
```

---

### **Issue 2: Multiplicity broadcast wrong keys**

```
Problem: VMs nhận Q thay vì A
Fix:
  1. Verify PowerToys working (test in Notepad on HOST)
  2. If Notepad shows Q → PowerToys not remapping
  3. Check if PowerToys has admin rights
  4. Restart PowerToys service
```

---

### **Issue 3: AHK script không convert lại**

```
Problem: Game nhận A thay vì Q
Fix:
  1. Verify AHK script running (icon "H" in tray)
  2. Check script is CLIENT1/2/3 REMAP version
  3. Test in Notepad: Bấm A → Q xuất hiện?
  4. If not, script có lỗi hoặc not admin
```

---

## 🎮 **READY FOR GAME!**

### **Final Checklist:**

```
HOST PC:
  ✅ PowerToys installed
  ✅ Keyboard Manager enabled
  ✅ All keys remapped (Q→A, W→S, etc.)
  ✅ Test in Notepad: Q shows as A
  
MULTIPLICITY:
  ✅ Connected to all VMs
  ✅ Broadcast mode works
  ✅ Test: Q broadcast shows A in VM Notepad
  
VM1 (Fast - 30-80ms):
  ✅ multiplicity_jitter_REMAP_CLIENT1.ahk running
  ✅ Script has admin rights
  ✅ Test: A → Q with delay
  
VM2 (Medium - 60-120ms):
  ✅ multiplicity_jitter_REMAP_CLIENT2.ahk running
  ✅ Script has admin rights
  ✅ Test: A → Q with delay
  
VM3 (Slow - 90-150ms):
  ✅ multiplicity_jitter_REMAP_CLIENT3.ahk running
  ✅ Script has admin rights
  ✅ Test: A → Q with delay

If ALL ✅ → LAUNCH MAPLESTORY! 🚀
```

---

## 💡 **TIPS**

### **Performance:**

```
- PowerToys remap has ZERO delay (kernel-level)
- Multiplicity broadcast: ~5-10ms
- AHK jitter: 30-150ms (intentional!)
- Total delay: Acceptable for MMO gameplay ✅
```

### **Customization:**

```
Nếu muốn remap keys khác:
  1. Edit PowerToys remap
  2. Edit AHK scripts (add new hotkeys)
  3. Test in Notepad first!
  4. Then test in game
```

---

## 🎊 **SUCCESS!**

**You now have:**
- ✅ PowerToys remapping on HOST
- ✅ Multiplicity broadcasting remapped keys
- ✅ AHK converting back with JITTER
- ✅ Different timing per VM
- ✅ Anti-detection working!

**🎉 READY TO FARM! 🚀**

