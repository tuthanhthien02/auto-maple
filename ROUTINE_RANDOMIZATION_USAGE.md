# Hướng Dẫn Sử Dụng Routine Randomization

## ✅ Cách Sử Dụng

### **KHÔNG CẦN GUI - Features Tự Động Enable!**

2 tính năng này **đã được tích hợp tự động** khi bot start. Bạn **KHÔNG CẦN** làm gì thêm để sử dụng!

---

## 🚀 Sử Dụng Cơ Bản

### **1. Mặc Định (Đã Enable)**

-   Khi bạn chạy bot, 2 tính năng này **tự động enable**
-   **Point Selection Randomization**: 10% chance skip points
-   **Routine Pattern Randomization**: Tự động switch variants

### **2. Không Cần Thao Tác**

-   Không cần click checkbox
-   Không cần save settings
-   Chỉ cần chạy bot như bình thường

---

## ⚙️ Điều Chỉnh (Nếu Muốn)

Nếu muốn thay đổi settings, edit file:
**`src/common/anti_detect_config.py`**

### **Disable Tính Năng:**

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

'routine_pattern': {
    'enabled': False,  # Disable pattern variants
    ...
}
```

### **Điều Chỉnh Skip Probability:**

```python
'point_selection': {
    'skip_probability': 0.15,  # 15% (tăng từ 10%)
    ...
}
```

### **Điều Chỉnh Variant Weights:**

```python
'variants': {
    'normal': {'weight': 0.80},      # Tăng normal
    'reverse': {'weight': 0.10},     # Giảm reverse
    'floor1_only': {'weight': 0.05},
    'floor2_only': {'weight': 0.05}
}
```

---

## 🎯 Có Cần GUI Không?

### **❌ KHÔNG CẦN GUI**

**Lý do:**

1. ✅ Features đã **auto-enable** khi bot start
2. ✅ Settings là **advanced options** - không cần thay đổi thường xuyên
3. ✅ Edit config file đơn giản hơn
4. ✅ Tránh làm GUI phức tạp

### **Nếu Muốn Thêm GUI (Optional):**

Có thể thêm sau nếu muốn, nhưng **không bắt buộc**. Có thể:

-   Thêm section "Routine Randomization" vào Settings tab
-   Checkboxes để enable/disable
-   Sliders để điều chỉnh probability

**Nhưng hiện tại KHÔNG CẦN** - features hoạt động tốt mà không cần GUI!

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

### **Default (Recommended):**

```python
'enabled': True,              # Enable cả 2 features
'skip_probability': 0.10,     # 10% skip (safe)
'variant_switch_probability': 0.15  # 15% switch (safe)
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

1. **KHÔNG CẦN GUI** - Features tự động enable
2. **KHÔNG CẦN THAO TÁC** - Chỉ cần chạy bot
3. **CÓ THỂ ĐIỀU CHỈNH** - Edit `anti_detect_config.py` nếu muốn
4. **OPTIONAL GUI** - Có thể thêm sau nếu muốn, nhưng không cần thiết

---

## 🎯 Kết Luận

**Bạn không cần làm gì cả!** Features đã hoạt động tự động. Chỉ cần chạy bot và enjoy randomization! 🎉

Nếu muốn customize, edit config file. Nếu muốn GUI, có thể thêm sau nhưng không bắt buộc.
