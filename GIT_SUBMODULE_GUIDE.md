# 📚 GIT SUBMODULE - HƯỚNG DẪN

## 🔍 **SUBMODULE LÀ GÌ?**

```
Submodule = Git repo con bên trong Git repo cha

Project structure:
  auto-maple/          ← Main repo
    ├── resources/     ← Submodule (có .git riêng!)
    ├── src/
    ├── main.py
    └── .git/          ← Main repo's git

resources/ là một Git repo độc lập!
```

---

## ⚠️ **VẤN ĐỀ THƯỜNG GẶP**

### **Error: `modified: resources (untracked content)`**

```bash
$ git status
Changes not staged for commit:
        modified:   resources (untracked content)
                              ^^^^^^^^^^^^^^^^^^
                              Có files chưa commit trong submodule!

$ git add resources
$ git commit -m "Update"
❌ KHÔNG WORK! Vì changes chưa commit trong submodule!
```

---

## ✅ **GIẢI PHÁP**

### **Step-by-Step:**

```bash
# 1. Vào submodule
cd resources

# 2. Check status trong submodule
git status

# 3. Add & commit trong submodule
git add .
git commit -m "Update resources files"

# 4. Quay lại main repo
cd ..

# 5. Commit submodule reference update
git add resources
git commit -m "Update resources submodule"

# 6. Verify
git status
# → "nothing to commit, working tree clean" ✅
```

---

## ⚡ **ONE-LINER (Fast)**

```bash
cd resources && git add . && git commit -m "Update" && cd .. && git add resources && git commit -m "Update submodule"
```

---

## 🔧 **COMMON COMMANDS**

### **Check submodule status:**

```bash
git status
# Nếu thấy: modified: resources (new commits)
# → Submodule có commits mới, cần commit ở main repo
```

### **Update submodule to latest:**

```bash
cd resources
git pull origin main
cd ..
git add resources
git commit -m "Update submodule to latest"
```

### **Clone repo với submodule:**

```bash
git clone <repo-url>
cd <repo-name>
git submodule init
git submodule update
```

Or:

```bash
git clone --recursive <repo-url>
```

---

## 📊 **WORKFLOW DIAGRAM**

```
Make changes in resources/
    ↓
cd resources
    ↓
git add . && git commit -m "..."
    ↓
cd ..
    ↓
git add resources
    ↓
git commit -m "Update submodule"
    ↓
DONE! ✅
```

---

## 🎯 **TIPS**

1. **Always commit in submodule first!**

    ```
    Submodule changes PHẢI commit trước
    Main repo changes commit sau
    ```

2. **Check both repos:**

    ```bash
    # Main repo
    git status

    # Submodule
    cd resources && git status && cd ..
    ```

3. **Use aliases:**

    ```bash
    # Add to ~/.gitconfig
    [alias]
      subcommit = "!f() { cd resources && git add . && git commit -m \"$1\" && cd .. && git add resources && git commit -m \"Update submodule: $1\"; }; f"

    # Usage:
    git subcommit "My update message"
    ```

---

## 🚨 **VÍ DỤ CỤ THỂ (Hôm nay)**

### **Vấn đề:**

```bash
$ git add resources
$ git commit -m "Update"
❌ Fail: nothing to commit
```

### **Nguyên nhân:**

```
resources/ có 9 files untracked:
  - command_books/luminous.py
  - keybindings/luminous
  - keybindings/shadower
  - routines/luminous/* (6 files)
```

### **Giải pháp:**

```bash
# 1. Commit trong submodule
cd resources
git add .
git commit -m "Add luminous custom files"
# → [main 4cda147] Add luminous custom files
# → 9 files changed, 595 insertions(+)

# 2. Commit submodule update ở main repo
cd ..
git add resources
git commit -m "Update resources submodule with luminous custom files"
# → [luminous-custom 2563361] Update resources submodule
# → 1 file changed, 1 insertion(+), 1 deletion(-)

✅ SUCCESS!
```

---

## 📁 **CHECK IF DIRECTORY IS SUBMODULE**

```bash
# Method 1: Check .git
ls -la resources/
# Nếu thấy `.git` directory → Submodule!

# Method 2: Check .gitmodules
cat .gitmodules
# Nếu có entry cho resources → Submodule!

# Method 3: Git status message
git status
# Nếu thấy "(untracked content)" hoặc "(new commits)"
# → Đó là submodule!
```

---

## 💾 **SAVE THIS WORKFLOW**

```bash
# Khi làm việc với resources/:

1. Edit files in resources/
2. cd resources
3. git add . && git commit -m "Update"
4. cd ..
5. git add resources && git commit -m "Update submodule"

DONE! ✅
```

---

**🎊 Giờ bạn đã biết cách xử lý Git submodules!** ✨
