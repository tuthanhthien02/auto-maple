# 🔍 So Sánh: bot-root.py vs bot.py

## 📊 **TỔNG QUAN**

-   **`bot-root.py`**: File bot gốc (original version)
-   **`bot.py`**: File bot hiện tại (current version với các cải tiến)

---

## 🔄 **KHÁC BIỆT CHÍNH**

### **1. Imports**

#### **bot-root.py (Gốc):**

```python
from src.common.vkeys import press, click
```

#### **bot.py (Hiện tại):**

```python
from src.common.anti_detect import initialize_anti_detect, cleanup_anti_detect, update_activity, get_human_delay
from src.common.process_stealth import enable_process_stealth, disable_process_stealth
from src.common.screenshot_blocker import enable_screenshot_blocking, disable_screenshot_blocking, protect_maplestory_window
from src.common.vkeys import press, click, press_with_behavioral_pause
from src.common.logger import get_logger

log = get_logger(__name__)
```

**Khác biệt:**

-   ✅ **Thêm anti-detect imports**
-   ✅ **Thêm process stealth imports**
-   ✅ **Thêm screenshot blocker imports**
-   ✅ **Thêm logger** (thay vì dùng `print()`)

---

### **2. start() Method**

#### **bot-root.py (Gốc):**

```python
def start(self):
    self.update_submodules()
    print('\n[~] Started main bot loop')
    self.thread.start()
```

#### **bot.py (Hiện tại):**

```python
def start(self):
    # Initialize anti-detect features
    initialize_anti_detect()

    # Routine randomization - DISABLED
    # initialize_routine_randomization()

    # Enable process stealth (optional) - DISABLED to reduce NGS detection risk
    # Process stealth features (hide console, memory obfuscation, process monitoring)
    # can trigger NGS detection as they are common automation tool signatures
    # try:
    #     enable_process_stealth()
    # except Exception as e:
    #     log.warning("Failed to enable process stealth: %s", e)

    # Enable screenshot blocking (recommended) - DISABLED TEMPORARILY
    # try:
    #     enable_screenshot_blocking()
    #     protect_maplestory_window()
    #     print("[Bot] Screenshot blocking enabled")
    # except Exception as e:
    #     print(f"[Bot] Failed to enable screenshot blocking: {e}")

    # tạm tắt cập nhật recoures
    # self.update_submodules()
    # print('\n[~] Started main bot loop')
    self.thread.start()
```

**Khác biệt:**

-   ✅ **Thêm anti-detect initialization**
-   ✅ **Process stealth disabled** (để giảm NGS detection risk)
-   ✅ **Screenshot blocking disabled**
-   ✅ **update_submodules disabled** (tạm thời)

---

### **3. \_main() Method**

#### **bot-root.py (Gốc):**

```python
def _main(self):
    print('\n[~] Initializing detection algorithm:\n')
    model = detection.load_model()
    print('\n[~] Initialized detection algorithm')

    self.ready = True
    config.listener.enabled = True
    last_fed = time.time()

    while True:
        if config.enabled and len(config.routine) > 0:
            # Buff and feed pets
            self.command_book.buff.main()
            pet_settings = config.gui.settings.pets
            auto_feed = pet_settings.auto_feed.get()
            num_pets = pet_settings.num_pets.get()
            now = time.time()
            if auto_feed and now - last_fed > 1200 / num_pets:
                press(self.config['Feed pet'], 1)
                last_fed = now

            # Highlight the current Point
            config.gui.view.routine.select(config.routine.index)
            config.gui.view.details.display_info(config.routine.index)

            # Execute next Point in the routine
            element = config.routine[config.routine.index]
            if self.rune_active and isinstance(element, Point) \
                    and element.location == self.rune_closest_pos:
                self._solve_rune(model)
            element.execute()
            config.routine.step()
        else:
            time.sleep(0.01)
```

#### **bot.py (Hiện tại):**

