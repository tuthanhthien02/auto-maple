# 🎯 Plan: Point Selection Randomization

## 📋 **Tổng Quan**

Plan này phân tích **khả thi** của việc **Randomize thứ tự ghé Points** trong codebase sử dụng routine structure với Labels, Jumps, và các dependencies.

---

## 🔍 **Phân Tích Routine Structure**

### **1. Routine Components**

Routine có các Components sau:
- **Point**: Vị trí trong routine, có commands
- **Label**: Đánh dấu vị trí (được sử dụng bởi Jump)
- **Jump**: Nhảy đến Label (thay đổi `config.routine.index`)
- **Setting**: Thay đổi settings
- **Comment**: Chỉ là comment (không execute)

### **2. Execution Flow**

**Current Flow:**
```python
# In Bot._main()
element = config.routine[config.routine.index]  # Get element at current index
element.execute()                                # Execute element
config.routine.step()                            # Step to next index (sequential)
```

**Step Function:**
```python
# In Routine.step()
def step(self):
    """Increments index and wraps back to 0 at the end."""
    self.index = (self.index + 1) % len(self.sequence) if len(self.sequence) > 0 else 0
```

### **3. Jump Commands**

**Jump Behavior:**
```python
# In Jump.main()
def main(self):
    if self.link is None:
        log.error("Label '%s' does not exist", self.label)
    else:
        if self.counter == 0:
            config.routine.index = self.link.index  # DIRECTLY change index
        self._increment_counter()
```

**Important:** Jump commands **directly change** `config.routine.index`, bypassing sequential stepping.

---

## 🎯 **Feasibility Analysis**

### **✅ CÓ THỂ Randomize Point Selection**

**Lý do:**
1. ✅ Routine structure linh hoạt: `sequence` là array, có thể access bất kỳ index nào
2. ✅ Labels và Jumps vẫn hoạt động: Labels có `index` property, Jumps có thể jump đến bất kỳ Label nào
3. ✅ Không có hard dependencies: Points độc lập, không phụ thuộc vào thứ tự (trừ khi có logic đặc biệt)

### **⚠️ CẦN CẨN THẬN VỚI:**

#### **1. Jump Commands** ⚠️⚠️⚠️

**Problem:**
- Nếu skip point có Jump command, có thể break loop logic
- Jump commands thay đổi index, không phải sequential

**Example:**
```
Routine:
- Point 0 (f1_pos_0)
- Point 1 (f1_pos_1)
- ...
- Point N (jump_down)
- Jump,f1_pos_0  ← Nếu skip Jump này, routine sẽ không loop lại!

Normal: Point N → Jump → Point 0 (loop)
Skip Jump: Point N → Point 0 (no loop, breaks logic)
```

**Solution:**
- **NEVER skip Jump commands** - Jump commands là critical for loop logic
- Skip chỉ áp dụng cho **Point components**, không áp dụng cho Jump, Label, Setting

---

#### **2. Sequential Dependencies** ⚠️⚠️

**Problem:**
- Một số points có thể phụ thuộc vào thứ tự (ví dụ: buff trước khi attack)
- Nếu skip point quan trọng, có thể break logic

**Example:**
```
Routine:
- Point 0: buff, buff_secondary  ← Critical: Must execute before attacks
- Point 1: reflection_random
- Point 2: reflection_random
- ...

If skip Point 0: Bot không có buff → break gameplay
```

**Solution:**
- **Skip probability thấp** (5-10%) để tránh skip quá nhiều
- **Track visited points** để đảm bảo không skip quá nhiều points liên tiếp
- **Never skip critical points** (có thể mark points as "critical" trong routine)

---

#### **3. Labels và Index Tracking** ⚠️

**Problem:**
- Labels có `index` property, nếu skip points, index có thể không match
- Jump commands sử dụng `label.index` để jump

**Example:**
```
Routine:
- Label,f1_pos_0  (index=0)
- Point 0
- Point 1
- Label,f1_pos_1  (index=3)
- Point 2
- Jump,f1_pos_0  ← Jumps to index=0

If skip Point 1: Label index vẫn đúng, nhưng có gap trong sequence
```

