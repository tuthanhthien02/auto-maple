# 🔍 Multiple Path Generation - Troubleshooting Guide

## ❌ **VẤN ĐỀ: Không thấy path random và không có log messages**

### **Nguyên nhân có thể:**

#### **1. Layout chưa được record đủ nodes (Nguyên nhân chính)**

**Vấn đề:**
- Layout chưa có đủ nodes (recorded positions)
- Alternative paths không thể generate vì không có đủ intermediate points
- Chỉ generate được 1 path (shortest path) → không có path variation

**Kiểm tra:**
1. Mở GUI → View tab
2. Xem minimap có nhiều green dots (nodes) không
3. Nếu ít nodes → Layout chưa được record đủ

**Giải pháp:**
1. **Record layout đầy đủ:**
   - Mở GUI → Settings tab
   - Bật "Record Layout"
   - Chạy routine một lần để record các positions
   - Layout sẽ được lưu tự động

2. **Kiểm tra layout file:**
   - Layout files được lưu tại: `resources/layouts/luminous/`
   - Tên file: `{routine_name}` (không có extension)
   - Xóa layout file cũ nếu cần record lại

---

#### **2. Positions quá gần nhau**

**Vấn đề:**
- Positions quá gần nhau (< 0.01)
- Path quá ngắn → không có alternative paths
- Chỉ generate được 1 path

**Kiểm tra:**
- Tính khoảng cách giữa các positions
- Ví dụ: `(0.229, 0.19)` → `(0.230, 0.19)` (distance ≈ 0.001) → QUÁ GẦN

**Giải pháp:**
- Tăng khoảng cách giữa các positions
- Khoảng cách tối thiểu: **> 0.03-0.05** (3-5% của map)
- Ví dụ: `(0.229, 0.19)` → `(0.268, 0.19)` (distance ≈ 0.039) → OK

---

#### **3. Alternative paths bị duplicate**

**Vấn đề:**
- Alternative paths giống hệt shortest path
- Bị loại bỏ như duplicate
- Chỉ còn 1 path

**Kiểm tra:**
- Xem log messages: `Multiple Paths: Generated X unique paths`
- Nếu chỉ có 1 path → Alternative paths bị duplicate

**Giải pháp:**
- Đã cải thiện duplicate detection (more lenient)
- Nếu vẫn bị duplicate → Cần more layout nodes hoặc different positions

---

#### **4. Code không được gọi (Approach 2 vẫn chạy)**

**Vấn đề:**
- Code Approach 2 (Path Randomization) vẫn đang chạy
- Code Approach 1 (Multiple Path Generation) không được gọi
- Log messages: "Path Randomization" thay vì "Multiple Paths"

**Kiểm tra:**
- Xem log file: `logs/auto_maple.log`
- Tìm "Path Randomization" → Approach 2 đang chạy
- Tìm "Multiple Paths" → Approach 1 đang chạy

**Giải pháp:**
- Đảm bảo code Approach 1 đã được implement
- Restart bot sau khi update code
- Kiểm tra `src/routine/components.py` có `generate_paths()` không

---

## ✅ **CÁCH KIỂM TRA**

### **1. Kiểm tra Log Messages**

**Sau khi chạy bot, xem log file:** `logs/auto_maple.log`

**Nếu Multiple Path Generation hoạt động:**
```
Multiple Paths: Generated 3 unique paths (requested 3, alternative: 2)
🔀 Multiple Paths: Selected path 1 of 3 (length=4, distance=0.045, weight=60.0%)
🔀 Multiple Paths: Selected path 2 of 3 (length=5, distance=0.048, weight=30.0%)
🔀 Multiple Paths: Selected path 1 of 3 (length=4, distance=0.045, weight=60.0%)
```

**Nếu chỉ có 1 path:**
```
Multiple Paths: Generated 1 unique paths (requested 3, alternative: 0)
⚠️ Multiple Paths: Only 1 path available (length=2, distance=0.039) - Need more layout nodes or different positions
```

**Nếu có lỗi:**
```
Multiple Paths: Error generating paths: [error message]
Multiple Paths: Failed to generate alternative path (strategy=1): [error message]
```

---

### **2. Kiểm tra Layout**

**Cách kiểm tra:**
1. Mở GUI → View tab
2. Xem minimap có nhiều green dots (nodes) không
3. Nếu ít nodes (< 10-20) → Cần record layout

**Cách record layout:**
1. Mở GUI → Settings tab
2. Bật "Record Layout"
3. Chạy routine một lần
4. Layout sẽ được lưu tự động

---

### **3. Kiểm tra Code**

**Kiểm tra file:** `src/routine/components.py`

**Tìm method:** `Move.main()`

