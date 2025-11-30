"""Displays Auto Maple's current settings and allows the user to edit them."""

import tkinter as tk
from tkinter import messagebox

from src.common import config
from src.common import vkeys
from src.common.logger import get_logger
from src.gui.interfaces import Frame, KeyBindings, LabelFrame, Tab
from src.gui.settings.routine_randomization import RoutineRandomization
from src.gui.settings.vmware_receiver import VMwareReceiver

log = get_logger(__name__)


class Settings(Tab):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "Settings", **kwargs)

        # Create scrollable frame
        self._create_scrollable_frame()

        self.columnconfigure(0, weight=1)
        self.columnconfigure(3, weight=1)

        self.column1 = Frame(self._scroll_content)
        self.column1.grid(row=0, column=1, sticky=tk.N, padx=10, pady=10)

        # Priority sections on top
        self.routine_randomization = RoutineRandomization(self.column1)
        self.routine_randomization.pack(side=tk.TOP, fill="x", expand=True)
        self.vmware_receiver = VMwareReceiver(self.column1)
        self.vmware_receiver.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))

        # AI Lie Detector Solvers
        self.ai_solver_settings = LabelFrame(
            self.column1, "AI Lie Detector Solvers", padding=(5, 5, 5, 5)
        )
        self.ai_solver_settings.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))
        self._build_ai_solver_section()

        self.key_output_settings = LabelFrame(
            self.column1, "Key Output", padding=(5, 5, 5, 5)
        )
        self.key_output_settings.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))
        self._build_key_output_section()

        self.mirror_settings = LabelFrame(
            self.column1, "Mirror Input (Hardware Forwarding)", padding=(5, 5, 5, 5)
        )
        self.mirror_settings.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))
        self._build_mirror_section()

        self.listener_settings = LabelFrame(
            self.column1, "Keyboard Listener", padding=(5, 5, 5, 5)
        )
        self.listener_settings.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))
        self.listener_toggle_var = tk.BooleanVar(
            value=getattr(config, "enable_keyboard_listener", True)
        )
        self.listener_toggle = tk.Checkbutton(
            self.listener_settings,
            text="Bật hook bàn phím (Insert / F6 / F7)",
            variable=self.listener_toggle_var,
            command=self._on_listener_toggle,
            anchor="w",
            justify=tk.LEFT,
        )
        self.listener_toggle.pack(side=tk.TOP, anchor="w")
        self.listener_hint = tk.Label(
            self.listener_settings,
            text="Tắt hook để hạn chế detection. Khi tắt, sử dụng nút 'Toggle Bot' ở tab View.",
            wraplength=260,
            justify=tk.LEFT,
            fg="gray",
        )
        self.listener_hint.pack(side=tk.TOP, fill="x", pady=(4, 0))

        self.record_settings = LabelFrame(
            self.column1, "Record Position", padding=(5, 5, 5, 5)
        )
        self.record_settings.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))
        self.record_live_var = tk.BooleanVar(
            value=getattr(config, "record_position_live_update", False)
        )
        self.record_live_checkbox = tk.Checkbutton(
            self.record_settings,
            text="Bật cập nhật vị trí khi record (tăng CPU)",
            variable=self.record_live_var,
            command=self._on_record_live_toggle,
            anchor="w",
            justify=tk.LEFT,
            wraplength=260,
        )
        self.record_live_checkbox.pack(side=tk.TOP, anchor="w")
        self.record_hint = tk.Label(
            self.record_settings,
            text="Chỉ bật khi cần ghi nhiều vị trí liên tiếp. Có thể tăng tải CPU.",
            wraplength=260,
            justify=tk.LEFT,
            fg="gray",
        )
        self.record_hint.pack(side=tk.TOP, fill="x", pady=(4, 0))
        self.common_bindings = KeyBindings(
            self.column1, "In-game Keybindings", config.bot
        )
        self.common_bindings.pack(side=tk.TOP, fill="x", expand=True, pady=(10, 0))

        self.column2 = Frame(self._scroll_content)
        self.column2.grid(row=0, column=2, sticky=tk.N, padx=10, pady=10)
        self.class_bindings = KeyBindings(
            self.column2, "No Command Book Selected", None
        )
        self.class_bindings.pack(side=tk.TOP, fill="x", expand=True)

    def _create_scrollable_frame(self):
        """Create a scrollable container for Settings content"""
        # Create canvas and scrollbar
        self._enable_horizontal_scroll = True

        self._canvas_container = Frame(self)
        self._canvas_container.pack(side="top", fill="both", expand=True)

        self._canvas = tk.Canvas(self._canvas_container, highlightthickness=0)
        self._scrollbar = tk.Scrollbar(
            self._canvas_container, orient="vertical", command=self._canvas.yview
        )
        self._hscrollbar = tk.Scrollbar(
            self, orient="horizontal", command=self._canvas.xview
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
        self._canvas.configure(
            yscrollcommand=self._scrollbar.set, xscrollcommand=self._hscrollbar.set
        )

        # Pack canvas and scrollbars
        self._canvas.pack(side="left", fill="both", expand=True)
        self._scrollbar.pack(side="right", fill="y")
        self._hscrollbar.pack(side="bottom", fill="x")

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
        if not getattr(self, "_enable_horizontal_scroll", False):
            canvas_width = event.width
            self._canvas.itemconfig(self._canvas_window, width=canvas_width)

    def update_class_bindings(self):
        self.class_bindings.destroy()
        class_name = config.bot.command_book.name.capitalize()
        self.class_bindings = KeyBindings(
            self.column2, f"{class_name} Keybindings", config.bot.command_book
        )
        self.class_bindings.pack(side=tk.TOP, fill="x", expand=True)

    def _build_key_output_section(self):
        tk.Label(
            self.key_output_settings,
            text="Chọn cách Auto Maple gửi phím vào MapleStory.",
            wraplength=260,
            justify=tk.LEFT,
            fg="gray",
        ).pack(side=tk.TOP, fill="x", pady=(0, 6))

        self.key_mode_display = {
            "sendinput": "SendInput (Host)",
            "arduino": "Arduino HID (Host)",
            "tcp": "TCP → VMware",
        }
        current_mode = getattr(config, "key_output_mode", "sendinput")
        if current_mode not in self.key_mode_display:
            current_mode = "sendinput"

        mode_frame = tk.Frame(self.key_output_settings)
        mode_frame.pack(side=tk.TOP, fill="x")
        tk.Label(mode_frame, text="Chế độ:", width=12, anchor="w").grid(
            row=0, column=0, sticky=tk.W
        )
        self.key_mode_var = tk.StringVar(value=current_mode)
        self.key_mode_menu = tk.OptionMenu(
            mode_frame,
            self.key_mode_var,
            *self.key_mode_display.keys(),
            command=lambda _=None: self._on_key_mode_change(),
        )
        self.key_mode_menu.grid(row=0, column=1, sticky=tk.EW, padx=(4, 0))
        mode_frame.grid_columnconfigure(1, weight=1)

        self.key_mode_summary = tk.Label(
            self.key_output_settings, text="", fg="gray", font=("Arial", 8)
        )
        self.key_mode_summary.pack(side=tk.TOP, fill="x", pady=(4, 0))

        tcp_frame = tk.Frame(self.key_output_settings)
        tcp_frame.pack(side=tk.TOP, fill="x", pady=(6, 0))
        tk.Label(tcp_frame, text="TCP Host:", width=12, anchor="w").grid(
            row=0, column=0, sticky=tk.W
        )
        self.tcp_host_var = tk.StringVar(
            value=getattr(config, "tcp_key_host", "127.0.0.1")
        )
        self.tcp_host_entry = tk.Entry(
            tcp_frame, textvariable=self.tcp_host_var, width=18
        )
        self.tcp_host_entry.grid(row=0, column=1, sticky=tk.W, padx=(4, 0))

        tk.Label(tcp_frame, text="TCP Port:", width=12, anchor="w").grid(
            row=1, column=0, sticky=tk.W, pady=(4, 0)
        )
        self.tcp_port_var = tk.StringVar(
            value=str(getattr(config, "tcp_key_port", 12345))
        )
        self.tcp_port_entry = tk.Entry(
            tcp_frame, textvariable=self.tcp_port_var, width=10
        )
        self.tcp_port_entry.grid(row=1, column=1, sticky=tk.W, padx=(4, 0), pady=(4, 0))

        self.tcp_apply_btn = tk.Button(
            tcp_frame,
            text="💾 Lưu TCP",
            command=self._on_tcp_settings_apply,
            cursor="hand2",
        )
        self.tcp_apply_btn.grid(
            row=2, column=0, columnspan=2, pady=(6, 0), sticky=tk.EW
        )

        self.key_output_status = tk.Label(
            self.key_output_settings, text="", fg="green", font=("Arial", 8)
        )
        self.key_output_status.pack(side=tk.TOP, fill="x", pady=(4, 0))

        self._update_key_output_ui()

    def _build_mirror_section(self):
        hint = tk.Label(
            self.mirror_settings,
            text="Hook phím thật trên host và forward tới VMware.",
            wraplength=260,
            justify=tk.LEFT,
            fg="gray",
        )
        hint.pack(side=tk.TOP, fill="x")

        enable_frame = tk.Frame(self.mirror_settings)
        enable_frame.pack(side=tk.TOP, fill="x", pady=(6, 0))
        self.mirror_enable_var = tk.BooleanVar(
            value=getattr(config, "mirror_input_enabled", False)
        )
        enable_toggle = tk.Checkbutton(
            enable_frame,
            text="Bật mirror input khi khởi động",
            variable=self.mirror_enable_var,
            command=self._on_mirror_enable_toggle,
            anchor="w",
            justify=tk.LEFT,
        )
        enable_toggle.pack(side=tk.LEFT, anchor="w")

        host_frame = tk.Frame(self.mirror_settings)
        host_frame.pack(side=tk.TOP, fill="x", pady=(6, 0))
        tk.Label(host_frame, text="VM Host:", width=12, anchor="w").grid(
            row=0, column=0, sticky=tk.W
        )
        self.mirror_host_var = tk.StringVar(
            value=getattr(config, "mirror_input_host", "127.0.0.1")
        )
        tk.Entry(host_frame, textvariable=self.mirror_host_var, width=18).grid(
            row=0, column=1, sticky=tk.W, padx=(4, 0)
        )

        tk.Label(host_frame, text="VM Port:", width=12, anchor="w").grid(
            row=1, column=0, sticky=tk.W, pady=(4, 0)
        )
        self.mirror_port_var = tk.StringVar(
            value=str(getattr(config, "mirror_input_port", 12345))
        )
        tk.Entry(host_frame, textvariable=self.mirror_port_var, width=10).grid(
            row=1, column=1, sticky=tk.W, padx=(4, 0), pady=(4, 0)
        )

        self.block_input_var = tk.BooleanVar(
            value=getattr(config, "mirror_input_block_original", False)
        )
        tk.Checkbutton(
            self.mirror_settings,
            text="Block bàn phím host khi mirror",
            variable=self.block_input_var,
            anchor="w",
        ).pack(side=tk.TOP, fill="x", pady=(6, 0))

        self.auto_connect_var = tk.BooleanVar(
            value=getattr(config, "mirror_input_auto_connect", False)
        )
        tk.Checkbutton(
            self.mirror_settings,
            text="Tự động kết nối khi mở Auto Maple",
            variable=self.auto_connect_var,
            anchor="w",
        ).pack(side=tk.TOP, fill="x", pady=(4, 0))

        self.mirror_save_btn = tk.Button(
            self.mirror_settings,
            text="💾 Lưu Mirror Input",
            command=self._on_mirror_save,
            cursor="hand2",
        )
        self.mirror_save_btn.pack(side=tk.TOP, fill="x", pady=(6, 0))

        self.mirror_status = tk.Label(
            self.mirror_settings, text="", fg="green", font=("Arial", 8)
        )
        self.mirror_status.pack(side=tk.TOP, fill="x", pady=(4, 0))

    def _on_listener_toggle(self):
        enabled = bool(self.listener_toggle_var.get())
        config.enable_keyboard_listener = enabled
        listener = getattr(config, "listener", None)
        if listener is not None:
            listener.enabled = enabled
        # Refresh status display if GUI view available
        try:
            if hasattr(config, "gui") and config.gui:
                if hasattr(config.gui, "view") and config.gui.view:
                    config.gui.view.status.update_input_method_status()
        except Exception:
            pass

    def _on_record_live_toggle(self):
        config.record_position_live_update = bool(self.record_live_var.get())

    # ------------------------------------------------------------------ key output helpers
    def _on_key_mode_change(self):
        mode = self.key_mode_var.get().strip().lower()
        if mode not in self.key_mode_display:
            mode = "sendinput"
            self.key_mode_var.set(mode)
        config.update_key_output_settings(mode=mode)
        if mode == "tcp":
            vkeys.reset_tcp_client()
        self._update_key_output_ui()

    def _on_tcp_settings_apply(self):
        host = self.tcp_host_var.get().strip()
        try:
            port = int(self.tcp_port_var.get().strip())
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                title="TCP settings",
                message="Port phải là số trong khoảng 1-65535.",
            )
            return

        if not host:
            messagebox.showerror(
                title="TCP settings", message="Host không được để trống."
            )
            return

        config.update_key_output_settings(host=host, port=port)
        vkeys.reset_tcp_client()
        self.key_output_status.config(text=f"✅ Đã lưu TCP ({host}:{port})", fg="green")
        self.after(3000, lambda: self.key_output_status.config(text=""))
        self._update_key_output_ui()

    def _update_key_output_ui(self):
        mode = self.key_mode_var.get().strip().lower()
        label = self.key_mode_display.get(mode, mode)
        self.key_mode_summary.config(text=f"Chế độ hiện tại: {label}")

        state = tk.NORMAL if mode == "tcp" else tk.DISABLED
        self.tcp_host_entry.config(state=state)
        self.tcp_port_entry.config(state=state)
        self.tcp_apply_btn.config(state=state)

    def refresh_key_output_section(self):
        if not hasattr(self, "key_mode_var"):
            return
        current_mode = getattr(config, "key_output_mode", "sendinput")
        if current_mode not in self.key_mode_display:
            current_mode = "sendinput"
        self.key_mode_var.set(current_mode)
        self.tcp_host_var.set(getattr(config, "tcp_key_host", "127.0.0.1"))
        self.tcp_port_var.set(str(getattr(config, "tcp_key_port", 12345)))
        self._update_key_output_ui()

    # ------------------------------------------------------------------ mirror input helpers
    def _on_mirror_enable_toggle(self):
        enabled = bool(self.mirror_enable_var.get())
        config.update_mirror_input_settings(enabled=enabled)
        mirror = getattr(config, "mirror_input", None)
        if mirror:
            if enabled and not mirror.is_running():
                mirror.configure(
                    getattr(config, "mirror_input_host", "127.0.0.1"),
                    getattr(config, "mirror_input_port", 12345),
                    getattr(config, "mirror_input_block_original", False),
                )
                mirror.start()
            elif not enabled and mirror.is_running():
                mirror.stop()
        self._update_mirror_status_label(
            "✅ Mirror auto-start ON" if enabled else "Mirror auto-start OFF", enabled
        )

    def _on_mirror_save(self):
        host = self.mirror_host_var.get().strip()
        try:
            port = int(self.mirror_port_var.get().strip())
            if not (1 <= port <= 65535):
                raise ValueError
        except ValueError:
            messagebox.showerror(
                title="Mirror Input", message="Port phải là số trong khoảng 1-65535."
            )
            return
        if not host:
            messagebox.showerror(
                title="Mirror Input", message="Host không được để trống."
            )
            return

        block = bool(self.block_input_var.get())
        auto_conn = bool(self.auto_connect_var.get())
        config.update_mirror_input_settings(
            host=host, port=port, block=block, auto_connect=auto_conn
        )
        mirror = getattr(config, "mirror_input", None)
        if mirror:
            mirror.configure(host, port, block)
            if auto_conn:
                mirror.connect()
            elif mirror.is_connected():
                mirror.disconnect()
        self._update_mirror_status_label(
            f"✅ Đã lưu ({host}:{port})", success=True, auto_clear=True
        )

    def refresh_mirror_section(self):
        if not hasattr(self, "mirror_host_var"):
            return
        self.mirror_enable_var.set(getattr(config, "mirror_input_enabled", False))
        self.mirror_host_var.set(getattr(config, "mirror_input_host", "127.0.0.1"))
        self.mirror_port_var.set(str(getattr(config, "mirror_input_port", 12345)))
        self.block_input_var.set(getattr(config, "mirror_input_block_original", False))
        self.auto_connect_var.set(getattr(config, "mirror_input_auto_connect", False))
        running = False
        mirror = getattr(config, "mirror_input", None)
        if mirror:
            running = mirror.is_running()
        connected = mirror.is_connected() if mirror else False
        status_text = "Mirror input đang chạy" if running else "Mirror input đang tắt"
        status_text += " | TCP Connected" if connected else " | TCP Disconnected"
        self._update_mirror_status_label(status_text, running or connected)

    def _build_ai_solver_section(self):
        """Build AI solver settings section."""
        # Puzzle solver
        self.puzzle_solver_var = tk.BooleanVar(
            value=getattr(config, "enable_puzzle_solver", False)
        )
        self.puzzle_solver_checkbox = tk.Checkbutton(
            self.ai_solver_settings,
            text="Bật AI Puzzle Solver",
            variable=self.puzzle_solver_var,
            command=self._on_puzzle_solver_toggle,
            anchor="w",
            justify=tk.LEFT,
        )
        self.puzzle_solver_checkbox.pack(side=tk.TOP, anchor="w")

        # Violetta solver
        self.violetta_solver_var = tk.BooleanVar(
            value=getattr(config, "enable_violetta_solver", False)
        )
        self.violetta_solver_checkbox = tk.Checkbutton(
            self.ai_solver_settings,
            text="Bật AI Violetta Solver",
            variable=self.violetta_solver_var,
            command=self._on_violetta_solver_toggle,
            anchor="w",
            justify=tk.LEFT,
        )
        self.violetta_solver_checkbox.pack(side=tk.TOP, anchor="w", pady=(5, 0))

        # Hint
        self.ai_solver_hint = tk.Label(
            self.ai_solver_settings,
            text="Tự động giải puzzle khi phát hiện. Cần train model trước.",
            wraplength=260,
            justify=tk.LEFT,
            fg="gray",
        )
        self.ai_solver_hint.pack(side=tk.TOP, fill="x", pady=(4, 0))

    def _on_puzzle_solver_toggle(self):
        """Handle puzzle solver toggle."""
        enabled = self.puzzle_solver_var.get()
        config.enable_puzzle_solver = enabled

        # Update notifier
        notifier = getattr(config, "notifier", None)
        if notifier:
            notifier.enable_puzzle_solver = enabled
            log.info(f"Puzzle solver: {'enabled' if enabled else 'disabled'}")

    def _on_violetta_solver_toggle(self):
        """Handle violetta solver toggle."""
        enabled = self.violetta_solver_var.get()
        config.enable_violetta_solver = enabled

        # Update notifier
        notifier = getattr(config, "notifier", None)
        if notifier:
            notifier.enable_violetta_solver = enabled
            log.info(f"Violetta solver: {'enabled' if enabled else 'disabled'}")

    def _update_mirror_status_label(self, text, success=True, auto_clear=False):
        self.mirror_status.config(text=text, fg="green" if success else "orange")
        if auto_clear:
            self.after(3000, lambda: self.mirror_status.config(text=""))
