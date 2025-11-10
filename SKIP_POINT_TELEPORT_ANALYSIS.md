# 🎯 Skip Point Teleport Analysis

## 📋 **Vấn Đề**

Khi skip point:
1. Bot không execute point đó (không có teleport command trong point đó)
2. Bot step() đến point tiếp theo
3. Bot execute point tiếp theo, có Move command
4. Move command sẽ dùng pathfinding và press key direction (walk) để di chuyển
5. **Vấn đề:** Nếu distance đủ xa, bot sẽ walk rất lâu, không efficient

**User muốn:** Nếu distance đủ xa thì teleport thay vì walk, nhưng vẫn giữ tính chất random.

---

## 🔍 **Phân Tích**

### **Current Flow:**

```
Skip Point → Step to Next Point → Execute Next Point → Move Command → Walk (press key direction)
```

### **Desired Flow:**

```
Skip Point → Step to Next Point → Execute Next Point → Move Command → 
  - If distance > threshold: Teleport (with probability để giữ random)
  - If distance <= threshold: Walk (press key direction)
```

---

## 🎯 **Giải Pháp**

### **Approach 1: Smart Move Command (Recommended)** ⭐⭐⭐⭐⭐

**Mô tả:**
- Modify Move command để check distance
- Nếu distance > threshold, có thể teleport (với probability)
- Nếu distance <= threshold, walk như bình thường
- Giữ tính chất random với probability

**Implementation:**
```python
class Move(Command):
    def main(self):
        distance = utils.distance(config.player_pos, self.target)
        teleport_threshold = 0.1  # Distance threshold for teleport
        
        # If distance is far, consider teleporting
        if distance > teleport_threshold:
            # Random decision: 70% teleport, 30% walk (giữ random)
            if random.random() < 0.70:
                # Teleport to target
                self._teleport_to_target()
                return
            # Otherwise, walk (30% chance)
        
        # Normal walk (pathfinding + press key direction)
        self._walk_to_target()
```

**Ưu điểm:**
- ✅ Giữ tính chất random (70% teleport, 30% walk)
- ✅ Efficient khi distance đủ xa
- ✅ Không break existing logic
- ✅ Có thể configure threshold và probability

**Nhược điểm:**
- ❌ Cần modify Move command
- ❌ Cần implement teleport logic

---

### **Approach 2: Skip Context Detection** ⭐⭐⭐

**Mô tả:**
- Detect khi đang skip point (track skip context)
- Nếu đang skip và distance > threshold, teleport
- Nếu không skip, walk như bình thường

**Implementation:**
```python
# In Routine class
self.is_skipping = False  # Track skip context

# In Bot._main()
if should_skip:
    config.routine.is_skipping = True
    config.routine.step()
else:
    config.routine.is_skipping = False
    element.execute()
    config.routine.step()

# In Move command
def main(self):
    distance = utils.distance(config.player_pos, self.target)
    teleport_threshold = 0.1
    
    # If skipping and distance is far, teleport
    if config.routine.is_skipping and distance > teleport_threshold:
        self._teleport_to_target()
        return
    
    # Normal walk
    self._walk_to_target()
```

**Ưu điểm:**
- ✅ Chỉ teleport khi skip point
- ✅ Không ảnh hưởng normal execution

**Nhược điểm:**
- ❌ Phức tạp hơn (cần track skip context)
- ❌ Không giữ random (luôn teleport khi skip và đủ xa)

---

### **Approach 3: Hybrid (Skip Context + Random)** ⭐⭐⭐⭐

**Mô tả:**
- Detect khi đang skip point
- Nếu đang skip và distance > threshold, có thể teleport (với probability)
- Nếu không skip, walk như bình thường
- Giữ tính chất random với probability

**Implementation:**
```python
# In Move command
def main(self):
    distance = utils.distance(config.player_pos, self.target)
    teleport_threshold = 0.1
    
    # If skipping and distance is far, consider teleporting
    if hasattr(config.routine, 'is_skipping') and config.routine.is_skipping:
        if distance > teleport_threshold:
            # Random decision: 80% teleport, 20% walk (giữ random)
            if random.random() < 0.80:
                self._teleport_to_target()
                return
            # Otherwise, walk (20% chance)
    
    # Normal walk
    self._walk_to_target()
```

**Ưu điểm:**
- ✅ Chỉ teleport khi skip point (efficient)
- ✅ Giữ tính chất random (80% teleport, 20% walk)
- ✅ Không ảnh hưởng normal execution

**Nhược điểm:**
- ❌ Phức tạp hơn (cần track skip context)

---

## 🎯 **Recommended Approach: Approach 1 (Smart Move Command)**

