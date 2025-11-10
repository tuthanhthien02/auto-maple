# 📖 Hướng Dẫn Sử Dụng Approach 2: Path Randomization

## 🎯 **GIỚI THIỆU**

**Approach 2: Path Randomization** là tính năng tự động tạo path variation trong movement, giúp bot di chuyển với các đường đi khác nhau mỗi lần, tránh pattern detection và tạo movement tự nhiên hơn.

---

## 🚀 **CÁCH SỬ DỤNG**

### **1. Tự Động (Mặc Định)**

Tính năng này **TỰ ĐỘNG** được kích hoạt khi bot di chuyển trong routine. **KHÔNG CẦN** chỉnh sửa routine files.

**Behavior mặc định:**
- **70% thời gian:** Sử dụng randomized path (variation: 10-15%)
- **30% thời gian:** Sử dụng shortest path (hiệu quả nhất)

**Ví dụ:**
```csv
# Routine file - KHÔNG CẦN THAY ĐỔI GÌ
*,0.229,0.19,adjust=False,frequency=1
Label,f1_pos_0
Comment,Floor 1 Pos 0
reflection_random
wait_random,0.1,0.3
teleport,right,1
```

→ Bot sẽ **tự động** sử dụng randomized path khi di chuyển đến position này.

---

## 🔧 **CẤU HÌNH NÂNG CAO**

### **1. Điều Chỉnh Tỷ Lệ Randomization (70/30)**

**File:** `src/routine/components.py`

**Vị trí:** Dòng 265

**Code hiện tại:**
```python
# 70% chance to use randomized path, 30% shortest path
use_randomized = random.random() < 0.7
```

**Cách điều chỉnh:**
```python
# 80% randomized, 20% shortest (more variation)
use_randomized = random.random() < 0.8

# 50% randomized, 50% shortest (balanced)
use_randomized = random.random() < 0.5

# 90% randomized, 10% shortest (maximum variation)
use_randomized = random.random() < 0.9
```

**Lưu ý:**
- **Tỷ lệ cao hơn (80-90%):** Nhiều variation hơn, nhưng có thể chậm hơn
- **Tỷ lệ thấp hơn (50-60%):** Ít variation hơn, nhưng hiệu quả hơn
- **Mặc định 70%:** Cân bằng tốt giữa variation và hiệu quả

---

### **2. Điều Chỉnh Variation Level (10-15%)**

**File:** `src/routine/components.py`

**Vị trí:** Dòng 270

**Code hiện tại:**
```python
# Generate path with randomization (10-15% variation)
variation = random.uniform(0.10, 0.15)
```

**Cách điều chỉnh:**
```python
# Minimal variation (5-10%)
variation = random.uniform(0.05, 0.10)

# Moderate variation (10-15%) - MẶC ĐỊNH
variation = random.uniform(0.10, 0.15)

# Higher variation (15-20%)
variation = random.uniform(0.15, 0.20)

# Maximum variation (20-25%) - CẨN THẬN: có thể tạo path dài hơn
variation = random.uniform(0.20, 0.25)
```

**Giải thích:**
- **Variation thấp (5-10%):** Path gần giống shortest path, ít variation
- **Variation trung bình (10-15%):** Cân bằng tốt (mặc định)
- **Variation cao (15-20%):** Nhiều variation, path có thể khác biệt đáng kể
- **Variation rất cao (20-25%):** Maximum variation, nhưng có thể tạo path dài hơn

---

### **3. Sử Dụng Trong Code (Advanced)**

Nếu bạn muốn sử dụng trực tiếp trong code Python:

**File:** `src/routine/layout.py`

**Method:** `shortest_path()`

**Cách sử dụng:**
```python
# Shortest path (no randomization)
path = config.layout.shortest_path(source, target)

# Randomized path (10% variation)
path = config.layout.shortest_path(source, target, randomize=True, variation=0.10)

# Randomized path (15% variation)
path = config.layout.shortest_path(source, target, randomize=True, variation=0.15)

# Randomized path (20% variation - maximum)
path = config.layout.shortest_path(source, target, randomize=True, variation=0.20)
```

**Parameters:**
- `source`: Vị trí bắt đầu `(x, y)`
- `target`: Vị trí đích `(x, y)`
- `randomize`: `True` để bật randomization, `False` để dùng shortest path
- `variation`: Mức độ variation (0.0 - 0.2, tương đương 0% - 20%)

---

## 📊 **MONITORING VÀ DEBUG**

