# Plan: Random Backward Feature

## 🎯 Mục Tiêu

Thêm tính năng **Random Backward** để tăng mức độ random pattern:
- Bot đang ở `f2_pos_1`, có thể backward về `f1_pos_last - 3` (backward về floor trước, 3 steps từ cuối)
- Backward dựa vào setting range min/max (ví dụ: 2-4 points)
- Backward về **floor trước** (f2 -> f1, f1 -> f2 nếu có)
- **Sau khi backward, bot tiếp tục chạy như bình thường** (không skip các index đã backward)
- **Backward áp dụng cho tất cả variants**: normal, reverse, floor-only
- Khi backward vẫn sẽ thực hiện các command trong routine
- Sự kiện random backward này có 10% xảy ra

### Ví Dụ Cụ Thể:

**Normal Variant:**
- Bot đang ở `f2_pos_1` (index 10), backward về `f1_pos_5` (index 5)
- Sau backward: Bot execute commands tại `f1_pos_5`
- Tiếp theo: Bot tiếp tục forward `f1_pos_5 -> f1_pos_6 -> ... -> f2_pos_1 -> ...` (theo normal flow)

**Reverse Variant:**
- Bot đang ở `f1_pos_3` (index 3), backward về `f2_pos_last - 2` (index 12)
- Sau backward: Bot execute commands tại index 12
- Tiếp theo: Bot tiếp tục reverse `index 12 -> 11 -> 10 -> ...` (theo reverse flow)

**Floor-Only Variant:**
- Bot đang ở `f1_pos_6` (forward direction), backward về `f2_pos_last - 3`
- Sau backward: Bot execute commands tại backwarded index
- Tiếp theo: Bot tiếp tục floor-only flow từ backwarded index

---

## ✅ Đánh Giá Tính Khả Thi

### Khả Thi: **CAO** ⭐⭐⭐⭐⭐

**Lý do:**
1. ✅ **Có sẵn infrastructure**: Đã có reverse variant logic, floor detection
2. ✅ **Dễ implement**: Chỉ cần thêm logic check backward chance và set index
3. ✅ **Tương thích**: Không conflict với các tính năng hiện có
4. ✅ **Low risk**: Có thể enable/disable dễ dàng

### Lợi Ích:
- ✅ **Tăng variation**: Tạo pattern không dự đoán được
- ✅ **Human-like**: Humans đôi khi quay lại để check hoặc adjust
- ✅ **Anti-detection**: Khó detect với backward movements
- ✅ **Flexible**: Có thể config chance và range

### Thách Thức:
- ⚠️ **Edge cases**: Cần xử lý khi đang ở pos_0, pos_1 (không đủ points để backward)
- ⚠️ **Floor detection**: Cần backward về floor trước (f2 -> f1, f1 -> f2)
- ⚠️ **Variant compatibility**: Cần hoạt động với tất cả variants (normal, reverse, floor-only)
- ⚠️ **Flow continuation**: Sau backward, bot phải tiếp tục flow theo variant hiện tại (không skip points)
- ⚠️ **Loop detection**: Cần đảm bảo backward không làm loop detection sai

---

## 📋 Implementation Plan

### Phase 1: Configuration & Setup

**File:** `src/routine/routine.py` - `Routine.__init__()`

```python
# Random Backward
self.backward_enabled = True  # Enable/disable backward feature
self.backward_chance = 0.10  # 10% chance to backward
self.backward_range_min = 2  # Minimum backward steps
self.backward_range_max = 4  # Maximum backward steps
self.backward_floor_only = True  # Only backward within same floor
```

**Settings:**
- `backward_enabled`: Boolean (enable/disable)
- `backward_chance`: Float 0.0-1.0 (probability)
- `backward_range_min`: Integer (min steps to backward)
- `backward_range_max`: Integer (max steps to backward)
- `backward_to_previous_floor`: Boolean (backward về floor trước, default: True)

---

### Phase 2: Backward Detection Logic

