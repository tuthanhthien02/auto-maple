# Routine Randomization - Label Requirements

## ⚠️ Requirements: Labels Phải Khớp Với Code

Để **Routine Pattern Randomization** hoạt động tốt, routine file **PHẢI** có các labels sau với đúng tên:

---

## 📋 Required Labels

### **1. Floor 1 Labels:**

```
Label,f1_pos_0    ← REQUIRED: Floor 1 start position
Label,f1_pos_1    ← Optional: Floor 1 position 1
Label,f1_pos_2    ← Optional: Floor 1 position 2
Label,f1_pos_3    ← Optional: Floor 1 position 3
Label,f1_pos_4    ← Optional: Floor 1 position 4
```

### **2. Transition Labels:**

```
Label,jump_up      ← REQUIRED: Transition Floor 1 → Floor 2
Label,jump_down    ← REQUIRED: Transition Floor 2 → Floor 1
```

### **3. Floor 2 Labels:**

```
Label,f2_pos_1     ← REQUIRED: Floor 2 start position
Label,f2_pos_2     ← Optional: Floor 2 position 2
Label,f2_pos_3     ← Optional: Floor 2 position 3
Label,f2_pos_4     ← Optional: Floor 2 position 4
Label,f2_pos_5     ← Optional: Floor 2 position 5
```

---

## 🎯 Code Requirements

Code hiện tại trong `src/common/routine_randomization.py` tìm các labels sau:

```python
variant_patterns = {
    'normal': None,  # Không cần labels
    'reverse': {
        'start_label': 'f2_pos_1',  # ← Tìm label này
        'end_label': 'f1_pos_0'     # ← Tìm label này
    },
    'floor1_only': {
        'start_label': 'f1_pos_0',  # ← Tìm label này
        'end_label': 'jump_up'      # ← Tìm label này
    },
    'floor2_only': {
        'start_label': 'f2_pos_1',  # ← Tìm label này
        'end_label': 'jump_down'    # ← Tìm label này
    }
}
```

---

## ✅ Routine File Hiện Tại (tree_2_floor.csv)

Routine file của bạn **ĐÃ CÓ ĐỦ** labels:

```
✅ Label,f1_pos_0     (line 12)
✅ Label,f1_pos_1     (line 23)
✅ Label,f1_pos_2     (line 31)
✅ Label,f1_pos_3     (line 39)
✅ Label,f1_pos_4     (line 47)
✅ Label,jump_up       (line 58)  ← Transition Floor 1 → 2
✅ Label,f2_pos_1     (line 69)
✅ Label,f2_pos_2     (line 78)
✅ Label,f2_pos_3     (line 86)
✅ Label,f2_pos_4     (line 94)
✅ Label,f2_pos_5     (line 102)
✅ Label,jump_down     (line 112) ← Transition Floor 2 → 1
```

**→ Routine file của bạn HOẠT ĐỘNG TỐT với randomization!**

---

## ⚠️ Nếu Routine Không Có Labels Đúng

### **Fallback Behavior:**

1. **Nếu label không tìm thấy:**

    - Code sẽ log warning: `"Could not find start label 'xxx' for variant, using default"`
    - Fallback về index 0 (bắt đầu từ đầu routine)
    - Variant sẽ không hoạt động đúng

2. **Nếu chỉ có một số labels:**
    - Variants có labels đó sẽ hoạt động
    - Variants thiếu labels sẽ fallback về normal

### **Ví dụ:**

**Routine không có `f2_pos_1`:**

-   Variant `normal`: ✅ Hoạt động
-   Variant `reverse`: ❌ Fallback về normal (không tìm thấy `f2_pos_1`)
-   Variant `floor1_only`: ✅ Hoạt động
-   Variant `floor2_only`: ❌ Fallback về normal (không tìm thấy `f2_pos_1`)

---

## 🔧 Customization Options

### **Option 1: Update Code để Match Routine Labels**

Nếu routine có labels khác tên, edit `src/common/routine_randomization.py`:

```python
variant_patterns = {
    'normal': None,
    'reverse': {
        'start_label': 'your_floor2_start_label',  # ← Đổi tên
        'end_label': 'your_floor1_start_label'
    },
    ...
}
```

### **Option 2: Update Routine để Match Code**

Thêm labels vào routine file với đúng tên:

```
Label,f1_pos_0
Label,f2_pos_1
Label,jump_up
Label,jump_down
```

---

## 📊 Check Labels Trong Routine

Để check xem routine có đủ labels không, chạy bot và xem logs:

```
[INFO] Routine randomization initialized
[WARNING] Could not find start label 'f2_pos_1' for variant, using default
```

Nếu có warning → Routine thiếu labels

---

## 🎯 Summary

### **Required Labels:**

-   ✅ `f1_pos_0` - Floor 1 start (REQUIRED cho floor1_only)
-   ✅ `f2_pos_1` - Floor 2 start (REQUIRED cho reverse, floor2_only)
-   ✅ `jump_up` - Transition Floor 1→2 (REQUIRED cho floor1_only)
-   ✅ `jump_down` - Transition Floor 2→1 (REQUIRED cho floor2_only)

### **Routine của bạn:**

-   ✅ **Đã có đủ** tất cả required labels
-   ✅ **Không cần update** routine file
-   ✅ **Randomization sẽ hoạt động tốt**

---

## 🔄 Future Improvement

Có thể cải thiện code để:

1. **Auto-detect labels** dựa trên pattern (tìm labels có "floor", "pos", "jump")
2. **Configurable labels** - cho phép config label names trong `anti_detect_config.py`
3. **Fallback thông minh hơn** - tìm labels tương tự nếu không tìm thấy exact match

Nhưng hiện tại: **Routine phải có labels khớp với code!**
