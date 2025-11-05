# Cải thiện Randomization trong Routine

## 📋 Tổng quan

Bot hiện tại đã có Arduino integration và một số randomization cơ bản. Tài liệu này liệt kê các cách cải thiện mức độ random trong routine execution để tránh detection tốt hơn.

---

## 🔍 Tình trạng hiện tại

### ✅ Đã có:

-   **Timing randomization**: `wait_random`, `get_human_delay` với Gaussian distribution
-   **Input pattern diversification**: Skip keys (5%), add random keys (2%)
-   **Timing variation**: 10-20% variation trong delays
-   **Micro pauses**: Random micro pauses giữa các key presses
-   **Position jitter**: ±1 pixel cho mouse clicks

### ❌ Chưa có:

-   Point selection randomization
-   Command sequence randomization
-   Position randomization (offset từ exact position)
-   Path randomization
-   Routine pattern variation
-   Command execution randomization

---

## 🎯 Các cách cải thiện Randomization

### 1. **Point Selection Randomization** ⭐⭐⭐⭐⭐

**Mức độ quan trọng:** Rất cao

**Mô tả:**

-   Đôi khi skip một số Points trong routine (không đi đến tất cả points)
-   Randomize thứ tự visit các Points (không phải lúc nào cũng tuần tự)
-   Tạo "shortcuts" - nhảy qua một số points đôi khi

**Ví dụ:**

```
Current: f1_pos_0 → f1_pos_1 → f1_pos_2 → f1_pos_3 → f1_pos_4
Randomized: f1_pos_0 → f1_pos_2 → f1_pos_4 (skip pos_1, pos_3)
```

**Implementation:**

-   Thêm probability để skip points (5-15%)
-   Randomize routine index selection (không phải lúc nào cũng `index + 1`)
-   Track visited points để tránh skip quá nhiều

**Ưu điểm:**

-   Giảm pattern detection rõ rệt
-   Tạo variation lớn trong routine execution
-   Rất khó detect vì không có pattern cố định

---

### 2. **Command Sequence Randomization** ⭐⭐⭐⭐⭐

**Mức độ quan trọng:** Rất cao

**Mô tả:**

-   Randomize thứ tự các commands trong mỗi Point
-   Đôi khi skip một số commands (không execute tất cả)
-   Đôi khi thêm commands không có trong routine (như wait_random ngẫu nhiên)

**Ví dụ:**

```
Current Point commands:
1. buff
2. buff_secondary
3. face_right
4. reflection_mix_random
5. wait_random,0.1,0.3
6. teleport,right,1

Randomized (50% chance):
- Execute commands theo thứ tự khác: 3, 1, 4, 6, 2, 5
- Skip command 2 đôi khi (10% chance)
- Thêm wait_random giữa commands (5% chance)
```

**Implementation:**

-   Randomize `self.commands` list trước khi execute
-   Thêm probability để skip từng command
-   Thêm random wait commands giữa các commands

**Ưu điểm:**

-   Phá vỡ pattern cố định trong command execution
-   Tạo variation ngay cả khi cùng một Point

---

### 3. **Position Randomization (Offset)** ⭐⭐⭐⭐

**Mức độ quan trọng:** Cao

**Mô tả:**

-   Thêm random offset nhỏ vào target position của mỗi Point
-   Không đi đến exact position (x, y) mà đi đến (x ± offset, y ± offset)
-   Tạo slight variation trong positioning

**Ví dụ:**

```
Current: move to (0.107, 0.090)
Randomized: move to (0.107 ± 0.005, 0.090 ± 0.003)
```

**Implementation:**

-   Thêm `position_offset_range` trong config (e.g., 0.003-0.008)
-   Modify `Point.main()` để apply offset trước khi move
-   Đảm bảo offset không làm bot đi sai đường

**Ưu điểm:**

-   Giảm exact positioning detection
-   Tạo natural variation trong movement
-   Không ảnh hưởng gameplay quá nhiều

---

### 4. **Path Randomization** ⭐⭐⭐⭐

**Mức độ quan trọng:** Cao

**Mô tả:**

-   Thay vì luôn dùng shortest path, đôi khi dùng path khác
-   Thêm slight detours trong movement
-   Vary số steps trong path (không phải lúc nào cũng optimal)

**Ví dụ:**

```
Current: shortest_path(A → B)
Randomized:
- 70% shortest_path
- 20% path với 1-2 extra steps
- 10% path với slight detour
```

**Implementation:**

