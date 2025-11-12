# AUTO_MAPLE_LIGHT_BUILD - Giải thích và Tác động

## Tóm tắt

**`AUTO_MAPLE_LIGHT_BUILD=1` KHÔNG gây lỗi khi chạy bot** ✅

## Chi tiết

### 1. Mục đích
- `AUTO_MAPLE_LIGHT_BUILD=1` chỉ dùng trong quá trình **BUILD** (PyInstaller)
- Giúp build thành công trên VM khi TensorFlow gây lỗi trong quá trình build

### 2. Tác động khi BUILD
- Khi build với `AUTO_MAPLE_LIGHT_BUILD=1`:
  - PyInstaller sẽ **exclude** TensorFlow khỏi executable
  - Build sẽ thành công (không bị lỗi `ModuleNotFoundError: torch`)
  - Executable sẽ **không có** TensorFlow

### 3. Tác động khi RUNTIME

#### A. Chạy Executable (đã build với light build)
- TensorFlow **không có** trong executable
- `detection.tf = None`
- Bot vẫn chạy bình thường vì:
  - ✅ Rune solving đã **disabled** trong `bot.py` (`model = None`)
  - ✅ Không có code nào gọi `detection.load_model()` hoặc `detection.merge_detection()`
  - ✅ Tất cả tính năng khác hoạt động bình thường

#### B. Chạy Source Code (với AUTO_MAPLE_LIGHT_BUILD=1 trong .env)
- TensorFlow sẽ **không được import** (do logic check biến môi trường)
- `detection.tf = None`
- Bot vẫn chạy bình thường vì:
  - ✅ Rune solving đã **disabled**
  - ✅ Không có code nào gọi detection functions

#### C. Chạy Source Code (không có AUTO_MAPLE_LIGHT_BUILD trong .env)
- TensorFlow sẽ **được import** nếu có sẵn
- Bot chạy bình thường

### 4. Tính năng bị ảnh hưởng

**Rune Detection/Solver** (đã disabled):
- Tính năng tự động giải Rune mini-game
- **Đã bị disable** trong `bot.py` (line 106: `model = None`)
- Code gọi rune solving đã bị comment (line 180-182)
- **Không ảnh hưởng** vì tính năng này không được sử dụng

### 5. Tính năng KHÔNG bị ảnh hưởng

✅ Tất cả tính năng khác hoạt động bình thường:
- Bot routine execution
- Key remapping
- Arduino output
- VMware Receiver
- Anti-detection features
- GUI
- Tất cả tính năng khác

## Kết luận

**`AUTO_MAPLE_LIGHT_BUILD=1` KHÔNG gây lỗi khi chạy bot** vì:

1. ✅ Rune solving đã disabled sẵn
2. ✅ Không có code nào gọi detection functions
3. ✅ Tất cả tính năng khác không phụ thuộc TensorFlow
4. ✅ Code đã handle trường hợp `tf = None` an toàn

## Khuyến nghị

- **Build trên VM**: Dùng `AUTO_MAPLE_LIGHT_BUILD=1` trong `.env`
- **Build trên Host**: Không cần set (build full với TensorFlow)
- **Chạy bot**: Không cần quan tâm, bot sẽ chạy bình thường

