# 📊 Phase 1: Timing Randomization Review - `luminous.py`

## 🎯 **MỤC TIÊU**

Thay thế **fixed timing** trong movement-related functions bằng **random timing variation** để làm cho movement giống human hơn.

---

## 📋 **PHÂN TÍCH FIXED TIMING HIỆN TẠI**

### **1. `step()` Function (Line 506-537)** ⭐⭐⭐ **CRITICAL**

**File:** `resources/command_books/luminous.py`

**Current Code:**
```python
def step(direction, target):
    # ... existing code ...
    
    if direction in ('left', 'right'):
        # Short walk for horizontal movement
        try:
            key_down(getattr(Key, direction))
            time.sleep(0.1)  # ❌ FIXED: 100ms
        finally:
            key_up(getattr(Key, direction))
        time.sleep(0.05)  # ❌ FIXED: 50ms
    else:
        # Teleport for vertical movement
        num_presses = 2 if direction in ('up', 'down') else 1
        press(Key.teleport, num_presses)
```

**Issues:**
- ❌ **Fixed timing `0.1s`** cho horizontal walk - không có variation
- ❌ **Fixed timing `0.05s`** cho post-walk pause - không có variation
- ❌ **No micro-pauses** giữa movements - không giống human

**Priority:** ⭐⭐⭐ **HIGH** - Đây là function chính cho movement

---

### **2. `Adjust` Class (Line 440-503)** ⭐⭐ **HIGH PRIORITY**

**File:** `resources/command_books/luminous.py`

**Current Code:**
```python
class Adjust(Command):
    def main(self):
        # ... existing code ...
        
        if toggle:
            # Horizontal adjustment
            if d_x < 0:
                try:
                    key_down('left')
                    while config.enabled and d_x < -1 * threshold and walk_counter < 60:
                        time.sleep(0.05)  # ❌ FIXED: 50ms
                        walk_counter += 1
                        d_x = self.target[0] - config.player_pos[0]
                finally:
                    key_up('left')
            else:
                try:
                    key_down('right')
                    while config.enabled and d_x > threshold and walk_counter < 60:
                        time.sleep(0.05)  # ❌ FIXED: 50ms
                        walk_counter += 1
                        d_x = self.target[0] - config.player_pos[0]
                finally:
                    key_up('right')
        else:
            # Vertical adjustment
            if d_y < 0:
                Teleport('up').main()
            else:
                key_down('down')
                time.sleep(0.05)  # ❌ FIXED: 50ms
                press(Key.jump, 3, down_time=0.1)
                key_up('down')
                time.sleep(0.05)  # ❌ FIXED: 50ms
```

**Issues:**
- ❌ **Fixed timing `0.05s`** trong while loop - không có variation
- ❌ **Fixed timing `0.05s`** cho jump down - không có variation
- ❌ **No micro-pauses** giữa adjustments - không giống human

**Priority:** ⭐⭐ **MEDIUM-HIGH** - Adjust được dùng thường xuyên

---

### **3. Other Fixed Timing (Lower Priority)**

#### **3.1. `Jump` Class (Line 330-343)**
```python
class Jump(Command):
    def main(self):
        for i in range(self.times):
            press(Key.jump, 1, down_time=0.1, up_time=0.1)
            if i < self.times - 1:
                time.sleep(0.1)  # ❌ FIXED: 100ms
```
**Priority:** ⭐ **LOW** - Đã có random trong `press()`, chỉ cần thay delay giữa jumps

#### **3.2. `Buff` Class (Line 418-437)**
```python
class Buff(Command):
    def main(self):
        if self.next_buff_time == 0.0 or now >= self.next_buff_time:
            press(Key.buff_main, 1)
            time.sleep(0.1)  # ❌ FIXED: 100ms
```
**Priority:** ⭐ **LOW** - Không phải movement-related, có thể bỏ qua trong Phase 1

