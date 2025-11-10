# 🗺️ Unique Pathfinding - Detailed Implementation Plan

## 🎯 **MỤC TIÊU**

Thêm tính năng **Unique Pathfinding** để tạo nhiều paths khác nhau đến cùng một target, giúp:
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

**Issues:**
- ❌ **Predictable** - Luôn dùng cùng một path
- ❌ **No variation** - Không có alternate routes
- ❌ **Pattern detection risk** - Dễ detect với fixed paths

---

## 🎯 **UNIQUE PATHFINDING APPROACHES**

### **Approach 1: Multiple Path Generation** ⭐⭐⭐ **RECOMMENDED**

**Mục tiêu:** Generate nhiều paths và chọn random một path

#### **Step 1.1: Generate Multiple Paths**

**File:** `src/routine/layout.py` - `Layout` class

**Proposed:**
```python
def generate_paths(self, source, target, num_paths=3):
    """
    Generate multiple paths from source to target.
    Returns a list of paths, sorted by length (shortest first).
    
    Args:
        source: Starting position (x, y)
        target: Target position (x, y)
        num_paths: Number of paths to generate (default: 3)
    
    Returns:
        List of paths, each path is a list of (x, y) tuples
    """
    paths = []
    
    # Generate shortest path (baseline)
    shortest = self.shortest_path(source, target)
    paths.append(shortest)
    
    # Generate alternative paths by modifying search parameters
    for i in range(num_paths - 1):
        # Method 1: Add randomness to heuristic (prefer slightly longer paths)
        # Method 2: Skip some intermediate points
        # Method 3: Use different search strategies
        alt_path = self._generate_alternative_path(source, target, variation=i)
        if alt_path and alt_path != shortest:
            paths.append(alt_path)
    
    # Remove duplicates and sort by length
    unique_paths = []
    seen = set()
    for path in paths:
        path_tuple = tuple(path)
        if path_tuple not in seen:
            seen.add(path_tuple)
            unique_paths.append(path)
    
    # Sort by path length (shortest first)
    unique_paths.sort(key=lambda p: self._calculate_path_length(p))
    
    return unique_paths[:num_paths]
```

**Benefits:**
- ✅ Multiple paths available
- ✅ Can choose random path
- ✅ Maintains shortest path as option

**Risk:** ⭐ **MEDIUM** - Cần modify A* algorithm

**Time:** 3-4 giờ

---

#### **Step 1.2: Alternative Path Generation**

**File:** `src/routine/layout.py` - `Layout` class

**Proposed:**
```python
def _generate_alternative_path(self, source, target, variation=0):
    """
    Generate an alternative path by adding variation to search.
    
    Args:
        source: Starting position
        target: Target position
        variation: Variation factor (0-2)
    
    Returns:
        Alternative path as list of (x, y) tuples
    """
    # Method 1: Add randomness to heuristic (weighted A*)
    # Prefer paths that are slightly longer but different
    
    # Method 2: Skip intermediate points (direct movement)
    # Skip some points in the path to create shorter but different path
    
    # Method 3: Use different search order (prefer horizontal vs vertical)
    # Change the order of searching (horizontal first vs vertical first)
    
    # Implementation:
    # - Variation 0: Prefer horizontal movement first
    # - Variation 1: Prefer vertical movement first
    # - Variation 2: Add randomness to heuristic (10-20% longer paths)
    
    if variation == 0:
        # Prefer horizontal movement first
        return self._path_with_preference(source, target, prefer_horizontal=True)
    elif variation == 1:
        # Prefer vertical movement first
        return self._path_with_preference(source, target, prefer_horizontal=False)
    else:
        # Add randomness to heuristic (weighted A*)
        return self._path_with_weighted_heuristic(source, target, weight=1.1 + variation * 0.1)
```

**Benefits:**
- ✅ Different paths based on variation
- ✅ Maintains path validity
- ✅ Can generate multiple unique paths

**Risk:** ⭐ **MEDIUM** - Cần implement alternative search strategies

**Time:** 2-3 giờ

---

#### **Step 1.3: Path Selection Strategy**

**File:** `src/routine/components.py` - `Move` class

**Proposed:**
```python
def main(self):
    # Unique Pathfinding: Generate multiple paths and select one
    from src.common import config
    
    # Generate multiple paths
    paths = config.layout.generate_paths(config.player_pos, self.target, num_paths=3)
    
    # Select path based on strategy
    # Strategy 1: Random selection (50% shortest, 50% others)
    # Strategy 2: Weighted random (prefer shorter paths)
    # Strategy 3: Round-robin (cycle through paths)
    
    if len(paths) > 1:
        # Weighted random: 60% shortest, 30% second, 10% third
        weights = [0.6, 0.3, 0.1][:len(paths)]
        path = random.choices(paths, weights=weights, k=1)[0]
        action_log.debug("Unique Pathfinding: Selected path %d of %d (length=%.3f)", 
                        paths.index(path) + 1, len(paths), self._calculate_path_length(path))
    else:
        # Fallback to shortest path
        path = paths[0]
    
    # Use selected path for movement
    for i, point in enumerate(path):
        # ... existing movement code ...
```

