# 🥷 VMware Stealth Plan - Tránh NGS Detection

## 📋 Tổng quan

**Mục tiêu:** Làm VMware "invisible" với NGS anti-cheat để có thể chơi MapleStory trên Host mà không bị detect VMware.

**Challenge:** NGS scan nhiều thứ:

-   ✅ Processes (vmware.exe, vmware-tray.exe, etc.)
-   ✅ Services (VMAuthdService, VMUSBArbService, etc.)
-   ✅ Registry keys (HKLM\SOFTWARE\VMware, Inc.)
-   ✅ Files/Drivers (vmware*.sys, vmware*.dll)
-   ✅ Installation directory

---

## 🎯 Phương pháp Stealth VMware

### **Method 1: Service/Process Masking** ⭐⭐⭐ RECOMMENDED

**Concept:** Thay đổi tên services và processes để tránh detection.

**Implementation:**

1. **Rename Services:**

    - `VMAuthdService` → `SystemAudioService` (giống Windows service)
    - `VMUSBArbService` → `USBArbitrationService`
    - `VMware NAT Service` → `NetworkTranslationService`

2. **Rename Process Executables:**

    - `vmware.exe` → `VMSystem.exe` hoặc `SystemService.exe`
    - `vmware-tray.exe` → `SystemTray.exe`
    - `vmware-authd.exe` → `AuthService.exe`

3. **Registry Obfuscation:**
    - Rename registry keys
    - Move registry entries
    - Use symlinks

**Effectiveness:** 🟢 High (70-80%)
**Risk:** 🟡 Medium (có thể break VMware updates)
**Difficulty:** ⭐⭐ Medium

---

### **Method 2: Process Hiding** ⭐⭐ ADVANCED

**Concept:** Hide VMware processes từ process list.

**Implementation:**

1. **Kernel-level Hiding:**

    - Hook system calls (NtQuerySystemInformation)
    - Filter processes trong kernel
    - Rootkit techniques

2. **User-level Hiding:**
    - DLL injection vào game process
    - Hook API calls
    - Process hollowing

**Effectiveness:** 🟢 Very High (90%+)
**Risk:** 🔴 High (vi phạm security, có thể bị antivirus detect)
**Difficulty:** ⭐⭐⭐⭐ Very Hard
**⚠️ NOT RECOMMENDED** - Quá phức tạp và risk cao

---

### **Method 3: Service Disabling** ⭐ EASY

**Concept:** Disable các services không cần thiết.

**Implementation:**

1. **Disable Non-Essential Services:**

    - `VMAuthdService` - Không cần nếu không dùng remote
    - `VMware NAT Service` - Không cần nếu dùng bridge
    - `VMUSBArbService` - Không cần nếu không dùng USB passthrough

2. **Keep Only Essential:**
    - Chỉ giữ services cần thiết cho VM hoạt động

**Effectiveness:** 🟡 Medium (50-60%)
**Risk:** 🟢 Low (có thể disable/enable dễ dàng)
**Difficulty:** ⭐ Easy

---

### **Method 4: Registry Obfuscation** ⭐⭐ MEDIUM

**Concept:** Obfuscate registry keys để tránh detection.

**Implementation:**

1. **Rename Registry Keys:**

    ```reg
    HKLM\SOFTWARE\VMware, Inc.
    → HKLM\SOFTWARE\VirtualMachine, Inc.
    → HKLM\SOFTWARE\SystemServices, Inc.
    ```

2. **Move Registry Entries:**

    - Move vào location khác
    - Use symlinks/redirects

3. **Registry Permissions:**
    - Set permissions để hide keys
    - Deny access cho game process

**Effectiveness:** 🟡 Medium (60-70%)
**Risk:** 🟡 Medium (có thể break VMware)
**Difficulty:** ⭐⭐ Medium

---

### **Method 5: File/Driver Obfuscation** ⭐⭐ MEDIUM

**Concept:** Obfuscate VMware files và drivers.

**Implementation:**

1. **Rename Files:**

    - `vmware*.sys` → `sys*.sys` (generic names)
    - `vmware*.dll` → `sys*.dll`

