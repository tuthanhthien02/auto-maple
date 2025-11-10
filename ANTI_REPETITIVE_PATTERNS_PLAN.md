# 🎯 Plan: Anti-Repetitive Patterns Recommendations

## 📋 **Tổng Quan**

Document này liệt kê các **repetitive patterns** hiện tại trong codebase và các **recommendations** để tránh chúng, giúp bot hoạt động **human-like** hơn và khó bị detect hơn.

---

## 🔍 **Repetitive Patterns Hiện Tại**

### **1. Execution Patterns (Bot Behavior)**

#### **Problem:**
- ✅ Bot luôn execute routine theo thứ tự: `Point 0 → Point 1 → Point 2 → ... → Point N → Loop`
- ✅ Bot luôn execute commands trong mỗi Point theo thứ tự: `buff → buff_secondary → face_right → reflection_random → wait_random → teleport`
- ✅ Bot luôn visit tất cả Points (không skip)

#### **Example:**
```
Routine: f1_pos_0 → f1_pos_1 → f1_pos_2 → f1_pos_3 → f1_pos_4 → f1_pos_5
Bot luôn đi: 0 → 1 → 2 → 3 → 4 → 5 → 0 → 1 → 2 → 3 → 4 → 5 → ...
```

#### **Detection Risk:** ⭐⭐⭐⭐⭐ (Rất cao)
- Anti-cheat có thể detect pattern cố định
- Dễ dàng predict bot's next action
- Không có variation trong execution

---

### **2. Movement Patterns (Path Selection)**

#### **Problem:**
- ✅ Bot luôn chọn shortest path giữa 2 points
- ✅ Bot luôn đi đến exact position `(x, y)` (không có offset)
- ✅ Bot luôn đi cùng một cách (không có detours)

#### **Example:**
```
Move from (0.229, 0.19) to (0.268, 0.19)
Bot luôn đi: Shortest path, exact position, same way every time
```

#### **Detection Risk:** ⭐⭐⭐⭐ (Cao)
- Movement patterns rất predictable
- Không có variation trong path selection
- Exact positioning dễ detect

---

### **3. Command Sequence Patterns**

#### **Problem:**
- ✅ Bot luôn execute commands trong cùng thứ tự
- ✅ Bot luôn execute tất cả commands (không skip)
- ✅ Bot không có random commands (như wait_random giữa commands)

#### **Example:**
```
Point commands:
1. buff
2. buff_secondary
3. face_right
4. reflection_random
5. wait_random,0.1,0.3
6. teleport,right,1

Bot luôn execute: 1 → 2 → 3 → 4 → 5 → 6 (same order every time)
```

#### **Detection Risk:** ⭐⭐⭐⭐⭐ (Rất cao)
- Command execution pattern rất predictable
- Không có variation trong command sequence
- Dễ detect bot behavior

---

### **4. Timing Patterns**

#### **Problem:**
- ✅ Bot có timing variation (đã có `get_human_delay`) nhưng vẫn có patterns
- ✅ Bot luôn wait cùng thời gian giữa các commands
- ✅ Bot không có random pauses (như occasional stops)

#### **Example:**
```
Command execution:
- reflection_random → wait 0.1-0.3s → teleport → wait 0.2-0.5s
- Pattern: Same timing every time (even with variation)
```

#### **Detection Risk:** ⭐⭐⭐ (Trung bình)
- Timing variation đã có nhưng vẫn có patterns
- Cần thêm variation trong timing

---

### **5. Code-Level Patterns (DRY Violations)**

#### **Problem:**
- ✅ Code duplication trong command execution
- ✅ Similar logic in multiple places
- ✅ Hard-coded values (magic numbers)

#### **Example:**
```python
# Duplication in Point.main()
move = config.bot.command_book['move']
move(*self.location).execute()
if self.adjust:
    adjust = config.bot.command_book['adjust']
    adjust(*self.location).execute()
for command in self.commands:
    command.execute()
```

#### **Detection Risk:** ⭐ (Thấp - không ảnh hưởng bot behavior)
- Code quality issue
- Không ảnh hưởng trực tiếp đến bot behavior
- Nhưng cần refactor để maintainability

---

## 🎯 **Recommendations**

### **1. Command Sequence Randomization** ⭐⭐⭐⭐⭐

#### **Mô tả:**
- Randomize thứ tự các commands trong mỗi Point
- Đôi khi skip một số commands (không execute tất cả)
- Đôi khi thêm random commands (như wait_random)

