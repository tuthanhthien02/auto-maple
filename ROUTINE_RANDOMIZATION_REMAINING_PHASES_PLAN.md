# Plan Cho Các Phase Còn Lại - Routine Randomization

## Tổng Quan
Hiện tại đã implement:
- ✅ **Phase 1: Point Selection Randomization** (đã tắt tạm thời để test reverse)
- ✅ **Phase 2: Routine Pattern Variation** (normal/reverse switching)

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

2. **Skip Commands (Optional)**
   - Đôi khi skip một số commands không quan trọng
   - Ví dụ: skip `wait_random` 10% chance
   - Safety: Không bao giờ skip `buff`, `reflection_random` (quan trọng)

3. **Add Random Waits**
   - Đôi khi thêm `wait_random` giữa các commands
   - Probability: 5-10% chance
   - Duration: 0.1-0.3s

### Implementation
- File: `src/routine/components.py` - Modify `Point.main()`
- Add config: `command_sequence_randomization_enabled`, `shuffle_probability`, `skip_probability`
- Logic:
  ```python
  if command_sequence_randomization_enabled:
      if random.random() < shuffle_probability:
          commands = shuffle_commands(commands)
      for command in commands:
          if should_skip_command(command):
              continue
          command.execute()
          if should_add_wait():
              wait_random(0.1, 0.3)
  ```

### Priority
- **High** - Tạo variation lớn trong command execution
- **Risk**: Low (chỉ ảnh hưởng thứ tự commands, không ảnh hưởng movement)

---

## Phase 4: Position Offset Randomization ⭐⭐⭐⭐

### Mục Tiêu
Thêm random offset nhỏ vào target position của mỗi Point để tạo variation trong positioning.

### Tính Năng
1. **Random Position Offset**
   - Thêm offset nhỏ vào (x, y) của mỗi Point
   - Ví dụ: (0.229, 0.19) → (0.229 ± 0.005, 0.19 ± 0.003)
   - Offset range: 0.003-0.008 (có thể config)

2. **Safety Checks**
   - Đảm bảo offset không làm bot đi sai đường
   - Không apply offset nếu distance quá xa từ original position
   - Không apply offset cho `adjust=True` points (quan trọng)

### Implementation
- File: `src/routine/components.py` - Modify `Point.main()` và `Move.main()`
- Add config: `position_offset_enabled`, `offset_range_min`, `offset_range_max`
- Logic:
  ```python
  if position_offset_enabled and not self.adjust:
      offset_x = random.uniform(-offset_range, offset_range)
      offset_y = random.uniform(-offset_range, offset_range)
      target = (self.location[0] + offset_x, self.location[1] + offset_y)
  else:
      target = self.location
  ```

### Priority
- **Medium** - Tạo variation nhỏ trong positioning
- **Risk**: Medium (có thể ảnh hưởng pathfinding nếu offset quá lớn)

---

## Phase 5: Path Randomization ⭐⭐⭐⭐

### Mục Tiêu
Thay vì luôn dùng shortest path, đôi khi dùng path khác hoặc thêm detours để tạo variation.

### Tính Năng
1. **Multiple Path Options**
   - Thay vì luôn dùng `shortest_path()`, có thể dùng path khác
   - Probability: 20-30% chance để dùng non-shortest path
   - Có thể thêm 1-2 extra steps trong path

2. **Slight Detours**
   - Đôi khi thêm detour nhỏ trong path
   - Ví dụ: đi qua một node gần đó trước khi đến target
   - Probability: 10-15% chance

3. **Path Selection Weights**
   - Shortest path: 70% weight
   - Path với 1 extra step: 20% weight
   - Path với 2 extra steps: 10% weight

### Implementation
- File: `src/routine/layout.py` - Modify `shortest_path()` hoặc thêm `random_path()`
- Add config: `path_randomization_enabled`, `detour_probability`
- Logic:
  ```python
  if path_randomization_enabled:
      if random.random() < detour_probability:
          path = random_path_with_detour(source, target)
      else:
          path = shortest_path(source, target)
  ```