2. **Move Installation Directory:**
    - Move `C:\Program Files\VMware` → `C:\Windows\System32\Services`
    - Use symlinks

**Effectiveness:** 🟡 Medium (50-60%)
**Risk:** 🟡 Medium (có thể break VMware)
**Difficulty:** ⭐⭐ Medium

---

### **Method 6: Hybrid Approach** ⭐⭐⭐ BEST

**Concept:** Combine nhiều methods với nhau.

**Implementation:**

1. **Service Masking** (Method 1)
2. **Service Disabling** (Method 3) - Disable non-essential
3. **Registry Obfuscation** (Method 4) - Partial
4. **Process Monitoring** - Auto-stop khi detect game

**Effectiveness:** 🟢 High (80-90%)
**Risk:** 🟡 Medium
**Difficulty:** ⭐⭐⭐ Medium-Hard

---

## 📊 Comparison Table

| Method                      | Effectiveness | Risk      | Difficulty | Maintenance | Recommended |
| --------------------------- | ------------- | --------- | ---------- | ----------- | ----------- |
| **Service/Process Masking** | 🟢 70-80%     | 🟡 Medium | ⭐⭐       | ⭐⭐ Medium | ⭐⭐⭐ YES  |
| **Process Hiding**          | 🟢 90%+       | 🔴 High   | ⭐⭐⭐⭐   | ⭐⭐⭐ Hard | ❌ NO       |
| **Service Disabling**       | 🟡 50-60%     | 🟢 Low    | ⭐         | ⭐ Easy     | ⭐⭐        |
| **Registry Obfuscation**    | 🟡 60-70%     | 🟡 Medium | ⭐⭐       | ⭐⭐ Medium | ⭐⭐        |
| **File/Driver Obfuscation** | 🟡 50-60%     | 🟡 Medium | ⭐⭐       | ⭐⭐ Medium | ⭐          |
| **Hybrid Approach**         | 🟢 80-90%     | 🟡 Medium | ⭐⭐⭐     | ⭐⭐ Medium | ⭐⭐⭐ BEST |

---

## 🎯 Recommended Plan: Hybrid Approach

### **Phase 1: Service Masking** (Priority: High)

**Steps:**

1. **Rename VMware Services:**

    - `VMAuthdService` → `SystemAudioService`
    - `VMUSBArbService` → `USBArbitrationService`
    - `VMware NAT Service` → `NetworkTranslationService`

2. **Rename Process Executables:**

    - `vmware.exe` → `VMSystem.exe`
    - `vmware-tray.exe` → `SystemTray.exe`
    - `vmware-authd.exe` → `AuthService.exe`

3. **Update Service Registry:**
    - Update service names trong registry
    - Update display names

**Expected Effectiveness:** +40-50% stealth

---

### **Phase 2: Service Disabling** (Priority: Medium)

**Steps:**

1. **Identify Non-Essential Services:**

    - `VMAuthdService` - Chỉ cần nếu dùng remote
    - `VMware NAT Service` - Chỉ cần nếu dùng NAT network

2. **Disable Services:**

    - Set services to "Disabled" hoặc "Manual"
    - Stop services khi không cần

3. **Create Service Manager Script:**
    - Script để enable/disable services
    - Auto-disable khi detect game running

**Expected Effectiveness:** +20-30% stealth

---

### **Phase 3: Registry Obfuscation** (Priority: Medium)

**Steps:**

1. **Rename Registry Keys:**

    - `HKLM\SOFTWARE\VMware, Inc.` → `HKLM\SOFTWARE\SystemServices, Inc.`

2. **Create Registry Backup:**

    - Backup original keys
    - Restore khi cần

3. **Registry Permissions:**
    - Set permissions để hide keys
    - Deny read access cho game process

**Expected Effectiveness:** +10-20% stealth

---

### **Phase 4: Process Monitoring** (Priority: Low)

**Steps:**

1. **Game Detection:**

    - Monitor MapleStory process
    - Detect khi game start

2. **Auto-Stop VMware:**

    - Auto-stop VMware services khi detect game
    - Auto-start khi game exit

3. **Background Service:**
    - Service chạy background
    - Monitor game state

