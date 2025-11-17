<!-- c7c38b91-4669-4d93-b46d-9872002379e0 a93c18da-766c-431d-b004-f85648eb5248 -->
# Human-Like Facing cho kỹ năng Luminous

## Mục tiêu

- Trước mỗi lần cast Reflection / Apocalypse / Death Scythe trong `Reflection_Mix_Random`, bot sẽ face trái/phải xen kẽ dựa trên hướng di chuyển hiện tại để giống người.
- Mỗi lần `press()` skill có `down_time`/`up_time` random trong khoảng hợp lý.
- Log chi tiết toàn bộ flow để dễ debug.

## Kế hoạch

### 1. Lấy hướng di chuyển hiện tại

- **File**: `resources/command_books/luminous.py`
- Đọc `config.routine.floor_direction` nếu có, ánh xạ thành "left"/"right".
- Nếu không có routine hoặc field bị thiếu, fallback về hướng đã face lần trước (mặc định right).
- Log nguồn gốc hướng baseline mỗi lần gọi.

### 2. Lưu trạng thái face

- Trong `Reflection_Mix_Random`, thêm biến instance `self._last_face_right`.
- Viết helper `face_direction(skill_name, direction)`:
- Tap `Key.left`/`Key.right` (dùng `press` với thời gian rất ngắn + random jitter).
- Cập nhật state và log: skill chuẩn bị cast, hướng mới, trạng thái toggle.

### 3. Chèn logic face xen kẽ trước từng skill

- Trước mỗi lần cast trong các vòng Reflection/Apocalypse/Death Scythe:

1. Tính hướng cần face (baseline cho lần đầu, sau đó đảo chiều liên tục).
2. Gọi helper face + log.
3. Cast skill theo logic cũ.

- Vẫn giữ nguyên xác suất skill và số lần cast.

### 4. Random hóa thời gian nhấn skill

- Thay các `press(..., down_time=0.1, up_time=0.1)` bằng `random.uniform` trong biên độ nhỏ:
- Ví dụ: Reflection down 0.08–0.12s, up 0.03–0.06s.
- Apocalypse/Death Scythe có thể dùng biên độ hơi lớn (0.1–0.15s, 0.04–0.07s).
- Log (hoặc comment) giải thích range.

### 5. Logging nâng cao

- Log đầu hàm: hướng baseline, tổng số cast, pattern face ban đầu.
- Log từng vòng: “Facing X trước skill Y (cast #n, down_time=X, up_time=Y)”.
- Nếu thiếu dữ liệu routine, log cảnh báo fallback.

## Kiểm thử

- Chạy `Reflection_Mix_Random` dưới routine thực tế hoặc mock để xem log:
- Hướng face thay đổi xen kẽ chính xác.
- Thời gian nhấn phím random nằm trong khoảng mong đợi.
- Đảm bảo không ảnh hưởng các phần khác của command book.

### To-dos

- [x] Lấy hướng baseline + log nguồn