**Benefits:**
- ✅ Random path selection
- ✅ Weighted towards shorter paths
- ✅ Variation trong movement

**Risk:** ⭐ **LOW** - Chỉ thay đổi path selection

**Time:** 1 giờ

---

### **Approach 2: Path Randomization** ⭐⭐ **ALTERNATIVE**

**Mục tiêu:** Thêm randomness vào path selection trong A* algorithm

#### **Step 2.1: Randomized Heuristic**

**File:** `src/routine/layout.py` - `Layout.shortest_path()`

**Proposed:**
```python
def shortest_path(self, source, target, randomize=False, variation=0.0):
    """
    Returns the shortest path from A to B using horizontal and vertical teleports.
    Can add randomization to create unique paths.
    
    Args:
        source: Starting position
        target: Target position
        randomize: Whether to randomize path selection
        variation: Variation factor (0.0-0.2, adds 0-20% randomness to heuristic)
    
    Returns:
        A list of all Nodes on the path in order.
    """
    # ... existing A* code ...
    
    def push_best(nodes):
        if nodes:
            points = [tuple(n) for n in nodes]
            
            if randomize and variation > 0:
                # Add randomness to distance calculation
                # Prefer points that are slightly farther but different
                import random
                scored_points = []
                for point in points:
                    base_distance = utils.distance(point, target)
                    # Add random variation (0-variation% of distance)
                    random_factor = 1.0 + random.uniform(-variation, variation)
                    scored_distance = base_distance * random_factor
                    scored_points.append((scored_distance, point))
                
                # Sort by scored distance and pick top candidate
                scored_points.sort(key=lambda x: x[0])
                closest = scored_points[0][1]
            else:
                # Original behavior: pick closest point
                closest = utils.closest_point(points, target)
            
            # ... rest of existing code ...
```

**Benefits:**
- ✅ Simple implementation
- ✅ Minimal changes to existing code
- ✅ Can generate different paths

**Risk:** ⭐ **LOW** - Chỉ thêm randomness vào heuristic

**Time:** 1-2 giờ

---

### **Approach 3: Path Point Variation** ⭐⭐ **ALTERNATIVE**

**Mục tiêu:** Thêm variation vào path points sau khi generate path

#### **Step 3.1: Path Point Randomization**

**File:** `src/routine/components.py` - `Move` class

**Proposed:**
```python
def _vary_path_points(self, path, variation=0.1):
    """
    Add variation to path points to create unique paths.
    
    Args:
        path: Original path (list of (x, y) tuples)
        variation: Variation factor (0.0-0.2, adds 0-20% variation to points)
    
    Returns:
        Varied path with slightly different points
    """
    if len(path) < 3:
        return path  # Too short to vary
    
    varied_path = [path[0]]  # Keep source
    
    for i in range(1, len(path) - 1):  # Skip source and target
        point = path[i]
        
        # Add small random variation to intermediate points
        # Only vary if point is not too close to source/target
        if random.random() < 0.3:  # 30% chance to vary each point
            # Small random offset (within move_tolerance)
            offset_x = random.uniform(-variation * settings.move_tolerance, 
                                     variation * settings.move_tolerance)
            offset_y = random.uniform(-variation * settings.move_tolerance, 
                                     variation * settings.move_tolerance)
            
            # Check if varied point is still valid (within layout)
            varied_point = (point[0] + offset_x, point[1] + offset_y)
            
            # Verify point is in layout (optional check)
            # if self._is_valid_point(varied_point):
            varied_path.append(varied_point)
        else:
            varied_path.append(point)
    
    varied_path.append(path[-1])  # Keep target
    
    return varied_path
```

**Benefits:**
- ✅ Simple implementation
- ✅ Can vary existing paths
- ✅ No changes to pathfinding algorithm

**Risk:** ⭐ **MEDIUM** - Cần verify varied points are valid

**Time:** 1-2 giờ

---

### **Approach 4: Path Caching with Variation** ⭐ **SIMPLE**

**Mục tiêu:** Cache paths và rotate through them

#### **Step 4.1: Path Cache with Rotation**

**File:** `src/routine/layout.py` - `Layout` class

