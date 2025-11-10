# 📊 Phase 3: Advanced Human Behavior - Detailed Plan

## 🎯 **MỤC TIÊU**

Thêm advanced human-like behaviors để làm cho movement patterns giống human hơn, bao gồm:
1. Movement Speed Variation
2. Occasional Corrections
3. Path Correction (new)
4. Adaptive Timing (new)
5. Fatigue Simulation (optional)

---

## 📋 **PHASE 3 IMPLEMENTATION PLAN**

### **PHASE 3.1: Movement Speed Variation** ⭐⭐⭐ HIGH PRIORITY

**Mục tiêu:** Thêm variation trong movement speed để simulate human behavior

#### **Step 3.1.1: Add Speed Variation to Delays**

**File:** `src/routine/components.py` - `Move.main()`

**Current:**
```python
if i < len(path) - 1:
    delay = get_human_delay(0.15, 'normal')
    time.sleep(delay)
```

**Proposed:**
```python
if i < len(path) - 1:
    # Phase 3.1: Movement speed variation (80-120% of base speed)
    # Humans don't move at constant speed - they vary based on situation
    speed_variation = random.uniform(0.8, 1.2)  # 80-120% of base speed
    base_delay = get_human_delay(0.15, 'normal')
    adjusted_delay = base_delay * speed_variation
    action_log.debug("Phase 3.1: Speed variation (factor=%.2f, delay=%.3fs)", speed_variation, adjusted_delay)
    time.sleep(adjusted_delay)
```

