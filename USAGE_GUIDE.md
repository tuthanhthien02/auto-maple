# Hướng dẫn sử dụng: Host → VMware → Arduino (TCP)

## 📋 Tổng quan

Hệ thống cho phép Host script gửi input qua TCP đến VMware, sau đó forward qua Serial đến Arduino HID.

```
Host Script → TCP → VMware Script → Serial → Arduino → USB HID → Game
```

## 🔧 Components

1. **host_sender.py** - Chạy trên Host (máy thật)
2. **vmware_receiver.py** - Chạy trên VMware
3. **arduino_hid_keyboard_tcp.ino** - Upload lên Arduino

## 🚀 Bước 1: Cài đặt Arduino

### 1.1. Upload code lên Arduino

1. Mở Arduino IDE
2. Mở file: `arduino_hid_keyboard_tcp/arduino_hid_keyboard_tcp.ino`
3. Chọn board: **Tools → Board → Arduino Leonardo** (hoặc Pro Micro)
4. Chọn port: **Tools → Port → COMx**
5. Click **Upload**

### 1.2. Kiểm tra Arduino

1. Mở Serial Monitor: **Tools → Serial Monitor** (115200 baud)
2. Gửi test command: `down:a\n`
3. Key 'a' sẽ được press ✅

## 🔧 Bước 2: Cấu hình Host

### 2.1. Tìm IP của VMware

**Trên VMware:**

```bash
ipconfig
```

Tìm **IPv4 Address** (ví dụ: `192.168.1.100`)

### 2.2. Sửa `host_sender.config.json`

```json
{
    "vmware_ip": "192.168.1.100", // Thay bằng IP thật của VMware
    "vmware_port": 12345,
    "reconnect_interval": 1.0,
    "enable_logging": false
}
```

**Lưu ý:**

-   `vmware_ip`: IP của VMware (bắt buộc)
-   `vmware_port`: Port TCP (mặc định: 12345)
-   `enable_logging`: Set `true` để debug

## 🔧 Bước 3: Cấu hình VMware

### 3.1. Kết nối Arduino vào VMware

-   Kết nối Arduino qua USB vào VMware
-   VMware sẽ nhận Arduino như một COM port

### 3.2. Sửa `vmware_receiver.config.json` (nếu cần)

```json
{
    "com_port": null, // null = auto-detect Arduino
    "baudrate": 115200,
    "server_port": 12345,
    "block_local_input": false,
    "enable_logging": false
}
```

**Lưu ý:**

-   `com_port`: `null` = tự động tìm Arduino, hoặc chỉ định: `"COM13"`
-   `enable_logging`: Set `true` để debug

## 🚀 Bước 4: Chạy hệ thống

### 4.1. Chạy VMware Receiver (trước)

**Cách 1: Dùng .bat file (khuyến nghị)**

```bash
run_vmware_receiver.bat
```

-   Tự động request admin privileges
-   Tự động tìm Arduino
-   Start TCP server

**Cách 2: Chạy Python trực tiếp**

```bash
python vmware_receiver.py
```

**Hoặc chỉ định COM port:**

```bash
python vmware_receiver.py COM13 115200 12345 false
```

**Output mẫu:**

```
[CONFIG] COM Port: AUTO-DETECT
[CONFIG] Baudrate: 115200
[CONFIG] Server Port: 12345
[CONFIG] Logging: false

[ARDUINO] Connecting to Arduino...
[ARDUINO] Auto-detecting Arduino port...
[ARDUINO] ✓ Connected successfully to COM13 (baudrate: 115200)
[ARDUINO] Initialized - all keys released

[SERVER] Starting TCP server on port 12345...
[SERVER] ✓ TCP server started on port 12345
[SERVER] Listening for Host sender connection...
[STATUS] Arduino: CONNECTED
[STATUS] Client: Waiting...
[STATUS] Press Ctrl+C to exit
```

### 4.2. Chạy Host Sender (sau)

**Cách 1: Dùng .bat file**

```bash
run_host_sender.bat
```