#### **Implementation:**
```python
# In Point.main()
def main(self):
    if self.counter == 0:
        update_activity()
        
        move = config.bot.command_book['move']
        move(*self.location).execute()
        if self.adjust:
            adjust = config.bot.command_book['adjust']
            adjust(*self.location).execute()
        
        # NEW: Randomize command sequence
        commands = self._randomize_command_sequence(self.commands)
        for command in commands:
            command.execute()
    self._increment_counter()

def _randomize_command_sequence(self, commands):
    """Randomize command sequence with skip probability."""
    import random
    
    # Shuffle commands (50% chance)
    if random.random() < 0.5:
        commands = random.sample(commands, len(commands))
    
    # Filter commands with skip probability (10% chance per command)
    filtered_commands = []
    for cmd in commands:
        if random.random() > 0.1:  # 90% chance to execute
            filtered_commands.append(cmd)
            # 5% chance to add random wait
            if random.random() < 0.05:
                from src.routine.components import Wait_Random
                filtered_commands.append(Wait_Random(0.1, 0.3))
    
    return filtered_commands
```

#### **Files to Modify:**
- `src/routine/components.py` - Add `_randomize_command_sequence()` to Point class

#### **Priority:** ⭐⭐⭐⭐⭐ (Rất cao)
#### **Difficulty:** ⭐⭐ (Dễ)
#### **Impact:** ⭐⭐⭐⭐⭐ (Rất cao)

---

### **2. Point Selection Randomization** ⭐⭐⭐⭐⭐

#### **Mô tả:**
- Đôi khi skip một số Points trong routine
- Randomize thứ tự visit các Points (không phải lúc nào cũng tuần tự)
- Tạo "shortcuts" - nhảy qua một số points

#### **Implementation:**
```python
# In Routine.step()
def step(self):
    """Increments index with randomization."""
    # Check if we should skip current point
    if self._should_skip_point():
        # Skip to next point
        self.index = (self.index + 1) % len(self.sequence) if len(self.sequence) > 0 else 0
    else:
        # Normal step
        self.index = (self.index + 1) % len(self.sequence) if len(self.sequence) > 0 else 0

def _should_skip_point(self):
    """Check if we should skip current point (10% chance)."""
    import random
    return random.random() < 0.10  # 10% chance to skip

# In Bot._main()
def _main(self):
    while True:
        if config.enabled and len(config.routine) > 0:
            # Check if we should skip BEFORE executing
            element = config.routine[config.routine.index]
            if not config.routine._should_skip_point():
                element.execute()
            config.routine.step()
```

#### **Files to Modify:**
- `src/routine/routine.py` - Add `_should_skip_point()` method
- `src/modules/bot.py` - Modify `_main()` to check skip before executing

#### **Priority:** ⭐⭐⭐⭐⭐ (Rất cao)
#### **Difficulty:** ⭐⭐⭐ (Trung bình)
#### **Impact:** ⭐⭐⭐⭐⭐ (Rất cao)

---

### **3. Position Randomization (Offset)** ⭐⭐⭐⭐

#### **Mô tả:**
- Thêm random offset nhỏ vào target position của mỗi Point
- Không đi đến exact position `(x, y)` mà đi đến `(x ± offset, y ± offset)`

#### **Implementation:**
```python
# In Point.__init__()
def __init__(self, x, y, frequency=1, skip='False', adjust='False'):
    super().__init__(locals())
    self.x = float(x)
    self.y = float(y)
    # NEW: Add random offset to position
    import random
    offset_x = random.uniform(-0.005, 0.005)  # ±0.005 offset
    offset_y = random.uniform(-0.003, 0.003)  # ±0.003 offset
    self.location = (self.x + offset_x, self.y + offset_y)
    # ... rest of code
```

#### **Files to Modify:**
- `src/routine/components.py` - Modify Point.__init__() to add random offset

#### **Priority:** ⭐⭐⭐⭐ (Cao)
#### **Difficulty:** ⭐ (Rất dễ)
#### **Impact:** ⭐⭐⭐⭐ (Cao)

---

### **4. Path Variation (Multiple Paths)** ⭐⭐⭐⭐

#### **Mô tả:**
- Đã có Multiple Path Generation nhưng cần improve
- Thêm path variation trong routine scope
- On-the-fly path regeneration

#### **Implementation:**
```python
# In Move.main()
def main(self):
    # Get routine scope
    routine_scope = config.routine.get_routine_scope()
    
    # Generate paths within routine scope
    if routine_scope:
        paths = config.layout.generate_paths_within_scope(
            config.player_pos,
            self.target,
            routine_scope,
            num_paths=3
        )
    else:
        paths = config.layout.generate_paths(
            config.player_pos,
            self.target,
            num_paths=3
        )
    
    # Select unique path (different each time)
    path = self._select_unique_path(paths)
    
    # Move along path with on-the-fly regeneration
    self._move_along_path_with_regeneration(path)
```

#### **Files to Modify:**
- `src/routine/components.py` - Improve Move command
- `src/routine/layout.py` - Add `generate_paths_within_scope()`
- `src/routine/routine.py` - Add `get_routine_scope()`

