# Routine Randomization Implementation Guide

## ✅ Đã Implement

### 1. **Point Selection Randomization**

-   **Mô tả:** Đôi khi skip một số Points trong routine để tạo variation
-   **Tính năng:**
    -   Skip probability: 10% mặc định
    -   Maximum 2 skips per loop
    -   Minimum 3 points giữa các skips
    -   **Safety:** Không bao giờ skip Labels, Jumps, hoặc transition points (adjust=True)

### 2. **Routine Pattern Randomization**

-   **Mô tả:** Switch giữa các variants của routine để tạo variation lớn
-   **Variants:**
    -   **Normal** (70%): Routine execution bình thường
    -   **Reverse** (15%): Bắt đầu từ Floor 2 thay vì Floor 1
    -   **Floor 1 Only** (10%): Chỉ train ở Floor 1
    -   **Floor 2 Only** (5%): Chỉ train ở Floor 2
-   **Switching:** Sau 3 loops, có 15% chance switch variant

---

## 📁 Files Modified

1. **`src/common/anti_detect_config.py`**

    - Thêm config cho routine randomization

2. **`src/common/routine_randomization.py`** (NEW)

    - Module mới chứa logic randomization

3. **`src/routine/routine.py`**

    - Modify `step()` để sử dụng randomization

4. **`src/modules/bot.py`**
    - Initialize randomization khi bot start
    - Set variant start index khi bot start

---

## ⚙️ Configuration

Config mẫu trong `src/common/anti_detect_config.py` (bật thủ công):

```python
'routine_randomization': {
    'enabled': True,
    'point_selection': {
        'enabled': True,
        'skip_probability': 0.10,  # 10% chance to skip
        'max_skip_per_loop': 2,
        'min_points_between_skips': 3,
        'never_skip_labels': True,
        'never_skip_jumps': True,
        'never_skip_transitions': True
    },
    'routine_pattern': {
        'enabled': True,
        'variant_switch_probability': 0.15,  # 15% chance to switch
        'min_loops_before_switch': 3,
        'floor_variant_chance': 0.10,
        'variants': {
            'normal': {'weight': 0.70},
            'reverse': {'weight': 0.15},
            'floor1_only': {'weight': 0.10},
            'floor2_only': {'weight': 0.05}
        }
    },
    'floor_descriptors': [
        {'id': 'floor1', 'labels': ['f1_pos_0', 'f1_pos_1'], 'y_range': [0.16, 1.0], 'priority': 10},
        {'id': 'floor2', 'labels': ['f2_pos_0', 'f2_pos_1'], 'y_range': [-1.0, 0.16], 'priority': 20}
    ],
    'command_sequence': {
        'enabled': True,
        'shuffle_probability': 0.30,
        'skip_probability': 0.08,
        'extra_wait_probability': 0.20,
        'extra_wait_range': (0.05, 0.12),
        'skip_blacklist': ['Teleport', 'Adjust'],
        'shuffle_blacklist': ['Teleport', 'Adjust']
    }
}
```

> **Lưu ý:** Trong repo mặc định, `enabled` cho cả block tổng và từng phần đều `False`. Bạn chỉ cần bật những phần cần dùng (qua GUI hoặc chỉnh file) theo ví dụ trên.

---

## 🎯 Cách Hoạt Động

### Point Selection Randomization

1. Khi `routine.step()` được gọi:

    - Check xem có nên skip point hiện tại không
    - Nếu skip: move đến point tiếp theo
    - Nếu không: execute point bình thường

2. Safety checks:

    - Không skip Labels (để đảm bảo routine structure)
    - Không skip Jumps (để đảm bảo loops)
    - Không skip transition points (adjust=True)

3. Reset counter sau mỗi loop

### Routine Pattern Randomization

1. Khi bot start:

    - Select variant dựa trên weights
    - Set start index dựa trên variant (nếu có)

2. Trong quá trình chạy:

    - Track số loops trong variant hiện tại
    - Sau N loops, có probability switch variant

3. Variant switching:
    - Check sau mỗi loop completion
    - Select variant mới dựa trên weights
    - Reset loop counter

---

## 🔧 Customization

### Điều chỉnh Skip Probability

