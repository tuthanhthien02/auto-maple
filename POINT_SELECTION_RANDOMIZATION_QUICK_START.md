# 🎯 Point Selection Randomization - Quick Start

## ✅ **Implementation Complete**

Point Selection Randomization đã được implement với skip probability **35%** (30-40% range for testing).

---

## 🎯 **Features**

1. **Skip Points:** 35% chance to skip points
2. **Max Consecutive Skips:** 2 (prevents skipping too many points in a row)
3. **Never Skip Critical Components:** Jump, Label, Setting are never skipped
4. **Logging:** Skipped points are logged (INFO level)

---

## 🚀 **How to Use**

### **1. Enable/Disable Skip:**

**Default:** Enabled (`skip_enabled = True`)

**To disable:**
```python
# In src/routine/routine.py - Routine.__init__()
self.skip_enabled = False  # Disable skip feature
```

---

### **2. Adjust Skip Probability:**

**Current:** 35% (for testing)

**To change:**
```python
# In src/routine/routine.py - Routine.__init__()
self.skip_probability = 0.35  # 35% chance to skip (0.0 - 1.0)
```

**Recommended values:**
- **Testing:** 30-40% (current)
- **Production:** 5-15% (after testing)

---

### **3. Adjust Max Consecutive Skips:**

**Current:** 2

**To change:**
```python
# In src/routine/routine.py - Routine.__init__()
self.max_consecutive_skips = 2  # Max 2 consecutive skips
```

**Recommended values:**
- **Testing:** 2 (current)
- **Production:** 1-2 (after testing)

---

## 📊 **Expected Behavior**

### **Without Skip:**
```
Loop: f1_pos_0 → f1_pos_1 → f1_pos_2 → ... → f1_pos_8 → Floor 2 → Loop
Pattern: Always sequential, predictable
```

### **With Skip (35% probability):**
```
Loop 1: f1_pos_0 → f1_pos_2 → f1_pos_4 → f1_pos_6 → f1_pos_8 (skip 1, 3, 5, 7)
Loop 2: f1_pos_0 → f1_pos_1 → f1_pos_3 → f1_pos_5 → f1_pos_7 → f1_pos_8 (skip 2, 4, 6)
Loop 3: f1_pos_0 → f1_pos_1 → f1_pos_2 → f1_pos_4 → f1_pos_7 → f1_pos_8 (skip 3, 5, 6)
Pattern: Varies each loop, unpredictable
```

---

## 📝 **Logging**

### **INFO Level (Skipped Points):**
```
⏭️ Point Selection Randomization: Skipping point at index 5 (location: 0.527, 0.190)
⏭️ Point Selection Randomization: Skipping point at index 7 (location: 0.649, 0.190)
```

### **DEBUG Level (Skip Decisions):**
```
Point Selection Randomization: Skipping point at index 3 (consecutive skips: 1)
Point Selection Randomization: Skipping point at index 4 (consecutive skips: 2)
```

---

## 🎯 **Testing**

### **Test Checklist:**

1. **Skip Points:**
   - [ ] Points are skipped randomly (35% chance)
   - [ ] Max 2 consecutive skips
   - [ ] Skip pattern varies each loop

2. **Never Skip Critical Components:**
   - [ ] Jump commands are never skipped
   - [ ] Label components are never skipped
   - [ ] Setting components are never skipped

3. **Logging:**
   - [ ] Skipped points are logged (INFO level)
   - [ ] Skip decisions are logged (DEBUG level)

4. **Routine Execution:**
   - [ ] Routine still loops correctly
   - [ ] Jump commands still work
   - [ ] Labels still work

---

## 🎯 **After Testing**

### **Adjust Skip Probability:**

**If skip too much:**
```python
self.skip_probability = 0.10  # Reduce to 10%
```

**If skip too little:**
```python
self.skip_probability = 0.20  # Increase to 20%
```

**Recommended for production:**
```python
self.skip_probability = 0.10  # 10% (good balance)
```

---

### **Adjust Max Consecutive Skips:**

**If skip too many consecutive:**
```python
self.max_consecutive_skips = 1  # Reduce to 1
```

**If skip too few consecutive:**
```python
self.max_consecutive_skips = 2  # Keep at 2 (current)
```

---

## 🎯 **Troubleshooting**

### **Problem: Points are not being skipped**

**Solution:**
- Check `skip_enabled = True` in `Routine.__init__()`
- Check `skip_probability` value (should be > 0)
- Check logs for skip decisions (DEBUG level)

---

### **Problem: Too many points are being skipped**

**Solution:**
- Reduce `skip_probability` (e.g., from 0.35 to 0.10)
- Reduce `max_consecutive_skips` (e.g., from 2 to 1)

---

### **Problem: Jump commands are being skipped**

**Solution:**
- This should never happen (Jump commands are never skipped)
- Check `should_skip_current_point()` logic
- Verify `isinstance(element, Point)` check

---

## 🎯 **Files Modified**

1. **`src/routine/routine.py`**
   - Added skip probability and tracking
   - Added `should_skip_current_point()` method

2. **`src/modules/bot.py`**
   - Modified `_main()` to check skip before executing

---

## 🎯 **Status**

✅ **Implementation Complete**
✅ **Ready for Testing**
✅ **No Linter Errors**
✅ **Code Compiles Successfully**

---

**Last Updated:** 2024
**Status:** ✅ Ready for Testing

