# 🔍 Path Randomization Troubleshooting Guide

## ❌ **VẤN ĐỀ: Không thấy path random khi sử dụng routine**

### **Nguyên nhân có thể:**

#### **1. Routine sử dụng Teleport Command (Nguyên nhân chính)**

**Vấn đề:**
- Nếu routine có `teleport,right,1` hoặc `teleport,left,1` giữa các positions
- Bot sẽ **teleport trực tiếp** đến position tiếp theo
- Sau đó `Move` command chỉ được dùng để **điều chỉnh vị trí cuối cùng** (fine-tuning)
- Path sẽ rất ngắn (1-2 points) hoặc direct path
- **Randomization không có tác dụng** vì path quá ngắn

**Ví dụ routine có vấn đề:**
```csv
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
reflection_random
wait_random,0.1,0.3
teleport,right,1    # ← Teleport trực tiếp, Move command sau đó chỉ điều chỉnh
wait_random,0.2,0.5

*,0.268,0.19,adjust=False,frequency=1
Label,f1_pos_1
reflection_random
wait_random,0.1,0.3
teleport,right,1    # ← Teleport trực tiếp
```

**Giải pháp:**
- **Loại bỏ teleport commands** giữa các positions
- Để bot sử dụng `Move` command để di chuyển tự nhiên giữa các positions
- Path randomization sẽ hoạt động tốt hơn với multi-step paths

---

#### **2. Layout không có đủ Nodes**

**Vấn đề:**
- Nếu layout không có nhiều nodes (recorded positions)
- Path sẽ luôn giống nhau vì không có nhiều lựa chọn
- Randomization không thể tạo variation nếu không có alternative paths

**Giải pháp:**
- **Record layout** đầy đủ trước khi chạy routine
- Đảm bảo layout có nhiều nodes ở các vị trí khác nhau
- Sử dụng "Record Layout" feature trong GUI để record map

---

#### **3. Positions quá gần nhau**

**Vấn đề:**
- Nếu các positions quá gần nhau (distance < move_tolerance)
- Path sẽ là direct path (chỉ 1 point)
- Randomization không có tác dụng

**Giải pháp:**
- Tăng khoảng cách giữa các positions
- Đảm bảo distance > `move_tolerance` (thường là 0.01-0.02)

---

#### **4. Debug Logging không được bật**

**Vấn đề:**
- Log messages mặc định ở DEBUG level
- Không thấy log messages nếu debug logging không được bật

**Giải pháp:**
- **Đã fix:** Thêm INFO level logging để luôn hiển thị
- Bây giờ bạn sẽ thấy log messages như:
  ```
  🔀 Path Randomization: Using randomized path (variation=20.5%, path_length=3)
  ⚡ Path Randomization: Using shortest path (path_length=2)
  ```

---

## ✅ **CÁCH KIỂM TRA**

### **1. Kiểm tra Log Messages**

Khi chạy bot, bạn sẽ thấy log messages:

**Nếu path randomization hoạt động:**
```
🔀 Path Randomization: Using randomized path (variation=18.3%, path_length=4)
⚡ Path Randomization: Using shortest path (path_length=3)
🔀 Path Randomization: Using randomized path (variation=22.1%, path_length=5)
```

**Nếu path quá ngắn:**
```
⚠️ Path Randomization: Direct path detected (path_length=1), randomization may not be visible
🔀 Path Randomization: Using randomized path (variation=19.7%, path_length=1)
```

**Nếu không thấy log messages:**
- Kiểm tra log file: `logs/auto_maple.log`
- Đảm bảo bot đang chạy và Move command được gọi

---

### **2. Kiểm tra Routine File**

**Xem routine file có teleport commands không:**
```bash
grep -i "teleport" resources/routines/luminous/tree_2_floor_new.csv
```

**Nếu có nhiều teleport commands:**
- Đây là nguyên nhân chính
- Cần loại bỏ hoặc giảm teleport commands
- Để bot sử dụng Move command tự nhiên

---

### **3. Kiểm tra Path Length**

**Trong log, kiểm tra `path_length`:**
- `path_length=1`: Direct path (randomization không có tác dụng)
- `path_length=2`: Very short path (randomization ít tác dụng)
- `path_length>=3`: Multi-step path (randomization hoạt động tốt)

**Nếu path_length luôn là 1-2:**
- Routine sử dụng teleport (nguyên nhân chính)
- Hoặc positions quá gần nhau
- Hoặc layout không có đủ nodes

---

### **4. Kiểm tra Layout**

**Kiểm tra xem layout có đủ nodes không:**
- Mở GUI → View tab
- Xem minimap có nhiều green dots (nodes) không
- Nếu ít nodes → Cần record layout

---

