# 🎯 Plan: Routine Pattern Variation

## 📋 **Tổng Quan**

Routine Pattern Variation là tính năng cho phép bot chạy routine theo nhiều "variants" (biến thể) khác nhau, giúp tạo variation lớn trong bot behavior và giảm pattern detection.

---

## 🎯 **Mục Tiêu**

### **1. Multiple Variants**
- **Normal:** Chạy routine theo thứ tự bình thường (0 → 1 → 2 → ... → N → 0)
- **Reverse:** Chạy routine theo thứ tự ngược lại (N → N-1 → ... → 1 → 0 → N)
- **Floor 1 Only:** Chỉ train ở Floor 1 (skip Floor 2)
- **Floor 2 Only:** Chỉ train ở Floor 2 (skip Floor 1)

### **2. Variant Switching**
- Switch variant sau mỗi N loops (random)
- Switch variant tại các label points (safe points)
- Track variant execution history

### **3. Floor Detection**
- Tự động detect Floor 1 vs Floor 2 dựa trên Y coordinate
- Hoặc dựa trên labels (f1_*, f2_*)
- Hoặc dựa trên routine structure

---

## 🔍 **Phân Tích Routine Structure**

### **Current Routine Structure (tree_2_floor_new.csv):**

```
Label,start_routine
Comment,=== FLOOR 1 START: Move Left → Right (y ≈ 0.19) ===
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
...
*,0.707,0.19,adjust=False,frequency=1
Label,f1_pos_8
Comment,=== FLOOR 2 START: Move Right → Left (y ≈ 0.13) ===
*,0.668,0.132,adjust=False,frequency=1
Label,f2_pos_0
...
*,0.244,0.132,adjust=False,frequency=1
Label,f2_pos_7
```

### **Floor Detection Methods:**

1. **Y Coordinate Based:**
   - Floor 1: `y ≈ 0.19` (horizontal movement)
   - Floor 2: `y ≈ 0.13` (horizontal movement)
   - Threshold: `y > 0.16` → Floor 1, `y <= 0.16` → Floor 2

2. **Label Based:**
   - Floor 1: Labels starting with `f1_*` (e.g., `f1_pos_0`, `f1_pos_1`)
   - Floor 2: Labels starting with `f2_*` (e.g., `f2_pos_0`, `f2_pos_1`)

3. **Comment Based:**
   - Floor 1: Comments containing "FLOOR 1"
   - Floor 2: Comments containing "FLOOR 2"

**Recommended:** Combine Y coordinate + Label for robust detection.

---

## 🎯 **Implementation Plan**

### **Phase 1: Floor Detection** ⭐⭐⭐⭐⭐

#### **1.1. Add Floor Detection to Routine Class**

```python
# In Routine class
def __init__(self):
    # ... existing code ...
    # Routine Pattern Variation
    self.variant_enabled = True
    self.current_variant = 'normal'
    self.variant_switch_counter = 0
    self.variant_switch_interval = random.randint(3, 7)  # Switch every 3-7 loops
    self.floor1_indices = []  # Indices of Floor 1 points
    self.floor2_indices = []  # Indices of Floor 2 points
    self.variant_weights = {
        'normal': 0.70,      # 70% normal
        'reverse': 0.15,     # 15% reverse
        'floor1_only': 0.10, # 10% floor1 only
        'floor2_only': 0.05  # 5% floor2 only
    }

def detect_floors(self):
    """Detect Floor 1 and Floor 2 points based on Y coordinate and labels."""
    self.floor1_indices = []
    self.floor2_indices = []
    
    for i, component in enumerate(self.sequence):
        if isinstance(component, Point):
            # Method 1: Y coordinate based
            y = component.location[1]
            if y > 0.16:  # Floor 1 threshold
                self.floor1_indices.append(i)
            else:  # Floor 2 threshold
                self.floor2_indices.append(i)
            
            # Method 2: Label based (more robust)
            # Check if there's a Label before this Point
            if i > 0 and isinstance(self.sequence[i-1], Label):
                label_name = self.sequence[i-1].name.lower()
                if label_name.startswith('f1_'):
                    if i not in self.floor1_indices:
                        self.floor1_indices.append(i)
                elif label_name.startswith('f2_'):
                    if i not in self.floor2_indices:
                        self.floor2_indices.append(i)
    
    log.info("Floor Detection: Floor 1: %d points, Floor 2: %d points", 
             len(self.floor1_indices), len(self.floor2_indices))
```

