# Hướng Dẫn Sử Dụng Routine Randomization

## ✅ Cách Sử Dụng

### **Tùy Chọn – Mặc định đang TẮT**

Point Selection và Routine Pattern hiện **tắt mặc định** để giảm rủi ro cho người dùng mới. Bạn cần bật thủ công (qua GUI hoặc config) khi muốn sử dụng.

---

## 🚀 Sử Dụng Cơ Bản

### **1. Bật Qua GUI (khuyến nghị)**

-   Vào `Settings > Routine Randomization`
-   Tick `Enable Point Selection Randomization` hoặc `Enable Routine Pattern Variation`
-   Điều chỉnh slider theo ý muốn (skip 10% mặc định, floor-only 10% chance)

### **2. Bật Qua Config (headless)**

-   Mở `src/common/anti_detect_config.py`
-   Thay đổi các khóa:
    ```python
    'routine_randomization': {
        'enabled': True,
        'point_selection': {'enabled': True, 'skip_probability': 0.10},
        'routine_pattern': {
            'enabled': True,
            'floor_variant_chance': 0.10,
            'variants': {
                'normal': {'weight': 0.70},
                'reverse': {'weight': 0.15},
                'floor1_only': {'weight': 0.10},
                'floor2_only': {'weight': 0.05},
            }
        }
    }
    ```

---

## ⚙️ Điều Chỉnh (Nếu Muốn)

Nếu muốn thay đổi settings, edit file:
**`src/common/anti_detect_config.py`**

### **Bật/Tắt từng phần:**

```python
# Disable cả routine randomization
'routine_randomization': {
    'enabled': False,  # ← Đổi thành False
    ...
}

# Hoặc disable từng phần
'point_selection': {
    'enabled': False,  # Disable point selection
    ...
}

'routine_pattern': {'enabled': True, ...}
```

### **Điều Chỉnh Skip Probability:**

```python
'point_selection': {
    'skip_probability': 0.15,  # 15% (tăng từ 10%)
    ...
}
```

### **Điều Chỉnh Variant Weights & Floor Chance:**

```python
'floor_variant_chance': 0.15
'variants': {
    'normal': {'weight': 0.80},
    'reverse': {'weight': 0.10},
    'floor1_only': {'weight': 0.05},
    'floor2_only': {'weight': 0.05},
}
```

---

## 🎯 GUI và Config – khi nào dùng?

-   **GUI**: Bật/tắt nhanh trong lúc chạy, lưu giá trị vào file config GUI → phù hợp khi test variation.
-   **Config**: Dùng cho môi trường không có GUI (Auto Maple chạy headless) hoặc cần commit cấu hình chung.

---

## 📊 Xem Logs Để Verify

Khi bot chạy, bạn sẽ thấy logs trong console:

```
[INFO] Routine randomization initialized
[DEBUG] Skipping point at index 5
[INFO] Switched to routine variant: reverse
```

---

## 🔧 Quick Settings Guide

### **Default (Safe – Do Nothing):**

```python
'enabled': False,             # Giữ nguyên để tránh thay đổi routine
'skip_probability': 0.10,     # Giá trị sẽ dùng khi bạn bật
'variant_switch_probability': 0.15,
'floor_variant_chance': 0.10,
```

### **More Randomization (More Variation):**

```python
'skip_probability': 0.15,              # 15% skip
'variant_switch_probability': 0.25,    # 25% switch
```

### **Less Randomization (Safer):**

```python
'skip_probability': 0.05,              # 5% skip
'variant_switch_probability': 0.10,    # 10% switch
```

### **Disable Completely:**

```python
'enabled': False  # Disable cả 2 features
```

---

## ✅ Tóm Lại

1. **Mặc định tắt** – không ảnh hưởng routine hiện tại.
2. **Bật qua GUI** nếu cần test nhanh (khuyến nghị).
3. **Bật qua config** khi chạy headless hoặc muốn commit cấu hình.
4. **Tuỳ chỉnh trọng số** để đa dạng nhưng hãy theo dõi log để đảm bảo lộ trình hợp lệ.

---

## 🎯 Kết Luận

**Tuỳ chọn hoàn toàn.** Chỉ bật khi routine và cấu hình sẵn sàng. Sau khi bật, theo dõi log để chắc chắn bot di chuyển đúng mong đợi.

---

## 🔍 Công cụ hỗ trợ nhanh

-   Mô phỏng tại chỗ, xem thống kê skip/backward và chuyển variant:

    ```bash
    python -m tools.randomization_diagnostics --routine resources/routines/your_routine.csv --loops 10 --enable-skip --enable-pattern
    ```

    Thống kê giúp bạn kiểm tra trước khi chạy bot thật (số vòng hoàn thành, variant hiện hành, chuyển đổi…).

-   Bật thêm command randomization (shuffle/skip/wait nhẹ):

    ```python
    'routine_randomization': {
        'command_sequence': {
            'enabled': True,
            'shuffle_probability': 0.3,
            'skip_probability': 0.08,
            'extra_wait_probability': 0.2
        }
    }
    ```

    Sau khi bật, theo dõi log `Point:` để chắc rằng command critical (Teleport/Adjust…) không bị bỏ qua.

-   Mô tả tầng bằng floor descriptors (hỗ trợ nhiều tầng hơn 2):

    ```python
    'routine_randomization': {
        'floor_descriptors': [
            {'id': 'floor1', 'labels': ['f1_pos_0', 'f1_pos_1'], 'y_range': [0.18, 1.0]},
            {'id': 'floor2', 'labels': ['f2_pos_0', 'f2_pos_1'], 'y_range': [-1.0, 0.17]},
            {'id': 'upper', 'labels': ['roof_entry'], 'priority': 5}
        ]
    }
    ```

    Bot sẽ ưu tiên match theo `labels`, sau đó `y_range`; `priority` giúp giải quyết tình huống nhiều descriptor trùng nhau.
