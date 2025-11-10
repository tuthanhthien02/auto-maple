# 🎯 Point Selection Randomization - Quick Reference

## 📋 **Tóm Tắt**

Plan này phân tích **khả thi** của việc **Randomize thứ tự ghé Points** trong codebase sử dụng routine structure.

---

## ✅ **FEASIBILITY: CÓ THỂ**

### **Khả thi:** ✅ **CÓ THỂ** implement Point Selection Randomization

**Lý do:**
1. ✅ Routine structure linh hoạt: có thể skip points
2. ✅ Jump commands vẫn hoạt động: chỉ skip Point components
3. ✅ Labels vẫn hoạt động: label.index không thay đổi
4. ✅ Có thể control skip probability và consecutive skips

---

## ⚠️ **CẦN CẨN THẬN VỚI:**

### **1. Jump Commands** ⚠️⚠️⚠️

**Problem:**
- Nếu skip point có Jump command, có thể break loop logic
- Jump commands thay đổi index, không phải sequential

**Solution:**
- ✅ **NEVER skip Jump commands** - Chỉ skip Point components
- ✅ Check `isinstance(element, Point)` before skipping

---

### **2. Sequential Dependencies** ⚠️⚠️

**Problem:**
- Một số points có thể phụ thuộc vào thứ tự (ví dụ: buff trước khi attack)
- Nếu skip point quan trọng, có thể break logic

**Solution:**
- ✅ **Skip probability thấp** (5-10%) để tránh skip quá nhiều
- ✅ **Max consecutive skips** (2) để tránh skip quá nhiều liên tiếp
- ✅ **Critical points** (Phase 2) để mark points as never skip

---

### **3. Labels và Index Tracking** ⚠️

**Problem:**
- Labels có `index` property, nếu skip points, index có thể không match

**Solution:**
- ✅ **Labels vẫn hoạt động đúng** vì `label.index` được set khi compile, không thay đổi
- ✅ **Jump commands vẫn hoạt động đúng** vì jump đến label.index

---

## 🎯 **Recommended Approach: Skip Points**

### **Mô tả:**
- Skip một số Points (5-10% chance)
- Chỉ skip **Point components**, không skip Jump, Label, Setting
- Track visited points để tránh skip quá nhiều

**Ưu điểm:**
- ✅ Đơn giản và dễ implement
- ✅ Không break Jump logic
- ✅ Không break Label logic
- ✅ Có thể control skip probability

---

## 📊 **Implementation Plan**

### **Phase 1: Basic Skip Logic** ✅

**Features:**
1. Skip Points (10% chance)
2. Max 2 consecutive skips
3. Never skip Jump, Label, Setting
4. Logging for skipped points

**Files to Modify:**
- `src/routine/routine.py` - Add `should_skip_current_point()` method, modify `step()` method

---

### **Phase 2: Advanced Features** (Optional) 🔄

**Features:**
1. Critical points (never skip)
2. Skip probability configuration
3. Visit tracking (ensure all points visited)

**Files to Modify:**
- `src/routine/components.py` - Add `critical` flag to Point class
- `src/common/settings.py` - Add skip probability configuration
- `src/routine/routine.py` - Add visit tracking

---

## 🎯 **Code Example**

### **Phase 1: Basic Skip Logic**

```python
# In Routine class
def __init__(self):
    # ... existing code ...
    self.skip_probability = 0.10  # 10% chance to skip
    self.consecutive_skips = 0
    self.max_consecutive_skips = 2  # Max 2 consecutive skips

def should_skip_current_point(self):
    """Check if we should skip current point."""
    import random
    from src.routine.components import Point
    
    # Get current element
    if self.index >= len(self.sequence):
        return False
    
    element = self.sequence[self.index]
    
    # NEVER skip non-Point components (Jump, Label, Setting)
    if not isinstance(element, Point):
        return False
    
    # Check consecutive skips
    if self.consecutive_skips >= self.max_consecutive_skips:
        return False
    
    # Random skip probability
    should_skip = random.random() < self.skip_probability
    
    if should_skip:
        self.consecutive_skips += 1
    else:
        self.consecutive_skips = 0
    
    return should_skip

def step(self):
    """Step to next index, skipping points if needed."""
    # Normal step
    self.index = (self.index + 1) % len(self.sequence) if len(self.sequence) > 0 else 0
    
    # Skip points if needed (but respect max consecutive skips)
    skip_count = 0
    while skip_count < self.max_consecutive_skips and self.should_skip_current_point():
        # Skip this point and move to next
        self.index = (self.index + 1) % len(self.sequence) if len(self.sequence) > 0 else 0
        skip_count += 1
        self.consecutive_skips = skip_count
```

---

## 🎯 **Expected Results**

### **After Phase 1:**

1. **Point Selection Randomization:**
   - ✅ Points can be skipped (10% chance)
   - ✅ Max 2 consecutive skips
   - ✅ Jump commands are never skipped
   - ✅ Labels and Settings are never skipped
   - ✅ Routine execution is less predictable

2. **Logging:**
   - ✅ Skipped points are logged
   - ✅ Consecutive skips are tracked

---

## 🎯 **Risks and Mitigations**

### **Risk 1: Breaking Jump Logic** ⚠️⚠️⚠️

**Mitigation:**
- ✅ **NEVER skip Jump commands** - Only skip Point components

### **Risk 2: Breaking Sequential Dependencies** ⚠️⚠️

**Mitigation:**
- ✅ **Skip probability thấp** (5-10%)
- ✅ **Max consecutive skips** (2)
- ✅ **Critical points** (Phase 2)

---

## 🎯 **Next Steps**

1. **Review Plan:** Xem xét `POINT_SELECTION_RANDOMIZATION_PLAN.md`
2. **Implement Phase 1:** Basic Skip Logic
3. **Test Phase 1:** Test với simple routine và routine có Jump commands
4. **Implement Phase 2 (Optional):** Advanced Features
5. **Test Phase 2:** Test advanced features

---

**Last Updated:** 2024
**Status:** ✅ Quick Reference Ready

