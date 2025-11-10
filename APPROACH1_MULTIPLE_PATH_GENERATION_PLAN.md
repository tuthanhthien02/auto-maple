# 🗺️ Approach 1: Multiple Path Generation - Detailed Implementation Plan

## 🎯 **MỤC TIÊU**

Implement **Approach 1: Multiple Path Generation** để tạo nhiều paths khác nhau đến cùng một target, giúp:
1. **Tránh pattern detection** - Không luôn dùng cùng một path
2. **Human-like behavior** - Humans không luôn đi shortest path
3. **Variation trong movement** - Mỗi lần di chuyển có thể có path khác nhau
4. **Anti-detection** - Khó detect hơn với multiple paths

---

## 📋 **PHÂN TÍCH HIỆN TRẠNG**

### **Current Pathfinding System:**

**File:** `src/routine/layout.py` - `Layout.shortest_path()`

**Current Behavior:**
- ✅ Sử dụng A* algorithm để tìm shortest path
- ✅ Luôn trả về cùng một path cho cùng source và target
- ✅ Path được lưu trong `config.path` và vẽ trên minimap
- ✅ Path được sử dụng trong `Move.main()` để di chuyển

**Current Code Structure:**
```python
def shortest_path(self, source, target):
    # A* search algorithm
    # - Uses fringe (priority queue)
    # - Uses vertices, distances, edge_to lists
    # - push_neighbors() adds candidates
    # - push_best() picks closest point
    # - Returns path from source to target
```

---

## 🎯 **APPROACH 1: MULTIPLE PATH GENERATION**

### **Overview:**

1. **Generate Multiple Paths:** Tạo 3-5 paths khác nhau
2. **Alternative Path Strategies:** Sử dụng các strategies khác nhau để generate paths
3. **Path Selection:** Chọn random một path với weighted probability

---

## 📝 **IMPLEMENTATION STEPS**

### **Step 1.1: Generate Multiple Paths Method**

**File:** `src/routine/layout.py` - `Layout` class

**New Method:** `generate_paths(source, target, num_paths=3)`

**Purpose:**
- Generate nhiều paths từ source đến target
- Sử dụng các strategies khác nhau để tạo variation
- Trả về list of paths, sorted by length

**Implementation:**
```python
def generate_paths(self, source, target, num_paths=3):
    """
    Generate multiple paths from source to target.
    Returns a list of paths, sorted by length (shortest first).
    
    Args:
        source: Starting position (x, y)
        target: Target position (x, y)
        num_paths: Number of paths to generate (default: 3, max: 5)
    
    Returns:
        List of paths, each path is a list of (x, y) tuples.
        Paths are sorted by length (shortest first).
    """
    paths = []
    
    # Validate num_paths
    num_paths = max(1, min(num_paths, 5))  # Between 1 and 5
    
    # Strategy 0: Generate shortest path (baseline)
    shortest = self.shortest_path(source, target)
    paths.append(shortest)
    
    # Strategy 1-4: Generate alternative paths
    for i in range(1, num_paths):
        alt_path = self._generate_alternative_path(source, target, strategy=i)
        if alt_path and alt_path != shortest:
            # Check if path is different (not duplicate)
            if not self._is_duplicate_path(alt_path, paths):
                paths.append(alt_path)
    
    # Remove duplicates and sort by length
    unique_paths = self._remove_duplicate_paths(paths)
    unique_paths.sort(key=lambda p: self._calculate_path_length(p))
    
    # Return up to num_paths unique paths
    return unique_paths[:num_paths]
```

**Key Features:**
- ✅ Generate shortest path first (baseline)
- ✅ Generate alternative paths với các strategies khác nhau
- ✅ Remove duplicate paths
- ✅ Sort by path length (shortest first)
- ✅ Return up to `num_paths` unique paths

---

### **Step 1.2: Alternative Path Generation**

**File:** `src/routine/layout.py` - `Layout` class

**New Method:** `_generate_alternative_path(source, target, strategy)`

**Purpose:**
- Generate alternative paths với các strategies khác nhau
- Mỗi strategy tạo paths với characteristics khác nhau

**Strategies:**

#### **Strategy 1: Prefer Horizontal Movement First**
- Ưu tiên di chuyển horizontal trước khi vertical
- Tạo paths đi ngang nhiều hơn

#### **Strategy 2: Prefer Vertical Movement First**
- Ưu tiên di chuyển vertical trước khi horizontal
- Tạo paths đi dọc nhiều hơn

