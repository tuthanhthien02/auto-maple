import tkinter as tk
from src.gui.interfaces import LabelFrame
from src.common import config


class Status(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'Status', **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        self.curr_cb = tk.StringVar()
        self.curr_routine = tk.StringVar()

        self.cb_label = tk.Label(self, text='Command Book:')
        self.cb_label.grid(row=0, column=1, padx=5, pady=(5, 0), sticky=tk.E)
        self.cb_entry = tk.Entry(self, textvariable=self.curr_cb, state=tk.DISABLED)
        self.cb_entry.grid(row=0, column=2, padx=(0, 5), pady=(5, 0), sticky=tk.EW)

        self.r_label = tk.Label(self, text='Routine:')
        self.r_label.grid(row=1, column=1, padx=5, pady=(0, 5), sticky=tk.E)
        self.r_entry = tk.Entry(self, textvariable=self.curr_routine, state=tk.DISABLED)
        self.r_entry.grid(row=1, column=2, padx=(0, 5), pady=(0, 5), sticky=tk.EW)

        # Recalibrate Minimap button
        self.recalibrate_btn = tk.Button(
            self,
            text='📍 Recalibrate Minimap',
            command=self._on_recalibrate_click,
            bg='#4CAF50',
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            relief=tk.RAISED,
            bd=2,
            cursor='hand2'
        )
        self.recalibrate_btn.grid(row=2, column=1, columnspan=2, padx=5, pady=(5, 5), sticky=tk.EW)
        
        # Status label for recalibration feedback
        self.recalibrate_status = tk.Label(
            self,
            text='',
            fg='green',
            font=('Arial', 8)
        )
        self.recalibrate_status.grid(row=3, column=1, columnspan=2, padx=5, pady=(0, 5))

    def set_cb(self, string):
        self.curr_cb.set(string)

    def set_routine(self, string):
        self.curr_routine.set(string)
    
    def _on_recalibrate_click(self):
        """Handle recalibrate minimap button click."""
        if not hasattr(config, 'capture') or config.capture is None:
            self.recalibrate_status.config(text='❌ Capture module not available', fg='red')
            self.after(3000, lambda: self.recalibrate_status.config(text=''))
            return
        
        if not config.capture.ready:
            self.recalibrate_status.config(text='⏳ Capture module not ready yet', fg='orange')
            self.after(3000, lambda: self.recalibrate_status.config(text=''))
            return
        
        # Disable button during recalibration
        self.recalibrate_btn.config(state=tk.DISABLED, text='⏳ Recalibrating...')
        self.recalibrate_status.config(text='🔄 Recalibrating minimap location...', fg='blue')
        
        # Request recalibration
        success = config.capture.recalibrate_minimap()
        
        if success:
            # Update status after a delay
            self.after(2000, lambda: self.recalibrate_status.config(
                text='✅ Recalibration started. Please wait...', fg='green'
            ))
            # Re-enable button after 5 seconds
            self.after(5000, self._recalibrate_complete)
        else:
            self.recalibrate_btn.config(state=tk.NORMAL, text='📍 Recalibrate Minimap')
            self.recalibrate_status.config(text='❌ Failed to start recalibration', fg='red')
            self.after(3000, lambda: self.recalibrate_status.config(text=''))
    
    def _recalibrate_complete(self):
        """Re-enable button after recalibration completes."""
        self.recalibrate_btn.config(state=tk.NORMAL, text='📍 Recalibrate Minimap')
        if hasattr(config, 'capture') and config.capture and config.capture.calibrated:
            self.recalibrate_status.config(text='✅ Recalibration complete!', fg='green')
            self.after(3000, lambda: self.recalibrate_status.config(text=''))
        else:
            self.recalibrate_status.config(text='⏳ Still calibrating...', fg='orange')
            # Check again after 2 seconds
            self.after(2000, self._recalibrate_complete)
