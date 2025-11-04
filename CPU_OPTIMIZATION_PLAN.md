# 🚀 Tối ưu CPU cho Bot - Phương án & Implementation Plan

## 📊 Phân tích CPU Usage Hiện tại

### **Top CPU Consumers:**

1. **Capture Loop (capture.py)** - ~40-60% CPU

    - `while True` loop không có sleep đủ lớn
    - Screenshot mỗi frame (mss.grab)
    - Template matching mỗi frame (cv2.matchTemplate)
    - Color conversion mỗi frame (BGRA → BGR)

2. **Template Matching (utils.py)** - ~20-30% CPU

    - `cv2.matchTemplate` được gọi nhiều lần
    - Color conversion (BGR → GRAY) cho mỗi match
    - Multiple template matching (player templates)

3. **Bot Loop (bot.py)** - ~10-15% CPU

    - `while True` với sleep(0.01) - vẫn tốn CPU
    - GUI updates
    - Activity updates

4. **GUI Updates** - ~5-10% CPU
    - Minimap resize và display
    - Image processing cho GUI

---

## 🎯 Phương án Tối ưu (Priority Order)

### **Priority 1: HIGH IMPACT - LOW RISK** ⭐⭐⭐

#### **1.1 Thêm Sleep vào Capture Loop**

**Current:** `time.sleep(0.001)` - 1000 FPS (quá nhanh!)
**Target:** `time.sleep(0.033)` - ~30 FPS (đủ cho game)

**Impact:**

-   ✅ Giảm CPU ~40-50%
-   ✅ Bot vẫn hoạt động tốt (30 FPS đủ cho minimap tracking)
-   ✅ Không ảnh hưởng gameplay

**Risk:** LOW - Chỉ giảm FPS, không ảnh hưởng logic

**Implementation:**

```python
# src/modules/capture.py line 288
time.sleep(0.033)  # 30 FPS instead of 1000 FPS
```

---

#### **1.2 Adaptive Frame Rate (Thông minh hơn)**

**Current:** Capture mỗi frame dù không cần
**Target:** Adaptive FPS dựa trên bot state

**Impact:**

-   ✅ Giảm CPU ~30-40% khi bot idle
-   ✅ Giữ FPS cao khi bot active

**Logic:**

-   Bot enabled + moving: 30 FPS
-   Bot enabled + idle: 10 FPS
-   Bot disabled: 5 FPS

**Risk:** LOW - Có thể điều chỉnh FPS dễ dàng

**Implementation:**

```python
# Adaptive sleep based on bot state
if config.enabled and len(config.path) > 0:
    time.sleep(0.033)  # 30 FPS - active
elif config.enabled:
    time.sleep(0.1)    # 10 FPS - idle
else:
    time.sleep(0.2)    # 5 FPS - disabled
```

---

#### **1.3 Skip Template Matching khi Position không đổi**

**Current:** Template matching mỗi frame dù position không đổi
**Target:** Chỉ match khi cần (position change hoặc timeout)

**Impact:**

-   ✅ Giảm CPU ~20-30% khi player stationary
-   ✅ Bot vẫn responsive khi moving

**Logic:**

-   Track last position
-   Nếu position không đổi > 0.5s, skip matching
-   Force update mỗi 1s để detect nếu stuck

**Risk:** LOW - Có timeout để detect stuck

**Implementation:**

```python
last_pos = None
last_pos_time = time.time()
pos_update_interval = 0.5  # Force update every 0.5s

if player:
    current_pos = utils.convert_to_relative(player[0], minimap)
    if current_pos != last_pos or (time.time() - last_pos_time) > pos_update_interval:
        config.player_pos = current_pos
        last_pos = current_pos
        last_pos_time = time.time()
```

---

### **Priority 2: MEDIUM IMPACT - LOW RISK** ⭐⭐

#### **2.1 Tối ưu Color Conversion**

**Current:** Convert BGRA → BGR → GRAY mỗi frame
**Target:** Convert trực tiếp BGRA → GRAY (bỏ BGR step)

**Impact:**

-   ✅ Giảm CPU ~5-10%
-   ✅ Giảm memory allocation

**Risk:** LOW - Chỉ tối ưu conversion

**Implementation:**

```python
# Current: 2 conversions
minimap_bgr = cv2.cvtColor(minimap, cv2.COLOR_BGRA2BGR)
gray = cv2.cvtColor(minimap_bgr, cv2.COLOR_BGR2GRAY)

# Optimized: 1 conversion
minimap_gray = cv2.cvtColor(minimap, cv2.COLOR_BGRA2GRAY)
```

---

#### **2.2 Cache Converted Minimap**

**Current:** Convert minimap mỗi frame
**Target:** Cache converted minimap, chỉ convert khi minimap thay đổi

**Impact:**

-   ✅ Giảm CPU ~5-10%
-   ✅ Giảm memory churn

**Risk:** LOW - Cần hash để detect thay đổi

**Implementation:**

```python
self.cached_minimap_gray = None
self.cached_minimap_hash = None

minimap_hash = hash(minimap.tobytes())
if minimap_hash != self.cached_minimap_hash:
    self.cached_minimap_gray = cv2.cvtColor(minimap, cv2.COLOR_BGRA2GRAY)
    self.cached_minimap_hash = minimap_hash
```

---

#### **2.3 Tối ưu Bot Loop Sleep**

**Current:** `time.sleep(0.01)` - 100 checks/second
**Target:** Adaptive sleep dựa trên state

**Impact:**

-   ✅ Giảm CPU ~5-10%
-   ✅ Responsive hơn khi cần

**Logic:**

-   Bot enabled: sleep(0.05) - 20 checks/second
-   Bot disabled: sleep(0.1) - 10 checks/second