### Priority
- **Medium** - Tạo variation trong movement paths
- **Risk**: Medium (có thể làm bot đi xa hơn, mất thời gian)

---

## Phase 6: Command Execution Randomization (Advanced) ⭐⭐⭐

### Mục Tiêu
Randomize parameters của commands (không phải lúc nào cũng exact values).

### Tính Năng
1. **Randomize Command Parameters**
   - Ví dụ: `teleport,right,1` có thể thành `teleport,right,2` (10% chance)
   - Ví dụ: `wait_random,0.1,0.3` có thể thành `wait_random,0.15,0.35`
   - Probability: 10-20% chance để randomize parameters

2. **Command Variants**
   - Tạo "variants" của commands
   - Ví dụ: `buff` có thể thành `buff` + `buff_secondary` (double buff)
   - Probability: 5-10% chance

### Implementation
- File: `src/routine/components.py` - Modify command execution
- Add config: `command_parameter_randomization_enabled`
- Logic:
  ```python
  if command_parameter_randomization_enabled:
      if isinstance(command, Teleport):
          # Đôi khi thêm 1 teleport extra
          if random.random() < 0.1:
              command.times += 1
  ```

### Priority
- **Low** - Tạo variation nhỏ trong command execution
- **Risk**: Low (chỉ ảnh hưởng parameters, không ảnh hưởng logic)

---

## Phase 7: Re-enable Point Selection Randomization ⭐⭐⭐⭐⭐

### Mục Tiêu
Re-enable Point Selection Randomization sau khi test reverse variant xong.

### Tính Năng
1. **Re-enable Skip Logic**
   - Bật lại `skip_enabled = True`
   - Test với reverse variant để đảm bảo hoạt động đúng

2. **Tuning Skip Probability**
   - Điều chỉnh `skip_probability` dựa trên test results
   - Có thể giảm xuống 20-30% (thay vì 35%)
   - Test với cả normal và reverse variant

3. **Skip Logic Improvements**
   - Đảm bảo skip logic hoạt động đúng với reverse variant
   - Có thể cần điều chỉnh logic detect loop completion khi skip

### Implementation
- File: `src/routine/routine.py` - Set `skip_enabled = True`
- Test với cả normal và reverse variant
- Tune `skip_probability` và `max_consecutive_skips`

### Priority
- **High** - Đây là tính năng chính đã implement nhưng tắt tạm thời
- **Risk**: Low (đã test trước đó, chỉ cần re-enable)

---

## Phase 8: Routine Pattern Variation - Floor Only Variants ⭐⭐⭐

### Mục Tiêu
Implement floor-only variants (floor1_only, floor2_only) đã có trong code nhưng chưa test.

### Tính Năng
1. **Floor 1 Only Variant**
   - Chỉ train ở Floor 1 points
   - Skip Floor 2 points hoàn toàn
   - Loop khi quay về first Floor 1 point

2. **Floor 2 Only Variant**
   - Chỉ train ở Floor 2 points
   - Skip Floor 1 points hoàn toàn
   - Loop khi quay về first Floor 2 point

3. **Variant Weights**
   - Normal: 70%
   - Reverse: 15%
   - Floor 1 Only: 10%
   - Floor 2 Only: 5%

### Implementation
- File: `src/routine/routine.py` - Đã có code, cần test
- Test với `tree_2_floor_new.csv` routine
- Đảm bảo floor detection hoạt động đúng
- Test variant switching giữa floor-only variants

### Priority
- **Medium** - Đã có code, chỉ cần test và tune
- **Risk**: Low (logic đã implement, chỉ cần test)

---

## Phase 9: Analytics & Monitoring ⭐⭐

### Mục Tiêu
Thêm analytics và monitoring để track performance của randomization.

### Tính Năng
1. **Statistics Tracking**
   - Track số loops completed per variant
   - Track số points skipped
   - Track số teleports vs walks
   - Track average distance per move

2. **Logging Improvements**
   - Thêm detailed logs cho mỗi phase
   - Log statistics mỗi N loops
   - Export statistics to file (optional)

