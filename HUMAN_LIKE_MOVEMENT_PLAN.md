# 🎯 Human-Like Movement Improvement Plan

## 📋 **PHÂN TÍCH HIỆN TRẠNG**

### **Movement System Hiện Tại:**

1. **Move Command (`src/routine/components.py`):**
   - Sử dụng `get_human_delay()` cho delays giữa các steps
   - Fixed delays: `0.15s` (horizontal), `0.05s` (vertical)
   - Toggle giữa horizontal và vertical movement
   - Không có variation trong movement patterns

2. **Step Function (`resources/command_books/luminous-corsair.py`):**
   - Fixed timing: `time.sleep(0.1)` cho horizontal walk
   - Fixed timing: `time.sleep(0.05)` sau walk
   - Không có random variation trong timing
   - Không có micro-pauses giữa movements

3. **Walk Command (`src/routine/components.py`):**
   - Sử dụng `get_human_delay()` cho duration
   - Fixed post-walk pause: `0.05s`
   - Không có variation trong walk patterns

4. **Adjust Command (`resources/command_books/luminous-corsair.py`):**
   - Fixed timing: `time.sleep(0.05)` cho walk
   - Fixed timing: `time.sleep(0.05)` sau jump
   - Không có random variation

### **Vấn Đề Hiện Tại:**

1. **Fixed Timing:**
   - ❌ `time.sleep(0.1)` - Fixed delay, không random
   - ❌ `time.sleep(0.05)` - Fixed delay, không random
   - ❌ Không có variation trong movement timing

2. **Predictable Patterns:**
   - ❌ Toggle giữa horizontal/vertical luôn theo pattern cố định
   - ❌ Không có random pauses giữa movements
   - ❌ Không có variation trong movement speed

3. **Lack of Human Behavior:**
   - ❌ Không có micro-adjustments (như human thường làm)
   - ❌ Không có occasional stops (như human nghỉ ngơi)
   - ❌ Không có variation trong movement direction changes

---

## 🎯 **MỤC TIÊU CẢI THIỆN**

### **Goal:**
Làm cho movement giống human hơn bằng cách:
1. Thêm random timing variation
2. Thêm micro-pauses giữa movements
3. Thêm occasional stops/adjustments
4. Thêm variation trong movement patterns
5. Thêm human-like behavior (như occasional corrections)

---

## 📊 **PLAN CHI TIẾT**

### **PHASE 1: Timing Randomization** ⭐⭐⭐ HIGH PRIORITY

**Mục tiêu:** Thay thế fixed timing bằng random timing variation

#### **Step 1.1: Replace Fixed Delays trong Step Function**

**File:** `resources/command_books/luminous-corsair.py`

**Current:**
```python
def step(direction, target):
    if direction in ('left', 'right'):
        key_down(getattr(Key, direction))
        time.sleep(0.1)  # ❌ Fixed delay
        key_up(getattr(Key, direction))
        time.sleep(0.05)  # ❌ Fixed delay
```

**Proposed:**
```python
def step(direction, target):
    from src.common.vkeys import _get_human_like_delay, _get_micro_pause
    
    if direction in ('left', 'right'):
        key_down(getattr(Key, direction))
        # Random delay: 0.08-0.15s (human-like)
        walk_delay = _get_human_like_delay(0.1, 'down')
        time.sleep(walk_delay)
        key_up(getattr(Key, direction))
        # Random micro-pause: 0.03-0.08s
        post_walk_delay = _get_human_like_delay(0.05, 'up')
        micro_pause = _get_micro_pause()
        time.sleep(post_walk_delay + micro_pause)
```

**Benefits:**
- ✅ Random timing variation
- ✅ Micro-pauses giữa movements
- ✅ Human-like behavior

**Risk:** LOW - Chỉ thay đổi timing, không thay đổi logic

**Time:** 1-2 giờ

---

#### **Step 1.2: Replace Fixed Delays trong Adjust Command**

**File:** `resources/command_books/luminous-corsair.py`

**Current:**
```python
class Adjust(Command):
    def main(self):
        key_down('right')
        time.sleep(0.05)  # ❌ Fixed delay
        # ...
        time.sleep(0.05)  # ❌ Fixed delay
```

**Proposed:**
```python
class Adjust(Command):
    def main(self):
        from src.common.vkeys import _get_human_like_delay, _get_micro_pause
        
        key_down('right')
        # Random delay: 0.03-0.08s
        walk_delay = _get_human_like_delay(0.05, 'fast')
        time.sleep(walk_delay)
        # ...
        # Random micro-pause: 0.02-0.06s
        post_delay = _get_human_like_delay(0.05, 'fast')
        micro_pause = _get_micro_pause()
        time.sleep(post_delay + micro_pause)
```