**File:** `src/routine/routine.py` - Thêm method `_should_backward()`

**Quan trọng:** Backward check áp dụng cho tất cả variants (normal, reverse, floor-only).

```python
def _should_backward(self):
    """
    Check if we should perform random backward.
    Áp dụng cho tất cả variants: normal, reverse, floor-only.
    
    Returns: (should_backward: bool, backward_steps: int)
    """
    if not self.backward_enabled:
        return False, 0
    
    # Check probability
    roll = random.random()
    if roll >= self.backward_chance:
        log.debug("🔄 Random Backward: Skipped (chance: %.0f%%, roll: %.3f, variant: '%s')", 
                 self.backward_chance * 100, roll, self.current_variant)
        return False, 0
    
    # Calculate backward steps
    backward_steps = random.randint(self.backward_range_min, self.backward_range_max)
    
    # Note: Không cần check "enough points behind" vì backward về floor trước
    # _get_backward_index() sẽ xử lý edge cases
    
    log.debug("🔄 Random Backward: Triggered (chance: %.0f%%, roll: %.3f, steps: %d, variant: '%s')", 
             self.backward_chance * 100, roll, backward_steps, self.current_variant)
    
    return True, backward_steps
```

---

### Phase 3: Backward to Previous Floor

**File:** `src/routine/routine.py` - Thêm method `_get_backward_index()`

**Quan trọng:** Method này hoạt động với tất cả variants (normal, reverse, floor-only). Backward về floor trước, sau đó bot tiếp tục flow theo variant hiện tại.

```python
def _get_backward_index(self, current_index, backward_steps):
    """
    Get backward index, backwarding to previous floor.
    
    Logic:
    - f2_pos_1 -> f1_pos_last - backward_steps (ví dụ: f1_pos_8 - 3 = f1_pos_5)
    - f1_pos_X -> f2_pos_last - backward_steps (nếu có f2)
    - Nếu không có floor trước, backward trong cùng floor
    - Hoạt động với tất cả variants: normal, reverse, floor-only
    
    Args:
        current_index: Current index
        backward_steps: Number of steps to backward
    
    Returns:
        Backward index, or current_index if cannot backward
    """
    if not self.backward_to_previous_floor:
        # Simple backward: just subtract steps
        backward_index = current_index - backward_steps
        if backward_index < 0:
            backward_index = 0
        return backward_index
    
    # Find which floor current_index belongs to
    current_floor = None
    previous_floor_indices = None
    
    if current_index in self.floor1_indices:
        current_floor = 'floor1'
        previous_floor_indices = self.floor2_indices  # f1 -> f2 (previous in sequence)
    elif current_index in self.floor2_indices:
        current_floor = 'floor2'
        previous_floor_indices = self.floor1_indices  # f2 -> f1 (previous in sequence)
    else:
        # Not in any floor, use simple backward
        backward_index = current_index - backward_steps
        if backward_index < 0:
            backward_index = 0
        log.debug("🔄 Random Backward: Index %d not in any floor, using simple backward to %d", 
                 current_index, backward_index)
        return backward_index
    
    # Check if previous floor exists
    if not previous_floor_indices or len(previous_floor_indices) == 0:
        # No previous floor, backward within same floor
        current_floor_indices = self.floor1_indices if current_floor == 'floor1' else self.floor2_indices
        try:
            current_floor_index = current_floor_indices.index(current_index)
            backward_floor_index = current_floor_index - backward_steps
            if backward_floor_index < 0:
                backward_floor_index = 0
            backward_index = current_floor_indices[backward_floor_index]
            log.info("🔄 Random Backward: No previous floor, backwarding within %s: Index %d -> %d (variant: '%s')", 
                    current_floor, current_index, backward_index, self.current_variant)
            return backward_index
        except ValueError:
            return current_index
    
    # Backward to previous floor: last position - backward_steps
    # Example: f2_pos_1 -> f1_pos_last - 3
    # If f1 has 9 points (pos_0 to pos_8), last index in list is 8, backward 3 -> index 5 (f1_pos_5)
    
    last_previous_floor_index = previous_floor_indices[-1]
    last_previous_floor_pos_in_list = len(previous_floor_indices) - 1  # Last position index in floor_indices list (0-based)
    
    # Calculate target position: last - backward_steps
    # Example: last index = 8, backward 3 -> index 5
    target_floor_pos_in_list = last_previous_floor_pos_in_list - backward_steps
    
    if target_floor_pos_in_list < 0:
        # Cannot backward enough steps, go to first position in previous floor
        target_floor_pos_in_list = 0
        log.debug("🔄 Random Backward: Cannot backward %d steps in previous floor, going to first position", 
                 backward_steps)
    
    backward_index = previous_floor_indices[target_floor_pos_in_list]
    
    previous_floor_name = 'floor1' if current_floor == 'floor2' else 'floor2'
    log.info("🔄 Random Backward: %s Index %d -> %s Index %d (pos_%d of %d, backward %d steps from last, variant: '%s')", 
            current_floor, current_index, previous_floor_name, backward_index, 
            target_floor_pos_in_list, len(previous_floor_indices), backward_steps, self.current_variant)
    
    return backward_index
```

