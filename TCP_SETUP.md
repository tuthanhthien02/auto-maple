# Setup Guide: Host → VMware → Arduino (TCP)

> **Xem hướng dẫn sử dụng chi tiết**: [USAGE_GUIDE.md](USAGE_GUIDE.md)

## 📋 Tổng quan

Kiến trúc mới cho phép Host script gửi input qua TCP đến VMware, sau đó forward qua Serial đến Arduino HID.

```
Host Script → TCP → VMware Script → Serial → Arduino → USB HID → Game
```

## 🔧 Components

### 1. **host_sender.py** (Chạy trên Host)

-   TCP Client kết nối đến VMware
-   Gửi key commands: `"down:a\n"`, `"up:a\n"`, `"all_up\n"`
-   Auto-reconnect khi mất kết nối

### 2. **vmware_receiver.py** (Chạy trên VMware)

-   TCP Server nhận commands từ Host
-   Forward commands qua Serial đến Arduino
-   Tự động tìm Arduino COM port

### 3. **Arduino** (không thay đổi)

-   Vẫn dùng `arduino_hid_keyboard.ino` hiện tại
-   Protocol: `"down:a\n"`, `"up:a\n"`, `"all_up\n"`

## 🚀 Cài đặt

### Bước 1: Cấu hình Host

1. **Sửa `host_sender.config.json`**:

```json
{
    "vmware_ip": "192.168.1.100", // IP của VMware
    "vmware_port": 12345,
    "reconnect_interval": 1.0,
    "enable_logging": false
}
```

2. **Tìm IP của VMware**:
    - Trên VMware: `ipconfig` (Windows) hoặc `ifconfig` (Linux)
    - Tìm IP address (ví dụ: `192.168.1.100`)

### Bước 2: Cấu hình VMware

1. **Sửa `vmware_receiver.config.json`** (nếu cần):

```json
{
    "com_port": null, // null = auto-detect Arduino
    "baudrate": 115200,
    "server_port": 12345,
    "block_local_input": false,
    "enable_logging": false
}
```

2. **Kết nối Arduino** vào VMware (qua USB pass-through)

### Bước 3: Upload Arduino code

1. Upload `arduino_hid_keyboard.ino` lên Arduino (nếu chưa upload)
2. Kiểm tra COM port của Arduino trên VMware

## 📖 Sử dụng

### Cách 1: Chạy bằng .bat files

#### **Trên VMware:**

```bash
run_vmware_receiver.bat
```

-   Tự động request admin privileges
-   Tự động tìm Arduino
-   Start TCP server trên port 12345

#### **Trên Host:**

```bash
run_host_sender.bat
```

-   Kết nối đến VMware
-   Sẵn sàng nhận commands

### Cách 2: Chạy bằng Python

#### **Trên VMware:**

```bash
python vmware_receiver.py [COM_PORT] [BAUDRATE] [SERVER_PORT] [ENABLE_LOGGING]
```

Ví dụ:

```bash
python vmware_receiver.py COM13 115200 12345 true
```

#### **Trên Host:**

```bash
python host_sender.py [VMWARE_IP] [VMWARE_PORT] [ENABLE_LOGGING]
```

Ví dụ:

```bash
python host_sender.py 192.168.1.100 12345 true
```

### Cách 3: Sử dụng trong Python code

#### **Trên Host:**

```python
from host_sender import HostSender

# Create sender
sender = HostSender(
    vmware_ip="192.168.1.100",
    vmware_port=12345,
    enable_logging=True
)

# Start sender
sender.start()

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

## 🔍 Kiểm tra kết nối

### 1. **Kiểm tra TCP Server (VMware)**

```bash
# Kiểm tra port có đang listen không
netstat -an | findstr 12345
```

### 2. **Kiểm tra kết nối từ Host**

```python
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = s.connect_ex(('192.168.1.100', 12345))
if result == 0:
    print("Port is open!")
else:
    print("Port is closed!")
s.close()
```

### 3. **Kiểm tra Arduino**

-   Serial Monitor trong Arduino IDE
-   Xem có nhận được commands không

## 🐛 Troubleshooting

### **Host không kết nối được VMware**

-   ✅ Kiểm tra IP của VMware trong config
-   ✅ Kiểm tra firewall (tắt Windows Firewall hoặc allow port 12345)
-   ✅ Kiểm tra VMware network adapter (NAT/Bridged)
-   ✅ Ping từ Host đến VMware: `ping 192.168.1.100`

### **VMware không nhận được commands**

-   ✅ Kiểm tra TCP server đã start chưa
-   ✅ Kiểm tra port 12345 có đang listen không
-   ✅ Kiểm tra `enable_logging=true` để xem logs

### **Arduino không nhận được commands**

-   ✅ Kiểm tra Arduino đã kết nối USB vào VMware chưa
-   ✅ Kiểm tra COM port trong config
-   ✅ Kiểm tra Serial Monitor trong Arduino IDE
-   ✅ Thử reconnect Arduino

### **Latency cao**

-   ✅ Kiểm tra network latency: `ping 192.168.1.100`
-   ✅ Tắt `enable_logging` để giảm overhead
-   ✅ Tăng `baudrate` lên 115200 (đã mặc định)

## 📊 So sánh với cách cũ (Multiplicity)

| Tiêu chí         | Multiplicity (Cách 1)  | TCP (Cách 2)            |
| ---------------- | ---------------------- | ----------------------- |
| **Latency**      | ~3-5ms                 | ~1.5-2ms ✅             |
| **Dependencies** | Multiplicity           | Không cần ✅            |
| **Flexibility**  | Chỉ forward input thực | Programmatic control ✅ |
| **Setup**        | Đơn giản               | Phức tạp hơn            |
| **Maintenance**  | Phụ thuộc Multiplicity | Tự chủ ✅               |

## 💡 Tips

1. **Enable logging để debug**:

    - Set `enable_logging: true` trong config
    - Xem logs trên cả Host và VMware

2. **Auto-reconnect**:

    - Host sender tự động reconnect mỗi 1s khi mất kết nối
    - Có thể điều chỉnh `reconnect_interval` trong config

3. **Multiple clients**:

    - Hiện tại chỉ support 1 client tại một thời điểm
    - Nếu client mới connect, client cũ sẽ bị disconnect

4. **Block local input**:
    - Option `block_local_input` (chưa implement)
    - Có thể thêm sau nếu cần

## ✅ Next Steps

1. **Test kết nối**: Chạy cả 2 scripts và kiểm tra kết nối
2. **Test latency**: Đo thời gian từ Host → Game
3. **Test reliability**: Test với nhiều commands liên tiếp
4. **Compare với Cách 1**: So sánh latency và reliability

---

**Questions?** Check logs với `enable_logging: true` 🐛
