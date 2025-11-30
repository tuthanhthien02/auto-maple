"""Simple GUI tool for labeling Violetta frames."""

import os
import sys
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import cv2
from PIL import Image, ImageTk
import shutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


# Violetta classes
VIOLETTA_CLASSES = [
    "click_top_left",
    "click_top_right",
    "click_bottom_left",
    "click_bottom_right",
    "wait",
    "success",
]


class ViolettaLabeler:
    def __init__(self, root):
        self.root = root
        self.root.title("Violetta Frame Labeler")
        self.root.geometry("800x600")

        # Data
        self.frames_dir = None
        self.frame_files = []
        self.current_index = 0
        self.labels = {}  # frame_path -> class_name

        # UI
        self.setup_ui()

        # Load last session
        self.load_session()

    def setup_ui(self):
        # Frame selection
        frame_frame = ttk.Frame(self.root, padding="10")
        frame_frame.pack(fill=tk.X)

        ttk.Button(
            frame_frame, text="Select Frames Directory", command=self.select_frames_dir
        ).pack(side=tk.LEFT, padx=5)

        self.frames_label = ttk.Label(frame_frame, text="No directory selected")
        self.frames_label.pack(side=tk.LEFT, padx=5)

        # Image display
        self.image_label = ttk.Label(self.root)
        self.image_label.pack(pady=10)

        # Class selection
        class_frame = ttk.Frame(self.root, padding="10")
        class_frame.pack(fill=tk.X)

        ttk.Label(class_frame, text="Class:").pack(side=tk.LEFT, padx=5)

        self.class_var = tk.StringVar()
        self.class_combo = ttk.Combobox(
            class_frame,
            textvariable=self.class_var,
            values=VIOLETTA_CLASSES,
            state="readonly",
            width=20,
        )
        self.class_combo.pack(side=tk.LEFT, padx=5)
        self.class_combo.bind("<<ComboboxSelected>>", self.on_class_selected)

        # Navigation
        nav_frame = ttk.Frame(self.root, padding="10")
        nav_frame.pack(fill=tk.X)

        ttk.Button(nav_frame, text="Previous", command=self.prev_frame).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(nav_frame, text="Next", command=self.next_frame).pack(
            side=tk.LEFT, padx=5
        )

        ttk.Button(nav_frame, text="Skip", command=self.skip_frame).pack(
            side=tk.LEFT, padx=5
        )

        # Status
        self.status_label = ttk.Label(self.root, text="Ready", font=("Arial", 10))
        self.status_label.pack(pady=5)

        # Save button
        ttk.Button(self.root, text="Save Labels", command=self.save_labels).pack(
            pady=10
        )

    def select_frames_dir(self):
        """Select directory containing frames to label."""
        dir_path = filedialog.askdirectory(
            title="Select Frames Directory",
            initialdir=os.path.join(
                project_root, "ai", "lie_detector", "violetta", "dataset", "raw_frames"
            ),
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

        self.frames_label.config(text=f"{len(self.frame_files)} frames found")
        self.current_index = 0
        self.load_frame()

    def load_frame(self):
        """Load and display current frame."""
        if not self.frame_files or self.current_index >= len(self.frame_files):
            self.status_label.config(text="No more frames")
            return

        frame_path = self.frame_files[self.current_index]

        # Load image
        frame = cv2.imread(str(frame_path))
        if frame is None:
            self.status_label.config(text=f"Error loading {frame_path.name}")
            return

        # Resize for display (max 600x400)
        height, width = frame.shape[:2]
        max_width, max_height = 600, 400
        scale = min(max_width / width, max_height / height, 1.0)
        new_width = int(width * scale)
        new_height = int(height * scale)

        frame_resized = cv2.resize(frame, (new_width, new_height))

        # Convert to RGB for tkinter
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame_rgb)
        photo = ImageTk.PhotoImage(image)

        self.image_label.config(image=photo)
        self.image_label.image = photo  # Keep a reference

        # Load existing label if any
        if str(frame_path) in self.labels:
            self.class_var.set(self.labels[str(frame_path)])
        else:
            self.class_var.set("")

        # Update status
        self.status_label.config(
            text=f"Frame {self.current_index + 1}/{len(self.frame_files)}: {frame_path.name}"
        )

    def on_class_selected(self, event=None):
        """Save label when class is selected."""
        if not self.frame_files or self.current_index >= len(self.frame_files):
            return

        frame_path = self.frame_files[self.current_index]
        class_name = self.class_var.get()

        if class_name:
            self.labels[str(frame_path)] = class_name

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
        """Skip current frame."""
        self.next_frame()

    def save_labels(self):
        """Save labels to dataset structure."""
        if not self.labels:
            messagebox.showwarning("No Labels", "No labels to save")
            return

        # Ask for output directory
        output_dir = filedialog.askdirectory(
            title="Select Output Dataset Directory",
            initialdir=os.path.join(
                project_root, "ai", "lie_detector", "violetta", "dataset"
            ),
        )

        if not output_dir:
            return

        # Organize by class
        train_dir = os.path.join(output_dir, "train")
        os.makedirs(train_dir, exist_ok=True)

        for class_name in VIOLETTA_CLASSES:
            os.makedirs(os.path.join(train_dir, class_name), exist_ok=True)

        # Copy frames to class directories
        copied = 0
        for frame_path, class_name in self.labels.items():
            if not class_name:
                continue

            src = Path(frame_path)
            dst = os.path.join(train_dir, class_name, src.name)
            shutil.copy2(src, dst)
            copied += 1

        messagebox.showinfo("Saved", f"Saved {copied} labeled frames to {train_dir}")

        # Save session
        self.save_session()

    def save_session(self):
        """Save current session state."""
        session_file = os.path.join(
            project_root, "ai", "lie_detector", "violetta", "labeling_session.json"
        )
        import json

        session_data = {
            "frames_dir": self.frames_dir,
            "current_index": self.current_index,
            "labels": self.labels,
        }

        os.makedirs(os.path.dirname(session_file), exist_ok=True)
        with open(session_file, "w") as f:
            json.dump(session_data, f, indent=2)

    def load_session(self):
        """Load last session state."""
        session_file = os.path.join(
            project_root, "ai", "lie_detector", "violetta", "labeling_session.json"
        )

        if not os.path.exists(session_file):
            return

        import json

        try:
            with open(session_file, "r") as f:
                session_data = json.load(f)

            self.frames_dir = session_data.get("frames_dir")
            self.labels = session_data.get("labels", {})

            if self.frames_dir and os.path.exists(self.frames_dir):
                # Reload frames
                self.frame_files = []
                for ext in ["*.png", "*.jpg", "*.jpeg"]:
                    self.frame_files.extend(Path(self.frames_dir).rglob(ext))
                self.frame_files = sorted(self.frame_files)

                self.current_index = session_data.get("current_index", 0)
                self.frames_label.config(text=f"{len(self.frame_files)} frames found")

                if self.frame_files:
                    self.load_frame()
        except Exception as e:
            print(f"Error loading session: {e}")


def main():
    root = tk.Tk()
    ViolettaLabeler(root)
    root.mainloop()


if __name__ == "__main__":
    main()
