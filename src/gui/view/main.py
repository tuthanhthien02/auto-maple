"""Displays the current minimap as well as various information regarding the current routine."""

import tkinter as tk
from src.gui.view.details import Details
from src.gui.view.minimap import Minimap
from src.gui.view.routine import Routine
from src.gui.view.status import Status
from src.gui.interfaces import Tab, Frame


class View(Tab):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'View', **kwargs)

        # Create scrollable frame
        self._create_scrollable_frame()

        self._scroll_content.grid_columnconfigure(0, weight=1)
        self._scroll_content.grid_columnconfigure(3, weight=1)

        self.minimap = Minimap(self._scroll_content)
        self.minimap.grid(row=0, column=2, sticky=tk.NSEW, padx=10, pady=10)

        self.status = Status(self._scroll_content)
        self.status.grid(row=1, column=2, sticky=tk.NSEW, padx=10, pady=10)

        self.details = Details(self._scroll_content)
        self.details.grid(row=2, column=2, sticky=tk.NSEW, padx=10, pady=10)

        # Store reference to View instance in scroll_content for widgets to access
        self._scroll_content.view_instance = self
        
        self.routine = Routine(self._scroll_content)
        self.routine.grid(row=0, column=1, rowspan=3, sticky=tk.NSEW, padx=10, pady=10)
    
    def _create_scrollable_frame(self):
        """Create a scrollable container for View content"""
        # Create canvas and scrollbar
        self._canvas = tk.Canvas(self, highlightthickness=0)
        self._scrollbar = tk.Scrollbar(self, orient="vertical", command=self._canvas.yview)
        self._scroll_content = Frame(self._canvas)
        
        # Configure scroll region
        self._scroll_content.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        )
        
        # Create window in canvas
        self._canvas_window = self._canvas.create_window((0, 0), window=self._scroll_content, anchor="nw")
        
        # Configure canvas scrolling
        self._canvas.configure(yscrollcommand=self._scrollbar.set)
        
        # Pack canvas and scrollbar
        self._canvas.pack(side="left", fill="both", expand=True)
        self._scrollbar.pack(side="right", fill="y")
        
        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            """Handle mouse wheel scrolling"""
            if event.num == 4 or (hasattr(event, 'delta') and event.delta > 0):
                self._canvas.yview_scroll(-1, "units")
            elif event.num == 5 or (hasattr(event, 'delta') and event.delta < 0):
                self._canvas.yview_scroll(1, "units")
        
        self._canvas.bind("<MouseWheel>", _on_mousewheel)
        self._canvas.bind("<Button-4>", _on_mousewheel)
        self._canvas.bind("<Button-5>", _on_mousewheel)
        
        # Update canvas width when window resizes
        self._canvas.bind('<Configure>', self._on_canvas_configure)
    
    def _on_canvas_configure(self, event):
        """Update canvas window width when canvas is resized"""
        canvas_width = event.width
        self._canvas.itemconfig(self._canvas_window, width=canvas_width)
