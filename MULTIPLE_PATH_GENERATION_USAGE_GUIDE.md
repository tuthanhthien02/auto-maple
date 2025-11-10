# 🗺️ Multiple Path Generation - Usage Guide

## 🎯 **GIỚI THIỆU**

**Approach 1: Multiple Path Generation** là tính năng tạo nhiều paths khác nhau đến cùng một target, sau đó chọn random một path để di chuyển. Tính năng này giúp:
1. **Tránh pattern detection** - Không luôn dùng cùng một path
2. **Human-like behavior** - Humans không luôn đi shortest path
3. **Variation trong movement** - Mỗi lần di chuyển có thể có path khác nhau
4. **Anti-detection** - Khó detect hơn với multiple paths

---

## 🚀 **CÁCH SỬ DỤNG**

### **1. Tự Động (Mặc Định)**

Tính năng này **TỰ ĐỘNG** được kích hoạt khi bot di chuyển trong routine. **KHÔNG CẦN** chỉnh sửa routine files.

**Behavior mặc định:**
- **Generate 3 paths** mỗi lần di chuyển
- **Weighted random selection:**
  - 60% shortest path
  - 30% second path
  - 10% third path

**Ví dụ:**
```csv
# Routine file - KHÔNG CẦN THAY ĐỔI GÌ
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
Comment,Floor 1 Pos 0
reflection_random
wait_random,0.1,0.3
```

→ Bot sẽ **tự động** generate 3 paths và chọn random một path khi di chuyển đến position này.

---

## 📋 **CÁCH TẠO ROUTINE TỐT VỚI MULTIPLE PATH GENERATION**

### **1. KHÔNG SỬ DỤNG TELEPORT COMMANDS GIỮA CÁC POSITIONS**

**❌ KHÔNG NÊN:**
```csv
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
reflection_random
wait_random,0.1,0.3
teleport,right,1    # ❌ BAD: Teleport trực tiếp, không có path variation
wait_random,0.2,0.5

*,0.268,0.19,adjust=False,frequency=1
Label,f1_pos_1
reflection_random
wait_random,0.1,0.3
teleport,right,1    # ❌ BAD: Teleport trực tiếp
```

**✅ NÊN:**
```csv
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
reflection_random
wait_random,0.1,0.3
# NO TELEPORT - Move command handles movement with multiple paths

*,0.268,0.19,adjust=False,frequency=1
Label,f1_pos_1
reflection_random
wait_random,0.1,0.3
# NO TELEPORT - Move command handles movement with multiple paths
```

**Lý do:**
- Teleport commands di chuyển trực tiếp, không có path variation
- Move command tự động generate multiple paths và chọn random
- Multiple paths chỉ hoạt động khi Move command được sử dụng

---

### **2. SPACE POSITIONS ĐỦ XA**

**✅ NÊN:**
- Khoảng cách giữa các positions: **> 0.03-0.05** (3-5% của map)
- Đủ xa để có thể generate nhiều paths khác nhau
- Ví dụ: `(0.229, 0.19)` → `(0.268, 0.19)` (distance ≈ 0.039)

**❌ KHÔNG NÊN:**
- Positions quá gần nhau: **< 0.01** (1% của map)
- Path sẽ quá ngắn, không có variation
- Ví dụ: `(0.229, 0.19)` → `(0.230, 0.19)` (distance ≈ 0.001)

---

### **3. RECORD LAYOUT ĐẦY ĐỦ**

**Quan trọng:**
- **Record layout** trước khi chạy routine
- Layout cần có nhiều nodes (recorded positions)
- Nhiều nodes = nhiều paths khác nhau có thể generate

**Cách record layout:**
1. Mở GUI → Settings tab
2. Bật "Record Layout"
3. Chạy routine một lần để record các positions
4. Layout sẽ được lưu tự động

---

### **4. SỬ DỤNG ADJUST KHI CẦN**