```python
def _main(self):
    log.info("Initializing detection algorithm")
    # model = detection.load_model()  # Disabled: rune solving turned off
    model = None
    log.info("Detection algorithm disabled (rune solving off)")

    self.ready = True
    config.listener.enabled = True
    last_fed = time.time()
    last_activity_update = time.time()

    # Variant switching - DISABLED
    # Routine starts from index 0 (normal behavior)

    while True:
        if config.enabled and len(config.routine) > 0:
            # Update activity for anti-detect
            current_time = time.time()
            if current_time - last_activity_update > 1.0:  # Update every second
                update_activity()
                last_activity_update = current_time

            # Buff and feed pets
            # self.command_book.buff.main()  # Disabled: auto buff turned off
            # Auto feed pet - Disabled
            # pet_settings = config.gui.settings.pets
            # auto_feed = pet_settings.auto_feed.get()
            # num_pets = pet_settings.num_pets.get()
            # now = time.time()
            # if auto_feed and now - last_fed > 1200 / num_pets:
            #     press(self.config['Feed pet'], 1)
            #     last_fed = now

            # Highlight the current Point
            config.gui.view.routine.select(config.routine.index)
            config.gui.view.details.display_info(config.routine.index)

            # Execute next Point in the routine
            element = config.routine[config.routine.index]
            # Disabled: rune solving turned off
            # if self.rune_active and isinstance(element, Point) \
            #         and element.location == self.rune_closest_pos:
            #     self._solve_rune(model)
            element.execute()
            config.routine.step()
            # CPU Optimization: Adaptive sleep - 20 Hz when active (sufficient responsiveness)
            time.sleep(0.05)
        else:
            # CPU Optimization: Lower frequency when disabled - 5 Hz (enough to detect enable)
            time.sleep(0.2)
```

**Khác biệt:**

-   ✅ **Model disabled** - Rune solving turned off (`model = None`)
-   ✅ **Buff disabled** - Auto buff turned off
-   ✅ **Auto feed pet disabled**
-   ✅ **Rune solving disabled**
-   ✅ **Thêm activity update** cho anti-detect (mỗi 1 giây)
-   ✅ **CPU Optimization** - Adaptive sleep:
    -   Active: `time.sleep(0.05)` (20 Hz)
    -   Disabled: `time.sleep(0.2)` (5 Hz)
-   ✅ **Dùng logger** thay vì `print()`

---

### **4. \_solve_rune() Method**

#### **bot-root.py (Gốc):**

```python
print('\nSolving rune:')
inferences = []
for _ in range(15):
    frame = config.capture.frame
    solution = detection.merge_detection(model, frame)
    if solution:
        print(', '.join(solution))
        if solution in inferences:
            print('Solution found, entering result')
            # ...
            rune_buff = utils.multi_match(frame[:frame.shape[0] // 8, :],
                                          RUNE_BUFF_TEMPLATE,
                                          threshold=0.9)
```

#### **bot.py (Hiện tại):**

```python
log.info("Solving rune")
inferences = []
for _ in range(15):
    frame = config.capture.frame
    solution = detection.merge_detection(model, frame)
    if solution:
        log.info(", ".join(solution))
        if solution in inferences:
            log.info("Solution found, entering result")
            # ...
            # CPU Optimization: Pre-convert to grayscale once
            frame_top_gray = cv2.cvtColor(frame[:frame.shape[0] // 8, :], cv2.COLOR_BGR2GRAY)
            rune_buff = utils.multi_match(frame_top_gray, RUNE_BUFF_TEMPLATE, threshold=0.9, is_gray=True)
```

**Khác biệt:**

-   ✅ **Dùng logger** (`log.info()`) thay vì `print()`
-   ✅ **CPU Optimization** - Pre-convert to grayscale một lần thay vì convert mỗi lần

---

### **5. update_submodules() Method**

#### **bot-root.py (Gốc):**

```python
utils.print_separator()
print('[~] Retrieving latest submodules:')
# ...
print(f" -  Initialized submodule '{path}'")
# ...
print(f" -  Updated submodule '{path}', restored local changes")
# ...
print(f" -  Updated submodule '{path}'")
# ...
print(f" -  Rebuilt submodule '{path}'")
```

#### **bot.py (Hiện tại):**