**Cách 2: Chạy Python trực tiếp**

```bash
python host_sender.py
```

**Hoặc chỉ định IP:**

```bash
python host_sender.py 192.168.1.100 12345 false
```

**Output mẫu:**

```
[CONFIG] VMware IP: 192.168.1.100
[CONFIG] VMware Port: 12345
[CONFIG] Reconnect Interval: 1.0s
[CONFIG] Logging: false

[CONNECT] Attempting to connect to 192.168.1.100:12345...
[CONNECT] ✓ Connected successfully to 192.168.1.100:12345
[START] Host sender started with auto-reconnect
[STATUS] Connection: CONNECTED
[STATUS] Press Ctrl+C to exit
```

### 4.3. Sử dụng trong Python code

```python
from host_sender import HostSender
import time

# Create sender
sender = HostSender()
sender.start()

# Đợi kết nối (nếu cần)
time.sleep(1)

# Send keys
sender.send_key('a', 'down')
time.sleep(0.1)
sender.send_key('a', 'up')

sender.send_key('space', 'down')
sender.send_key('space', 'up')

# Release all keys
sender.send_all_up()

# Stop sender
sender.stop()
```

## 📊 Theo dõi trạng thái

### Host Sender Status

```
[STATUS] Connection: CONNECTED/DISCONNECTED
[RECONNECT] Attempting to reconnect... (nếu mất kết nối)
[RECONNECT] ✓ Reconnected successfully (total reconnects: X)
```

### VMware Receiver Status

```
[STATUS] Arduino: CONNECTED/DISCONNECTED
[STATUS] Client: CONNECTED (IP:PORT) / Waiting... / DISCONNECTED
[CLIENT] ✓ Connected from 192.168.1.50:12345
[FORWARD] down:a (8 bytes)
```

## 🐛 Troubleshooting

### Host không kết nối được VMware

**Kiểm tra:**

1. ✅ VMware receiver đã start chưa?
2. ✅ IP của VMware trong config đúng chưa?
3. ✅ Firewall có block port 12345 không?
4. ✅ Ping được VMware không? `ping 192.168.1.100`

**Giải pháp:**

-   Tắt Windows Firewall hoặc allow port 12345
-   Kiểm tra VMware network adapter (NAT/Bridged)
-   Set `enable_logging: true` để xem chi tiết

**Error mẫu:**

```
[ERROR] Connection timeout to 192.168.1.100:12345
[ERROR] Check if VMware receiver is running and firewall allows connection
```

### VMware không nhận được commands

**Kiểm tra:**

1. ✅ TCP server đã start chưa? (Xem `[SERVER] ✓ TCP server started`)
2. ✅ Client đã connect chưa? (Xem `[CLIENT] ✓ Connected`)
3. ✅ Set `enable_logging: true` để xem commands

**Giải pháp:**

-   Kiểm tra port 12345 có đang listen không:
    ```bash
    netstat -an | findstr 12345
    ```
-   Xem logs chi tiết với `enable_logging: true`

### Arduino không nhận được commands

**Kiểm tra:**

1. ✅ Arduino đã kết nối USB vào VMware chưa?
2. ✅ COM port trong config đúng chưa?
3. ✅ Serial Monitor trong Arduino IDE có nhận được commands không?

**Giải pháp:**

-   Kiểm tra Arduino trong Device Manager (VMware)
-   Thử chỉ định COM port cụ thể trong config: `"com_port": "COM13"`
-   Xem Serial Monitor trong Arduino IDE để debug

**Error mẫu:**

```
[ERROR] Arduino not found. Please specify COM port in config file.
[ERROR] Available ports:
[ERROR]   - COM1: Serial Port
[ERROR]   - COM13: Arduino Leonardo
```

### Latency cao

**Giải pháp:**

1. ✅ Kiểm tra network latency: `ping 192.168.1.100` (< 1ms là tốt)
2. ✅ Tắt `enable_logging` để giảm overhead
3. ✅ Kiểm tra baudrate: 115200 (đã tối ưu)