#### **3.3. `Random_Teleport` Class (Line 543-565)**
```python
class Random_Teleport(Command):
    def main(self):
        if utils.bernoulli(self.probability):
            for _ in range(self.count):
                # ... code ...
                time.sleep(0.05)  # ❌ FIXED: 50ms
                # ... code ...
            time.sleep(0.15)  # ❌ FIXED: 150ms
```
**Priority:** ⭐ **LOW** - Đã có random trong logic, chỉ cần thay delay

#### **3.4. Other Commands**
- `Apocalypse`, `Light_Reflection`, `Dark_Reflection`: `time.sleep(0.2)` - **LOW PRIORITY** (skill-related, không phải movement)
- `Random_Attack`, `Conditional_Action`: `time.sleep(0.1)` - **LOW PRIORITY** (attack-related, không phải movement)

---

## ✅ **ĐỀ XUẤT THAY ĐỔI**

### **Step 1.1: Replace Fixed Delays trong `step()` Function** ⭐⭐⭐

**File:** `resources/command_books/luminous.py`

**Proposed Code:**
```python
def step(direction, target):
    """
    Performs one movement step in the given DIRECTION towards TARGET.
    Should not press any arrow keys, as those are handled by Auto Maple.
    Based on Kanna's intelligent step() with Luminous improvements.
    """

    # Anti-detect delay (from Kanna)
    if config.stage_fright and direction != 'up' and utils.bernoulli(0.75):
        time.sleep(utils.rand_float(0.1, 0.3))

    # Check Y distance for vertical movements (from Kanna - SMART!)
    d_y = target[1] - config.player_pos[1]
    if abs(d_y) > settings.move_tolerance * 1.5:
        if direction == 'down':
            press(Key.jump, 3)
        elif direction == 'up':
            press(Key.jump, 1)

    # Handle different directions (hybrid approach)
    if direction in ('left', 'right'):
        # Short walk for horizontal movement (from Luminous)
        try:
            key_down(getattr(Key, direction))
            # ✅ RANDOM: Use human-like delay instead of fixed 0.1s
            from src.common.vkeys import _get_human_like_delay, _get_micro_pause
            walk_delay = _get_human_like_delay(0.1, 'down')  # Random: ~0.08-0.15s
            time.sleep(walk_delay)
        finally:
            key_up(getattr(Key, direction))
        # ✅ RANDOM: Use human-like delay + micro-pause instead of fixed 0.05s
        post_walk_delay = _get_human_like_delay(0.05, 'up')  # Random: ~0.03-0.08s
        micro_pause = _get_micro_pause()  # Random: 0.001-0.025s
        time.sleep(post_walk_delay + micro_pause)
    else:
        # Teleport for vertical movement (from Kanna)
        num_presses = 2 if direction in ('up', 'down') else 1
        press(Key.teleport, num_presses)
```

**Changes:**
1. ✅ Import `_get_human_like_delay` và `_get_micro_pause` từ `src.common.vkeys`
2. ✅ Thay `time.sleep(0.1)` → `_get_human_like_delay(0.1, 'down')`
3. ✅ Thay `time.sleep(0.05)` → `_get_human_like_delay(0.05, 'up') + _get_micro_pause()`

**Benefits:**
- ✅ Random timing variation (0.08-0.15s cho walk, 0.03-0.08s + 0.001-0.025s cho post-walk)
- ✅ Micro-pauses giữa movements (human-like behavior)
- ✅ Gaussian distribution (tự nhiên hơn uniform random)

**Risk:** ⭐ **LOW** - Chỉ thay đổi timing, không thay đổi logic

---

### **Step 1.2: Replace Fixed Delays trong `Adjust` Class** ⭐⭐

**File:** `resources/command_books/luminous.py`

