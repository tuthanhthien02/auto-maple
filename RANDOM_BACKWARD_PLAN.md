# Plan: Random Move Backward Feature

## 1. Overview
Tính năng Random Move Backward cho phép bot di chuyển backward một số index (2-3) một cách ngẫu nhiên để tạo pattern random, tăng tính tự nhiên của bot.

## 2. Requirements
- **Range**: Backward 2-3 indices (random trong range này)
- **Enable/Disable**: Có thể bật/tắt giống Point Selection Randomization
- **Optional**: Không ảnh hưởng đến luồng chính của bot
- **Tương thích**: Có thể kết hợp với Point Selection Randomization và Floor-only
- **Timing**: Sự kiện backward xuất hiện TRƯỚC khi bot thực hiện bất kì command nào
- **Logic**: Khi backward xảy ra, `self.index` di chuyển backward 2-3 steps

## 3. Implementation Plan

### 3.1. Routine Class (`src/routine/routine.py`)

#### 3.1.1. Add Attributes
```python
# Random Move Backward
self.backward_enabled = False  # Enable/disable backward feature
self.backward_probability = 0.10  # 10% chance to backward (default)
self.backward_range = (2, 3)  # Backward 2-3 indices (hardcode)
self.backward_cooldown = 0  # Cooldown counter to prevent consecutive backward
self.backward_cooldown_min = 5  # Min cooldown (5 points)
self.backward_cooldown_max = 10  # Max cooldown (10 points)
```

#### 3.1.2. Add Method: `should_backward()`
```python
def should_backward(self):
    """
    Check if we should backward at current index.
    Returns: (should_backward: bool, backward_steps: int)
    """
    # Check if enabled
    if not self.backward_enabled:
        return False, 0
    
    # Check cooldown
    if self.backward_cooldown > 0:
        self.backward_cooldown -= 1
        return False, 0
    
    # Check if we can backward (need at least backward_range[1] indices before current)
    min_steps = self.backward_range[1]  # Max backward steps (3)
    if self.index < min_steps:
        # Not enough indices to backward
        return False, 0
    
    # Random probability check
    random_value = random.random()
    if random_value < self.backward_probability:
        # Backward event triggered
        backward_steps = random.randint(self.backward_range[0], self.backward_range[1])
        # Set cooldown
        self.backward_cooldown = random.randint(self.backward_cooldown_min, self.backward_cooldown_max)
        log.info("⏮️ Random Backward: Triggered at index %d, backwarding %d steps (cooldown: %d)", 
                self.index, backward_steps, self.backward_cooldown)
        return True, backward_steps
    else:
        return False, 0
```

#### 3.1.3. Add Method: `apply_backward(backward_steps)`
```python
def apply_backward(self, backward_steps):
    """
    Apply backward movement to current index.
    Args:
        backward_steps: Number of steps to backward (2-3)
    """
    if len(self.sequence) == 0:
        return
    
    old_index = self.index
    # Backward: move index backward
    self.index = (self.index - backward_steps) % len(self.sequence)
    
    log.info("⏮️ Random Backward: Index %d -> %d (backwarded %d steps)", 
            old_index, self.index, backward_steps)
    
    # Reset skip context (backward is a new movement, not skip)
    self.is_skipping_context = False
    # Reset consecutive skips (backward is a new pattern, reset skip counter)
    self.consecutive_skips = 0
```

#### 3.1.4. Update `_load_randomization_settings()`
- Load `backward_enabled` và `backward_probability` từ GUI settings

#### 3.1.5. Update `load()` method
- Reset backward cooldown khi load routine mới

### 3.2. Bot Module (`src/modules/bot.py`)

#### 3.2.1. Update `_main()` method
Thêm backward check TRƯỚC skip check:

```python
# Random Move Backward: Check if we should backward BEFORE any command execution
should_backward, backward_steps = config.routine.should_backward()
if should_backward:
    # Apply backward movement
    config.routine.apply_backward(backward_steps)
    # Get new element after backward
    element = config.routine[config.routine.index]
    element_type = element.__class__.__name__
    log.info("⏮️ Random Backward: Now at index %d, element type: %s", 
            config.routine.index, element_type)

# Point Selection Randomization: Check if we should skip BEFORE executing
element = config.routine[config.routine.index]
element_type = element.__class__.__name__
...
```

### 3.3. GUI Settings (`src/gui/settings/routine_randomization.py`)