#### **Priority:** ⭐⭐⭐⭐ (Cao)
#### **Difficulty:** ⭐⭐⭐⭐ (Khó)
#### **Impact:** ⭐⭐⭐⭐ (Cao)

---

### **5. Routine Pattern Variation** ⭐⭐⭐⭐⭐

#### **Mô tả:**
- Đôi khi chạy routine theo thứ tự ngược lại (reverse)
- Đôi khi skip một floor hoàn toàn
- Tạo multiple "variants" của routine và switch giữa chúng

#### **Implementation:**
```python
# In Routine class
def __init__(self):
    self.dirty = False
    self.path = ''
    self.labels = {}
    self.index = 0
    self.sequence = []
    self.display = []
    # NEW: Routine variants
    self.variants = ['normal', 'reverse', 'floor1_only', 'floor2_only']
    self.current_variant = 'normal'
    self.variant_switch_counter = 0

def step(self):
    """Step with variant switching."""
    # Switch variant every 5-10 loops (random)
    if self.variant_switch_counter > 0:
        self.variant_switch_counter -= 1
    else:
        self._switch_variant()
        self.variant_switch_counter = random.randint(5, 10)
    
    # Step based on current variant
    if self.current_variant == 'normal':
        self.index = (self.index + 1) % len(self.sequence) if len(self.sequence) > 0 else 0
    elif self.current_variant == 'reverse':
        self.index = (self.index - 1) % len(self.sequence) if len(self.sequence) > 0 else len(self.sequence) - 1
    elif self.current_variant == 'floor1_only':
        # Only visit floor 1 points
        self.index = self._get_next_floor1_point()
    elif self.current_variant == 'floor2_only':
        # Only visit floor 2 points
        self.index = self._get_next_floor2_point()

def _switch_variant(self):
    """Switch to a random variant."""
    import random
    self.current_variant = random.choice(self.variants)
    log.info(f"Switched to variant: {self.current_variant}")
```

#### **Files to Modify:**
- `src/routine/routine.py` - Add variant switching logic

#### **Priority:** ⭐⭐⭐⭐⭐ (Rất cao)
#### **Difficulty:** ⭐⭐⭐⭐ (Khó)
#### **Impact:** ⭐⭐⭐⭐⭐ (Rất cao)

---

### **6. Code Refactoring (DRY)** ⭐⭐

#### **Mô tả:**
- Refactor code duplication
- Extract common logic into functions
- Remove magic numbers

#### **Implementation:**
```python
# Extract common logic
def execute_commands_with_randomization(commands, skip_probability=0.1):
    """Execute commands with randomization."""
    import random
    
    # Shuffle commands
    if random.random() < 0.5:
        commands = random.sample(commands, len(commands))
    
    # Filter commands
    filtered_commands = []
    for cmd in commands:
        if random.random() > skip_probability:
            filtered_commands.append(cmd)
    
    return filtered_commands

# Use in Point.main()
def main(self):
    if self.counter == 0:
        update_activity()
        move = config.bot.command_book['move']
        move(*self.location).execute()
        if self.adjust:
            adjust = config.bot.command_book['adjust']
            adjust(*self.location).execute()
        
        # Use extracted function
        commands = execute_commands_with_randomization(self.commands)
        for command in commands:
            command.execute()
    self._increment_counter()
```

#### **Files to Modify:**
- `src/routine/components.py` - Extract common logic
- `src/common/utils.py` - Add utility functions

#### **Priority:** ⭐⭐ (Thấp)
#### **Difficulty:** ⭐⭐ (Dễ)
#### **Impact:** ⭐ (Thấp - chỉ ảnh hưởng code quality)

---

## 📊 **Implementation Priority**

### **Phase 1: High Priority (Immediate)**

1. **Command Sequence Randomization** ⭐⭐⭐⭐⭐
   - Priority: Rất cao
   - Difficulty: Dễ
   - Impact: Rất cao
   - **Implement First**

2. **Point Selection Randomization** ⭐⭐⭐⭐⭐
   - Priority: Rất cao
   - Difficulty: Trung bình
   - Impact: Rất cao
   - **Implement Second**

3. **Position Randomization (Offset)** ⭐⭐⭐⭐
   - Priority: Cao
   - Difficulty: Rất dễ
   - Impact: Cao
   - **Implement Third**

---

### **Phase 2: Medium Priority (Next)**

4. **Routine Pattern Variation** ⭐⭐⭐⭐⭐
   - Priority: Rất cao
   - Difficulty: Khó
   - Impact: Rất cao
   - **Implement After Phase 1**

5. **Path Variation (Multiple Paths)** ⭐⭐⭐⭐
   - Priority: Cao
   - Difficulty: Khó
   - Impact: Cao
   - **Implement After Phase 1**

---

### **Phase 3: Low Priority (Optional)**

