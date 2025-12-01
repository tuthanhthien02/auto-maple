"""Main tool to process videos: extract frames, detect ROI, and auto-label."""

import os
import sys
import argparse
from pathlib import Path
import cv2
import numpy as np

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.modules.notifier import get_asset_path  # noqa: E402
from src.common.utils import multi_match_multi_scale  # noqa: E402
from tools.lie_dataset.extract_frames import extract_frames_from_video  # noqa: E402
from tools.lie_dataset.auto_label_puzzle import auto_label_puzzle_frame  # noqa: E402


def get_template_path(template_name: str) -> str:
    """Get path to template image."""
    # Note: violetta now uses multi-template matching from violetta-matching folder
    if template_name == "violetta":
        # This is kept for backward compatibility but not used
        return get_asset_path("assets/lie-detector/violetta_game.png")
    return get_asset_path(f"assets/lie-detector/{template_name}_crop.png")


def get_violetta_templates():
    """
    Load all templates from violetta-matching folder.

    Returns:
        dict with keys: 'top_left', 'bottom_right'
        Each contains list of (template, name) tuples
    """
    templates = {"top_left": [], "bottom_right": []}

    matching_dir = get_asset_path("assets/lie-detector/violetta-matching")

    if not os.path.exists(matching_dir):
        print(f"Warning: Violetta templates directory not found: {matching_dir}")
        return templates

    # Load top-left templates (violetta_top-left-*.png)
    for i in range(1, 10):  # Check up to 9 templates
        template_path = os.path.join(matching_dir, f"violetta_top-left-{i}.png")
        if os.path.exists(template_path):
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is not None:
                templates["top_left"].append((template, f"top-left-{i}"))

    # Load bottom-right templates (violetta_bottom-righ-*t.png)
    for i in range(1, 10):  # Check up to 9 templates
        # Try both naming patterns
        for pattern in [
            f"violetta_bottom-righ-{i}t.png",
            f"violetta_bottom-right-{i}t.png",
        ]:
            template_path = os.path.join(matching_dir, pattern)
            if os.path.exists(template_path):
                template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
                if template is not None:
                    templates["bottom_right"].append((template, f"bottom-right-{i}"))
                    break  # Found, don't try other pattern

    # Log loaded templates
    if templates["top_left"] or templates["bottom_right"]:
        print(
            f"  Loaded {len(templates['top_left'])} top-left templates, {len(templates['bottom_right'])} bottom-right templates"
        )
    else:
        print(f"  Warning: No templates loaded from {matching_dir}")

    return templates


def get_puzzle_templates():
    """
    Load all templates from puzzle-matching folder.

    Returns:
        dict with keys: 'top_left', 'bottom_right'
        Each contains list of (template, name) tuples
    """
    templates = {"top_left": [], "bottom_right": []}

    matching_dir = get_asset_path("assets/lie-detector/puzzle-matching")

    if not os.path.exists(matching_dir):
        print(f"Warning: Puzzle templates directory not found: {matching_dir}")
        return templates

    # Load top-left templates (puzzle_top-left-*.png)
    for i in range(1, 10):  # Check up to 9 templates
        template_path = os.path.join(matching_dir, f"puzzle_top-left-{i}.png")
        if os.path.exists(template_path):
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is not None:
                templates["top_left"].append((template, f"top-left-{i}"))

    # Load bottom-right templates (puzzle_bottom-right-*.png)
    for i in range(1, 10):  # Check up to 9 templates
        template_path = os.path.join(matching_dir, f"puzzle_bottom-right-{i}.png")
        if os.path.exists(template_path):
            template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
            if template is not None:
                templates["bottom_right"].append((template, f"bottom-right-{i}"))

    # Log loaded templates
    if templates["top_left"] or templates["bottom_right"]:
        print(
            f"  Loaded {len(templates['top_left'])} top-left templates, {len(templates['bottom_right'])} bottom-right templates"
        )
    else:
        print(f"  Warning: No templates loaded from {matching_dir}")

    return templates