### **1. Xem Log Messages**

Tính năng tự động log path selection. Xem log để biết bot đang sử dụng loại path nào:

**Log examples:**
```
[DEBUG] Unique Pathfinding: Using randomized path (variation=12.34%)
[DEBUG] Unique Pathfinding: Using shortest path
[DEBUG] Unique Pathfinding: Using randomized path (variation=14.56%)
```

**Cách xem log:**
- Xem trong console khi chạy bot
- Hoặc xem file log: `logs/auto_maple.log`

---

### **2. Kiểm Tra Path Variation**

Để kiểm tra xem path có thực sự khác nhau không:

1. **Chạy routine nhiều lần** với cùng một điểm đến
2. **Quan sát movement** trong game
3. **Xem log messages** để xác nhận path selection
4. **So sánh paths** giữa các lần chạy

**Kỳ vọng:**
- Path nên khác nhau giữa các lần chạy
- 70% thời gian sử dụng randomized path
- 30% thời gian sử dụng shortest path

---

## 🎛️ **CẤU HÌNH ĐỀ XUẤT**

### **1. Cấu Hình Cân Bằng (Mặc Định - Khuyên Dùng)**

```python
# 70% randomized, 30% shortest
use_randomized = random.random() < 0.7
variation = random.uniform(0.10, 0.15)  # 10-15%
```

**Ưu điểm:**
- ✅ Cân bằng tốt giữa variation và hiệu quả
- ✅ Path variation đủ để tránh detection
- ✅ Vẫn duy trì hiệu quả movement

**Phù hợp cho:**
- Hầu hết các routine
- Training maps thông thường
- General gameplay

---

### **2. Cấu Hình Maximum Variation (Chống Detection Mạnh)**

```python
# 90% randomized, 10% shortest
use_randomized = random.random() < 0.9
variation = random.uniform(0.15, 0.20)  # 15-20%
```

**Ưu điểm:**
- ✅ Maximum variation
- ✅ Rất khó detect pattern
- ✅ Movement rất tự nhiên

**Nhược điểm:**
- ⚠️ Có thể chậm hơn một chút
- ⚠️ Path có thể dài hơn

**Phù hợp cho:**
- High-risk areas (nơi có khả năng bị detect cao)
- Long training sessions
- Anti-detection priority

---

### **3. Cấu Hình Hiệu Quả (Speed Priority)**

```python
# 50% randomized, 50% shortest
use_randomized = random.random() < 0.5
variation = random.uniform(0.05, 0.10)  # 5-10%
```

**Ưu điểm:**
- ✅ Tối ưu speed
- ✅ Path ngắn hơn
- ✅ Movement nhanh hơn

**Nhược điểm:**
- ⚠️ Ít variation hơn
- ⚠️ Có thể dễ detect pattern hơn

**Phù hợp cho:**
- Speed farming
- Short training sessions
- Low-risk areas

---

## ❓ **FAQ - CÂU HỎI THƯỜNG GẶP**

### **Q1: Tính năng này có ảnh hưởng đến performance không?**

**A:** Có, nhưng rất nhỏ. Randomized path có thể dài hơn shortest path một chút (5-20%), nhưng vẫn đảm bảo đến đích. 30% thời gian vẫn sử dụng shortest path để duy trì hiệu quả.

---

### **Q2: Có cần thay đổi routine files không?**

**A:** Không. Tính năng này tự động hoạt động với tất cả routines hiện tại. Không cần chỉnh sửa routine files.

---

### **Q3: Có thể tắt tính năng này không?**

**A:** Có. Đặt `use_randomized = False` trong `src/routine/components.py` (dòng 265) để luôn sử dụng shortest path.

```python
# Tắt randomization - luôn dùng shortest path
use_randomized = False
```

---

### **Q4: Variation level nào là tốt nhất?**

**A:** 
- **10-15% (mặc định):** Cân bằng tốt nhất, khuyên dùng
- **15-20%:** Nếu muốn nhiều variation hơn
- **5-10%:** Nếu muốn tối ưu speed

---

### **Q5: Bot có thể bị stuck vì randomized path không?**

**A:** Không. Randomized path vẫn đảm bảo đến đích, chỉ là đường đi có thể khác một chút so với shortest path. Bot vẫn sẽ đến được target position.

---

### **Q6: Có thể sử dụng với tất cả routines không?**

**A:** Có. Tính năng này hoạt động với tất cả routines, không phụ thuộc vào routine type hoặc map layout.

