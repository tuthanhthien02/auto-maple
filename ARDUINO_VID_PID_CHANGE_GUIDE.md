# 🎯 Arduino Phase 2 - Change VID/PID Implementation Guide

## 📋 **TẠI SAO CHANGE VID/PID?**

### **Vấn đề:**

- ✅ **Arduino VID/PID** có thể được NGS học và detect
- ✅ **Common Arduino VID/PIDs:**
  - `VID_2341` (Arduino LLC)
  - `VID_1B4F` (SparkFun)
  - `PID_0036` (Arduino Leonardo)
  - `PID_0037` (Arduino Micro)
- ✅ **NGS có thể có database** của automation device VID/PIDs

### **Risk:**

⚠️ **MEDIUM RISK** - NGS có thể detect Arduino qua VID/PID

---

## 🔧 **HOW TO CHANGE VID/PID**

### **Step 1: Enable VID/PID Change in Script**

**File:** `modify_arduino_device_name.py`

**Change:**
```python
# Before:
CHANGE_VID_PID = False  # Disable VID/PID change

# After:
CHANGE_VID_PID = True  # Enable VID/PID change
```

**Configure VID/PID:**
```python
# Example: Logitech VID/PID (generic keyboard)
NEW_VID = "0x046D"  # Logitech VID
NEW_PID = "0xC077"  # Generic keyboard PID

# Or use other generic VID/PID:
# NEW_VID = "0x04D9"  # Holtek (generic keyboard)
# NEW_PID = "0x0001"  # Generic keyboard PID
```

---

### **Step 2: Run Script**

```batch
python modify_arduino_device_name.py
```

**Script sẽ:**
1. Modify device name
2. Modify VID/PID (if enabled)
3. Backup boards.txt
4. Verify modifications

---

### **Step 3: Manual Change (Alternative)**

**File:** `boards.txt`

**Tìm dòng:**
```ini
pro.vid.0=0x2341
pro.pid.0=0x0037
```

**Thay đổi thành:**
```ini
pro.vid.0=0x046D  # Logitech VID (example)
pro.pid.0=0xC077  # Generic keyboard PID (example)
```

---

## ⚠️ **IMPORTANT WARNINGS**

### **1. Valid VID/PID Only:**

- ⚠️ **KHÔNG dùng VID/PID đã được đăng ký** bởi nhà sản xuất khác
- ✅ Chỉ dùng generic VID/PID hoặc tự đăng ký VID/PID

### **2. Driver Issues:**

- ⚠️ **Change VID/PID có thể gây driver issues**
- ✅ Test kỹ sau khi change VID/PID
- ✅ Có thể cần reinstall drivers

### **3. Legal Considerations:**

- ⚠️ **Sử dụng VID/PID của nhà sản xuất khác có thể vi phạm pháp luật**
- ✅ Chỉ dùng generic/unregistered VID/PID
- ✅ Hoặc đăng ký VID/PID riêng (costly)

---

## 📊 **VID/PID OPTIONS**

### **Option 1: Generic Keyboard VID/PID (Recommended)**

**Examples:**
```python
# Logitech (generic keyboard)
NEW_VID = "0x046D"  # Logitech VID
NEW_PID = "0xC077"  # Generic keyboard PID

# Holtek (generic keyboard)
NEW_VID = "0x04D9"  # Holtek VID
NEW_PID = "0x0001"  # Generic keyboard PID

# Chicony (generic keyboard)
NEW_VID = "0x04F2"  # Chicony VID
NEW_PID = "0x0111"  # Generic keyboard PID
```

**Risk:** ✅ **LOW** - Generic keyboard VID/PID không có automation signatures

---

### **Option 2: Keep Arduino VID/PID (Safer)**

**Keep default:**
```python
CHANGE_VID_PID = False  # Don't change VID/PID
```

**Risk:** ⚠️ **MEDIUM** - Arduino VID/PID có thể bị detect