## 🔧 **GIẢI PHÁP CHO ROUTINE CỦA BẠN**

### **Vấn đề với `tree_2_floor_new.csv`:**

Routine hiện tại có `teleport,right,1` và `teleport,left,1` giữa mỗi position:

```csv
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
reflection_random
wait_random,0.1,0.3
teleport,right,1    # ← Vấn đề: Teleport trực tiếp
wait_random,0.2,0.5

*,0.268,0.19,adjust=False,frequency=1
Label,f1_pos_1
reflection_random
wait_random,0.1,0.3
teleport,right,1    # ← Vấn đề: Teleport trực tiếp
```

### **Giải pháp 1: Loại bỏ Teleport Commands (Khuyên dùng)**

**Sửa routine để loại bỏ teleport commands:**
```csv
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
reflection_random
wait_random,0.1,0.3
# Loại bỏ: teleport,right,1
# Loại bỏ: wait_random,0.2,0.5

*,0.268,0.19,adjust=False,frequency=1
Label,f1_pos_1
reflection_random
wait_random,0.1,0.3
# Loại bỏ: teleport,right,1
```

**Kết quả:**
- Bot sẽ sử dụng `Move` command để di chuyển giữa các positions
- Path sẽ có nhiều steps (3-5 points)
- Path randomization sẽ hoạt động tốt

---

### **Giải pháp 2: Giảm Teleport Frequency**

**Giữ một số teleport commands nhưng giảm frequency:**
```csv
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
reflection_random
wait_random,0.1,0.3
# Chỉ teleport mỗi 3-4 positions
teleport,right,1
wait_random,0.2,0.5

*,0.268,0.19,adjust=False,frequency=1
Label,f1_pos_1
reflection_random
wait_random,0.1,0.3
# Không teleport, để bot move tự nhiên

*,0.327,0.19,adjust=False,frequency=1
Label,f1_pos_2
reflection_random
wait_random,0.1,0.3
# Không teleport, để bot move tự nhiên
```

---

### **Giải pháp 3: Sử dụng Move Command trực tiếp**

**Thay thế teleport bằng move commands:**
```csv
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
reflection_random
wait_random,0.1,0.3
# Thay vì teleport, để Move command tự nhiên di chuyển

*,0.268,0.19,adjust=False,frequency=1
Label,f1_pos_1
reflection_random
wait_random,0.1,0.3
```

**Lưu ý:** Move command được gọi tự động khi đến mỗi Point position, không cần thêm command.

---

## 📊 **CẢI THIỆN ĐÃ THỰC HIỆN**

### **1. Tăng Variation Level**
- **Trước:** 10-15% variation
- **Sau:** 15-25% variation (dễ thấy hơn)

### **2. Thêm INFO Level Logging**
- **Trước:** Chỉ DEBUG level (không hiển thị)
- **Sau:** INFO level (luôn hiển thị)
- Log messages:
  ```
  🔀 Path Randomization: Using randomized path (variation=20.5%, path_length=4)
  ⚡ Path Randomization: Using shortest path (path_length=3)
  ```

### **3. Thêm Cảnh báo Direct Path**
- Cảnh báo khi path quá ngắn (path_length=1)
- Giúp identify vấn đề nhanh chóng

### **4. Thêm Path Details Logging**
- Log path length, distance, và số points
- Giúp debug và monitor path variation

---

## 🎯 **KHUYẾN NGHỊ**

### **Để Path Randomization hoạt động tốt:**

1. **Loại bỏ teleport commands** giữa các positions (khuyên dùng nhất)
2. **Record layout đầy đủ** trước khi chạy routine
3. **Tăng khoảng cách** giữa các positions nếu quá gần
4. **Monitor log messages** để xác nhận path randomization hoạt động
5. **Kiểm tra path_length** trong log (nên >= 3 để thấy rõ variation)

### **Nếu vẫn không thấy variation:**

1. **Kiểm tra log messages** - có thấy "Using randomized path" không?
2. **Kiểm tra path_length** - có >= 3 không?
3. **Kiểm tra routine file** - có teleport commands không?
4. **Kiểm tra layout** - có đủ nodes không?
5. **Test với routine đơn giản** - chỉ 2-3 positions, không có teleport

---

## 📝 **TÓM TẮT**

**Vấn đề chính:** Routine sử dụng `teleport` commands, khiến `Move` command chỉ điều chỉnh vị trí cuối cùng, path quá ngắn, randomization không có tác dụng.

**Giải pháp:** Loại bỏ hoặc giảm teleport commands, để bot sử dụng `Move` command tự nhiên giữa các positions.

**Đã cải thiện:** Tăng variation level, thêm INFO logging, thêm cảnh báo direct path.

---

**Last Updated:** 2024
**Status:** ✅ Ready for Testing