-   Modify `Move.main()` để có multiple path options
-   Randomize path selection với weights
-   Add slight detours trong path calculation

**Ưu điểm:**

-   Giảm pattern trong movement paths
-   Tạo variation trong cách đi giữa các points

---

### 5. **Routine Pattern Randomization** ⭐⭐⭐⭐⭐

**Mức độ quan trọng:** Rất cao

**Mô tả:**

-   Đôi khi chạy routine theo thứ tự ngược lại (reverse)
-   Đôi khi skip một floor hoàn toàn và chỉ train ở một floor
-   Tạo multiple "variants" của routine và switch giữa chúng

**Ví dụ:**

```
Current: Floor 1 → Floor 2 → Floor 1 (loop)
Variants:
- Variant 1: Floor 1 → Floor 2 → Floor 1 (normal)
- Variant 2: Floor 2 → Floor 1 → Floor 2 (reverse)
- Variant 3: Floor 1 only (5 loops)
- Variant 4: Floor 2 only (5 loops)
```

**Implementation:**

-   Tạo multiple routine "variants" hoặc "modes"
-   Switch giữa variants sau mỗi N loops (random)
-   Track current variant và adjust routine execution

**Ưu điểm:**

-   Variation lớn nhất trong routine execution
-   Rất khó detect vì pattern thay đổi đáng kể
-   Có thể implement như "different training styles"

---

### 6. **Command Execution Randomization** ⭐⭐⭐⭐

**Mức độ quan trọng:** Cao

**Mô tả:**

-   Randomize parameters của commands (không phải lúc nào cũng exact values)
-   Đôi khi skip commands hoàn toàn
-   Đôi khi execute commands nhiều lần hơn bình thường

**Ví dụ:**

```
Current: teleport,right,1
Randomized:
- teleport,right,1 (70%)
- teleport,right,1 + wait_random,0.1,0.2 (20%)
- teleport,right,1 + teleport,right,1 (double, 10%)

Current: wait_random,0.1,0.3
Randomized:
- wait_random,0.1,0.3 (normal)
- wait_random,0.15,0.35 (slightly longer, 30%)
- Skip wait đôi khi (5%)
```

**Implementation:**

-   Modify command execution để có probability variations
-   Randomize command parameters trong valid range
-   Add conditional execution based on probability

**Ưu điểm:**

-   Tạo variation trong command execution
-   Không cần thay đổi routine file

---

### 7. **Loop Pattern Randomization** ⭐⭐⭐

**Mức độ quan trọng:** Trung bình

**Mô tả:**

-   Vary số lần loop qua routine trước khi restart
-   Đôi khi break loop sớm và restart
-   Đôi khi loop nhiều hơn bình thường

**Ví dụ:**

```
Current: Always loop back to start after complete routine
Randomized:
- 70%: Normal loop
- 20%: Loop 2-3 times before restart
- 10%: Break early và restart routine
```

**Implementation:**

-   Track loop count
-   Randomize loop break conditions
-   Add early restart logic

**Ưu điểm:**

-   Variation trong routine duration
-   Tạo natural breaks

---

### 8. **Route Variation (Alternate Paths)** ⭐⭐⭐⭐

**Mức độ quan trọng:** Cao

**Mô tả:**

-   Thay vì luôn đi theo cùng một route giữa hai points, đôi khi đi route khác
-   Tạo "alternative routes" và switch giữa chúng
-   Ví dụ: giữa pos_1 và pos_2, có thể đi thẳng hoặc đi vòng qua pos_3

**Ví dụ:**

```
Current: Always go f1_pos_0 → f1_pos_1 → f1_pos_2
Alternative: Sometimes go f1_pos_0 → f1_pos_2 (skip pos_1)
Or: f1_pos_0 → f1_pos_1 → f1_pos_0 → f1_pos_2 (backtrack)
```

**Implementation:**

-   Pre-define alternative routes trong routine
-   Randomize route selection với weights
-   Track route history để tránh lặp lại quá nhiều

**Ưu điểm:**

-   Variation lớn trong movement patterns
-   Khó detect vì không có fixed route

---

### 9. **Timing Variation Enhancement** ⭐⭐⭐

**Mức độ quan trọng:** Trung bình

**Mô tả:**

-   Tăng variance trong timing randomization
-   Thêm longer pauses đôi khi (simulate "thinking" hoặc "checking")
-   Vary timing dựa trên context (time of day, fatigue level)

**Ví dụ:**

