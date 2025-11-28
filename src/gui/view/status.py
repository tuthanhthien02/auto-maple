import json
import os
import subprocess
import sys
import tkinter as tk

from src.gui.interfaces import LabelFrame
from src.common import config, manual_capture_config, utils, vkeys
from src.routine.components import Point


class Status(LabelFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, "Status", **kwargs)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(3, weight=1)

        # Hidden vars for compatibility (e.g. Edit tab reuses StringVars)
        self.curr_cb = tk.StringVar()
        self.curr_routine = tk.StringVar()
        self.command_sequence_var = tk.StringVar()

        # Dynamic Paths Status
        self.dynamic_paths_label = tk.Label(self, text="Dynamic Paths:")
        self.dynamic_paths_label.grid(row=0, column=1, padx=5, pady=(5, 5), sticky=tk.E)
        self.dynamic_paths_var = tk.StringVar(value="Disabled")
        self.dynamic_paths_entry = tk.Entry(
            self, textvariable=self.dynamic_paths_var, state=tk.DISABLED, width=30
        )
        self.dynamic_paths_entry.grid(
            row=0, column=2, padx=(0, 5), pady=(5, 5), sticky=tk.EW
        )

        # Command Sequence Status (shows command order after shuffle)
        # Input Method Status (Arduino/SendInput)
        self.input_method_label = tk.Label(self, text="Input Method:")
        self.input_method_label.grid(row=1, column=1, padx=5, pady=(0, 5), sticky=tk.E)
        self.input_method_var = tk.StringVar(value="Checking...")
        self.input_method_entry = tk.Entry(
            self, textvariable=self.input_method_var, state=tk.DISABLED, width=30
        )
        self.input_method_entry.grid(
            row=2, column=2, padx=(0, 5), pady=(0, 5), sticky=tk.EW
        )

        # Manual capture selection controls
        self.capture_region_label = tk.Label(self, text="Manual Capture:")
        self.capture_region_label.grid(
            row=2, column=1, padx=5, pady=(0, 5), sticky=tk.E
        )
        self.capture_region_var = tk.StringVar(
            value=self._format_region(config.manual_capture_rect)
        )
        self.capture_region_entry = tk.Entry(
            self, textvariable=self.capture_region_var, state=tk.DISABLED, width=30
        )
        self.capture_region_entry.grid(
            row=2, column=2, padx=(0, 5), pady=(0, 5), sticky=tk.EW
        )

        self.select_region_btn = tk.Button(
            self,
            text="📐 Chọn vùng màn hình",
            command=self._on_select_region_click,
            bg="#9C27B0",
            fg="white",
            activebackground="#7B1FA2",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
        )
        self.select_region_btn.grid(
            row=3, column=1, columnspan=2, padx=5, pady=(0, 5), sticky=tk.EW
        )

        self.start_capture_btn = tk.Button(
            self,
            text="🖥️ Start Capture",
            command=self._on_start_capture_click,
            bg="#795548",
            fg="white",
            activebackground="#5D4037",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
            state=tk.DISABLED,
        )
        self.start_capture_btn.grid(
            row=4, column=1, columnspan=2, padx=5, pady=(0, 5), sticky=tk.EW
        )

        self.capture_status_label = tk.Label(
            self, text="", fg="orange", font=("Arial", 8)
        )
        self.capture_status_label.grid(
            row=5, column=1, columnspan=2, padx=5, pady=(0, 5)
        )

        self.mirror_btn = tk.Button(
            self,
            text="Mirror Input: OFF",
            command=self._on_toggle_mirror,
            bg="#9E9E9E",
            fg="white",
            activebackground="#757575",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
        )
        self.mirror_btn.grid(
            row=6, column=1, columnspan=2, padx=5, pady=(0, 5), sticky=tk.EW
        )

        # Recalibrate Minimap button
        self.recalibrate_btn = tk.Button(
            self,
            text="📍 Recalibrate Minimap",
            command=self._on_recalibrate_click,
            bg="#4CAF50",
            fg="white",
            activebackground="#45a049",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
        )
        self.recalibrate_btn.grid(
            row=7, column=1, columnspan=2, padx=5, pady=(5, 5), sticky=tk.EW
        )
        self.toggle_btn = tk.Button(
            self,
            text="▶ Toggle Bot (Start/Stop)",
            command=self._on_toggle_bot_click,
            bg="#2196F3",
            fg="white",
            activebackground="#1976D2",
            activeforeground="white",
            relief=tk.RAISED,
            bd=2,
            cursor="hand2",
        )
        self.toggle_btn.grid(
            row=8, column=1, columnspan=2, padx=5, pady=(0, 5), sticky=tk.EW
        )

        # Status label for recalibration feedback
        self.recalibrate_status = tk.Label(self, text="", fg="green", font=("Arial", 8))
        self.recalibrate_status.grid(row=9, column=1, columnspan=2, padx=5, pady=(0, 5))

        self._update_capture_controls()
        self._set_capture_status("🎯 Hãy chọn vùng MapleStory", "orange")

    def set_cb(self, string):
        self.curr_cb.set(string)

    def set_routine(self, string):
        self.curr_routine.set(string)

    def update_dynamic_paths_status(self):
        """Update Dynamic Paths status display."""
        try:
            if not hasattr(config, "routine") or config.routine is None:
                self.dynamic_paths_var.set("No routine loaded")
                return

            routine = config.routine
            if not routine.dynamic_paths_enabled:
                self.dynamic_paths_var.set("Disabled")
                return

            if not routine.dynamic_paths or not routine.current_path_id:
                self.dynamic_paths_var.set("Enabled (no paths)")
                return

            # Get current path info
            current_path = next(
                (
                    p
                    for p in routine.dynamic_paths
                    if p["id"] == routine.current_path_id
                ),
                None,
            )
            if not current_path:
                self.dynamic_paths_var.set(
                    f"Enabled ({routine.current_path_id} - not found)"
                )
                return

            # Calculate path number (1-based) and total paths
            total_paths = len(routine.dynamic_paths)
            path_number = (
                next(
                    (
                        i
                        for i, p in enumerate(routine.dynamic_paths)
                        if p["id"] == routine.current_path_id
                    ),
                    0,
                )
                + 1
            )

            # Get current position in path
            current_path_points = len(current_path["indices"])
            current_index = getattr(routine, "index", 0)
            try:
                current_position_in_path = (
                    current_path["indices"].index(current_index) + 1
                )
            except (ValueError, AttributeError):
                current_position_in_path = 0

            # Build status string with clear "Path X/Y" format
            switch_info = (
                f"{routine.path_switch_counter}/{routine.path_switch_interval}"
            )
            loops_remaining = routine.path_switch_interval - routine.path_switch_counter

            if current_position_in_path > 0:
                status = f"Path {path_number}/{total_paths} | Point {current_position_in_path}/{current_path_points} | Loop {switch_info} | {loops_remaining} remaining"
            else:
                status = f"Path {path_number}/{total_paths} | {current_path_points} points | Loop {switch_info} | {loops_remaining} remaining"

            self.dynamic_paths_var.set(status)
        except Exception:
            # Silently handle errors to avoid spamming
            pass

    def update_command_sequence_status(self):
        """Update Command Sequence status display - shows command order after shuffle."""
        try:
            if not hasattr(config, "routine") or config.routine is None:
                self.command_sequence_var.set("No routine loaded")
                return

            routine = config.routine
            cmd_cfg = routine.command_randomization

            if not cmd_cfg.get("enabled", False):
                self.command_sequence_var.set("Disabled")
                return

            # Get current point
            try:
                current_index = getattr(routine, "index", 0)
                if current_index < 0 or current_index >= len(routine.sequence):
                    self.command_sequence_var.set("No point selected")
                    return

                current_item = routine.sequence[current_index]
                if not isinstance(current_item, Point):
                    self.command_sequence_var.set("Not a Point")
                    return

                # Get variant info for command order preview
                current_variant = getattr(routine, "current_variant", "normal")
                is_reverse = current_variant == "reverse"
                is_floor_only = current_variant in ["floor1_only", "floor2_only"]
                floor_direction = getattr(routine, "floor_direction", "forward")
                is_floor_reverse = is_floor_only and floor_direction == "reverse"

                # Get command order preview
                command_order = current_item.get_command_order_preview(
                    is_reverse, is_floor_reverse
                )

                if not command_order:
                    self.command_sequence_var.set("No commands")
                    return

                # Build display string (limit length to fit in entry)
                order_str = " → ".join(command_order)
                if len(order_str) > 80:
                    # Truncate if too long
                    order_str = order_str[:77] + "..."

                self.command_sequence_var.set(order_str)
            except (AttributeError, IndexError, TypeError):
                # If we can't get command order, show enabled status
                self.command_sequence_var.set("Enabled (preview unavailable)")
        except Exception:
            # Silently handle errors to avoid spamming
            pass

    def update_input_method_status(self):
        """Update Input Method status display - shows Arduino or SendInput."""
        try:
            mode = getattr(config, "key_output_mode", "sendinput")
            status = None
            if mode == "tcp":
                host = getattr(config, "tcp_key_host", "127.0.0.1")
                port = getattr(config, "tcp_key_port", 12345)
                status = f"TCP → {host}:{port}"
            elif mode == "arduino":
                try:
                    from src.common.vkeys import _get_arduino_output

                    arduino = _get_arduino_output()
                    if arduino and hasattr(arduino, "connected") and arduino.connected:
                        try:
                            from src.common.shared_arduino_connection import (
                                SharedArduinoConnection,
                            )

                            shared_conn = SharedArduinoConnection()
                            com_port = getattr(shared_conn, "com_port", None)
                            if com_port:
                                status = f"Arduino ({com_port})"
                            else:
                                status = "Arduino (Connected)"
                        except Exception:
                            status = "Arduino (Connected)"
                    else:
                        status = "SendInput (Arduino failed)"
                except Exception:
                    status = "SendInput (Arduino error)"
            else:
                status = "SendInput"
            if not config.enable_keyboard_listener:
                hook_note = "Keyboard hook off"
                status = f"{status} | {hook_note}" if status else hook_note

            if not status:
                status = "Unknown"

            self.input_method_var.set(status)
            if not config.enable_keyboard_listener:
                self.toggle_btn.config(
                    text="▶ Toggle Bot (Hook Off)",
                    bg="#FF9800",
                    fg="white",
                    activebackground="#F57C00",
                    activeforeground="white",
                )
            else:
                self.toggle_btn.config(
                    text="▶ Toggle Bot (Start/Stop)",
                    bg="#2196F3",
                    fg="white",
                    activebackground="#1976D2",
                    activeforeground="white",
                )
            self._update_toggle_button_state()
            self._update_mirror_button()
        except Exception:
            # Silently handle errors to avoid spamming
            pass

    def _on_recalibrate_click(self):
        """Handle recalibrate minimap button click."""
        if not hasattr(config, "capture") or config.capture is None:
            self.recalibrate_status.config(
                text="❌ Capture module not available", fg="red"
            )
            self.after(3000, lambda: self.recalibrate_status.config(text=""))
            return

        if not config.capture.ready:
            self.recalibrate_status.config(
                text="⏳ Capture module not ready yet", fg="orange"
            )
            self.after(3000, lambda: self.recalibrate_status.config(text=""))
            return

        # Disable button during recalibration
        self.recalibrate_btn.config(state=tk.DISABLED, text="⏳ Recalibrating...")
        self._set_status_message("🔄 Recalibrating minimap location...", "blue", 0)

        # Request recalibration
        success = config.capture.recalibrate_minimap()

        if success:
            # Update status after a delay
            self.after(
                2000,
                lambda: self.recalibrate_status.config(
                    text="✅ Recalibration started. Please wait...", fg="green"
                ),
            )
            # Re-enable button after 5 seconds
            self.after(5000, self._recalibrate_complete)
        else:
            self.recalibrate_btn.config(state=tk.NORMAL, text="📍 Recalibrate Minimap")
            self._set_status_message("❌ Failed to start recalibration", "red")

    def _recalibrate_complete(self):
        """Re-enable button after recalibration completes."""
        self.recalibrate_btn.config(state=tk.NORMAL, text="📍 Recalibrate Minimap")
        if hasattr(config, "capture") and config.capture and config.capture.calibrated:
            self._set_status_message("✅ Recalibration complete!", "green")
        else:
            self._set_status_message("⏳ Still calibrating...", "orange", 0)
            self.after(2000, self._recalibrate_complete)

    def _on_toggle_bot_click(self):
        """Toggle bot enabled state without relying on keyboard hook."""
        try:
            capture_ready = (
                hasattr(config, "capture")
                and config.capture is not None
                and config.capture.ready
            )
            if not capture_ready:
                self._set_status_message(
                    "❌ Hãy start capture trước khi bật bot", "red"
                )
                return

            if hasattr(config, "listener") and config.listener:
                from src.modules.listener import Listener  # Local import to avoid cycle

                Listener.toggle_enabled()
            else:
                config.enabled = not config.enabled
                utils.print_state()
            state_text = "▶ Bot enabled" if config.enabled else "⏸️ Bot paused"
            color = "green" if config.enabled else "orange"
            self._set_status_message(state_text, color)
        except Exception as exc:
            self._set_status_message(f"❌ Toggle failed: {exc}", "red")

    def _set_status_message(self, text, color, duration=3000):
        """Utility to update status label with auto-clear."""
        self.recalibrate_status.config(text=text, fg=color)
        if duration:
            self.after(duration, lambda: self.recalibrate_status.config(text=""))

    def _update_mirror_button(self):
        mode = getattr(config, "key_output_mode", "sendinput")
        if mode == "tcp":
            host = getattr(config, "tcp_key_host", "127.0.0.1")
            port = getattr(config, "tcp_key_port", 12345)
            self.mirror_btn.config(
                text=f"Mirror Input: ON ({host}:{port})",
                bg="#16A34A",
                activebackground="#15803D",
            )
        else:
            self.mirror_btn.config(
                text="Mirror Input: OFF",
                bg="#9E9E9E",
                activebackground="#757575",
            )

    def _on_toggle_mirror(self):
        mode = getattr(config, "key_output_mode", "sendinput")
        if mode != "tcp":
            config.mirror_prev_key_mode = mode
            config.update_key_output_settings(mode="tcp")
            self._set_status_message("✅ Mirror input ON (TCP)", "green")
        else:
            fallback = getattr(config, "mirror_prev_key_mode", None) or "sendinput"
            config.update_key_output_settings(mode=fallback)
            config.mirror_prev_key_mode = None
            self._set_status_message(
                f"Mirror input OFF (mode={fallback})", "orange", duration=2000
            )
        vkeys.reset_tcp_client()
        self.update_input_method_status()
        try:
            if hasattr(config, "gui") and config.gui:
                if hasattr(config.gui, "settings") and config.gui.settings:
                    config.gui.settings.refresh_key_output_section()
        except Exception:
            pass

    def _format_region(self, rect):
        if not rect:
            return "Chưa chọn"
        return f"{rect['width']}x{rect['height']} @ ({rect['left']}, {rect['top']})"

    def _get_selector_script_path(self):
        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..")
        )
        return os.path.join(project_root, "src", "tools", "manual_region_selector.py")

    def _update_capture_controls(self):
        rect = getattr(config, "manual_capture_rect", None)
        self.capture_region_var.set(self._format_region(rect))
        capture_ready = (
            hasattr(config, "capture")
            and config.capture is not None
            and config.capture.ready
        )
        if rect and not capture_ready:
            self.start_capture_btn.config(state=tk.NORMAL)
        else:
            self.start_capture_btn.config(state=tk.DISABLED)
        self._update_toggle_button_state()
        self._update_mirror_button()

        if capture_ready:
            self._set_capture_status("✅ Capture đang chạy", "green")
        elif rect:
            self._set_capture_status("ℹ️ Nhấn 'Start Capture' để bắt đầu", "orange")
        else:
            self._set_capture_status("🎯 Hãy chọn vùng MapleStory", "orange")

    def _set_capture_status(self, text, color="green"):
        self.capture_status_label.config(text=text, fg=color)

    def _on_select_region_click(self):
        script_path = self._get_selector_script_path()
        if not os.path.exists(script_path):
            self._set_capture_status("❌ Không tìm thấy tool chọn vùng", "red")
            return

        try:
            result = subprocess.run(
                [sys.executable, script_path],
                capture_output=True,
                text=True,
                check=False,
            )
        except Exception as exc:
            self._set_capture_status(f"❌ Lỗi khi chạy tool: {exc}", "red")
            return

        output = result.stdout.strip()
        if not output:
            self._set_capture_status("ℹ️ Đã hủy chọn vùng", "orange")
            return

        try:
            rect = json.loads(output)
        except json.JSONDecodeError:
            self._set_capture_status("❌ Không đọc được vùng đã chọn", "red")
            return

        capture = getattr(config, "capture", None)
        if capture is not None:
            capture.set_manual_region(rect, persist=True)
        else:
            manual_capture_config.save_manual_region(rect)

        self._set_capture_status("✅ Đã lưu vùng MapleStory", "green")
        self._update_capture_controls()

    def _on_start_capture_click(self):
        rect = getattr(config, "manual_capture_rect", None)
        if not rect:
            self._set_capture_status("❌ Chưa chọn vùng màn hình", "red")
            return

        capture = getattr(config, "capture", None)
        if capture is None:
            self._set_capture_status("❌ Capture module không khả dụng", "red")
            return

        try:
            capture.start_manual_capture(rect)
            self._set_capture_status("⏳ Đang khởi động capture...", "blue")
            self.start_capture_btn.config(state=tk.DISABLED)
            self._poll_capture_ready()
        except Exception as exc:
            self._set_capture_status(f"❌ Không thể start capture: {exc}", "red")

    def _poll_capture_ready(self):
        capture = getattr(config, "capture", None)
        if capture and capture.ready:
            self._set_capture_status("✅ Capture đang chạy", "green")
            self._update_capture_controls()
            return
        self.after(500, self._poll_capture_ready)

    def _update_toggle_button_state(self):
        capture_ready = (
            hasattr(config, "capture")
            and config.capture is not None
            and config.capture.ready
        )
        state = tk.NORMAL if capture_ready else tk.DISABLED
        self.toggle_btn.config(state=state)
