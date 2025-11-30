"""Phân tích chi tiết các frame Violetta để tìm pattern và đề xuất cải thiện."""

import cv2
import numpy as np
from pathlib import Path
import json
from collections import defaultdict
from typing import Dict, List, Tuple, Optional


def analyze_frame(frame_path: Path) -> Optional[Dict]:
    """Phân tích một frame và trả về các metrics."""
    img = cv2.imread(str(frame_path))
    if img is None:
        return None

    h, w = img.shape[:2]

    # Convert to different color spaces
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Basic stats
    stats = {
        "path": str(frame_path),
        "name": frame_path.name,
        "size": (w, h),
        "file_size_mb": frame_path.stat().st_size / (1024 * 1024),
    }

    # Color analysis
    stats["bgr_mean"] = img.mean(axis=(0, 1)).tolist()
    stats["bgr_std"] = img.std(axis=(0, 1)).tolist()
    stats["gray_mean"] = float(gray.mean())
    stats["gray_std"] = float(gray.std())

    # HSV analysis (useful for game UI detection)
    stats["hsv_mean"] = hsv.mean(axis=(0, 1)).tolist()
    stats["hsv_std"] = hsv.std(axis=(0, 1)).tolist()

    # Edge detection (to find UI elements)
    edges = cv2.Canny(gray, 50, 150)
    stats["edge_density"] = float((edges > 0).sum() / (w * h))

    # Histogram analysis
    hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
    hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
    hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])

    stats["hist_peaks_b"] = int(np.argmax(hist_b))
    stats["hist_peaks_g"] = int(np.argmax(hist_g))
    stats["hist_peaks_r"] = int(np.argmax(hist_r))

    # Detect if there's a game window (look for specific colors)
    # Violetta game typically has blue/purple UI
    hsv_mask = cv2.inRange(hsv, (100, 80, 70), (130, 255, 255))
    stats["violetta_color_ratio"] = float((hsv_mask > 0).sum() / (w * h))

    # Detect text regions (high contrast areas)
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    stats["text_region_ratio"] = float((binary > 127).sum() / (w * h))

    # Detect button-like regions (rectangular shapes)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    button_candidates = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if 500 < area < 50000:  # Reasonable button size
            x, y, w_cnt, h_cnt = cv2.boundingRect(cnt)
            aspect_ratio = w_cnt / h_cnt if h_cnt > 0 else 0
            if 0.5 < aspect_ratio < 2.0:  # Not too elongated
                button_candidates.append((x, y, w_cnt, h_cnt, area))

    stats["button_candidates"] = len(button_candidates)

    # Detect if frame shows specific game states
    # Look for common UI elements
    stats["has_high_contrast"] = stats["gray_std"] > 50
    stats["has_ui_elements"] = stats["edge_density"] > 0.1

    return stats


def detect_violetta_roi(frame: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    """Detect Violetta game window ROI."""
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Violetta game has blue/purple UI
    mask = cv2.inRange(hsv, (100, 80, 70), (130, 255, 255))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    # Find largest contour
    largest = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest)

    # Add padding
    padding = 20
    h_img, w_img = frame.shape[:2]
    x0 = max(0, x - padding)
    y0 = max(0, y - padding)
    x1 = min(w_img, x + w + padding)
    y1 = min(h_img, y + h + padding)

    return (x0, y0, x1 - x0, y1 - y0)


