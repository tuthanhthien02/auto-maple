"""GUI tool for labeling Puzzle frames with bounding boxes (YOLO format)."""

import json
import os
import sys
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import cv2
from PIL import Image, ImageTk

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class PuzzleYOLOLabeler:
    def __init__(self, root):
        self.root = root
        self.root.title("Puzzle YOLO Labeler")
        self.root.geometry("1000x800")

        # Data
        self.frames_dir = None
        self.labels_dir = None
        self.frame_files = []
        self.current_index = 0
        self.current_bbox = None
        self.drawing = False
        self.start_x = 0
        self.start_y = 0
        self.display_scale = 1.0
        self.original_size = (0, 0)
        self.image_x_offset = 0
        self.image_y_offset = 0

        # UI
        self.setup_ui()

        # Load last session
        self.load_session()

    def setup_ui(self):
        # Directory selection
        dir_frame = ttk.Frame(self.root, padding="10")
        dir_frame.pack(fill=tk.X)

        ttk.Button(
            dir_frame, text="Select Frames Directory", command=self.select_frames_dir
        ).pack(side=tk.LEFT, padx=5)

        self.frames_label = ttk.Label(dir_frame, text="No directory selected")
        self.frames_label.pack(side=tk.LEFT, padx=5)

        # Frame counter (prominent display)
        counter_frame = ttk.Frame(self.root, padding="5")
        counter_frame.pack(fill=tk.X)

        self.frame_counter_label = ttk.Label(
            counter_frame,
            text="Frame: 0/0",
            font=("Arial", 12, "bold"),
            foreground="blue",
        )
        self.frame_counter_label.pack(side=tk.LEFT, padx=10)

        # Instructions with detailed guidance
        info_frame = ttk.Frame(self.root, padding="5")
        info_frame.pack(fill=tk.X)

        instructions_text = (
            "📋 Instructions:\n"
            "1. Click and drag to draw bounding box around the green circular target\n"
            "2. Label the target that appears in the puzzle (the green circle to follow)\n"
            "3. Skip frames without target or unclear frames"
        )

        ttk.Label(
            info_frame,
            text=instructions_text,
            font=("Arial", 9),
            foreground="darkgreen",
            justify=tk.LEFT,
        ).pack(anchor=tk.W, padx=10)

        # Hotkeys help
        hotkeys_frame = ttk.Frame(self.root, padding="5")
        hotkeys_frame.pack(fill=tk.X)

        hotkeys_text = (
            "⌨️ Hotkeys: "
            "[Space/→] Next | "
            "[Backspace/←] Previous | "
            "[S] Save | "
            "[D] Delete | "
            "[C] Clear | "
            "[K] Skip | "
            "[Esc] Clear"
        )

        ttk.Label(
            hotkeys_frame,
            text=hotkeys_text,
            font=("Arial", 8),
            foreground="darkblue",
        ).pack(anchor=tk.W, padx=10)

        # Image display with canvas for drawing
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(pady=10)

        # Canvas with scrollbars if needed
        self.canvas = tk.Canvas(
            canvas_frame, width=800, height=600, bg="black", highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        # Bind hotkeys
        self.setup_hotkeys()

        # Controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        ttk.Button(control_frame, text="Save Label", command=self.save_label).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(control_frame, text="Delete Label", command=self.delete_label).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(control_frame, text="Clear Box", command=self.clear_box).pack(
            side=tk.LEFT, padx=5
        )

        # Navigation
        nav_frame = ttk.Frame(self.root, padding="10")
        nav_frame.pack(fill=tk.X)

        ttk.Button(nav_frame, text="Previous", command=self.prev_frame).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(nav_frame, text="Next", command=self.next_frame).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(nav_frame, text="Skip (No Target)", command=self.skip_frame).pack(
            side=tk.LEFT, padx=5
        )

        # Status
        self.status_label = ttk.Label(self.root, text="Ready", font=("Arial", 10))
        self.status_label.pack(pady=5)

        # Progress
        self.progress_label = ttk.Label(
            self.root, text="", font=("Arial", 9), foreground="blue"
        )
        self.progress_label.pack(pady=2)

    def setup_hotkeys(self):
        """Setup keyboard shortcuts."""
        # Navigation
        self.root.bind("<space>", lambda e: self.next_frame())
        self.root.bind("<Right>", lambda e: self.next_frame())
        self.root.bind("<BackSpace>", lambda e: self.prev_frame())
        self.root.bind("<Left>", lambda e: self.prev_frame())

        # Actions
        self.root.bind("<s>", lambda e: self.save_label())
        self.root.bind("<S>", lambda e: self.save_label())
        self.root.bind("<d>", lambda e: self.delete_label())
        self.root.bind("<D>", lambda e: self.delete_label())
        self.root.bind("<c>", lambda e: self.clear_box())
        self.root.bind("<C>", lambda e: self.clear_box())
        self.root.bind("<k>", lambda e: self.skip_frame())
        self.root.bind("<K>", lambda e: self.skip_frame())
        self.root.bind("<Escape>", lambda e: self.clear_box())

        # Also bind to canvas for better interaction
        self.canvas.bind("<space>", lambda e: self.next_frame())
        self.canvas.bind("<Right>", lambda e: self.next_frame())
        self.canvas.bind("<BackSpace>", lambda e: self.prev_frame())
        self.canvas.bind("<Left>", lambda e: self.prev_frame())
        self.canvas.bind("<s>", lambda e: self.save_label())
        self.canvas.bind("<S>", lambda e: self.save_label())
        self.canvas.bind("<d>", lambda e: self.delete_label())
        self.canvas.bind("<D>", lambda e: self.delete_label())
        self.canvas.bind("<c>", lambda e: self.clear_box())
        self.canvas.bind("<C>", lambda e: self.clear_box())
        self.canvas.bind("<k>", lambda e: self.skip_frame())
        self.canvas.bind("<K>", lambda e: self.skip_frame())
        self.canvas.bind("<Escape>", lambda e: self.clear_box())

        # Focus on canvas for better interaction
        self.canvas.focus_set()

    def select_frames_dir(self):
        """Select directory containing frames to label."""
        base_dir = os.path.join(
            project_root, "ai", "lie_detector", "puzzle", "dataset", "raw_frames"
        )

        dir_path = filedialog.askdirectory(
            title="Select Frames Directory", initialdir=base_dir
        )

        if not dir_path:
            return

        self.frames_dir = dir_path

        # Find all image files
        self.frame_files = []
        for ext in ["*.png", "*.jpg", "*.jpeg"]:
            self.frame_files.extend(Path(dir_path).rglob(ext))

        self.frame_files = sorted(self.frame_files)

        if not self.frame_files:
            messagebox.showwarning("No Frames", "No image files found in directory")
            return

        # Determine labels directory
        # If frames are in raw_frames/puzzle_001/, labels go to labels/puzzle_001/
        rel_path = Path(dir_path).relative_to(
            Path(project_root)
            / "ai"
            / "lie_detector"
            / "puzzle"
            / "dataset"
            / "raw_frames"
        )
        self.labels_dir = os.path.join(
            project_root,
            "ai",
            "lie_detector",
            "puzzle",
            "dataset",
            "labels",
            str(rel_path),
        )
        os.makedirs(self.labels_dir, exist_ok=True)

        self.frames_label.config(text=f"{len(self.frame_files)} frames found")
        self.current_index = 0
        self.frame_counter_label.config(text=f"Frame: 0/{len(self.frame_files)}")
        self.update_progress()
        self.load_frame()

    def get_label_path(self, frame_path: Path) -> str:
        """Get corresponding label file path."""
        if not self.labels_dir:
            return None

        label_path = Path(self.labels_dir) / f"{frame_path.stem}.txt"
        return str(label_path)

    def load_yolo_label(
        self, label_path: str, img_width: int, img_height: int
    ) -> tuple:
        """Load YOLO format label and convert to pixel coordinates."""
        try:
            with open(label_path, "r") as f:
                line = f.readline().strip()
                if not line:
                    return None

                parts = line.split()
                if len(parts) < 5:
                    return None

                center_x = float(parts[1]) * img_width
                center_y = float(parts[2]) * img_height
                width = float(parts[3]) * img_width
                height = float(parts[4]) * img_height

                x_min = center_x - width / 2
                y_min = center_y - height / 2
                x_max = center_x + width / 2
                y_max = center_y + height / 2

                return (int(x_min), int(y_min), int(x_max), int(y_max))
        except Exception as e:
            print(f"Error loading label: {e}")
            return None

    def load_frame(self):
        """Load current frame and its label."""
        if not self.frame_files or self.current_index >= len(self.frame_files):
            self.status_label.config(text="No more frames")
            return

        frame_path = self.frame_files[self.current_index]

        # Load image
        frame = cv2.imread(str(frame_path))
        if frame is None:
            self.status_label.config(text=f"Error loading {frame_path.name}")
            return

        # Resize for display
        height, width = frame.shape[:2]
        self.original_size = (width, height)
        max_width, max_height = 800, 600

        # Calculate scale to fit within canvas while maintaining aspect ratio
        scale = min(max_width / width, max_height / height, 1.0)
        new_width = int(width * scale)
        new_height = int(height * scale)

        self.display_scale = scale

        # Resize frame
        frame_resized = cv2.resize(
            frame, (new_width, new_height), interpolation=cv2.INTER_AREA
        )

        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image)

        # Clear canvas
        self.canvas.delete("all")

        # Update canvas scroll region to match image size (ensure full image is accessible)
        self.canvas.config(
            scrollregion=(0, 0, max(new_width, 800), max(new_height, 600))
        )

        # Display image centered or at top-left, ensuring no clipping
        # If image is smaller than canvas, center it; otherwise start from (0,0)
        if new_width < 800 and new_height < 600:
            # Center small images
            img_x = (800 - new_width) // 2
            img_y = (600 - new_height) // 2
        else:
            # Start from top-left for larger images
            img_x = 0
            img_y = 0

        self.canvas.create_image(img_x, img_y, anchor=tk.NW, image=photo)
        self.canvas.image = photo  # Keep reference to prevent garbage collection

        # Store image position for coordinate conversion
        self.image_x_offset = img_x
        self.image_y_offset = img_y

        # Load label if exists
        label_path = self.get_label_path(frame_path)
        self.current_bbox = None

        if label_path and os.path.exists(label_path):
            bbox = self.load_yolo_label(label_path, width, height)
            if bbox:
                self.current_bbox = bbox
                self.draw_bbox(bbox, scale)

        # Update frame counter (prominent)
        self.frame_counter_label.config(
            text=f"Frame: {self.current_index + 1}/{len(self.frame_files)}"
        )

        # Update status
        self.status_label.config(text=f"Current: {frame_path.name}")
        self.update_progress()

    def draw_bbox(self, bbox: tuple, scale: float = 1.0):
        """Draw bounding box on canvas."""
        x_min, y_min, x_max, y_max = bbox
        x_min = int(x_min * scale) + self.image_x_offset
        y_min = int(y_min * scale) + self.image_y_offset
        x_max = int(x_max * scale) + self.image_x_offset
        y_max = int(y_max * scale) + self.image_y_offset

        self.canvas.create_rectangle(
            x_min, y_min, x_max, y_max, outline="green", width=3, tags="bbox"
        )

    def on_canvas_click(self, event):
        """Start drawing new bbox."""
        # Adjust for image offset
        click_x = event.x - self.image_x_offset
        click_y = event.y - self.image_y_offset

        # Only start drawing if click is within image bounds
        if click_x < 0 or click_y < 0:
            return

        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y
        self.canvas.delete("bbox_preview")

    def on_canvas_drag(self, event):
        """Update bbox while dragging."""
        if self.drawing:
            self.canvas.delete("bbox_preview")
            self.canvas.create_rectangle(
                self.start_x,
                self.start_y,
                event.x,
                event.y,
                outline="yellow",
                width=2,
                tags="bbox_preview",
            )

    def on_canvas_release(self, event):
        """Finish drawing bbox."""
        if self.drawing:
            self.drawing = False

            # Adjust for image offset
            start_x_adj = self.start_x - self.image_x_offset
            start_y_adj = self.start_y - self.image_y_offset
            end_x_adj = event.x - self.image_x_offset
            end_y_adj = event.y - self.image_y_offset

            # Only save if click is within image bounds
            if start_x_adj < 0 or start_y_adj < 0 or end_x_adj < 0 or end_y_adj < 0:
                self.canvas.delete("bbox_preview")
                return

            # Calculate bbox in display coordinates (relative to image)
            x_min = min(start_x_adj, end_x_adj)
            y_min = min(start_y_adj, end_y_adj)
            x_max = max(start_x_adj, end_x_adj)
            y_max = max(start_y_adj, end_y_adj)

            # Only save if bbox is large enough
            if abs(x_max - x_min) < 10 or abs(y_max - y_min) < 10:
                self.canvas.delete("bbox_preview")
                return

            # Convert to original coordinates
            scale = self.display_scale
            orig_x_min = max(0, int(x_min / scale))
            orig_y_min = max(0, int(y_min / scale))
            orig_x_max = min(self.original_size[0], int(x_max / scale))
            orig_y_max = min(self.original_size[1], int(y_max / scale))

            self.current_bbox = (orig_x_min, orig_y_min, orig_x_max, orig_y_max)

            # Redraw with saved bbox
            self.canvas.delete("bbox_preview")
            self.draw_bbox(self.current_bbox, scale)

    def save_label(self):
        """Save current bbox as YOLO label."""
        if not self.current_bbox or not self.frame_files:
            messagebox.showwarning("No Box", "Please draw a bounding box first")
            return

        frame_path = self.frame_files[self.current_index]
        label_path = self.get_label_path(frame_path)

        if not label_path:
            messagebox.showerror("Error", "Cannot determine label path")
            return

        # Create directory if needed
        os.makedirs(os.path.dirname(label_path), exist_ok=True)

        # Convert to YOLO format
        x_min, y_min, x_max, y_max = self.current_bbox
        width, height = self.original_size

        center_x = ((x_min + x_max) / 2.0) / width
        center_y = ((y_min + y_max) / 2.0) / height
        bbox_width = (x_max - x_min) / width
        bbox_height = (y_max - y_min) / height

        # Clamp to [0, 1]
        center_x = max(0.0, min(1.0, center_x))
        center_y = max(0.0, min(1.0, center_y))
        bbox_width = max(0.0, min(1.0, bbox_width))
        bbox_height = max(0.0, min(1.0, bbox_height))

        # Write YOLO format: class_id center_x center_y width height
        with open(label_path, "w") as f:
            f.write(
                f"0 {center_x:.6f} {center_y:.6f} {bbox_width:.6f} {bbox_height:.6f}\n"
            )

        self.status_label.config(text=f"Label saved: {frame_path.name}")
        self.save_session()

    def delete_label(self):
        """Delete current label."""
        if not self.frame_files or self.current_index >= len(self.frame_files):
            return

        frame_path = self.frame_files[self.current_index]
        label_path = self.get_label_path(frame_path)

        if label_path and os.path.exists(label_path):
            os.remove(label_path)
            self.current_bbox = None
            self.canvas.delete("bbox")
            self.status_label.config(text=f"Label deleted: {frame_path.name}")
            self.save_session()
        else:
            messagebox.showinfo("No Label", "No label to delete")

    def clear_box(self):
        """Clear current bbox without saving."""
        self.current_bbox = None
        self.canvas.delete("bbox")
        self.canvas.delete("bbox_preview")

    def update_progress(self):
        """Update progress label."""
        if not self.frame_files:
            self.progress_label.config(text="")
            return

        # Count labeled frames
        labeled_count = 0
        for frame_path in self.frame_files:
            label_path = self.get_label_path(frame_path)
            if label_path and os.path.exists(label_path):
                labeled_count += 1

        self.progress_label.config(
            text=f"Progress: {labeled_count}/{len(self.frame_files)} frames labeled ({labeled_count*100//len(self.frame_files) if self.frame_files else 0}%)"
        )

    def prev_frame(self):
        """Go to previous frame."""
        if self.current_index > 0:
            self.current_index -= 1
            self.load_frame()

    def next_frame(self):
        """Go to next frame."""
        if self.current_index < len(self.frame_files) - 1:
            self.current_index += 1
            self.load_frame()
        else:
            messagebox.showinfo("Complete", "All frames processed!")

    def skip_frame(self):
        """Skip frame (no target in this frame)."""
        # Just move to next frame without saving
        self.next_frame()

    def save_session(self):
        """Save current session state."""
        session_file = os.path.join(
            project_root, "ai", "lie_detector", "puzzle", "yolo_labeling_session.json"
        )

        session_data = {
            "frames_dir": self.frames_dir,
            "labels_dir": self.labels_dir,
            "current_index": self.current_index,
        }

        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)

    def load_session(self):
        """Load last session state."""
        session_file = os.path.join(
            project_root, "ai", "lie_detector", "puzzle", "yolo_labeling_session.json"
        )

        if not os.path.exists(session_file):
            return

        try:
            with open(session_file, "r") as f:
                session_data = json.load(f)

            self.frames_dir = session_data.get("frames_dir")
            self.labels_dir = session_data.get("labels_dir")

            if self.frames_dir and os.path.exists(self.frames_dir):
                # Reload frames
                self.frame_files = []
                for ext in ["*.png", "*.jpg", "*.jpeg"]:
                    self.frame_files.extend(Path(self.frames_dir).rglob(ext))
                self.frame_files = sorted(self.frame_files)

                self.current_index = session_data.get("current_index", 0)
                self.frames_label.config(text=f"{len(self.frame_files)} frames found")
                self.frame_counter_label.config(
                    text=f"Frame: {self.current_index + 1}/{len(self.frame_files)}"
                )

                if self.frame_files:
                    self.update_progress()
                    self.load_frame()
        except Exception as e:
            print(f"Error loading session: {e}")


def main():
    root = tk.Tk()
    PuzzleYOLOLabeler(root)
    root.mainloop()


if __name__ == "__main__":
    main()
