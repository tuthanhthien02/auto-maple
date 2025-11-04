# 🚨 NGS Detection với VMware - Troubleshooting Guide

## 📋 Vấn đề

**Error:** `NGS Hacking Detected (0xD2020201)`  
**Message:** "You cannot run the game and external programs simultaneously"

**Nguyên nhân:** NGS (Nexon Game Security) detect VMware processes trên máy host, ngay cả khi bot chưa chạy.

---

## 🔍 Tại sao VMware bị NGS detect?

### **1. VMware Processes được NGS coi là Suspicious**

NGS có thể detect các processes sau:

-   `vmware.exe` - VMware Workstation main process
-   `vmware-vmx.exe` - VM process
-   `vmware-usbarbitrator.exe` - USB arbitration service
-   `vmware-hostd.exe` - Host daemon
-   `vmware-authd.exe` - Authentication service
-   `vmware-tray.exe` - System tray process
-   `vmware-converter.exe` - Converter process
-   `vmware-vprobe.exe` - VM probe tool

### **2. VMware Registry Keys**

NGS có thể scan registry cho VMware keys:

-   `HKEY_LOCAL_MACHINE\SOFTWARE\VMware, Inc.`
-   `HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Services\vmware*`

### **3. VMware Services**

NGS có thể detect services:

-   `VMAuthdService` - VMware Authentication Service
-   `VMwareHostOpen` - VMware Host Service
-   `VMUSBArbService` - VMware USB Arbitration Service
-   `VMware NAT Service`

### **4. VMware Files/Drivers**

NGS có thể scan cho VMware files:

-   `vmware*.sys` drivers
-   `vmware*.dll` libraries
-   VMware installation directory

---

## ✅ Giải pháp

### **Solution 1: Chạy Game trên Host, Bot trên VM** ⭐ RECOMMENDED

**Setup:**

```
HOST Machine
├── MapleStory (Game) - Chạy trực tiếp trên Host
└── VM1 → Bot → Arduino → TCP → Host
```

**Ưu điểm:**

-   ✅ Game không detect VMware vì không chạy cùng process space
-   ✅ Bot chạy trên VM độc lập
-   ✅ NGS không scan VM processes

**Setup Steps:**

1. Game chạy trên Host
2. Bot chạy trên VM
3. Bot gửi commands qua TCP → Host → Arduino

---

### **Solution 2: Stop VMware Services khi chơi Game**

**Các services cần stop:**

```batch
# Stop VMware services
net stop VMAuthdService
net stop VMwareHostOpen
net stop VMUSBArbService
net stop "VMware NAT Service"

# Stop VMware processes
taskkill /F /IM vmware.exe
taskkill /F /IM vmware-tray.exe
taskkill /F /IM vmware-usbarbitrator.exe
```

**⚠️ Lưu ý:**

-   VMs sẽ bị disconnect khi stop services
-   Cần restart services sau khi chơi game

---

### **Solution 3: Rename VMware Processes** (Advanced)

Rename VMware processes để tránh detection:

```batch
# Rename VMware executables
ren "C:\Program Files\VMware\VMware Workstation\vmware.exe" "VMSystem.exe"
ren "C:\Program Files\VMware\VMware Workstation\vmware-tray.exe" "VMTray.exe"
```

**⚠️ Risks:**

-   VMware có thể không hoạt động sau khi rename
-   Updates có thể restore tên gốc
-   Cần permissions cao

---

### **Solution 4: Sandbox VMware** (Advanced)

Chạy VMware trong sandbox để hide processes:

1. **Dùng Sandboxie** (deprecated nhưng vẫn work)
2. **Dùng Windows Sandbox** (Windows 10/11 Pro)
3. **Dùng Hyper-V** isolation (Windows Pro)

**⚠️ Lưu ý:**

-   Performance có thể giảm
-   Setup phức tạp

---

### **Solution 5: Chạy Game trên VM thay vì Host** ⭐ BEST

**Setup:**

```
HOST Machine
└── VM1 → MapleStory (Game) + Bot → Arduino
```

**Ưu điểm:**

-   ✅ Host không có game → NGS không scan host
-   ✅ Game và bot cùng VM → không có VMware detection
-   ✅ Isolation tốt

**Setup Steps:**

1. Cài MapleStory trên VM
2. Chạy bot trên VM
3. Arduino connect trực tiếp vào VM (USB passthrough)

---

### **Solution 6: Hide VMware từ Process List** (Advanced)

Dùng process hiding techniques (advanced, có risk):

1. **Process Hollowing** - Hide process trong legitimate process
2. **DLL Injection** - Inject vào legitimate process
3. **Rootkit** - Hide từ kernel level

**⚠️ WARNING:**

-   Rất phức tạp và có risk
-   Có thể vi phạm TOS
-   Không khuyến khích

