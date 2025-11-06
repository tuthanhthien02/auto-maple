# 📦 Hướng Dẫn Chuyển File Build Vào VMware

## 📋 **TỔNG QUAN**

Có nhiều cách để chuyển file build (compiled executable) từ Host vào VMware. Guide này sẽ hướng dẫn các phương pháp phổ biến nhất.

---

## 🚀 **PHƯƠNG PHÁP 1: VMware Shared Folders** ⭐⭐⭐⭐⭐ RECOMMENDED

### **Ưu Điểm:**

-   ✅ Nhanh và tiện lợi nhất
-   ✅ Tự động sync giữa Host và VM
-   ✅ Không cần network setup
-   ✅ Dễ sử dụng

### **Yêu Cầu:**

-   ✅ VMware Tools đã được cài đặt trong VM
-   ✅ Shared Folders đã được enable

### **Cách Làm:**

#### **Bước 1: Enable Shared Folders trong VMware**

1. **VM đang TẮT** hoặc **đang CHẠY** (cả 2 đều được)
2. **VM → Settings → Options → Shared Folders**
3. Chọn **"Always enabled"** hoặc **"Enabled"**
4. Click **"Add..."** để thêm folder
5. Chọn folder trên Host (ví dụ: `C:\Users\YourName\Desktop\auto-maple\dist`)
6. Đặt tên share (ví dụ: `auto-maple-build`)
7. Check **"Enable this share"**
8. Click **"Finish"**
9. Click **"OK"**

#### **Bước 2: Access Shared Folder từ VM**

**Trên Windows VM:**

-   Shared folder sẽ xuất hiện tại: `\\vmware-host\Shared Folders\auto-maple-build`
-   Hoặc: `\\vmware-host\Shared Folders\[tên share]`
-   Hoặc: Trong File Explorer → Network → vmware-host → Shared Folders

**Trên Linux VM:**

-   Shared folder thường mount tại: `/mnt/hgfs/auto-maple-build`
-   Hoặc: `/mnt/hgfs/[tên share]`

#### **Bước 3: Copy File Build**

1. **Trên Host:** Copy file build vào shared folder

    ```
    C:\Users\...\auto-maple\dist\ExplorerSettings.exe
    → Copy vào shared folder
    ```

2. **Trên VM:** Access shared folder và copy file vào VM
    ```
    \\vmware-host\Shared Folders\auto-maple-build\ExplorerSettings.exe
    → Copy vào Desktop hoặc folder mong muốn
    ```

---

## 🌐 **PHƯƠNG PHÁP 2: Network Share (SMB)** ⭐⭐⭐⭐

### **Ưu Điểm:**

-   ✅ Không cần VMware Tools
-   ✅ Hoạt động với mọi VM
-   ✅ Có thể share nhiều folders

### **Yêu Cầu:**

-   ✅ Host và VM cùng network (NAT hoặc Bridged)
-   ✅ File sharing enabled trên Host

### **Cách Làm:**

#### **Bước 1: Share Folder trên Host**

1. **Right-click** folder chứa file build (ví dụ: `dist` folder)
2. Chọn **"Properties"**
3. Tab **"Sharing"**
4. Click **"Share..."**
5. Chọn user hoặc **"Everyone"**
6. Set permissions: **"Read/Write"**
7. Click **"Share"**
8. Note lại network path (ví dụ: `\\DESKTOP-ABC123\dist`)

#### **Bước 2: Access từ VM**

**Trên Windows VM:**

1. Mở **File Explorer**
2. Gõ vào address bar: `\\[IP của Host]\dist`
    - Hoặc: `\\DESKTOP-ABC123\dist`
3. Nhập username/password của Host nếu được hỏi
4. Copy file build vào VM

**Tìm IP của Host:**

```bash
# Trên Host, chạy:
ipconfig
# Tìm IPv4 Address (ví dụ: 192.168.1.100)
```

**Trên Linux VM:**

```bash
# Mount SMB share
sudo mkdir /mnt/host-share
sudo mount -t cifs //192.168.1.100/dist /mnt/host-share -o username=YourUsername,password=YourPassword

# Copy file
cp /mnt/host-share/ExplorerSettings.exe ~/Desktop/

# Unmount khi xong
sudo umount /mnt/host-share
```

