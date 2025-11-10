# Plan: GUI Settings cho Routine Randomization Features

## Tổng quan
Mở rộng GUI Settings để cho phép user config các tính năng randomization:
- Point Selection Randomization
- Routine Pattern Variation (Normal/Reverse)
- Floor-Only Variants

## Giải thích Switch Interval

**Switch Interval** là số loops mà bot sẽ chạy một variant (normal/reverse) trước khi có thể switch sang variant khác hoặc kích hoạt floor-only variant.

### Ví dụ:
- Nếu `variant_switch_interval = 5`: Bot sẽ chạy 5 loops normal trước khi có thể switch sang reverse hoặc kích hoạt floor-only
- Hiện tại hardcode là `random.randint(3, 7)` - nghĩa là mỗi lần switch sẽ random từ 3-7 loops

### Có cần thêm vào GUI không?
- **Không cần thiết** nếu bạn muốn giữ random 3-7 loops (để tăng tính random)
- **Có thể thêm** nếu bạn muốn control chính xác số loops trước khi switch (ví dụ: luôn 5 loops)

**Khuyến nghị**: Giữ hardcode `random.randint(3, 7)` để tăng tính random, không cần thêm vào GUI.

## Cấu trúc GUI hiện tại
File: `src/gui/settings/routine_randomization.py`
- Hiện tại chỉ có 2 checkboxes cơ bản
- Cần mở rộng thành panel chi tiết với các options cần thiết

## Plan chi tiết

### 1. Point Selection Randomization Panel

#### UI Components:
```
┌─ Point Selection Randomization ─────────────┐
│ ☑ Enable Point Selection Randomization     │
│                                              │
│ Skip Probability: [30]%  (Slider 0-100)    │
└─────────────────────────────────────────────┘
```

#### Settings Keys:
- `Point Selection Enabled` (Boolean)
- `Point Selection Skip Probability` (Float 0.0-1.0)
- `Point Selection Max Consecutive Skips` (Integer 1-3) - **HARDCODE, không cần GUI**

#### Implementation:
- Checkbox: Enable/Disable
- Slider hoặc Spinbox: Skip Probability (0-100%)
- Max Consecutive Skips: Hardcode 1-3 trong code

### 2. Routine Pattern Variation Panel

#### UI Components:
```
┌─ Routine Pattern Variation ─────────────────┐
│ ☑ Enable Routine Pattern Variation         │
│                                              │
│ Floor-Only Activation Chance: [10]%        │
│   (Slider 0-100)                             │
└─────────────────────────────────────────────┘
```

#### Settings Keys:
- `Routine Pattern Enabled` (Boolean)
- `Routine Pattern Floor Only Chance` (Float 0.0-1.0)
- `Routine Pattern Switch Interval` (Integer 3-7) - **HARDCODE random.randint(3, 7), không cần GUI**
- `Routine Pattern Floor Only Loop Min` (Integer 3) - **HARDCODE, không cần GUI**
- `Routine Pattern Floor Only Loop Max` (Integer 5) - **HARDCODE, không cần GUI**

#### Implementation:
- Checkbox: Enable/Disable main feature
- Slider hoặc Spinbox: Floor-Only Activation Chance (0-100%)
- Switch Interval: Hardcode `random.randint(3, 7)` trong code
- Floor-Only Loop Range: Hardcode `(3, 5)` trong code

### 3. Layout Structure

#### Simplified Panel Design:
```
┌─ Routine Randomization ──────────────────────┐
│                                              │
│ ┌─ Point Selection ───────────────────────┐ │
│ │ ☑ Enable                                 │ │
│ │ Probability: [30]%                       │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ ┌─ Routine Pattern ────────────────────────┐ │
│ │ ☑ Enable                                 │ │
│ │ Floor-Only Chance: [10]%                 │ │
│ └──────────────────────────────────────────┘ │
│                                              │
│ [Reset to Defaults]                         │
└──────────────────────────────────────────────┘
```

### 4. Implementation Steps

#### Step 1: Update Settings Class
- Mở rộng `RoutineRandomizationSettings` với các keys mới
- Thêm default values cho tất cả settings