def match_multiple_templates(frame_gray, templates, threshold=0.75, debug=False):
    """
    Match multiple templates and return best match.

    Args:
        frame_gray: Grayscale frame
        templates: List of (template, name) tuples
        threshold: Minimum match score
        debug: Enable debug logging

    Returns:
        (x, y, w, h, score, name) of best match, or None
    """
    best_match = None
    best_score = 0
    all_scores = []

    for template, name in templates:
        matches = multi_match_multi_scale(
            frame_gray,
            template,
            threshold=threshold,
            is_gray=True,
            scales=[0.75, 0.85, 0.95, 1.0, 1.1, 1.2, 1.3],
        )

        if matches:
            # Get best match from this template
            x, y, score = matches[0]
            h, w = template.shape
            all_scores.append((name, score))

            # Update best match if score is higher
            if score > best_score:
                best_score = score
                best_match = (x, y, w, h, score, name)
        elif debug:
            # Try with lower threshold to see what scores we get
            matches_low = multi_match_multi_scale(
                frame_gray,
                template,
                threshold=0.5,  # Very low threshold just to see scores
                is_gray=True,
                scales=[0.75, 0.85, 0.95, 1.0, 1.1, 1.2, 1.3],
            )
            if matches_low:
                x, y, score = matches_low[0]
                all_scores.append((name, f"{score:.3f} (below threshold {threshold})"))

    if debug and all_scores:
        print(f"      Template scores: {all_scores}")
        if best_match:
            print(f"      Best match: {best_match[5]} with score {best_match[4]:.3f}")

    return best_match


def detect_puzzle_window(frame: np.ndarray, debug=False) -> tuple:
    """
    Detect puzzle window in frame using multi-template matching:
    - Multiple top-left templates
    - Multiple bottom-right templates

    Args:
        frame: Input frame
        debug: Enable debug logging

    Returns:
        (x, y, w, h) if found, None otherwise
    """
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    templates = get_puzzle_templates()

    if debug:
        print(
            f"    Debug: Loaded {len(templates['top_left'])} top-left, {len(templates['bottom_right'])} bottom-right templates"
        )

    # Thresholds for puzzle matching
    top_threshold = 0.65
    bottom_threshold = 0.60

    # Match top-left templates
    top_match = None
    if templates["top_left"]:
        if debug:
            print(
                f"    Debug: Matching {len(templates['top_left'])} top-left templates (threshold={top_threshold})..."
            )
        top_match = match_multiple_templates(
            frame_gray, templates["top_left"], threshold=top_threshold, debug=debug
        )

    # Match bottom-right templates
    bottom_match = None
    if templates["bottom_right"]:
        if debug:
            print(
                f"    Debug: Matching {len(templates['bottom_right'])} bottom-right templates (threshold={bottom_threshold})..."
            )
        bottom_match = match_multiple_templates(
            frame_gray,
            templates["bottom_right"],
            threshold=bottom_threshold,
            debug=debug,
        )

    if debug:
        print(
            f"    Debug: Top match: {top_match is not None}, Bottom match: {bottom_match is not None}"
        )

    # Case 1: Both top and bottom matched → Calculate ROI accurately
    if top_match and bottom_match:
        tx, ty, tw, th, t_score, t_name = top_match
        bx, by, bw, bh, b_score, b_name = bottom_match

        if debug:
            print(
                f"    Debug: Top at ({tx}, {ty}) size ({tw}, {th}) score {t_score:.3f}"
            )
            print(
                f"    Debug: Bottom at ({bx}, {by}) size ({bw}, {bh}) score {b_score:.3f}"
            )

        # Verify: Top must be above bottom
        if ty < by:
            # Calculate ROI from both
            # Top-left template marks the top-left corner, bottom-right marks the bottom-right corner
            # Add padding to left and top to avoid cutting off edges
            # Use larger padding to ensure we capture the full window (template may not be at exact corner)
            roi_x = max(
                0, tx - 50
            )  # Start from top-left template x with left padding (50px)
            roi_y = max(
                0, ty - 20
            )  # Start from top-left template y with top padding (20px)
            # Bottom-right template's right edge (bx + bw) is the right edge of window
            # Recalculate width and height from the new roi_x and roi_y
            roi_w = (bx + bw) - roi_x  # Width from new roi_x to bottom-right edge
            roi_h = (by + bh) - roi_y  # Height from new roi_y to bottom-right edge

            if debug:
                print(
                    f"    Debug: Calculated ROI: ({roi_x}, {roi_y}, {roi_w}, {roi_h})"
                )
                print(f"    Debug: Frame size: {frame.shape[1]}x{frame.shape[0]}")

            # Verification
            if (
                roi_w > 300
                and roi_h > 300
                and roi_w < frame.shape[1]
                and roi_h < frame.shape[0]
            ):
                if debug:
                    print("    Debug: ROI accepted (both matched)")
                return (roi_x, roi_y, roi_w, roi_h)
            elif debug:
                print(
                    f"    Debug: ROI verification failed: w={roi_w} (min 300), h={roi_h} (min 300)"
                )
        elif debug:
            print(f"    Debug: Top not above bottom: ty={ty} >= by={by}")

    # Case 2: Only top matched → Estimate ROI
    if top_match:
        tx, ty, tw, th, t_score, t_name = top_match
        roi_x = max(0, tx - 50)  # Start from top-left template with left padding (50px)
        roi_y = max(0, ty - 20)  # Start from top-left template with top padding (20px)
        # Estimate: puzzle window is typically around 600-700px wide
        # Use template width as reference, estimate window is ~3-4x template width
        estimated_window_width = tw * 3.5
        roi_w = min(frame.shape[1] - roi_x, int(estimated_window_width))
        roi_h = min(frame.shape[0] - roi_y, 600)  # Estimate height

        if debug:
            print(f"    Debug: Top-only ROI: ({roi_x}, {roi_y}, {roi_w}, {roi_h})")

        # Verification
        if roi_w > 300 and roi_h > 300:
            if debug:
                print("    Debug: ROI accepted (top-only)")
            return (roi_x, roi_y, roi_w, roi_h)
        elif debug:
            print(f"    Debug: Top-only ROI verification failed: w={roi_w}, h={roi_h}")

    # Case 3: Only bottom matched → Estimate ROI
    if bottom_match:
        bx, by, bw, bh, b_score, b_name = bottom_match
        # Bottom-right template marks the bottom-right corner
        # Estimate top-left position (puzzle window is typically ~600px tall)
        estimated_window_height = 600
        estimated_window_width = bw * 3.5
        roi_x = max(
            0, (bx + bw) - int(estimated_window_width) - 30
        )  # Estimate left edge with padding
        roi_y = max(
            0, (by + bh) - estimated_window_height - 15
        )  # Estimate top edge with padding
        roi_w = (bx + bw) - roi_x  # Width to bottom-right edge
        roi_h = (by + bh) - roi_y  # Height to bottom-right edge

        if debug:
            print(f"    Debug: Bottom-only ROI: ({roi_x}, {roi_y}, {roi_w}, {roi_h})")

        # Verification
        if roi_w > 300 and roi_h > 300:
            if debug:
                print("    Debug: ROI accepted (bottom-only)")
            return (roi_x, roi_y, roi_w, roi_h)
        elif debug:
            print(
                f"    Debug: Bottom-only ROI verification failed: w={roi_w}, h={roi_h}"
            )

    if debug:
        print("    Debug: No valid ROI found")

        return None