## 📈 Statistics

Khi dừng script (Ctrl+C), sẽ hiển thị statistics:

**Host Sender:**

```
==================================================
=== FINAL STATISTICS ===
==================================================
Connection: CONNECTED
Total sent: 1250
Total errors: 2
Total reconnects: 1
Error rate: 0.2%
==================================================
```

**VMware Receiver:**

```
==================================================
=== FINAL STATISTICS ===
==================================================
Total received: 1250
Total forwarded: 1248
Total errors: 2
Total clients: 1
Success rate: 99.8%
==================================================
```

## 🔑 Hotkeys & Commands

### Host Sender

-   **Ctrl+C**: Exit và hiển thị statistics

### VMware Receiver

-   **Ctrl+C**: Exit và hiển thị statistics

### Arduino Commands

-   `down:a\n` - Press key 'a'
-   `up:a\n` - Release key 'a'
-   `all_up\n` - Release all keys

## 📝 Config Files

### host_sender.config.json

```json
{
    "vmware_ip": "192.168.1.100",
    "vmware_port": 12345,
    "reconnect_interval": 1.0,
    "enable_logging": false
}
```

### vmware_receiver.config.json

```json
{
    "com_port": null,
    "baudrate": 115200,
    "server_port": 12345,
    "block_local_input": false,
    "enable_logging": false
}
```

## ✅ Quick Start Checklist

-   [ ] Upload Arduino code (`arduino_hid_keyboard_tcp.ino`)
-   [ ] Kết nối Arduino vào VMware
-   [ ] Tìm IP của VMware (`ipconfig` trên VMware)
-   [ ] Sửa `host_sender.config.json` với IP VMware
-   [ ] Chạy `run_vmware_receiver.bat` trên VMware
-   [ ] Chạy `run_host_sender.bat` trên Host
-   [ ] Test gửi keys: `sender.send_key('a', 'down')`

## 🎯 Example: Complete Setup

### 1. Setup Arduino

```
Arduino IDE → Upload arduino_hid_keyboard_tcp.ino
COM Port: COM13
```

### 2. Setup VMware Receiver

```
Config: vmware_receiver.config.json
{
    "com_port": null,  // auto-detect
    "baudrate": 115200,
    "server_port": 12345,
    "enable_logging": false
}

Run: run_vmware_receiver.bat
```

### 3. Setup Host Sender

```
Config: host_sender.config.json
{
    "vmware_ip": "192.168.1.100",  // IP của VMware
    "vmware_port": 12345,
    "enable_logging": false
}

Run: run_host_sender.bat
```

### 4. Test

```python
from host_sender import HostSender
import time

sender = HostSender()
sender.start()
time.sleep(1)  # Wait for connection

# Test keys
sender.send_key('a', 'down')
time.sleep(0.1)
sender.send_key('a', 'up')

sender.stop()
```

## 📚 Files Structure

```
auto-maple/
├── host_sender.py                    # Host sender script
├── host_sender.config.json           # Host sender config
├── run_host_sender.bat              # Host sender launcher
├── vmware_receiver.py                # VMware receiver script
├── vmware_receiver.config.json       # VMware receiver config
├── run_vmware_receiver.bat          # VMware receiver launcher
├── arduino_hid_keyboard_tcp/
│   ├── arduino_hid_keyboard_tcp.ino # Arduino code
│   └── README.md                    # Arduino docs
└── USAGE_GUIDE.md                   # This file
```

## 💡 Tips

1. **Debug mode**: Set `enable_logging: true` trong config để xem logs chi tiết
2. **Auto-reconnect**: Host sender tự động reconnect mỗi 1s nếu mất kết nối
3. **Statistics**: Nhấn Ctrl+C để xem statistics trước khi exit
4. **Multiple clients**: Hiện tại chỉ support 1 client tại một thời điểm
5. **Network latency**: Ping VMware để kiểm tra latency (< 1ms là tốt)

---

**Questions?** Check logs với `enable_logging: true` hoặc xem error messages! 🐛
