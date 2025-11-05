# Cách Disable Routine Randomization Features

## 📍 Vị trí File Config

File: **`src/common/anti_detect_config.py`**

---

## 🔧 Cách Disable

### **Option 1: Disable Cả 2 Tính Năng (Khuyến Nghị)**

Edit file `src/common/anti_detect_config.py`, tìm dòng **88**:

```python
'routine_randomization': {
    'enabled': False,  # ← Đổi thành False
    'point_selection': {
        'enabled': True,
        ...
    },
    'routine_pattern': {
        'enabled': True,
        ...
    }
}
```

**→ Disable toàn bộ routine randomization**

---

### **Option 2: Disable Từng Tính Năng**

#### **Disable Point Selection Randomization:**

Edit file `src/common/anti_detect_config.py`, tìm dòng **90**:

```python
'point_selection': {
    'enabled': False,  # ← Đổi thành False
    'skip_probability': 0.10,
    ...
}
```

#### **Disable Routine Pattern Randomization:**

Edit file `src/common/anti_detect_config.py`, tìm dòng **100**:

```python
'routine_pattern': {
    'enabled': False,  # ← Đổi thành False
    'variant_switch_probability': 0.15,
    ...
}
```

---

## 📝 Ví Dụ Code Sau Khi Disable

### **Disable Cả 2:**

```python
'routine_randomization': {
    'enabled': False,  # ← Disable cả 2 tính năng
    'point_selection': {
        'enabled': True,  # Không quan trọng nếu parent disabled
        ...
    },
    'routine_pattern': {
        'enabled': True,  # Không quan trọng nếu parent disabled
        ...
    }
}
```

### **Disable Point Selection Only:**

```python
'routine_randomization': {
    'enabled': True,  # Keep enabled
    'point_selection': {
        'enabled': False,  # ← Disable chỉ Point Selection
        ...
    },
    'routine_pattern': {
        'enabled': True,  # Keep enabled
        ...
    }
}
```

### **Disable Routine Pattern Only:**

```python
'routine_randomization': {
    'enabled': True,  # Keep enabled
    'point_selection': {
        'enabled': True,  # Keep enabled
        ...
    },
    'routine_pattern': {
        'enabled': False,  # ← Disable chỉ Routine Pattern
        ...
    }
}
```

---

## ✅ Sau Khi Disable

1. **Restart bot** để áp dụng thay đổi
2. **Check logs** để verify:
    ```
    [INFO] Routine randomization initialized  ← Vẫn có này nếu enabled=True
    ```
    Nhưng sẽ không có skip hay variant switching nếu disabled

---

## 🎯 Quick Reference

| Muốn Disable        | File                    | Line | Đổi Thành          |
| ------------------- | ----------------------- | ---- | ------------------ |
| **Cả 2 tính năng**  | `anti_detect_config.py` | 88   | `'enabled': False` |
| **Point Selection** | `anti_detect_config.py` | 90   | `'enabled': False` |
| **Routine Pattern** | `anti_detect_config.py` | 100  | `'enabled': False` |

---

## ⚠️ Lưu Ý

-   **Không cần restart Python** - chỉ cần restart bot
-   **Config được load khi bot start** - thay đổi sẽ áp dụng lần start tiếp theo
-   **Nếu disable cả 2** - chỉ cần set `'enabled': False` ở level `routine_randomization`