def classify_violetta_state(
    frame: np.ndarray, roi: Optional[Tuple[int, int, int, int]] = None
) -> str:
    """
    Phân loại trạng thái của Violetta game dựa trên visual features.
    Đây là heuristic-based classification để hiểu pattern.
    """
    if roi:
        x, y, w, h = roi
        roi_frame = frame[y : y + h, x : x + w]
    else:
        roi_frame = frame

    if roi_frame.size == 0:
        return "unknown"

    h, w = roi_frame.shape[:2]
    gray = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2GRAY)

    # Divide into 4 quadrants
    mid_x, mid_y = w // 2, h // 2

    top_left = gray[0:mid_y, 0:mid_x]
    top_right = gray[0:mid_y, mid_x:w]
    bottom_left = gray[mid_y:h, 0:mid_x]
    bottom_right = gray[mid_y:h, mid_x:w]

    # Calculate brightness/activity in each quadrant
    tl_brightness = top_left.mean()
    tr_brightness = top_right.mean()
    bl_brightness = bottom_left.mean()
    br_brightness = bottom_right.mean()

    # Detect which quadrant is most active (likely has button/indicator)
    quadrants = {
        "top_left": tl_brightness,
        "top_right": tr_brightness,
        "bottom_left": bl_brightness,
        "bottom_right": br_brightness,
    }

    # Find brightest quadrant (likely has active element)
    brightest = max(quadrants.items(), key=lambda x: x[1])

    # Check for specific patterns
    # Look for text/buttons (high contrast regions)
    edges = cv2.Canny(gray, 50, 150)
    edge_density = (edges > 0).sum() / (w * h)

    if edge_density < 0.05:
        return "wait"  # Static screen, waiting

    # Check if there's a success indicator (usually bright/green)
    hsv = cv2.cvtColor(roi_frame, cv2.COLOR_BGR2HSV)
    green_mask = cv2.inRange(hsv, (40, 50, 50), (80, 255, 255))
    green_ratio = (green_mask > 0).sum() / (w * h)

    if green_ratio > 0.1:
        return "success"

    # Classify based on active quadrant
    if brightest[0] == "top_left":
        return "click_top_left"
    elif brightest[0] == "top_right":
        return "click_top_right"
    elif brightest[0] == "bottom_left":
        return "click_bottom_left"
    elif brightest[0] == "bottom_right":
        return "click_bottom_right"

    return "wait"


def analyze_frames_directory(frames_dir: Path) -> Optional[Dict]:
    """Phân tích tất cả frames trong một thư mục."""
    print(f"\n{'='*60}")
    print(f"Phan tich thu muc: {frames_dir}")
    print(f"{'='*60}")

    frame_files = sorted(frames_dir.glob("*.png"))
    if not frame_files:
        print(f"Khong tim thay frame nao trong {frames_dir}")
        return None

    print(f"Tim thay {len(frame_files)} frames")

    all_stats = []
    state_distribution = defaultdict(int)
    roi_detections = []

    for i, frame_path in enumerate(frame_files):
        print(
            f"  Dang phan tich {frame_path.name}... ({i+1}/{len(frame_files)})",
            end="\r",
        )

        stats = analyze_frame(frame_path)
        if stats is None:
            continue

        all_stats.append(stats)

        # Load frame for ROI detection and classification
        frame = cv2.imread(str(frame_path))
        if frame is not None:
            roi = detect_violetta_roi(frame)
            if roi:
                roi_detections.append(roi)
                state = classify_violetta_state(frame, roi)
                state_distribution[state] += 1
                stats["detected_state"] = state
                stats["roi"] = roi
            else:
                # Try without ROI
                state = classify_violetta_state(frame)
                state_distribution[state] += 1
                stats["detected_state"] = state

    print(f"\n  Hoan thanh phan tich {len(all_stats)} frames")

    # Aggregate statistics
    if not all_stats:
        return None

    summary = {
        "directory": str(frames_dir),
        "total_frames": len(all_stats),
        "state_distribution": dict(state_distribution),
        "avg_file_size_mb": np.mean([s["file_size_mb"] for s in all_stats]),
        "size_consistency": {
            "widths": [s["size"][0] for s in all_stats],
            "heights": [s["size"][1] for s in all_stats],
        },
        "color_stats": {
            "avg_bgr_mean": np.mean(
                [s["bgr_mean"] for s in all_stats], axis=0
            ).tolist(),
            "avg_gray_mean": np.mean([s["gray_mean"] for s in all_stats]),
            "avg_edge_density": np.mean([s["edge_density"] for s in all_stats]),
        },
        "roi_detection_rate": len(roi_detections) / len(all_stats) if all_stats else 0,
        "frames_with_ui": sum(1 for s in all_stats if s.get("has_ui_elements", False)),
        "frames_with_high_contrast": sum(
            1 for s in all_stats if s.get("has_high_contrast", False)
        ),
    }

    return {
        "summary": summary,
        "detailed_stats": all_stats[:10],  # Only keep first 10 for report size
    }