#### **Strategy 3: Weighted Heuristic (Slightly Longer)**
- Sử dụng weighted heuristic (1.1x - 1.2x)
- Tạo paths dài hơn một chút nhưng khác biệt

#### **Strategy 4: Reverse Search Order**
- Đảo ngược thứ tự search (vertical trước, horizontal sau)
- Tạo paths với pattern khác

**Implementation:**
```python
def _generate_alternative_path(self, source, target, strategy=1):
    """
    Generate an alternative path using different search strategy.
    
    Args:
        source: Starting position (x, y)
        target: Target position (x, y)
        strategy: Strategy to use (1-4)
            - 1: Prefer horizontal movement first
            - 2: Prefer vertical movement first
            - 3: Weighted heuristic (1.1x - 1.2x)
            - 4: Reverse search order
    
    Returns:
        Alternative path as list of (x, y) tuples, or None if failed
    """
    if strategy == 1:
        # Strategy 1: Prefer horizontal movement first
        return self._path_with_preference(source, target, prefer_horizontal=True)
    elif strategy == 2:
        # Strategy 2: Prefer vertical movement first
        return self._path_with_preference(source, target, prefer_horizontal=False)
    elif strategy == 3:
        # Strategy 3: Weighted heuristic (slightly longer paths)
        weight = 1.1 + (strategy - 3) * 0.05  # 1.1x to 1.2x
        return self._path_with_weighted_heuristic(source, target, weight=weight)
    elif strategy == 4:
        # Strategy 4: Reverse search order
        return self._path_with_reverse_order(source, target)
    else:
        # Fallback to shortest path
        return self.shortest_path(source, target)
```

---

### **Step 1.3: Helper Methods for Alternative Paths**

#### **Method 1: Path with Preference (Horizontal/Vertical)**

**File:** `src/routine/layout.py` - `Layout` class

**New Method:** `_path_with_preference(source, target, prefer_horizontal=True)`

**Purpose:**
- Generate path với preference cho horizontal hoặc vertical movement
- Modify A* algorithm để prefer một direction trước

**Implementation:**
```python
def _path_with_preference(self, source, target, prefer_horizontal=True):
    """
    Generate path with preference for horizontal or vertical movement.
    
    Args:
        source: Starting position (x, y)
        target: Target position (x, y)
        prefer_horizontal: If True, prefer horizontal movement first
    
    Returns:
        Path as list of (x, y) tuples
    """
    # Similar to shortest_path() but modify push_neighbors()
    # to prefer horizontal or vertical movement first
    
    fringe = []
    vertices = [source]
    distances = [0]
    edge_to = [0]
    
    def push_neighbors(index):
        point = vertices[index]
        
        def push_best(nodes, is_horizontal):
            if nodes:
                points = [tuple(n) for n in nodes]
                
                # If prefer_horizontal and this is horizontal, boost score
                # If prefer_horizontal and this is vertical, reduce score
                # Vice versa for vertical preference
                
                if prefer_horizontal and is_horizontal:
                    # Boost horizontal candidates (reduce distance by 10%)
                    scored_points = []
                    for p in points:
                        base_dist = utils.distance(point, p)
                        dist_to_target = utils.distance(p, target)
                        # Reduce distance by 10% to prefer horizontal
                        scored_dist = base_dist * 0.9 + dist_to_target
                        scored_points.append((scored_dist, p))
                    scored_points.sort(key=lambda x: x[0])
                    closest = scored_points[0][1]
                elif not prefer_horizontal and not is_horizontal:
                    # Boost vertical candidates (reduce distance by 10%)
                    scored_points = []
                    for p in points:
                        base_dist = utils.distance(point, p)
                        dist_to_target = utils.distance(p, target)
                        # Reduce distance by 10% to prefer vertical
                        scored_dist = base_dist * 0.9 + dist_to_target
                        scored_points.append((scored_dist, p))
                    scored_points.sort(key=lambda x: x[0])
                    closest = scored_points[0][1]
                else:
                    # Normal selection (no preference boost)
                    closest = utils.closest_point(points, target)
                
                # Push to fringe
                distance = distances[index] + utils.distance(point, closest)
                heuristic = distance + utils.distance(closest, target)
                heappush(fringe, (heuristic, len(vertices)))
                
                vertices.append(closest)
                distances.append(distance)
                edge_to.append(index)
        
        x_error = (target[0] - point[0])
        y_error = (target[1] - point[1])
        delta = settings.move_tolerance / math.sqrt(2)
        
        # Push neighbors based on preference
        if prefer_horizontal:
            # Push horizontal first
            if abs(x_error) > settings.move_tolerance:
                # ... horizontal teleport code ...
                push_best(candidates, is_horizontal=True)
            if abs(y_error) > settings.move_tolerance:
                # ... vertical teleport code ...
                push_best(candidates, is_horizontal=False)
        else:
            # Push vertical first
            if abs(y_error) > settings.move_tolerance:
                # ... vertical teleport code ...
                push_best(candidates, is_horizontal=False)
            if abs(x_error) > settings.move_tolerance:
                # ... horizontal teleport code ...
                push_best(candidates, is_horizontal=True)
    
    # Perform A* search
    i = 0
    while utils.distance(vertices[i], target) > settings.move_tolerance:
        push_neighbors(i)
        if len(fringe) == 0:
            break
        i = heappop(fringe)[1]
    
    # Extract path
    path = [target]
    while i != 0:
        path.append(vertices[i])
        i = edge_to[i]
    path.append(source)
    path = list(reversed(path))
    
    return path
```