**Khi nào dùng `adjust=True`:**
- Transition points (jump_teleport_up, jump_down)
- Critical positions cần độ chính xác cao
- Ví dụ: `*,0.668,0.132,adjust=True,frequency=1`

**Khi nào dùng `adjust=False`:**
- Normal positions (hầu hết positions)
- Cho phép path variation
- Ví dụ: `*,0.229,0.19,adjust=False,frequency=1`

---

### **5. ROUTINE STRUCTURE TỐT**

**Ví dụ routine structure:**
```csv
Label,start_routine

# ========================================
# FLOOR 1: LEFT → RIGHT
# ========================================
Comment,=== FLOOR 1 START: Move Left → Right - MULTIPLE PATHS ENABLED ===

*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
Comment,Floor 1 Pos 0: Reflection Random
buff
buff_secondary
face_right
reflection_random
wait_random,0.1,0.3
# NO TELEPORT - Move command handles movement

*,0.268,0.19,adjust=False,frequency=1
Label,f1_pos_1
Comment,Floor 1 Pos 1: Reflection Random
reflection_random
wait_random,0.1,0.3
# NO TELEPORT - Move command handles movement

# ... more positions ...

# ========================================
# TRANSITION: FLOOR 1 → FLOOR 2
# ========================================
*,0.668,0.132,adjust=True,frequency=1
Label,jump_up
Comment,Critical transition point
jump_teleport_up,1
wait_random,0.8,1.5

# ... Floor 2 positions ...

# ========================================
# LOOP BACK TO START
# ========================================
Jump,f1_pos_0
```

---

## 🔍 **KIỂM TRA MULTIPLE PATH GENERATION**

### **1. Xem Log Messages**

Khi chạy bot, bạn sẽ thấy log messages:

**Nếu multiple paths hoạt động:**
```
🔀 Multiple Paths: Selected path 1 of 3 (length=4, distance=0.045)
🔀 Multiple Paths: Selected path 2 of 3 (length=5, distance=0.048)
🔀 Multiple Paths: Selected path 1 of 3 (length=4, distance=0.045)
🔀 Multiple Paths: Selected path 3 of 3 (length=6, distance=0.052)
```

**Nếu chỉ có 1 path:**
```
Multiple Paths: Using shortest path (only one path available)
```

**Giải thích:**
- `path 1 of 3`: Đã chọn path 1 trong 3 paths
- `length=4`: Path có 4 points
- `distance=0.045`: Tổng distance của path

---

### **2. Kiểm tra Path Variation**

**Cách kiểm tra:**
1. Chạy routine nhiều lần với cùng một điểm đến
2. Xem log messages - paths nên khác nhau
3. Quan sát movement trong game - paths nên khác nhau mỗi lần

**Kỳ vọng:**
- 60% thời gian: path 1 (shortest)
- 30% thời gian: path 2 (second)
- 10% thời gian: path 3 (third)
- Paths nên khác nhau về length và distance

---

### **3. Kiểm tra Layout**

**Kiểm tra xem layout có đủ nodes không:**
- Mở GUI → View tab
- Xem minimap có nhiều green dots (nodes) không
- Nếu ít nodes → Cần record layout

---

## ⚙️ **CẤU HÌNH NÂNG CAO**

### **1. Điều Chỉnh Số Lượng Paths**

**File:** `src/routine/components.py`

**Vị trí:** Dòng 272

**Code hiện tại:**
```python
num_paths = 3  # Generate 3 paths
```

**Cách điều chỉnh:**
```python
num_paths = 2  # Generate 2 paths (faster)
num_paths = 4  # Generate 4 paths (more variation)
num_paths = 5  # Generate 5 paths (maximum variation)
```

**Lưu ý:**
- **Nhiều paths hơn:** Nhiều variation hơn, nhưng chậm hơn
- **Ít paths hơn:** Nhanh hơn, nhưng ít variation hơn
- **Mặc định 3 paths:** Cân bằng tốt

---

### **2. Điều Chỉnh Weighted Selection**

**File:** `src/routine/components.py`

**Vị trí:** Dòng 285-294

