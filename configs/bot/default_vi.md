# Giải thích `default.json`

Tệp `configs/bot/default.json` khai báo cấu hình mặc định cho bot, gồm hai phần chính:

1. `defaults`: bộ giá trị dùng chung cho mọi hồ sơ (profile).
2. `profiles`: các hồ sơ cấu hình khác nhau kế thừa từ `defaults` và có thể ghi đè một số tham số.

Dưới đây là mô tả chi tiết từng nhóm.

---

## 1. Khối `defaults`

### `routine_randomization`

Điều khiển mức độ “ngẫu nhiên hóa” hành vi của routine nhằm tạo cảm giác tự nhiên hơn.

-   `enabled`: bật/tắt toàn bộ ngẫu nhiên hóa.

#### a. `point_selection`

Quyết định có bỏ qua (skip) một số điểm (point) trong routine hay không.

| Khóa                       | Ý nghĩa                                                      |
| -------------------------- | ------------------------------------------------------------ |
| `enabled`                  | Cho phép bỏ qua điểm (skip) hay không.                       |
| `skip_probability`         | Xác suất bỏ qua một điểm (0.1 = 10%).                        |
| `max_skip_per_loop`        | Số lần bỏ qua tối đa trong một vòng lặp routine.             |
| `min_points_between_skips` | Số điểm tối thiểu phải đi qua trước khi được phép skip tiếp. |
| `never_skip_labels`        | Nếu true: không skip các point có gắn Label quan trọng.      |
| `never_skip_jumps`         | Không skip các Jump (điểm nhảy nhãn).                        |
| `never_skip_transitions`   | Không skip các điểm chuyển tầng/map.                         |

#### b. `routine_pattern`

Random hóa hướng đi, thứ tự mặt sàn.

| Khóa                         | Ý nghĩa                                          |
| ---------------------------- | ------------------------------------------------ |
| `enabled`                    | Bật/tắt biến đổi pattern.                        |
| `variant_switch_probability` | Xác suất đổi pattern sau mỗi loop.               |
| `min_loops_before_switch`    | Số loop tối thiểu trước khi được đổi pattern.    |
| `floor_variant_chance`       | Xác suất kích hoạt variant chỉ chạy một mặt sàn. |
| `variants`                   | Định nghĩa chi tiết từng pattern kèm trọng số.   |

Các variant mặc định:

-   `normal`: chạy bình thường (70%).
-   `reverse`: đảo thứ tự mặt sàn (15%).
-   `floor1_only`: chỉ chạy tầng 1 (10%).
-   `floor2_only`: chỉ chạy tầng 2 (5%).

#### c. `command_sequence`

Trộn/lược bỏ một số lệnh phụ để tránh lặp lại máy móc.

| Khóa                     | Ý nghĩa                                                                                           |
| ------------------------ | ------------------------------------------------------------------------------------------------- |
| `enabled`                | Bật/tắt random chuỗi lệnh _(có thể bật/tắt trực tiếp trên GUI Settings → Routine Randomization)_. |
| `shuffle_probability`    | Xác suất hoán đổi vị trí lệnh.                                                                    |
| `skip_probability`       | Xác suất bỏ qua lệnh nhỏ (không thuộc blacklist).                                                 |
| `extra_wait_probability` | Xác suất chèn thêm thời gian đợi.                                                                 |
| `extra_wait_range`       | Khoảng thời gian đợi thêm (giây).                                                                 |
| `skip_blacklist`         | Các lệnh không được bỏ qua.                                                                       |
| `shuffle_blacklist`      | Các lệnh không được hoán đổi vị trí.                                                              |

#### d. `movement`

Điều chỉnh chuyển động vi mô.

##### `position_offset`

-   `enabled`: có dịch chuyển vị trí ngẫu nhiên hay không _(có checkbox trong GUI)_.
-   `range`: biên độ dịch chuyển tối đa (đơn vị tọa độ chuẩn hóa 0–1).
-   `axes`: cho phép dịch chuyển theo trục `x`/`y`.

##### `micro_gesture`

