import tkinter as tk
from src.common import config
from src.gui.interfaces import Frame


class Controls(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        
        # Get edit_instance from parent or config.gui
        if hasattr(parent, 'edit_instance'):
            self.edit_instance = parent.edit_instance
        elif hasattr(config, 'gui') and hasattr(config.gui, 'edit'):
            self.edit_instance = config.gui.edit
        else:
            self.edit_instance = parent

        self.up_arrow = tk.Button(self, text='▲', width=6, command=self.move('up'))
        self.up_arrow.grid(row=0, column=0)

        self.down_arrow = tk.Button(self, text='▼', width=6, command=self.move('down'))
        self.down_arrow.grid(row=0, column=1, padx=(5, 0))

        self.delete = tk.Button(self, text='\U00002715', width=3, command=self.delete)
        self.delete.grid(row=0, column=2, padx=(5, 0))

        self.new = tk.Button(self, text='\U00002795', width=6, command=self.new)
        self.new.grid(row=0, column=3, padx=(5, 0))

    def move(self, direction):
        """
        Returns a Button callback that moves the currently selected Component
        in the given DIRECTION.
        """

        assert direction in {'up', 'down'}, f"'{direction}' is an invalid direction."

        def callback():
            # Use edit_instance to access Edit tab attributes
            if self.edit_instance and hasattr(self.edit_instance, 'routine'):
                routine = self.edit_instance.routine
                edit = self.edit_instance
            else:
                # Fallback to parent chain
                routine = self.parent
                edit = self.parent.parent
            
            components = routine.components.listbox.curselection()
            commands = routine.commands.listbox.curselection()
            if len(components) > 0:
                p_index = int(components[0])
                if len(commands) > 0:
                    point = config.routine[p_index]
                    c_index = int(commands[0])
                    if direction == 'up':
                        new_index = config.routine.move_command_up(p_index, c_index)
                    else:
                        new_index = config.routine.move_command_down(p_index, c_index)

                    if new_index != c_index:
                        commands = edit.routine.commands
                        commands.update_display()
                        commands.select(new_index)
                        edit.editor.create_edit_ui(point.commands, new_index,
                                                   commands.update_obj)
                else:
                    if direction == 'up':
                        new_index = config.routine.move_component_up(p_index)
                    else:
                        new_index = config.routine.move_component_down(p_index)

                    if new_index != p_index:
                        components = edit.routine.components
                        components.select(new_index)
                        edit.editor.create_edit_ui(config.routine.sequence, new_index,
                                                   components.update_obj)
        return callback

    def delete(self):
        # Use edit_instance to access Edit tab attributes
        if self.edit_instance and hasattr(self.edit_instance, 'routine'):
            routine = self.edit_instance.routine
            edit = self.edit_instance
        else:
            # Fallback to parent chain
            routine = self.parent
            edit = self.parent.parent
        
        components = routine.components.listbox.curselection()
        commands = routine.commands.listbox.curselection()
        if len(components) > 0:
            p_index = int(components[0])
            if len(commands) > 0:
                c_index = int(commands[0])
                config.routine.delete_command(p_index, c_index)

                edit.routine.commands.update_display()
                edit.routine.commands.clear_selection()
                edit.editor.create_edit_ui(config.routine.sequence, p_index,
                                           edit.routine.components.update_obj)
            else:
                config.routine.delete_component(p_index)

                edit.minimap.redraw()
                edit.routine.components.clear_selection()
                edit.routine.commands_var.set([])
                edit.editor.reset()

    def new(self):
        # Use edit_instance to access Edit tab attributes
        if self.edit_instance and hasattr(self.edit_instance, 'editor'):
            edit = self.edit_instance
        else:
            # Fallback to parent chain
            edit = self.parent.parent
        edit.editor.create_add_prompt()
