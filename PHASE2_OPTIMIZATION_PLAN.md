# 🚀 Phase 2 Optimization Plan - Medium Optimizations

## 📋 Tổng quan

**Phase 2:** Medium Impact - Low Risk optimizations  
**Expected CPU Reduction:** ~15-25% additional  
**Time Estimate:** 2-3 hours

---

## 🎯 Phase 2 Tasks

### **2.1 Template Matching Color Conversion Optimization** 🎨

**File:** `src/common/utils.py` (lines 91-111)

**Current Problem:**

```python
def multi_match(frame, template, threshold=0.95):
    # Convert BGR→GRAY mỗi lần được gọi
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Expensive!
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    # ...
```

**Issue:**

-   `multi_match()` được gọi nhiều lần với cùng frame
-   Trong `capture.py`: gọi với `minimap_bgr` (đã convert BGR)
-   Nhưng `multi_match()` lại convert BGR→GRAY mỗi lần
-   Trong `notifier.py`: cũng gọi với frames đã convert
-   Wasted conversions

**Call Sites:**

1. `capture.py:310` - Player template matching (multiple templates)
2. `notifier.py:94` - Elite template matching
3. `notifier.py:102` - Other players template matching
4. `notifier.py:115` - Rune template matching
5. `bot.py:178` - Rune buff template matching (disabled)

**Optimization Strategy:**

**Option A: Add `is_gray` Parameter** (Recommended)

```python
def multi_match(frame, template, threshold=0.95, is_gray=False):
    if not is_gray:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    else:
        gray = frame  # Already gray
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    # ...
```

**Benefits:**

-   Backward compatible (default `is_gray=False`)
-   Callers có thể pre-convert và pass `is_gray=True`
-   Minimal code changes

**Option B: Pre-convert in Callers** (Alternative)

-   Convert BGR→GRAY trong `capture.py` trước khi match
-   Convert trong `notifier.py` trước khi match
-   Pass gray frame vào `multi_match()`

**Implementation:**

1. Modify `multi_match()` to accept `is_gray` parameter
2. Modify `capture.py` to pre-convert gray cho player matching
3. Modify `notifier.py` to pre-convert gray cho elite/others/rune matching
4. Update `single_match()` similarly (if used)

**Expected Impact:**

-   Giảm CPU ~5-10% trong template matching
-   Giảm redundant color conversions
-   Risk: LOW - Backward compatible

---

### **2.2 Notifier Image Processing Cache** 🔍

**File:** `src/modules/notifier.py` (lines 84-89)

**Current Problem:**

```python
# CPU Optimization: Check black screen every 0.2s (5 Hz)
if current_time - last_black_check > 0.2:
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert mỗi 0.2s
    if np.count_nonzero(gray < 15) / height / width > self.room_change_threshold:
        self._alert('siren')
    last_black_check = current_time
```

**Issue:**

-   Convert BGR→GRAY mỗi 0.2s cho black screen check
-   Frame có thể không thay đổi giữa các checks
-   Có thể cache gray conversion

**Optimization:**

```python
# Cache gray frame
cached_frame_hash = None
cached_gray = None

# CPU Optimization: Check black screen every 0.2s (5 Hz)
if current_time - last_black_check > 0.2:
    # Only convert if frame changed
    frame_hash = hash(frame.tobytes())
    if frame_hash != cached_frame_hash:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cached_gray = gray
        cached_frame_hash = frame_hash
    else:
        gray = cached_gray

    if np.count_nonzero(gray < 15) / height / width > self.room_change_threshold:
        self._alert('siren')
    last_black_check = current_time
```

**Expected Impact:**

-   Giảm CPU ~2-5% trong Notifier (black screen check)
-   Risk: LOW - Cache-based optimization

**Note:** Optimization này có thể không cần thiết nếu frame thay đổi mỗi 0.2s. Cần test để verify.

---

### **2.3 Minimap GUI Drawing Optimization** 🖼️

**File:** `src/gui/view/minimap.py` (lines 28-104)

**Current State (after Phase 1):**

-   ✅ Base minimap đã được cache (convert BGR→RGB và resize)
-   ✅ Chỉ convert/resize khi minimap data thay đổi
-   ⚠️ Vẫn tạo `ImageTk.PhotoImage()` mỗi frame (expensive!)
-   ⚠️ Vẫn vẽ path/rune/player_pos mỗi frame (ngay cả khi không đổi)

**Remaining Optimizations:**

**2.3.1 Cache PhotoImage when base minimap unchanged**

**Current:**

```python
# Display the minimap in the Canvas
img = ImageTk.PhotoImage(Image.fromarray(img))  # Created every frame
if self.container is None:
    self.container = self.canvas.create_image(...)
else:
    self.canvas.itemconfig(self.container, image=img)
```

**Optimization:**

