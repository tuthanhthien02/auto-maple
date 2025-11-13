import tkinter as tk
from src.gui.interfaces import LabelFrame
from src.common import config


class Routine(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Routine', **kwargs)
        
        # Get view_instance from kwargs if provided (for scrollbar support)
        self.view_instance = kwargs.pop('view_instance', None)
        if self.view_instance is None:
            # Fallback: try to get from parent chain
            self.view_instance = parent

        self.scroll = tk.Scrollbar(self)
        self.scroll.pack(side=tk.RIGHT, fill='both', pady=5)

        self.listbox = tk.Listbox(self, width=25,
                                  listvariable=config.gui.routine_var,
                                  exportselection=False,
                                  activestyle='none',
                                  yscrollcommand=self.scroll.set)
        self.listbox.bind('<Up>', lambda e: 'break')
        self.listbox.bind('<Down>', lambda e: 'break')
        self.listbox.bind('<Left>', lambda e: 'break')
        self.listbox.bind('<Right>', lambda e: 'break')
        # Use view_instance to access details
        if hasattr(self.view_instance, 'details'):
            self.listbox.bind('<<ListboxSelect>>', self.view_instance.details.show_details)
        self.listbox.pack(side=tk.LEFT, expand=True, fill='both', padx=(5, 0), pady=5)

        self.scroll.config(command=self.listbox.yview)

    def select(self, i):
        self.listbox.selection_clear(0, 'end')
        self.listbox.selection_set(i)
        self.listbox.see(i)
