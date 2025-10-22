# 🔧 Hướng dẫn FIX setup.py chi tiết

## ❌ Lỗi gặp phải:

```python
ModuleNotFoundError: No module named 'win32com'
```

---

## 📝 Giải thích vấn đề:

### **Tại sao lỗi?**

1. `setup.py` dùng `win32com.client` để tạo desktop shortcut
2. Module `win32com` thuộc package `pywin32`
3. Sau khi cài `pywin32`, cần **register COM DLLs** bằng post-install script
4. Script này cần **quyền Administrator** để register DLLs vào Windows Registry

### **File cần register:**

```
pythoncomXX.dll  (COM interface)
pywintypesXX.dll (Windows types)
```

---

## ✅ Giải pháp (Chọn 1 trong 3):

---

## 🚀 **Cách 1: Script tự động (Khuyến nghị nhất)**

### **Bước 1: Chạy script với quyền Admin**

**Double-click file này:**

```
fix_pywin32_admin.bat
```

Script sẽ:

-   ✅ Tự động xin quyền Administrator
-   ✅ Xóa và cài lại pywin32
-   ✅ Register COM DLLs
-   ✅ Test win32com

### **Bước 2: Chạy setup.py**

Sau khi script chạy xong và thấy "THANH CONG!", chạy:

```bash
conda activate automaple
python setup.py
```

Hoặc với option `--stay` (giữ cmd mở):

```bash
python setup.py --stay
```

---

## 🔧 **Cách 2: Fix thủ công**

### **Bước 1: Mở Anaconda Prompt AS ADMINISTRATOR**

1. **Search** "Anaconda Prompt" trong Start Menu
2. **Right-click** → **"Run as Administrator"**
3. Click **Yes** khi Windows hỏi

### **Bước 2: Kích hoạt environment**

```bash
conda activate automaple
```

### **Bước 3: Cài lại pywin32**

```bash
# Xóa version cũ
pip uninstall pywin32 -y

# Cài version mới
pip install --upgrade pywin32
```

### **Bước 4: Chạy post-install script**

```bash
# Cách 1: Từ Scripts folder
python "%CONDA_PREFIX%\Scripts\pywin32_postinstall.py" -install

# Nếu lỗi, thử Cách 2: Từ site-packages
python "%CONDA_PREFIX%\Lib\site-packages\pywin32_postinstall.py" -install
```

### **Bước 5: Kiểm tra**

```bash
python -c "import win32com.client; print('OK!')"
```

Nếu thấy `OK!` → Thành công!

### **Bước 6: Chạy setup.py**

```bash
python setup.py
```

---

## 💻 **Cách 3: Dùng PowerShell (Alternative)**

### **Mở PowerShell AS ADMINISTRATOR**

```powershell
# Kích hoạt conda
conda activate automaple

# Reinstall pywin32
pip install --upgrade --force-reinstall pywin32

# Register COM
python $env:CONDA_PREFIX\Scripts\pywin32_postinstall.py -install

# Test
python -c "import win32com.client; print('OK!')"

# Chạy setup
python setup.py
```

---

## 🎯 **Sau khi fix thành công:**

### **Chạy setup.py:**

```bash
# Mặc định: Tắt cmd sau khi bot tắt
python setup.py

# Hoặc: Giữ cmd mở (để debug)
python setup.py --stay
```

### **Kết quả:**

Sẽ có file shortcut trên Desktop:

```
Auto Maple.lnk
```

**Tính năng shortcut:**

-   ✅ Double-click để chạy bot
-   ✅ Tự động chuyển đến thư mục bot
-   ✅ Chạy `python main.py`
-   ✅ Có icon Auto Maple
-   ✅ **Run as Administrator** đã được enable

---

## 🔍 **Debug: Kiểm tra chi tiết**

### **1. Kiểm tra pywin32 đã cài chưa:**

```bash
conda activate automaple
pip show pywin32
```

### **2. Kiểm tra các modules:**