---

### Phase 4: Integration với step()

**File:** `src/routine/routine.py` - Modify `step()`

**Quan trọng:** Backward check **SAU KHI** execute point hiện tại, **TRƯỚC KHI** get next index. Sau backward, bot tiếp tục flow bình thường từ backwarded index.

```python
@utils.run_if_enabled
def step(self):
    """Increments config.seq_index and wraps back to 0 at the end of config.sequence."""
    if len(self.sequence) == 0:
        return
    
    # Save current index before stepping
    old_index = self.index
    
    # Check if we should switch variant (before stepping)
    if self._should_switch_variant():
        self._switch_variant()
        self.index = self._get_variant_start_index()
        self.last_index = -1
        log.info("🔄 Routine Pattern Variation: Reset to start index %d (variant: '%s')", 
                 self.index, self.current_variant)
        return
    
    # Check for random backward BEFORE getting next index
    # Backward áp dụng cho tất cả variants (normal, reverse, floor-only)
    should_backward, backward_steps = self._should_backward()
    if should_backward:
        backward_index = self._get_backward_index(self.index, backward_steps)
        if backward_index != self.index:
            # Perform backward
            log.info("🔄 Random Backward: Backwarding from index %d to %d (%d steps, variant: '%s', chance: %.0f%%)", 
                    self.index, backward_index, backward_steps, self.current_variant,
                    self.backward_chance * 100)
            self.index = backward_index
            # Bot sẽ execute commands tại backwarded index trong lần step() tiếp theo
            # Sau đó tiếp tục flow bình thường từ backwarded index
        else:
            log.debug("🔄 Random Backward: Cannot backward (staying at index %d)", self.index)
    
    # Step based on current variant (sau khi backward, nếu có)
    old_idx_before_step = self.index
    self.index = self._get_variant_next_index(self.index)
    
    # Log step for floor-only variants
    if self.current_variant in ['floor1_only', 'floor2_only']:
        log.info("🛗 Floor-only STEP: Variant '%s', Index %d -> %d, Direction: %s", 
                self.current_variant, old_idx_before_step, self.index, self.floor_direction)
    
    # Detect loop completion (after stepping)
    # ... (existing loop detection logic)
    
    # Update last_index for next iteration
    self.last_index = old_index
```

**Flow sau backward:**
1. Bot đang ở `f2_pos_1` (index 10)
2. Backward về `f1_pos_5` (index 5)
3. Bot execute commands tại `f1_pos_5` (trong lần step() tiếp theo)
4. Sau đó, bot tiếp tục flow theo variant:
   - **Normal**: `f1_pos_5 -> f1_pos_6 -> ... -> f2_pos_1 -> ...`
   - **Reverse**: `f1_pos_5 -> f1_pos_4 -> ...` (nếu đang reverse)
   - **Floor-only**: Tiếp tục floor-only flow từ `f1_pos_5`

