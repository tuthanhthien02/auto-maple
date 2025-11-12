# VMware Receiver Integration - Hướng dẫn sử dụng

## Tổng quan

VMware Receiver đã được tích hợp vào GUI để dùng chung serial connection, tránh lỗi "Access is denied" khi chạy cùng lúc với bot.

## Kiến trúc

```
GUI Process
├── SharedArduinoConnection (Singleton)
│   └── Quản lý serial.Serial connection (chỉ một instance)
│
├── ArduinoSerialOutput
│   └── Bot commands → SharedArduinoConnection
│
└── VMwareReceiverIntegrated
    └── TCP server → SharedArduinoConnection
```

## Cách sử dụng

### 1. Enable VMware Receiver

Mở file `src/common/config.py` và set:

```python
# Enable/disable VMware Receiver TCP server
enable_vmware_receiver = True  # Set to True để enable

# VMware Receiver TCP server port
vmware_receiver_port = 12345

# Enable/disable keyboard hook for End key hotkey
vmware_receiver_hotkey_hook = False  # False = zero delay (recommended)
```

### 2. Chạy GUI

```bash
python main.py
```

VMware Receiver sẽ tự động start trong background thread nếu `enable_vmware_receiver = True`.

### 3. Kết nối từ Host

Từ Host machine, chạy `host_sender.py` để gửi commands:

```bash
python host_sender.py
```

## Config file

VMware Receiver vẫn sử dụng `vmware_receiver.config.json` để load:
- COM port (nếu không set trong code)
- Baudrate
- Key remapping
- Server port
- Hotkey hook setting

## Key Remapping

Key remapping được quản lý bởi `SharedArduinoConnection` và áp dụng cho cả:
- Bot commands (từ `ArduinoSerialOutput`)
- TCP commands (từ `VMwareReceiverIntegrated`)

### Cấu hình remapping

1. Trong `src/common/config.py`:
```python
arduino_key_mapping = {
    'a': 'rbracket',  # Press 'a' → outputs ']'
    'w': 'lbracket',  # Press 'w' → outputs '['
    'e': 'p'         # Press 'e' → outputs 'p'
}
arduino_remapping_enabled = True
```

2. Hoặc trong `vmware_receiver.config.json`:
```json
{
    "key_mapping": {
        "a": "rbracket",
        "w": "lbracket",
        "e": "p"
    }
}
```

### Toggle remapping

- Nếu `vmware_receiver_hotkey_hook = True`: Nhấn **End key** để toggle
- Hoặc trong code: `config.vmware_receiver.shared_connection.toggle_remapping()`

## Lợi ích

✅ **Tránh "Access is denied"**: Chỉ một serial connection duy nhất  
✅ **Thread-safe**: Lock đảm bảo không conflict  
✅ **Backward compatible**: `ArduinoSerialOutput` API không thay đổi  
✅ **Dễ quản lý**: Tất cả trong một process  
✅ **Zero delay**: Hotkey hook disabled by default  

## Troubleshooting

### Lỗi "Access is denied"

Nếu vẫn gặp lỗi này:
1. Đảm bảo không chạy `vmware_receiver.py` standalone cùng lúc
2. Kiểm tra xem có process nào khác đang dùng COM port không
3. Restart GUI

### TCP server không start

1. Kiểm tra `enable_vmware_receiver = True` trong `config.py`
2. Kiểm tra port 12345 có bị chiếm không
3. Xem logs để biết lỗi cụ thể

### Key remapping không hoạt động

1. Kiểm tra `arduino_remapping_enabled = True`
2. Kiểm tra key mapping trong config
3. Xem logs để debug

## Migration từ standalone

Nếu bạn đang dùng `vmware_receiver.py` standalone:

1. **Không cần chạy** `vmware_receiver.py` nữa
2. Set `enable_vmware_receiver = True` trong `config.py`
3. Chạy `main.py` như bình thường
4. TCP server sẽ tự động start

File `vmware_receiver.py` vẫn giữ nguyên để dùng standalone nếu cần.

## Testing

### Test 1: Bot commands
1. Enable bot trong GUI
2. Verify bot commands hoạt động qua Arduino

### Test 2: TCP commands
1. Enable VMware Receiver
2. Chạy `host_sender.py` từ Host
3. Verify TCP commands hoạt động

### Test 3: Cả hai cùng lúc
1. Enable cả bot và VMware Receiver
2. Chạy bot và gửi TCP commands cùng lúc
3. Verify không có conflict

## Logs

VMware Receiver sử dụng logger module:
- `log.info()`: Thông tin chung
- `log.debug()`: Debug messages (khi `enable_logging = True`)
- `log.warning()`: Warnings
- `log.error()`: Errors

Xem logs trong console hoặc log files.