3. **GUI Integration**
   - Hiển thị statistics trong GUI
   - Hiển thị current variant và loop count
   - Hiển thị skip probability và teleport usage

### Implementation
- File: `src/routine/routine.py` - Add statistics tracking
- File: `src/gui/` - Add GUI panels cho statistics
- Add config: `analytics_enabled`, `statistics_export_enabled`

### Priority
- **Low** - Nice to have, không ảnh hưởng core functionality
- **Risk**: Low (chỉ tracking, không ảnh hưởng logic)

---

## Phase 10: Configuration & Settings ⭐⭐⭐

### Mục Tiêu
Thêm configuration và settings để user có thể tune randomization.

### Tính Năng
1. **Settings File**
   - Tạo settings file cho randomization
   - Ví dụ: `routine_randomization_config.json`
   - Có thể enable/disable từng phase
   - Có thể tune probabilities và thresholds

2. **GUI Settings Panel**
   - Thêm settings panel trong GUI
   - Enable/disable từng phase
   - Tune probabilities và thresholds
   - Save/load settings

3. **Presets**
   - Tạo presets (Low, Medium, High randomization)
   - User có thể chọn preset hoặc custom

### Implementation
- File: `src/common/settings.py` - Add randomization settings
- File: `src/gui/settings/` - Add randomization settings panel
- File: `routine_randomization_config.json` - Settings file

### Priority
- **Medium** - Giúp user tune randomization dễ dàng
- **Risk**: Low (chỉ configuration, không ảnh hưởng logic)

---

## Thứ Tự Ưu Tiên Implement

### High Priority (Implement Trước)
1. **Phase 7: Re-enable Point Selection Randomization** ⭐⭐⭐⭐⭐
2. **Phase 3: Command Sequence Randomization** ⭐⭐⭐⭐⭐
3. **Phase 8: Routine Pattern Variation - Floor Only Variants** ⭐⭐⭐

### Medium Priority (Implement Sau)
4. **Phase 4: Position Offset Randomization** ⭐⭐⭐⭐
5. **Phase 5: Path Randomization** ⭐⭐⭐⭐
6. **Phase 10: Configuration & Settings** ⭐⭐⭐

### Low Priority (Implement Cuối)
7. **Phase 6: Command Execution Randomization (Advanced)** ⭐⭐⭐
8. **Phase 9: Analytics & Monitoring** ⭐⭐

---

## Testing Checklist

### Cho Mỗi Phase
- [ ] Test với normal variant
- [ ] Test với reverse variant
- [ ] Test với floor-only variants (nếu applicable)
- [ ] Test với Point Selection Randomization enabled
- [ ] Test với Point Selection Randomization disabled
- [ ] Verify không có bugs hoặc unexpected behavior
- [ ] Verify performance không bị ảnh hưởng đáng kể
- [ ] Verify logs hiển thị đúng thông tin

### Integration Testing
- [ ] Test tất cả phases cùng lúc
- [ ] Test với different routines (1 floor, 2 floors)
- [ ] Test với different maps
- [ ] Test long-running sessions (1+ hours)

---

## Notes

1. **Safety First**: Luôn đảm bảo randomization không làm bot đi sai đường hoặc stuck
2. **Performance**: Đảm bảo randomization không làm bot chậm đáng kể
3. **Configurability**: Cho phép user enable/disable và tune từng phase
4. **Testing**: Test kỹ với cả normal và reverse variant trước khi release
5. **Documentation**: Update documentation sau mỗi phase

---

## Timeline Ước Tính

- **Phase 7**: 1-2 days (re-enable và test)
- **Phase 3**: 3-5 days (implement và test)
- **Phase 8**: 2-3 days (test và tune)
- **Phase 4**: 2-3 days (implement và test)
- **Phase 5**: 3-4 days (implement và test)
- **Phase 10**: 2-3 days (implement và test)
- **Phase 6**: 2-3 days (implement và test)
- **Phase 9**: 1-2 days (implement và test)

**Total**: ~20-30 days (tùy vào độ phức tạp và testing)

