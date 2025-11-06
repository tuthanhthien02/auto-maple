# 📊 Routine Frequency Optimization Guide - tree_2_floor.csv

## 🎯 **TỔNG QUAN**

Routine hiện tại có **TẤT CẢ points với `frequency=1`**, nghĩa là execute mỗi lần (100%). Điều này tạo pattern dễ detect.

**Frequency hoạt động như sau:**

-   `frequency=1`: Execute mỗi lần (100%)
-   `frequency=2`: Execute mỗi 2 lần (50%)
-   `frequency=3`: Execute mỗi 3 lần (33%)
-   `frequency=4`: Execute mỗi 4 lần (25%)

---

## 📋 **PHÂN TÍCH ROUTINE**

### **Cấu Trúc Routine:**

```
Floor 1: 5 positions (pos_0 → pos_4)
  ↓
jump_up (transition)
  ↓
Floor 2: 5 positions (pos_1 → pos_5)
  ↓
jump_down (transition)
  ↓
Loop back to Floor 1
```

### **Points Breakdown:**

1. **f1_pos_0**: Start point với buff
2. **f1_pos_1**: Regular farming point
3. **f1_pos_2**: Regular farming point
4. **f1_pos_3**: Regular farming point
5. **f1_pos_4**: Last point trước transition
6. **jump_up**: Critical transition (KHÔNG THỂ SKIP)
7. **f2_pos_1**: Regular farming point
8. **f2_pos_2**: Regular farming point
9. **f2_pos_3**: Regular farming point
10. **f2_pos_4**: Regular farming point
11. **f2_pos_5**: Last point trước transition
12. **jump_down**: Critical transition (KHÔNG THỂ SKIP)

---

## ✅ **ĐỀ XUẤT FREQUENCY**

### **Nguyên Tắc:**

1. **Critical Transitions** → `frequency=1` (KHÔNG THỂ SKIP)

    - `jump_up`: Luôn phải execute để lên Floor 2
    - `jump_down`: Luôn phải execute để xuống Floor 1

2. **Last Points Before Transition** → `frequency=1` (CẦN THIẾT)

    - `f1_pos_4`: Cần để đảm bảo đến transition point
    - `f2_pos_5`: Cần để đảm bảo đến transition point

3. **Buff Points** → `frequency=2-3` (KHÔNG CẦN MỖI LOOP)

    - `f1_pos_0`: Buff không cần mỗi loop, có thể skip một số lần

4. **Regular Farming Points** → `frequency=2` (CÓ THỂ SKIP)
    - `f1_pos_1`, `f1_pos_2`, `f1_pos_3`: Có thể skip để tạo variation
    - `f2_pos_1`, `f2_pos_2`, `f2_pos_3`, `f2_pos_4`: Có thể skip để tạo variation

---

## 📊 **FREQUENCY ASSIGNMENT**

| Point         | Current       | Recommended   | Lý Do                                |
| ------------- | ------------- | ------------- | ------------------------------------ |
| **f1_pos_0**  | `frequency=1` | `frequency=3` | Buff point - không cần mỗi loop      |
| **f1_pos_1**  | `frequency=1` | `frequency=2` | Regular point - có thể skip          |
| **f1_pos_2**  | `frequency=1` | `frequency=2` | Regular point - có thể skip          |
| **f1_pos_3**  | `frequency=1` | `frequency=2` | Regular point - có thể skip          |
| **f1_pos_4**  | `frequency=1` | `frequency=1` | Last point - cần để đến transition   |
| **jump_up**   | `frequency=1` | `frequency=1` | Critical transition - KHÔNG THỂ SKIP |
| **f2_pos_1**  | `frequency=1` | `frequency=2` | Regular point - có thể skip          |
| **f2_pos_2**  | `frequency=1` | `frequency=2` | Regular point - có thể skip          |
| **f2_pos_3**  | `frequency=1` | `frequency=2` | Regular point - có thể skip          |
| **f2_pos_4**  | `frequency=1` | `frequency=2` | Regular point - có thể skip          |
| **f2_pos_5**  | `frequency=1` | `frequency=1` | Last point - cần để đến transition   |
| **jump_down** | `frequency=1` | `frequency=1` | Critical transition - KHÔNG THỂ SKIP |

---

## 🎯 **CHI TIẾT ĐỀ XUẤT**

### **Option 1: Conservative (An Toàn)** ⭐⭐⭐

**Frequency values:**

-   Buff point: `frequency=3` (execute 33% - buff không cần thường xuyên)
-   Regular points: `frequency=2` (execute 50% - tạo variation vừa phải)
-   Last points: `frequency=1` (execute 100% - đảm bảo đến transition)
-   Transitions: `frequency=1` (execute 100% - không thể skip)

**Benefits:**

-   ✅ An toàn - không làm bot fail
-   ✅ Tạo variation đáng kể
-   ✅ Giảm detection risk