-   `enabled`: có thêm cử chỉ nhỏ (micro-gesture) hay không _(có checkbox trong GUI)_.
-   `mirror_chance`: xác suất lặp lại động tác theo kiểu phản chiếu.
-   `duration_range`: thời lượng mỗi micro-gesture.

##### `observability`

-   `log_every_loops`: cứ bao nhiêu vòng lặp thì ghi log quan sát (0 = tắt).

#### e. `dynamic_paths`

Tự động tạo nhiều "đường đi" (paths) khác nhau từ cùng 1 routine, sau đó random chọn và switch giữa các paths.

| Khóa                     | Ý nghĩa                                                                  |
| ------------------------ | ------------------------------------------------------------------------ |
| `enabled`                | Bật/tắt tính năng Dynamic Paths _(có checkbox trong GUI)_.               |
| `path_count`             | Số lượng paths tự động generate (2-10, mặc định: 4).                     |
| `generation_strategy`    | Cách generate paths: `random_skip`, `partial`, `mixed`.                  |
| `skip_percentage_range`  | Khoảng skip points khi generate paths (ví dụ: [0.1, 0.3] = 10-30%).      |
| `selection_mode`         | Cách chọn path: `random`, `weighted`, `transition_matrix`, `sequential`. |
| `switch_interval`        | Khoảng loops để switch path (min/max).                                   |
| `transition_matrix.auto` | Tự động generate transition probabilities (40% stay, 60% switch).        |

**Cách hoạt động:**

1. Khi load routine, tự động generate N paths từ routine gốc
2. Path 1 luôn là full path (100% points)
3. Path 2-N được generate bằng cách skip random points (10-30%)
4. Bot chạy 1 path trong 2-5 loops, sau đó switch sang path khác
5. Transition matrix quyết định xác suất chuyển đổi giữa paths

**So sánh với các tính năng khác:**

-   **vs Point Selection**: Dynamic Paths = macro-variation (switch paths), Point Selection = micro-variation (skip points). Có thể dùng cả 2.
-   **vs Routine Pattern**: Cả 2 đều tạo macro-variation, nhưng Dynamic Paths tự động generate paths (flexible hơn). **Khuyến nghị: chỉ dùng Dynamic Paths, bỏ Routine Pattern**.
-   **vs Command Sequence**: Khác level (path level vs command level). Có thể dùng cả 2.

**Khuyến nghị setup:**

-   Maximum variation: `dynamic_paths` + `point_selection` + `command_sequence` (bỏ `routine_pattern`)
-   Balanced: `dynamic_paths` + `command_sequence` (bỏ `point_selection` và `routine_pattern`)

---

## 2. Khối `profiles`

Mỗi profile là một tập cấu hình kế thừa `defaults`. Nếu không ghi đè gì thì dùng nguyên bản.

-   `default`: trống nên dùng hoàn toàn `defaults`.
-   `safe`: điều chỉnh nhẹ để an toàn hơn.
    -   `routine_randomization.point_selection.skip_probability`: giảm còn 5%.
    -   `movement.position_offset.range`: giảm biên độ dịch chuyển.
    -   `movement.micro_gesture.mirror_chance`: giảm xác suất cử chỉ phản chiếu.
-   `aggressive`: hành vi ngẫu nhiên mạnh hơn.
    -   `point_selection`: bật skip với xác suất 18%.
    -   `movement.position_offset`: bật dịch chuyển, biên độ lớn hơn, cho phép trục Y.
    -   `micro_gesture`: bật hoàn toàn, tăng mirror chance.

---

### Cách sử dụng

1. `active_profile` quyết định profile nào đang áp dụng (`default`, `safe`, `aggressive`, hoặc tự thêm profile mới).
2. Khi chạy, hệ thống sẽ:
    - Nạp `defaults`.
    - Áp dụng giá trị ghi đè của profile tương ứng.
3. Có thể tạo profile mới bằng cách thêm mục mới dưới `profiles`.

Tệp `default.json` là điểm khởi đầu giúp cân bằng giữa tính “human-like” và rủi ro phát hiện, tùy nhu cầu mà bật/tắt các nhánh randomization tương ứng.