**Code nên có:**
```python
def main(self):
    # Unique Pathfinding - Approach 1: Multiple Path Generation
    num_paths = 3  # Generate 3 paths
    
    paths = config.layout.generate_paths(
        config.player_pos, 
        self.target, 
        num_paths=num_paths
    )
    
    if len(paths) > 1:
        # Weighted random selection
        ...
        action_log.info("🔀 Multiple Paths: Selected path %d of %d", ...)
```

**Nếu không có → Code chưa được update**

---

### **4. Kiểm tra Routine File**

**Kiểm tra routine file có teleport commands không:**
```bash
grep -i "teleport" resources/routines/luminous/tree_2_floor_multiple_paths.csv
```

**Nếu có teleport commands:**
- ❌ BAD: Teleport trực tiếp, không có path variation
- ✅ GOOD: Không có teleport, Move command handles movement

---

## 🔧 **GIẢI PHÁP**

### **Solution 1: Record Layout Đầy Đủ**

**Steps:**
1. Mở GUI → Settings tab
2. Bật "Record Layout"
3. Chạy routine một lần (để record positions)
4. Tắt "Record Layout" (optional)
5. Chạy routine lại và xem log messages

**Expected result:**
- Log messages: "Multiple Paths: Generated 3 unique paths"
- Multiple paths available
- Path variation visible

---

### **Solution 2: Tăng Khoảng Cách Positions**

**Nếu positions quá gần:**
1. Mở routine file
2. Tăng khoảng cách giữa các positions
3. Khoảng cách tối thiểu: > 0.03-0.05

**Example:**
```csv
# BAD: Too close
*,0.229,0.19,adjust=False,frequency=1
*,0.230,0.19,adjust=False,frequency=1  # Distance ≈ 0.001

# GOOD: Enough distance
*,0.229,0.19,adjust=False,frequency=1
*,0.268,0.19,adjust=False,frequency=1  # Distance ≈ 0.039
```

---

### **Solution 3: Enable Debug Logging**

**Để xem detailed logs:**
1. Set environment variable: `AUTO_MAPLE_ACTION_LOG=1`
2. Hoặc modify code để enable debug logging
3. Xem log file: `logs/auto_maple.log`

**Expected logs:**
```
Multiple Paths: Generated shortest path (length=4)
Multiple Paths: Generated alternative path 1 (strategy=1, length=5)
Multiple Paths: Generated alternative path 2 (strategy=2, length=6)
Multiple Paths: Generated 3 unique paths (requested 3, alternative: 2)
Multiple Paths: Available path 1: length=4, distance=0.045
Multiple Paths: Available path 2: length=5, distance=0.048
Multiple Paths: Available path 3: length=6, distance=0.052
🔀 Multiple Paths: Selected path 2 of 3 (length=5, distance=0.048, weight=30.0%)
```

---

## 📊 **DEBUG CHECKLIST**

### **Checklist để debug:**

- [ ] **Code được update:**
  - [ ] `src/routine/components.py` có `generate_paths()` call
  - [ ] `src/routine/layout.py` có `generate_paths()` method
  - [ ] Restart bot sau khi update code

- [ ] **Layout được record:**
  - [ ] Layout file exists: `resources/layouts/luminous/{routine_name}`
  - [ ] Minimap có nhiều green dots (nodes)
  - [ ] Record layout một lần trước khi chạy

- [ ] **Routine file đúng:**
  - [ ] Không có teleport commands giữa positions
  - [ ] Positions spaced đủ xa (> 0.03-0.05)
  - [ ] Sử dụng routine: `tree_2_floor_multiple_paths.csv`

- [ ] **Log messages:**
  - [ ] Xem log file: `logs/auto_maple.log`
  - [ ] Tìm "Multiple Paths" messages
  - [ ] Check số lượng paths generated

- [ ] **Path variation:**
  - [ ] Quan sát movement trong game
  - [ ] Paths nên khác nhau mỗi lần
  - [ ] Log messages nên show different paths

---

## 🎯 **TÓM TẮT**

### **Vấn đề phổ biến:**

1. **Layout chưa được record đủ nodes** → Chỉ generate được 1 path
2. **Positions quá gần nhau** → Không có alternative paths
3. **Alternative paths bị duplicate** → Chỉ còn 1 path
4. **Code không được gọi** → Approach 2 vẫn chạy

### **Giải pháp:**

1. **Record layout đầy đủ** trước khi chạy
2. **Tăng khoảng cách** giữa positions
3. **Enable debug logging** để xem detailed logs
4. **Kiểm tra code** đã được update chưa

### **Expected result:**

- Log messages: "Multiple Paths: Generated 3 unique paths"
- Path selection: "🔀 Multiple Paths: Selected path X of 3"
- Path variation visible trong game
- Different paths mỗi lần di chuyển

---

**Last Updated:** 2024
**Status:** 🔍 Troubleshooting Guide