```python
# Cache PhotoImage if base minimap + path/rune/player_pos unchanged
path_hash = hash(str(path)) if path else None
rune_hash = hash((rune_active, rune_pos)) if rune_pos else None
player_hash = hash(player_pos) if player_pos else None
combined_hash = (minimap_hash, path_hash, rune_hash, player_hash)

if combined_hash != self.cached_photo_hash:
    img_photo = ImageTk.PhotoImage(Image.fromarray(img))
    self.cached_photo_hash = combined_hash
else:
    img_photo = self.cached_photo_image  # Reuse cached PhotoImage
```

**Expected Impact:**

-   Giảm CPU ~3-5% trong GUI (PhotoImage creation)
-   Risk: LOW - Cache-based optimization

**2.3.2 Optimize Drawing Operations**

**Current:**

-   Vẽ path/rune/player_pos mỗi frame (ngay cả khi không đổi)
-   Vẽ routine points mỗi frame (ngay cả khi routine không đổi)

**Optimization:**

-   Cache base image với path/rune/player_pos đã vẽ
-   Chỉ redraw khi path/rune/player_pos/routine thay đổi
-   Separate base minimap layer và overlay layer

**Expected Impact:**

-   Giảm CPU ~2-5% trong GUI (drawing operations)
-   Risk: MEDIUM - Cần test carefully để đảm bảo updates đúng

**Note:** Optimization này phức tạp hơn và có thể không cần thiết vì drawing operations không quá expensive.

---

## 📊 Implementation Priority

### **Priority 1: Template Matching Optimization** ⭐⭐⭐

-   **Impact:** High (~5-10% CPU)
-   **Risk:** Low (backward compatible)
-   **Complexity:** Medium
-   **Recommendation:** ✅ Implement

### **Priority 2: PhotoImage Caching** ⭐⭐

-   **Impact:** Medium (~3-5% CPU)
-   **Risk:** Low (cache-based)
-   **Complexity:** Low
-   **Recommendation:** ✅ Implement

### **Priority 3: Notifier Gray Cache** ⭐

-   **Impact:** Low (~2-5% CPU)
-   **Risk:** Low (cache-based)
-   **Complexity:** Low
-   **Recommendation:** ⚠️ Optional (test first)

### **Priority 4: Drawing Operations Optimization** ⭐

-   **Impact:** Low (~2-5% CPU)
-   **Risk:** Medium (có thể miss updates)
-   **Complexity:** High
-   **Recommendation:** ❌ Skip (not worth complexity)

---

## 📋 Implementation Checklist

### **Step 1: Template Matching Optimization** (1-2 hours)

-   [ ] Add `is_gray` parameter to `multi_match()` in `utils.py`
-   [ ] Add `is_gray` parameter to `single_match()` in `utils.py` (if used)
-   [ ] Pre-convert gray trong `capture.py` cho player matching
-   [ ] Pre-convert gray trong `notifier.py` cho elite/others/rune matching
-   [ ] Test: Verify matching still works correctly
-   [ ] Test: Measure CPU reduction

### **Step 2: PhotoImage Caching** (30-60 minutes)

-   [ ] Add cache variables trong `minimap.py`
-   [ ] Implement hash-based caching cho PhotoImage
-   [ ] Test: Verify GUI updates correctly
-   [ ] Test: Measure CPU reduction

### **Step 3: Notifier Gray Cache** (Optional, 30 minutes)

-   [ ] Add cache variables trong `notifier.py`
-   [ ] Implement frame hash-based caching
-   [ ] Test: Verify black screen detection still works
-   [ ] Test: Measure CPU reduction (may be minimal)

---

## 🎯 Expected Results

**After Phase 2:**

-   **CPU Reduction:** ~15-25% additional (from Phase 2)
-   **Total CPU Reduction:** ~45-70% (Phase 1 + Phase 2)
-   **Risk:** LOW-MEDIUM (mostly LOW)

---

## ⚠️ Testing Requirements

**Before Implementation:**

-   [ ] Measure baseline CPU usage
-   [ ] Identify most expensive operations (profiling)

**After Implementation:**

-   [ ] Test template matching accuracy (không giảm accuracy)
-   [ ] Test GUI updates (không miss updates)
-   [ ] Test notifier alerts (không miss alerts)
-   [ ] Measure CPU reduction
-   [ ] Verify bot functionality (không break bot)

---

## 📝 Notes

1. **Template Matching Optimization** là highest priority - có impact lớn nhất
2. **PhotoImage Caching** là easy win - low risk, medium impact
3. **Notifier Gray Cache** có thể không cần thiết - test trước
4. **Drawing Optimization** quá phức tạp - skip

---

## ✅ Recommendation

**Implement:**

1. ✅ **Template Matching Optimization** - Priority 1
2. ✅ **PhotoImage Caching** - Priority 2
3. ⚠️ **Notifier Gray Cache** - Optional (test first)

**Skip:**

-   ❌ **Drawing Operations Optimization** - Too complex, low impact

---

**Ready to implement?** Bắt đầu với Step 1 (Template Matching Optimization) để có impact lớn nhất!
