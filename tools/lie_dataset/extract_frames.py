"""Extract frames from video files using ffmpeg."""

import os
import subprocess
import cv2
import numpy as np
from pathlib import Path


def extract_frames_from_video(
    video_path: str,
    output_dir: str,
    fps: float = 1.0,
    prefix: str = "frame",
    start_time: float = None,
    duration: float = None,
):
    """
    Extract frames from video using ffmpeg.

    Args:
        video_path: Path to input video file
        output_dir: Directory to save extracted frames
        fps: Frames per second to extract (1.0 = 1 frame per second)
        prefix: Prefix for output frame filenames
        start_time: Start time in seconds (None = from beginning)
        duration: Duration in seconds (None = to end)

    Returns:
        List of extracted frame file paths
    """
    os.makedirs(output_dir, exist_ok=True)

    # Use ffmpeg to extract frames
    output_pattern = os.path.join(output_dir, f"{prefix}_%06d.png")

    # Build ffmpeg command
    cmd = ["ffmpeg"]

    # Add start time if specified (before -i for faster seeking)
    if start_time is not None:
        cmd.extend(["-ss", str(start_time)])

    cmd.extend(["-i", video_path])

    # Add duration if specified
    if duration is not None:
        cmd.extend(["-t", str(duration)])

    cmd.extend(
        [
            "-vf",
            f"fps={fps}",
            "-y",  # Overwrite output files
            output_pattern,
        ]
    )

    try:
        subprocess.run(cmd, check=True, capture_output=True)
    except subprocess.CalledProcessError as e:
        print(f"Error extracting frames from {video_path}: {e}")
        print(f"ffmpeg stderr: {e.stderr.decode() if e.stderr else 'No stderr'}")
        return []
    except FileNotFoundError:
        print("Error: ffmpeg not found. Please install ffmpeg.")
        return []

    # Get list of extracted frames
    frame_files = sorted(Path(output_dir).glob(f"{prefix}_*.png"))
    return [str(f) for f in frame_files]


def load_frame(frame_path: str) -> np.ndarray:
    """Load a frame image."""
    return cv2.imread(frame_path)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print(
            "Usage: python extract_frames.py <video_path> <output_dir> [fps] [start_time] [duration]"
        )
        print("Example: python extract_frames.py video.mp4 output/ 1.0 5.0 20.0")
        sys.exit(1)

    video_path = sys.argv[1]
    output_dir = sys.argv[2]
    fps = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
    start_time = float(sys.argv[4]) if len(sys.argv) > 4 and sys.argv[4] else None
    duration = float(sys.argv[5]) if len(sys.argv) > 5 and sys.argv[5] else None

    frames = extract_frames_from_video(
        video_path, output_dir, fps, start_time=start_time, duration=duration
    )
    print(f"Extracted {len(frames)} frames to {output_dir}")