def detect_violet_window(frame: np.ndarray, debug=False) -> tuple:
    """
    Detect violet game window using multi-template matching:
    - Multiple top-left templates (banner)
    - Multiple bottom-right templates (buttons)

    Args:
        frame: Input frame
        debug: Enable debug logging

    Returns:
        (x, y, w, h) if found, None otherwise
    """
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    templates = get_violetta_templates()

    if debug:
        print(
            f"    Debug: Loaded {len(templates['top_left'])} top-left, {len(templates['bottom_right'])} bottom-right templates"
        )

    # Lower thresholds for better detection
    top_threshold = 0.65  # Reduced from 0.75
    bottom_threshold = 0.60  # Reduced from 0.70

    # Match top-left templates (banner)
    top_match = None
    if templates["top_left"]:
        if debug:
            print(
                f"    Debug: Matching {len(templates['top_left'])} top-left templates (threshold={top_threshold})..."
            )
        top_match = match_multiple_templates(
            frame_gray, templates["top_left"], threshold=top_threshold, debug=debug
        )

    # Match bottom-right templates (buttons)
    bottom_match = None
    if templates["bottom_right"]:
        if debug:
            print(
                f"    Debug: Matching {len(templates['bottom_right'])} bottom-right templates (threshold={bottom_threshold})..."
            )
        bottom_match = match_multiple_templates(
            frame_gray,
            templates["bottom_right"],
            threshold=bottom_threshold,
            debug=debug,
        )

    if debug:
        print(
            f"    Debug: Top match: {top_match is not None}, Bottom match: {bottom_match is not None}"
        )

    # Case 1: Both top and bottom matched → Calculate ROI accurately
    if top_match and bottom_match:
        tx, ty, tw, th, t_score, t_name = top_match
        bx, by, bw, bh, b_score, b_name = bottom_match

        if debug:
            print(
                f"    Debug: Top at ({tx}, {ty}) size ({tw}, {th}) score {t_score:.3f}"
            )
            print(
                f"    Debug: Bottom at ({bx}, {by}) size ({bw}, {bh}) score {b_score:.3f}"
            )

        # Verify: Top must be above bottom
        if ty < by:
            # Calculate ROI from both
            roi_x = min(tx, bx) - 20
            roi_y = max(0, ty - 10)
            roi_w = max(tx + tw, bx + bw) - roi_x + 20
            roi_h = (by + bh) - roi_y + 20

            if debug:
                print(
                    f"    Debug: Calculated ROI: ({roi_x}, {roi_y}, {roi_w}, {roi_h})"
                )
                print(f"    Debug: Frame size: {frame.shape[1]}x{frame.shape[0]}")

            # Relaxed verification (reduced from 400 to 300)
            if (
                roi_w > 300
                and roi_h > 300
                and roi_w < frame.shape[1]
                and roi_h < frame.shape[0]
            ):
                if debug:
                    print("    Debug: ROI accepted (both matched)")
                return (roi_x, roi_y, roi_w, roi_h)
            elif debug:
                print(
                    f"    Debug: ROI verification failed: w={roi_w} (min 300), h={roi_h} (min 300)"
                )
        elif debug:
            print(f"    Debug: Top not above bottom: ty={ty} >= by={by}")

    # Case 2: Only top matched → Estimate ROI
    if top_match:
        tx, ty, tw, th, t_score, t_name = top_match
        roi_x = max(0, tx - 20)
        roi_y = max(0, ty - 10)
        roi_w = min(frame.shape[1] - roi_x, tw + 40)
        roi_h = min(frame.shape[0] - roi_y, 600)  # Estimate height

        if debug:
            print(f"    Debug: Top-only ROI: ({roi_x}, {roi_y}, {roi_w}, {roi_h})")

        # Relaxed verification
        if roi_w > 300 and roi_h > 300:
            if debug:
                print("    Debug: ROI accepted (top-only)")
            return (roi_x, roi_y, roi_w, roi_h)
        elif debug:
            print(f"    Debug: Top-only ROI verification failed: w={roi_w}, h={roi_h}")

    # Case 3: Only bottom matched → Estimate ROI
    if bottom_match:
        bx, by, bw, bh, b_score, b_name = bottom_match
        roi_x = max(0, bx - 20)
        roi_y = max(0, by - 500)  # Estimate: buttons + characters + banner
        roi_w = min(frame.shape[1] - roi_x, bw + 40)
        roi_h = min(frame.shape[0] - roi_y, 600)  # Estimate height

        if debug:
            print(f"    Debug: Bottom-only ROI: ({roi_x}, {roi_y}, {roi_w}, {roi_h})")

        # Relaxed verification
        if roi_w > 300 and roi_h > 300:
            if debug:
                print("    Debug: ROI accepted (bottom-only)")
            return (roi_x, roi_y, roi_w, roi_h)
        elif debug:
            print(
                f"    Debug: Bottom-only ROI verification failed: w={roi_w}, h={roi_h}"
            )

    if debug:
        print("    Debug: No ROI detected")

        # No match found
        return None


