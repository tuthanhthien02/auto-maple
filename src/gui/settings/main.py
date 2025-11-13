"""Displays Auto Maple's current settings and allows the user to edit them."""

import tkinter as tk
from src.gui.interfaces import KeyBindings
from src.gui.settings.pets import Pets
from src.gui.settings.routine_randomization import RoutineRandomization
from src.gui.settings.vmware_receiver import VMwareReceiver
from src.gui.interfaces import Tab, Frame
from src.common import config


class Settings(Tab):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "Settings", **kwargs)

        # Create scrollable frame
        self._create_scrollable_frame()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

        self.column1 = Frame(self._scroll_content)
        self.column1.grid(row=0, column=1, sticky=tk.N, padx=10, pady=10)

        self.controls = KeyBindings(
            self.column1, "Auto Maple Controls", config.listener
        )
        self.controls.pack(side=tk.TOP, fill="x", expand=True)
        self.common_bindings = KeyBindings(
            self.column1, "In-game Keybindings", config.bot
        )
        self.common_bindings.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))
        self.pets = Pets(self.column1)
        self.pets.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))
        self.routine_randomization = RoutineRandomization(self.column1)
        self.routine_randomization.pack(
            side=tk.TOP, fill="x", expand=True, pady=(10, 0)
        )
        self.vmware_receiver = VMwareReceiver(self.column1)
        self.vmware_receiver.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))

        self.column2 = Frame(self._scroll_content)
        self.column2.grid(row=0, column=2, sticky=tk.N, padx=10, pady=10)
        self.class_bindings = KeyBindings(
            self.column2, "No Command Book Selected", None
        )
        self.class_bindings.pack(side=tk.TOP, fill="x", expand=True)

    def _create_scrollable_frame(self):
        """Create a scrollable container for Settings content"""
        # Create canvas and scrollbar
        self._canvas = tk.Canvas(self, highlightthickness=0)
        self._scrollbar = tk.Scrollbar(
            self, orient="vertical", command=self._canvas.yview
        )
        self._scroll_content = Frame(self._canvas)

        # Configure scroll region
        self._scroll_content.bind(
            "<Configure>",
            lambda e: self._canvas.configure(scrollregion=self._canvas.bbox("all")),
        )

        # Create window in canvas
        self._canvas_window = self._canvas.create_window(
            (0, 0), window=self._scroll_content, anchor="nw"
        )

        # Configure canvas scrolling
        self._canvas.configure(yscrollcommand=self._scrollbar.set)

        # Pack canvas and scrollbar
        self._canvas.pack(side="left", fill="both", expand=True)
        self._scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel to canvas
        def _on_mousewheel(event):
            """Handle mouse wheel scrolling"""
            # Windows: event.delta is typically 120 or -120
            # Linux: event.num is 4 (scroll up) or 5 (scroll down)
            if event.num == 4 or (hasattr(event, "delta") and event.delta > 0):
                self._canvas.yview_scroll(-1, "units")
            elif event.num == 5 or (hasattr(event, "delta") and event.delta < 0):
                self._canvas.yview_scroll(1, "units")

        # Bind mouse wheel events
        # Windows uses <MouseWheel>
        self._canvas.bind("<MouseWheel>", _on_mousewheel)
        # Linux uses <Button-4> and <Button-5>
        self._canvas.bind("<Button-4>", _on_mousewheel)
        self._canvas.bind("<Button-5>", _on_mousewheel)

        # Also bind to parent to ensure scrolling works even when hovering over canvas
        self.bind(
            "<MouseWheel>",
            lambda e: (
                _on_mousewheel(e)
                if self._canvas.winfo_containing(e.x_root, e.y_root)
                else None
            ),
        )

        # Update canvas width when window resizes
        self._canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_canvas_configure(self, event):
        """Update canvas window width when canvas is resized"""
        canvas_width = event.width
        self._canvas.itemconfig(self._canvas_window, width=canvas_width)

    def update_class_bindings(self):
        self.class_bindings.destroy()
        class_name = config.bot.command_book.name.capitalize()
        self.class_bindings = KeyBindings(
            self.column2, f"{class_name} Keybindings", config.bot.command_book
        )
        self.class_bindings.pack(side=tk.TOP, fill="x", expand=True)