**Benefits:**
- ✅ Random timing variation
- ✅ Micro-pauses giữa adjustments
- ✅ Human-like behavior

**Risk:** LOW - Chỉ thay đổi timing

**Time:** 1 giờ

---

### **PHASE 2: Movement Pattern Variation** ⭐⭐ MEDIUM PRIORITY

**Mục tiêu:** Thêm variation trong movement patterns

#### **Step 2.1: Add Occasional Stops**

**File:** `src/routine/components.py` - `Move` class

**Proposed:**
```python
def main(self):
    # ... existing code ...
    
    # Occasional stop (5% chance) - human-like behavior
    if random.random() < 0.05 and i > 0:
        stop_delay = _get_human_like_delay(0.2, 'thinking')
        time.sleep(stop_delay)
    
    # ... continue movement ...
```

**Benefits:**
- ✅ Occasional stops giống human
- ✅ Variation trong movement patterns
- ✅ Khó detect hơn

**Risk:** LOW-MEDIUM - Có thể làm bot chậm hơn

**Time:** 1-2 giờ

---

#### **Step 2.2: Add Micro-Adjustments**

**File:** `src/routine/components.py` - `Move` class

**Proposed:**
```python
def main(self):
    # ... existing code ...
    
    # Micro-adjustment (10% chance) - human-like behavior
    if random.random() < 0.10 and i > 0:
        # Small random movement correction
        micro_delay = _get_human_like_delay(0.05, 'fast')
        time.sleep(micro_delay)
        # Optional: small position nudge
    
    # ... continue movement ...
```

**Benefits:**
- ✅ Micro-adjustments giống human
- ✅ Variation trong movement patterns
- ✅ Khó detect hơn

**Risk:** LOW - Chỉ thêm small delays

**Time:** 1-2 giờ

---

#### **Step 2.3: Add Direction Change Variation**

**File:** `src/routine/components.py` - `Move` class

**Proposed:**
```python
def main(self):
    # ... existing code ...
    
    # Variation trong toggle pattern (không luôn toggle)
    if random.random() < 0.15:  # 15% chance to skip toggle
        toggle = not toggle  # Skip one direction
    
    # ... continue movement ...
```

**Benefits:**
- ✅ Variation trong movement patterns
- ✅ Không luôn toggle giữa horizontal/vertical
- ✅ Khó detect hơn

**Risk:** MEDIUM - Có thể làm bot miss target

**Time:** 2-3 giờ

---

### **PHASE 3: Advanced Human Behavior** ⭐ LOW PRIORITY

**Mục tiêu:** Thêm advanced human-like behaviors

#### **Step 3.1: Add Movement Speed Variation**

**File:** `src/routine/components.py` - `Move` class

**Proposed:**
```python
def main(self):
    # ... existing code ...
    
    # Movement speed variation (80-120% of base speed)
    speed_variation = random.uniform(0.8, 1.2)
    adjusted_delay = delay * speed_variation
    time.sleep(adjusted_delay)
```

**Benefits:**
- ✅ Variation trong movement speed
- ✅ Human-like behavior
- ✅ Khó detect hơn

**Risk:** LOW - Chỉ thay đổi timing

**Time:** 1 giờ

---

#### **Step 3.2: Add Occasional Corrections**

**File:** `src/routine/components.py` - `Move` class

**Proposed:**
```python
def main(self):
    # ... existing code ...
    
    # Occasional correction (5% chance) - human-like behavior
    if random.random() < 0.05 and error > settings.move_tolerance * 1.5:
        # Small correction movement
        correction_delay = _get_human_like_delay(0.1, 'normal')
        time.sleep(correction_delay)
```

**Benefits:**
- ✅ Occasional corrections giống human
- ✅ Variation trong movement patterns
- ✅ Khó detect hơn

**Risk:** LOW - Chỉ thêm small corrections

**Time:** 1-2 giờ

---

#### **Step 3.3: Add Fatigue Simulation**

**File:** `src/routine/components.py` - `Move` class

**Proposed:**
```python
def main(self):
    # ... existing code ...
    
    # Fatigue simulation (movement slows down over time)
    fatigue_factor = 1.0 + (counter / self.max_steps) * 0.2  # 0-20% slower
    adjusted_delay = delay * fatigue_factor
    time.sleep(adjusted_delay)
```

**Benefits:**
- ✅ Fatigue simulation giống human
- ✅ Variation trong movement patterns
- ✅ Khó detect hơn

**Risk:** MEDIUM - Có thể làm bot chậm hơn đáng kể

**Time:** 1-2 giờ

---

## 📊 **IMPLEMENTATION PRIORITY**

