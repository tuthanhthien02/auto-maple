# 🐛 BUG FIX: CHAIN REMAP ISSUE

## ❌ **VẤN ĐỀ PHÁT HIỆN:**

Khi ấn **Q**, xuất hiện **cả P và Home**!

```
Test trên keytest.vn:
  Press Q → Shows P, then Home ❌
```

---

## 🔍 **NGUYÊN NHÂN: CHAIN REMAP**

```
Q pressed by user
  ↓
AHK: q:: → SendInput, P
  ↓
AHK: p:: → SendInput, Home  ← CHAIN REACTION! ❌
  ↓
RESULT: Q → P → Home (both keys triggered!)
```

**AHK triggers hotkeys from its own `SendInput`!**

Khi script send `P`, AHK lại intercept `P` và chạy hotkey `p::`!

---

## ✅ **SOLUTION: `$` PREFIX**

`$` prefix tells AHK: **"Don't trigger this hotkey from SendInput within this script!"**

### **Before (BUG):**

```ahk
q::
    ApplyJitterAndSend("p")
    return

p::
    ApplyJitterAndSend("Home")
    return
```

**Result:** Q → P → Home (chain!)

---

### **After (FIXED):**

```ahk
$q::
    ApplyJitterAndSend("p")
    return

$p::
    ApplyJitterAndSend("Home")
    return
```

**Result:** Q → P only! ✅

---

## 🔧 **WHAT `$` DOES:**

```
Without $:
  q:: → SendInput P → p:: triggered ❌

With $:
  $q:: → SendInput P → $p:: NOT triggered ✅
```

The `$` prefix prevents the hotkey from being triggered by the keyboard hook used by `Send` commands.

---

## 📦 **FILES FIXED:**

```
✅ multiplicity_jitter_VM1.ahk
   - All hotkeys now use $q::, $w::, $1::, etc.

✅ multiplicity_jitter_VM2.ahk
   - All hotkeys now use $q::, $w::, $1::, etc.

✅ multiplicity_jitter_VM3.ahk
   - All hotkeys now use $q::, $w::, $1::, etc.
```

---

## 🧪 **TEST NOW:**

```bash
1. Close old AHK script (right-click H icon → Exit)

2. Double-click fixed script

3. Test on keytest.vn:
   Press Q → Should show ONLY P ✅
   Press P → Should show ONLY Home ✅
   Press 1 → Should show ONLY Numpad1 ✅

4. No more chain reactions! 🎉
```

---

## 📚 **AHK DOCUMENTATION:**

From AHK docs:

> **$ (dollar sign) prefix:**
>
> This is usually only necessary if the script uses the Send command to send the keys that comprise the hotkey itself, which might otherwise cause the hotkey to trigger itself.
>
> The $ prefix forces the keyboard hook to be used to implement this hotkey, which as a side-effect prevents the Send command from triggering it.

---

## 🎯 **KEY TAKEAWAY:**

```
⚠️ When remapping keys that chain (Q→P, P→Home):
   ALWAYS use $ prefix!

✅ $q:: instead of q::
✅ $p:: instead of p::
✅ $1:: instead of 1::

This prevents SendInput from triggering your own hotkeys!
```

---

## ✅ **STATUS:**

```
✅ Bug identified
✅ Root cause found (chain remap)
✅ Solution applied ($ prefix)
✅ All 3 scripts fixed
✅ Ready to test!
```

---

**🚀 Test the fixed scripts now!**

**Q should only produce P, not P+Home!** ✨