**Proposed Code:**
```python
class Adjust(Command):
    """Fine-tunes player position using small movements."""
    
    def main(self):
        # ✅ Import timing functions
        from src.common.vkeys import _get_human_like_delay, _get_micro_pause
        
        counter = self.max_steps
        toggle = True
        error = utils.distance(config.player_pos, self.target)
        while config.enabled and counter > 0 and error > settings.adjust_tolerance:
            if toggle:
                d_x = self.target[0] - config.player_pos[0]
                threshold = settings.adjust_tolerance / math.sqrt(2)
                if abs(d_x) > threshold:
                    walk_counter = 0
                    if d_x < 0:
                        try:
                            key_down('left')
                            while config.enabled and d_x < -1 * threshold and walk_counter < 60:
                                # ✅ RANDOM: Use human-like delay instead of fixed 0.05s
                                walk_delay = _get_human_like_delay(0.05, 'fast')  # Random: ~0.03-0.08s
                                time.sleep(walk_delay)
                                walk_counter += 1
                                d_x = self.target[0] - config.player_pos[0]
                        finally:
                            key_up('left')
                    else:
                        try:
                            key_down('right')
                            while config.enabled and d_x > threshold and walk_counter < 60:
                                # ✅ RANDOM: Use human-like delay instead of fixed 0.05s
                                walk_delay = _get_human_like_delay(0.05, 'fast')  # Random: ~0.03-0.08s
                                time.sleep(walk_delay)
                                walk_counter += 1
                                d_x = self.target[0] - config.player_pos[0]
                        finally:
                            key_up('right')
                    counter -= 1
            else:
                d_y = self.target[1] - config.player_pos[1]
                if abs(d_y) > settings.adjust_tolerance / math.sqrt(2):
                    if d_y < 0:
                        # Use Luminous teleport up
                        Teleport('up').main()
                    else:
                        # Use Luminous jump down
                        key_down('down')
                        # ✅ RANDOM: Use human-like delay instead of fixed 0.05s
                        down_delay = _get_human_like_delay(0.05, 'fast')  # Random: ~0.03-0.08s
                        time.sleep(down_delay)
                        press(Key.jump, 3, down_time=0.1)
                        key_up('down')
                        # ✅ RANDOM: Use human-like delay + micro-pause instead of fixed 0.05s
                        post_jump_delay = _get_human_like_delay(0.05, 'up')  # Random: ~0.03-0.08s
                        micro_pause = _get_micro_pause()  # Random: 0.001-0.025s
                        time.sleep(post_jump_delay + micro_pause)
                    counter -= 1
            error = utils.distance(config.player_pos, self.target)
            toggle = not toggle

        # Safety: ensure all movement keys are released
        key_up('left')
        key_up('right')
        key_up('up')
        key_up('down')
```

**Changes:**
1. ✅ Import `_get_human_like_delay` và `_get_micro_pause` từ `src.common.vkeys`
2. ✅ Thay `time.sleep(0.05)` trong while loop → `_get_human_like_delay(0.05, 'fast')`
3. ✅ Thay `time.sleep(0.05)` cho jump down → `_get_human_like_delay(0.05, 'fast')`
4. ✅ Thay `time.sleep(0.05)` sau jump → `_get_human_like_delay(0.05, 'up') + _get_micro_pause()`

**Benefits:**
- ✅ Random timing variation trong adjustment loops
- ✅ Micro-pauses sau jumps (human-like behavior)
- ✅ Gaussian distribution (tự nhiên hơn)

**Risk:** ⭐ **LOW** - Chỉ thay đổi timing, không thay đổi logic

---

## 📊 **TÓM TẮT THAY ĐỔI**

### **Files to Modify:**
1. ✅ `resources/command_books/luminous.py`
   - `step()` function (Line 506-537)
   - `Adjust` class (Line 440-503)

### **Total Changes:**
- **5 fixed timing locations** trong `step()` function
- **4 fixed timing locations** trong `Adjust` class
- **Total: 9 fixed timing locations** cần thay đổi

### **Import Statements:**
```python
from src.common.vkeys import _get_human_like_delay, _get_micro_pause
```

---

## ⚠️ **RISK ASSESSMENT**

### **Low Risk:**
- ✅ Chỉ thay đổi timing, không thay đổi logic
- ✅ Gaussian distribution tự nhiên hơn fixed timing
- ✅ Micro-pauses không ảnh hưởng đáng kể đến performance