### **Lý Do:**
1. ✅ **Đơn giản:** Không cần track skip context
2. ✅ **Random:** Giữ tính chất random với probability
3. ✅ **Efficient:** Teleport khi distance đủ xa
4. ✅ **Flexible:** Có thể configure threshold và probability

---

## 🎯 **Implementation Plan**

### **Step 1: Modify Move Command**

**Add teleport logic:**
```python
class Move(Command):
    def __init__(self, x, y, max_steps=15):
        super().__init__(locals())
        self.target = (float(x), float(y))
        self.max_steps = settings.validate_nonnegative_int(max_steps)
        self.prev_direction = ''
        # Teleport configuration
        self.teleport_threshold = 0.1  # Distance threshold for teleport
        self.teleport_probability = 0.70  # 70% chance to teleport if distance > threshold
    
    def _teleport_to_target(self):
        """Teleport to target using Luminous teleport command."""
        from src.common.vkeys import press
        from resources.command_books.luminous import Key
        
        # Calculate direction
        d_x = self.target[0] - config.player_pos[0]
        d_y = self.target[1] - config.player_pos[1]
        
        # Teleport in direction
        if abs(d_x) > abs(d_y):
            # Horizontal teleport
            if d_x > 0:
                # Teleport right
                press(Key.teleport, 1)
                press(Key.right, 1)
            else:
                # Teleport left
                press(Key.teleport, 1)
                press(Key.left, 1)
        else:
            # Vertical teleport
            if d_y > 0:
                # Teleport down
                press(Key.teleport, 1)
                press(Key.down, 1)
            else:
                # Teleport up
                press(Key.teleport, 1)
                press(Key.up, 1)
        
        # Wait for teleport
        time.sleep(0.2)
        
        # Adjust position if needed
        error = utils.distance(config.player_pos, self.target)
        if error > settings.move_tolerance:
            # Use Adjust command to fine-tune
            adjust = config.bot.command_book['adjust']
            adjust(*self.target).execute()
    
    def main(self):
        distance = utils.distance(config.player_pos, self.target)
        
        # If distance is far, consider teleporting (with probability để giữ random)
        if distance > self.teleport_threshold:
            import random
            if random.random() < self.teleport_probability:
                # Teleport to target (70% chance)
                action_log.info("🚀 Move: Teleporting to target (distance: %.3f, threshold: %.3f)", 
                               distance, self.teleport_threshold)
                self._teleport_to_target()
                return
            # Otherwise, walk (30% chance)
            action_log.info("🚶 Move: Walking to target (distance: %.3f, threshold: %.3f)", 
                           distance, self.teleport_threshold)
        
        # Normal walk (pathfinding + press key direction)
        self._walk_to_target()
```

---

### **Step 2: Extract Walk Logic**

**Extract walk logic to separate method:**
```python
def _walk_to_target(self):
    """Walk to target using pathfinding and press key direction."""
    counter = self.max_steps
    path = config.layout.shortest_path(config.player_pos, self.target)
    # ... existing walk logic ...
```

---

## 🎯 **Tính Chất Random**

### **Giữ Tính Chất Random:**

1. **Random Probability:** 70% teleport, 30% walk (có thể configure)
2. **Random trong Teleport:** Teleport direction cũng có thể random
3. **Random trong Walk:** Walk path vẫn có pathfinding variation

### **Ví Dụ:**

```
Distance = 0.15 (far)
- Random = 0.65 (< 0.70) → Teleport ✅
- Random = 0.75 (>= 0.70) → Walk ✅

Distance = 0.05 (near)
- Always walk (distance <= threshold)
```

---

## 🎯 **Configuration**

### **Teleport Threshold:**
- **Default:** 0.1 (distance > 0.1 → consider teleport)
- **Location:** `Move.__init__()` - `self.teleport_threshold = 0.1`
- **To change:** Modify `teleport_threshold` value

### **Teleport Probability:**
- **Default:** 0.70 (70% chance to teleport if distance > threshold)
- **Location:** `Move.__init__()` - `self.teleport_probability = 0.70`
- **To change:** Modify `teleport_probability` value

---

## 🎯 **Expected Results**

### **Without Teleport:**
```
Skip Point → Next Point → Move Command → Walk (slow if distance is far)
```

### **With Teleport:**
```
Skip Point → Next Point → Move Command → 
  - Distance > 0.1: 70% Teleport (fast), 30% Walk (slow)
  - Distance <= 0.1: Always Walk (normal)
```

---

## 🎯 **Status**

✅ **Plan Ready for Implementation**
✅ **Giữ Tính Chất Random**
✅ **Efficient khi Distance Đủ Xa**

---

**Last Updated:** 2024
**Status:** ✅ Plan Ready for Review

