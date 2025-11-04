# 🚀 CPU & Codebase Optimization Plan - Chi tiết

## 📊 Phân tích CPU Usage Hiện tại

### **Đã Optimize (Capture Loop):**

✅ **Adaptive Frame Rate** - Giảm từ 1000 FPS → 30/10/5 FPS
✅ **Skip Template Matching** - Skip khi position không đổi
✅ **Reuse Color Conversion** - Convert BGRA→BGR một lần, reuse cho GUI

**Impact:** Giảm ~50-60% CPU trong Capture Loop

---

## 🎯 Các điểm cần tối ưu tiếp theo

### **Priority 1: HIGH IMPACT - LOW RISK** ⭐⭐⭐

#### **1.1 Bot Loop Sleep Optimization** ⏱️

**File:** `src/modules/bot.py` (line 142)

**Current:**

```python
while True:
    if config.enabled and len(config.routine) > 0:
        # ... bot logic ...
    else:
        time.sleep(0.01)  # 100 checks/second khi disabled
```

**Problem:**

-   `time.sleep(0.01)` = 100 checks/second khi bot disabled
-   Không cần check quá nhanh khi disabled
-   Wasted CPU cycles

**Optimization:**

```python
while True:
    if config.enabled and len(config.routine) > 0:
        # ... bot logic ...
        time.sleep(0.05)  # 20 Hz khi active (đủ responsive)
    else:
        time.sleep(0.2)   # 5 Hz khi disabled (đủ để detect enable)
```

**Expected Impact:**

-   Giảm CPU ~5-10% trong Bot Loop
-   Risk: LOW - Bot vẫn responsive

---

#### **1.2 Notifier Loop Optimization** 🔔

**File:** `src/modules/notifier.py` (line 113)

**Current:**

```python
while True:
    if config.enabled:
        # ... detection logic ...
        # Multiple expensive operations:
        # - cv2.cvtColor(frame, COLOR_BGR2GRAY) - mỗi loop
        # - utils.filter_color() - mỗi loop
        # - utils.multi_match() - mỗi loop
    time.sleep(0.05)  # 20 checks/second
```

**Problems:**

1. **Color conversion mỗi loop** - Không cần convert mỗi 0.05s
2. **Template matching mỗi loop** - Không cần check quá thường xuyên
3. **Sleep quá ngắn** - 20 Hz là quá nhiều cho notifier

**Optimization:**

```python
while True:
    if config.enabled:
        current_time = time.time()

        # Check black screen - mỗi 0.2s
        if current_time - last_black_check > 0.2:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # ... black screen check ...
            last_black_check = current_time

        # Check elite - mỗi 0.5s
        if current_time - last_elite_check > 0.5:
            elite_frame = frame[height // 4:3 * height // 4, width // 4:3 * width // 4]
            elite = utils.multi_match(elite_frame, ELITE_TEMPLATE, threshold=0.9)
            # ... elite check ...
            last_elite_check = current_time

        # Check other players - mỗi 0.3s
        if current_time - last_others_check > 0.3:
            filtered = utils.filter_color(minimap, OTHER_RANGES)
            others = len(utils.multi_match(filtered, OTHER_TEMPLATE, threshold=0.5))
            # ... others check ...
            last_others_check = current_time

        # Check rune - mỗi 0.5s
        if current_time - last_rune_check > 0.5:
            # ... rune check ...
            last_rune_check = current_time

    time.sleep(0.1)  # 10 Hz - đủ cho notifier
```

**Expected Impact:**

-   Giảm CPU ~15-20% trong Notifier Loop
-   Giảm unnecessary color conversions
-   Risk: LOW - Notifications vẫn timely

---

#### **1.3 GUI Minimap Display Optimization** 🖼️

**File:** `src/modules/gui.py` (line 94-98) và `src/gui/view/minimap.py`

**Current:**