def crop_roi(frame: np.ndarray, window_bbox: tuple, padding: int = 0) -> np.ndarray:
    """Crop ROI from frame with optional padding."""
    x, y, w, h = window_bbox
    height, width = frame.shape[:2]

    # Add minimal padding if needed (default 0 for puzzle since ROI is already calculated precisely)
    x0 = max(0, x - padding)
    y0 = max(0, y - padding)
    x1 = min(width, x + w + padding)
    y1 = min(height, y + h + padding)

    return frame[y0:y1, x0:x1]


def process_video(
    video_path: str,
    output_base_dir: str,
    puzzle_type: str,  # "puzzle" or "violetta"
    fps: float = 1.0,
    start_time: float = None,
    duration: float = None,
    debug: bool = False,
):
    """
    Process a single video: extract frames, detect ROI, crop, and organize.

    Args:
        video_path: Path to input video
        output_base_dir: Base directory for output dataset
        puzzle_type: "puzzle" or "violetta"
        fps: Frames per second to extract
        start_time: Start time in seconds (None = from beginning)
        duration: Duration in seconds (None = to end)
    """
    video_name = Path(video_path).stem

    # Create temp directory for extracted frames
    temp_dir = os.path.join(output_base_dir, "temp", video_name)
    os.makedirs(temp_dir, exist_ok=True)

    print(f"Processing {video_path}...")
    if start_time is not None or duration is not None:
        time_info = []
        if start_time is not None:
            time_info.append(f"from {start_time}s")
        if duration is not None:
            time_info.append(f"for {duration}s")
        print(f"  Time range: {' '.join(time_info)}")
    print(f"  Extracting frames at {fps} fps...")

    # Extract frames
    frame_files = extract_frames_from_video(
        video_path,
        temp_dir,
        fps=fps,
        prefix=video_name,
        start_time=start_time,
        duration=duration,
    )

    if not frame_files:
        print(f"  Warning: No frames extracted from {video_path}")
        return

    print(f"  Extracted {len(frame_files)} frames")

    # Detect window and process frames
    detected_count = 0
    processed_frames = []

    for frame_file in frame_files:
        frame = cv2.imread(frame_file)
        if frame is None:
            continue

        # Detect window
        if puzzle_type == "puzzle":
            window_bbox = detect_puzzle_window(frame, debug=debug)
        elif puzzle_type == "violetta":
            if debug and detected_count < 3:  # Debug first 3 frames only
                print(
                    f"    Processing frame {detected_count + 1}: {Path(frame_file).name}"
                )
            window_bbox = detect_violet_window(
                frame, debug=debug and detected_count < 3
            )
        else:
            print(f"  Error: Unknown puzzle type: {puzzle_type}")
            return

        if window_bbox is None:
            if debug and detected_count < 3:
                print(f"    Frame {detected_count + 1}: No ROI detected")
            continue

        # Crop ROI
        # Puzzle: no padding (ROI is calculated precisely from templates)
        # Violetta: small padding for safety
        padding = 5 if puzzle_type == "violetta" else 0
        roi = crop_roi(frame, window_bbox, padding=padding)

        # Save processed frame
        output_dir = os.path.join(
            output_base_dir, puzzle_type, "dataset", "raw_frames", video_name
        )
        os.makedirs(output_dir, exist_ok=True)

        frame_name = Path(frame_file).name
        output_path = os.path.join(output_dir, frame_name)
        cv2.imwrite(output_path, roi)

        processed_frames.append(
            {
                "frame_path": output_path,
                "original_frame": frame_file,
                "window_bbox": window_bbox,
            }
        )

        detected_count += 1

    print(f"  Detected window in {detected_count}/{len(frame_files)} frames")

    # Auto-label for puzzle
    if puzzle_type == "puzzle" and processed_frames:
        print(f"  Auto-labeling {len(processed_frames)} frames...")
        labels_dir = os.path.join(
            output_base_dir, puzzle_type, "dataset", "labels", video_name
        )
        os.makedirs(labels_dir, exist_ok=True)

        labeled_count = 0
        for frame_info in processed_frames:
            roi = cv2.imread(frame_info["frame_path"])
            if roi is None:
                continue

            annotation = auto_label_puzzle_frame(roi)
            if annotation:
                # Save YOLO format annotation
                frame_name = Path(frame_info["frame_path"]).stem
                label_path = os.path.join(labels_dir, f"{frame_name}.txt")
                with open(label_path, "w") as f:
                    f.write(annotation)
                labeled_count += 1

        print(f"  Labeled {labeled_count}/{len(processed_frames)} frames")

    # For violetta, frames are ready for manual labeling
    if puzzle_type == "violetta":
        print(f"  {len(processed_frames)} frames ready for labeling")
        print("  Run: python tools/lie_dataset/label_violetta_gui.py")

    return processed_frames