---

## 📋 **PHƯƠNG PHÁP 3: Copy/Paste (VMware Tools)** ⭐⭐⭐

### **Ưu Điểm:**

-   ✅ Đơn giản, không cần setup
-   ✅ Hoạt động với clipboard

### **Yêu Cầu:**

-   ✅ VMware Tools đã được cài đặt
-   ✅ Copy/Paste enabled trong VM settings

### **Cách Làm:**

#### **Bước 1: Enable Copy/Paste**

1. **VM → Settings → Options → Guest Isolation**
2. Check **"Enable copy and paste"**
3. Click **"OK"**

#### **Bước 2: Copy File**

**Cách 1: Copy file trực tiếp**

-   **Trên Host:** Right-click file → Copy
-   **Trên VM:** Right-click Desktop → Paste

**Cách 2: Copy qua Explorer**

-   **Trên Host:** Copy file từ Explorer
-   **Trên VM:** Paste vào Explorer

**Lưu ý:** File lớn có thể mất thời gian, không khuyến nghị cho file >100MB.

---

## 💾 **PHƯƠNG PHÁP 4: USB Passthrough** ⭐⭐⭐

### **Ưu Điểm:**

-   ✅ Không cần network
-   ✅ Hoạt động với mọi VM
-   ✅ Tốc độ nhanh

### **Yêu Cầu:**

-   ✅ USB drive (USB flash, external HDD)
-   ✅ USB passthrough enabled trong VM

### **Cách Làm:**

#### **Bước 1: Copy File vào USB trên Host**

1. Cắm USB vào Host
2. Copy file build vào USB:
    ```
    ExplorerSettings.exe → USB drive
    ```

#### **Bước 2: Passthrough USB vào VM**

1. **VM đang CHẠY**
2. **VM → Removable Devices → [USB Drive Name] → Connect (Disconnect from Host)**
3. USB sẽ disconnect từ Host và connect vào VM

#### **Bước 3: Copy File từ USB trong VM**

1. **Trên VM:** Mở USB drive
2. Copy file build vào VM (Desktop hoặc folder mong muốn)
3. **Disconnect USB** khi xong:
    - **VM → Removable Devices → [USB Drive Name] → Disconnect (Connect to Host)**

---

## ☁️ **PHƯƠNG PHÁP 5: Cloud Storage** ⭐⭐⭐⭐

### **Ưu Điểm:**

-   ✅ Không cần network setup
-   ✅ Có thể access từ bất kỳ đâu
-   ✅ Backup tự động

### **Yêu Cầu:**

-   ✅ Internet connection trên cả Host và VM
-   ✅ Cloud storage account (OneDrive, Google Drive, Dropbox, etc.)

### **Cách Làm:**

#### **Bước 1: Upload File lên Cloud**

1. **Trên Host:** Upload file build lên cloud storage
    - OneDrive: Copy vào OneDrive folder
    - Google Drive: Upload qua web hoặc desktop app
    - Dropbox: Copy vào Dropbox folder

#### **Bước 2: Download từ VM**

1. **Trên VM:** Mở browser hoặc cloud storage app
2. Download file build từ cloud
3. Save vào VM

---

## 🔧 **PHƯƠNG PHÁP 6: FTP/SCP (Advanced)** ⭐⭐

### **Ưu Điểm:**

-   ✅ Tốc độ nhanh với file lớn
-   ✅ Có thể script tự động

### **Yêu Cầu:**

-   ✅ FTP/SSH server trên Host hoặc VM
-   ✅ Network connection

### **Cách Làm:**

#### **Setup FTP Server trên Host:**

1. **Enable FTP Server trên Windows:**

    - Control Panel → Programs → Turn Windows features on/off
    - Check **"Internet Information Services"** → **"FTP Server"**
    - OK

2. **Configure FTP:**

    - IIS Manager → Add FTP Site
    - Set physical path (folder chứa file build)
    - Set port (21)
    - Allow Anonymous hoặc set credentials

3. **Access từ VM:**
    ```bash
    # Trên VM, dùng FileZilla hoặc command line:
    ftp 192.168.1.100
    # Login và download file
    ```

---

## 📊 **SO SÁNH CÁC PHƯƠNG PHÁP**