```python
# Tăng skip probability (nhiều variation hơn, nhưng risk hơn)
'skip_probability': 0.15  # 15%

# Giảm skip probability (ít variation, an toàn hơn)
'skip_probability': 0.05  # 5%
```

### Điều chỉnh Variant Weights

```python
# Tăng weight cho normal (ít variation)
'normal': {'weight': 0.90}

# Tăng weight cho reverse (nhiều variation)
'reverse': {'weight': 0.30}
```

### Command Sequence Randomization

```python
'command_sequence': {
    'enabled': True,
    'shuffle_probability': 0.40,      # Tỷ lệ shuffle command (trừ blacklist)
    'skip_probability': 0.10,         # Xác suất skip các command phụ
    'extra_wait_probability': 0.25,   # Xác suất thêm delay nhỏ
    'extra_wait_range': (0.05, 0.12), # Khoảng delay thêm (trước khi humanize)
    'skip_blacklist': ['Teleport', 'Adjust'],    # Không skip các command critical
    'shuffle_blacklist': ['Teleport', 'Adjust']  # Giữ order cố định
}
```

### Floor Descriptors

- Khai báo rõ mô tả cho từng tầng, hỗ trợ >2 floor.
- Mỗi descriptor gồm:
  - `id`: tên tầng (`floor1`, `floor2`, `upper`, …)
  - `labels`: danh sách label (không phân biệt hoa thường) để match nhanh.
  - `y_range`: (optional) min/max tọa độ Y.
  - `priority`: ưu tiên khi nhiều descriptor match (số nhỏ ưu tiên cao).
- Ví dụ thêm tầng phụ:

```python
'floor_descriptors': [
    {'id': 'floor1', 'labels': ['f1_pos_0'], 'y_range': [0.20, 1.0], 'priority': 5},
    {'id': 'floor2', 'labels': ['f2_pos_0'], 'y_range': [0.0, 0.19], 'priority': 10},
    {'id': 'lower_cave', 'labels': [], 'y_range': [-1.0, -0.1], 'priority': 20}
]
```

> Nếu bạn không khai báo, bot tự tạo descriptor mặc định dựa theo prefix `f1_`/`f2_` và ngưỡng Y, nhằm giữ tương thích với routine cũ.

### Disable Features

```python
# Disable point selection
'point_selection': {'enabled': False}

# Disable routine pattern
'routine_pattern': {'enabled': False}

# Disable cả hai
'routine_randomization': {'enabled': False}
```

---

## ⚠️ Notes & Limitations

1. **Variant Labels:**

    - Variant system dựa trên heuristic label names (f1_pos_0, f2_pos_1, etc.)
    - Nếu routine có label names khác, có thể cần adjust `get_variant_labels()`

2. **Loop Detection:**

    - Loop detection dựa trên heuristic (index quay về 0 hoặc < 5)
    - Có thể không hoạt động đúng với mọi routine structure

3. **Variant Switching:**

    - Variant switching chỉ xảy ra sau khi complete một loop
    - Nếu routine không có loop structure rõ ràng, variant switching có thể không hoạt động

4. **Safety First:**
    - Luôn có safety checks để không skip critical components
    - Có thể cần adjust cho routine cụ thể

---

## 🧪 Testing

### Test Point Selection:

1. Enable bot và chạy routine
2. Quan sát logs để xem có skip points không
3. Verify routine vẫn chạy đúng

### Test Variant Switching:

1. Enable bot và chạy nhiều loops
2. Quan sát logs để xem variant switch
3. Verify variant start index được set đúng

---

## 📊 Expected Results

-   **Pattern Detection:** Giảm đáng kể do không có fixed patterns
-   **Variation:** Tăng rõ rệt trong routine execution
-   **Natural Behavior:** Giống human behavior hơn
-   **Detection Risk:** Giảm đáng kể

---

## 🔄 Future Improvements

1. **Smart Variant Detection:**

    - Auto-detect routine structure
    - Generate variants dynamically

2. **Better Loop Detection:**

    - Track Jump commands để detect loops chính xác hơn

3. **Route Variation:**

    - Implement alternate routes giữa points

4. **Position Randomization:**
    - Add random offset vào target positions