def load_video_config(config_path: str) -> dict:
    """
    Load video configuration from JSON file.

    Args:
        config_path: Path to config JSON file

    Returns:
        Dict mapping video filename to config: {video_name: {start_time, duration}}
    """
    import json

    if not os.path.exists(config_path):
        return {}

    try:
        with open(config_path, "r") as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"Warning: Error loading config file {config_path}: {e}")
        return {}


def main():
    parser = argparse.ArgumentParser(
        description="Process videos: extract frames, detect ROI, and auto-label"
    )
    parser.add_argument(
        "--type",
        required=True,
        choices=["puzzle", "violetta"],
        help="Type of puzzle to process",
    )
    parser.add_argument(
        "--input",
        default="recordings",
        help="Input directory containing videos (default: recordings)",
    )
    parser.add_argument(
        "--output",
        default="ai/lie_detector",
        help="Output base directory (default: ai/lie_detector)",
    )
    parser.add_argument(
        "--fps",
        type=float,
        default=1.0,
        help="Frames per second to extract (default: 1.0)",
    )
    parser.add_argument(
        "--video",
        default=None,
        help="Specific video file to process (default: process all videos)",
    )
    parser.add_argument(
        "--start-time",
        type=float,
        default=None,
        help="Start time in seconds (default: from beginning)",
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=None,
        help="Duration in seconds (default: to end)",
    )
    parser.add_argument(
        "--config",
        default=None,
        help="Path to JSON config file with video time ranges (default: auto-detect)",
    )
    parser.add_argument(
        "--config-only",
        action="store_true",
        help="Only process videos that are in config file (skip others)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode (show detailed matching info for first few frames)",
    )

    args = parser.parse_args()

    # Find videos in input directory
    input_dir = Path(args.input) / args.type
    if not input_dir.exists():
        print(f"Error: Input directory not found: {input_dir}")
        return

    # Load config file if specified or auto-detect
    config_path = args.config
    if config_path is None:
        # Auto-detect config file in input directory
        config_path = input_dir / "video_config.json"
        if not config_path.exists():
            config_path = None

    video_config = {}
    if config_path:
        video_config = load_video_config(str(config_path))
        if video_config:
            print(f"Loaded config from: {config_path}")

    # Find video(s) to process
    if args.video:
        # Process specific video
        video_path = input_dir / args.video
        if not video_path.exists():
            print(f"Error: Video file not found: {video_path}")
            return
        video_files = [video_path]
    else:
        # Process all videos
        video_files = list(input_dir.glob("*.mp4")) + list(input_dir.glob("*.avi"))

        # Filter by config if --config-only is set
        if args.config_only:
            if not video_config:
                print(
                    "Warning: --config-only specified but no config file found or empty"
                )
                print("No videos will be processed")
                return

            # Only keep videos that are in config
            video_files = [vf for vf in video_files if vf.name in video_config]

            if not video_files:
                print("No videos found in config file")
                return

            print(
                f"Config-only mode: Processing {len(video_files)} video(s) from config"
            )

    if not video_files:
        print(f"No video files found in {input_dir}")
        return

    print(f"Found {len(video_files)} video(s) to process")
    print(f"Type: {args.type}")
    print(f"Output: {args.output}")
    if video_config:
        print(f"Config: {len(video_config)} video(s) with time ranges")
    if args.config_only:
        print("Mode: Config-only (only videos in config will be processed)")
    print()

    # Process video(s)
    total_frames = 0
    for video_file in video_files:
        video_name = video_file.name

        # Get time range from config or command line args
        start_time = args.start_time
        duration = args.duration

        # Override with config if available
        if video_name in video_config:
            config = video_config[video_name]
            if start_time is None:
                start_time = config.get("start_time")
            if duration is None:
                duration = config.get("duration")

        # Convert None to actual None (in case config has null)
        if start_time is not None:
            try:
                start_time = float(start_time) if start_time != "" else None
            except (ValueError, TypeError):
                start_time = None

        if duration is not None:
            try:
                duration = float(duration) if duration != "" else None
            except (ValueError, TypeError):
                duration = None

        processed = process_video(
            str(video_file),
            args.output,
            args.type,
            fps=args.fps,
            start_time=start_time,
            duration=duration,
            debug=args.debug,
        )
        if processed:
            total_frames += len(processed)
        print()

    print("Processing complete!")
    print(f"Total processed frames: {total_frames}")

    if args.type == "puzzle":
        print("\nNext steps:")
        print(
            "1. Review labels: python tools/lie_dataset/review_labels.py --type puzzle"
        )
        print("2. Train model: python tools/lie_dataset/train_auto.py --type puzzle")
    elif args.type == "violetta":
        print("\nNext steps:")
        print("1. Label frames: python tools/lie_dataset/label_violetta_gui.py")
        print("2. Train model: python tools/lie_dataset/train_auto.py --type violetta")


if __name__ == "__main__":
    main()