### **Potential Issues:**
- ⚠️ **Performance:** Random delays có thể làm bot chậm hơn một chút (0.001-0.025s per movement)
- ⚠️ **Testing:** Cần test kỹ để đảm bảo movement vẫn chính xác

### **Mitigation:**
- ✅ Sử dụng `'fast'` delay type cho adjustments (ít variance hơn)
- ✅ Giữ nguyên bounds (min 0.03s, max 0.08s) để đảm bảo reliability
- ✅ Test thoroughly với routine thực tế

---

## 🧪 **TESTING PLAN**

### **Step 1: Unit Testing**
- Test `_get_human_like_delay()` với các delay types khác nhau
- Verify random delays trong expected ranges
- Check không có errors

### **Step 2: Integration Testing**
- Test `step()` function với các directions khác nhau
- Test `Adjust` class với các positions khác nhau
- Verify bot vẫn reach targets chính xác

### **Step 3: Behavior Testing**
- Test movement với routine thực tế (`tree_2_floor.csv`, `tree_single_floor_left_right.csv`)
- Verify timing variation không làm bot miss targets
- Check performance impact (nếu có)

---

## 📝 **IMPLEMENTATION CHECKLIST**

### **Step 1.1: `step()` Function**
- [ ] Import `_get_human_like_delay` và `_get_micro_pause`
- [ ] Thay `time.sleep(0.1)` → `_get_human_like_delay(0.1, 'down')`
- [ ] Thay `time.sleep(0.05)` → `_get_human_like_delay(0.05, 'up') + _get_micro_pause()`
- [ ] Test với horizontal movement (left/right)
- [ ] Test với vertical movement (up/down)

### **Step 1.2: `Adjust` Class**
- [ ] Import `_get_human_like_delay` và `_get_micro_pause`
- [ ] Thay `time.sleep(0.05)` trong while loop (left) → `_get_human_like_delay(0.05, 'fast')`
- [ ] Thay `time.sleep(0.05)` trong while loop (right) → `_get_human_like_delay(0.05, 'fast')`
- [ ] Thay `time.sleep(0.05)` cho jump down → `_get_human_like_delay(0.05, 'fast')`
- [ ] Thay `time.sleep(0.05)` sau jump → `_get_human_like_delay(0.05, 'up') + _get_micro_pause()`
- [ ] Test với horizontal adjustment
- [ ] Test với vertical adjustment

---

## 🎯 **EXPECTED RESULTS**

### **Before (Fixed Timing):**
- ❌ `step()`: Fixed `0.1s` walk, fixed `0.05s` pause
- ❌ `Adjust`: Fixed `0.05s` trong loops, fixed `0.05s` sau jumps
- ❌ Predictable patterns, dễ detect

### **After (Random Timing):**
- ✅ `step()`: Random `0.08-0.15s` walk, random `0.03-0.08s + 0.001-0.025s` pause
- ✅ `Adjust`: Random `0.03-0.08s` trong loops, random `0.03-0.08s + 0.001-0.025s` sau jumps
- ✅ Human-like patterns, khó detect hơn

---

## 🚀 **NEXT STEPS**

1. **Review** plan này với user
2. **Implement** Step 1.1 (`step()` function)
3. **Test** Step 1.1 với routine thực tế
4. **Implement** Step 1.2 (`Adjust` class)
5. **Test** Step 1.2 với routine thực tế
6. **Evaluate** results và proceed to Phase 2 (nếu cần)

---

## 📊 **SUMMARY**

### **Current State:**
- ❌ 9 fixed timing locations trong movement-related functions
- ❌ Predictable patterns, dễ detect

### **Target State:**
- ✅ Random timing variation với Gaussian distribution
- ✅ Micro-pauses giữa movements
- ✅ Human-like behavior, khó detect hơn

### **Implementation:**
- **Step 1.1:** `step()` function (5 locations)
- **Step 1.2:** `Adjust` class (4 locations)
- **Total Time:** 2-3 giờ
- **Difficulty:** ⭐ Easy
- **Risk:** ⭐ LOW

---

**REMEMBER:** Start with Step 1.1 (`step()` function) - đây là function chính cho movement! ⭐