### **Priority 1: Phase 1 (Timing Randomization)** ⭐⭐⭐

**Why:**
- ✅ High impact (thay thế fixed timing)
- ✅ Low risk (chỉ thay đổi timing)
- ✅ Easy to implement
- ✅ Immediate benefit

**Steps:**
1. Step 1.1: Replace fixed delays trong step function
2. Step 1.2: Replace fixed delays trong Adjust command

**Time:** 2-3 giờ
**Difficulty:** ⭐ Easy

---

### **Priority 2: Phase 2 (Movement Pattern Variation)** ⭐⭐

**Why:**
- ✅ Medium impact (thêm variation)
- ✅ Low-Medium risk (có thể ảnh hưởng performance)
- ✅ Medium difficulty
- ✅ Good benefit

**Steps:**
1. Step 2.1: Add occasional stops
2. Step 2.2: Add micro-adjustments
3. Step 2.3: Add direction change variation

**Time:** 4-7 giờ
**Difficulty:** ⭐⭐ Medium

---

### **Priority 3: Phase 3 (Advanced Human Behavior)** ⭐

**Why:**
- ✅ Low impact (advanced features)
- ✅ Medium risk (có thể ảnh hưởng performance)
- ✅ Medium-Hard difficulty
- ✅ Optional benefit

**Steps:**
1. Step 3.1: Add movement speed variation
2. Step 3.2: Add occasional corrections
3. Step 3.3: Add fatigue simulation (optional)

**Time:** 3-5 giờ
**Difficulty:** ⭐⭐ Medium

---

## ⚠️ **RISK ASSESSMENT**

### **Low Risk:**
- ✅ Phase 1: Timing Randomization (chỉ thay đổi timing)
- ✅ Phase 2.1: Occasional Stops (chỉ thêm delays)
- ✅ Phase 2.2: Micro-Adjustments (chỉ thêm small delays)

### **Medium Risk:**
- ⚠️ Phase 2.3: Direction Change Variation (có thể miss target)
- ⚠️ Phase 3.3: Fatigue Simulation (có thể làm bot chậm)

### **High Risk:**
- ❌ None (tất cả changes đều low-medium risk)

---

## 🎯 **RECOMMENDED APPROACH**

### **Option 1: Conservative (Recommended)** ⭐⭐⭐

**Steps:**
1. ✅ Phase 1: Timing Randomization (Priority 1)
2. ✅ Phase 2.1: Occasional Stops (Priority 2)
3. ✅ Phase 2.2: Micro-Adjustments (Priority 2)
4. ⏳ Phase 2.3: Direction Change Variation (Optional)
5. ⏳ Phase 3: Advanced Features (Optional)

**Result:**
- Risk: LOW
- Time: 4-6 giờ
- Difficulty: ⭐ Easy-Medium
- Benefit: HIGH

---

### **Option 2: Aggressive**

**Steps:**
1. ✅ Phase 1: Timing Randomization
2. ✅ Phase 2: Movement Pattern Variation
3. ✅ Phase 3: Advanced Human Behavior

**Result:**
- Risk: MEDIUM
- Time: 9-15 giờ
- Difficulty: ⭐⭐ Medium-Hard
- Benefit: VERY HIGH

---

## 📝 **TESTING PLAN**

### **Step 1: Unit Testing**
- Test timing randomization functions
- Test movement pattern variations
- Verify không có errors

### **Step 2: Integration Testing**
- Test movement với routine thực tế
- Verify bot vẫn reach targets
- Check performance impact

### **Step 3: Behavior Testing**
- Test human-like behavior
- Verify variation patterns
- Check detection risk

---

## 🚀 **NEXT STEPS**

1. **Review plan** này với team/user
2. **Decide priority** - Phase nào muốn implement
3. **Start with Phase 1** - Quick wins (timing randomization)
4. **Test thoroughly** sau mỗi phase
5. **Evaluate results** trước khi proceed

---

## 📊 **SUMMARY**

### **Current State:**
- ❌ Fixed timing (0.1s, 0.05s)
- ❌ Predictable patterns
- ❌ No human-like behavior

### **Target State:**
- ✅ Random timing variation
- ✅ Movement pattern variation
- ✅ Human-like behavior (stops, adjustments, corrections)

### **Implementation:**
- **Phase 1:** Timing Randomization (2-3h, ⭐ Easy)
- **Phase 2:** Movement Pattern Variation (4-7h, ⭐⭐ Medium)
- **Phase 3:** Advanced Human Behavior (3-5h, ⭐⭐ Medium)

---

**REMEMBER:** Start with Phase 1 (timing randomization) - high impact, low risk, easy to implement! ⭐

