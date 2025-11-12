# Plan: Tích hợp VMware Receiver vào GUI

## Vấn đề hiện tại

1. **"Access is denied"**: Khi chạy `vmware_receiver.py` và GUI cùng lúc, cả hai đều cố mở cùng một COM port → conflict
2. **Hai process riêng biệt**:
   - `vmware_receiver.py`: Standalone TCP server nhận commands từ Host và forward đến Arduino
   - `ArduinoSerialOutput` (trong GUI): Bot gửi commands trực tiếp đến Arduino
3. **Không thể dùng chung**: Serial port chỉ cho phép một process mở tại một thời điểm

## Giải pháp: Shared Serial Connection

### Kiến trúc mới

```
┌─────────────────────────────────────────────────┐
│                    GUI Process                   │
│                                                  │
│  ┌──────────────────────────────────────────┐   │
│  │   SharedArduinoConnection (Singleton)    │   │
│  │   - Quản lý serial.Serial connection    │   │
│  │   - Thread-safe send_command()          │   │
│  └──────────────────────────────────────────┘   │
│              ▲                    ▲             │
│              │                    │             │
│  ┌───────────┴──────┐  ┌─────────┴──────────┐  │
│  │ ArduinoSerial     │  │ VMwareReceiver     │  │
│  │ Output            │  │ (TCP Server)       │  │
│  │                   │  │                    │  │
│  │ - Bot commands    │  │ - TCP commands     │  │
│  │ - Direct send     │  │ - Forward to       │  │
│  │                   │  │   shared serial   │  │
│  └───────────────────┘  └────────────────────┘  │
└─────────────────────────────────────────────────┘
```

### Các bước thực hiện

## Phase 1: Tạo SharedArduinoConnection Class

**File mới**: `src/common/shared_arduino_connection.py`

### Chức năng:
- Singleton pattern để đảm bảo chỉ có một instance
- Quản lý serial.Serial connection
- Thread-safe `send_command()` method (dùng lock)
- Auto-reconnect khi mất kết nối
- Hỗ trợ key remapping (giống vmware_receiver)
- Load config từ `vmware_receiver.config.json`

### API:
```python
class SharedArduinoConnection:
    def __init__(self, com_port=None, baudrate=115200, key_mapping=None)
    def send_command(self, action: str, key: str = None) -> bool
    def send_all_up(self) -> bool
    def is_connected(self) -> bool
    def get_serial(self) -> Optional[serial.Serial]  # For backward compat
```

## Phase 2: Refactor ArduinoSerialOutput

**File**: `src/common/output_arduino.py`

### Thay đổi:
- Thay vì tạo `serial.Serial` riêng, sử dụng `SharedArduinoConnection`
- Giữ nguyên API hiện tại (backward compatible)
- Tất cả methods (`send_command`, `press`, `key_down`, etc.) vẫn hoạt động như cũ

### Implementation:
```python
from src.common.shared_arduino_connection import SharedArduinoConnection

class ArduinoSerialOutput:
    def __init__(self, ...):
        # Get shared connection instead of creating new
        self.shared_connection = SharedArduinoConnection.get_instance(
            com_port=com_port,
            baudrate=baudrate,
            key_mapping=key_mapping,
            remapping_enabled=remapping_enabled
        )
    
    def send_command(self, action, key=None):
        return self.shared_connection.send_command(action, key)
```

## Phase 3: Tích hợp VMwareReceiver vào GUI

**File mới**: `src/modules/vmware_receiver_integrated.py`

### Thay đổi từ `vmware_receiver.py`:
- **KHÔNG** tạo `serial.Serial` riêng
- Sử dụng `SharedArduinoConnection` để gửi commands
- Giữ nguyên TCP server logic
- Giữ nguyên keyboard hook (optional)
- Chạy TCP server trong daemon thread

### API:
```python
class VMwareReceiverIntegrated:
    def __init__(self, server_port=12345, enable_hotkey_hook=False, ...)
    def start_tcp_server(self)  # Start in background thread
    def stop_tcp_server(self)
    def is_running(self) -> bool
```

## Phase 4: Khởi tạo trong main.py

**File**: `main.py`

### Thay đổi:
- Khởi tạo `VMwareReceiverIntegrated` sau khi GUI ready
- Start TCP server trong background thread
- Cleanup khi exit

### Code:
```python
# After GUI initialization
if config.enable_vmware_receiver:  # New config flag
    from src.modules.vmware_receiver_integrated import VMwareReceiverIntegrated
    vmware_receiver = VMwareReceiverIntegrated(
        server_port=config.vmware_receiver_port,
        enable_hotkey_hook=config.vmware_receiver_hotkey_hook
    )
    vmware_receiver.start_tcp_server()
    config.vmware_receiver = vmware_receiver  # Store for cleanup
```

## Phase 5: Config Integration

**File**: `src/common/config.py`

### Thêm config flags:
```python
# VMware Receiver Integration
enable_vmware_receiver = False  # Enable/disable TCP server
vmware_receiver_port = 12345
vmware_receiver_hotkey_hook = False  # End key hotkey (disabled by default)
```

## Phase 6: Cleanup & Error Handling

### Cleanup:
- Khi GUI exit, stop TCP server và release serial connection
- Handle "Access is denied" gracefully (nếu vẫn xảy ra)
- Logging để debug

### Error Handling:
- Nếu serial connection fail, cả bot và TCP server đều không hoạt động
- Retry logic trong `SharedArduinoConnection`
- Status indicators trong GUI (optional)

## Lợi ích

1. ✅ **Tránh "Access is denied"**: Chỉ một serial connection duy nhất
2. ✅ **Dùng chung connection**: Bot và TCP server cùng dùng một serial port
3. ✅ **Thread-safe**: Lock đảm bảo không conflict khi gửi commands
4. ✅ **Backward compatible**: `ArduinoSerialOutput` API không thay đổi
5. ✅ **Tích hợp mượt**: VMware receiver chạy trong GUI process
6. ✅ **Dễ quản lý**: Tất cả trong một process, dễ debug và monitor

## Testing Plan

1. **Test 1**: Chạy GUI với bot → Verify bot commands hoạt động
2. **Test 2**: Chạy GUI với TCP server → Verify TCP commands hoạt động
3. **Test 3**: Chạy cả bot và TCP server cùng lúc → Verify không conflict
4. **Test 4**: Test key remapping từ cả bot và TCP
5. **Test 5**: Test reconnect khi mất kết nối
6. **Test 6**: Test cleanup khi exit

## Migration Notes

- `vmware_receiver.py` standalone vẫn có thể dùng (không bị xóa)
- Nếu muốn dùng integrated version, set `config.enable_vmware_receiver = True`
- Config file `vmware_receiver.config.json` vẫn được sử dụng

## Implementation Order

1. ✅ Phase 1: Tạo `SharedArduinoConnection`
2. ✅ Phase 2: Refactor `ArduinoSerialOutput`
3. ✅ Phase 3: Tạo `VMwareReceiverIntegrated`
4. ✅ Phase 4: Tích hợp vào `main.py`
5. ✅ Phase 5: Thêm config flags
6. ✅ Phase 6: Testing & cleanup

