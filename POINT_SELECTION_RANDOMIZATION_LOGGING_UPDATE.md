# 🎯 Point Selection Randomization - Logging Update

## ✅ **Enhanced Logging Added**

Đã thêm logging chi tiết để quan sát Point Selection Randomization dễ dàng hơn.

---

## 📝 **New Logging Features**

### **1. Initialization Logging**

Khi routine được load, sẽ log:
```
📊 Routine Loaded: X Points, Y Jumps, Z Labels, N Total Components
🎯 Point Selection Randomization: Ready (35.0% skip probability, max 2 consecutive skips)
```

---

### **2. Skip Decision Logging**

**For Points:**
```
✅ Point Selection Randomization: Index X - Point (0.xxx, 0.yyy) - EXECUTE (probability: 35.0%, random: 0.xxx)
⏭️ Point Selection Randomization: Index X - Point (0.xxx, 0.yyy) - SKIP (probability: 35.0%, random: 0.xxx, consecutive: 1/2)
```

**For Non-Points (Jump, Label, Setting):**
```
🔄 Point Selection Randomization: Index X - Jump (NOT a Point - will execute)
🔄 Point Selection Randomization: Index X - Label (NOT a Point - will execute)
```

**For Max Consecutive Skips:**
```
✅ Point Selection Randomization: Index X - Point (0.xxx, 0.yyy) - EXECUTE (max consecutive skips reached: 2/2)
```

---

### **3. Execution Logging**

**When Executing:**
```
▶️ Point Selection Randomization: EXECUTING point at index X (location: 0.xxx, 0.yyy)
```

**When Skipping:**
```
🚫 Point Selection Randomization: SKIPPING execution of point at index X
```

---

### **4. Debug Logging**

**Routine Execution State:**
```
📍 Routine Execution: Index X/Y - Point
📍 Routine Execution: Index X/Y - Jump
```

---

## 🎯 **Log Examples**

### **Example 1: Normal Execution (No Skip)**

```
🎯 Point Selection Randomization: Ready (35.0% skip probability, max 2 consecutive skips)
✅ Point Selection Randomization: Index 0 - Point (0.229, 0.190) - EXECUTE (probability: 35.0%, random: 0.456)
▶️ Point Selection Randomization: EXECUTING point at index 0 (location: 0.229, 0.190)
✅ Point Selection Randomization: Index 1 - Point (0.268, 0.190) - EXECUTE (probability: 35.0%, random: 0.789)
▶️ Point Selection Randomization: EXECUTING point at index 1 (location: 0.268, 0.190)
```

---

### **Example 2: Skipping Points**

```
🎯 Point Selection Randomization: Ready (35.0% skip probability, max 2 consecutive skips)
✅ Point Selection Randomization: Index 0 - Point (0.229, 0.190) - EXECUTE (probability: 35.0%, random: 0.456)
▶️ Point Selection Randomization: EXECUTING point at index 0 (location: 0.229, 0.190)
⏭️ Point Selection Randomization: Index 1 - Point (0.268, 0.190) - SKIP (probability: 35.0%, random: 0.234, consecutive: 1/2)
🚫 Point Selection Randomization: SKIPPING execution of point at index 1
⏭️ Point Selection Randomization: Index 2 - Point (0.327, 0.190) - SKIP (probability: 35.0%, random: 0.123, consecutive: 2/2)
🚫 Point Selection Randomization: SKIPPING execution of point at index 2
✅ Point Selection Randomization: Index 3 - Point (0.385, 0.190) - EXECUTE (max consecutive skips reached: 2/2)
▶️ Point Selection Randomization: EXECUTING point at index 3 (location: 0.385, 0.190)
```

---

### **Example 3: Non-Point Components (Jump, Label)**

```
🔄 Point Selection Randomization: Index 171 - Jump (NOT a Point - will execute)
🔄 Point Selection Randomization: Index 5 - Label (NOT a Point - will execute)
```

---

## 🎯 **How to Observe**

### **1. Check Log File**

Mở file `logs/auto_maple.log` và tìm các dòng:
- `🎯 Point Selection Randomization: Ready` - Initialization
- `✅ Point Selection Randomization: Index X` - Execute decision
- `⏭️ Point Selection Randomization: Index X` - Skip decision
- `▶️ Point Selection Randomization: EXECUTING` - Execution
- `🚫 Point Selection Randomization: SKIPPING` - Skipping

---

### **2. Filter Logs**

Sử dụng grep để filter logs:
```bash
grep "Point Selection Randomization" logs/auto_maple.log
```

---

### **3. Observe Pattern**

**Without Skip:**
- Tất cả points đều có `✅ EXECUTE`
- Không có `⏭️ SKIP`

**With Skip:**
- Một số points có `✅ EXECUTE`
- Một số points có `⏭️ SKIP`
- Pattern varies mỗi loop

---

## 🎯 **What to Look For**

### **1. Skip Probability Working:**

```
⏭️ Point Selection Randomization: Index X - Point (0.xxx, 0.yyy) - SKIP (probability: 35.0%, random: 0.234, consecutive: 1/2)
```

**Check:**
- Random value < 0.35 (skip probability) → Should skip
- Random value >= 0.35 → Should execute

---

### **2. Max Consecutive Skips Working:**

```
⏭️ Point Selection Randomization: Index 1 - SKIP (consecutive: 1/2)
⏭️ Point Selection Randomization: Index 2 - SKIP (consecutive: 2/2)
✅ Point Selection Randomization: Index 3 - EXECUTE (max consecutive skips reached: 2/2)
```

**Check:**
- After 2 consecutive skips, next point should execute (even if random < 0.35)

---

### **3. Never Skip Non-Points:**

```
🔄 Point Selection Randomization: Index X - Jump (NOT a Point - will execute)
🔄 Point Selection Randomization: Index X - Label (NOT a Point - will execute)
```

**Check:**
- Jump, Label, Setting are never skipped
- They always execute

---

## 🎯 **Troubleshooting**

### **Problem: No Skip Logs**

**Solution:**
- Check `skip_enabled = True` in `Routine.__init__()`
- Check `skip_probability` value (should be > 0)
- Check logs for initialization message

---

### **Problem: All Points Execute (No Skips)**

**Solution:**
- Check random values in logs
- If all random values >= skip_probability, that's normal (random)
- Increase skip_probability for testing (e.g., 0.50 for 50%)

---

### **Problem: Too Many Skips**

**Solution:**
- Check skip_probability value
- Reduce skip_probability (e.g., from 0.35 to 0.10)
- Check max_consecutive_skips (should limit consecutive skips)

---

## 🎯 **Files Modified**

1. **`src/routine/routine.py`**
   - Enhanced `should_skip_current_point()` with detailed logging
   - Added logging in `load()` method
   - Log skip decisions, probabilities, and consecutive skips

2. **`src/modules/bot.py`**
   - Added execution logging (EXECUTING vs SKIPPING)
   - Added debug logging for routine state

---

## 🎯 **Status**

✅ **Enhanced Logging Complete**
✅ **Ready for Observation**
✅ **No Linter Errors (only warnings)**

---

**Last Updated:** 2024
**Status:** ✅ Enhanced Logging Ready