**Lưu ý:**
- Backward chỉ thay đổi `self.index`, không thay đổi variant flow
- Sau backward, `_get_variant_next_index()` sẽ tính next index dựa trên variant hiện tại
- Không skip các points đã backward qua - bot sẽ visit lại các points đó theo variant flow

---

### Phase 5: Command Execution

**File:** `src/routine/components.py` - `Point.main()`

**Không cần thay đổi!** Vì:
- `Point.main()` đã execute commands dựa trên `self.location`
- Khi backward, `self.index` thay đổi, nhưng `Point.main()` vẫn execute commands tại point đó
- Commands sẽ được execute như bình thường

**Lưu ý:**
- Commands tại backwarded point sẽ được execute đầy đủ
- Nếu routine có `teleport,right` commands, chúng sẽ được execute (trừ khi đang trong reverse variant)
- **Không cần skip teleport khi backward** vì backward chỉ là thay đổi index, không phải reverse variant
- Bot sẽ visit lại các points đã backward qua theo variant flow bình thường

---

### Phase 6: Logging

**Thêm logs chi tiết:**

```python
# In _should_backward()
log.info("🔄 Random Backward: Triggered (chance: %.0f%%, roll: %.3f, steps: %d)", 
         self.backward_chance * 100, roll, backward_steps)

# In _get_backward_index()
log.info("🔄 Random Backward: %s - Index %d -> Index %d (backward %d steps)", 
         current_floor, current_index, backward_index, backward_steps)

# In step()
log.info("🔄 Random Backward: Backwarding from index %d to %d (%d steps)", 
         self.index, backward_index, backward_steps)
```

---

### Phase 7: GUI Settings (Optional)

**File:** `src/gui/settings/routine_randomization.py`

Thêm panel cho Random Backward:
- Checkbox: Enable Random Backward
- Slider: Backward Chance (0-100%)
- Spinbox: Backward Range Min (1-10)
- Spinbox: Backward Range Max (1-10)
- Checkbox: Floor-Only Backward

---

## 🧪 Testing Strategy

### Unit Tests:
- [ ] Test `_should_backward()` với different probabilities
- [ ] Test `_get_backward_index()` với different floors
- [ ] Test edge cases (index 0, index 1, not enough points)
- [ ] Test floor-aware backward

### Integration Tests:
- [ ] Test với normal variant
- [ ] Test với reverse variant
- [ ] Test với floor-only variants
- [ ] Test với Point Selection Randomization enabled
- [ ] Test với different backward ranges

### Real-world Tests:
- [ ] Test với routine có nhiều points
- [ ] Test với 1-floor và 2-floor routines
- [ ] Verify commands được execute đúng khi backward
- [ ] Verify loop detection không bị ảnh hưởng

---

## ⚠️ Edge Cases & Considerations

### 1. Not Enough Points to Backward in Previous Floor
**Scenario:** Bot ở `f2_pos_0`, backward 5 steps, nhưng f1 chỉ có 3 points
**Solution:** Backward về `f1_pos_0` (first position in previous floor)

### 2. No Previous Floor
**Scenario:** Bot ở `f1_pos_X`, nhưng không có f2 (1-floor routine)
**Solution:** Backward trong cùng floor (f1_pos_X -> f1_pos_X - backward_steps)

### 3. Backward at Start of Floor
**Scenario:** Bot ở `f1_pos_0`, backward về f2, nhưng f2 không tồn tại
**Solution:** Backward trong cùng floor hoặc skip backward

### 4. Backward với Reverse Variant
**Scenario:** Bot đang ở `f1_pos_3` trong reverse variant, backward về `f2_pos_last - 2`
**Solution:** 
- Backward về `f2_pos_last - 2`
- Execute commands tại backwarded point
- Tiếp tục reverse flow: `f2_pos_last - 2 -> f2_pos_last - 3 -> ...` (backward direction)