**Risks:**

-   ⚠️ Có thể skip một số farming points (nhưng không ảnh hưởng nhiều)

---

### **Option 2: Moderate (Cân Bằng)** ⭐⭐⭐⭐ RECOMMENDED

**Frequency values:**

-   Buff point: `frequency=3` (execute 33%)
-   Regular points: `frequency=2` (execute 50%)
-   Last points: `frequency=1` (execute 100%)
-   Transitions: `frequency=1` (execute 100%)

**Benefits:**

-   ✅ Cân bằng giữa variation và efficiency
-   ✅ Giảm detection risk đáng kể
-   ✅ Vẫn đảm bảo farming efficiency

**Risks:**

-   ⚠️ Minimal - safe choice

---

### **Option 3: Aggressive (Tối Đa Variation)** ⭐⭐⭐

**Frequency values:**

-   Buff point: `frequency=4` (execute 25%)
-   Regular points: `frequency=3` (execute 33%)
-   Last points: `frequency=1` (execute 100%)
-   Transitions: `frequency=1` (execute 100%)

**Benefits:**

-   ✅ Maximum variation
-   ✅ Giảm detection risk cao nhất

**Risks:**

-   ⚠️ Có thể skip nhiều farming points
-   ⚠️ Efficiency giảm đáng kể

---

## 📝 **IMPLEMENTATION**

### **File Đã Tối Ưu:**

Đã tạo file `tree_2_floor_optimized.csv` với frequency được optimize theo **Option 2 (Moderate)**.

**Changes:**

-   `f1_pos_0`: `frequency=1` → `frequency=3` (buff point)
-   `f1_pos_1`: `frequency=1` → `frequency=2` (regular point)
-   `f1_pos_2`: `frequency=1` → `frequency=2` (regular point)
-   `f1_pos_3`: `frequency=1` → `frequency=2` (regular point)
-   `f1_pos_4`: `frequency=1` → `frequency=1` (last point - giữ nguyên)
-   `jump_up`: `frequency=1` → `frequency=1` (transition - giữ nguyên)
-   `f2_pos_1`: `frequency=1` → `frequency=2` (regular point)
-   `f2_pos_2`: `frequency=1` → `frequency=2` (regular point)
-   `f2_pos_3`: `frequency=1` → `frequency=2` (regular point)
-   `f2_pos_4`: `frequency=1` → `frequency=2` (regular point)
-   `f2_pos_5`: `frequency=1` → `frequency=1` (last point - giữ nguyên)
-   `jump_down`: `frequency=1` → `frequency=1` (transition - giữ nguyên)

---

## ⚠️ **LƯU Ý QUAN TRỌNG**

### **KHÔNG BAO GIỜ:**

1. ❌ **Đặt `frequency > 1` cho transition points** (jump_up, jump_down)

    - Bot sẽ không thể chuyển floor → fail routine

2. ❌ **Đặt `frequency > 1` cho last points trước transition**

    - Bot có thể không đến được transition point → fail routine

3. ❌ **Đặt `frequency` quá cao** (frequency > 4)
    - Bot sẽ skip quá nhiều points → efficiency giảm đáng kể

### **NÊN:**

1. ✅ **Giữ `frequency=1` cho critical points**

    - Transitions (jump_up, jump_down)
    - Last points trước transitions (f1_pos_4, f2_pos_5)

2. ✅ **Dùng `frequency=2-3` cho regular points**

    - Tạo variation vừa phải
    - Không ảnh hưởng nhiều đến efficiency

3. ✅ **Dùng `frequency=3-4` cho buff points**
    - Buff không cần mỗi loop
    - Giảm detection risk

---

## 📊 **EXPECTED RESULTS**

### **Before (frequency=1 cho tất cả):**

-   Execute pattern: **100% predictable**
-   Detection risk: **HIGH**
-   Efficiency: **100%**

### **After (frequency optimized):**

-   Execute pattern: **Variable** (33-100% tùy point)
-   Detection risk: **MEDIUM-LOW**
-   Efficiency: **~70-80%** (vẫn tốt)

---

## 🎯 **KHUYẾN NGHỊ**

### **Sử dụng file đã optimize:**

1. ✅ **Test routine mới** (`tree_2_floor_optimized.csv`)
2. ✅ **Verify bot không fail** (đảm bảo transitions luôn execute)
3. ✅ **Monitor efficiency** (nếu giảm quá nhiều, giảm frequency)
4. ✅ **Adjust frequency** nếu cần (có thể tăng/giảm tùy preference)

### **Customization:**

Nếu muốn variation nhiều hơn:

-   Tăng frequency của regular points: `frequency=2` → `frequency=3`

Nếu muốn efficiency cao hơn:

-   Giảm frequency của regular points: `frequency=2` → `frequency=1`

---

**REMEMBER:** Frequency optimization giúp giảm detection risk bằng cách tạo variation trong execution pattern! ⭐
