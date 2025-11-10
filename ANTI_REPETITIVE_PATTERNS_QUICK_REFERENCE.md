# 🎯 Anti-Repetitive Patterns - Quick Reference

## 📋 **Tóm Tắt**

Document này tóm tắt các **repetitive patterns** hiện tại và **recommendations** để tránh chúng.

---

## 🔍 **Repetitive Patterns Hiện Tại**

### **1. Execution Patterns** ⭐⭐⭐⭐⭐
- ❌ Bot luôn execute routine theo thứ tự: `Point 0 → Point 1 → Point 2 → ...`
- ❌ Bot luôn execute commands theo thứ tự: `buff → buff_secondary → face_right → ...`
- ❌ Bot luôn visit tất cả Points (không skip)

### **2. Movement Patterns** ⭐⭐⭐⭐
- ❌ Bot luôn chọn shortest path
- ❌ Bot luôn đi đến exact position `(x, y)`
- ❌ Bot luôn đi cùng một cách

### **3. Command Sequence Patterns** ⭐⭐⭐⭐⭐
- ❌ Bot luôn execute commands trong cùng thứ tự
- ❌ Bot luôn execute tất cả commands (không skip)
- ❌ Bot không có random commands

### **4. Timing Patterns** ⭐⭐⭐
- ✅ Bot có timing variation (đã có `get_human_delay`)
- ❌ Bot luôn wait cùng thời gian giữa các commands
- ❌ Bot không có random pauses

---

## 🎯 **Top 5 Recommendations**

### **1. Command Sequence Randomization** ⭐⭐⭐⭐⭐

**Mô tả:**
- Randomize thứ tự các commands (50% chance)
- Skip một số commands (10% chance per command)
- Thêm random waits (5% chance)

**Impact:** ⭐⭐⭐⭐⭐ (Rất cao)
**Difficulty:** ⭐⭐ (Dễ)
**Priority:** **Implement First**

---

### **2. Point Selection Randomization** ⭐⭐⭐⭐⭐

**Mô tả:**
- Skip một số Points (10% chance)
- Randomize thứ tự visit các Points

**Impact:** ⭐⭐⭐⭐⭐ (Rất cao)
**Difficulty:** ⭐⭐⭐ (Trung bình)
**Priority:** **Implement Second**

---

### **3. Position Randomization (Offset)** ⭐⭐⭐⭐

**Mô tả:**
- Thêm random offset nhỏ vào target position (±0.005, ±0.003)
- Không đi đến exact position

**Impact:** ⭐⭐⭐⭐ (Cao)
**Difficulty:** ⭐ (Rất dễ)
**Priority:** **Implement Third**

---

### **4. Routine Pattern Variation** ⭐⭐⭐⭐⭐

**Mô tả:**
- Chạy routine theo thứ tự ngược lại (reverse)
- Skip một floor hoàn toàn
- Switch giữa multiple variants

**Impact:** ⭐⭐⭐⭐⭐ (Rất cao)
**Difficulty:** ⭐⭐⭐⭐ (Khó)
**Priority:** **Implement After Phase 1**

---

### **5. Path Variation (Multiple Paths)** ⭐⭐⭐⭐

**Mô tả:**
- Generate multiple paths
- Select paths randomly
- Paths within routine scope

**Impact:** ⭐⭐⭐⭐ (Cao)
**Difficulty:** ⭐⭐⭐⭐ (Khó)
**Priority:** **Implement After Phase 1**

---

## 📊 **Implementation Priority**

### **Phase 1: Quick Wins (1-2 days)** ✅

1. **Command Sequence Randomization** ⭐⭐⭐⭐⭐
2. **Position Randomization (Offset)** ⭐⭐⭐⭐
3. **Point Selection Randomization** ⭐⭐⭐⭐⭐

### **Phase 2: Advanced Features (3-5 days)** 🔄

4. **Routine Pattern Variation** ⭐⭐⭐⭐⭐
5. **Path Variation (Multiple Paths)** ⭐⭐⭐⭐

---

## 🎯 **Quick Implementation Guide**

### **Step 1: Command Sequence Randomization**

**File:** `src/routine/components.py`

**Add to Point class:**
```python
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

# Modify Point.main()
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
```

---

### **Step 2: Position Randomization (Offset)**

**File:** `src/routine/components.py`

**Modify Point.__init__():**
```python
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

---

### **Step 3: Point Selection Randomization**

**File:** `src/routine/routine.py`

**Add to Routine class:**
```python
def _should_skip_point(self):
    """Check if we should skip current point (10% chance)."""
    import random
    return random.random() < 0.10  # 10% chance to skip
```

**File:** `src/modules/bot.py`

**Modify Bot._main():**
```python
def _main(self):
    while True:
        if config.enabled and len(config.routine) > 0:
            # Check if we should skip BEFORE executing
            element = config.routine[config.routine.index]
            if not config.routine._should_skip_point():
                element.execute()
            config.routine.step()
```

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

## 📚 **Files to Modify**

### **Phase 1:**
- `src/routine/components.py` - Add command sequence randomization, position randomization
- `src/routine/routine.py` - Add point selection randomization
- `src/modules/bot.py` - Modify to check skip before executing

### **Phase 2:**
- `src/routine/routine.py` - Add variant switching logic
- `src/routine/layout.py` - Add path variation
- `src/routine/components.py` - Improve Move command

---

## 🎯 **Next Steps**

1. **Review Plan:** Xem xét `ANTI_REPETITIVE_PATTERNS_PLAN.md`
2. **Implement Phase 1:** Command Sequence Randomization, Position Randomization, Point Selection Randomization
3. **Test Phase 1:** Test các tính năng mới
4. **Implement Phase 2:** Routine Pattern Variation, Path Variation
5. **Test Phase 2:** Test các tính năng nâng cao

---

**Last Updated:** 2024
**Status:** ✅ Quick Reference Ready