```python
# GUI loop
DISPLAY_FRAME_RATE = 30  # 30 FPS
def _display_minimap(self):
    delay = 1 / GUI.DISPLAY_FRAME_RATE  # 0.033s
    while True:
        self.view.minimap.display_minimap()
        time.sleep(delay)

# Minimap display
def display_minimap(self):
    # cv2.cvtColor() - mỗi frame
    # cv2.resize() - mỗi frame
    # Multiple cv2.circle() và cv2.line() - mỗi frame
    # ImageTk.PhotoImage() - mỗi frame (expensive!)
```

**Problems:**

1. **30 FPS cho GUI** - Quá cao, mắt người không phân biệt được >15 FPS
2. **Color conversion mỗi frame** - `cv2.cvtColor(BGR2RGB)` mỗi 0.033s
3. **Resize mỗi frame** - `cv2.resize()` mỗi frame
4. **ImageTk.PhotoImage()** - Tạo object mới mỗi frame (expensive!)

**Optimization:**

```python
# GUI loop
DISPLAY_FRAME_RATE = 10  # 10 FPS - đủ smooth cho GUI
def _display_minimap(self):
    delay = 1 / GUI.DISPLAY_FRAME_RATE  # 0.1s
    while True:
        if config.enabled or config.capture.ready:  # Chỉ update khi cần
            self.view.minimap.display_minimap()
        time.sleep(delay)

# Minimap display - Cache converted image
def display_minimap(self):
    minimap = config.capture.minimap
    if minimap:
        # Cache BGR→RGB conversion
        if self.cached_minimap_hash != hash(minimap['minimap'].tobytes()):
            img = cv2.cvtColor(minimap['minimap'], cv2.COLOR_BGR2RGB)
            # Cache resize nếu size không đổi
            if self.cached_size != (width, height):
                img = cv2.resize(img, (new_width, new_height), ...)
                self.cached_size = (new_width, new_height)
            self.cached_minimap = img
            self.cached_minimap_hash = hash(minimap['minimap'].tobytes())
        else:
            img = self.cached_minimap.copy()  # Reuse cached

        # Draw on cached image
        # ... drawing operations ...

        # Only create PhotoImage if changed
        if self.cached_photo_hash != hash(img.tobytes()):
            img_photo = ImageTk.PhotoImage(Image.fromarray(img))
            # ... update canvas ...
```

**Expected Impact:**

-   Giảm CPU ~10-15% trong GUI Loop
-   Giảm memory churn từ frequent object creation
-   Risk: LOW - GUI vẫn smooth với 10 FPS

---

### **Priority 2: MEDIUM IMPACT - LOW RISK** ⭐⭐

#### **2.1 Template Matching Color Conversion Optimization** 🎨

**File:** `src/common/utils.py` (lines 83, 102)

**Current:**

```python
def single_match(frame, template):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert mỗi lần
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
    # ...

def multi_match(frame, template, threshold=0.95):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert mỗi lần
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    # ...
```

**Problem:**

-   Convert BGR→GRAY mỗi lần `multi_match()` được gọi
-   Trong Capture Loop, `multi_match()` được gọi nhiều lần với cùng frame
-   Wasted conversions

**Optimization:**

```python
# Option 1: Pre-convert frame to gray trước khi match
# Trong capture.py:
minimap_gray = cv2.cvtColor(minimap_bgr, cv2.COLOR_BGR2GRAY)
for name, tpl in PLAYER_TEMPLATES:
    player = utils.multi_match(minimap_gray, tpl, threshold=thr, is_gray=True)

# Option 2: Cache gray conversion trong utils
def multi_match(frame, template, threshold=0.95, is_gray=False):
    if not is_gray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame  # Already gray
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    # ...
```

**Expected Impact:**

-   Giảm CPU ~5-10% trong template matching
-   Risk: LOW - Chỉ thay đổi function signature

---

#### **2.2 Notifier Image Processing Optimization** 🔍

**File:** `src/modules/notifier.py` (lines 77, 88-89, 99-100)

**Current:**