#### **Method 2: Path with Weighted Heuristic**

**File:** `src/routine/layout.py` - `Layout` class

**New Method:** `_path_with_weighted_heuristic(source, target, weight=1.1)`

**Purpose:**
- Generate path với weighted heuristic
- Tạo paths dài hơn một chút nhưng khác biệt

**Implementation:**
```python
def _path_with_weighted_heuristic(self, source, target, weight=1.1):
    """
    Generate path with weighted heuristic (prefer slightly longer paths).
    
    Args:
        source: Starting position (x, y)
        target: Target position (x, y)
        weight: Weight factor for heuristic (1.1 = 10% longer paths)
    
    Returns:
        Path as list of (x, y) tuples
    """
    # Similar to shortest_path() but modify heuristic calculation
    # Multiply heuristic by weight to prefer slightly longer paths
    
    fringe = []
    vertices = [source]
    distances = [0]
    edge_to = [0]
    
    def push_neighbors(index):
        point = vertices[index]
        
        def push_best(nodes):
            if nodes:
                points = [tuple(n) for n in nodes]
                
                # Use weighted heuristic (prefer slightly longer paths)
                scored_points = []
                for p in points:
                    base_dist = utils.distance(point, p)
                    dist_to_target = utils.distance(p, target)
                    # Apply weight to heuristic (not distance)
                    heuristic = (base_dist + dist_to_target) * weight
                    scored_points.append((heuristic, p))
                
                scored_points.sort(key=lambda x: x[0])
                closest = scored_points[0][1]
                
                # Push to fringe (use actual distance, not weighted)
                distance = distances[index] + utils.distance(point, closest)
                heuristic = distance + utils.distance(closest, target) * weight
                heappush(fringe, (heuristic, len(vertices)))
                
                vertices.append(closest)
                distances.append(distance)
                edge_to.append(index)
        
        # ... rest of push_neighbors code (same as shortest_path) ...
    
    # Perform A* search (same as shortest_path)
    # ... extract path ...
    
    return path
```

#### **Method 3: Path with Reverse Order**

**File:** `src/routine/layout.py` - `Layout` class

**New Method:** `_path_with_reverse_order(source, target)`

**Purpose:**
- Generate path với reverse search order
- Đảo ngược thứ tự search để tạo paths khác

**Implementation:**
```python
def _path_with_reverse_order(self, source, target):
    """
    Generate path with reverse search order (vertical first, then horizontal).
    
    Args:
        source: Starting position (x, y)
        target: Target position (x, y)
    
    Returns:
        Path as list of (x, y) tuples
    """
    # Similar to _path_with_preference but always push vertical first
    return self._path_with_preference(source, target, prefer_horizontal=False)
```

---

### **Step 1.4: Helper Methods for Path Management**

#### **Method 1: Calculate Path Length**

**File:** `src/routine/layout.py` - `Layout` class

**New Method:** `_calculate_path_length(path)`

**Purpose:**
- Calculate total length of a path
- Used for sorting paths by length