def compare_directories(dir1_analysis: Dict, dir2_analysis: Dict) -> Optional[Dict]:
    """So sánh phân tích giữa 2 thư mục."""
    if dir1_analysis is None or dir2_analysis is None:
        return None

    s1 = dir1_analysis["summary"]
    s2 = dir2_analysis["summary"]

    comparison = {
        "frame_count_diff": s2["total_frames"] - s1["total_frames"],
        "file_size_diff_mb": s2["avg_file_size_mb"] - s1["avg_file_size_mb"],
        "size_consistency": {
            "dir1": {
                "width_range": (
                    min(s1["size_consistency"]["widths"]),
                    max(s1["size_consistency"]["widths"]),
                ),
                "height_range": (
                    min(s1["size_consistency"]["heights"]),
                    max(s1["size_consistency"]["heights"]),
                ),
            },
            "dir2": {
                "width_range": (
                    min(s2["size_consistency"]["widths"]),
                    max(s2["size_consistency"]["widths"]),
                ),
                "height_range": (
                    min(s2["size_consistency"]["heights"]),
                    max(s2["size_consistency"]["heights"]),
                ),
            },
        },
        "color_difference": {
            "bgr_mean_diff": (
                np.array(s2["color_stats"]["avg_bgr_mean"])
                - np.array(s1["color_stats"]["avg_bgr_mean"])
            ).tolist(),
            "gray_mean_diff": s2["color_stats"]["avg_gray_mean"]
            - s1["color_stats"]["avg_gray_mean"],
        },
        "state_distribution": {
            "dir1": s1["state_distribution"],
            "dir2": s2["state_distribution"],
        },
        "roi_detection": {
            "dir1_rate": s1["roi_detection_rate"],
            "dir2_rate": s2["roi_detection_rate"],
        },
    }

    return comparison


def generate_recommendations(
    analysis: Dict, comparison: Optional[Dict] = None
) -> List[str]:
    """Tạo các đề xuất cải thiện dựa trên phân tích."""
    recommendations = []

    if analysis is None:
        return recommendations

    summary = analysis["summary"]

    # 1. ROI Detection
    if summary["roi_detection_rate"] < 0.8:
        recommendations.append(
            f"⚠️ ROI Detection Rate thấp ({summary['roi_detection_rate']*100:.1f}%). "
            f"Cải thiện: Điều chỉnh HSV color range trong detect_violetta_roi() hoặc "
            f"sử dụng template matching với violetta_game.png"
        )

    # 2. State Distribution
    state_dist = summary["state_distribution"]
    if len(state_dist) < 3:
        recommendations.append(
            f"⚠️ Chỉ phát hiện {len(state_dist)} states khác nhau. "
            f"Cần đảm bảo dataset có đủ diversity: {list(state_dist.keys())}"
        )

    # 3. File Size
    if summary["avg_file_size_mb"] > 3.0:
        recommendations.append(
            f"⚠️ File size lớn ({summary['avg_file_size_mb']:.2f}MB/frame). "
            f"Cân nhắc: Giảm resolution hoặc compression khi extract frames"
        )

    # 4. Size Consistency
    widths = summary["size_consistency"]["widths"]
    heights = summary["size_consistency"]["heights"]
    if len(set(widths)) > 1 or len(set(heights)) > 1:
        recommendations.append(
            f"⚠️ Kích thước frame không nhất quán. "
            f"Width: {min(widths)}-{max(widths)}, Height: {min(heights)}-{max(heights)}. "
            f"Cần normalize về cùng resolution trước khi train"
        )

    # 5. UI Elements Detection
    ui_rate = summary["frames_with_ui"] / summary["total_frames"]
    if ui_rate < 0.5:
        recommendations.append(
            f"⚠️ Chỉ {ui_rate*100:.1f}% frames có UI elements. "
            f"Có thể frames không chứa game window hoặc cần cải thiện detection"
        )

    # 6. Model Recommendations
    if comparison:
        comp = comparison
        if comp["roi_detection"]["dir2_rate"] > comp["roi_detection"]["dir1_rate"]:
            recommendations.append(
                f"✅ Dir2 có ROI detection tốt hơn ({comp['roi_detection']['dir2_rate']*100:.1f}% vs "
                f"{comp['roi_detection']['dir1_rate']*100:.1f}%). Có thể do time range khác nhau"
            )

    # 7. Data Augmentation
    recommendations.append(
        "💡 Data Augmentation: Áp dụng rotation (±5°), brightness (±20%), "
        "contrast (±15%), và slight translation để tăng dataset diversity"
    )

    # 8. Model Architecture
    num_classes = len(summary["state_distribution"])
    if num_classes <= 6:
        recommendations.append(
            f"✅ {num_classes} classes phù hợp với EfficientNet-B1 hoặc MobileNetV3. "
            f"Không cần model quá lớn"
        )

    return recommendations


