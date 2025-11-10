# Phase 5: Path Variation - Detailed Implementation Plan

## 🎯 Mục Tiêu

Implement **Path Variation** để tạo nhiều paths khác nhau giữa 2 points, giúp:
1. **Tránh pattern detection** - Không luôn dùng cùng một path
2. **Human-like behavior** - Humans không luôn đi shortest path
3. **Variation trong movement** - Mỗi lần di chuyển có thể có path khác nhau
4. **Anti-detection** - Khó detect hơn với multiple paths

---

## 📋 Phân Tích Codebase Hiện Tại

### Current Pathfinding System

**File:** `src/routine/layout.py` - `Layout.shortest_path()`

**Current Implementation:**
- ✅ Sử dụng A* algorithm với heuristic
- ✅ Sử dụng quadtree để search nodes
- ✅ Tìm shortest path từ source đến target
- ✅ Sử dụng horizontal và vertical teleports
- ✅ Path được lưu trong `config.path` và vẽ trên minimap
- ✅ Path được sử dụng trong `Move.main()` để di chuyển

**Current Code Flow:**
```python
# In Move.main()
path = config.layout.shortest_path(config.player_pos, self.target)
for i, point in enumerate(path):
    # Move to each point in path
```

**Issues:**
- ❌ **Predictable** - Luôn dùng cùng một path cho cùng source/target
- ❌ **No variation** - Không có alternate routes
- ❌ **Pattern detection risk** - Dễ detect với fixed paths

---

## 🎯 Path Variation Approach

### Strategy: Multiple Path Generation với Weighted Selection

**Concept:**
1. Generate 2-3 paths khác nhau từ source đến target
2. Sử dụng các strategies khác nhau để tạo variation
3. Chọn random một path với weighted probability (shortest path có weight cao hơn)

**Advantages:**
- ✅ Phù hợp với codebase hiện tại (dựa trên A*)
- ✅ Không cần thay đổi core pathfinding logic
- ✅ Có thể enable/disable dễ dàng
- ✅ Low risk (fallback về shortest path nếu không generate được alternative)

---

## 📝 Implementation Plan

### Step 1: Add Helper Methods to Layout Class

**File:** `src/routine/layout.py`

#### 1.1: Calculate Path Length
```python
def _calculate_path_length(self, path):
    """Calculate total distance of a path."""
    if len(path) < 2:
        return 0
    total = 0
    for i in range(len(path) - 1):
        total += utils.distance(path[i], path[i + 1])
    return total
```

#### 1.2: Check Duplicate Paths
```python
def _is_duplicate_path(self, path1, path2, tolerance=0.01):
    """Check if two paths are essentially the same."""
    if len(path1) != len(path2):
        return False
    for p1, p2 in zip(path1, path2):
        if utils.distance(p1, p2) > tolerance:
            return False
    return True
```

#### 1.3: Remove Duplicate Paths
```python
def _remove_duplicate_paths(self, paths):
    """Remove duplicate paths from list."""
    unique = []
    for path in paths:
        is_duplicate = False
        for existing in unique:
            if self._is_duplicate_path(path, existing):
                is_duplicate = True
                break
        if not is_duplicate:
            unique.append(path)
    return unique
```

---

### Step 2: Alternative Path Generation Strategies

**File:** `src/routine/layout.py`

#### 2.1: Path with Preference (Horizontal/Vertical First)

**Strategy:** Prefer horizontal movement trước, hoặc vertical movement trước

```python
def _path_with_preference(self, source, target, prefer_horizontal=True):
    """
    Generate path with preference for horizontal or vertical movement first.
    
    Args:
        source: Starting position
        target: Target position
        prefer_horizontal: If True, prefer horizontal movement first
    
    Returns:
        Path as list of (x, y) tuples, or None if failed
    """
    # Modify push_neighbors logic to prefer horizontal/vertical first
    # Similar to shortest_path but with different ordering
    # Implementation similar to shortest_path but change push_best logic
```

**Note:** Cần modify `push_neighbors` logic để prefer một direction trước.

#### 2.2: Path with Weighted Heuristic

