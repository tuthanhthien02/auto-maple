# Build Instructions for vmware_receiver.py

Hướng dẫn compile `vmware_receiver.py` thành standalone executable để giảm khả năng bị detect.

## Yêu cầu

- Python 3.7+
- PyInstaller (sẽ tự động cài đặt nếu chưa có)
- pyserial (sẽ tự động cài đặt nếu chưa có)

## Cách build

### Cách 1: Sử dụng Python script (Khuyến nghị)

```bash
python build_vmware_receiver.py
```

Script sẽ:
- Tự động kiểm tra và cài đặt PyInstaller nếu cần
- Tự động kiểm tra và cài đặt dependencies
- Clean previous builds
- Build executable với tên `system_service.exe` (generic name)

### Cách 2: Sử dụng Windows Batch script

```bash
build_vmware_receiver.bat
```

Double-click file `.bat` hoặc chạy từ command prompt.

### Cách 3: Sử dụng PyInstaller trực tiếp với spec file

```bash
pyinstaller vmware_receiver.spec
```

### Cách 4: Sử dụng PyInstaller với command line

```bash
pyinstaller --onefile --noconsole --name=system_service --add-data="src;src" vmware_receiver.py
```

## Kết quả

Sau khi build thành công, bạn sẽ tìm thấy:
- **Executable**: `dist/system_service.exe`
- **Size**: Khoảng 10-20 MB (tùy thuộc vào dependencies)

## Tính năng build

- ✅ **One-file executable**: Tất cả dependencies được bundle vào 1 file
- ✅ **No console window**: Chạy ẩn (không hiện console)
- ✅ **Generic name**: Tên `system_service.exe` thay vì `vmware_receiver.exe` để giảm detect
- ✅ **Includes src directory**: Tự động include thư mục `src/` với modules
- ✅ **Hidden imports**: Tự động include các hidden imports cần thiết

## Sử dụng executable

Sau khi build, copy `dist/system_service.exe` vào VMware machine và chạy:

```bash
# Chạy với auto-detect COM port
system_service.exe

# Chỉ định COM port
system_service.exe COM3

# Chỉ định COM port và baudrate
system_service.exe COM3 115200

# Chỉ định đầy đủ tham số
system_service.exe COM3 115200 12345 false
```

**Tham số:**
1. `COM_PORT` (optional): COM port của Arduino (ví dụ: COM3)
2. `BAUDRATE` (optional): Baudrate, mặc định 115200
3. `SERVER_PORT` (optional): TCP server port, mặc định 12345
4. `ENABLE_LOGGING` (optional): true/false, mặc định false

## Tùy chỉnh

### Đổi tên executable

Sửa trong `build_vmware_receiver.py` hoặc `vmware_receiver.spec`:
```python
EXE_NAME = "your_custom_name"  # Thay đổi ở đây
```

### Thêm icon

1. Tạo file `.ico` (ví dụ: `icon.ico`)
2. Sửa trong `build_vmware_receiver.py`:
```python
ICON_FILE = "icon.ico"
```

Hoặc trong `vmware_receiver.spec`:
```python
icon='icon.ico',  # Thêm vào EXE() section
```

### Thêm console window (để debug)

Sửa trong `build_vmware_receiver.py`:
```python
# Xóa dòng này:
"--noconsole",
```

Hoặc trong `vmware_receiver.spec`:
```python
console=True,  # Thay đổi từ False thành True
```

## Troubleshooting

### Lỗi: "PyInstaller not found"
```bash
pip install pyinstaller
```

### Lỗi: "Module not found"
Thêm vào `hiddenimports` trong spec file hoặc build script:
```python
"--hidden-import=module_name",
```

### Lỗi: "File not found" khi chạy exe
Đảm bảo `src/` directory được include. Kiểm tra trong spec file:
```python
datas=[('src', 'src')],
```

### Exe quá lớn
- Sử dụng `--exclude-module` để loại bỏ modules không cần thiết
- Hoặc dùng `--onedir` thay vì `--onefile` (sẽ tạo thư mục với nhiều files)

## Lưu ý bảo mật

- ✅ Executable được build với tên generic (`system_service.exe`)
- ✅ Không có console window (chạy ẩn)
- ✅ Tất cả dependencies được bundle (không cần cài đặt thêm)
- ⚠️ Vẫn có thể detect qua:
  - Process name trong Task Manager
  - Network port listening
  - Config file (`vmware_receiver.config.json`)
  - Serial communication patterns

## Clean build

Để xóa tất cả build artifacts:
```bash
# Xóa build và dist directories
rmdir /s /q build dist

# Hoặc trên Linux/Mac
rm -rf build dist
```