**Proposed:**
```python
class Layout:
    def __init__(self):
        # ... existing code ...
        self.path_cache = {}  # Cache of paths: (source, target) -> [paths]
        self.path_index = {}  # Current index for each (source, target) pair
    
    def get_unique_path(self, source, target, use_cache=True):
        """
        Get a unique path by rotating through cached paths.
        
        Args:
            source: Starting position
            target: Target position
            use_cache: Whether to use cached paths
        
        Returns:
            A path from source to target
        """
        cache_key = (tuple(source), tuple(target))
        
        if use_cache and cache_key in self.path_cache:
            # Rotate through cached paths
            paths = self.path_cache[cache_key]
            if cache_key not in self.path_index:
                self.path_index[cache_key] = 0
            
            index = self.path_index[cache_key]
            path = paths[index]
            
            # Increment index for next time
            self.path_index[cache_key] = (index + 1) % len(paths)
            
            return path
        else:
            # Generate new path and cache it
            path = self.shortest_path(source, target)
            
            if use_cache:
                # Generate a few variations and cache them
                variations = [path]  # Start with shortest
                
                # Generate 2-3 alternative paths
                for i in range(2):
                    # Use different search strategies
                    alt_path = self._generate_alternative_path(source, target, variation=i)
                    if alt_path and alt_path != path:
                        variations.append(alt_path)
                
                self.path_cache[cache_key] = variations
                self.path_index[cache_key] = 0
            
            return path
```

**Benefits:**
- ✅ Simple implementation
- ✅ Caches paths for performance
- ✅ Rotates through paths

**Risk:** ⭐ **LOW** - Minimal changes

**Time:** 1-2 giờ

---

## 📊 **IMPLEMENTATION PRIORITY**

### **Priority 1: Approach 1 (Multiple Path Generation)** ⭐⭐⭐ **RECOMMENDED**

**Why:**
- ✅ Most flexible (multiple paths available)
- ✅ Best anti-detection (truly unique paths)
- ✅ Can combine with other approaches
- ✅ Maintains shortest path option

**Steps:**
1. Step 1.1: Generate Multiple Paths
2. Step 1.2: Alternative Path Generation
3. Step 1.3: Path Selection Strategy

**Time:** 5-8 giờ
**Difficulty:** ⭐⭐ Medium

---

### **Priority 2: Approach 2 (Path Randomization)** ⭐⭐ **ALTERNATIVE**

**Why:**
- ✅ Simple implementation
- ✅ Minimal changes to existing code
- ✅ Can generate different paths

**Steps:**
1. Step 2.1: Randomized Heuristic

**Time:** 1-2 giờ
**Difficulty:** ⭐ Easy-Medium

---

### **Priority 3: Approach 3 (Path Point Variation)** ⭐⭐ **ALTERNATIVE**

**Why:**
- ✅ Simple implementation
- ✅ Can vary existing paths
- ✅ No changes to pathfinding algorithm

**Steps:**
1. Step 3.1: Path Point Randomization

**Time:** 1-2 giờ
**Difficulty:** ⭐ Easy

---

### **Priority 4: Approach 4 (Path Caching)** ⭐ **SIMPLE**

**Why:**
- ✅ Simplest implementation
- ✅ Good performance (caching)
- ✅ Rotates through paths

**Steps:**
1. Step 4.1: Path Cache with Rotation

**Time:** 1-2 giờ
**Difficulty:** ⭐ Easy

---

## ⚠️ **RISK ASSESSMENT**

### **Low Risk:**
- ✅ Approach 2: Path Randomization (minimal changes)
- ✅ Approach 3: Path Point Variation (post-processing)
- ✅ Approach 4: Path Caching (simple caching)

### **Medium Risk:**
- ⚠️ Approach 1: Multiple Path Generation (modify A* algorithm)
  - Need to verify alternative paths are valid
  - Need to ensure paths don't cause movement issues

### **High Risk:**
- ❌ None (tất cả approaches đều low-medium risk)

---

## 🎯 **RECOMMENDED APPROACH**

### **Option 1: Hybrid Approach (Recommended)** ⭐⭐⭐

**Steps:**
1. ✅ **Approach 2: Path Randomization** (Quick win - 1-2h)
   - Add randomness to heuristic
   - Simple implementation
   - Immediate benefit

2. ✅ **Approach 4: Path Caching** (Enhancement - 1-2h)
   - Cache paths with variation
   - Rotate through paths
   - Better performance

3. ⏳ **Approach 1: Multiple Path Generation** (Advanced - 5-8h)
   - Generate multiple paths
   - Best anti-detection
   - Most flexible

**Result:**
- Risk: LOW-MEDIUM
- Time: 7-12 giờ (phased implementation)
- Difficulty: ⭐⭐ Medium
- Benefit: VERY HIGH