**Implementation:**
```python
def _calculate_path_length(self, path):
    """
    Calculate total length of a path.
    
    Args:
        path: List of (x, y) tuples
    
    Returns:
        Total path length (float)
    """
    if len(path) < 2:
        return 0.0
    
    total_length = 0.0
    for i in range(len(path) - 1):
        total_length += utils.distance(path[i], path[i + 1])
    
    return total_length
```

#### **Method 2: Check if Path is Duplicate**

**File:** `src/routine/layout.py` - `Layout` class

**New Method:** `_is_duplicate_path(path, paths)`

**Purpose:**
- Check if a path is duplicate of existing paths
- Compare paths point-by-point

**Implementation:**
```python
def _is_duplicate_path(self, path, paths):
    """
    Check if a path is duplicate of existing paths.
    
    Args:
        path: Path to check (list of (x, y) tuples)
        paths: List of existing paths
    
    Returns:
        True if duplicate, False otherwise
    """
    if not path or not paths:
        return False
    
    path_tuple = tuple(path)
    for existing_path in paths:
        if tuple(existing_path) == path_tuple:
            return True
    
    return False
```

#### **Method 3: Remove Duplicate Paths**

**File:** `src/routine/layout.py` - `Layout` class

**New Method:** `_remove_duplicate_paths(paths)`

**Purpose:**
- Remove duplicate paths from a list
- Keep only unique paths

**Implementation:**
```python
def _remove_duplicate_paths(self, paths):
    """
    Remove duplicate paths from a list.
    
    Args:
        paths: List of paths
    
    Returns:
        List of unique paths
    """
    unique_paths = []
    seen = set()
    
    for path in paths:
        path_tuple = tuple(path)
        if path_tuple not in seen:
            seen.add(path_tuple)
            unique_paths.append(path)
    
    return unique_paths
```

---

### **Step 1.5: Path Selection in Move Command**

**File:** `src/routine/components.py` - `Move` class

**Modify:** `Move.main()`

**Purpose:**
- Generate multiple paths
- Select random path with weighted probability
- Use selected path for movement

**Implementation:**
```python
def main(self):
    import random
    from src.common.logger import get_action_logger
    action_log = get_action_logger()
    
    # Unique Pathfinding - Approach 1: Multiple Path Generation
    # Generate multiple paths and select one randomly
    num_paths = 3  # Generate 3 paths
    
    # Generate multiple paths
    paths = config.layout.generate_paths(
        config.player_pos, 
        self.target, 
        num_paths=num_paths
    )
    
    # Select path based on weighted random selection
    # Weighted: 60% shortest, 30% second, 10% third (if available)
    if len(paths) > 1:
        # Calculate weights based on path length
        # Shorter paths get higher weights
        weights = []
        if len(paths) >= 1:
            weights.append(0.6)  # 60% for shortest
        if len(paths) >= 2:
            weights.append(0.3)  # 30% for second
        if len(paths) >= 3:
            weights.append(0.1)  # 10% for third
        # Normalize weights if we have fewer paths
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Select path randomly with weights
        path = random.choices(paths, weights=weights, k=1)[0]
        
        # Log path selection
        path_index = paths.index(path)
        path_length = len(path)
        path_distance = self._calculate_path_distance(path)
        action_log.info("🔀 Path Selection: Selected path %d of %d (length=%d, distance=%.3f)", 
                       path_index + 1, len(paths), path_length, path_distance)
    else:
        # Fallback to shortest path (only one path available)
        path = paths[0]
        action_log.debug("Path Selection: Using shortest path (only one path available)")
    
    # Store selected path in config for minimap display
    config.path = path.copy()
    
    # Use selected path for movement (existing code)
    counter = self.max_steps
    for i, point in enumerate(path):
        # ... existing movement code ...
```

**Helper Method:**
```python
def _calculate_path_distance(self, path):
    """Calculate total distance of a path."""
    if len(path) < 2:
        return 0.0
    
    total_distance = 0.0
    for i in range(len(path) - 1):
        total_distance += utils.distance(path[i], path[i + 1])
    
    return total_distance
```

---

## 📊 **IMPLEMENTATION SUMMARY**

### **Files to Modify:**

1. **`src/routine/layout.py`**
   - Add `generate_paths()` method
   - Add `_generate_alternative_path()` method
   - Add `_path_with_preference()` method
   - Add `_path_with_weighted_heuristic()` method
   - Add `_path_with_reverse_order()` method
   - Add `_calculate_path_length()` method
   - Add `_is_duplicate_path()` method
   - Add `_remove_duplicate_paths()` method