**Reason:**
- Device name đã change → Giảm detection risk đáng kể
- VID/PID change có thể gây driver issues
- Device name change đủ để giảm risk từ HIGH → MEDIUM

---

## 🎯 **RECOMMENDATION**

### **Priority 1: Change Device Name** ⭐⭐⭐⭐ **RECOMMENDED**

**Why:**
- ✅ Easy to implement
- ✅ Low risk
- ✅ High effectiveness
- ✅ No driver issues

**Result:** Risk reduction từ HIGH → MEDIUM

---

### **Priority 2: Change VID/PID** ⭐⭐⭐ **OPTIONAL**

**Why:**
- ✅ Further risk reduction
- ⚠️ May cause driver issues
- ⚠️ Requires valid VID/PID
- ⚠️ Legal considerations

**Result:** Risk reduction từ MEDIUM → LOW (additional)

---

## 📋 **IMPLEMENTATION STEPS**

### **Step 1: Change Device Name (DONE)**

- ✅ Device name đã change thành "USB Keyboard"
- ✅ Manufacturer đã change thành "Generic"

---

### **Step 2: Change VID/PID (OPTIONAL)**

**Enable in script:**
```python
CHANGE_VID_PID = True
NEW_VID = "0x046D"  # Example
NEW_PID = "0xC077"  # Example
```

**Run script:**
```batch
python modify_arduino_device_name.py
```

**Verify:**
- Check Device Manager → Properties → Details
- Verify VID/PID đã change

---

## 🔍 **VERIFY VID/PID**

### **Method 1: Device Manager**

1. **Windows + X → Device Manager**
2. **Keyboards → Find your device**
3. **Right-click → Properties → Details**
4. **Property:** `Hardware Ids`
5. **Value:** Should show new VID/PID (e.g., `VID_046D&PID_C077`)

### **Method 2: PowerShell**

```powershell
Get-PnpDevice | Where-Object {$_.Class -eq "Keyboard"} | Select-Object FriendlyName, InstanceId
```

**Expected output:**
- Should see new VID/PID in InstanceId (e.g., `HID\VID_046D&PID_C077`)

---

## ⚠️ **TROUBLESHOOTING**

### **Issue 1: Driver Not Found After VID/PID Change**

**Solution:**
1. Unplug Arduino
2. Reinstall Arduino drivers
3. Plug Arduino back in
4. Windows will install drivers for new VID/PID

---

### **Issue 2: Device Not Recognized**

**Solution:**
1. Check VID/PID is valid
2. Try different VID/PID
3. Or revert to original VID/PID

---

### **Issue 3: Arduino IDE Can't Upload**

**Solution:**
1. Check boards.txt modification
2. Restart Arduino IDE
3. Try different COM port
4. Or revert VID/PID change

---

## 📊 **SUMMARY**

### **Current Status:**

- ✅ **Device Name:** Changed to "USB Keyboard"
- ✅ **Manufacturer:** Changed to "Generic"
- ❌ **VID/PID:** Not changed (disabled by default)

### **Next Steps:**

1. **Option 1: Keep Current (Recommended)**
   - Device name change đủ để giảm risk
   - No driver issues
   - Risk: MEDIUM

2. **Option 2: Change VID/PID (Advanced)**
   - Enable `CHANGE_VID_PID = True` in script
   - Configure valid VID/PID
   - Test carefully
   - Risk: LOW (but may have driver issues)

---

## 🎯 **RECOMMENDATION**

### **For Most Users:**

✅ **Keep VID/PID unchanged** (Device name change is enough)
- Device name change giảm risk từ HIGH → MEDIUM
- No driver issues
- Easier to maintain

### **For Advanced Users:**

⏳ **Change VID/PID** (Additional risk reduction)
- Further risk reduction (MEDIUM → LOW)
- May cause driver issues
- Requires valid VID/PID
- Test carefully

---

**REMEMBER:** Device name change is the most important step! VID/PID change is optional and may cause issues! ⭐

