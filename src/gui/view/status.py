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

        # Dynamic Paths Status
        self.dynamic_paths_label = tk.Label(self, text='Dynamic Paths:')
        self.dynamic_paths_label.grid(row=2, column=1, padx=5, pady=(0, 5), sticky=tk.E)
        self.dynamic_paths_var = tk.StringVar(value='Disabled')
        self.dynamic_paths_entry = tk.Entry(self, textvariable=self.dynamic_paths_var, state=tk.DISABLED, width=30)
        self.dynamic_paths_entry.grid(row=2, column=2, padx=(0, 5), pady=(0, 5), sticky=tk.EW)

        # Command Sequence Status
        self.command_sequence_label = tk.Label(self, text='Command Sequence:')
        self.command_sequence_label.grid(row=3, column=1, padx=5, pady=(0, 5), sticky=tk.E)
        self.command_sequence_var = tk.StringVar(value='Disabled')
        self.command_sequence_entry = tk.Entry(self, textvariable=self.command_sequence_var, state=tk.DISABLED, width=30)
        self.command_sequence_entry.grid(row=3, column=2, padx=(0, 5), pady=(0, 5), sticky=tk.EW)

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
        self.recalibrate_btn.grid(row=4, column=1, columnspan=2, padx=5, pady=(5, 5), sticky=tk.EW)
        
        # Status label for recalibration feedback
        self.recalibrate_status = tk.Label(
            self,
            text='',
            fg='green',
            font=('Arial', 8)
        )
        self.recalibrate_status.grid(row=5, column=1, columnspan=2, padx=5, pady=(0, 5))

    def set_cb(self, string):
        self.curr_cb.set(string)

    def set_routine(self, string):
        self.curr_routine.set(string)
    
    def update_dynamic_paths_status(self):
        """Update Dynamic Paths status display."""
        try:
            if not hasattr(config, 'routine') or config.routine is None:
                self.dynamic_paths_var.set('No routine loaded')
                return
            
            routine = config.routine
            if not routine.dynamic_paths_enabled:
                self.dynamic_paths_var.set('Disabled')
                return
            
            if not routine.dynamic_paths or not routine.current_path_id:
                self.dynamic_paths_var.set('Enabled (no paths)')
                return
            
            # Get current path info
            current_path = next((p for p in routine.dynamic_paths if p['id'] == routine.current_path_id), None)
            if not current_path:
                self.dynamic_paths_var.set(f'Enabled ({routine.current_path_id} - not found)')
                return
            
            # Build status string
            path_count = len(routine.dynamic_paths)
            current_path_points = len(current_path['indices'])
            switch_info = f"{routine.path_switch_counter}/{routine.path_switch_interval}"
            loops_remaining = routine.path_switch_interval - routine.path_switch_counter
            
            status = f"{routine.current_path_id} ({current_path_points} pts) | {switch_info} loops | {loops_remaining} remaining"
            self.dynamic_paths_var.set(status)
        except Exception as e:
            # Silently handle errors to avoid spamming
            pass
    
    def update_command_sequence_status(self):
        """Update Command Sequence status display."""
        try:
            if not hasattr(config, 'routine') or config.routine is None:
                self.command_sequence_var.set('No routine loaded')
                return
            
            routine = config.routine
            cmd_cfg = routine.command_randomization
            
            if not cmd_cfg.get('enabled', False):
                self.command_sequence_var.set('Disabled')
                return
            
            # Get statistics
            stats = routine.command_sequence_stats
            shuffle_prob = cmd_cfg.get('shuffle_probability', 0.0) * 100
            skip_prob = cmd_cfg.get('skip_probability', 0.0) * 100
            wait_prob = cmd_cfg.get('extra_wait_probability', 0.0) * 100
            
            # Build status string
            status_parts = []
            if shuffle_prob > 0:
                status_parts.append(f"Shuffle: {shuffle_prob:.0f}%")
            if skip_prob > 0:
                status_parts.append(f"Skip: {skip_prob:.0f}%")
            if wait_prob > 0:
                status_parts.append(f"Wait: {wait_prob:.0f}%")
            
            if stats['total_shuffles'] > 0 or stats['total_skips'] > 0 or stats['total_extra_waits'] > 0:
                stats_str = f" | Stats: {stats['total_shuffles']}S/{stats['total_skips']}K/{stats['total_extra_waits']}W"
                status_parts.append(stats_str)
            
            status = ' | '.join(status_parts) if status_parts else 'Enabled (no activity)'
            self.command_sequence_var.set(status)
        except Exception as e:
            # Silently handle errors to avoid spamming
            pass
    
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