#### Step 2: Update GUI Class
- Thay thế 2 checkboxes đơn giản bằng panel chi tiết
- Thêm các widgets:
  - Slider cho skip probability
  - Slider cho floor-only chance
  - Checkboxes cho enable/disable

#### Step 3: Hardcode Values trong Routine Class
- `max_consecutive_skips`: Hardcode 1-3 (random.randint(1, 3))
- `variant_switch_interval`: Hardcode random.randint(3, 7)
- `floor_variant_loop_range`: Hardcode (3, 5)

#### Step 4: Sync với Routine Class
- Update `Routine.__init__()` để load từ settings
- Update `Routine.load()` để apply settings khi load routine
- Đảm bảo settings được apply real-time khi user thay đổi

#### Step 5: Validation
- Validate probabilities (0-100%)
- Show warnings nếu config không hợp lý

### 5. Code Structure

#### File: `src/gui/settings/routine_randomization.py`

```python
class RoutineRandomization(LabelFrame):
    def __init__(self, parent, **kwargs):
        # Point Selection Panel
        self.point_selection_frame = LabelFrame(self, "Point Selection")
        # Checkbox: Enable
        # Slider: Skip Probability (0-100%)
        
        # Routine Pattern Panel
        self.routine_pattern_frame = LabelFrame(self, "Routine Pattern")
        # Checkbox: Enable
        # Slider: Floor-Only Activation Chance (0-100%)
        
    def _on_point_selection_change(self):
        # Update settings and sync to routine
        
    def _on_routine_pattern_change(self):
        # Update settings and sync to routine
        
    def _sync_to_routine(self):
        # Apply settings to config.routine
```

#### File: `src/routine/routine.py`

```python
def __init__(self):
    # Hardcode values
    self.max_consecutive_skips = random.randint(1, 3)  # Hardcode 1-3
    self.variant_switch_interval = random.randint(3, 7)  # Hardcode 3-7
    self.floor_variant_loop_range = (3, 5)  # Hardcode 3-5
    
    # Load settings from GUI
    self._load_randomization_settings()
    
def _load_randomization_settings(self):
    from src.gui.settings.routine_randomization import RoutineRandomizationSettings
    settings = RoutineRandomizationSettings('routine_randomization')
    # Load enabled flags and probabilities only
```

### 6. Settings File Location
- Settings được lưu trong: `config/routine_randomization.json`
- Format JSON với các keys cần thiết

### 7. Real-time Updates
- Khi user thay đổi settings trong GUI:
  1. Save to settings file
  2. Update `config.routine` object immediately
  3. Log changes for debugging

### 8. Default Values

```python
DEFAULT_CONFIG = {
    # Point Selection
    'Point Selection Enabled': False,
    'Point Selection Skip Probability': 0.30,
    # Max Consecutive Skips: Hardcode random.randint(1, 3)
    
    # Routine Pattern
    'Routine Pattern Enabled': False,
    'Routine Pattern Floor Only Chance': 0.10,
    # Switch Interval: Hardcode random.randint(3, 7)
    # Floor-Only Loop Range: Hardcode (3, 5)
}
```

## Hardcode Values Summary

### Point Selection Randomization:
- `max_consecutive_skips`: `random.randint(1, 3)` - Random từ 1-3 skips liên tiếp

### Routine Pattern Variation:
- `variant_switch_interval`: `random.randint(3, 7)` - Random từ 3-7 loops trước khi switch
- `floor_variant_loop_range`: `(3, 5)` - Floor-only chạy 3-5 loops rồi quay về normal

## Testing Checklist
- [ ] Settings được load đúng khi start bot
- [ ] Settings được apply real-time khi thay đổi
- [ ] Settings được save vào file
- [ ] Hardcode values hoạt động đúng
- [ ] Validation hoạt động đúng
- [ ] UI responsive và dễ sử dụng
- [ ] Logs hiển thị settings changes

## Notes
- Giữ backward compatibility với settings hiện tại
- Hardcode values giúp tăng tính random mà không cần config phức tạp
- Settings chỉ apply khi bot restart hoặc routine reload
- Có thể thêm "Apply Now" button để apply ngay lập tức