**Strategy:** Sử dụng weighted heuristic (1.1x-1.2x) để tìm paths khác

```python
def _path_with_weighted_heuristic(self, source, target, weight=1.1):
    """
    Generate path using weighted heuristic (allows slightly longer paths).
    
    Args:
        source: Starting position
        target: Target position
        weight: Heuristic weight multiplier (1.1 = 10% more lenient)
    
    Returns:
        Path as list of (x, y) tuples, or None if failed
    """
    # Similar to shortest_path but multiply heuristic by weight
    # This allows algorithm to explore slightly longer paths
```

**Implementation:**
- Modify heuristic calculation: `heuristic = (distance + utils.distance(closest, target)) * weight`
- Weight 1.1 = 10% more lenient, allows slightly longer paths
- Weight 1.2 = 20% more lenient, allows more variation

#### 2.3: Path with Detour

**Strategy:** Thêm một detour point gần đó trước khi đến target

```python
def _path_with_detour(self, source, target, detour_range=0.02):
    """
    Generate path with a small detour.
    
    Args:
        source: Starting position
        target: Target position
        detour_range: Range to search for detour point (default: 0.02)
    
    Returns:
        Path as list of (x, y) tuples, or None if failed
    """
    # Find a point near the middle of the path
    mid_x = (source[0] + target[0]) / 2
    mid_y = (source[1] + target[1]) / 2
    
    # Search for nearby nodes
    candidates = self.search(
        mid_x - detour_range, mid_x + detour_range,
        mid_y - detour_range, mid_y + detour_range
    )
    
    if candidates:
        # Pick a random candidate as detour point
        detour_point = random.choice(candidates)
        
        # Generate path: source -> detour -> target
        path1 = self.shortest_path(source, detour_point)
        path2 = self.shortest_path(detour_point, target)
        
        if path1 and path2:
            # Combine paths (remove duplicate detour point)
            return path1[:-1] + path2
```

---

### Step 3: Multiple Path Generation Method

**File:** `src/routine/layout.py`

```python
def generate_paths(self, source, target, num_paths=3, enabled=True):
    """
    Generate multiple paths from source to target.
    
    Args:
        source: Starting position (x, y)
        target: Target position (x, y)
        num_paths: Number of paths to generate (default: 3, max: 5)
        enabled: Whether path variation is enabled
    
    Returns:
        List of paths, each path is a list of (x, y) tuples.
        Paths are sorted by length (shortest first).
        If enabled=False or only one path available, returns [shortest_path]
    """
    if not enabled:
        # Fallback to shortest path only
        return [self.shortest_path(source, target)]
    
    paths = []
    
    # Validate num_paths
    num_paths = max(1, min(num_paths, 5))  # Between 1 and 5
    
    # Strategy 0: Generate shortest path (baseline)
    shortest = self.shortest_path(source, target)
    if not shortest:
        return []
    paths.append(shortest)
    
    # Strategy 1: Prefer horizontal movement first
    if num_paths > 1:
        path_h = self._path_with_preference(source, target, prefer_horizontal=True)
        if path_h and not self._is_duplicate_path(path_h, shortest):
            paths.append(path_h)
    
    # Strategy 2: Prefer vertical movement first
    if num_paths > 2:
        path_v = self._path_with_preference(source, target, prefer_horizontal=False)
        if path_v and not self._is_duplicate_path(path_v, shortest):
            paths.append(path_v)
    
    # Strategy 3: Weighted heuristic (1.1x)
    if num_paths > 3:
        path_w1 = self._path_with_weighted_heuristic(source, target, weight=1.1)
        if path_w1 and not self._is_duplicate_path(path_w1, shortest):
            paths.append(path_w1)
    
    # Strategy 4: Path with detour
    if num_paths > 4:
        path_d = self._path_with_detour(source, target)
        if path_d and not self._is_duplicate_path(path_d, shortest):
            paths.append(path_d)
    
    # Remove duplicates and sort by length
    unique_paths = self._remove_duplicate_paths(paths)
    unique_paths.sort(key=lambda p: self._calculate_path_length(p))
    
    # Return up to num_paths unique paths
    return unique_paths[:num_paths]
```