**Solution:**
- **Labels vẫn hoạt động đúng** vì `label.index` được set khi compile, không thay đổi
- **Jump commands vẫn hoạt động đúng** vì jump đến label.index, không phụ thuộc vào sequential stepping

---

#### **4. GUI Display** ⚠️

**Problem:**
- GUI highlight current point: `config.gui.view.routine.select(config.routine.index)`
- Nếu skip points, GUI có thể không hiển thị đúng

**Solution:**
- **GUI vẫn hoạt động đúng** vì nó chỉ highlight `config.routine.index`, không phụ thuộc vào sequential stepping
- Có thể thêm log để track skipped points

---

## 🎯 **Implementation Strategy**

### **Approach 1: Skip Points (Recommended)** ⭐⭐⭐⭐⭐

**Mô tả:**
- Skip một số Points (5-10% chance)
- Chỉ skip **Point components**, không skip Jump, Label, Setting
- Track visited points để tránh skip quá nhiều

**Ưu điểm:**
- ✅ Đơn giản và dễ implement
- ✅ Không break Jump logic
- ✅ Không break Label logic
- ✅ Có thể control skip probability

**Nhược điểm:**
- ❌ Không randomize thứ tự (chỉ skip)
- ❌ Vẫn có pattern (sequential với skip)

---

### **Approach 2: Randomize Order (Advanced)** ⭐⭐⭐

**Mô tả:**
- Randomize thứ tự visit các Points
- Vẫn respect Jump commands
- Tạo "visit queue" với random order

**Ưu điểm:**
- ✅ Randomize thứ tự thực sự
- ✅ Tạo variation lớn

**Nhược điểm:**
- ❌ Phức tạp hơn
- ❌ Có thể break sequential dependencies
- ❌ Khó track visited points

---

### **Approach 3: Hybrid (Skip + Limited Randomization)** ⭐⭐⭐⭐

**Mô tả:**
- Skip một số Points (5-10% chance)
- Đôi khi jump đến point khác (không phải next) với probability thấp (2-5%)
- Vẫn respect Jump commands

**Ưu điểm:**
- ✅ Có cả skip và randomization
- ✅ Không break Jump logic
- ✅ Tạo variation tốt

**Nhược điểm:**
- ❌ Phức tạp hơn Approach 1
- ❌ Cần track visited points carefully

---

## 🎯 **Recommended Approach: Skip Points (Approach 1)**

### **Implementation Plan**

#### **Phase 1: Basic Skip Logic**

**Step 1: Add Skip Logic to Routine Class**

```python
# In Routine class
def __init__(self):
    self.dirty = False
    self.path = ''
    self.labels = {}
    self.index = 0
    self.sequence = []
    self.display = []
    # NEW: Point selection randomization
    self.skip_probability = 0.10  # 10% chance to skip
    self.consecutive_skips = 0
    self.max_consecutive_skips = 2  # Max 2 consecutive skips

def should_skip_current_point(self):
    """
    Check if we should skip current point.
    Only skip Point components, never skip Jump, Label, Setting.
    """
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
        return False  # Don't skip if we've skipped too many consecutive points
    
    # Random skip probability
    should_skip = random.random() < self.skip_probability
    
    if should_skip:
        self.consecutive_skips += 1
    else:
        self.consecutive_skips = 0  # Reset counter
    
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

#### **Step 2: Modify Bot._main() to Check Skip Before Execute**

```python
# In Bot._main()
def _main(self):
    while True:
        if config.enabled and len(config.routine) > 0:
            # Update activity for anti-detect
            current_time = time.time()
            if current_time - last_activity_update > 1.0:
                update_activity()
                last_activity_update = current_time
            
            # Highlight the current Point
            config.gui.view.routine.select(config.routine.index)
            config.gui.view.details.display_info(config.routine.index)
            
            # Get current element
            element = config.routine[config.routine.index]
            
            # NEW: Check if we should skip BEFORE executing
            # Note: We check skip in step() now, so we just execute
            # But we can add additional skip check here if needed
            element.execute()
            
            # Step to next (with skip logic)
            config.routine.step()
            
            time.sleep(0.05)
        else:
            time.sleep(0.2)
