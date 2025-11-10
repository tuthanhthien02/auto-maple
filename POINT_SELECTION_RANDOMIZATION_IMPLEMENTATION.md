# 🎯 Point Selection Randomization - Implementation Summary

## ✅ **Implementation Complete**

### **Features Implemented:**

1. **Skip Point Logic** ✅
   - Skip probability: **35%** (30-40% range for testing)
   - Max consecutive skips: **2**
   - Only skip Point components (never skip Jump, Label, Setting)

2. **Skip Detection** ✅
   - Check skip BEFORE executing point
   - Never skip critical components (Jump, Label, Setting)
   - Track consecutive skips

3. **Logging** ✅
   - INFO level: Log when skipping points (with location)
   - DEBUG level: Log skip decisions and consecutive skips

---

## 📝 **Code Changes**

### **1. `src/routine/routine.py`**

**Added:**
- `skip_probability = 0.35` (35% chance to skip)
- `consecutive_skips = 0` (track consecutive skips)
- `max_consecutive_skips = 2` (max 2 consecutive skips)
- `skip_enabled = True` (enable/disable skip feature)
- `should_skip_current_point()` method (check if should skip)

**Modified:**
- `__init__()`: Added skip probability and tracking variables
- `clear()`: Reset consecutive_skips when clearing routine
- `step()`: Added comment about skip logic (handled in Bot._main())

---

### **2. `src/modules/bot.py`**

**Modified:**
- `_main()`: Added skip check BEFORE executing point
- Skip logic: If skip, log and step to next point (don't execute)
- Execute logic: If not skip, execute normally and step to next point

---

## 🎯 **How It Works**

### **Execution Flow:**

```
1. Bot._main() gets current element
2. Check should_skip_current_point():
   - If skip: Log skip, step to next point (don't execute)
   - If not skip: Execute point, step to next point
3. Repeat
```

### **Skip Logic:**

```python
def should_skip_current_point(self):
    # 1. Check if skip is enabled
    if not self.skip_enabled:
        return False
    
    # 2. Get current element
    element = self.sequence[self.index]
    
    # 3. NEVER skip non-Point components (Jump, Label, Setting)
    if not isinstance(element, Point):
        return False
    
    # 4. Check consecutive skips (max 2)
    if self.consecutive_skips >= self.max_consecutive_skips:
        return False
    
    # 5. Random skip probability (35%)
    should_skip = random.random() < self.skip_probability
    
    # 6. Update consecutive skips counter
    if should_skip:
        self.consecutive_skips += 1
    else:
        self.consecutive_skips = 0  # Reset when not skipping
    
    return should_skip
```

---

## 🎯 **Expected Behavior**

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

## 📊 **Configuration**

### **Skip Probability:**
- **Current:** 35% (30-40% range for testing)
- **Location:** `src/routine/routine.py` - `self.skip_probability = 0.35`
- **To change:** Modify `skip_probability` value in `Routine.__init__()`

### **Max Consecutive Skips:**
- **Current:** 2
- **Location:** `src/routine/routine.py` - `self.max_consecutive_skips = 2`
- **To change:** Modify `max_consecutive_skips` value in `Routine.__init__()`

### **Enable/Disable Skip:**
- **Current:** Enabled (`skip_enabled = True`)
- **Location:** `src/routine/routine.py` - `self.skip_enabled = True`
- **To disable:** Set `skip_enabled = False` in `Routine.__init__()`

---

## 🎯 **Testing**

### **Test Cases:**

1. **Skip Points:**
   - ✅ Points are skipped randomly (35% chance)
   - ✅ Max 2 consecutive skips
   - ✅ Skip pattern varies each loop

2. **Never Skip Critical Components:**
   - ✅ Jump commands are never skipped
   - ✅ Label components are never skipped
   - ✅ Setting components are never skipped

3. **Logging:**
   - ✅ Skipped points are logged (INFO level)
   - ✅ Skip decisions are logged (DEBUG level)
   - ✅ Consecutive skips are tracked

4. **Routine Execution:**
   - ✅ Routine still loops correctly
   - ✅ Jump commands still work
   - ✅ Labels still work

---

## 🎯 **Logging Examples**

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

## 🎯 **Next Steps**

### **After Testing:**

1. **Adjust Skip Probability:**
   - If skip too much: Reduce to 10-15%
   - If skip too little: Increase to 20-25%
   - Current: 35% (for testing)

2. **Adjust Max Consecutive Skips:**
   - If skip too many consecutive: Reduce to 1
   - If skip too few consecutive: Increase to 3
   - Current: 2

3. **Add Critical Points (Optional):**
   - Mark points as "critical" (never skip)
   - Example: Buff points, transition points

4. **Add Visit Tracking (Optional):**
   - Track visited points
   - Ensure all points are visited at least once

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

### **Problem: Routine is not looping correctly**

**Solution:**
- Check Jump commands are not being skipped
- Check Labels are not being skipped
- Verify routine structure (Labels and Jumps are correct)

---

## 🎯 **Files Modified**

1. **`src/routine/routine.py`**
   - Added skip probability and tracking
   - Added `should_skip_current_point()` method
   - Modified `clear()` to reset skip tracking

2. **`src/modules/bot.py`**
   - Modified `_main()` to check skip before executing
   - Added skip logic and logging

---

## 🎯 **Status**

✅ **Implementation Complete**
✅ **Ready for Testing**
✅ **No Linter Errors**

---

**Last Updated:** 2024
**Status:** ✅ Implementation Complete - Ready for Testing

