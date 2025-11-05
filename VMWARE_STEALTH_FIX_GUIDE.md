# VMware Stealth Fix Guide - Hướng Dẫn Fix NGS Detection

## 📋 Tổng Quan

Script `check_vmware_stealth.py` đã phát hiện các VMware traces có thể bị NGS detect. Guide này sẽ hướng dẫn cách fix từng vấn đề.

---

## 🔴 HIGH RISK ISSUES - Cách Fix

### **1. VMware Registry Keys**

**Vấn đề:**

-   Registry keys như `HKLM\SYSTEM\CurrentControlSet\Services\vmci` tồn tại
-   Đây là VMware Communication Interface service

**⚠️ Lưu ý:**

-   Registry keys **KHÔNG THỂ xóa hoàn toàn** (vì là phần của VMware installation)
-   Nhưng có thể **disable service** để giảm detection risk

**Cách Fix:**

#### **Option 1: Disable VMware Services (RECOMMENDED)**

1. **Mở Services Manager:**

    - Press `Win + R`
    - Type `services.msc`
    - Press Enter

2. **Tìm và Disable các VMware services:**
    - Tìm các services có tên bắt đầu với "VMware":
        - `VMware Tools`
        - `VMware USB Arbitration Service`
        - `VMware Authorization Service`
        - `VMware Host Open Service`
        - `VMCI` (VMware Communication Interface)
3. **Disable từng service:**

    - Double-click vào service
    - Set **Startup type** = **Disabled**
    - Click **Stop** (nếu đang chạy)
    - Click **OK**

4. **Restart VM** để áp dụng changes

#### **Option 2: Disable từ Command Line (Nhanh hơn)**

```batch
REM Run as Administrator
sc config "VMTools" start= disabled
sc stop "VMTools"

sc config "VMUSBArbService" start= disabled
sc stop "VMUSBArbService"

sc config "VMwareHostOpen" start= disabled
sc stop "VMwareHostOpen"

sc config "vmci" start= disabled
sc stop "vmci"
```

**Lưu ý:** Một số services có thể không tồn tại tùy vào VMware version.

---

### **2. VMware Processes**

**Vấn đề:**

-   Các processes như `vmwaretools.exe`, `vmtoolsd.exe` đang chạy

**Cách Fix:**

#### **Option 1: Disable VMware Tools**

1. **VM đang CHẠY**
2. VM → Settings → Options → VMware Tools
3. Uncheck **"Time synchronization between guest and host"**
4. Uncheck **"Enable VMware Tools background services"**
5. Click **OK**

#### **Option 2: Kill Processes Thủ Công**

```batch
REM Run as Administrator
taskkill /F /IM vmwaretools.exe
taskkill /F /IM vmtoolsd.exe
taskkill /F /IM vmwaretray.exe
taskkill /F /IM vmwareuser.exe
```

**⚠️ Lưu ý:** Processes có thể tự động restart nếu VMware Tools đang enabled.

---

### **3. VMware Services**

**Vấn đề:**

-   Các services như `vmware-tools`, `vmci` đang chạy

**Cách Fix:**

Xem phần **"1. VMware Registry Keys"** ở trên (cùng cách disable services).

---

## 🟡 WARNINGS - Cách Fix

### **1. Hardware Traces**

**Vấn đề:**

-   Hardware devices có thể có VMware traces (VID/PID, ACPI devices)

**Cách Check:**

1. **Download RawInputViewer:**

    - Search "RawInputViewer" trên Google
    - Download và chạy tool

2. **Check các devices:**

    - Keyboard: Phải có VID/PID (không phải ACPI)
    - Mouse: Phải có VID/PID (không phải VMware VID/PID)

3. **Nếu phát hiện VMware traces:**

    **Fix cho Keyboard:**

    - ✅ Pass-through USB keyboard vào VM
    - ✅ Hoặc dùng Arduino HID Keyboard (RECOMMENDED)

    **Fix cho Mouse:**

    - ✅ Pass-through physical mouse vào VM
    - ✅ Hoặc dùng USB mouse thật

---

### **2. VM Detection Signatures**

**Vấn đề:**

-   File paths như `C:\Program Files\VMware` tồn tại

**⚠️ Lưu ý:**

-   File paths **KHÔNG THỂ xóa** (vì là VMware installation)
-   NGS sẽ không chỉ dựa vào file paths để detect
-   Quan trọng hơn là **processes, services, và hardware traces**

**Không cần fix** - Đây là normal và không thể tránh được.

---

## ✅ Step-by-Step Fix Process

### **Bước 1: Disable VMware Services**

1. Mở `services.msc`
2. Disable tất cả VMware services:
    - `VMware Tools`
    - `VMCI`
    - `VMware USB Arbitration Service`
    - `VMware Authorization Service`
    - `VMware Host Open Service`

### **Bước 2: Disable VMware Tools Features**

1. VM → Settings → Options → VMware Tools
2. Uncheck tất cả options
3. Click OK

### **Bước 3: Kill VMware Processes**

```batch
taskkill /F /IM vmwaretools.exe
taskkill /F /IM vmtoolsd.exe
taskkill /F /IM vmwaretray.exe
```

