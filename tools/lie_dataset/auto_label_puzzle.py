"""Auto-label puzzle target using color detection."""

import cv2
import numpy as np


def detect_green_circular_target(frame: np.ndarray) -> tuple:
    """
    Detect green circular target in puzzle frame using color detection.

    Args:
        frame: Input frame (BGR format)

    Returns:
        (center_x, center_y, radius) if found, None otherwise
    """
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Green color range (adjust based on actual target color)
    # Typical green: H=60-80, S=100-255, V=100-255
    lower_green = np.array([50, 100, 100])
    upper_green = np.array([80, 255, 255])

    # Create mask
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Morphological operations to clean up mask
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        return None

    # Find largest contour (likely the target)
    largest_contour = max(contours, key=cv2.contourArea)

    # Check if it's roughly circular
    area = cv2.contourArea(largest_contour)
    if area < 100:  # Too small
        return None

    # Fit circle
    (x, y), radius = cv2.minEnclosingCircle(largest_contour)

    # Check circularity
    circularity = 4 * np.pi * area / (cv2.arcLength(largest_contour, True) ** 2)
    if circularity < 0.7:  # Not circular enough
        return None

    return (int(x), int(y), int(radius))


def auto_label_puzzle_frame(frame: np.ndarray) -> str:
    """
    Auto-label puzzle frame and return YOLO format annotation.

    Args:
        frame: Input frame (BGR format, already cropped to ROI)

    Returns:
        YOLO format annotation string: "class_id center_x center_y width height"
        Returns empty string if target not found
    """
    target = detect_green_circular_target(frame)

    if target is None:
        return ""

    center_x, center_y, radius = target
    height, width = frame.shape[:2]

    # Calculate bounding box
    x_min = max(0, center_x - radius)
    y_min = max(0, center_y - radius)
    x_max = min(width, center_x + radius)
    y_max = min(height, center_y + radius)

    # Convert to YOLO format (normalized)
    bbox_center_x = (x_min + x_max) / 2.0 / width
    bbox_center_y = (y_min + y_max) / 2.0 / height
    bbox_width = (x_max - x_min) / width
    bbox_height = (y_max - y_min) / height

    # Class ID: 0 for puzzle_target
    class_id = 0

    return f"{class_id} {bbox_center_x:.6f} {bbox_center_y:.6f} {bbox_width:.6f} {bbox_height:.6f}"


def visualize_detection(frame: np.ndarray, save_path: str = None) -> np.ndarray:
    """
    Visualize detected target on frame.

    Args:
        frame: Input frame
        save_path: Optional path to save visualization

    Returns:
        Frame with visualization
    """
    target = detect_green_circular_target(frame)

    vis_frame = frame.copy()

    if target:
        center_x, center_y, radius = target
        cv2.circle(vis_frame, (center_x, center_y), radius, (0, 255, 0), 2)
        cv2.circle(vis_frame, (center_x, center_y), 2, (0, 0, 255), -1)

    if save_path:
        cv2.imwrite(save_path, vis_frame)

    return vis_frame


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python auto_label_puzzle.py <frame_path> [output_vis_path]")
        sys.exit(1)

    frame_path = sys.argv[1]
    frame = cv2.imread(frame_path)

    if frame is None:
        print(f"Error: Could not load frame from {frame_path}")
        sys.exit(1)

    annotation = auto_label_puzzle_frame(frame)

    if annotation:
        print(f"Annotation: {annotation}")
    else:
        print("No target detected")

    if len(sys.argv) > 2:
        visualize_detection(frame, sys.argv[2])
        print(f"Visualization saved to {sys.argv[2]}")
