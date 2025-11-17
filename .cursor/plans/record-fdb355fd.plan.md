<!-- fdb355fd-462c-464f-9c33-eabc5200bfcd 3969b515-6c40-4548-8ca8-6faf32c9a0bf -->
## Nâng cấp Host Sender đa VMware + GUI

### 1. Cập nhật cấu hình để hỗ trợ nhiều receiver

- Chỉnh `host_sender.config.json` sang dạng mảng các entry `{ "vmware_ip", "vmware_port", "reconnect_interval", ... }`, vẫn giữ các trường cũ cho từng entry; thêm nhãn `name` tùy chọn để hiển thị trong GUI.
- Đảm bảo tương thích ngược: nếu file chỉ có format cũ (trường đơn), tự bọc thành một entry và ghi lại ở format mới.
- Sửa `HostSender._load_config()` / `_save_config()` để đọc/ghi danh sách receivers, kèm trạng thái chung (logging, block input) và giá trị mặc định cho từng session.

### 2. Trừu tượng hóa lớp kết nối (receiver session)

- Tách logic hiện tại thành lớp mới, ví dụ `ReceiverSession`, quản lý socket, hook forwarding state, thống kê, luồng auto-reconnect cho từng VMware.
- `HostSender` giữ danh sách session và vòng đời hook chính thu thập input rồi phát tới các session đang bật mirror.
- Điều chỉnh send_key/send_all_up để phát tới các session được bật (hoặc cả danh sách tùy trạng thái).

### 3. Thêm GUI Tkinter quản lý receivers

- Tạo cửa sổ Tkinter trong `host_sender.py` sau khi load config.
- Hiển thị list (Frame/Treeview) mỗi receiver gồm nhãn + 3 nút nằm ngang:

1. `Toggle Bot` (gửi command text `toggle_bot\n` để yêu cầu receiver tự bật/tắt bot, thay thế hotkey thủ công).
2. `Enable/Disable Mirror` (bật/tắt forwarding cho session; đổi màu nút tùy trạng thái, ví dụ xanh = ON, cam = OFF).
3. `Connect/Disconnect` toggle (một nút duy nhất: nếu đang kết nối thì nhấn để ngắt và dừng auto-reconnect; nếu đang ngắt thì nhấn để kết nối lại). Nút đổi màu để phản ánh trạng thái (ví dụ đỏ = disconnected, xám = connecting, xanh = connected).

- Màu sắc: ví dụ Toggle Bot (blue), Mirror (green/orange), Connect toggle (xanh/đỏ). Trạng thái cập nhật theo session.

### 4. Tích hợp GUI với vòng đời hook + đa session

- Khi GUI chạy, keyboard hook vẫn hoạt động nền, nhưng forwarding chỉ gửi tới các session `forwarding_enabled=True`.
- Nút Toggle Bot gửi command `toggle_bot\n` tới riêng session (không ảnh hưởng hook).
- Nút Disconnect dừng auto-reconnect cho session và thay nút thành "Connect" nếu muốn tái kết nối.
- Bổ sung khả năng refresh/backoff nếu config thay đổi (đọc lại file khi nhấn nút reload hoặc khởi động lại script).

### 5. Kiểm thử thủ công

- Tạo config với ≥2 receiver (có thể mock IP cục bộ), khởi chạy host_sender, xác nhận GUI list hiển thị đúng.
- Kiểm tra: Toggle mirror cho từng receiver, gửi toggle_bot, ngắt kết nối, auto-reconnect hoạt động.
- Đảm bảo khi đóng ứng dụng, tất cả session đóng socket và lưu config cập nhật.

### To-dos

- [x] Confirm current record-position and capture update flow in listener, record UI, and capture modules.
- [x] Add a global config flag (and optional JSON/bot-config mapping) to control live position tracking for recording.
- [x] Add a Tkinter checkbox in the edit/record UI that toggles the live tracking config flag, defaulting to off.
- [x] Modify capture CPU-optimization logic to bypass skipping when live tracking is enabled so player_pos updates frequently.
- [x] Manually test both modes (checkbox on/off) to verify CPU behavior and that multiple positions record correctly.