```

---

#### **Step 3: Add Logging**

```python
# In Routine.should_skip_current_point()
def should_skip_current_point(self):
    """Check if we should skip current point."""
    import random
    from src.routine.components import Point
    from src.common.logger import get_logger
    
    log = get_logger(__name__)
    
    # Get current element
    if self.index >= len(self.sequence):
        return False
    
    element = self.sequence[self.index]
    
    # NEVER skip non-Point components
    if not isinstance(element, Point):
        return False
    
    # Check consecutive skips
    if self.consecutive_skips >= self.max_consecutive_skips:
        return False
    
    # Random skip probability
    should_skip = random.random() < self.skip_probability
    
    if should_skip:
        self.consecutive_skips += 1
        log.debug("Skipping point at index %d (consecutive skips: %d)", 
                 self.index, self.consecutive_skips)
    else:
        self.consecutive_skips = 0
    
    return should_skip
```

---

### **Phase 2: Advanced Features (Optional)**

#### **Feature 1: Critical Points**

**Mô tả:**
- Mark points as "critical" (never skip)
- Critical points: buff points, transition points, etc.

**Implementation:**
```python
# In Point class
def __init__(self, x, y, frequency=1, skip='False', adjust='False', critical='False'):
    super().__init__(locals())
    self.x = float(x)
    self.y = float(y)
    self.location = (self.x, self.y)
    self.frequency = settings.validate_nonnegative_int(frequency)
    self.counter = int(settings.validate_boolean(skip))
    self.adjust = settings.validate_boolean(adjust)
    self.critical = settings.validate_boolean(critical)  # NEW: Critical point flag
    if not hasattr(self, 'commands'):
        self.commands = []

# In Routine.should_skip_current_point()
def should_skip_current_point(self):
    """Check if we should skip current point."""
    # ... existing code ...
    
    # NEVER skip critical points
    if hasattr(element, 'critical') and element.critical:
        return False
    
    # ... rest of code ...
```

---

#### **Feature 2: Skip Probability Configuration**

**Mô tả:**
- Allow user to configure skip probability
- Add GUI setting for skip probability

**Implementation:**
```python
# In settings.py
SKIP_PROBABILITY = 0.10  # 10% chance to skip
MAX_CONSECUTIVE_SKIPS = 2  # Max 2 consecutive skips

# In Routine class
def __init__(self):
    # ... existing code ...
    self.skip_probability = settings.SKIP_PROBABILITY
    self.max_consecutive_skips = settings.MAX_CONSECUTIVE_SKIPS
```

---

#### **Feature 3: Visit Tracking**

**Mô tả:**
- Track visited points
- Ensure all points are visited at least once before skipping

**Implementation:**
```python
# In Routine class
def __init__(self):
    # ... existing code ...
    self.visited_points = set()  # Track visited point indices
    self.visit_all_before_skip = True  # Visit all points before skipping

def should_skip_current_point(self):
    """Check if we should skip current point."""
    # ... existing code ...
    
    # If visit_all_before_skip is True, don't skip until all points visited
    if self.visit_all_before_skip:
        point_indices = [i for i, e in enumerate(self.sequence) if isinstance(e, Point)]
        if len(self.visited_points) < len(point_indices):
            # Haven't visited all points yet, don't skip
            return False
    
    # ... rest of code ...

def step(self):
    """Step to next index, tracking visited points."""
    # Mark current point as visited
    element = self.sequence[self.index]
    if isinstance(element, Point):
        self.visited_points.add(self.index)
    
    # ... rest of step logic ...
