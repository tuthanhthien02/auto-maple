# 💡 ADD ARROW KEYS TO JITTER SCRIPT

## 🎯 **OPTION:**

Thêm arrow keys vào script để có jitter!

---

## ✅ **SOLUTION: ADD TO REMAP TABLE!**

### **Edit: multiplicity_jitter_WITH_PAUSE.ahk**

```ahk
Lines 38-70:

; ═══════════════════════════════════════════════════════════
; 🎨 REMAP TABLE
; ═══════════════════════════════════════════════════════════

global remap := {}

; MAIN KEYS (Q W E R → A S D F)
remap["q"] := "a"
remap["w"] := "s"
remap["e"] := "d"
remap["r"] := "f"

; ... other keys ...

; ─────────────────────────────────────
; ARROW KEYS (PASSTHROUGH WITH JITTER!)
; ─────────────────────────────────────
remap["Up"] := "Up"       ; ← Same key, but gets JITTER!
remap["Down"] := "Down"   ; ← Same key, but gets JITTER!
remap["Left"] := "Left"   ; ← Same key, but gets JITTER!
remap["Right"] := "Right" ; ← Same key, but gets JITTER!
remap["Space"] := "Space" ; ← Jump also gets JITTER!
```

**What this does:**

```
Arrow keys:
  → Still send same key (Up→Up, Down→Down)
  → BUT goes through ApplyJitterAndSend()
  → Gets JITTER delay! ✅

Result:
  Host presses UP at T=0
  → VM1: UP at T=47ms   (30-80ms jitter)
  → VM2: UP at T=83ms   (60-120ms jitter)
  → VM3: UP at T=118ms  (90-150ms jitter)

  ALREADY DONE by default! ✅
```

---

## ⚠️ **WAIT! THIS IS ALREADY WORKING!**

Script behavior:

```ahk
HandleKey:
    pressedKey := SubStr(A_ThisHotkey, 2)
    outputKey := remap[pressedKey]

    if (outputKey != "") {
        ApplyJitterAndSend(outputKey)  ← Has jitter!
    }
    return
```

**If arrow keys NOT in remap table:**

-   Script doesn't intercept them
-   They pass through WITHOUT jitter ❌

**If arrow keys IN remap table (remap to SAME key):**

-   Script intercepts them
-   Applies jitter ✅
-   Sends same key ✅

---

## 🎯 **RECOMMENDATION:**

### **ALREADY GOOD AS-IS!**

Current script WITHOUT arrow keys in remap:

```
Arrow keys:
  → NOT intercepted
  → Pass through directly
  → NO jitter ❌
  → All VMs receive at SAME TIME ⚠️
```

### **BETTER: ADD ARROW KEYS TO REMAP!**

Add to remap table:

```ahk
remap["Up"] := "Up"
remap["Down"] := "Down"
remap["Left"] := "Left"
remap["Right"] := "Right"
remap["Space"] := "Space"
```

Result:

```
Arrow keys:
  → Intercepted by script
  → Apply jitter ✅
  → Send same key ✅
  → VMs receive at DIFFERENT TIMES! ✅
```

---

## 📊 **COMPARISON:**

| Setup               | Arrow Keys Jitter? | Detection Risk | Verdict    |
| ------------------- | ------------------ | -------------- | ---------- |
| **Current**         | ❌ NO              | MEDIUM ⚠️      | Acceptable |
| **+Arrow in remap** | ✅ YES             | LOW ✅         | Better!    |

---

## ✅ **CONCLUSION:**

```
Arrow keys SHOULD be added to remap table!

Why?
  ✅ Still sends same key (no game impact)
  ✅ But adds jitter (different timing per VM)
  ✅ Reduces detection risk
  ✅ Zero extra work (just add 5 lines!)

Add to script:
  remap["Up"] := "Up"
  remap["Down"] := "Down"
  remap["Left"] := "Left"
  remap["Right"] := "Right"
  remap["Space"] := "Space"
```
