# 🎯 Skip Point Teleport Implementation

## ✅ **Implementation Complete**

Đã implement teleport khi skip point và distance đủ xa, vẫn giữ tính chất random.

---

## 🎯 **Features**

### **1. Skip Context Detection**

- Track skip context trong Routine class
- `is_skipping_context = True` khi skip point
- `is_skipping_context = False` khi execute point

### **2. Smart Move Command**

- Check skip context và distance
- Nếu skipping và distance > threshold: teleport (75% chance) hoặc walk (25% chance)
- Nếu không skipping hoặc distance <= threshold: walk như bình thường

### **3. Random Teleport Decision**

- **Teleport Probability:** 75% (có thể configure)
- **Walk Probability:** 25% (giữ random)
- Giữ tính chất random để tránh pattern detection

---

## 📝 **Code Changes**

### **1. `src/routine/routine.py`**

**Added:**
- `is_skipping_context = False` - Track skip context

**Modified:**
- `clear()` - Reset `is_skipping_context` khi clear routine

---

### **2. `src/modules/bot.py`**

**Modified:**
- `_main()` - Set `is_skipping_context = True` khi skip point
- `_main()` - Reset `is_skipping_context = False` sau khi execute point

---

### **3. `src/routine/components.py`**

**Added:**
- `import random` - For random teleport decision
- `teleport_threshold = 0.08` - Distance threshold for teleport
- `teleport_probability = 0.75` - 75% chance to teleport
- `_teleport_to_target()` method - Teleport to target using Luminous teleport command

**Modified:**
- `Move.__init__()` - Add teleport configuration
- `Move.main()` - Check skip context and distance, decide teleport or walk

---

## 🎯 **How It Works**

### **Execution Flow:**

```
1. Skip Point → Set is_skipping_context = True
2. Step to Next Point
3. Execute Next Point → Move Command
4. Move Command:
   - Check is_skipping_context and distance
   - If skipping and distance > 0.08:
     - 75% chance: Teleport
     - 25% chance: Walk (giữ random)
   - If not skipping or distance <= 0.08:
     - Always Walk
5. Reset is_skipping_context = False after execute
```

---

## 🎯 **Teleport Logic**

### **When to Teleport:**

1. **Skip Context:** `is_skipping_context = True`
2. **Distance:** `distance > teleport_threshold` (0.08)
3. **Random:** `random() < teleport_probability` (0.75)

### **Teleport Implementation:**

```python
def _teleport_to_target(self):
    # Calculate direction (horizontal or vertical)
    d_x = self.target[0] - config.player_pos[0]
    d_y = self.target[1] - config.player_pos[1]
    
    # Determine primary direction
    if abs(d_x) > abs(d_y):
        direction = 'right' if d_x > 0 else 'left'
    else:
        direction = 'down' if d_y > 0 else 'up'
    
    # Calculate number of teleports needed
    distance = utils.distance(config.player_pos, self.target)
    num_teleports = max(1, min(int(distance / 0.06), 3))
    
    # Execute teleport command
    teleport_cmd(direction, num_teleports).execute()
```

---

## 🎯 **Tính Chất Random**

### **Giữ Tính Chất Random:**

1. **Random Probability:** 75% teleport, 25% walk (có thể configure)
2. **Random trong Teleport:** Teleport direction và số lượng teleports
3. **Random trong Walk:** Walk path vẫn có pathfinding variation

### **Ví Dụ:**

```
Skip Point → Next Point (distance = 0.12)
- Random = 0.65 (< 0.75) → Teleport ✅
- Random = 0.80 (>= 0.75) → Walk ✅

Skip Point → Next Point (distance = 0.05)
- Always Walk (distance <= 0.08)

Execute Point → Next Point (distance = 0.15)
- Always Walk (not skipping)
```

---

## 📊 **Configuration**

### **Teleport Threshold:**

- **Default:** 0.08 (distance > 0.08 → consider teleport)
- **Location:** `Move.__init__()` - `self.teleport_threshold = 0.08`
- **To change:** Modify `teleport_threshold` value

### **Teleport Probability:**

- **Default:** 0.75 (75% chance to teleport if distance > threshold and skipping)
- **Location:** `Move.__init__()` - `self.teleport_probability = 0.75`
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
  - Skipping + Distance > 0.08: 75% Teleport (fast), 25% Walk (slow)
  - Not Skipping or Distance <= 0.08: Always Walk (normal)
```

---

## 📝 **Logging**

### **Teleport Logs:**

```
🚀 Move: Teleporting right 2 times (distance: 0.120, threshold: 0.080)
Move: Teleport successful, reached target
```

### **Walk Logs:**

```
🚶 Move: Walking to target (distance: 0.120, threshold: 0.080, skipping: True, random: walk)
Move: Normal walk (distance: 0.050, skipping: False)
```

---

## 🎯 **Testing**

### **Test Cases:**

1. **Skip Point với Distance Xa:**
   - ✅ 75% chance: Teleport
   - ✅ 25% chance: Walk (giữ random)

2. **Skip Point với Distance Gần:**
   - ✅ Always Walk (distance <= threshold)

3. **Execute Point (Not Skipping):**
   - ✅ Always Walk (không teleport)

4. **Tính Chất Random:**
   - ✅ Random decision mỗi lần (75% teleport, 25% walk)
   - ✅ Không có pattern cố định

---

## 🎯 **Troubleshooting**

### **Problem: Teleport không hoạt động**

**Solution:**
- Check `is_skipping_context = True` khi skip point
- Check `distance > teleport_threshold` (0.08)
- Check `teleport_probability` value (0.75)
- Check logs for teleport decisions

---

### **Problem: Teleport quá nhiều**

**Solution:**
- Reduce `teleport_probability` (e.g., from 0.75 to 0.50)
- Increase `teleport_threshold` (e.g., from 0.08 to 0.12)

---

### **Problem: Teleport không đủ xa**

**Solution:**
- Increase `num_teleports` calculation
- Adjust `teleport_distance` estimate (0.06)
- Check teleport command execution

---

## 🎯 **Status**

✅ **Implementation Complete**
✅ **Giữ Tính Chất Random**
✅ **Efficient khi Skip Point và Distance Đủ Xa**
✅ **Ready for Testing**

---

## 🎯 **Next Steps**

1. **Test với routine:**
   - Test skip point với distance xa
   - Test skip point với distance gần
   - Test execute point (not skipping)

2. **Adjust Configuration:**
   - Tune `teleport_threshold` (0.08)
   - Tune `teleport_probability` (0.75)
   - Tune `num_teleports` calculation

3. **Monitor Logs:**
   - Check teleport decisions
   - Check walk decisions
   - Check random values

---

**Last Updated:** 2024
**Status:** ✅ Implementation Complete - Ready for Testing

