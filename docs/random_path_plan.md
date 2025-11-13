# Plan: Random Path Feature

## Mục tiêu
Cho phép cùng 1 routine có thể chạy 3-5 path khác nhau, tăng tính human-like và giảm detection risk.

## 1. Cấu trúc Descriptor

### Option A: Multiple Path Labels (Recommended)
Định nghĩa nhiều path bằng cách sử dụng label convention:
```
Label,start_routine
# Path 1: Standard path
Label,path1_start
*,0.107,0.090
Label,f1_pos_0
...
Jump,path1_end

Label,path1_end
Jump,path1_start  # Loop back

# Path 2: Alternative path (skip some points)
Label,path2_start
*,0.170,0.090  # Skip first 2 points
Label,f1_pos_2
...
Jump,path2_end

Label,path2_end
Jump,path2_start  # Loop back
```

### Option B: Path Directive (More structured)
Thêm directive mới `Path` để group paths:
```
Label,start_routine

Path,path1
Label,path1_start
*,0.107,0.090
...
Jump,path1_start

Path,path2
Label,path2_start
*,0.170,0.090
...
Jump,path2_start
```

**Recommendation: Option A** - Đơn giản hơn, tương thích với code hiện tại, chỉ cần convention về label naming.

## 2. Path Detection Logic

### 2.1 Auto-detect paths từ labels
- Scan tất cả labels trong routine
- Detect pattern: `path{N}_start` và `path{N}_end`
- Validate: mỗi path phải có start và end label
- Validate: path end phải có Jump về path start

### 2.2 Path metadata
- `path_id`: "path1", "path2", ...
- `start_label`: Label object cho path start
- `end_label`: Label object cho path end
- `start_index`: Index trong sequence
- `end_index`: Index trong sequence
- `weight`: Weight cho random selection (default: equal)

## 3. Path Selection Mechanism

### 3.1 Selection modes
1. **Random per loop**: Chọn path mới mỗi loop
2. **Random per interval**: Chọn path mới sau N loops (3-7 loops)
3. **Weighted random**: Chọn path dựa trên weight
4. **Sequential**: Chạy tuần tự path1 → path2 → ... → path1

### 3.2 Selection timing
- Khi loop completion detected
- Khi routine starts
- Khi path switch interval reached

## 4. Configuration

### 4.1 default.json structure
```json
{
  "routine_randomization": {
    "random_path": {
      "enabled": false,
      "selection_mode": "random_per_loop",  // "random_per_loop", "random_per_interval", "weighted", "sequential"
      "switch_interval": {
        "enabled": false,  // Only for random_per_interval
        "min_loops": 3,
        "max_loops": 7
      },
      "path_weights": {  // Only for weighted mode
        "path1": 0.4,
        "path2": 0.3,
        "path3": 0.3
      },
      "auto_detect": true,  // Auto-detect paths from labels
      "paths": [  // Manual path definition (if auto_detect = false)
        {
          "id": "path1",
          "start_label": "path1_start",
          "end_label": "path1_end"
        }
      ]
    }
  }
}
```

## 5. Implementation Steps

### Step 1: Path Detection & Storage
- [ ] Add `path_config` dict to Routine class
- [ ] Add `detect_paths()` method to scan labels
- [ ] Add `path_metadata` list to store path info
- [ ] Add `current_path_id` to track active path

### Step 2: Path Selection Logic
- [ ] Add `select_next_path()` method
- [ ] Implement selection modes (random, weighted, sequential)
- [ ] Add path switch interval logic

### Step 3: Path Execution
- [ ] Modify loop completion detection to check path end
- [ ] Modify step() to handle path switching
- [ ] Update index to path start when switching

### Step 4: Integration với existing features
- [ ] Ensure compatibility với Routine Pattern Variation
- [ ] Ensure compatibility với Point Selection Randomization
- [ ] Ensure compatibility với Random Backward

### Step 5: Configuration & GUI
- [ ] Add random_path config to default.json
- [ ] Add GUI panel for random path settings
- [ ] Add path visualization in routine view

### Step 6: Metrics & Logging
- [ ] Track path switches in MetricsLogger
- [ ] Log path selection decisions
- [ ] Add path stats to periodic summary

## 6. Edge Cases & Validation

### 6.1 Validation
- Validate path start/end labels exist
- Validate path end has Jump to path start
- Validate at least 2 paths if enabled
- Validate path weights sum to 1.0 (if weighted mode)

### 6.2 Edge cases
- No paths detected: fallback to normal routine
- Path start label not found: skip to next path
- Path end label not found: use last point in path
- Path switching during backward movement: handle gracefully

## 7. Example Usage

### Descriptor example:
```csv
Label,start_routine

# Path 1: Full path
Label,path1_start
*,0.107,0.090
Label,f1_pos_0
...
*,0.244,0.090
Label,f1_pos_4
Jump,path1_end

Label,path1_end
Jump,path1_start

# Path 2: Skip first 2 points
Label,path2_start
*,0.170,0.090
Label,f1_pos_2
...
*,0.244,0.090
Label,f1_pos_4
Jump,path2_end

Label,path2_end
Jump,path2_start

# Path 3: Skip last 2 points
Label,path3_start
*,0.107,0.090
Label,f1_pos_0
...
*,0.170,0.090
Label,f1_pos_2
Jump,path3_end

Label,path3_end
Jump,path3_start
```

### Config example:
```json
{
  "random_path": {
    "enabled": true,
    "selection_mode": "random_per_loop",
    "auto_detect": true
  }
}
```

## 8. Testing Plan

1. **Unit tests**:
   - Path detection from labels
   - Path selection logic (all modes)
   - Path switching logic

2. **Integration tests**:
   - Path switching với routine pattern variation
   - Path switching với point selection randomization
   - Long-run stability với path switching

3. **Manual tests**:
   - Test với 3-5 paths
   - Test các selection modes
   - Test edge cases

## 9. Metrics to Track

- Path switch count
- Time spent per path
- Path selection distribution
- Path switch frequency

## 10. Future Enhancements

- Path transition probabilities (path1 → path2: 30%, path1 → path3: 70%)
- Dynamic path weights based on performance
- Path learning: prefer paths with better results
- Path templates: define path variations programmatically