#### **1.2. Call Floor Detection on Routine Load**

```python
# In Routine.load()
def load(self, file=None):
    # ... existing code ...
    # Detect floors after loading routine
    if self.variant_enabled:
        self.detect_floors()
```

---

### **Phase 2: Variant Switching Logic** ⭐⭐⭐⭐⭐

#### **2.1. Add Variant Switching Methods**

```python
# In Routine class
def _switch_variant(self):
    """Switch to a random variant based on weights."""
    import random
    
    variants = list(self.variant_weights.keys())
    weights = list(self.variant_weights.values())
    
    # Select variant based on weights
    self.current_variant = random.choices(variants, weights=weights, k=1)[0]
    
    # Reset switch counter
    self.variant_switch_interval = random.randint(3, 7)
    self.variant_switch_counter = 0
    
    log.info("🔄 Routine Pattern Variation: Switched to variant '%s' (switch every %d loops)", 
             self.current_variant, self.variant_switch_interval)

def _should_switch_variant(self):
    """Check if we should switch variant."""
    if not self.variant_enabled:
        return False
    
    # Increment counter
    self.variant_switch_counter += 1
    
    # Check if we've completed enough loops
    if self.variant_switch_counter >= self.variant_switch_interval:
        return True
    
    return False

def _get_variant_start_index(self):
    """Get start index based on current variant."""
    if self.current_variant == 'normal':
        return 0
    elif self.current_variant == 'reverse':
        return len(self.sequence) - 1
    elif self.current_variant == 'floor1_only':
        return self.floor1_indices[0] if self.floor1_indices else 0
    elif self.current_variant == 'floor2_only':
        return self.floor2_indices[0] if self.floor2_indices else 0
    return 0

def _get_variant_next_index(self, current_index):
    """Get next index based on current variant."""
    if len(self.sequence) == 0:
        return 0
    
    if self.current_variant == 'normal':
        # Normal: forward
        return (current_index + 1) % len(self.sequence)
    elif self.current_variant == 'reverse':
        # Reverse: backward
        return (current_index - 1) % len(self.sequence)
    elif self.current_variant == 'floor1_only':
        # Floor 1 only: only visit Floor 1 points
        return self._get_next_floor_index(current_index, self.floor1_indices)
    elif self.current_variant == 'floor2_only':
        # Floor 2 only: only visit Floor 2 points
        return self._get_next_floor_index(current_index, self.floor2_indices)
    return (current_index + 1) % len(self.sequence)

def _get_next_floor_index(self, current_index, floor_indices):
    """Get next index within a specific floor."""
    if not floor_indices:
        return (current_index + 1) % len(self.sequence)
    
    # Find current index in floor_indices
    try:
        current_floor_index = floor_indices.index(current_index)
        # Move to next floor point
        next_floor_index = (current_floor_index + 1) % len(floor_indices)
        return floor_indices[next_floor_index]
    except ValueError:
        # Current index not in floor, start from first floor point
        return floor_indices[0]
```

---

### **Phase 3: Integrate Variant Logic into Step** ⭐⭐⭐⭐⭐

#### **3.1. Modify Step Method**

```python
# In Routine class
def step(self):
    """Step to next component based on current variant."""
    if len(self.sequence) == 0:
        return
    
    # Check if we should switch variant
    if self._should_switch_variant():
        self._switch_variant()
        # Reset to variant start index
        self.index = self._get_variant_start_index()
        return
    
    # Step based on current variant
    self.index = self._get_variant_next_index(self.index)
    
    # Log variant step
    log.debug("Routine Pattern Variation: Variant '%s', Index: %d/%d", 
              self.current_variant, self.index, len(self.sequence) - 1)
```

#### **3.2. Modify Load Method to Initialize Variant**

```python
# In Routine.load()
def load(self, file=None):
    # ... existing code ...
    # Initialize variant
    if self.variant_enabled:
        self.detect_floors()
        self._switch_variant()  # Initialize with random variant
        self.index = self._get_variant_start_index()
        log.info("🎯 Routine Pattern Variation: Initialized with variant '%s'", 
                 self.current_variant)
```

---

### **Phase 4: Label-Based Switching (Advanced)** ⭐⭐⭐⭐

#### **4.1. Switch Variant at Label Points**