```
Current: wait_random,0.1,0.3 (uniform)
Enhanced:
- 70%: Normal wait_random
- 20%: Longer wait (0.3-0.6) - "thinking"
- 10%: Very short wait (0.05-0.1) - "fast decision"
```

**Implementation:**

-   Enhance `wait_random` với weighted distribution
-   Add context-aware timing (time of day, session duration)
-   Implement fatigue simulation nếu chưa có

**Ưu điểm:**

-   More natural timing patterns
-   Context-aware behavior

---

### 10. **Command Frequency Randomization** ⭐⭐⭐

**Mức độ quan trọng:** Trung bình

**Mô tả:**

-   Vary frequency của các commands (không phải lúc nào cũng execute mỗi loop)
-   Ví dụ: buff không phải lúc nào cũng execute mỗi point, mà có probability

**Ví dụ:**

```
Current: buff executes every time at pos_0
Randomized:
- 80%: Execute buff
- 15%: Skip buff this loop
- 5%: Execute buff twice
```

**Implementation:**

-   Add probability-based execution cho commands
-   Track command execution history
-   Implement frequency-based randomization

**Ưu điểm:**

-   Natural variation trong command execution
-   Không execute commands quá predictably

---

## 📊 Priority Ranking

### High Priority (Implement First):

1. ⭐⭐⭐⭐⭐ **Point Selection Randomization** - Tác động lớn nhất
2. ⭐⭐⭐⭐⭐ **Routine Pattern Randomization** - Variation lớn nhất
3. ⭐⭐⭐⭐⭐ **Command Sequence Randomization** - Dễ implement, hiệu quả cao

### Medium Priority:

4. ⭐⭐⭐⭐ **Position Randomization** - Tốt nhưng cần careful
5. ⭐⭐⭐⭐ **Path Randomization** - Tốt nhưng có thể phức tạp
6. ⭐⭐⭐⭐ **Route Variation** - Tốt nhưng cần planning

### Lower Priority:

7. ⭐⭐⭐ **Command Execution Randomization** - Nice to have
8. ⭐⭐⭐ **Timing Variation Enhancement** - Đã có cơ bản
9. ⭐⭐⭐ **Loop Pattern Randomization** - Nice to have
10. ⭐⭐⭐ **Command Frequency Randomization** - Nice to have

---

## 🛠️ Implementation Strategy

### Phase 1: Core Randomization (High Impact)

1. Implement **Point Selection Randomization**
2. Implement **Command Sequence Randomization**
3. Implement **Routine Pattern Randomization**

### Phase 2: Movement Randomization

4. Implement **Position Randomization**
5. Implement **Path Randomization**
6. Implement **Route Variation**

### Phase 3: Enhancement

7. Enhance existing timing randomization
8. Add command frequency randomization
9. Add loop pattern randomization

---

## ⚙️ Configuration Options

Mỗi randomization feature nên có:

-   **Enable/Disable flag**
-   **Probability/Weight settings**
-   **Min/Max ranges**
-   **Safety checks** (không làm bot fail)

Ví dụ config:

```python
ROUTINE_RANDOMIZATION_CONFIG = {
    'point_selection': {
        'enabled': True,
        'skip_probability': 0.10,  # 10% chance to skip a point
        'randomize_order': True,
        'max_skip_per_loop': 2
    },
    'command_sequence': {
        'enabled': True,
        'randomize_order': True,
        'skip_command_probability': 0.05,  # 5% per command
        'add_random_wait_probability': 0.03  # 3% chance
    },
    'position_offset': {
        'enabled': True,
        'x_offset_range': (0.003, 0.008),
        'y_offset_range': (0.003, 0.008)
    },
    # ... etc
}
```

---

## 🎯 Expected Results

Sau khi implement:

-   **Pattern detection**: Giảm đáng kể do không có fixed patterns
-   **Variation**: Tăng rõ rệt trong routine execution
-   **Natural behavior**: Giống human behavior hơn
-   **Detection risk**: Giảm đáng kể

---

## 📝 Notes

-   **Safety first**: Đảm bảo randomization không làm bot fail hoặc đi sai đường
-   **Gradual implementation**: Implement từng feature một và test kỹ
-   **Configurable**: Mọi feature phải có config để enable/disable và adjust
-   **Backward compatible**: Không break existing routines

---

## 🔄 Next Steps

1. Review và approve plan
2. Implement Phase 1 features
3. Test với routine hiện tại
4. Adjust probabilities và ranges
5. Implement Phase 2 và 3
