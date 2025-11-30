"""GUI tool to review and fix auto-generated labels."""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import cv2
from PIL import Image, ImageTk

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class LabelReviewer:
    def __init__(self, root, puzzle_type: str):
        self.root = root
        self.root.title(f"Review Labels - {puzzle_type}")
        self.root.geometry("900x700")

        self.puzzle_type = puzzle_type
        self.frames_dir = None
        self.labels_dir = None
        self.frame_files = []
        self.current_index = 0
        self.current_bbox = None

        self.setup_ui()

    def setup_ui(self):
        # Directory selection
        dir_frame = ttk.Frame(self.root, padding="10")
        dir_frame.pack(fill=tk.X)

        ttk.Button(
            dir_frame, text="Select Dataset Directory", command=self.select_dataset_dir
        ).pack(side=tk.LEFT, padx=5)

        self.dir_label = ttk.Label(dir_frame, text="No directory selected")
        self.dir_label.pack(side=tk.LEFT, padx=5)

        # Image display with canvas for drawing
        canvas_frame = ttk.Frame(self.root)
        canvas_frame.pack(pady=10)

        self.canvas = tk.Canvas(canvas_frame, width=640, height=480, bg="black")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.canvas.bind("<B1-Motion>", self.on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_canvas_release)

        self.drawing = False
        self.start_x = 0
        self.start_y = 0

        # Controls
        control_frame = ttk.Frame(self.root, padding="10")
        control_frame.pack(fill=tk.X)

        ttk.Button(control_frame, text="Approve", command=self.approve_label).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(control_frame, text="Reject", command=self.reject_label).pack(
            side=tk.LEFT, padx=5
        )
        ttk.Button(control_frame, text="Fix", command=self.fix_label).pack(
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

        # Status
        self.status_label = ttk.Label(self.root, text="Ready", font=("Arial", 10))
        self.status_label.pack(pady=5)

    def select_dataset_dir(self):
        """Select dataset directory."""
        base_dir = os.path.join(
            project_root, "ai", "lie_detector", self.puzzle_type, "dataset"
        )

        dir_path = filedialog.askdirectory(
            title="Select Dataset Directory", initialdir=base_dir
        )

        if not dir_path:
            return

        self.frames_dir = os.path.join(dir_path, "raw_frames")
        self.labels_dir = os.path.join(dir_path, "labels")

        if not os.path.exists(self.frames_dir):
            messagebox.showerror(
                "Error", f"Frames directory not found: {self.frames_dir}"
            )
            return

        # Find all frames
        self.frame_files = []
        for ext in ["*.png", "*.jpg", "*.jpeg"]:
            for subdir in Path(self.frames_dir).rglob(ext):
                self.frame_files.append(subdir)

        self.frame_files = sorted(self.frame_files)

        if not self.frame_files:
            messagebox.showwarning("No Frames", "No frames found")
            return

        self.dir_label.config(text=f"{len(self.frame_files)} frames found")
        self.current_index = 0
        self.load_frame()

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
        max_width, max_height = 640, 480
        scale = min(max_width / width, max_height / height, 1.0)
        new_width = int(width * scale)
        new_height = int(height * scale)

        self.display_scale = scale
        self.original_size = (width, height)

        frame_resized = cv2.resize(frame, (new_width, new_height))

        # Convert to RGB
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image)

        self.canvas.delete("all")
        self.canvas.create_image(0, 0, anchor=tk.NW, image=photo)
        self.canvas.image = photo

        # Load label if exists
        label_path = self.get_label_path(frame_path)
        self.current_bbox = None

        if label_path and os.path.exists(label_path):
            bbox = self.load_yolo_label(label_path, width, height)
            if bbox:
                self.current_bbox = bbox
                self.draw_bbox(bbox, scale)

        # Update status
        self.status_label.config(
            text=f"Frame {self.current_index + 1}/{len(self.frame_files)}: {frame_path.name}"
        )

    def get_label_path(self, frame_path: Path) -> str:
        """Get corresponding label file path."""
        if not self.labels_dir:
            return None

        # Find relative path from frames_dir
        rel_path = frame_path.relative_to(Path(self.frames_dir))
        label_path = Path(self.labels_dir) / rel_path.parent / f"{frame_path.stem}.txt"
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

    def draw_bbox(self, bbox: tuple, scale: float = 1.0):
        """Draw bounding box on canvas."""
        x_min, y_min, x_max, y_max = bbox
        x_min = int(x_min * scale)
        y_min = int(y_min * scale)
        x_max = int(x_max * scale)
        y_max = int(y_max * scale)

        self.canvas.create_rectangle(
            x_min, y_min, x_max, y_max, outline="green", width=2
        )

    def on_canvas_click(self, event):
        """Start drawing new bbox."""
        self.drawing = True
        self.start_x = event.x
        self.start_y = event.y

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
            # Save new bbox
            x_min = min(self.start_x, event.x)
            y_min = min(self.start_y, event.y)
            x_max = max(self.start_x, event.x)
            y_max = max(self.start_y, event.y)

            # Convert to original coordinates
            scale = self.display_scale
            orig_x_min = int(x_min / scale)
            orig_y_min = int(y_min / scale)
            orig_x_max = int(x_max / scale)
            orig_y_max = int(y_max / scale)

            self.current_bbox = (orig_x_min, orig_y_min, orig_x_max, orig_y_max)

            # Redraw
            self.load_frame()

    def approve_label(self):
        """Approve current label."""
        if not self.current_bbox:
            messagebox.showwarning("No Label", "No label to approve")
            return

        self.next_frame()

    def reject_label(self):
        """Reject current label (delete it)."""
        if not self.frame_files or self.current_index >= len(self.frame_files):
            return

        frame_path = self.frame_files[self.current_index]
        label_path = self.get_label_path(frame_path)

        if label_path and os.path.exists(label_path):
            os.remove(label_path)
            messagebox.showinfo("Rejected", "Label deleted")

        self.current_bbox = None
        self.load_frame()

    def fix_label(self):
        """Fix label by drawing new bbox."""
        messagebox.showinfo(
            "Fix Label",
            "Click and drag on canvas to draw new bounding box, then click Fix again to save",
        )

    def save_label(self):
        """Save current bbox as YOLO label."""
        if not self.current_bbox or not self.frame_files:
            return

        frame_path = self.frame_files[self.current_index]
        label_path = self.get_label_path(frame_path)

        if not label_path:
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

        # Write YOLO format
        with open(label_path, "w") as f:
            f.write(
                f"0 {center_x:.6f} {center_y:.6f} {bbox_width:.6f} {bbox_height:.6f}"
            )

    def prev_frame(self):
        """Go to previous frame."""
        if self.current_bbox:
            self.save_label()

        if self.current_index > 0:
            self.current_index -= 1
            self.load_frame()

    def next_frame(self):
        """Go to next frame."""
        if self.current_bbox:
            self.save_label()

        if self.current_index < len(self.frame_files) - 1:
            self.current_index += 1
            self.load_frame()
        else:
            messagebox.showinfo("Complete", "All frames reviewed!")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Review auto-generated labels")
    parser.add_argument(
        "--type", required=True, choices=["puzzle", "violetta"], help="Puzzle type"
    )

    args = parser.parse_args()

    root = tk.Tk()
    LabelReviewer(root, args.type)
    root.mainloop()


if __name__ == "__main__":
    main()