```python
# In Routine class
def _should_switch_variant_at_label(self):
    """Check if we should switch variant at label point."""
    if not self.variant_enabled:
        return False
    
    # Check if current component is a Label
    if self.index < len(self.sequence):
        component = self.sequence[self.index]
        if isinstance(component, Label):
            # 20% chance to switch variant at label point
            import random
            if random.random() < 0.20:
                return True
    
    return False

# Modify step() to check label switching
def step(self):
    """Step to next component based on current variant."""
    if len(self.sequence) == 0:
        return
    
    # Check if we should switch variant at label
    if self._should_switch_variant_at_label():
        self._switch_variant()
        self.index = self._get_variant_start_index()
        log.info("🔄 Routine Pattern Variation: Switched variant at label '%s'", 
                 self.sequence[self.index].name if self.index < len(self.sequence) else 'unknown')
        return
    
    # ... existing step logic ...
```

---

### **Phase 5: Loop Detection** ⭐⭐⭐

#### **5.1. Track Loop Completion**

```python
# In Routine class
def __init__(self):
    # ... existing code ...
    self.loop_count = 0
    self.last_index = -1

def step(self):
    """Step to next component based on current variant."""
    if len(self.sequence) == 0:
        return
    
    # Detect loop completion (when index wraps around)
    if self.last_index != -1 and self.index < self.last_index:
        self.loop_count += 1
        log.info("🔄 Routine Pattern Variation: Loop %d completed (variant: '%s')", 
                 self.loop_count, self.current_variant)
    
    self.last_index = self.index
    
    # ... existing step logic ...
```

---

## 📊 **Variant Execution Examples**

### **Variant 1: Normal**

```
Loop 1: f1_pos_0 → f1_pos_1 → ... → f1_pos_8 → f2_pos_0 → ... → f2_pos_7 → f1_pos_0
Loop 2: f1_pos_0 → f1_pos_1 → ... → f1_pos_8 → f2_pos_0 → ... → f2_pos_7 → f1_pos_0
```

### **Variant 2: Reverse**

```
Loop 1: f2_pos_7 → f2_pos_6 → ... → f2_pos_0 → f1_pos_8 → ... → f1_pos_0 → f2_pos_7
Loop 2: f2_pos_7 → f2_pos_6 → ... → f2_pos_0 → f1_pos_8 → ... → f1_pos_0 → f2_pos_7
```

### **Variant 3: Floor 1 Only**

```
Loop 1: f1_pos_0 → f1_pos_1 → ... → f1_pos_8 → f1_pos_0
Loop 2: f1_pos_0 → f1_pos_1 → ... → f1_pos_8 → f1_pos_0
Loop 3: f1_pos_0 → f1_pos_1 → ... → f1_pos_8 → f1_pos_0
```

### **Variant 4: Floor 2 Only**

```
Loop 1: f2_pos_0 → f2_pos_1 → ... → f2_pos_7 → f2_pos_0
Loop 2: f2_pos_0 → f2_pos_1 → ... → f2_pos_7 → f2_pos_0
Loop 3: f2_pos_0 → f2_pos_1 → ... → f2_pos_7 → f2_pos_0
```

---

## 🎯 **Configuration**

### **Variant Weights:**

```python
self.variant_weights = {
    'normal': 0.70,      # 70% normal (default)
    'reverse': 0.15,     # 15% reverse
    'floor1_only': 0.10, # 10% floor1 only
    'floor2_only': 0.05  # 5% floor2 only
}
```

### **Switch Interval:**

```python
self.variant_switch_interval = random.randint(3, 7)  # Switch every 3-7 loops
```

### **Label Switch Probability:**

```python
label_switch_probability = 0.20  # 20% chance to switch at label
```

---

## 📝 **Files to Modify**

### **1. `src/routine/routine.py`**

**Changes:**
- Add variant attributes to `__init__()`
- Add `detect_floors()` method
- Add `_switch_variant()` method
- Add `_should_switch_variant()` method
- Add `_get_variant_start_index()` method
- Add `_get_variant_next_index()` method
- Add `_get_next_floor_index()` method
- Modify `step()` to use variant logic
- Modify `load()` to initialize variant
- Add `_should_switch_variant_at_label()` method (optional)
- Add loop detection (optional)

---

## 🎯 **Implementation Steps**

### **Step 1: Floor Detection (Day 1)**