---

### **Option 2: Simple Start**

**Steps:**
1. ✅ **Approach 2: Path Randomization** (1-2h)
2. ✅ **Approach 3: Path Point Variation** (1-2h)

**Result:**
- Risk: LOW
- Time: 2-4 giờ
- Difficulty: ⭐ Easy
- Benefit: MEDIUM-HIGH

---

### **Option 3: Full Implementation**

**Steps:**
1. ✅ **Approach 1: Multiple Path Generation** (5-8h)
2. ✅ **Approach 2: Path Randomization** (1-2h)
3. ✅ **Approach 3: Path Point Variation** (1-2h)
4. ✅ **Approach 4: Path Caching** (1-2h)

**Result:**
- Risk: MEDIUM
- Time: 8-14 giờ
- Difficulty: ⭐⭐ Medium
- Benefit: VERY HIGH

---

## 📝 **IMPLEMENTATION DETAILS**

### **Step 1: Path Randomization (Quick Win)**

**File:** `src/routine/layout.py`

**Changes:**
1. Add `randomize` parameter to `shortest_path()`
2. Add randomness to heuristic calculation
3. Add variation factor (0.0-0.2)

**Code:**
```python
def shortest_path(self, source, target, randomize=False, variation=0.1):
    # ... existing code ...
    
    def push_best(nodes):
        if nodes:
            points = [tuple(n) for n in nodes]
            
            if randomize and variation > 0:
                # Add randomness to distance calculation
                scored_points = []
                for point in points:
                    base_distance = utils.distance(point, target)
                    random_factor = 1.0 + random.uniform(-variation, variation)
                    scored_distance = base_distance * random_factor
                    scored_points.append((scored_distance, point))
                
                scored_points.sort(key=lambda x: x[0])
                closest = scored_points[0][1]
            else:
                closest = utils.closest_point(points, target)
            
            # ... rest of code ...
```

---

### **Step 2: Path Selection in Move**

**File:** `src/routine/components.py` - `Move.main()`

**Changes:**
1. Add path randomization option
2. Select path with variation

**Code:**
```python
def main(self):
    # Unique Pathfinding: Randomize path selection
    import random
    
    # 70% chance to use randomized path, 30% shortest path
    use_randomized = random.random() < 0.7
    
    if use_randomized:
        # Generate path with randomization (10-15% variation)
        variation = random.uniform(0.10, 0.15)
        path = config.layout.shortest_path(
            config.player_pos, 
            self.target, 
            randomize=True, 
            variation=variation
        )
        action_log.debug("Unique Pathfinding: Using randomized path (variation=%.2f)", variation)
    else:
        # Use shortest path (30% of time)
        path = config.layout.shortest_path(config.player_pos, self.target)
        action_log.debug("Unique Pathfinding: Using shortest path")
    
    # ... rest of movement code ...
```

---

## 🧪 **TESTING PLAN**

### **Step 1: Unit Testing**
- Test path generation với various sources/targets
- Test path randomization với various variations
- Verify paths are valid (reach target)
- Check path lengths are reasonable

### **Step 2: Integration Testing**
- Test movement với randomized paths
- Test movement với routine thực tế
- Verify bot vẫn reach targets chính xác
- Check performance impact

### **Step 3: Behavior Testing**
- Verify paths are different each time
- Check path variation doesn't cause issues
- Monitor for any movement problems
- Evaluate anti-detection improvement

---

## 📊 **SUMMARY**

### **Current State:**
- ❌ Fixed pathfinding (always shortest path)
- ❌ Predictable paths
- ❌ Pattern detection risk

### **Target State:**
- ✅ Multiple path generation
- ✅ Randomized path selection
- ✅ Path variation
- ✅ Anti-detection improvement

### **Implementation:**
- **Approach 1:** Multiple Path Generation (5-8h, ⭐⭐ Medium) - **RECOMMENDED**
- **Approach 2:** Path Randomization (1-2h, ⭐ Easy) - **QUICK WIN**
- **Approach 3:** Path Point Variation (1-2h, ⭐ Easy)
- **Approach 4:** Path Caching (1-2h, ⭐ Easy)

---

## 🚀 **NEXT STEPS**

1. **Review** plan này với user
2. **Decide** which approach to implement (Recommended: Approach 2 first, then Approach 1)
3. **Start with Approach 2** - Quick wins (path randomization)
4. **Test thoroughly** sau mỗi approach
5. **Evaluate results** trước khi proceed

---

**REMEMBER:** Start with Approach 2 (Path Randomization) - quick win, simple implementation, immediate benefit! ⭐