#### 3.3.1. Add Constants
```python
RANDOM_BACKWARD_KEY = 'Random Backward Enabled'
RANDOM_BACKWARD_PROBABILITY_KEY = 'Random Backward Probability'
```

#### 3.3.2. Add UI Elements
- **Panel**: "Random Move Backward"
- **Checkbox**: "Enable Random Move Backward"
- **Slider**: "Backward Probability" (0-100%, default 10%)

#### 3.3.3. Add Event Handlers
- `_on_backward_change()`: Handle enable/disable
- `_on_backward_probability_change()`: Handle probability change

#### 3.3.4. Update `_sync_to_routine()`
- Sync `backward_enabled` và `backward_probability` to `config.routine`

#### 3.3.5. Update `DEFAULT_CONFIG`
```python
RANDOM_BACKWARD_KEY: False,  # DISABLED by default
RANDOM_BACKWARD_PROBABILITY_KEY: 0.10,  # 10% default
```

### 3.4. Settings File
- Add keys to settings file structure
- Load/save backward settings

## 4. Logic Flow

### 4.1. Normal Flow (Backward Disabled)
```
Get element -> Check skip -> Execute/Skip -> Step
```

### 4.2. With Backward Enabled
```
Get element -> Check backward -> (If backward: Apply backward, get new element) -> Check skip -> Execute/Skip -> Step
```

### 4.3. Backward + Skip Combination
```
Get element -> Check backward -> (If backward: Apply backward) -> Check skip -> Execute/Skip -> Step
```
- Backward có thể xảy ra trước skip
- Nếu backward xảy ra, bot sẽ execute point tại index mới (có thể bị skip nếu skip check trả về True)

### 4.4. Backward + Floor-only Combination
```
Get element -> Check backward -> (If backward: Apply backward) -> Check skip -> Execute/Skip -> Step
```
- Backward vẫn hoạt động trong floor-only mode
- Backward có thể move index ra ngoài floor (cần xử lý edge case)

## 5. Edge Cases & Considerations

### 5.1. Index Bounds
- **Case**: Backward từ index 0, 1, 2 (không đủ 3 steps)
- **Solution**: Check `if self.index < min_steps: return False, 0`

### 5.2. Backward trong Floor-only
- **Case**: Backward có thể move index ra ngoài floor
- **Solution**: Cho phép backward, nhưng khi step() sẽ tự động điều chỉnh về floor indices

### 5.3. Backward trong Reverse Variant
- **Case**: Backward trong reverse mode
- **Solution**: Backward vẫn hoạt động bình thường (backward là absolute movement, không phụ thuộc variant)

### 5.4. Consecutive Backward
- **Case**: Backward liên tục
- **Solution**: Sử dụng cooldown (5-10 points) để tránh backward liên tục

### 5.5. Backward + Skip
- **Case**: Backward xảy ra, sau đó skip check cũng trả về True
- **Solution**: Cho phép cả hai, backward trước, sau đó skip check

## 6. Logging

### 6.1. Backward Event
```
⏮️ Random Backward: Triggered at index X, backwarding Y steps (cooldown: Z)
⏮️ Random Backward: Index X -> Y (backwarded Z steps)
⏮️ Random Backward: Now at index X, element type: Y
```

### 6.2. Cooldown
```
🎲 Random Backward: Cooldown active (X points remaining)
```

## 7. Testing Checklist

- [ ] Backward enabled/disabled works
- [ ] Backward probability works (10% default)
- [ ] Backward range 2-3 works
- [ ] Cooldown prevents consecutive backward
- [ ] Backward works with Point Selection Randomization
- [ ] Backward works with Floor-only variants
- [ ] Backward works with Reverse variant
- [ ] Edge case: Backward from index 0, 1, 2
- [ ] Edge case: Backward in floor-only (move outside floor)
- [ ] Logging is clear and informative
- [ ] Settings persist correctly
- [ ] GUI syncs with routine object

## 8. Implementation Order

1. **Phase 1**: Add attributes và methods trong `Routine` class
2. **Phase 2**: Integrate backward check vào `bot.py`
3. **Phase 3**: Add GUI settings
4. **Phase 4**: Testing và bug fixes
5. **Phase 5**: Documentation và cleanup

## 9. Notes

- Backward là **optional feature**, không ảnh hưởng luồng chính khi disabled
- Backward xảy ra **TRƯỚC** skip check để đảm bảo timing đúng
- Backward range **hardcode** 2-3 (không cần GUI)
- Cooldown **hardcode** 5-10 points (không cần GUI)
- Probability có thể điều chỉnh từ GUI (0-100%)