1. ✅ Add floor detection attributes to `Routine.__init__()`
2. ✅ Implement `detect_floors()` method
3. ✅ Call `detect_floors()` in `Routine.load()`
4. ✅ Test floor detection with `tree_2_floor_new.csv`

### **Step 2: Variant Switching Logic (Day 2)**

1. ✅ Add variant switching methods
2. ✅ Implement `_switch_variant()` method
3. ✅ Implement `_get_variant_start_index()` method
4. ✅ Implement `_get_variant_next_index()` method
5. ✅ Test variant switching logic

### **Step 3: Integrate into Step (Day 3)**

1. ✅ Modify `step()` to use variant logic
2. ✅ Modify `load()` to initialize variant
3. ✅ Test variant execution with bot

### **Step 4: Advanced Features (Day 4-5, Optional)**

1. ✅ Add label-based switching
2. ✅ Add loop detection
3. ✅ Add variant execution history tracking
4. ✅ Test advanced features

---

## 🎯 **Testing Plan**

### **Test 1: Floor Detection**

```python
# Test with tree_2_floor_new.csv
routine.load('tree_2_floor_new.csv')
routine.detect_floors()
assert len(routine.floor1_indices) > 0
assert len(routine.floor2_indices) > 0
```

### **Test 2: Variant Switching**

```python
# Test variant switching
routine._switch_variant()
assert routine.current_variant in ['normal', 'reverse', 'floor1_only', 'floor2_only']
```

### **Test 3: Variant Execution**

```python
# Test variant execution
routine.current_variant = 'floor1_only'
routine.index = routine._get_variant_start_index()
for i in range(10):
    routine.step()
    assert routine.index in routine.floor1_indices
```

### **Test 4: Integration Test**

```python
# Test with bot
bot.start()
# Observe variant switching in logs
# Verify bot executes different variants
```

---

## 🎯 **Expected Results**

### **After Implementation:**

1. ✅ **Floor Detection:** Bot automatically detects Floor 1 and Floor 2 points
2. ✅ **Variant Switching:** Bot switches between variants every 3-7 loops
3. ✅ **Variant Execution:** Bot executes routine according to current variant
4. ✅ **Variation:** Bot behavior varies significantly between variants

### **Logs:**

```
🎯 Routine Pattern Variation: Initialized with variant 'normal'
🔄 Routine Pattern Variation: Switched to variant 'reverse' (switch every 5 loops)
🔄 Routine Pattern Variation: Loop 5 completed (variant: 'reverse')
🔄 Routine Pattern Variation: Switched to variant 'floor1_only' (switch every 4 loops)
```

---

## 🎯 **Risks and Mitigation**

### **Risk 1: Floor Detection Accuracy**

**Risk:** Floor detection might not be accurate for all routines.

**Mitigation:**
- Use multiple detection methods (Y coordinate + Label)
- Allow manual floor configuration (optional)
- Log floor detection results for debugging

### **Risk 2: Variant Switching Too Frequent**

**Risk:** Switching too frequently might cause confusion.

**Mitigation:**
- Use reasonable switch interval (3-7 loops)
- Switch only at safe points (labels)
- Track variant execution history

### **Risk 3: Floor-Only Variants Stuck**

**Risk:** Floor-only variants might get stuck if floor detection fails.

**Mitigation:**
- Fallback to normal variant if floor detection fails
- Validate floor indices before switching
- Log warnings if floor detection fails

---

## 🎯 **Next Steps**

1. **Review Plan:** Review và approve plan
2. **Implement Phase 1:** Floor Detection
3. **Test Phase 1:** Test floor detection
4. **Implement Phase 2:** Variant Switching Logic
5. **Test Phase 2:** Test variant switching
6. **Implement Phase 3:** Integrate into Step
7. **Test Phase 3:** Test variant execution
8. **Implement Phase 4 (Optional):** Advanced Features
9. **Test All Phases:** Integration test

---

## 📚 **References**

- `ANTI_REPETITIVE_PATTERNS_PLAN.md` - Overall anti-repetitive patterns plan
- `POINT_SELECTION_RANDOMIZATION_PLAN.md` - Point selection randomization (already implemented)
- `resources/routines/luminous/tree_2_floor_new.csv` - Example routine file

---

**Last Updated:** 2024
**Status:** ✅ Plan Ready for Implementation