**Code hiện tại:**
```python
weights = []
if len(paths) >= 1:
    weights.append(0.6)  # 60% for shortest
if len(paths) >= 2:
    weights.append(0.3)  # 30% for second
if len(paths) >= 3:
    weights.append(0.1)  # 10% for third
```

**Cách điều chỉnh:**
```python
# More variation (50/30/20)
weights.append(0.5)  # 50% for shortest
weights.append(0.3)  # 30% for second
weights.append(0.2)  # 20% for third

# Less variation (70/20/10)
weights.append(0.7)  # 70% for shortest
weights.append(0.2)  # 20% for second
weights.append(0.1)  # 10% for third
```

---

## 📊 **ROUTINE MẪU**

### **Routine Mẫu: `tree_2_floor_multiple_paths.csv`**

Routine mẫu đã được tạo tại: `resources/routines/luminous/tree_2_floor_multiple_paths.csv`

**Đặc điểm:**
- ✅ **Không có teleport commands** giữa các positions
- ✅ **Positions spaced đủ xa** để có path variation
- ✅ **Comments chi tiết** giải thích multiple path generation
- ✅ **Optimized** cho multiple path generation

**Sử dụng:**
1. Load routine: `tree_2_floor_multiple_paths.csv`
2. Record layout trước khi chạy
3. Chạy routine và xem log messages
4. Quan sát path variation trong game

---

## ❓ **FAQ - CÂU HỎI THƯỜNG GẶP**

### **Q1: Tại sao không thấy path variation?**

**A:** Có thể do:
1. **Routine sử dụng teleport commands** - Loại bỏ teleport commands
2. **Layout không có đủ nodes** - Record layout đầy đủ
3. **Positions quá gần nhau** - Tăng khoảng cách giữa positions
4. **Chỉ có 1 path available** - Kiểm tra layout và positions

---

### **Q2: Có cần thay đổi routine files không?**

**A:** Không. Tính năng này tự động hoạt động. Chỉ cần:
- Loại bỏ teleport commands (nếu có)
- Đảm bảo positions spaced đủ xa
- Record layout đầy đủ

---

### **Q3: Performance có bị ảnh hưởng không?**

**A:** Có, nhưng rất nhỏ:
- Generate 3 paths: ~3x thời gian so với 1 path
- Nhưng chỉ generate khi di chuyển, không phải mỗi frame
- Impact: < 1% performance loss

---

### **Q4: Có thể tắt tính năng này không?**

**A:** Có. Sửa `Move.main()` trong `src/routine/components.py`:
```python
# Thay vì:
paths = config.layout.generate_paths(...)

# Dùng:
path = config.layout.shortest_path(config.player_pos, self.target)
```

---

### **Q5: Weighted selection có thể điều chỉnh không?**

**A:** Có. Xem phần "Cấu Hình Nâng Cao" ở trên.

---

## 🎯 **TÓM TẮT**

### **Để Multiple Path Generation hoạt động tốt:**

1. ✅ **Loại bỏ teleport commands** giữa các positions
2. ✅ **Space positions đủ xa** (> 0.03-0.05)
3. ✅ **Record layout đầy đủ** trước khi chạy
4. ✅ **Sử dụng adjust=True** cho transition points
5. ✅ **Monitor log messages** để xác nhận hoạt động

### **Routine Mẫu:**

- File: `resources/routines/luminous/tree_2_floor_multiple_paths.csv`
- Đặc điểm: Optimized cho multiple path generation
- Sử dụng: Load và chạy routine mẫu

---

## 📚 **REFERENCES**

- **Implementation Plan:** `APPROACH1_MULTIPLE_PATH_GENERATION_PLAN.md`
- **Implementation Files:**
  - `src/routine/layout.py` (generate_paths, alternative paths)
  - `src/routine/components.py` (path selection)
- **Sample Routine:** `resources/routines/luminous/tree_2_floor_multiple_paths.csv`

---

**Last Updated:** 2024
**Status:** ✅ Ready to Use

