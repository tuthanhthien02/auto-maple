# Plan: On/Off Routine Randomization Settings trên GUI (Đơn Giản)

## 📋 Mục Tiêu

Thêm 2 checkboxes trên GUI Settings tab để on/off:

1. **Point Selection Randomization** (enable/disable)
2. **Routine Pattern Randomization** (enable/disable)

---

## 🎯 Approach: Đơn Giản Nhất (Giống Pets)

### **Pattern Hiện Tại (Pets):**

-   ✅ 1 file duy nhất: `src/gui/settings/pets.py`
-   ✅ Chứa cả GUI component VÀ Settings class
-   ✅ Settings class extends `Configurable` → auto save/load
-   ✅ Thêm vào Settings tab là xong

### **Áp Dụng Cho Routine Randomization:**

-   Tạo 1 file: `src/gui/settings/routine_randomization.py`
-   Chứa: GUI component + Settings class (giống Pets)
-   Khi change → save settings + sync với `anti_detect_config.py`
-   Thêm vào `src/gui/settings/main.py`

---

## 📁 Files Structure

```
src/
├── gui/
│   └── settings/
│       ├── main.py                        # Thêm 1 dòng import + 1 dòng pack()
│       └── routine_randomization.py      # NEW: GUI + Settings (1 file)
.settings/
└── routine_randomization                 # Auto-generated (pickle)
```

**Chỉ cần:**

-   ✅ 1 file mới
-   ✅ 2 dòng code trong main.py
-   ✅ Không cần tạo thêm folder/class phức tạp

---

## 🔄 Data Flow

```
User clicks checkbox
    ↓
routine_randomization.py (GUI) saves settings
    ↓
.settings/routine_randomization (auto save bởi Configurable)
    ↓
Sync với ANTI_DETECT_CONFIG
    ↓
Randomization behavior changes
```

---

## 📝 Implementation Details

### **1. File: `src/gui/settings/routine_randomization.py`**

```python
import tkinter as tk
from src.gui.interfaces import LabelFrame
from src.common.interfaces import Configurable

class RoutineRandomization(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Routine Randomization', **kwargs)

        self.settings = RoutineRandomizationSettings('routine_randomization')

        # Load từ settings file
        point_enabled = self.settings.get('Point Selection Enabled')
        pattern_enabled = self.settings.get('Routine Pattern Enabled')

        # Create checkboxes
        self.point_var = tk.BooleanVar(value=point_enabled)
        self.pattern_var = tk.BooleanVar(value=pattern_enabled)

        tk.Checkbutton(
            self,
            variable=self.point_var,
            text='Point Selection Randomization',
            command=self._on_change
        ).pack(side=tk.TOP, anchor='w', padx=5, pady=2)

        tk.Checkbutton(
            self,
            variable=self.pattern_var,
            text='Routine Pattern Randomization',
            command=self._on_change
        ).pack(side=tk.TOP, anchor='w', padx=5, pady=2)

    def _on_change(self):
        # Save to settings file
        self.settings.set('Point Selection Enabled', self.point_var.get())
        self.settings.set('Routine Pattern Enabled', self.pattern_var.get())
        self.settings.save_config()

        # Sync với anti_detect_config
        self._sync_to_anti_detect()

    def _sync_to_anti_detect(self):
        """Sync settings to ANTI_DETECT_CONFIG."""
        from src.common.anti_detect_config import ANTI_DETECT_CONFIG
        ANTI_DETECT_CONFIG['routine_randomization']['point_selection']['enabled'] = \
            self.settings.get('Point Selection Enabled')
        ANTI_DETECT_CONFIG['routine_randomization']['routine_pattern']['enabled'] = \
            self.settings.get('Routine Pattern Enabled')


class RoutineRandomizationSettings(Configurable):
    DEFAULT_CONFIG = {
        'Point Selection Enabled': True,
        'Routine Pattern Enabled': True
    }

    def get(self, key):
        return self.config[key]

    def set(self, key, value):
        assert key in self.config
        self.config[key] = value
```

### **2. File: `src/gui/settings/main.py`**

```python
# Thêm import
from src.gui.settings.routine_randomization import RoutineRandomization

# Trong __init__, sau self.pets:
self.routine_randomization = RoutineRandomization(self.column1)
self.routine_randomization.pack(side=tk.TOP, fill='x', expand=True, pady=(10, 0))
```

### **3. Load Settings Khi Bot Start (Optional - nếu cần)**

Nếu muốn load settings TRƯỚC khi bot start, có thể thêm vào `src/modules/bot.py`:

```python
def start(self):
    # ... existing code ...

    # Load routine randomization settings và sync
    from src.gui.settings.routine_randomization import RoutineRandomizationSettings
    from src.common.anti_detect_config import ANTI_DETECT_CONFIG

    settings = RoutineRandomizationSettings('routine_randomization')
    ANTI_DETECT_CONFIG['routine_randomization']['point_selection']['enabled'] = \
        settings.get('Point Selection Enabled')
    ANTI_DETECT_CONFIG['routine_randomization']['routine_pattern']['enabled'] = \
        settings.get('Routine Pattern Enabled')
```

**Lưu ý:** Nếu GUI load trước thì không cần bước này vì GUI đã sync rồi.

---

## ✅ Advantages

1. **Đơn Giản:**

    - ✅ Chỉ 1 file mới
    - ✅ 2 dòng code trong main.py
    - ✅ Không cần folder/class phức tạp

2. **Consistent:**

    - ✅ Giống pattern Pets (đã có sẵn)
    - ✅ Dễ maintain

3. **Auto Persist:**

    - ✅ Configurable class tự động save/load
    - ✅ Không cần implement thêm logic

4. **GUI Ready:**
    - ✅ Checkboxes hiển thị ngay
    - ✅ Toggle → auto save → auto sync

---

## ⚠️ Considerations

1. **Sync Strategy:**

    - Khi GUI load → load settings → sync với `anti_detect_config`
    - Khi user change → save settings → sync với `anti_detect_config`
    - Code khác vẫn dùng `is_feature_enabled()` như cũ

2. **Initialization:**

    - GUI load trước → settings được load → sync với config
    - Bot start sau → đọc config (đã được sync)

3. **Backward Compatibility:**
    - Nếu không có settings file → use defaults (True, True)
    - Settings file corrupt → use defaults

---

## 📊 Summary

| Aspect              | Simple Plan                         |
| ------------------- | ----------------------------------- |
| **Files to Create** | 1 file (`routine_randomization.py`) |
| **Files to Modify** | 1 file (`main.py` - 2 dòng)         |
| **Complexity**      | ✅ Very Low                         |
| **Consistency**     | ✅ High (giống Pets)                |
| **Persistence**     | ✅ Auto (Configurable)              |
| **GUI Ready**       | ✅ Yes                              |

**→ Đơn giản, nhanh, hiệu quả!**