**Benefits:**
- ✅ Variation trong movement speed (80-120%)
- ✅ Human-like behavior (humans don't move at constant speed)
- ✅ Less predictable patterns

**Risk:** ⭐ **LOW** - Chỉ thay đổi timing, không ảnh hưởng accuracy

**Time:** 1 giờ

**Location:** 2 locations (horizontal và vertical delays)

---

### **PHASE 3.2: Occasional Corrections** ⭐⭐ MEDIUM PRIORITY

**Mục tiêu:** Thêm occasional corrections khi error lớn để simulate human behavior

#### **Step 3.2.1: Add Correction Logic**

**File:** `src/routine/components.py` - `Move.main()`

**Proposed:**
```python
# Phase 3.2: Occasional correction (5% chance when error is large)
# Humans sometimes pause and correct their path when they realize they're off target
if random.random() < 0.05 and global_error > settings.move_tolerance * 1.5:
    correction_delay = get_human_delay(0.1, 'thinking')
    action_log.debug("Phase 3.2: Occasional correction (error=%.3f, delay=%.3fs)", global_error, correction_delay)
    time.sleep(correction_delay)
    # Optional: Small correction movement (nudge towards target)
    # This could be a small step in the correct direction
```

**Benefits:**
- ✅ Occasional corrections giống human behavior
- ✅ Variation trong movement patterns
- ✅ More natural behavior khi error lớn

**Risk:** ⭐ **LOW-MEDIUM** - Có thể làm bot chậm hơn một chút khi error lớn

**Time:** 1-2 giờ

**Location:** Inside movement loop, after error calculation

---

### **PHASE 3.3: Path Correction** ⭐⭐ MEDIUM PRIORITY (NEW)

**Mục tiêu:** Thêm small corrections trong path để simulate human path adjustments

#### **Step 3.3.1: Add Path Correction**

**File:** `src/routine/components.py` - `Move.main()`

**Proposed:**
```python
# Phase 3.3: Path correction (3% chance)
# Humans sometimes make small corrections even when on the right path
# This adds natural variation to movement
if random.random() < 0.03 and i > 0:
    # Small correction delay to simulate "checking" position
    correction_delay = _get_human_like_delay(0.02, 'micro')
    action_log.debug("Phase 3.3: Path correction (delay=%.3fs)", correction_delay)
    time.sleep(correction_delay)
```

**Benefits:**
- ✅ Path corrections giống human behavior
- ✅ Variation trong movement patterns
- ✅ More natural behavior

**Risk:** ⭐ **LOW** - Chỉ thêm small delays (0.006-0.04s)

**Time:** 1 giờ

**Location:** Inside path loop, after first point

---

### **PHASE 3.4: Adaptive Timing** ⭐ LOW PRIORITY (NEW)

**Mục tiêu:** Thêm adaptive timing dựa trên distance và error

#### **Step 3.4.1: Add Adaptive Timing**

**File:** `src/routine/components.py` - `Move.main()`

**Proposed:**
```python
# Phase 3.4: Adaptive timing based on distance and error
# Humans adjust their movement speed based on how far they are from target
# Closer to target = slower, more careful movement
# Farther from target = faster, less careful movement

distance_factor = min(global_error / settings.move_tolerance, 2.0)  # Max 2x
# Closer to target (smaller error) = slower movement (longer delay)
# Farther from target (larger error) = faster movement (shorter delay)
adaptive_multiplier = 1.0 + (1.0 - min(distance_factor / 2.0, 1.0)) * 0.3  # 1.0-1.3x

if i < len(path) - 1:
    base_delay = get_human_delay(0.15, 'normal')
    adaptive_delay = base_delay * adaptive_multiplier
    action_log.debug("Phase 3.4: Adaptive timing (error=%.3f, factor=%.2f, delay=%.3fs)", 
                     global_error, adaptive_multiplier, adaptive_delay)
    time.sleep(adaptive_delay)
```

**Benefits:**
- ✅ Adaptive timing giống human behavior
- ✅ More careful movement khi gần target
- ✅ Faster movement khi xa target

**Risk:** ⭐ **LOW-MEDIUM** - Có thể làm bot chậm hơn khi gần target

**Time:** 1-2 giờ

**Location:** Replace existing delay calculations

---

### **PHASE 3.5: Fatigue Simulation** ⭐ LOW PRIORITY (OPTIONAL)

**Mục tiêu:** Simulate human fatigue over time (movement slows down)

#### **Step 3.5.1: Add Fatigue Simulation**

**File:** `src/routine/components.py` - `Move.main()`

**Proposed:**
```python
# Phase 3.5: Fatigue simulation (movement slows down over time)
# Humans get tired after prolonged movement
# This simulates gradual fatigue during long movements

# Calculate fatigue based on steps remaining (more steps = more fatigue)
fatigue_factor = 1.0 + (counter / self.max_steps) * 0.15  # 0-15% slower
# At start: fatigue_factor = 1.0 (no fatigue)
# At end: fatigue_factor = 1.15 (15% slower)

if i < len(path) - 1:
    base_delay = get_human_delay(0.15, 'normal')
    fatigued_delay = base_delay * fatigue_factor
    action_log.debug("Phase 3.5: Fatigue simulation (steps_remaining=%d, factor=%.2f, delay=%.3fs)", 
                     counter, fatigue_factor, fatigued_delay)
    time.sleep(fatigued_delay)
```

**Benefits:**
- ✅ Fatigue simulation giống human behavior
- ✅ More realistic movement patterns
- ✅ Less predictable patterns

**Risk:** ⭐ **MEDIUM** - Có thể làm bot chậm hơn đáng kể (15% slower)

**Time:** 1-2 giờ

**Location:** Replace existing delay calculations

**Note:** ⚠️ **OPTIONAL** - Có thể disable nếu performance bị ảnh hưởng

---

## 📊 **IMPLEMENTATION PRIORITY**

### **Priority 1: Phase 3.1 (Movement Speed Variation)** ⭐⭐⭐

**Why:**
- ✅ High impact (variation trong speed)
- ✅ Low risk (chỉ thay đổi timing)
- ✅ Easy to implement
- ✅ Immediate benefit

**Steps:**
1. Add speed variation (80-120%) to horizontal delay
2. Add speed variation (80-120%) to vertical delay

**Time:** 1 giờ
**Difficulty:** ⭐ Easy

---

### **Priority 2: Phase 3.2 (Occasional Corrections)** ⭐⭐

**Why:**
- ✅ Medium impact (corrections khi error lớn)
- ✅ Low-Medium risk (có thể làm bot chậm)
- ✅ Medium difficulty
- ✅ Good benefit

**Steps:**
1. Add correction logic khi error > tolerance * 1.5
2. Add correction delay (5% chance)

**Time:** 1-2 giờ
**Difficulty:** ⭐⭐ Medium

---

### **Priority 3: Phase 3.3 (Path Correction)** ⭐⭐

**Why:**
- ✅ Medium impact (path corrections)
- ✅ Low risk (chỉ thêm small delays)
- ✅ Easy to implement
- ✅ Good benefit

**Steps:**
1. Add path correction (3% chance)
2. Add correction delay

**Time:** 1 giờ
**Difficulty:** ⭐ Easy

---

### **Priority 4: Phase 3.4 (Adaptive Timing)** ⭐

**Why:**
- ✅ Low impact (adaptive timing)
- ✅ Low-Medium risk (có thể làm bot chậm)
- ✅ Medium difficulty
- ✅ Optional benefit

**Steps:**
1. Calculate adaptive multiplier based on error
2. Apply adaptive timing to delays

**Time:** 1-2 giờ
**Difficulty:** ⭐⭐ Medium

---

### **Priority 5: Phase 3.5 (Fatigue Simulation)** ⭐

**Why:**
- ✅ Low impact (fatigue simulation)
- ✅ Medium risk (có thể làm bot chậm 15%)
- ✅ Medium difficulty
- ✅ Optional benefit

**Steps:**
1. Calculate fatigue factor based on steps
2. Apply fatigue to delays

**Time:** 1-2 giờ
**Difficulty:** ⭐⭐ Medium

**Note:** ⚠️ **OPTIONAL** - Có thể skip nếu performance bị ảnh hưởng

---

## ⚠️ **RISK ASSESSMENT**

### **Low Risk:**
- ✅ Phase 3.1: Movement Speed Variation (chỉ thay đổi timing)
- ✅ Phase 3.3: Path Correction (chỉ thêm small delays)

### **Medium Risk:**
- ⚠️ Phase 3.2: Occasional Corrections (có thể làm bot chậm)
- ⚠️ Phase 3.4: Adaptive Timing (có thể làm bot chậm khi gần target)
- ⚠️ Phase 3.5: Fatigue Simulation (có thể làm bot chậm 15%)

### **High Risk:**
- ❌ None (tất cả changes đều low-medium risk)

---

## 🎯 **RECOMMENDED APPROACH**

### **Option 1: Conservative (Recommended)** ⭐⭐⭐

**Steps:**
1. ✅ Phase 3.1: Movement Speed Variation (Priority 1)
2. ✅ Phase 3.3: Path Correction (Priority 3)
3. ⏳ Phase 3.2: Occasional Corrections (Optional)
4. ⏳ Phase 3.4: Adaptive Timing (Optional)
5. ⏳ Phase 3.5: Fatigue Simulation (Skip)

**Result:**
- Risk: LOW
- Time: 2-3 giờ
- Difficulty: ⭐ Easy-Medium
- Benefit: HIGH

---

### **Option 2: Moderate**

**Steps:**
1. ✅ Phase 3.1: Movement Speed Variation
2. ✅ Phase 3.2: Occasional Corrections
3. ✅ Phase 3.3: Path Correction
4. ⏳ Phase 3.4: Adaptive Timing (Optional)
5. ⏳ Phase 3.5: Fatigue Simulation (Skip)

**Result:**
- Risk: LOW-MEDIUM
- Time: 3-5 giờ
- Difficulty: ⭐⭐ Medium
- Benefit: VERY HIGH

---

### **Option 3: Aggressive**

**Steps:**
1. ✅ Phase 3.1: Movement Speed Variation
2. ✅ Phase 3.2: Occasional Corrections
3. ✅ Phase 3.3: Path Correction
4. ✅ Phase 3.4: Adaptive Timing
5. ✅ Phase 3.5: Fatigue Simulation

**Result:**
- Risk: MEDIUM
- Time: 5-8 giờ
- Difficulty: ⭐⭐ Medium
- Benefit: VERY HIGH

---

## 📝 **IMPLEMENTATION DETAILS**

### **Phase 3.1: Movement Speed Variation**

**Location:** `src/routine/components.py` - `Move.main()`

**Changes:**
- Add speed variation (80-120%) to horizontal delay (line ~303)
- Add speed variation (80-120%) to vertical delay (line ~327)

**Code:**
```python
# Horizontal delay
if i < len(path) - 1:
    # Phase 3.1: Movement speed variation (80-120% of base speed)
    speed_variation = random.uniform(0.8, 1.2)
    base_delay = get_human_delay(0.15, 'normal')
    adjusted_delay = base_delay * speed_variation
    action_log.debug("Phase 3.1: Speed variation (factor=%.2f, delay=%.3fs)", speed_variation, adjusted_delay)
    time.sleep(adjusted_delay)

# Vertical delay
if i < len(path) - 1:
    # Phase 3.1: Movement speed variation (80-120% of base speed)
    speed_variation = random.uniform(0.8, 1.2)
    base_delay = get_human_delay(0.05, 'fast')
    adjusted_delay = base_delay * speed_variation
    action_log.debug("Phase 3.1: Speed variation (factor=%.2f, delay=%.3fs)", speed_variation, adjusted_delay)
    time.sleep(adjusted_delay)
```

---

### **Phase 3.2: Occasional Corrections**

**Location:** `src/routine/components.py` - `Move.main()`

**Changes:**
- Add correction logic sau error calculation (line ~330)

**Code:**
```python
local_error = utils.distance(config.player_pos, point)
global_error = utils.distance(config.player_pos, self.target)

# Phase 3.2: Occasional correction (5% chance when error is large)
# Humans sometimes pause and correct their path when they realize they're off target
if random.random() < 0.05 and global_error > settings.move_tolerance * 1.5:
    correction_delay = get_human_delay(0.1, 'thinking')
    action_log.debug("Phase 3.2: Occasional correction (error=%.3f, delay=%.3fs)", global_error, correction_delay)
    time.sleep(correction_delay)
```

---

### **Phase 3.3: Path Correction**

**Location:** `src/routine/components.py` - `Move.main()`

**Changes:**
- Add path correction trong path loop (line ~270)

**Code:**
```python
# Phase 3.3: Path correction (3% chance)
# Humans sometimes make small corrections even when on the right path
if random.random() < 0.03 and i > 0:
    correction_delay = _get_human_like_delay(0.02, 'micro')
    action_log.debug("Phase 3.3: Path correction (delay=%.3fs)", correction_delay)
    time.sleep(correction_delay)
```

---

### **Phase 3.4: Adaptive Timing**

**Location:** `src/routine/components.py` - `Move.main()`

**Changes:**
- Replace existing delay calculations với adaptive timing

**Code:**
```python
# Phase 3.4: Adaptive timing based on distance and error
distance_factor = min(global_error / settings.move_tolerance, 2.0)
adaptive_multiplier = 1.0 + (1.0 - min(distance_factor / 2.0, 1.0)) * 0.3  # 1.0-1.3x

if i < len(path) - 1:
    base_delay = get_human_delay(0.15, 'normal')
    adaptive_delay = base_delay * adaptive_multiplier
    action_log.debug("Phase 3.4: Adaptive timing (error=%.3f, factor=%.2f, delay=%.3fs)", 
                     global_error, adaptive_multiplier, adaptive_delay)
    time.sleep(adaptive_delay)
```

---

### **Phase 3.5: Fatigue Simulation**

**Location:** `src/routine/components.py` - `Move.main()`

**Changes:**
- Replace existing delay calculations với fatigue simulation

**Code:**
```python
# Phase 3.5: Fatigue simulation (movement slows down over time)
fatigue_factor = 1.0 + (counter / self.max_steps) * 0.15  # 0-15% slower

if i < len(path) - 1:
    base_delay = get_human_delay(0.15, 'normal')
    fatigued_delay = base_delay * fatigue_factor
    action_log.debug("Phase 3.5: Fatigue simulation (steps_remaining=%d, factor=%.2f, delay=%.3fs)", 
                     counter, fatigue_factor, fatigued_delay)
    time.sleep(fatigued_delay)
```

---

## 🧪 **TESTING PLAN**

### **Step 1: Unit Testing**
- Test speed variation với các factors khác nhau
- Test correction logic với various error values
- Test path correction với various conditions
- Test adaptive timing với various distances
- Test fatigue simulation với various step counts

### **Step 2: Integration Testing**
- Test movement với routine thực tế (`tree_2_floor.csv`)
- Test movement với routine thực tế (`tree_single_floor_left_right.csv`)
- Verify bot vẫn reach targets chính xác
- Check performance impact

### **Step 3: Behavior Testing**
- Verify movement patterns are more human-like
- Check speed variation doesn't cause issues
- Monitor corrections don't cause excessive delays
- Evaluate overall behavior improvement

---

## 📊 **SUMMARY**

### **Current State:**
- ✅ Phase 1: Timing Randomization - COMPLETE
- ✅ Phase 2: Movement Pattern Variation - COMPLETE
- ⏳ Phase 3: Advanced Human Behavior - PENDING

### **Target State:**
- ✅ Movement speed variation (80-120%)
- ✅ Occasional corrections (5% chance)
- ✅ Path correction (3% chance)
- ✅ Adaptive timing (optional)
- ✅ Fatigue simulation (optional)

### **Implementation:**
- **Phase 3.1:** Movement Speed Variation (1h, ⭐ Easy) - **START HERE**
- **Phase 3.2:** Occasional Corrections (1-2h, ⭐⭐ Medium)
- **Phase 3.3:** Path Correction (1h, ⭐ Easy)
- **Phase 3.4:** Adaptive Timing (1-2h, ⭐⭐ Medium) - Optional
- **Phase 3.5:** Fatigue Simulation (1-2h, ⭐⭐ Medium) - Optional

---

## 🚀 **NEXT STEPS**

1. **Review** plan này với user
2. **Decide** which phases to implement (Recommended: 3.1, 3.3)
3. **Start with Phase 3.1** - Quick wins (movement speed variation)
4. **Test thoroughly** sau mỗi phase
5. **Evaluate results** trước khi proceed

---

**REMEMBER:** Start with Phase 3.1 (Movement Speed Variation) - high impact, low risk, easy to implement! ⭐

