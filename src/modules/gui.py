"""User friendly GUI to interact with Auto Maple."""

import time
import threading
import tkinter as tk
from tkinter import ttk
from src.common import config, settings
from src.gui import Menu, View, Edit, Settings
import os


class GUI:
    # CPU Optimization: Reduced from 30 FPS to 10 FPS (sufficient for GUI, human eye can't distinguish >15 FPS)
    DISPLAY_FRAME_RATE = 10
    RESOLUTIONS = {
        'DEFAULT': '800x900',
        'Edit': '1400x800',
        'View': '1400x800'
    }

    def __init__(self):
        config.gui = self

        self.root = tk.Tk()
        self.root.title('Explorer Settings')
        # Thiết lập icon cửa sổ: stealth thành Explorer Settings
        icon_path = os.path.join('assets', 'explorer-icon.ico')
        if os.path.exists(icon_path):
            try:
                self.root.iconbitmap(icon_path)
            except Exception:
                pass
        self.root.geometry(GUI.RESOLUTIONS['DEFAULT'])
        self.root.resizable(False, False)

        # Initialize GUI variables
        self.routine_var = tk.StringVar()

        # Build the GUI
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)

        self.navigation = ttk.Notebook(self.root)

        self.view = View(self.navigation)
        self.edit = Edit(self.navigation)
        self.settings = Settings(self.navigation)

        self.navigation.pack(expand=True, fill='both')
        self.navigation.bind('<<NotebookTabChanged>>', self._resize_window)
        self.root.focus()

    def set_routine(self, arr):
        self.routine_var.set(arr)

    def clear_routine_info(self):
        """
        Clears information in various GUI elements regarding the current routine.
        Does not clear Listboxes containing routine Components, as that is handled by Routine.
        """

        self.view.details.clear_info()
        self.view.status.set_routine('')

        self.edit.minimap.redraw()
        self.edit.routine.commands.clear_contents()
        self.edit.routine.commands.update_display()
        self.edit.editor.reset()

    def _resize_window(self, e):
        """Callback to resize entire Tkinter window every time a new Page is selected."""

        nav = e.widget
        curr_id = nav.select()
        nav.nametowidget(curr_id).focus()      # Focus the current Tab
        page = nav.tab(curr_id, 'text')
        if self.root.state() != 'zoomed':
            if page in GUI.RESOLUTIONS:
                self.root.geometry(GUI.RESOLUTIONS[page])
            else:
                self.root.geometry(GUI.RESOLUTIONS['DEFAULT'])

    def start(self):
        """Starts the GUI as well as any scheduled functions."""

        display_thread = threading.Thread(target=self._display_minimap)
        display_thread.daemon = True
        display_thread.start()

        layout_thread = threading.Thread(target=self._save_layout)
        layout_thread.daemon = True
        layout_thread.start()
        
        # Refresh VMware Receiver status periodically
        vmware_status_thread = threading.Thread(target=self._refresh_vmware_status)
        vmware_status_thread.daemon = True
        vmware_status_thread.start()
        
        # Refresh Dynamic Paths status periodically
        dynamic_paths_status_thread = threading.Thread(target=self._refresh_dynamic_paths_status)
        dynamic_paths_status_thread.daemon = True
        dynamic_paths_status_thread.start()
        
        # Refresh Command Sequence status periodically
        command_sequence_status_thread = threading.Thread(target=self._refresh_command_sequence_status)
        command_sequence_status_thread.daemon = True
        command_sequence_status_thread.start()
        
        # Refresh Input Method status periodically
        input_method_status_thread = threading.Thread(target=self._refresh_input_method_status)
        input_method_status_thread.daemon = True
        input_method_status_thread.start()

        self.root.mainloop()
    
    def _refresh_vmware_status(self):
        """Periodically refresh VMware Receiver status in GUI"""
        import time
        while True:
            try:
                # Refresh status every 2 seconds
                time.sleep(2.0)
                if hasattr(config, 'gui') and config.gui:
                    if hasattr(config.gui, 'settings') and config.gui.settings:
                        if hasattr(config.gui.settings, 'vmware_receiver') and config.gui.settings.vmware_receiver:
                            try:
                                config.gui.settings.vmware_receiver.refresh_status()
                            except Exception as e:
                                # Ignore errors during refresh (widget might be destroyed)
                                pass
            except Exception as e:
                # Silently ignore errors to avoid spamming logs
                pass
    
    def _refresh_dynamic_paths_status(self):
        """Periodically refresh Dynamic Paths status in GUI"""
        import time
        while True:
            try:
                # Refresh status every 1 second (more frequent for better UX)
                time.sleep(1.0)
                if hasattr(config, 'gui') and config.gui:
                    if hasattr(config.gui, 'view') and config.gui.view:
                        if hasattr(config.gui.view, 'status') and config.gui.view.status:
                            try:
                                config.gui.view.status.update_dynamic_paths_status()
                            except Exception as e:
                                # Ignore errors during refresh (widget might be destroyed)
                                pass
            except Exception as e:
                # Silently ignore errors to avoid spamming logs
                pass
    
    def _refresh_command_sequence_status(self):
        """Periodically refresh Command Sequence status in GUI"""
        import time
        while True:
            try:
                # Refresh status every 1 second
                time.sleep(1.0)
                if hasattr(config, 'gui') and config.gui:
                    if hasattr(config.gui, 'view') and config.gui.view:
                        if hasattr(config.gui.view, 'status') and config.gui.view.status:
                            try:
                                config.gui.view.status.update_command_sequence_status()
                            except Exception as e:
                                # Ignore errors during refresh (widget might be destroyed)
                                pass
            except Exception as e:
                # Silently ignore errors to avoid spamming logs
                pass
    
    def _refresh_input_method_status(self):
        """Periodically refresh Input Method status in GUI"""
        import time
        while True:
            try:
                # Refresh status every 2 seconds (less frequent since it doesn't change often)
                time.sleep(2.0)
                if hasattr(config, 'gui') and config.gui:
                    if hasattr(config.gui, 'view') and config.gui.view:
                        if hasattr(config.gui.view, 'status') and config.gui.view.status:
                            try:
                                config.gui.view.status.update_input_method_status()
                            except Exception as e:
                                # Ignore errors during refresh (widget might be destroyed)
                                pass
            except Exception as e:
                # Silently ignore errors to avoid spamming logs
                pass

    def _display_minimap(self):
        """Display minimap in loop with exception handling"""
        delay = 1 / GUI.DISPLAY_FRAME_RATE
        while True:
            try:
                self.view.minimap.display_minimap()
                time.sleep(delay)
            except Exception as e:
                from src.common.logger import get_logger
                log = get_logger(__name__)
                log.error(f"[GUI] Error in _display_minimap: {e}")
                import traceback
                log.error(traceback.format_exc())
                time.sleep(1)  # Wait before retrying

    def _save_layout(self):
        """Periodically saves the current Layout object with exception handling"""
        while True:
            try:
                if config.layout is not None and settings.record_layout:
                    config.layout.save()
                time.sleep(5)
            except Exception as e:
                from src.common.logger import get_logger
                log = get_logger(__name__)
                log.error(f"[GUI] Error in _save_layout: {e}")
                import traceback
                log.error(traceback.format_exc())
                time.sleep(5)  # Wait before retrying


if __name__ == '__main__':
    gui = GUI()
    gui.start()