### 5. Backward với Floor-Only Variant
**Scenario:** Bot đang ở `f1_pos_6` (forward direction), backward về `f2_pos_last - 3`
**Solution:**
- Backward về `f2_pos_last - 3`
- Execute commands tại backwarded point
- Tiếp tục floor-only flow từ backwarded point (có thể cần reset `floor_direction` nếu cần)

### 6. Loop Detection
**Scenario:** Backward có thể làm loop detection sai?
**Solution:** **Không**, vì backward chỉ thay đổi index, không thay đổi variant flow. Loop detection dựa trên variant flow (normal/reverse/floor-only), không phụ thuộc vào backward.

### 7. Commands Execution
**Scenario:** Khi backward về `f1_pos_5`, có `teleport,right` command
**Solution:** Execute như bình thường. Commands sẽ được execute đầy đủ tại backwarded point.

### 8. Flow Continuation
**Scenario:** Sau backward, bot có skip các points đã backward qua không?
**Solution:** **Không**, bot sẽ tiếp tục flow bình thường từ backwarded index. Ví dụ: backward về `f1_pos_5`, bot sẽ tiếp tục `f1_pos_5 -> f1_pos_6 -> ...` theo variant flow.

---

## 📊 Expected Results

### Benefits:
- ✅ **Variation**: Tăng variation trong movement pattern
- ✅ **Human-like**: Humans đôi khi quay lại
- ✅ **Anti-detection**: Khó detect với backward movements
- ✅ **Flexible**: Có thể config chance và range

### Trade-offs:
- ⚠️ **Performance**: Thêm một số checks (minimal overhead)
- ⚠️ **Complexity**: Code phức tạp hơn một chút
- ⚠️ **Testing**: Cần test kỹ với different scenarios

---

## 🎯 Implementation Priority

**Priority:** Medium-High ⭐⭐⭐⭐

**Reasons:**
- Tăng variation đáng kể
- Khả thi cao
- Low risk
- Có thể implement nhanh

**Estimated Time:** 2-3 hours

**Dependencies:**
- Floor detection (đã có)
- Reverse variant logic (đã có)

---

## 📝 Implementation Checklist

### Phase 1: Configuration (30 min)
- [ ] Add backward config to `Routine.__init__()`
- [ ] Add backward settings keys
- [ ] Test config loading

### Phase 2: Backward Detection (30 min)
- [ ] Implement `_should_backward()`
- [ ] Test với different probabilities
- [ ] Test edge cases

### Phase 3: Floor-Aware Backward (1 hour)
- [ ] Implement `_get_backward_index()`
- [ ] Test với different floors
- [ ] Test edge cases

### Phase 4: Integration (30 min)
- [ ] Modify `step()` to check backward
- [ ] Test với different variants
- [ ] Verify commands execution

### Phase 5: Logging (15 min)
- [ ] Add detailed logs
- [ ] Test log output

### Phase 6: Testing (1 hour)
- [ ] Unit tests
- [ ] Integration tests
- [ ] Real-world testing

---

## 🔄 Alternative Approaches

### Approach 1: Simple Backward (Không floor-aware)
- Đơn giản hơn
- Nhưng có thể backward across floors
- **Không khuyến nghị** nếu muốn backward trong cùng floor

### Approach 2: Backward với Skip Commands
- Skip teleport commands khi backward
- **Không cần thiết** vì backward không phải reverse variant

### Approach 3: Backward với Probability per Point
- Mỗi point có probability riêng
- **Phức tạp hơn**, không cần thiết

---

## ✅ Kết Luận

**Random Backward là tính năng khả thi và có giá trị cao:**
- ✅ Khả thi: CAO
- ✅ Lợi ích: Tăng variation, human-like, anti-detection
- ✅ Risk: LOW
- ✅ Implementation: 2-3 hours
- ✅ Tương thích: Không conflict với tính năng hiện có

**Khuyến nghị:** Implement theo plan trên, bắt đầu với Phase 1-4, test kỹ, sau đó thêm GUI settings nếu cần.