2. **`src/routine/components.py`**
   - Modify `Move.main()` to use `generate_paths()`
   - Add path selection logic
   - Add logging for path selection
   - Add `_calculate_path_distance()` helper method

### **New Dependencies:**
- `import random` (already imported in components.py)
- No new external dependencies

---

## 🧪 **TESTING PLAN**

### **Unit Testing:**

1. **Test `generate_paths()`:**
   - Test with various sources/targets
   - Test with num_paths=1, 2, 3, 5
   - Verify paths are different
   - Verify paths are sorted by length
   - Verify no duplicate paths

2. **Test `_generate_alternative_path()`:**
   - Test each strategy (1-4)
   - Verify paths are valid (reach target)
   - Verify paths are different from shortest path

3. **Test Helper Methods:**
   - Test `_calculate_path_length()`
   - Test `_is_duplicate_path()`
   - Test `_remove_duplicate_paths()`

### **Integration Testing:**

1. **Test Movement:**
   - Test movement với multiple paths
   - Test movement với routine thực tế
   - Verify bot vẫn reach targets chính xác
   - Check performance impact

2. **Test Path Selection:**
   - Test weighted random selection
   - Verify path selection distribution (60/30/10)
   - Verify paths are different each time

### **Behavior Testing:**

1. **Test Path Variation:**
   - Verify paths are different each time
   - Verify path selection works correctly
   - Check path variation doesn't cause issues

2. **Test Anti-Detection:**
   - Monitor path patterns
   - Evaluate anti-detection improvement
   - Check for any movement problems

---

## ⚠️ **RISK ASSESSMENT**

### **Low Risk:**
- ✅ Helper methods (path length, duplicate detection)
- ✅ Path selection logic (weighted random)

### **Medium Risk:**
- ⚠️ Alternative path generation (modify A* algorithm)
  - Need to verify alternative paths are valid
  - Need to ensure paths don't cause movement issues
  - Need to test with various map layouts

### **High Risk:**
- ❌ None (all components are low-medium risk)

---

## 📝 **IMPLEMENTATION ORDER**

### **Phase 1: Core Methods (2-3 hours)**
1. ✅ Implement `_calculate_path_length()`
2. ✅ Implement `_is_duplicate_path()`
3. ✅ Implement `_remove_duplicate_paths()`
4. ✅ Test helper methods

### **Phase 2: Alternative Path Generation (3-4 hours)**
1. ✅ Implement `_path_with_preference()`
2. ✅ Implement `_path_with_weighted_heuristic()`
3. ✅ Implement `_path_with_reverse_order()`
4. ✅ Implement `_generate_alternative_path()`
5. ✅ Test alternative path generation

### **Phase 3: Multiple Path Generation (1-2 hours)**
1. ✅ Implement `generate_paths()`
2. ✅ Test multiple path generation
3. ✅ Verify paths are unique and sorted

### **Phase 4: Path Selection (1 hour)**
1. ✅ Modify `Move.main()` to use `generate_paths()`
2. ✅ Add path selection logic
3. ✅ Add logging
4. ✅ Test path selection

### **Phase 5: Testing & Refinement (1-2 hours)**
1. ✅ Unit testing
2. ✅ Integration testing
3. ✅ Behavior testing
4. ✅ Performance testing
5. ✅ Refinement based on test results

**Total Time:** 8-12 hours
**Difficulty:** ⭐⭐ Medium

---

## 🎯 **EXPECTED RESULTS**

### **Before Implementation:**
- ❌ Always uses shortest path
- ❌ Predictable paths
- ❌ Pattern detection risk

### **After Implementation:**
- ✅ Multiple paths available (3 paths)
- ✅ Random path selection (weighted 60/30/10)
- ✅ Path variation each time
- ✅ Anti-detection improvement
- ✅ Human-like behavior (not always shortest path)

---

## 📚 **REFERENCES**

- **Plan Document:** `UNIQUE_PATHFINDING_PLAN.md`
- **Implementation Files:**
  - `src/routine/layout.py` (main implementation)
  - `src/routine/components.py` (path selection)

---

## 🚀 **NEXT STEPS**

1. **Review** plan này với user
2. **Start Implementation** với Phase 1 (Core Methods)
3. **Test thoroughly** sau mỗi phase
4. **Refine** based on test results
5. **Evaluate** results trước khi proceed to next phase

---

**Last Updated:** 2024
**Status:** 📋 Ready for Implementation