---

### Step 4: Modify Move Class to Use Path Variation

**File:** `src/routine/components.py` - `Move.main()`

#### 4.1: Add Path Variation Logic

```python
# In Move.main(), replace:
path = config.layout.shortest_path(config.player_pos, self.target)

# With:
if path_variation_enabled:
    # Generate multiple paths
    paths = config.layout.generate_paths(
        config.player_pos, 
        self.target, 
        num_paths=path_count,
        enabled=True
    )
    
    if len(paths) > 1:
        # Weighted random selection
        # Shortest path: 60%, Second: 30%, Third: 10%
        weights = [0.6, 0.3, 0.1][:len(paths)]
        # Normalize weights
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Select path randomly with weights
        path = random.choices(paths, weights=weights, k=1)[0]
        
        # Log path selection
        path_index = paths.index(path)
        path_length = len(path)
        action_log.info("🔀 Path Variation: Selected path %d of %d (length=%d)", 
                       path_index + 1, len(paths), path_length)
    else:
        # Fallback to shortest path
        path = paths[0] if paths else config.layout.shortest_path(config.player_pos, self.target)
else:
    # Use shortest path only
    path = config.layout.shortest_path(config.player_pos, self.target)
```

---

### Step 5: Add Configuration

**File:** `src/routine/routine.py` - `Routine.__init__()`

```python
# Path Variation
self.path_variation_enabled = False  # Enable/disable path variation
self.path_count = 3  # Number of paths to generate (2-5)
self.path_selection_weighted = True  # Use weighted selection
```

**File:** `src/routine/components.py` - `Move.__init__()`

```python
# Load path variation settings from routine
self.path_variation_enabled = getattr(config.routine, 'path_variation_enabled', False)
self.path_count = getattr(config.routine, 'path_count', 3)
```

---

### Step 6: GUI Settings Integration

**File:** `src/gui/settings/routine_randomization.py`

Add to `RoutineRandomization` class:

```python
# Path Variation Panel
self.path_variation_frame = LabelFrame(self, 'Path Variation')
self.path_variation_frame.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=5)

# Enable checkbox
self.path_variation_var = tk.BooleanVar(value=path_variation_enabled)
tk.Checkbutton(
    self.path_variation_frame,
    variable=self.path_variation_var,
    text='Enable Path Variation',
    command=self._on_path_variation_change
).pack(side=tk.TOP, anchor='w', padx=5, pady=2)

# Path count spinbox
count_row = Frame(self.path_variation_frame)
count_row.pack(side=tk.TOP, fill='x', expand=True, padx=5, pady=(0, 5))
tk.Label(count_row, text='Number of Paths:').pack(side=tk.LEFT, padx=(0, 10))
self.path_count_var = tk.IntVar(value=path_count)
tk.Spinbox(
    count_row,
    from_=2,
    to=5,
    textvariable=self.path_count_var,
    command=self._on_path_variation_change,
    width=5
).pack(side=tk.LEFT)
```

**Settings Keys:**
- `Path Variation Enabled` (Boolean)
- `Path Count` (Integer 2-5)

---

## ⚠️ Compatibility & Risk Assessment

### Compatibility với Codebase

✅ **Phù hợp:**
- Dựa trên `shortest_path()` hiện có
- Không thay đổi core pathfinding logic
- Có thể enable/disable dễ dàng
- Fallback về shortest path nếu fail

⚠️ **Cần lưu ý:**
- `_path_with_preference()` cần modify `push_neighbors` logic (có thể phức tạp)
- `_path_with_weighted_heuristic()` cần modify heuristic calculation
- `_path_with_detour()` cần generate 2 paths và combine (có thể chậm hơn)

### Risk Assessment

**Low Risk:**
- ✅ Fallback về shortest path nếu không generate được alternative
- ✅ Có thể disable dễ dàng
- ✅ Không ảnh hưởng đến existing functionality

