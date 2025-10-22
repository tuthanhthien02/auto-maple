# 🚀 Quick Setup Guide

## ⚠️ Script bị tắt khi ấn phím?

Nếu `setup_conda.bat` bị tắt ngay sau khi ấn phím, hãy thử:

### ✅ Cách 1: Dùng version verbose (debug)

**Double-click file:**

```
setup_conda_verbose.bat
```

File này sẽ:

-   ✅ Hiển thị TẤT CẢ output (không bị ẩn)
-   ✅ Đợi 5 giây trước khi bắt đầu (xem được thông báo)
-   ✅ Pause ở cuối để xem kết quả

### ✅ Cách 2: Chạy qua Anaconda Prompt

1. Mở **Anaconda Prompt** (search trong Start Menu)
2. Di chuyển đến thư mục bot:
    ```bash
    cd "C:\Users\Thanh Thien\Desktop\New folder\auto-maple"
    ```
3. Chạy script:
    ```bash
    setup_conda.bat
    ```

### ✅ Cách 3: Chạy từng lệnh thủ công

Mở **Anaconda Prompt**, chạy từng lệnh:

```bash
# 1. Tạo environment
conda create -n automaple python=3.10 -y

# 2. Kích hoạt
conda activate automaple

# 3. Cài packages từ conda
conda install numpy opencv pillow -y

# 4. Cài packages từ pip
pip install keyboard pywin32 pygame GitPython mss

# 5. Kiểm tra
python -c "import cv2, numpy, mss, win32api; print('OK!')"
```

---

## 📋 Các scripts có sẵn

| File                      | Mô tả                     | Khi nào dùng          |
| ------------------------- | ------------------------- | --------------------- |
| `setup_conda.bat`         | Setup tự động (ít output) | Bình thường           |
| `setup_conda_verbose.bat` | Setup với debug mode      | Khi có lỗi/bị tắt sớm |
| `run_bot_conda.bat`       | Chạy bot                  | Sau khi setup xong    |
| `check_conda_env.bat`     | Kiểm tra environment      | Debug                 |

---

## 🔍 Debug: Tại sao script bị tắt?

### Nguyên nhân 1: Conda chưa được cài

**Kiểm tra:**

```bash
conda --version
```

**Nếu báo lỗi "conda is not recognized":**

-   Cài Miniconda: https://docs.conda.io/en/latest/miniconda.html
-   ✅ Nhớ tick "Add to PATH" khi cài!
-   Restart máy

### Nguyên nhân 2: Script chạy quá nhanh

**Giải pháp:**

-   Dùng `setup_conda_verbose.bat` để xem chi tiết
-   Hoặc chạy qua Anaconda Prompt

### Nguyên nhân 3: Lỗi khi tạo environment

**Kiểm tra:**

```bash
conda create -n test python=3.10 -y
```

**Nếu lỗi:**

-   Kiểm tra kết nối internet
-   Thử: `conda update conda`
-   Hoặc dùng cách thủ công (Cách 3 ở trên)

---

## ✅ Sau khi setup thành công

Nếu thấy output cuối cùng:

```
✓✓✓ TAT CA PACKAGES DA DUOC CAI DAT THANH CONG! ✓✓✓
```

→ Chạy bot bằng cách **double-click:**

```
run_bot_conda.bat
```

---

## 🆘 Vẫn không được?

Chạy các lệnh sau và gửi kết quả:

```bash
# Kiểm tra Python
python --version

# Kiểm tra Conda
conda --version

# Xem environments
conda env list

# Kiểm tra PATH
echo %PATH%
```