---

### **Q7: Làm sao biết tính năng đang hoạt động?**

**A:** Xem log messages. Bạn sẽ thấy:
```
[DEBUG] Unique Pathfinding: Using randomized path (variation=12.34%)
[DEBUG] Unique Pathfinding: Using shortest path
```

---

### **Q8: Có thể điều chỉnh tỷ lệ 70/30 không?**

**A:** Có. Xem phần **"Điều Chỉnh Tỷ Lệ Randomization"** ở trên.

---

### **Q9: Variation 20% có quá cao không?**

**A:** 20% là mức tối đa khuyên dùng. Variation cao hơn (25%+) có thể tạo path dài hơn đáng kể, ảnh hưởng đến performance.

---

### **Q10: Tính năng này có tương thích với Phase 1 và Phase 2 không?**

**A:** Có. Tính năng này hoàn toàn tương thích với:
- Phase 1: Timing Randomization
- Phase 2: Movement Pattern Variation

Tất cả các tính năng hoạt động cùng nhau để tạo movement tự nhiên nhất.

---

## 🔍 **TROUBLESHOOTING**

### **Vấn Đề 1: Bot không sử dụng randomized path**

**Nguyên nhân:**
- Code chưa được cập nhật
- `use_randomized` đã bị set thành `False`

**Giải pháp:**
1. Kiểm tra file `src/routine/components.py` dòng 265
2. Đảm bảo `use_randomized = random.random() < 0.7`
3. Restart bot

---

### **Vấn Đề 2: Path quá dài, bot chậm**

**Nguyên nhân:**
- Variation level quá cao
- Tỷ lệ randomized quá cao

**Giải pháp:**
1. Giảm variation level: `variation = random.uniform(0.05, 0.10)`
2. Giảm tỷ lệ randomized: `use_randomized = random.random() < 0.5`
3. Hoặc dùng cấu hình "Hiệu Quả" ở trên

---

### **Vấn Đề 3: Không thấy log messages**

**Nguyên nhân:**
- Log level không đúng
- Debug mode chưa bật

**Giải pháp:**
1. Kiểm tra log level trong config
2. Đảm bảo debug mode được bật
3. Xem file log: `logs/auto_maple.log`

---

### **Vấn Đề 4: Path vẫn giống nhau mỗi lần**

**Nguyên nhân:**
- Variation level quá thấp
- Random seed không đổi

**Giải pháp:**
1. Tăng variation level: `variation = random.uniform(0.15, 0.20)`
2. Đảm bảo `random.seed()` không được gọi với cùng một giá trị
3. Kiểm tra xem có đủ candidate points không

---

## 📝 **TÓM TẮT**

### **Sử Dụng Cơ Bản:**
- ✅ **Tự động hoạt động** - Không cần chỉnh sửa routine files
- ✅ **70/30 split** - 70% randomized, 30% shortest
- ✅ **10-15% variation** - Cân bằng tốt

### **Cấu Hình Nâng Cao:**
- 🔧 Điều chỉnh tỷ lệ randomization (70/30)
- 🔧 Điều chỉnh variation level (10-15%)
- 🔧 Sử dụng trực tiếp trong code

### **Monitoring:**
- 📊 Xem log messages
- 📊 Kiểm tra path variation
- 📊 So sánh paths giữa các lần chạy

### **Cấu Hình Đề Xuất:**
- ⚙️ **Cân bằng (mặc định):** 70% randomized, 10-15% variation
- ⚙️ **Maximum variation:** 90% randomized, 15-20% variation
- ⚙️ **Hiệu quả:** 50% randomized, 5-10% variation

---

## 🎯 **KẾT LUẬN**

**Approach 2: Path Randomization** là một tính năng mạnh mẽ và dễ sử dụng để tạo path variation, giúp bot di chuyển tự nhiên hơn và tránh pattern detection.

**Khuyến nghị:**
- Sử dụng cấu hình mặc định (70/30, 10-15% variation) cho hầu hết trường hợp
- Điều chỉnh theo nhu cầu cụ thể (anti-detection priority hoặc speed priority)
- Monitor log messages để đảm bảo tính năng hoạt động đúng

---

**Tài liệu này được tạo để hướng dẫn sử dụng Approach 2: Path Randomization.**
**Nếu có câu hỏi hoặc vấn đề, vui lòng xem phần FAQ hoặc Troubleshooting ở trên.**

---

**Last Updated:** 2024
**Status:** ✅ Ready to Use