| Phương Pháp         | Tốc Độ     | Độ Khó | Yêu Cầu      | Khuyến Nghị    |
| ------------------- | ---------- | ------ | ------------ | -------------- |
| **Shared Folders**  | ⭐⭐⭐⭐⭐ | ⭐     | VMware Tools | ✅ **BEST**    |
| **Network Share**   | ⭐⭐⭐⭐   | ⭐⭐   | Network      | ✅ **GOOD**    |
| **Copy/Paste**      | ⭐⭐⭐     | ⭐     | VMware Tools | ⚠️ Small files |
| **USB Passthrough** | ⭐⭐⭐⭐   | ⭐⭐   | USB drive    | ✅ **GOOD**    |
| **Cloud Storage**   | ⭐⭐⭐     | ⭐     | Internet     | ✅ **GOOD**    |
| **FTP/SCP**         | ⭐⭐⭐⭐   | ⭐⭐⭐ | Server setup | ⚠️ Advanced    |

---

## 🎯 **KHUYẾN NGHỊ**

### **Cho File Build (Executable):**

1. ✅ **VMware Shared Folders** - Nhanh nhất, tiện nhất
2. ✅ **Network Share** - Nếu không có VMware Tools
3. ✅ **USB Passthrough** - Nếu cần transfer nhanh

### **Workflow Khuyến Nghị:**

```batch
REM Step 1: Build trên Host
pyinstaller ExplorerSettings.spec
REM File build: dist\ExplorerSettings.exe

REM Step 2: Copy vào Shared Folder
copy dist\ExplorerSettings.exe "\\vmware-host\Shared Folders\auto-maple-build\"

REM Step 3: Trên VM, copy từ Shared Folder vào Desktop
REM \\vmware-host\Shared Folders\auto-maple-build\ExplorerSettings.exe
REM → Copy vào Desktop
```

---

## ⚠️ **TROUBLESHOOTING**

### **Shared Folders Không Hiện:**

**Nguyên nhân:**

-   VMware Tools chưa được cài đặt
-   Shared Folders chưa được enable

**Giải pháp:**

1. **Cài đặt VMware Tools:**

    - VM → Install VMware Tools
    - Follow wizard
    - Restart VM

2. **Enable Shared Folders:**
    - VM → Settings → Options → Shared Folders
    - Check "Always enabled"
    - Add folder nếu chưa có

### **Network Share Không Access Được:**

**Nguyên nhân:**

-   Firewall blocking
-   Network discovery disabled
-   Wrong credentials

**Giải pháp:**

1. **Disable Firewall tạm thời** để test
2. **Enable Network Discovery:**
    - Control Panel → Network and Sharing Center
    - Change advanced sharing settings
    - Enable network discovery
3. **Check credentials:**
    - Dùng username/password của Host
    - Hoặc enable Guest access

### **Copy/Paste Không Hoạt Động:**

**Nguyên nhân:**

-   VMware Tools chưa được cài đặt
-   Copy/Paste disabled

**Giải pháp:**

1. **Reinstall VMware Tools**
2. **Enable Copy/Paste:**
    - VM → Settings → Options → Guest Isolation
    - Check "Enable copy and paste"

---

## 📝 **QUICK REFERENCE**

### **Shared Folders Path:**

**Windows VM:**

```
\\vmware-host\Shared Folders\[share name]
```

**Linux VM:**

```
/mnt/hgfs/[share name]
```

### **Network Share Path:**

**Windows VM:**

```
\\[Host IP]\[share name]
\\[Host Name]\[share name]
```

**Linux VM:**

```
//[Host IP]/[share name]
```

---

## ✅ **CHECKLIST**

### **Before Transferring:**

-   [ ] File build đã được compile thành công
-   [ ] File build location: `dist\ExplorerSettings.exe`
-   [ ] Chọn phương pháp transfer phù hợp
-   [ ] Setup phương pháp (nếu cần)

### **After Transferring:**

-   [ ] File đã được copy vào VM
-   [ ] File location trong VM (ví dụ: Desktop)
-   [ ] Test chạy file trong VM
-   [ ] Verify file không bị corrupt

---

**REMEMBER:** VMware Shared Folders là phương pháp nhanh nhất và tiện nhất! ⭐
