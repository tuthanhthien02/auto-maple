<!-- c7c38b91-4669-4d93-b46d-9872002379e0 de9422dc-b328-49b3-94ed-2ee32f30f2b2 -->
# Khắc phục độ trễ khi chuyển tầng

## Phân tích vấn đề

Bot đổi tầng thành công nhưng thường đứng chờ khá lâu tại khu vực chuyển tầng. Ba nguyên nhân chính:

1. Thời gian chờ sau teleport trong `Move` chỉ 0.2s nên game chưa kịp cập nhật vị trí khi lên/xuống tầng
2. Hàm `step()` không đợi vị trí cập nhật sau khi teleport dọc nên bot nghĩ vẫn chưa qua tầng
3. Không có cơ chế xác nhận khi `player_pos` thay đổi đáng kể, bot tưởng mình vẫn ở tầng cũ
4. Watchdog trên Arduino auto-release phím sau ~3s khiến các thao tác giữ phím (giữ hướng/teleport) bị ngắt giữa chừng

## Giải pháp

### 1. Thêm thời gian chờ sau teleport dọc trong `step()`

**File**: `resources/command_books/luminous.py`

- Sau khi thả phím hướng (cuối hàm `step`), nếu di chuyển theo hướng `up/down` thì chờ ngẫu nhiên 0.15–0.25s để trò chơi xử lý đổi tầng

### 2. Tăng thời gian chờ trong `Move._teleport_to_target()` cho teleport dọc

**File**: `src/routine/components.py`

- Nhận biết teleport theo hướng `up/down`
- Với teleport dọc: chờ ngẫu nhiên 0.4–0.6s để camera/minimap cập nhật; teleport ngang giữ 0.2s

### 3. Poll vị trí sau teleport dọc

**File**: `src/routine/components.py`

- Sau khi chờ dài, lặp kiểm tra `config.player_pos` mỗi 0.1s (tối đa 1.0s)
- Thoát vòng lặp khi vị trí thay đổi >0.05 để chắc chắn bot đã sang tầng mới trước khi tiếp tục logic kế tiếp

### 4. Tăng timeout watchdog trên Arduino lên 10s

**File**: `arduino_hid_keyboard_tcp/arduino_hid_keyboard_tcp.ino`

- Sửa `WATCHDOG_TIMEOUT_MS` từ 3000 lên 10000 để phím có thể giữ tới ~10s
- Cập nhật ghi chú trong code để team hiểu rõ lý do

## Kiểm thử

- Test lên tầng (floor 1 → floor 2)
- Test xuống tầng (floor 2 → floor 1)
- Test giữ phím trên Arduino >5s để chắc chắn watchdog mới hoạt động đúng
- Quan sát log/hành vi đảm bảo teleport ngang không bị chậm

### To-dos

- [ ] Optimize capture frame rate: increase delays when bot idle, add adaptive frame rate based on player movement
- [ ] Optimize image processing in capture: cache HSV conversions, skip processing when position stable
- [ ] Reduce debug logging in bot main loop: remove or conditionally enable log.debug calls
- [ ] Optimize GUI updates in bot loop: only update when routine index changes
- [ ] Reduce minimap display FPS from 10 to 5-7 FPS
- [ ] Optimize GUI status refresh threads: increase intervals or combine threads
- [ ] Add position validation wait in step() function after vertical teleport (0.15-0.25s) to allow floor transition to complete
- [ ] Increase wait time in Move._teleport_to_target() for vertical teleports (0.4-0.6s) vs horizontal (0.2s)
- [ ] Add position polling logic after vertical teleport to wait for position update (max 1.0s)
- [ ] Test floor 1->2 and floor 2->1 transitions to verify delays are fixed