### **Bước 4: Restart VM**

1. Shutdown VM
2. Start lại VM
3. Chạy lại `check_vmware_stealth.bat` để verify

### **Bước 5: Setup Hardware Stealth**

1. **Keyboard:**

    - Pass-through USB keyboard vào VM
    - Hoặc dùng Arduino HID Keyboard (RECOMMENDED)

2. **Mouse:**

    - Pass-through physical mouse vào VM

3. **Check RawInputViewer:**
    - Verify không có VMware traces trong hardware devices

---

## 🎯 Quick Fix Script

Tạo file `fix_vmware_stealth.bat`:

```batch
@echo off
echo ========================================
echo VMware Stealth Fix Script
echo ========================================
echo.
echo [WARNING] This script requires Administrator privileges!
echo.

REM Check admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Please run as Administrator!
    pause
    exit /b 1
)

echo [1/4] Stopping VMware processes...
taskkill /F /IM vmwaretools.exe >nul 2>&1
taskkill /F /IM vmtoolsd.exe >nul 2>&1
taskkill /F /IM vmwaretray.exe >nul 2>&1
taskkill /F /IM vmwareuser.exe >nul 2>&1
echo Done.

echo.
echo [2/4] Disabling VMware services...
sc config "VMTools" start= disabled >nul 2>&1
sc stop "VMTools" >nul 2>&1

sc config "VMUSBArbService" start= disabled >nul 2>&1
sc stop "VMUSBArbService" >nul 2>&1

sc config "VMwareHostOpen" start= disabled >nul 2>&1
sc stop "VMwareHostOpen" >nul 2>&1

sc config "vmci" start= disabled >nul 2>&1
sc stop "vmci" >nul 2>&1

echo Done.

echo.
echo [3/4] Checking results...
timeout /t 2 >nul

echo.
echo [4/4] Running stealth check...
python check_vmware_stealth.py

echo.
echo ========================================
echo Fix completed!
echo ========================================
echo.
echo [IMPORTANT] Restart VM to apply all changes!
echo.
pause
```

---

## 📊 Expected Results After Fix

Sau khi fix, script sẽ hiển thị:

```
✅ VMware Stealth Status: PASS
   Không tìm thấy VMware traces quan trọng.
```

Hoặc ít nhất giảm số lượng issues xuống 0-1 (chỉ còn registry keys - không thể tránh được).

---

## ⚠️ Important Notes

### **1. Registry Keys Không Thể Xóa Hoàn Toàn**

-   Registry keys như `HKLM\SYSTEM\CurrentControlSet\Services\vmci` là **bắt buộc** của VMware
-   **Không thể xóa** mà không làm hỏng VMware
-   **NGS sẽ không chỉ dựa vào registry keys** để detect
-   Quan trọng hơn là **processes, services, và hardware traces**

### **2. VMware Tools Disable**

-   Disable VMware Tools có thể làm mất một số tính năng:
    -   Copy/paste giữa Host và VM
    -   Drag & drop files
    -   Time synchronization
-   **Nhưng đây là trade-off** để tránh NGS detection

### **3. Hardware Traces Quan Trọng Nhất**

-   **Hardware traces** (VID/PID, ACPI devices) là **quan trọng nhất**
-   NGS sẽ check hardware devices để detect VM
-   **BẮT BUỘC** dùng:
    -   Arduino HID Keyboard (hardware riêng)
    -   Physical mouse pass-through

---

## 🎯 Final Recommendations

### **Must Do:**

1. ✅ **Disable VMware services** (services.msc)
2. ✅ **Disable VMware Tools features** (VM Settings)
3. ✅ **Dùng Arduino HID Keyboard** (hardware riêng)
4. ✅ **Pass-through physical mouse** vào VM

### **Should Do:**

1. ✅ **Check RawInputViewer** để verify hardware
2. ✅ **Restart VM** sau khi disable services
3. ✅ **Chạy lại stealth check** để verify

### **Nice to Have:**

1. ✅ **Minimize VMware processes** (kill không cần thiết)
2. ✅ **Disable VMware auto-start** (nếu có)

---

## 📝 Summary

**Các bước fix:**

1. **Disable VMware services** → Giảm detection risk
2. **Disable VMware Tools** → Giảm processes
3. **Setup hardware stealth** → Arduino HID + Physical mouse
4. **Verify với RawInputViewer** → Check hardware traces
5. **Restart VM** → Áp dụng changes

**Kết quả mong đợi:**

-   ✅ Không còn VMware processes đang chạy
-   ✅ Không còn VMware services đang chạy
-   ✅ Hardware devices không có VMware traces
-   ⚠️ Registry keys vẫn tồn tại (nhưng không quan trọng)

---

## 🔗 Related Files

-   `check_vmware_stealth.py` - Stealth checker script
-   `check_vmware_stealth.bat` - Batch file để chạy script
-   `USB_KEYBOARD_VMWARE_PASSTHROUGH.md` - Guide pass-through keyboard
-   `VMWARE_KEYBOARD_PASSTHROUGH_GUIDE.md` - General keyboard guide
