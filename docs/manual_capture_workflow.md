# Manual Capture Workflow

This workflow lets bạn chạy Auto Maple trên host/VMware bằng cách chọn vùng MapleStory thủ công rồi mới bật bot.

## Các bước

1. **Chạy `main.py`**
   - Lần khởi động này sẽ bỏ qua bước auto-capture.
   - GUI xuất hiện ngay lập tức với các nút mới trong tab **View → Status**.

2. **Chọn vùng MapleStory**
   - Nhấn nút `📐 Chọn vùng màn hình`.
   - Một overlay toàn màn hình xuất hiện (nằm trên cả VMware). Giữ chuột trái và kéo bao quanh cửa sổ MapleStory → thả chuột để xác nhận.
   - Vùng đã chọn sẽ được lưu vào `configs/manual_capture_region.json` và hiện trong GUI.

3. **Start Capture**
   - Khi đã có toạ độ, nút `🖥️ Start Capture` sẽ sáng. Nhấn để khởi động module capture.
   - GUI sẽ báo `⏳ Đang khởi động capture...` và chuyển sang `✅ Capture đang chạy` khi hoàn tất.
   - Nút `▶ Toggle Bot` và các thao tác routine/command book chỉ khả dụng sau khi capture chạy thành công.

4. **Load command book, routine, start bot**
   - Sau khi capture chạy ổn định, bạn có thể load command book/routine và bật bot như trước đây.
   - Nếu Maplestory chạy trong VMware, chỉ cần đảm bảo vùng chọn chính xác phần hiển thị game.

## Lưu ý

- Để chọn lại vùng khác, bấm `📐 Chọn vùng màn hình` và lặp lại bước 2 → sau đó Start Capture lại để áp dụng.
- Nếu muốn quay về chế độ auto-detect cũ, xoá file `configs/manual_capture_region.json` hoặc dùng nút reset (sẽ bổ sung sau).
- Workflow này giúp chạy Auto Maple từ host trong khi game nằm trong VM (capture thông qua cửa sổ VMware).