```python
utils.print_separator()
log.info("Retrieving latest submodules")
# ...
log.info("Initialized submodule '%s'", path)
# ...
log.info("Updated submodule '%s', restored local changes", path)
# ...
log.info("Updated submodule '%s'", path)
# ...
log.info("Rebuilt submodule '%s'", path)
```

**Khác biệt:**

-   ✅ **Dùng logger** (`log.info()`) thay vì `print()`
-   ✅ **String formatting** với `%s` thay vì f-strings

---

## 📋 **TỔNG KẾT KHÁC BIỆT**

| Feature                 | bot-root.py (Gốc) | bot.py (Hiện tại)              |
| ----------------------- | ----------------- | ------------------------------ |
| **Anti-Detect**         | ❌ Không có       | ✅ Có (initialized)            |
| **Process Stealth**     | ❌ Không có       | ⚠️ Disabled (NGS risk)         |
| **Screenshot Blocking** | ❌ Không có       | ⚠️ Disabled                    |
| **Logger**              | ❌ Dùng `print()` | ✅ Dùng `log.info()`           |
| **Model Loading**       | ✅ Enabled        | ❌ Disabled (rune solving off) |
| **Auto Buff**           | ✅ Enabled        | ❌ Disabled                    |
| **Auto Feed Pet**       | ✅ Enabled        | ❌ Disabled                    |
| **Rune Solving**        | ✅ Enabled        | ❌ Disabled                    |
| **Activity Update**     | ❌ Không có       | ✅ Có (anti-detect)            |
| **CPU Optimization**    | ❌ Không có       | ✅ Adaptive sleep              |
| **update_submodules**   | ✅ Enabled        | ⚠️ Disabled (tạm thời)         |

---

## 🎯 **CÁC CẢI TIẾN TRONG bot.py**

### **1. Anti-Detection Features**

-   ✅ Initialize anti-detect để giảm detection risk
-   ✅ Activity update để track hoạt động

### **2. NGS Detection Prevention**

-   ✅ Disable process stealth (HIGH RISK trigger NGS)
-   ✅ Disable screenshot blocking (tạm thời)

### **3. Performance Optimization**

-   ✅ CPU Optimization với adaptive sleep
-   ✅ Pre-convert to grayscale trong rune solving (nếu enabled)

### **4. Logging System**

-   ✅ Dùng logger thay vì `print()` (professional hơn)
-   ✅ Structured logging với log levels

### **5. Feature Disabling**

-   ✅ Disable các features không cần thiết:
    -   Model loading (rune solving)
    -   Auto buff
    -   Auto feed pet
    -   Rune solving

---

## ⚠️ **LƯU Ý**

### **Các Features Đã Disable:**

1. **Process Stealth** - Disabled để giảm NGS detection risk
2. **Screenshot Blocking** - Disabled tạm thời
3. **update_submodules** - Disabled tạm thời
4. **Model Loading** - Disabled (rune solving off)
5. **Auto Buff** - Disabled
6. **Auto Feed Pet** - Disabled
7. **Rune Solving** - Disabled

### **Các Features Đã Thêm:**

1. ✅ **Anti-Detect Initialization** - Giảm detection risk
2. ✅ **Activity Update** - Track hoạt động cho anti-detect
3. ✅ **CPU Optimization** - Adaptive sleep để giảm CPU usage
4. ✅ **Logger System** - Professional logging

---

## 🔧 **KHUYẾN NGHỊ**

### **Nếu Muốn Enable Lại Các Features:**

1. **Auto Buff và Auto Feed Pet:**

    - Uncomment code trong `_main()` method

2. **Rune Solving:**

    - Uncomment `model = detection.load_model()`
    - Uncomment rune solving logic

3. **update_submodules:**
    - Uncomment `self.update_submodules()` trong `start()`

### **Nếu Muốn Disable Thêm:**

1. **Anti-Detect:**

    - Comment `initialize_anti_detect()`

2. **Activity Update:**
    - Comment activity update code trong `_main()`

---

**REMEMBER:** bot.py hiện tại đã được tối ưu cho NGS detection prevention và performance optimization!