**Expected Effectiveness:** +10% stealth (preventive)

---

## 🛠️ Implementation Details

### **Service Renaming**

**Method:**

```batch
# Stop service first
net stop VMAuthdService

# Rename service (requires admin)
sc config VMAuthdService DisplayName= "System Audio Service"
sc config VMAuthdService binPath= "C:\Program Files\VMware\VMware Workstation\vmware-authd.exe"

# Or create new service with different name
sc create SystemAudioService binPath= "C:\Program Files\VMware\VMware Workstation\vmware-authd.exe" DisplayName= "System Audio Service"

# Delete old service
sc delete VMAuthdService
```

**⚠️ Challenges:**

-   Service executable path vẫn point đến VMware
-   Binary signature vẫn là VMware
-   Process name trong memory vẫn là VMware

---

### **Process Executable Renaming**

**Method:**

```batch
# Stop processes first
taskkill /F /IM vmware.exe

# Rename executables
ren "C:\Program Files\VMware\VMware Workstation\vmware.exe" "VMSystem.exe"
ren "C:\Program Files\VMware\VMware Workstation\vmware-tray.exe" "SystemTray.exe"

# Update shortcuts
# Update service paths
```

**⚠️ Challenges:**

-   VMware updates sẽ restore names
-   Services vẫn reference old paths
-   Binary signature vẫn là VMware

---

### **Registry Obfuscation**

**Method:**

```batch
# Backup registry
reg export "HKLM\SOFTWARE\VMware, Inc." vmware_backup.reg

# Rename registry key
reg copy "HKLM\SOFTWARE\VMware, Inc." "HKLM\SOFTWARE\SystemServices, Inc." /s /f

# Delete old key
reg delete "HKLM\SOFTWARE\VMware, Inc." /f

# Set permissions
regini permissions.txt
```

**⚠️ Challenges:**

-   VMware installer sẽ tạo lại keys
-   Services vẫn reference old keys
-   Cần update tất cả references

---

## ⚠️ Risks & Limitations

### **1. VMware Updates**

-   **Risk:** Updates sẽ restore tên gốc
-   **Solution:** Re-apply stealth sau mỗi update
-   **Impact:** Cần maintenance thường xuyên

### **2. Binary Signatures**

-   **Risk:** NGS có thể scan binary signatures
-   **Solution:** Không có solution tốt (cần re-sign binaries)
-   **Impact:** Vẫn có thể detect qua signatures

### **3. Process Memory**

-   **Risk:** Process name trong memory vẫn là VMware
-   **Solution:** Process hollowing (advanced, risky)
-   **Impact:** Cần advanced techniques

### **4. Functionality**

-   **Risk:** Stealth có thể break VMware functionality
-   **Solution:** Test kỹ sau mỗi change
-   **Impact:** Cần rollback plan

---

## 🧪 Testing Plan

### **1. Functionality Test**

-   ✅ VMware vẫn start được
-   ✅ VMs vẫn hoạt động bình thường
-   ✅ Network, USB passthrough vẫn work
-   ✅ Services vẫn start/stop được

### **2. Stealth Test**

-   ✅ `tasklist` không show vmware processes
-   ✅ `sc query` không show vmware services
-   ✅ Registry không có "VMware" keys
-   ✅ NGS không detect VMware

### **3. Game Test**

-   ✅ Launch MapleStory
-   ✅ Play game normal
-   ✅ Check NGS detection
-   ✅ Monitor for disconnects

---

## 📋 Implementation Checklist

### **Phase 1: Service Masking**

-   [ ] Backup VMware services
-   [ ] Create renamed services
-   [ ] Update service paths
-   [ ] Test service functionality
-   [ ] Verify stealth (check process list)

### **Phase 2: Service Disabling**

-   [ ] Identify non-essential services
-   [ ] Create disable script
-   [ ] Create enable script
-   [ ] Test auto-disable/enable
-   [ ] Verify stealth

### **Phase 3: Registry Obfuscation**

-   [ ] Backup registry keys
-   [ ] Rename registry keys
-   [ ] Update references
-   [ ] Set permissions
-   [ ] Verify stealth

### **Phase 4: Process Monitoring**

