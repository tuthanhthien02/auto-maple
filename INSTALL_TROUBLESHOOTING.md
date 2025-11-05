# Hướng dẫn khắc phục lỗi khi cài đặt requirements

## Lỗi phổ biến

### 1. FileNotFoundError khi build wheel

**Nguyên nhân:** Thiếu Visual Studio Build Tools hoặc compiler C++

**Giải pháp:**

1. Tải và cài đặt Visual Studio Build Tools:

    - Truy cập: https://visualstudio.microsoft.com/downloads/
    - Tải "Build Tools for Visual Studio"
    - Trong quá trình cài đặt, chọn "Desktop development with C++" workload
    - Khởi động lại máy tính sau khi cài đặt

2. Hoặc cài đặt Visual Studio Community (nếu chưa có):
    - Tải từ: https://visualstudio.microsoft.com/downloads/
    - Chọn "Desktop development with C++" workload

### 2. Lỗi khi cài đặt TensorFlow

**Giải pháp:**

```bash
# Cài đặt TensorFlow riêng biệt
python -m pip install tensorflow

# Hoặc nếu gặp lỗi với Python 3.13, thử:
python -m pip install tensorflow --pre
```

### 3. Lỗi khi cài đặt numpy/pygame

**Giải pháp:**

```bash
# Nâng cấp pip, setuptools, wheel trước
python -m pip install --upgrade pip setuptools wheel

# Sau đó cài đặt lại
python -m pip install numpy pygame --upgrade
```

### 4. Lỗi với pywin32

**Giải pháp:**

```bash
# Cài đặt pywin32 riêng biệt
python -m pip install pywin32

# Sau khi cài đặt, chạy post-install script
python -m pywin32_postinstall -install
```

## Cách sử dụng script install_requirements.bat

1. **Double-click** vào file `install_requirements.bat`
2. Script sẽ tự động:
    - Kiểm tra Python
    - Nâng cấp pip, setuptools, wheel
    - Cài đặt tất cả packages
    - Nếu có lỗi, sẽ cài đặt từng package một để xác định package nào gây lỗi
    - Kiểm tra và hiển thị kết quả cài đặt

## Cài đặt thủ công từng package

Nếu script không hoạt động, bạn có thể cài đặt từng package một:

```bash
python -m pip install --upgrade pip setuptools wheel
python -m pip install GitPython
python -m pip install keyboard
python -m pip install mss
python -m pip install numpy
python -m pip install opencv-python-headless
python -m pip install Pillow
python -m pip install pygame
python -m pip install pywin32
python -m pip install pyserial
python -m pip install psutil
python -m pip install tensorflow
```

## Kiểm tra cài đặt

Sau khi cài đặt, kiểm tra các package:

```bash
python -c "import cv2; print('OpenCV:', cv2.__version__)"
python -c "import numpy; print('NumPy:', numpy.__version__)"
python -c "import tensorflow; print('TensorFlow:', tensorflow.__version__)"
python -c "import keyboard; print('Keyboard: OK')"
python -c "import mss; print('MSS: OK')"
python -c "import pygame; print('Pygame:', pygame.version.ver)"
python -c "import psutil; print('PSUtil:', psutil.__version__)"
python -c "import serial; print('PySerial: OK')"
python -c "import git; print('GitPython: OK')"
```

## Lưu ý

-   Python 3.8-3.12 được khuyến nghị. Python 3.13 có thể gặp vấn đề với một số package.
-   Đảm bảo bạn đã cài đặt Python với quyền Administrator nếu cần.
-   Nếu sử dụng virtual environment, kích hoạt nó trước khi chạy script.
