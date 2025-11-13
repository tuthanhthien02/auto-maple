import os
import tkinter as tk
from src.common import config, utils
from src.gui.interfaces import MenuBarItem
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesno


class File(MenuBarItem):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, 'File', **kwargs)
        # parent.add_cascade(label='File', menu=self)

        self.add_command(
            label='New Routine',
            command=utils.async_callback(self, File._new_routine),
            state=tk.DISABLED
        )
        self.add_command(
            label='Save Routine',
            command=utils.async_callback(self, File._save_routine),
            state=tk.DISABLED
        )
        self.add_separator()
        self.add_command(label='Load Command Book', command=utils.async_callback(self, File._load_commands))
        self.add_command(
            label='Load Routine',
            command=utils.async_callback(self, File._load_routine),
            state=tk.DISABLED
        )

    def enable_routine_state(self):
        self.entryconfig('New Routine', state=tk.NORMAL)
        self.entryconfig('Save Routine', state=tk.NORMAL)
        self.entryconfig('Load Routine', state=tk.NORMAL)

    @staticmethod
    @utils.run_if_disabled('\n[!] Cannot create a new routine while Auto Maple is enabled')
    def _new_routine():
        if config.routine.dirty:
            if not askyesno(title='New Routine',
                            message='The current routine has unsaved changes. '
                                    'Would you like to proceed anyways?',
                            icon='warning'):
                return
        config.routine.clear()

    @staticmethod
    @utils.run_if_disabled('\n[!] Cannot save routines while Auto Maple is enabled')
    def _save_routine():
        file_path = asksaveasfilename(initialdir=get_routines_dir(),
                                      title='Save routine',
                                      filetypes=[('*.csv', '*.csv')],
                                      defaultextension='*.csv')
        if file_path:
            config.routine.save(file_path)

    @staticmethod
    @utils.run_if_disabled('\n[!] Cannot load routines while Auto Maple is enabled')
    def _load_routine():
        try:
            # Check if routine is initialized
            if not hasattr(config, 'routine') or config.routine is None:
                from tkinter.messagebox import showerror
                showerror(title='Error', message='Routine not initialized. Please restart the application.')
                return
            
            if config.routine.dirty:
                if not askyesno(title='Load Routine',
                                message='The current routine has unsaved changes. '
                                        'Would you like to proceed anyways?',
                                icon='warning'):
                    return
            file_path = askopenfilename(initialdir=get_routines_dir(),
                                        title='Select a routine',
                                        filetypes=[('*.csv', '*.csv')])
            if file_path:
                try:
                    config.routine.load(file_path)
                except Exception as e:
                    from tkinter.messagebox import showerror
                    import traceback
                    error_msg = f"Failed to load routine:\n{str(e)}\n\n{traceback.format_exc()}"
                    showerror(title='Load Routine Error', message=error_msg)
                    from src.common.logger import get_logger
                    log = get_logger(__name__)
                    log.error(f"Error loading routine: {e}")
                    log.error(traceback.format_exc())
        except Exception as e:
            from tkinter.messagebox import showerror
            import traceback
            error_msg = f"Unexpected error in Load Routine:\n{str(e)}\n\n{traceback.format_exc()}"
            showerror(title='Error', message=error_msg)
            from src.common.logger import get_logger
            log = get_logger(__name__)
            log.error(f"Unexpected error in _load_routine: {e}")
            log.error(traceback.format_exc())

    @staticmethod
    @utils.run_if_disabled('\n[!] Cannot load command books while Auto Maple is enabled')
    def _load_commands():
        if config.routine.dirty:
            if not askyesno(title='Load Command Book',
                            message='Loading a new command book will discard the current routine, '
                                    'which has unsaved changes. Would you like to proceed anyways?',
                            icon='warning'):
                return
        file_path = askopenfilename(initialdir=os.path.join(config.RESOURCES_DIR, 'command_books'),
                                    title='Select a command book',
                                    filetypes=[('*.py', '*.py')])
        if file_path:
            config.bot.load_commands(file_path)


def get_routines_dir():
    """Get routines directory for current command book"""
    try:
        if not hasattr(config, 'bot') or config.bot is None:
            # Fallback to default directory if bot not initialized
            target = os.path.join(config.RESOURCES_DIR, 'routines')
        elif not hasattr(config.bot, 'command_book') or config.bot.command_book is None:
            # Fallback to default directory if command book not loaded
            target = os.path.join(config.RESOURCES_DIR, 'routines')
        else:
            target = os.path.join(config.RESOURCES_DIR, 'routines', config.bot.command_book.name)
        
        if not os.path.exists(target):
            os.makedirs(target)
        return target
    except Exception as e:
        # Fallback to resources/routines if anything fails
        target = os.path.join(config.RESOURCES_DIR, 'routines')
        if not os.path.exists(target):
            try:
                os.makedirs(target)
            except Exception:
                pass
        return target