```python
# Check black screen
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert mỗi loop
if np.count_nonzero(gray < 15) / height / width > threshold:
    # ...

# Check other players
filtered = utils.filter_color(minimap, OTHER_RANGES)  # Filter mỗi loop
others = len(utils.multi_match(filtered, OTHER_TEMPLATE, threshold=0.5))

# Check rune
filtered = utils.filter_color(minimap, RUNE_RANGES)  # Filter mỗi loop
matches = utils.multi_match(filtered, RUNE_TEMPLATE, threshold=0.9)
```

**Problems:**

1. **Color conversion mỗi loop** - Không cần convert mỗi 0.05s
2. **Color filtering mỗi loop** - Expensive operation
3. **Template matching mỗi loop** - Không cần check quá thường xuyên

**Optimization:** (Đã đề cập trong 1.2 - Combine với Notifier Loop Optimization)

**Expected Impact:**

-   Giảm CPU ~10-15% trong Notifier
-   Risk: LOW - Combine với 1.2

---

#### **2.3 Minimap GUI Drawing Optimization** 🎨

**File:** `src/gui/view/minimap.py` (lines 40, 42-73)

**Current:**

```python
def display_minimap(self):
    # Resize mỗi frame
    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Multiple drawing operations mỗi frame
    if rune_active:
        cv2.circle(img, ...)  # Mỗi frame

    for i in range(len(path) - 1):
        cv2.line(img, ...)  # Mỗi frame

    for p in config.routine.sequence:
        utils.draw_location(img, ...)  # Mỗi frame

    # Convert to PhotoImage mỗi frame
    img = ImageTk.PhotoImage(Image.fromarray(img))
```

**Optimization:**

```python
# Cache base minimap image
# Chỉ redraw khi path/routine thay đổi
if self.cached_path_hash != hash(str(config.path)):
    # Redraw path
    self.cached_path_hash = hash(str(config.path))

if self.cached_routine_hash != hash(str(config.routine.sequence)):
    # Redraw routine points
    self.cached_routine_hash = hash(str(config.routine.sequence))
```

**Expected Impact:**

-   Giảm CPU ~5-10% trong GUI drawing
-   Risk: LOW - Cache-based optimization

---

### **Priority 3: LOW IMPACT - MEDIUM RISK** ⭐

#### **3.1 Template Matching ROI Optimization** 🔍

**File:** `src/common/utils.py` (line 91)

**Current:**

```python
def multi_match(frame, template, threshold=0.95):
    # Match trên toàn bộ frame
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    # ...
```

**Optimization:**

```python
def multi_match(frame, template, threshold=0.95, roi=None):
    if roi:
        # Chỉ match trong ROI (Region of Interest)
        x, y, w, h = roi
        roi_frame = gray[y:y+h, x:x+w]
        result = cv2.matchTemplate(roi_frame, template, cv2.TM_CCOEFF_NORMED)
        # Adjust coordinates back to full frame
    else:
        # Full frame match
        result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
```

**Expected Impact:**

-   Giảm CPU ~15-20% khi dùng ROI
-   Risk: MEDIUM - Cần test accuracy với ROI

---

#### **3.2 Minimap Downscale for Template Matching** 📐

**File:** `src/modules/capture.py` (line 310)

**Current:**

```python
# Match với full resolution minimap
player = utils.multi_match(minimap_bgr, tpl, threshold=thr)
```

**Optimization:**

```python
# Downscale minimap for matching (75% size)
scale_factor = 0.75
small_minimap = cv2.resize(minimap_bgr, None, fx=scale_factor, fy=scale_factor)
player = utils.multi_match(small_minimap, tpl, threshold=thr)
# Scale results back up
if player:
    player[0] = (int(player[0][0] / scale_factor), int(player[0][1] / scale_factor))
```

**Expected Impact:**

-   Giảm CPU ~10-15% trong template matching
-   Risk: MEDIUM - Có thể giảm accuracy

---

### **Priority 4: CODEBASE OPTIMIZATION** 🔧

#### **4.1 Reduce Unnecessary Imports** 📦

**Check:** Các file có import không dùng đến

**Files to check:**