```

---

## 🎯 **Implementation Checklist**

### **Phase 1: Basic Skip Logic**

- [ ] Add `should_skip_current_point()` method to Routine class
- [ ] Add `skip_probability` and `max_consecutive_skips` to Routine class
- [ ] Modify `step()` method to skip points
- [ ] Modify `Bot._main()` to handle skip logic (if needed)
- [ ] Add logging for skipped points
- [ ] Test skip logic with simple routine
- [ ] Test skip logic with routine containing Jump commands
- [ ] Test skip logic with routine containing Labels

---

### **Phase 2: Advanced Features (Optional)**

- [ ] Add `critical` flag to Point class
- [ ] Modify `should_skip_current_point()` to respect critical points
- [ ] Add skip probability configuration to settings
- [ ] Add GUI setting for skip probability (if needed)
- [ ] Add visit tracking to Routine class
- [ ] Modify `step()` to track visited points
- [ ] Test advanced features

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

### **After Phase 2:**

3. **Advanced Features:**
   - ✅ Critical points are never skipped
   - ✅ Skip probability is configurable
   - ✅ Visit tracking ensures all points are visited

---

## 📚 **Files to Modify**

### **Phase 1:**
- `src/routine/routine.py` - Add `should_skip_current_point()` method, modify `step()` method
- `src/modules/bot.py` - Modify `_main()` if needed (may not be necessary)

### **Phase 2:**
- `src/routine/components.py` - Add `critical` flag to Point class
- `src/common/settings.py` - Add skip probability configuration
- `src/routine/routine.py` - Add visit tracking

---

## 🎯 **Risks and Mitigations**

### **Risk 1: Breaking Jump Logic** ⚠️⚠️⚠️

**Risk:**
- Nếu skip Jump command, routine sẽ không loop lại
- Jump commands là critical for loop logic

**Mitigation:**
- ✅ **NEVER skip Jump commands** - Only skip Point components
- ✅ Check `isinstance(element, Point)` before skipping

---

### **Risk 2: Breaking Sequential Dependencies** ⚠️⚠️

**Risk:**
- Một số points có thể phụ thuộc vào thứ tự (ví dụ: buff trước khi attack)
- Nếu skip point quan trọng, có thể break logic

**Mitigation:**
- ✅ **Skip probability thấp** (5-10%) để tránh skip quá nhiều
- ✅ **Max consecutive skips** (2) để tránh skip quá nhiều liên tiếp
- ✅ **Critical points** (Phase 2) để mark points as never skip

---

### **Risk 3: GUI Display Issues** ⚠️

**Risk:**
- GUI có thể không hiển thị đúng nếu skip points
- User có thể confused về current point

**Mitigation:**
- ✅ **GUI vẫn hoạt động đúng** vì nó chỉ highlight `config.routine.index`
- ✅ **Logging** để track skipped points
- ✅ **GUI can show skipped points** (optional, Phase 2)

---

## 🎯 **Conclusion**

### **✅ FEASIBLE: Point Selection Randomization**

**Khả thi:** ✅ **CÓ THỂ** implement Point Selection Randomization

**Lý do:**
1. ✅ Routine structure linh hoạt: có thể skip points
2. ✅ Jump commands vẫn hoạt động: chỉ skip Point components
3. ✅ Labels vẫn hoạt động: label.index không thay đổi
4. ✅ Có thể control skip probability và consecutive skips

**Limitations:**
1. ⚠️ Chỉ skip Point components, không skip Jump, Label, Setting
2. ⚠️ Cần skip probability thấp (5-10%) để tránh break logic
3. ⚠️ Cần max consecutive skips (2) để tránh skip quá nhiều

**Recommended Approach:**
- ✅ **Approach 1: Skip Points** (Recommended)
- ✅ **Phase 1: Basic Skip Logic** (Implement First)
- ✅ **Phase 2: Advanced Features** (Optional)

---

## 🎯 **Next Steps**

1. **Review Plan:** Xem xét plan và đưa ra feedback
2. **Implement Phase 1:** Basic Skip Logic
3. **Test Phase 1:** Test với simple routine và routine có Jump commands
4. **Implement Phase 2 (Optional):** Advanced Features
5. **Test Phase 2:** Test advanced features

---

**Last Updated:** 2024
**Status:** ✅ Plan Ready for Review