```bash
python -c "import win32com.client; print('win32com.client: OK')"
python -c "import win32api; print('win32api: OK')"
python -c "import win32con; print('win32con: OK')"
python -c "import pywintypes; print('pywintypes: OK')"
```

### **3. Tìm file pywin32_postinstall.py:**

```bash
# Windows
dir /s /b "%CONDA_PREFIX%\*pywin32_postinstall.py"
```

### **4. Xem error chi tiết:**

```bash
python setup.py 2>&1 | more
```

---

## ⚠️ **Troubleshooting:**

### **Lỗi 1: "PermissionError: [WinError 5] Access is denied"**

**Nguyên nhân:** Thiếu quyền Administrator

**Fix:**

-   Chạy Anaconda Prompt **AS ADMINISTRATOR**
-   Hoặc dùng `fix_pywin32_admin.bat` (tự động xin quyền)

---

### **Lỗi 2: "FileNotFoundError: pywin32_postinstall.py"**

**Nguyên nhân:** File không tìm thấy ở đường dẫn mặc định

**Fix:**

```bash
# Tìm file
where /r "%CONDA_PREFIX%" pywin32_postinstall.py

# Chạy từ đường dẫn đầy đủ
python "<full_path_to_file>" -install
```

---

### **Lỗi 3: "ImportError: DLL load failed"**

**Nguyên nhân:** DLLs chưa được register hoặc bị conflict

**Fix:**

```bash
# Reinstall pywin32
pip uninstall pywin32 -y
pip cache purge
pip install pywin32 --no-cache-dir

# Register với Administrator
python "%CONDA_PREFIX%\Scripts\pywin32_postinstall.py" -install
```

---

### **Lỗi 4: "com_error: (-2147221005, 'Invalid class string')"**

**Nguyên nhân:** COM registration chưa đúng

**Fix:**

```bash
# Unregister old COM objects
python "%CONDA_PREFIX%\Scripts\pywin32_postinstall.py" -remove

# Re-register
python "%CONDA_PREFIX%\Scripts\pywin32_postinstall.py" -install
```

---

## 📋 **Scripts có sẵn:**

| File                    | Mô tả                | Khi nào dùng                         |
| ----------------------- | -------------------- | ------------------------------------ |
| `fix_pywin32.bat`       | Fix bình thường      | Thử đầu tiên                         |
| `fix_pywin32_admin.bat` | Tự động xin admin    | Nếu `fix_pywin32.bat` lỗi Permission |
| `setup.py`              | Tạo desktop shortcut | Sau khi fix xong                     |

---

## 🎊 **Checklist hoàn tất:**

-   [ ] Đã chạy `fix_pywin32_admin.bat` hoặc fix thủ công
-   [ ] Test `python -c "import win32com.client; print('OK!')"` thành công
-   [ ] Chạy `python setup.py` không lỗi
-   [ ] Có file `Auto Maple.lnk` trên Desktop
-   [ ] Double-click shortcut, bot chạy được

---

## 💡 **Tips:**

### **Tạo shortcut với custom icon:**

```bash
python setup.py
```

Shortcut sẽ dùng icon từ `assets/icon.ico`

### **Shortcut giữ cmd mở (để debug):**

```bash
python setup.py --stay
```

Useful khi muốn xem error messages.

### **Tạo lại shortcut:**

Nếu muốn tạo lại:

1. Xóa shortcut cũ trên Desktop
2. Chạy lại `python setup.py`

---

## 🆘 **Vẫn không được?**

### **Option: Tạo shortcut thủ công**

**Double-click:**

```
create_shortcut_simple.bat
```

Script này tạo shortcut **KHÔNG cần** win32com!

---

## 📞 **Cần thêm hỗ trợ?**

Chạy các lệnh sau và gửi kết quả:

```bash
# 1. Python version
python --version

# 2. Conda prefix
echo %CONDA_PREFIX%

# 3. Check pywin32
pip show pywin32

# 4. Test imports
python -c "import win32com.client; print('OK')"

# 5. Find post-install script
dir /s /b "%CONDA_PREFIX%\*pywin32_postinstall.py"
```
