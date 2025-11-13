import tkinter as tk

from src.common import config
from src.routine.components import Point
from src.gui.interfaces import Frame


class Commands(Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # Get edit_instance from parent or config.gui
        if hasattr(parent, "edit_instance"):
            self.edit_instance = parent.edit_instance
        elif hasattr(config, "gui") and hasattr(config.gui, "edit"):
            self.edit_instance = config.gui.edit
        else:
            self.edit_instance = parent

        self.label = tk.Label(self, text="Commands")
        self.label.pack(fill="x", padx=5)

        self.scroll = tk.Scrollbar(self)
        self.scroll.pack(side=tk.RIGHT, fill="y", pady=(0, 5))

        # Get commands_var from routine or parent chain
        if hasattr(self.edit_instance, "routine"):
            commands_var = self.edit_instance.routine.commands_var
        else:
            commands_var = parent.parent.commands_var

        self.listbox = tk.Listbox(
            self,
            width=25,
            listvariable=commands_var,
            exportselection=False,
            activestyle="none",
            yscrollcommand=self.scroll.set,
        )
        self.listbox.bind("<Up>", lambda e: "break")
        self.listbox.bind("<Down>", lambda e: "break")
        self.listbox.bind("<Left>", lambda e: "break")
        self.listbox.bind("<Right>", lambda e: "break")
        self.bind_select()
        self.listbox.pack(
            side=tk.LEFT, expand=True, fill="both", padx=(5, 0), pady=(0, 5)
        )

        self.scroll.config(command=self.listbox.yview)

    def bind_select(self):
        self.listbox.bind("<<ListboxSelect>>", self.on_select)

    def unbind_select(self):
        self.listbox.bind("<<ListboxSelect>>", lambda e: "break")

    def on_select(self, e):
        # Use edit_instance to access Edit tab attributes
        if self.edit_instance and hasattr(self.edit_instance, "routine"):
            routine = self.edit_instance.routine
            edit = self.edit_instance
        else:
            # Fallback to parent chain
            routine = self.parent.parent
            edit = routine.parent

        selections = e.widget.curselection()
        pt_selects = routine.components.listbox.curselection()
        if len(selections) > 0 and len(pt_selects) > 0:
            c_index = int(selections[0])
            pt_index = int(pt_selects[0])
            edit.editor.create_edit_ui(
                config.routine[pt_index].commands, c_index, self.update_obj
            )
        else:
            edit.editor.reset()

    def update_obj(self, arr, i, stringvars):
        def f():
            # Use edit_instance to access Edit tab attributes
            if self.edit_instance and hasattr(self.edit_instance, "routine"):
                routine = self.edit_instance.routine
                edit = self.edit_instance
            else:
                # Fallback to parent chain
                routine = self.parent.parent
                edit = self.parent.parent.parent

            pt_selects = routine.components.listbox.curselection()
            if len(pt_selects) > 0:
                index = int(pt_selects[0])
                new_kwargs = {k: v.get() for k, v in stringvars.items()}
                config.routine.update_command(index, i, new_kwargs)
            edit.editor.create_edit_ui(arr, i, self.update_obj)

        return f

    def update_display(self):
        # Use edit_instance to access Edit tab attributes
        if self.edit_instance and hasattr(self.edit_instance, "routine"):
            routine = self.edit_instance.routine
            commands_var = routine.commands_var
        else:
            # Fallback to parent chain
            routine = self.parent.parent
            commands_var = routine.commands_var

        pt_selects = routine.components.listbox.curselection()
        if len(pt_selects) > 0:
            index = int(pt_selects[0])
            obj = config.routine[index]
            if isinstance(obj, Point):
                commands_var.set([c.id for c in obj.commands])
            else:
                commands_var.set([])
        else:
            commands_var.set([])

    def clear_selection(self):
        self.listbox.selection_clear(0, "end")

    def clear_contents(self):
        # Use edit_instance to access Edit tab attributes
        if self.edit_instance and hasattr(self.edit_instance, "routine"):
            commands_var = self.edit_instance.routine.commands_var
        else:
            # Fallback to parent chain
            commands_var = self.parent.parent.commands_var
        commands_var.set([])

    def select(self, i):
        self.listbox.selection_clear(0, "end")
        self.listbox.selection_set(i)
        self.listbox.see(i)
