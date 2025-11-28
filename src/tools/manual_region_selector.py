"""
Utility overlay that lets the user drag a rectangle on screen and returns the
selected region (left, top, width, height). Designed to be launched from the
Auto Maple GUI for manual capture workflows.
"""

from __future__ import annotations

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
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.attributes("-alpha", 0.15)
    root.configure(bg="black")
    root.attributes("-topmost", True)
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
    root.mainloop()

    return result or None


if __name__ == "__main__":
    region = select_region()
    if region:
        print(json.dumps(region))
    else:
        print("")