def main():
    """Main function để chạy phân tích."""
    import sys
    import io

    # Fix encoding for Windows
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(
            sys.stdout.buffer, encoding="utf-8", errors="replace"
        )
        sys.stderr = io.TextIOWrapper(
            sys.stderr.buffer, encoding="utf-8", errors="replace"
        )

    project_root = Path(__file__).parent.parent.parent
    logs_dir = project_root / "logs"

    dir1 = logs_dir / "violetta_frames"
    dir2 = logs_dir / "violetta_frames2"

    print("=" * 60)
    print("PHAN TICH CHI TIET VIOLETTA FRAMES")
    print("=" * 60)

    # Analyze both directories
    analysis1 = analyze_frames_directory(dir1)
    analysis2 = analyze_frames_directory(dir2)

    # Compare
    comparison = None
    if analysis1 and analysis2:
        comparison = compare_directories(analysis1, analysis2)

    # Generate report
    print("\n" + "=" * 60)
    print("BAO CAO PHAN TICH")
    print("=" * 60)

    if analysis1:
        print("\n[VIOLETTA_FRAMES]")
        s1 = analysis1["summary"]
        print(f"  - Tong frames: {s1['total_frames']}")
        print(f"  - Avg file size: {s1['avg_file_size_mb']:.2f} MB")
        print(f"  - ROI detection rate: {s1['roi_detection_rate']*100:.1f}%")
        print(f"  - State distribution: {s1['state_distribution']}")
        print(f"  - Frames with UI: {s1['frames_with_ui']}/{s1['total_frames']}")
        print(f"  - Edge density: {s1['color_stats']['avg_edge_density']:.4f}")

    if analysis2:
        print("\n[VIOLETTA_FRAMES2]")
        s2 = analysis2["summary"]
        print(f"  - Tong frames: {s2['total_frames']}")
        print(f"  - Avg file size: {s2['avg_file_size_mb']:.2f} MB")
        print(f"  - ROI detection rate: {s2['roi_detection_rate']*100:.1f}%")
        print(f"  - State distribution: {s2['state_distribution']}")
        print(f"  - Frames with UI: {s2['frames_with_ui']}/{s2['total_frames']}")
        print(f"  - Edge density: {s2['color_stats']['avg_edge_density']:.4f}")

    if comparison:
        print("\n[SO SANH]")
        print(f"  - Frame count diff: {comparison['frame_count_diff']}")
        print(f"  - File size diff: {comparison['file_size_diff_mb']:.2f} MB")
        print(
            f"  - ROI detection: Dir1={comparison['roi_detection']['dir1_rate']*100:.1f}%, "
            f"Dir2={comparison['roi_detection']['dir2_rate']*100:.1f}%"
        )
        print(
            f"  - Gray mean diff: {comparison['color_difference']['gray_mean_diff']:.2f}"
        )

    # Recommendations
    print("\n" + "=" * 60)
    print("DE XUAT CAI THIEN")
    print("=" * 60)

    recommendations = []
    if analysis1:
        recommendations.extend(generate_recommendations(analysis1, comparison))
    if analysis2:
        recommendations.extend(generate_recommendations(analysis2, comparison))

    for i, rec in enumerate(set(recommendations), 1):
        print(f"\n{i}. {rec}")

    # Save detailed report
    report = {
        "analysis1": analysis1,
        "analysis2": analysis2,
        "comparison": comparison,
        "recommendations": list(set(recommendations)),
    }

    report_path = logs_dir / "violetta_analysis_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False, default=str)

    print(f"\n[OK] Da luu bao cao chi tiet: {report_path}")

    return report


if __name__ == "__main__":
    main()