**Risk:** LOW - Bot vẫn responsive

**Implementation:**

```python
# src/modules/bot.py line 142
if config.enabled:
    time.sleep(0.05)  # 20 Hz when active
else:
    time.sleep(0.1)    # 10 Hz when idle
```

---

### **Priority 3: LOW IMPACT - MEDIUM RISK** ⭐

#### **3.1 Downscale Minimap cho Template Matching**

**Current:** Match với full resolution minimap
**Target:** Downscale minimap trước khi match (giảm resolution)

**Impact:**

-   ✅ Giảm CPU ~10-15%
-   ⚠️ Có thể giảm accuracy

**Risk:** MEDIUM - Cần test accuracy

**Implementation:**

```python
# Downscale minimap for matching (keep template original)
scale_factor = 0.75  # 75% size
small_minimap = cv2.resize(minimap_gray, None, fx=scale_factor, fy=scale_factor)
result = cv2.matchTemplate(small_minimap, template, cv2.TM_CCOEFF_NORMED)
# Scale results back up
```

---

#### **3.2 ROI-based Template Matching**

**Current:** Match trên toàn bộ minimap
**Target:** Chỉ match trong ROI (Region of Interest) quanh last position

**Impact:**

-   ✅ Giảm CPU ~15-20%
-   ⚠️ Có thể miss nếu teleport xa

**Risk:** MEDIUM - Cần fallback full match

**Implementation:**

```python
# Only match in ROI around last position
roi_size = 50  # pixels
if last_pos:
    roi_x = max(0, last_pos[0] - roi_size)
    roi_y = max(0, last_pos[1] - roi_size)
    roi = minimap_gray[roi_y:roi_y+roi_size*2, roi_x:roi_x+roi_size*2]
    # Match in ROI
else:
    # Full match if no last position
```

---

#### **3.3 Lazy GUI Updates**

**Current:** GUI update mỗi frame
**Target:** Update GUI mỗi 0.1s (10 FPS cho GUI)

**Impact:**

-   ✅ Giảm CPU ~5-10%
-   ✅ GUI vẫn smooth

**Risk:** LOW - GUI không cần 30 FPS

**Implementation:**

```python
# GUI update every 0.1s
last_gui_update = time.time()
if time.time() - last_gui_update > 0.1:
    # Update GUI
    last_gui_update = time.time()
```

---

### **Priority 4: ADVANCED OPTIMIZATIONS** 🔧

#### **4.1 Multi-threading Template Matching**

**Current:** Sequential template matching
**Target:** Parallel template matching với threading

**Impact:**

-   ✅ Giảm CPU time ~20-30% (với multi-core)
-   ⚠️ Complexity cao hơn

**Risk:** HIGH - Cần threading safe

---

#### **4.2 GPU Acceleration (OpenCV CUDA)**

**Current:** CPU-based template matching
**Target:** GPU-accelerated matching

**Impact:**

-   ✅ Giảm CPU ~30-50%
-   ⚠️ Cần GPU + CUDA setup

**Risk:** MEDIUM - Dependency issues

---

## 📋 Implementation Plan

### **Phase 1: Quick Wins (1-2 hours)**

✅ **1.1** Thêm Sleep vào Capture Loop
✅ **1.2** Adaptive Frame Rate
✅ **2.3** Tối ưu Bot Loop Sleep

**Expected CPU Reduction:** ~50-60%

---

### **Phase 2: Medium Optimizations (2-3 hours)**

✅ **1.3** Skip Template Matching khi Position không đổi
✅ **2.1** Tối ưu Color Conversion
✅ **2.2** Cache Converted Minimap

**Expected CPU Reduction:** ~15-20% additional

---

### **Phase 3: Advanced (Optional)**

-   **3.1** Downscale Minimap
-   **3.2** ROI-based Matching
-   **3.3** Lazy GUI Updates

**Expected CPU Reduction:** ~10-15% additional

---

## 🎯 Target CPU Usage

**Current:** ~70-90% CPU (single core)
**Target:** ~20-30% CPU (single core)

**Reduction:** ~60-70% CPU usage

---

## ⚠️ Lưu ý

1. **Test từng optimization riêng** - Để biết impact
2. **Monitor bot performance** - Đảm bảo bot vẫn hoạt động tốt
3. **Có thể rollback** - Mỗi optimization nên có flag để enable/disable
4. **Balance** - Không giảm FPS quá thấp (minimum 10 FPS)

---

## ✅ Checklist

-   [ ] **Phase 1:** Quick Wins
    -   [ ] 1.1 Sleep trong Capture Loop
    -   [ ] 1.2 Adaptive Frame Rate
    -   [ ] 2.3 Bot Loop Sleep
-   [ ] **Phase 2:** Medium Optimizations
    -   [ ] 1.3 Skip Template Matching
    -   [ ] 2.1 Color Conversion Optimization
    -   [ ] 2.2 Cache Minimap
-   [ ] **Phase 3:** Advanced (Optional)
    -   [ ] 3.1 Downscale Minimap
    -   [ ] 3.2 ROI Matching
    -   [ ] 3.3 Lazy GUI

---

## 📊 Monitoring

**Metrics to track:**

-   CPU usage per core
-   FPS (capture loop)
-   Bot responsiveness (time to detect position change)
-   Memory usage
-   Template matching accuracy

**Tools:**

-   `taskmgr` (Windows) - CPU monitoring
-   `time.time()` - FPS measurement
-   Profiler (cProfile) - Detailed analysis

---

**Ready to implement?** Bắt đầu với Phase 1 (Quick Wins) để có impact lớn nhất với risk thấp nhất!