6. **Code Refactoring (DRY)** ⭐⭐
   - Priority: Thấp
   - Difficulty: Dễ
   - Impact: Thấp
   - **Implement When Time Permits**

---

## 🎯 **Implementation Strategy**

### **Strategy 1: Incremental Implementation (Recommended)**

**Phase 1: Quick Wins (1-2 days)**
- ✅ Command Sequence Randomization
- ✅ Position Randomization (Offset)
- ✅ Point Selection Randomization

**Phase 2: Advanced Features (3-5 days)**
- ✅ Routine Pattern Variation
- ✅ Path Variation (Multiple Paths)

**Phase 3: Code Quality (1-2 days)**
- ✅ Code Refactoring (DRY)

---

### **Strategy 2: Full Implementation (Advanced)**

**Implement tất cả cùng lúc:**
- ✅ Có đầy đủ tính năng ngay
- ❌ Phức tạp và khó debug
- ❌ Khó test từng phần

---

## 📝 **Implementation Checklist**

### **Phase 1: High Priority**

- [ ] **Command Sequence Randomization**
  - [ ] Add `_randomize_command_sequence()` to Point class
  - [ ] Test command sequence randomization
  - [ ] Verify commands are randomized

- [ ] **Point Selection Randomization**
  - [ ] Add `_should_skip_point()` to Routine class
  - [ ] Modify `Bot._main()` to check skip before executing
  - [ ] Test point selection randomization
  - [ ] Verify points are skipped randomly

- [ ] **Position Randomization (Offset)**
  - [ ] Modify Point.__init__() to add random offset
  - [ ] Test position randomization
  - [ ] Verify positions have offset

---

### **Phase 2: Medium Priority**

- [ ] **Routine Pattern Variation**
  - [ ] Add variant switching logic to Routine class
  - [ ] Add `_switch_variant()` method
  - [ ] Add `_get_next_floor1_point()` and `_get_next_floor2_point()` methods
  - [ ] Test routine pattern variation
  - [ ] Verify variants are switched

- [ ] **Path Variation (Multiple Paths)**
  - [ ] Add `get_routine_scope()` to Routine class
  - [ ] Add `generate_paths_within_scope()` to Layout class
  - [ ] Improve Move command with path variation
  - [ ] Test path variation
  - [ ] Verify paths are varied

---

### **Phase 3: Low Priority**

- [ ] **Code Refactoring (DRY)**
  - [ ] Extract common logic into functions
  - [ ] Remove code duplication
  - [ ] Remove magic numbers
  - [ ] Test refactored code
  - [ ] Verify code quality improvement

---

## 🎯 **Expected Results**

### **After Phase 1:**

1. **Command Sequence Randomization:**
   - ✅ Commands are randomized (50% chance)
   - ✅ Commands can be skipped (10% chance per command)
   - ✅ Random waits can be added (5% chance)

2. **Point Selection Randomization:**
   - ✅ Points can be skipped (10% chance)
   - ✅ Routine execution is less predictable

3. **Position Randomization:**
   - ✅ Positions have random offset (±0.005, ±0.003)
   - ✅ Bot doesn't go to exact positions

---

### **After Phase 2:**

4. **Routine Pattern Variation:**
   - ✅ Routine can run in reverse
   - ✅ Routine can skip floors
   - ✅ Routine can switch variants

5. **Path Variation:**
   - ✅ Multiple paths are generated
   - ✅ Paths are selected randomly
   - ✅ Paths are within routine scope

---

### **After Phase 3:**

6. **Code Refactoring:**
   - ✅ Code duplication is reduced
   - ✅ Code quality is improved
   - ✅ Maintainability is improved

---

## 📚 **Files to Modify**

### **Phase 1:**
- `src/routine/components.py` - Add command sequence randomization
- `src/routine/routine.py` - Add point selection randomization
- `src/modules/bot.py` - Modify to check skip before executing

### **Phase 2:**
- `src/routine/routine.py` - Add variant switching logic
- `src/routine/layout.py` - Add path variation
- `src/routine/components.py` - Improve Move command

### **Phase 3:**
- `src/routine/components.py` - Refactor code
- `src/common/utils.py` - Add utility functions

---

## 🎯 **Next Steps**

1. **Review Plan:** Xem xét plan và đưa ra feedback
2. **Implement Phase 1:** Command Sequence Randomization, Point Selection Randomization, Position Randomization
3. **Test Phase 1:** Test các tính năng mới
4. **Implement Phase 2:** Routine Pattern Variation, Path Variation
5. **Test Phase 2:** Test các tính năng nâng cao
6. **Implement Phase 3 (Optional):** Code Refactoring
7. **Test All Phases:** Test toàn bộ tính năng

---

**Last Updated:** 2024
**Status:** ✅ Plan Ready for Review