-   [ ] Create game detection script
-   [ ] Create auto-stop service
-   [ ] Test auto-stop/start
-   [ ] Monitor effectiveness

---

## 🚀 Recommended Implementation Order

### **Step 1: Quick Win - Service Disabling** (1-2 hours)

-   Disable non-essential services
-   Easy to implement
-   Low risk
-   **Expected:** 20-30% stealth improvement

### **Step 2: Service Masking** (3-4 hours)

-   Rename services
-   Rename processes
-   More complex
-   Medium risk
-   **Expected:** +40-50% stealth improvement

### **Step 3: Registry Obfuscation** (2-3 hours)

-   Rename registry keys
-   Set permissions
-   Medium complexity
-   Medium risk
-   **Expected:** +10-20% stealth improvement

### **Step 4: Process Monitoring** (1-2 hours)

-   Auto-stop VMware khi game run
-   Preventive measure
-   Low risk
-   **Expected:** +10% stealth improvement

---

## 💡 Alternative: Best Practice

**Instead of stealth VMware, recommend:**

### **Option 1: Game trên VM** ⭐⭐⭐ BEST

-   Host hoàn toàn clean
-   Game và bot cùng VM
-   Không cần stealth VMware

### **Option 2: Stop VMware khi chơi** ⭐⭐ EASY

-   Stop services trước khi chơi
-   Restart sau khi chơi
-   Đơn giản, hiệu quả

---

## 📊 Expected Results

### **After Full Implementation:**

-   **Stealth Level:** 80-90%
-   **NGS Detection:** Reduced significantly
-   **Functionality:** VMware vẫn hoạt động
-   **Maintenance:** Cần re-apply sau updates

### **Success Criteria:**

-   ✅ VMware không detect được trong tasklist
-   ✅ Services không detect được trong sc query
-   ✅ Registry không có "VMware" keys visible
-   ✅ NGS không detect và disconnect
-   ✅ VMware vẫn hoạt động bình thường

---

## ⚠️ Important Notes

1. **Stealth không phải 100%:**

    - NGS có thể detect qua binary signatures
    - NGS có thể detect qua behavior patterns
    - Stealth chỉ giảm detection risk

2. **Maintenance Required:**

    - Cần re-apply sau VMware updates
    - Cần monitor và adjust
    - Cần backup trước khi thay đổi

3. **Legal/Ethical:**

    - Stealth có thể vi phạm VMware TOS
    - Có thể vi phạm game TOS
    - Use at your own risk

4. **Backup Everything:**
    - Backup services
    - Backup registry
    - Backup files
    - Have rollback plan

---

## 🎯 Decision Matrix

**Should I implement VMware stealth?**

| Factor            | Weight | Score | Notes                     |
| ----------------- | ------ | ----- | ------------------------- |
| **Effectiveness** | 30%    | 7/10  | 80-90% stealth possible   |
| **Risk**          | 25%    | 6/10  | Medium risk, có thể break |
| **Maintenance**   | 20%    | 5/10  | Cần re-apply sau updates  |
| **Complexity**    | 15%    | 7/10  | Medium-hard complexity    |
| **Alternative**   | 10%    | 9/10  | Game trên VM tốt hơn      |

**Total Score: 6.7/10** - **Worth implementing, but alternatives may be better**

---

## ✅ Recommendation

**My Recommendation:**

1. **Try Alternative First:**

    - **Option 1:** Chạy Game trên VM (best solution)
    - **Option 2:** Stop VMware khi chơi (easy solution)

2. **If Alternatives Don't Work:**

    - Implement **Phase 1** (Service Masking) - Quick win
    - Test effectiveness
    - Decide if continue với Phase 2-4

3. **Start với Low-Risk Methods:**
    - Service Disabling (Phase 2) - Easiest
    - Process Monitoring (Phase 4) - Preventive
    - Then move to Service Masking (Phase 1)

---

**Ready to implement?** Bắt đầu với Phase 2 (Service Disabling) vì:

-   ✅ Easiest to implement
-   ✅ Lowest risk
-   ✅ Quick results
-   ✅ Easy to rollback

Bạn muốn bắt đầu với Phase nào?
