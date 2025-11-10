# Plan Cho Các Phase Còn Lại - Routine Randomization

## Tổng Quan
Hiện tại đã implement:
- ✅ **Phase 1: Point Selection Randomization** (skip points với probability)
- ✅ **Phase 2: Routine Pattern Variation** (normal/reverse switching)
- ✅ **Phase 2.5: Floor-Only Variants** (floor1_only, floor2_only với forward/reverse)
- ✅ **Phase 2.6: GUI Settings** (config enable/disable và probabilities)

Các phase còn lại cần implement:

---

## Phase 3: Command Sequence Randomization ⭐⭐⭐⭐⭐

### Mục Tiêu
Randomize thứ tự các commands trong mỗi Point để tạo variation trong cách execute commands.

### Tính Năng
1. **Randomize Command Order**
   - Đôi khi shuffle thứ tự commands trong Point
   - Ví dụ: `buff -> buff_secondary -> reflection_random` có thể thành `reflection_random -> buff -> buff_secondary`
   - Probability: 30-50% chance để shuffle
   - Safety: Giữ `move` command luôn đầu tiên (nếu có)

2. **Skip Commands (Optional)**
   - Đôi khi skip một số commands không quan trọng
   - Ví dụ: skip `wait_random` 10% chance
   - Safety: Không bao giờ skip `buff`, `reflection_random`, `move` (quan trọng)
   - Configurable: List commands có thể skip

3. **Add Random Waits**
   - Đôi khi thêm `wait_random` giữa các commands
   - Probability: 5-10% chance
   - Duration: 0.1-0.3s

### Implementation
- File: `src/routine/components.py` - Modify `Point.main()`
- Add config: 
  - `command_sequence_randomization_enabled` (Boolean)
  - `command_shuffle_probability` (Float 0.0-1.0)
  - `command_skip_probability` (Float 0.0-1.0)
  - `command_add_wait_probability` (Float 0.0-1.0)
- Logic:
  ```python
  if command_sequence_randomization_enabled:
      commands_copy = list(commands)
      if random.random() < command_shuffle_probability:
          commands_copy = shuffle_commands(commands_copy, keep_move_first=True)
      for command in commands_copy:
          if should_skip_command(command):
              continue
          command.execute()
          if should_add_wait():
              wait_random(0.1, 0.3)
  ```

### GUI Settings
- Checkbox: Enable Command Sequence Randomization
- Slider: Shuffle Probability (0-100%)
- Slider: Skip Command Probability (0-100%)
- Slider: Add Random Wait Probability (0-100%)

### Priority
- **High** - Tạo variation lớn trong command execution
- **Risk**: Low (chỉ ảnh hưởng thứ tự commands, không ảnh hưởng movement)
- **Estimated Time**: 2-3 hours

---

## Phase 4: Position Offset Randomization ⭐⭐⭐⭐

### Mục Tiêu
Thêm random offset nhỏ vào target position của mỗi Point để tạo variation trong positioning.

### Tính Năng
1. **Random Position Offset**
   - Thêm offset nhỏ (±0.003 - ±0.008) vào x, y coordinates
   - Chỉ áp dụng khi move đến Point
   - Không ảnh hưởng đến adjust logic

2. **Configurable Range**
   - Min/Max offset range có thể config
   - Default: (0.003, 0.008) - đủ nhỏ để không ảnh hưởng gameplay

### Implementation
- File: `src/routine/components.py` - Modify `Point.__init__()` hoặc `Move.main()`
- Add config:
  - `position_offset_enabled` (Boolean)
  - `position_offset_min` (Float 0.003)
  - `position_offset_max` (Float 0.008)
- Logic:
  ```python
  if position_offset_enabled:
      offset_x = random.uniform(-offset_max, offset_max)
      offset_y = random.uniform(-offset_max, offset_max)
      target_x = original_x + offset_x
      target_y = original_y + offset_y
  ```

### GUI Settings
- Checkbox: Enable Position Offset Randomization
- Spinbox: Min Offset (0.001-0.010)
- Spinbox: Max Offset (0.001-0.010)

### Priority
- **Medium** - Tạo variation trong positioning
- **Risk**: Medium (có thể ảnh hưởng đến pathfinding nếu offset quá lớn)
- **Estimated Time**: 1-2 hours

---

## Phase 5: Path Variation (Multiple Paths) ⭐⭐⭐⭐

### Mục Tiêu
Tạo nhiều paths khác nhau giữa 2 points để tạo variation trong movement.

### Tính Năng
1. **Multiple Path Generation**
   - Generate 2-3 paths khác nhau giữa 2 points
   - Random chọn 1 path mỗi lần move
   - Paths có thể đi qua các waypoints khác nhau

2. **Path Selection**
   - Random chọn path mỗi lần move
   - Có thể weighted (một số paths được chọn thường xuyên hơn)

### Implementation
- File: `src/routine/components.py` - Modify `Move.main()`
- File: `src/common/layout.py` - Add path generation logic
- Add config:
  - `path_variation_enabled` (Boolean)
  - `path_count` (Integer 2-3)
  - `path_selection_weighted` (Boolean)
- Logic:
  ```python
  if path_variation_enabled:
      paths = generate_multiple_paths(start, end, count=path_count)
      selected_path = random.choices(paths, weights=weights)[0]
      follow_path(selected_path)
  ```

### GUI Settings
- Checkbox: Enable Path Variation
- Spinbox: Number of Paths (2-3)
- Checkbox: Use Weighted Selection