---

## 🛠️ Diagnostic Script

### **Check VMware Processes**

```powershell
# Check VMware processes
Get-Process | Where-Object {$_.ProcessName -like "*vmware*"} | Select-Object ProcessName, Id, Path

# Check VMware services
Get-Service | Where-Object {$_.DisplayName -like "*VMware*"} | Select-Object Name, Status, DisplayName

# Check VMware registry keys
Get-ItemProperty "HKLM:\SOFTWARE\VMware, Inc." -ErrorAction SilentlyContinue
```

---

## 📊 Comparison Table

| Solution                        | Difficulty         | Effectiveness | Risk      | Recommendation     |
| ------------------------------- | ------------------ | ------------- | --------- | ------------------ |
| **Game trên Host, Bot trên VM** | ⭐ Easy            | 🟢 High       | 🟢 Low    | ⭐⭐⭐ RECOMMENDED |
| **Stop VMware Services**        | ⭐⭐ Medium        | 🟡 Medium     | 🟡 Medium | ⭐⭐               |
| **Rename Processes**            | ⭐⭐⭐ Hard        | 🟡 Medium     | 🟡 Medium | ⭐                 |
| **Sandbox VMware**              | ⭐⭐⭐ Hard        | 🟡 Medium     | 🟡 Medium | ⭐                 |
| **Game trên VM**                | ⭐⭐ Medium        | 🟢 High       | 🟢 Low    | ⭐⭐⭐ BEST        |
| **Process Hiding**              | ⭐⭐⭐⭐ Very Hard | 🟢 High       | 🔴 High   | ❌ NOT RECOMMENDED |

---

## 🎯 Recommended Approach

### **Option A: Game trên Host, Bot trên VM** (Current Setup)

**Steps:**

1. ✅ Game chạy trên Host (không detect VMware)
2. ✅ Bot chạy trên VM (độc lập)
3. ✅ Bot gửi commands qua TCP → Host → Arduino

**If vẫn bị detect:**

-   Check xem có VMware processes nào đang chạy trên Host không
-   Stop VMware services trước khi chơi game
-   Hoặc chuyển sang Option B

---

### **Option B: Game trên VM** (Best for Stealth)

**Steps:**

1. ✅ Cài MapleStory trên VM
2. ✅ Bot chạy trên VM
3. ✅ Arduino USB passthrough vào VM

**Benefits:**

-   ✅ Host hoàn toàn clean (không có game, không có VMware processes)
-   ✅ Game và bot cùng VM → không detect VMware
-   ✅ Isolation tốt nhất

---

## 🔧 Quick Fix Script

Tạo script để stop VMware services khi chơi game:

```batch
@echo off
REM stop_vmware_for_game.bat
echo Stopping VMware services for game...

net stop VMAuthdService 2>nul
net stop VMwareHostOpen 2>nul
net stop VMUSBArbService 2>nul
net stop "VMware NAT Service" 2>nul

taskkill /F /IM vmware.exe 2>nul
taskkill /F /IM vmware-tray.exe 2>nul
taskkill /F /IM vmware-usbarbitrator.exe 2>nul

echo VMware services stopped!
echo Launch MapleStory now...
pause
```

**Restart script:**

```batch
@echo off
REM start_vmware_after_game.bat
echo Starting VMware services...

net start VMAuthdService
net start VMwareHostOpen
net start VMUSBArbService
net start "VMware NAT Service"

echo VMware services started!
pause
```

---

## ⚠️ Important Notes

1. **NGS Detection là Real-time:**

    - NGS scan liên tục, không chỉ lúc start game
    - Nếu detect VMware sau khi vào game → vẫn disconnect

2. **VMware Detection Methods:**

    - Process scanning
    - Service scanning
    - Registry scanning
    - File scanning
    - Driver scanning

3. **Best Practice:**
    - **Chạy Game trên VM** là cách tốt nhất
    - Hoặc **Stop VMware services** trước khi chơi game
    - **Không chạy Game và VMware cùng lúc trên Host**

---

## 🚀 Next Steps

1. **Test Solution 1** (Game trên Host, Bot trên VM):

    - Stop VMware services
    - Chạy game
    - Nếu vẫn detect → chuyển Solution 5

2. **Nếu vẫn detect → Chuyển Solution 5** (Game trên VM):

    - Cài MapleStory trên VM
    - Bot và Game cùng VM
    - USB passthrough Arduino vào VM

3. **Monitor NGS Detection:**
    - Check xem khi nào bị detect
    - Log các VMware processes đang chạy
    - Fine-tune solution

---

**Status:** ⚠️ **VMware Detection là vấn đề phổ biến với NGS anti-cheat. Solution tốt nhất là chạy Game trên VM thay vì Host.**

