"""
Utility overlay that lets the user drag a rectangle on screen and returns the
selected region (left, top, width, height). Designed to be launched from the
Auto Maple GUI for manual capture workflows.
"""

from __future__ import annotations

import ctypes
import json
import tkinter as tk
from typing import Dict, Optional


def select_region() -> Optional[Dict[str, int]]:
    """
    Launch a fullscreen semi-transparent overlay to let the user select a region.

    Returns:
        A dict containing left/top/width/height if a region was selected,
        otherwise None.
    """

    result: Dict[str, int] = {}

    # Make sure the process is DPI-aware so the coordinates match physical pixels.
    try:
        awareness = ctypes.c_int(2)  # PROCESS_PER_MONITOR_DPI_AWARE
        ctypes.windll.shcore.SetProcessDpiAwareness(awareness)
    except Exception:
        try:
            ctypes.windll.user32.SetProcessDPIAware()
        except Exception:
            pass
    existing_root = tk._default_root
    if existing_root is None:
        root = tk.Tk()
        is_standalone = True
    else:
        root = tk.Toplevel(existing_root)
        is_standalone = False

    root.withdraw()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.overrideredirect(True)
    root.geometry(f"{screen_width}x{screen_height}+0+0")
    root.attributes("-alpha", 0.18)
    root.configure(bg="black")
    root.attributes("-topmost", True)
    root.deiconify()
    root.lift()
    root.focus_force()
    root.title("Select Capture Region - Drag to select, Esc to cancel")

    canvas = tk.Canvas(root, highlightthickness=0, cursor="crosshair", bg="black")
    canvas.pack(fill="both", expand=True)

    start = {"x": 0, "y": 0}
    rect_id = {"value": None}

    def on_press(event):
        start["x"] = event.x_root
        start["y"] = event.y_root
        if rect_id["value"] is not None:
            canvas.delete(rect_id["value"])
            rect_id["value"] = None

    def on_drag(event):
        if rect_id["value"] is not None:
            canvas.delete(rect_id["value"])
        rect_id["value"] = canvas.create_rectangle(
            start["x"],
            start["y"],
            event.x_root,
            event.y_root,
            outline="#00FF00",
            width=2,
        )

    def on_release(event):
        left = min(start["x"], event.x_root)
        top = min(start["y"], event.y_root)
        width = abs(event.x_root - start["x"])
        height = abs(event.y_root - start["y"])
        if width < 10 or height < 10:
            # Ignore accidental clicks
            root.destroy()
            return
        result.update({"left": left, "top": top, "width": width, "height": height})
        root.destroy()

    def on_escape(_event):
        result.clear()
        root.destroy()

    canvas.bind("<ButtonPress-1>", on_press)
    canvas.bind("<B1-Motion>", on_drag)
    canvas.bind("<ButtonRelease-1>", on_release)
    root.bind("<Escape>", on_escape)

    # Run modal loop
    if is_standalone:
        root.mainloop()
    else:
        try:
            root.grab_set()
        except Exception:
            pass
        root.wait_window()

    return result or None


if __name__ == "__main__":
    region = select_region()
    if region:
        print(json.dumps(region))
    else:
        print("")