-   `src/modules/bot.py` - Check unused imports
-   `src/modules/notifier.py` - Check unused imports
-   `src/common/utils.py` - Check unused imports

**Expected Impact:**

-   Giảm startup time
-   Giảm memory footprint
-   Risk: LOW

---

#### **4.2 Lazy Loading** ⏳

**File:** `src/modules/notifier.py` (lines 23-37)

**Current:**

```python
# Load templates khi import module
RUNE_TEMPLATE = cv2.cvtColor(rune_filtered, cv2.COLOR_BGR2GRAY)
OTHER_TEMPLATE = cv2.cvtColor(other_filtered, cv2.COLOR_BGR2GRAY)
ELITE_TEMPLATE = cv2.imread(get_asset_path('assets/elite_template.jpg'), 0)
```

**Optimization:**

```python
# Lazy load templates
_rune_template = None
def get_rune_template():
    global _rune_template
    if _rune_template is None:
        rune_filtered = utils.filter_color(cv2.imread(...), RUNE_RANGES)
        _rune_template = cv2.cvtColor(rune_filtered, cv2.COLOR_BGR2GRAY)
    return _rune_template
```

**Expected Impact:**

-   Giảm startup time
-   Giảm memory nếu không dùng notifier
-   Risk: LOW

---

#### **4.3 Remove Debug Code** 🐛

**Check:** Các file có debug code hoặc commented code

**Files to check:**

-   `src/modules/bot.py` - Nhiều commented code (lines 119-266)
-   `src/modules/capture.py` - Check debug flags

**Expected Impact:**

-   Cleaner codebase
-   Slightly faster execution
-   Risk: LOW

---

## 📋 Implementation Checklist

### **Phase 1: Quick Wins (2-3 hours)**

-   [ ] **1.1** Bot Loop Sleep Optimization
-   [ ] **1.2** Notifier Loop Optimization
-   [ ] **1.3** GUI Minimap Display Optimization

**Expected CPU Reduction:** ~30-45% additional

---

### **Phase 2: Medium Optimizations (2-3 hours)**

-   [ ] **2.1** Template Matching Color Conversion Optimization
-   [ ] **2.2** Notifier Image Processing Optimization (combine với 1.2)
-   [ ] **2.3** Minimap GUI Drawing Optimization

**Expected CPU Reduction:** ~15-25% additional

---

### **Phase 3: Advanced (Optional) (2-3 hours)**

-   [ ] **3.1** Template Matching ROI Optimization
-   [ ] **3.2** Minimap Downscale for Template Matching

**Expected CPU Reduction:** ~10-15% additional (nếu implement)

---

### **Phase 4: Codebase Cleanup (1-2 hours)**

-   [ ] **4.1** Reduce Unnecessary Imports
-   [ ] **4.2** Lazy Loading
-   [ ] **4.3** Remove Debug Code

**Expected Impact:** Cleaner code, faster startup

---

## 🎯 Target CPU Usage

**Current (after Capture Loop optimization):** ~40-50% CPU
**After Phase 1:** ~20-30% CPU
**After Phase 2:** ~10-20% CPU
**After Phase 3:** ~5-15% CPU

**Total Reduction:** ~70-85% CPU usage

---

## ⚠️ Lưu ý

1. **Test từng optimization riêng** - Để biết impact
2. **Monitor bot performance** - Đảm bảo bot vẫn hoạt động tốt
3. **Measure before/after** - Dùng profiler để verify
4. **Balance** - Không giảm FPS quá thấp (minimum 5-10 FPS)

---

## 📊 Monitoring

**Metrics to track:**

-   CPU usage per core
-   FPS (capture loop, GUI loop)
-   Bot responsiveness
-   Memory usage
-   Template matching accuracy

**Tools:**

-   `taskmgr` (Windows) - CPU monitoring
-   `cProfile` - Detailed profiling
-   `time.time()` - FPS measurement

---

**Ready to implement?** Bắt đầu với Phase 1 để có impact lớn nhất với risk thấp nhất!
