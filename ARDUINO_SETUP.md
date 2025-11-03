# Hướng dẫn sử dụng Arduino Pro Micro với Multiplicity

## Mục đích

Nhận input từ Multiplicity 4 (mirror input từ máy khác) và forward qua Arduino Pro Micro như USB HID keyboard.

## Yêu cầu

### Phần cứng:

-   Arduino Pro Micro (hoặc Leonardo)
-   Cáp USB để kết nối Arduino với máy tính

### Phần mềm:

-   Arduino IDE (để upload code lên Arduino)
-   Python 3.x
-   Thư viện Python: `pyserial`

## Cài đặt

### 1. Cài đặt thư viện Python

```bash
pip install pyserial
```

### 2. Upload code lên Arduino

1. Mở Arduino IDE
2. Mở file `arduino_hid_keyboard.ino`
3. Chọn board: **Tools → Board → Arduino Leonardo** (hoặc Pro Micro nếu có)
4. Chọn port COM: **Tools → Port → COMx** (x là số port của Arduino)
5. Click **Upload** để upload code lên Arduino

### 3. Tìm COM port của Arduino

Sau khi upload, Arduino sẽ xuất hiện như một COM port:

-   Windows: Device Manager → Ports (COM & LPT) → Arduino Leonardo
-   Hoặc chạy script Python, nó sẽ tự động list các ports

## Sử dụng

### Chạy script Python

```bash
# Tự động tìm Arduino
python keyboard_to_arduino.py

# Hoặc chỉ định COM port cụ thể
python keyboard_to_arduino.py COM3

# Chỉ định cả baudrate (mặc định 9600)
python keyboard_to_arduino.py COM3 9600
```

### Workflow

1. **Kết nối Arduino** vào máy tính
2. **Upload code** `arduino_hid_keyboard.ino` lên Arduino
3. **Bật Multiplicity 4** và thiết lập mirror input
4. **Chạy script** `keyboard_to_arduino.py`
5. **Sử dụng bàn phím** từ máy khác qua Multiplicity → Input sẽ được forward qua Arduino

### Dừng script

Nhấn `Ctrl+C` để dừng script. Script sẽ tự động:

-   Gỡ bỏ keyboard hook
-   Đóng kết nối Serial với Arduino

## Cách hoạt động

```
Multiplicity Input → Windows Keyboard Hook (BLOCK) → Python Script → Serial/USB → Arduino Pro Micro → USB HID Keyboard → Game
```

1. **Multiplicity 4** gửi input từ máy khác đến máy này
2. **Python keyboard hook** chặn (BLOCK) tất cả keyboard input từ Multiplicity
3. **Python script** forward command qua Serial đến Arduino
4. **Arduino** nhận command và gửi như USB HID keyboard
5. **Game chỉ nhận input từ Arduino** (không nhận trực tiếp từ Multiplicity)

### ⚠️ QUAN TRỌNG: Input Blocking

Script mặc định **BLOCK tất cả input gốc** để đảm bảo game chỉ nhận input từ Arduino. Điều này có nghĩa:

-   ✅ Input từ Multiplicity bị block → chỉ forward qua Arduino
-   ✅ Game chỉ nhận input từ Arduino (đúng pipeline)
-   ⚠️ Bàn phím thật của máy này cũng sẽ bị block khi script chạy

Nếu muốn không block input gốc (không khuyến khích), dùng:

```bash
python keyboard_to_arduino.py COM3 9600 false
```

## Troubleshooting

### Không tìm thấy Arduino

-   Kiểm tra Arduino đã được kết nối USB
-   Kiểm tra Device Manager xem COM port đã xuất hiện chưa
-   Thử chỉ định COM port thủ công: `python keyboard_to_arduino.py COM3`

### Script không nhận input

-   Kiểm tra Multiplicity đã bật mirror input chưa
-   Chạy script với quyền Administrator (cần cho keyboard hook)

### Arduino không gửi input

-   Kiểm tra Serial Monitor trong Arduino IDE xem có nhận được command không
-   Kiểm tra baudrate (mặc định 9600)
-   Thử upload lại code Arduino

### Lỗi permission

-   Chạy Python script với quyền Administrator
-   Keyboard hook cần quyền admin để hoạt động

## Lưu ý

-   **Quyền Administrator**: Script cần quyền admin để cài đặt keyboard hook
-   **Chỉ forward input từ Multiplicity**: Script hook tất cả keyboard input, bao gồm cả input từ bàn phím thật của máy này. Nếu muốn chỉ forward input từ Multiplicity, cần filter theo process hoặc window.
-   **Latency**: Có độ trễ nhỏ khi forward qua Serial (thường < 10ms)

## Tùy chỉnh

### Thêm key mapping

Sửa `VK_TO_KEY` trong `keyboard_to_arduino.py` để thêm key mới:

```python
VK_TO_KEY[0xXX] = 'keyname'
```

Sửa `keyMap[]` trong `arduino_hid_keyboard.ino` để thêm key code:

```cpp
{"keyname", KEY_CODE}
```

### Thay đổi baudrate

Mặc định 9600. Có thể tăng lên 115200 để giảm latency:

-   Python: `python keyboard_to_arduino.py COM3 115200`
-   Arduino: `Serial.begin(115200);` trong `setup()`
