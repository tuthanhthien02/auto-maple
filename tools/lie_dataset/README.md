# Lie Detector Dataset Tools

Tools để thu thập và xử lý dataset cho AI solvers (Puzzle và Violetta).

## Workflow

1. **Record videos** → Đặt vào `recordings/puzzle/` hoặc `recordings/violetta/`
2. **Extract frames** → Chạy `process_all.py`
3. **Label** → Sử dụng GUI tools để label bounding boxes:
   - Puzzle: `python tools/lie_dataset/label_puzzle_yolo.py`
   - Violetta: `python tools/lie_dataset/label_violetta_yolo.py`
4. **Train** → Chạy `train_auto.py`

## Sử dụng process_all.py

### Xử lý tất cả videos

```bash
# Xử lý tất cả videos trong thư mục
python tools/lie_dataset/process_all.py --type violetta
```

### Xử lý 1 video cụ thể

```bash
# Xử lý 1 video với time range
python tools/lie_dataset/process_all.py --type violetta --video violetta_001.mp4 --start-time 5.0 --duration 20.0

# Xử lý toàn bộ video
python tools/lie_dataset/process_all.py --type violetta --video violetta_001.mp4
```

### Sử dụng file config

#### Violetta

Tạo file `recordings/violetta/video_config.json`:

```json
{
  "violetta_001.mp4": {
    "start_time": 5.0,
    "duration": 20.0
  },
  "violetta_002.mp4": {
    "start_time": 0.0,
    "duration": 15.0
  },
  "violetta_003.mp4": {
    "start_time": null,
    "duration": null
  }
}
```

#### Puzzle

Tạo file `recordings/puzzle/video_config.json`:

```json
{
  "puzzle_001.mp4": {
    "start_time": 0.0,
    "duration": null,
    "comment": "Extract entire video"
  },
  "puzzle_002.mp4": {
    "start_time": 10.0,
    "duration": 30.0,
    "comment": "Extract from 10s to 40s"
  }
}
```

#### Sử dụng config

```bash
# Tự động đọc config từ recordings/{type}/video_config.json
python tools/lie_dataset/process_all.py --type violetta --video violetta_001.mp4
python tools/lie_dataset/process_all.py --type puzzle --video puzzle_001.mp4

# Hoặc chỉ định config file khác
python tools/lie_dataset/process_all.py --type violetta --video violetta_001.mp4 --config path/to/config.json
python tools/lie_dataset/process_all.py --type puzzle --video puzzle_001.mp4 --config path/to/config.json
```

### Tham số

- `--type`: `puzzle` hoặc `violetta` (bắt buộc)
- `--input`: Thư mục chứa videos (default: `recordings`)
- `--output`: Thư mục output (default: `ai/lie_detector`)
- `--fps`: Frames per second để extract (default: 1.0)
- `--video`: Video cụ thể để xử lý (default: tất cả)
- `--start-time`: Thời gian bắt đầu (giây)
- `--duration`: Thời lượng extract (giây)
- `--config`: Đường dẫn đến file config JSON
- `--config-only`: Chỉ xử lý videos có trong config file (bỏ qua videos khác)

### Ưu tiên tham số

1. Command line args (`--start-time`, `--duration`) - ưu tiên cao nhất
2. Config file - nếu không có command line args
3. Toàn bộ video - nếu không có cả hai

## Ví dụ

```bash
# Ví dụ 1: Xử lý 1 video với time range từ command line
python tools/lie_dataset/process_all.py --type violetta --video violetta_001.mp4 --start-time 5.0 --duration 20.0

# Ví dụ 2: Xử lý 1 video với config file
python tools/lie_dataset/process_all.py --type violetta --video violetta_001.mp4

# Ví dụ 3: Xử lý tất cả videos (mỗi video 1 lần nếu có config)
python tools/lie_dataset/process_all.py --type violetta

# Ví dụ 4: Chỉ xử lý videos có trong config (bỏ qua videos khác)
python tools/lie_dataset/process_all.py --type violetta --config-only

# Ví dụ 5: Puzzle với time range
python tools/lie_dataset/process_all.py --type puzzle --video puzzle_001.mp4 --start-time 10.0 --duration 30.0
```

## Labeling với GUI Tools

### Puzzle Labeling

```bash
# Mở GUI tool để label Puzzle frames
python tools/lie_dataset/label_puzzle_yolo.py
```

**Hướng dẫn:**
1. Click "Select Frames Directory" → Chọn thư mục `ai/lie_detector/puzzle/dataset/raw_frames/puzzle_001/`
2. Click và drag để vẽ bounding box xung quanh green circular target
3. Nhấn `S` hoặc click "Save Label" để lưu
4. Dùng `Space` hoặc `→` để chuyển frame tiếp theo
5. Dùng `Backspace` hoặc `←` để quay lại frame trước

**Hotkeys:**
- `Space` / `→`: Next frame
- `Backspace` / `←`: Previous frame
- `S`: Save label
- `D`: Delete label
- `C`: Clear box
- `K`: Skip frame
- `Esc`: Clear box

### Violetta Labeling

```bash
# Mở GUI tool để label Violetta frames
python tools/lie_dataset/label_violetta_yolo.py
```

**Hướng dẫn tương tự Puzzle**, nhưng label Violetta có make-up (chỉ label Violetta ĐÚNG cần click).

