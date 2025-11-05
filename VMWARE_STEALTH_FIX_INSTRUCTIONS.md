# Fix VMware Stealth - Hướng Dẫn Chi Tiết

## ⚠️ QUAN TRỌNG: Script phải chạy TRONG VM!

**Script này phải chạy TRONG VMware VM, không phải trên Host!**

Nếu bạn chạy trên Host, bạn sẽ thấy:

-   `vmware.exe` - VMware Workstation trên Host (NORMAL, không phải vấn đề)
-   `vmware-vmx.exe` - VM process manager trên Host (NORMAL, không phải vấn đề)

**Các processes này là bình thường và không cần fix!**

---

## 🔍 Phân Biệt Host vs VM

### **Host Processes (KHÔNG CẦN FIX):**

-   `vmware.exe` - VMware Workstation application
-   `vmware-vmx.exe` - VM process manager
-   `vmware-vmx-debug.exe` - Debug version

**Đây là processes của VMware Workstation trên Host, không phải trong VM!**

### **VM Processes (CẦN FIX):**

-   `vmwaretools.exe` - VMware Tools trong VM
-   `vmtoolsd.exe` - VMware Tools daemon trong VM
-   `vmwaretray.exe` - VMware Tools tray trong VM

**Đây là processes TRONG VM và cần disable!**

---

## ✅ Fix Các Vấn Đề Thực Sự

Từ kết quả check, có các vấn đề cần fix:

### **1. VMware NAT Service**

**Fix:**

```batch
REM Run as Administrator trong VM
sc config "VMware NAT Service" start= disabled
sc stop "VMware NAT Service"
```

Hoặc:

1. `services.msc` trong VM
2. Tìm "VMware NAT Service"
3. Disable và Stop

### **2. VmwareAutostartService**

**Fix:**

```batch
REM Run as Administrator trong VM
sc config "VmwareAutostartService" start= disabled
sc stop "VmwareAutostartService"
```

Hoặc:

1. `services.msc` trong VM
2. Tìm "VMware Autostart Service"
3. Disable và Stop

---

## 🔧 Updated Fix Script

Script `fix_vmware_stealth.bat` đã được update để:

1. ✅ Skip Host processes (`vmware.exe`, `vmware-vmx.exe`)
2. ✅ Disable "VMware NAT Service"
3. ✅ Disable "VmwareAutostartService"

**Chạy script trong VM:**

```batch
fix_vmware_stealth.bat
```

---

## 📋 Step-by-Step Fix (Trong VM)

### **Bước 1: Chạy Script Fix**

1. **Mở VM** (đang chạy Windows)
2. **Copy `fix_vmware_stealth.bat` vào VM**
3. **Right-click → Run as Administrator**
4. **Chờ script chạy xong**

### **Bước 2: Verify Services Đã Disable**

Mở Command Prompt (Run as Administrator) trong VM:

```batch
sc query "VMware NAT Service"
sc query "VmwareAutostartService"
sc query "vmci"
```

Tất cả phải hiển thị `STATE: STOPPED` và `START_TYPE: DISABLED`

### **Bước 3: Chạy Lại Stealth Check**

```batch
check_vmware_stealth.bat
```

**Kết quả mong đợi:**

```
✅ VMware Stealth Status: PASS
   Không tìm thấy VMware traces quan trọng.
```

Hoặc chỉ còn warnings về registry keys (đã disable, không quan trọng).

---

## 🎯 Checklist

-   [ ] Script chạy **TRONG VM** (không phải trên Host)
-   [ ] Disable "VMware NAT Service"
-   [ ] Disable "VmwareAutostartService"
-   [ ] Disable "vmci" service
-   [ ] Disable "VMTools" service
-   [ ] Restart VM
-   [ ] Chạy lại `check_vmware_stealth.bat` để verify

---

## 💡 Tips

### **Nếu vẫn thấy Host processes:**

-   Nếu bạn chạy script trên Host và thấy `vmware.exe`, `vmware-vmx.exe` → **Đây là bình thường**
-   Các processes này **KHÔNG cần fix** vì chúng là Host processes
-   Script đã được update để **skip** các Host processes này

### **Nếu service không disable được:**

1. **Check bạn đang chạy trong VM** (không phải Host)
2. **Check bạn có admin privileges**
3. **Try disable thủ công trong services.msc**

### **Nếu vẫn có HIGH RISK sau khi fix:**

1. **Restart VM** (services cần restart để apply)
2. **Check lại services** đã disable chưa
3. **Check processes** còn đang chạy không

---

## 📝 Summary

**Vấn đề:**

-   Script đang detect Host processes (`vmware.exe`, `vmware-vmx.exe`) → **Bình thường, không cần fix**
-   Cần fix: "VMware NAT Service" và "VmwareAutostartService" **TRONG VM**

**Solution:**

1. ✅ **Chạy script TRONG VM** (không phải Host)
2. ✅ **Disable services** trong VM
3. ✅ **Restart VM** để apply
4. ✅ **Verify** với `check_vmware_stealth.bat`

**Kết quả:**

-   ✅ Không còn HIGH RISK issues
-   ✅ Chỉ còn warnings về registry keys (đã disable, không quan trọng)
