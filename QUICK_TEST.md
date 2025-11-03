# Quick Test Guide - Host → VMware → Arduino

## ⚠️ QUAN TRỌNG

**`host_sender.py` KHÔNG nhận keyboard input thực!**

Nó chỉ là TCP client để gửi commands từ code. Bạn **PHẢI** gửi commands từ Python code, không thể chỉ ấn phím trên Host.

## 🧪 Cách test nhanh

### Bước 1: Enable logging

**VMware:**
Sửa `vmware_receiver.config.json`:

```json
{
    "enable_logging": true // ← Thay false thành true
}
```

**Host:**
Sửa `host_sender.config.json`:

```json
{
    "enable_logging": true // ← Thay false thành true (nếu có)
}
```

### Bước 2: Chạy VMware Receiver

```bash
run_vmware_receiver.bat
```

Kiểm tra output:

```
[ARDUINO] ✓ Connected successfully to COM13
[SERVER] ✓ TCP server started on port 12345
[STATUS] Client: Waiting...
```

### Bước 3: Chạy Host Sender

```bash
run_host_sender.bat
```

Kiểm tra output:

```
[CONNECT] ✓ Connected successfully to 192.168.1.100:12345
[STATUS] Connection: CONNECTED
```

### Bước 4: Test gửi commands

**Cách 1: Dùng test script (khuyến nghị)**

```bash
python test_host_sender.py
```

Script sẽ tự động:

1. Kết nối đến VMware
2. Gửi `down:a`
3. Đợi 0.5s
4. Gửi `up:a`
5. Test space key
6. Hiển thị stats

**Cách 2: Dùng Python interactive**

```python
python
>>> from host_sender import HostSender
>>> sender = HostSender()
>>> sender.start()
>>> sender.send_key('a', 'down')
>>> sender.send_key('a', 'up')
```

## 🔍 Debug nếu không hoạt động

### 1. Kiểm tra VMware Receiver logs

**Nếu thấy:**

```
[RECEIVED] Command: down:a
[PROCESS] Parsed: action='down', key='a'
[FORWARD] down:a (8 bytes) → Arduino
```

✅ **Tốt!** Command đã được nhận và forward.

**Nếu KHÔNG thấy:**

-   ❌ Host sender chưa gửi → Kiểm tra connection
-   ❌ Command không đến → Kiểm tra network

### 2. Kiểm tra Arduino

**Mở Serial Monitor** (Arduino IDE):

-   Baudrate: 115200
-   Xem có nhận được `down:a` không

**Nếu thấy:**

```
down:a
```

✅ **Tốt!** Arduino đã nhận command.

**Nếu KHÔNG thấy:**

-   ❌ VMware không forward → Kiểm tra Serial connection
-   ❌ Arduino không nhận → Kiểm tra baudrate

### 3. Test với logging enabled

**Trên VMware:**

```
[STATUS] enable_logging: true
[RECEIVED] Command: down:a
[PROCESS] Parsed: action='down', key='a'
[FORWARD] down:a (8 bytes) → Arduino
```

**Trên Host:**

```
[SEND] down:a (8 bytes)
```

## 🐛 Common Issues

### **Issue 1: Host sender không connect được**

```
[ERROR] Connection timeout
```

**Fix:**

-   Kiểm tra VMware receiver đã start chưa
-   Kiểm tra IP trong config đúng chưa
-   Ping VMware: `ping 192.168.1.100`

### **Issue 2: VMware nhận command nhưng không forward**

```
[RECEIVED] Command: down:a
[ERROR] Serial not connected
```

**Fix:**

-   Kiểm tra Arduino đã connect chưa
-   Kiểm tra COM port trong config
-   Thử chỉ định COM port: `"com_port": "COM13"`

### **Issue 3: Arduino không nhận được**

```
[FORWARD] down:a → Arduino
```

Nhưng Serial Monitor không thấy gì.
**Fix:**

-   Kiểm tra baudrate: 115200
-   Kiểm tra Serial Monitor đã mở chưa
-   Thử reconnect Arduino

## ✅ Success Checklist

-   [ ] VMware receiver: `[STATUS] Arduino: CONNECTED`
-   [ ] VMware receiver: `[STATUS] Client: CONNECTED`
-   [ ] Host sender: `[STATUS] Connection: CONNECTED`
-   [ ] VMware receiver: `[RECEIVED] Command: down:a`
-   [ ] VMware receiver: `[FORWARD] down:a → Arduino`
-   [ ] Arduino Serial Monitor: `down:a` ✅
-   [ ] Game nhận input ✅

## 🎯 Quick Test Command

```bash
# Test nhanh
python test_host_sender.py
```

Script sẽ tự động test toàn bộ pipeline!

---

**Lưu ý:** `host_sender.py` **KHÔNG** nhận keyboard input thực. Bạn phải gửi commands từ code! 🎹