### Priority
- **Medium** - Tạo variation trong movement paths
- **Risk**: Medium-High (có thể phức tạp và ảnh hưởng đến pathfinding)
- **Estimated Time**: 4-6 hours

---

## Phase 6: Command Execution Timing Randomization ⭐⭐⭐

### Mục Tiêu
Randomize timing giữa các commands để tạo variation trong execution speed.

### Tính Năng
1. **Variable Command Delays**
   - Thêm random delay giữa các commands
   - Range: 0.05-0.15s
   - Probability: 20-30% chance

2. **Command-Specific Delays**
   - Một số commands có thể có delay riêng
   - Ví dụ: `buff` có thể delay 0.1-0.2s sau khi execute

### Implementation
- File: `src/routine/components.py` - Modify `Point.main()`
- Add config:
  - `command_timing_randomization_enabled` (Boolean)
  - `command_delay_probability` (Float 0.0-1.0)
  - `command_delay_min` (Float 0.05)
  - `command_delay_max` (Float 0.15)

### GUI Settings
- Checkbox: Enable Command Timing Randomization
- Slider: Delay Probability (0-100%)
- Spinbox: Min Delay (0.05-0.20s)
- Spinbox: Max Delay (0.05-0.20s)

### Priority
- **Low** - Nice to have, nhưng timing randomization đã có cơ bản
- **Risk**: Low
- **Estimated Time**: 1-2 hours

---

## Phase 7: Loop Pattern Randomization ⭐⭐⭐

### Mục Tiêu
Randomize số loops trước khi switch variant hoặc thay đổi pattern.

### Tính Năng
1. **Variable Loop Counts**
   - Randomize số loops cho mỗi variant
   - Hiện tại đã có: `random.randint(3, 7)` cho switch interval
   - Có thể mở rộng: randomize floor-only loop range

2. **Dynamic Pattern Switching**
   - Switch pattern dựa trên conditions khác nhau
   - Ví dụ: switch sau khi kill X mobs, hoặc sau Y seconds

### Implementation
- File: `src/routine/routine.py` - Modify `_pick_switch_interval()`
- Add config:
  - `loop_pattern_randomization_enabled` (Boolean)
  - `switch_interval_min` (Integer 3)
  - `switch_interval_max` (Integer 7)

### GUI Settings
- Checkbox: Enable Loop Pattern Randomization
- Spinbox: Min Switch Interval (2-10)
- Spinbox: Max Switch Interval (2-10)

### Priority
- **Low** - Đã có cơ bản với hardcode random
- **Risk**: Low
- **Estimated Time**: 1 hour

---

## Implementation Priority & Timeline

### High Priority (Implement First)
1. **Phase 3: Command Sequence Randomization** ⭐⭐⭐⭐⭐
   - Impact: Rất cao
   - Risk: Thấp
   - Time: 2-3 hours
   - **Recommend: Implement ngay**

### Medium Priority (Implement Next)
2. **Phase 4: Position Offset Randomization** ⭐⭐⭐⭐
   - Impact: Cao
   - Risk: Trung bình
   - Time: 1-2 hours
   - **Recommend: Implement sau Phase 3**

3. **Phase 5: Path Variation** ⭐⭐⭐⭐
   - Impact: Cao
   - Risk: Trung bình-Cao
   - Time: 4-6 hours
   - **Recommend: Implement sau Phase 4**

### Low Priority (Optional)
4. **Phase 6: Command Timing Randomization** ⭐⭐⭐
   - Impact: Trung bình
   - Risk: Thấp
   - Time: 1-2 hours
   - **Recommend: Implement khi có thời gian**

5. **Phase 7: Loop Pattern Randomization** ⭐⭐⭐
   - Impact: Thấp (đã có cơ bản)
   - Risk: Thấp
   - Time: 1 hour
   - **Recommend: Optional**

---

## Testing Strategy

### Phase 3 Testing
- [ ] Test command shuffle với các Point khác nhau
- [ ] Verify commands quan trọng không bị skip
- [ ] Test với routine có nhiều commands
- [ ] Verify không ảnh hưởng đến movement

### Phase 4 Testing
- [ ] Test position offset với các ranges khác nhau
- [ ] Verify không ảnh hưởng đến pathfinding
- [ ] Test với adjust=True và adjust=False
- [ ] Verify bot vẫn reach target đúng

### Phase 5 Testing
- [ ] Test multiple path generation
- [ ] Verify paths không overlap hoặc conflict
- [ ] Test path selection randomness
- [ ] Verify bot vẫn reach target đúng

---

## Configuration Summary

### Settings Keys cần thêm:
```python
# Phase 3: Command Sequence
'Command Sequence Enabled': False
'Command Shuffle Probability': 0.40
'Command Skip Probability': 0.10
'Command Add Wait Probability': 0.05

# Phase 4: Position Offset
'Position Offset Enabled': False
'Position Offset Min': 0.003
'Position Offset Max': 0.008

# Phase 5: Path Variation
'Path Variation Enabled': False
'Path Count': 2
'Path Selection Weighted': False

# Phase 6: Command Timing
'Command Timing Enabled': False
'Command Delay Probability': 0.25
'Command Delay Min': 0.05
'Command Delay Max': 0.15

# Phase 7: Loop Pattern
'Loop Pattern Enabled': True  # Already implemented
'Switch Interval Min': 3
'Switch Interval Max': 7
```

---

## Notes
- Tất cả phases đều có enable/disable flag
- Settings được lưu trong GUI và sync với routine
- Hardcode values được giữ cho các tính năng không cần config
- Testing cần thorough để đảm bảo không break existing functionality