**Medium Risk:**
- ⚠️ Alternative path generation có thể fail (không tìm được path)
- ⚠️ Detour path có thể dài hơn, mất thời gian hơn
- ⚠️ Performance: Generate multiple paths có thể chậm hơn

**Mitigation:**
- Always fallback to shortest path
- Limit number of paths (max 5)
- Cache paths if same source/target
- Add timeout for path generation

---

## 🧪 Testing Strategy

### Unit Tests
- [ ] Test `_calculate_path_length()` với various paths
- [ ] Test `_is_duplicate_path()` với duplicate và non-duplicate paths
- [ ] Test `_remove_duplicate_paths()` với mixed paths
- [ ] Test `generate_paths()` với different num_paths values
- [ ] Test fallback khi không generate được alternative paths

### Integration Tests
- [ ] Test với `Move.main()` để verify path selection
- [ ] Test với different source/target combinations
- [ ] Test với enabled/disabled path variation
- [ ] Test weighted selection distribution
- [ ] Test performance (should not be too slow)

### Real-world Tests
- [ ] Test với routine có nhiều points
- [ ] Test với 1-floor và 2-floor routines
- [ ] Test long-running sessions
- [ ] Verify paths không làm bot stuck
- [ ] Verify paths vẫn reach target đúng

---

## 📊 Expected Results

### Benefits
- ✅ **Variation**: Mỗi lần move có thể có path khác nhau
- ✅ **Anti-detection**: Khó detect với multiple paths
- ✅ **Human-like**: Không luôn đi shortest path

### Trade-offs
- ⚠️ **Performance**: Generate multiple paths có thể chậm hơn (10-20% overhead)
- ⚠️ **Complexity**: Code phức tạp hơn
- ⚠️ **Path Quality**: Alternative paths có thể dài hơn shortest path

---

## 🎯 Implementation Priority

**Priority:** Medium ⭐⭐⭐⭐

**Reasons:**
- Tạo variation lớn trong movement
- Phù hợp với codebase hiện tại
- Có thể implement incrementally
- Risk manageable với fallback

**Estimated Time:** 4-6 hours

**Dependencies:**
- None (có thể implement độc lập)

---

## 📝 Implementation Checklist

### Phase 1: Core Methods (2 hours)
- [ ] Implement `_calculate_path_length()`
- [ ] Implement `_is_duplicate_path()`
- [ ] Implement `_remove_duplicate_paths()`
- [ ] Test core methods

### Phase 2: Alternative Path Strategies (2-3 hours)
- [ ] Implement `_path_with_preference()` (horizontal/vertical)
- [ ] Implement `_path_with_weighted_heuristic()`
- [ ] Implement `_path_with_detour()`
- [ ] Test each strategy individually

### Phase 3: Multiple Path Generation (1 hour)
- [ ] Implement `generate_paths()`
- [ ] Test với different num_paths
- [ ] Test fallback logic

### Phase 4: Integration (1 hour)
- [ ] Modify `Move.main()` to use path variation
- [ ] Add configuration to `Routine` class
- [ ] Test integration

### Phase 5: GUI Settings (1 hour)
- [ ] Add GUI settings panel
- [ ] Add settings keys
- [ ] Test GUI integration

### Phase 6: Testing & Tuning (1-2 hours)
- [ ] Unit tests
- [ ] Integration tests
- [ ] Real-world testing
- [ ] Performance tuning

---

## 🔄 Alternative Approaches (Nếu Approach 1 không work)

### Approach 2: Simple Path Perturbation
- Thêm small random offsets vào các points trong path
- Đơn giản hơn nhưng ít variation hơn

### Approach 3: Path Caching với Variation
- Cache multiple paths cho common routes
- Chọn random từ cache
- Nhanh hơn nhưng cần pre-compute

---

## 📌 Notes

1. **Start Simple**: Implement `_path_with_weighted_heuristic()` trước (dễ nhất)
2. **Incremental**: Add strategies từng cái một và test
3. **Fallback**: Luôn có fallback về shortest path
4. **Performance**: Monitor performance, có thể cần optimize
5. **Testing**: Test kỹ với different routines và maps

