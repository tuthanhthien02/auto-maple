"""A keyboard listener to track user inputs."""

import time
import threading
import winsound
from datetime import datetime
from src.common.interfaces import Configurable
from src.common import config, utils, vkeys
from src.common.logger import get_logger

try:
    import keyboard as kb  # noqa: WPS433
except ImportError:  # pragma: no cover
    kb = None  # type: ignore

log = get_logger(__name__)


class Listener(Configurable):
    DEFAULT_CONFIG = {
        "Start/stop": "insert",
        "Reload routine": "f6",
        "Record position": "f7",
        "Toggle mirror input": "delete",
    }
    BLOCK_DELAY = 1  # Delay after blocking restricted button press

    def __init__(self):
        """Initializes this Listener object's main thread."""

        super().__init__("controls")
        config.listener = self

        # Ensure all hotkeys are valid (not empty) - fix any empty values
        config_fixed = False
        for action, default_value in self.DEFAULT_CONFIG.items():
            current_value = self.config.get(action, "").strip()
            if not current_value:
                self.config[action] = default_value
                log.info(f"Restored '{action}' hotkey to default: {default_value}")
                config_fixed = True
            # Update "Toggle mirror input" from old "f8" to new "delete"
            elif action == "Toggle mirror input" and current_value.lower() == "f8":
                self.config[action] = default_value
                log.info(f"Updated '{action}' hotkey from f8 to {default_value}")
                config_fixed = True

        # Save config if any fixes were made
        if config_fixed:
            self.save_config()

        self.enabled = False
        self.ready = False
        self.block_time = 0
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True
        self.keyboard_available = kb is not None

    def _is_valid_hotkey(self, action):
        """Check if hotkey exists and is not empty."""
        hotkey = self.config.get(action, "").strip()
        if not hotkey:
            # If empty, restore from default
            if action in self.DEFAULT_CONFIG:
                self.config[action] = self.DEFAULT_CONFIG[action]
                self.save_config()
                log.info(
                    f"Restored '{action}' hotkey to default: {self.DEFAULT_CONFIG[action]}"
                )
                return True
            return False
        return True

    def start(self):
        """
        Starts listening to user inputs.
        :return:    None
        """

        if not self.keyboard_available:
            self.ready = True
            log.warning(
                "Keyboard module unavailable; keyboard hotkeys are disabled. Use GUI controls instead."
            )
            return

        if config.enable_keyboard_listener:
            log.info("Started keyboard listener")
        else:
            log.info(
                "Keyboard listener thread running (hook disabled via configuration)."
            )
        self.thread.start()

    def _main(self):
        """
        Constantly listens for user inputs and updates variables in config accordingly.
        :return:    None
        """

        if not self.keyboard_available:
            self.ready = True
            return

        self.ready = True
        consecutive_errors = 0
        max_consecutive_errors = 10

        while True:
            try:
                if not config.enable_keyboard_listener:
                    self.enabled = False
                    time.sleep(0.1)
                    consecutive_errors = 0
                    continue

                if kb is None:
                    time.sleep(0.05)
                    continue

                # Check hotkeys that work regardless of bot state
                # Check Start/stop first (highest priority)
                start_stop = self.config.get("Start/stop", "").strip()
                if start_stop and kb.is_pressed(start_stop):
                    Listener.toggle_enabled()
                # Check Toggle mirror input (works even when bot disabled)
                elif self._is_valid_hotkey("Toggle mirror input"):
                    mirror_hotkey = self.config["Toggle mirror input"].strip()
                    if kb.is_pressed(mirror_hotkey):
                        Listener.toggle_mirror_input()
                # Check other hotkeys only when listener is enabled
                elif self.enabled:
                    if self._is_valid_hotkey("Reload routine") and kb.is_pressed(
                        self.config["Reload routine"]
                    ):
                        Listener.reload_routine()
                    elif self.restricted_pressed("Record position"):
                        Listener.record_position()

                if self.enabled:
                    # CPU Optimization: 50 Hz when enabled (sufficient for keyboard responsiveness)
                    time.sleep(0.02)
                else:
                    # CPU Optimization: 20 Hz when disabled (enough to detect enable)
                    time.sleep(0.05)

                # Reset error counter on successful iteration
                consecutive_errors = 0

            except KeyboardInterrupt:
                log.info("Listener loop interrupted by user")
                raise
            except Exception as e:
                consecutive_errors += 1
                log.error(
                    "Listener error (consecutive: %d/%d): %s",
                    consecutive_errors,
                    max_consecutive_errors,
                    e,
                    exc_info=True,
                )

                # If too many errors, disable listener temporarily
                if consecutive_errors >= max_consecutive_errors:
                    log.warning("Too many listener errors, temporarily disabling")
                    self.enabled = False
                    consecutive_errors = 0
                    time.sleep(2)
                else:
                    time.sleep(0.1)  # Brief pause before retry

    def restricted_pressed(self, action):
        """Returns whether the key bound to ACTION is pressed only if the bot is disabled."""

        if (
            not self.keyboard_available
            or not config.enable_keyboard_listener
            or kb is None
        ):
            return False

        if kb.is_pressed(self.config[action]):
            if not config.enabled:
                return True
            now = time.time()
            if now - self.block_time > Listener.BLOCK_DELAY:
                log.warning("Cannot use '%s' while Auto Maple is enabled", action)
                self.block_time = now
        return False

    @staticmethod
    def toggle_enabled():
        """Resumes or pauses the current routine. Plays a sound to notify the user."""

        config.bot.rune_active = False

        was_enabled = config.enabled
        if was_enabled:
            try:
                released = vkeys.release_tracked_keys()
                if released:
                    log.info(
                        "[Listener] Released %d tracked key(s) before disabling bot",
                        released,
                    )
            except Exception as release_error:
                log.warning(
                    "[Listener] Failed to release tracked keys before disabling: %s",
                    release_error,
                )

        if not config.enabled:
            Listener.recalibrate_minimap()  # Recalibrate only when being enabled.

        config.enabled = not config.enabled
        utils.print_state()

        if not config.enabled:
            notifier = getattr(config, "notifier", None)
            if notifier is not None:
                notifier.stop_lie_detector_sound()

        if config.enabled:
            winsound.Beep(784, 333)  # G5
        else:
            winsound.Beep(523, 333)  # C5
        time.sleep(0.267)

    @staticmethod
    def reload_routine():
        Listener.recalibrate_minimap()

        config.routine.load(config.routine.path)

        winsound.Beep(523, 200)  # C5
        winsound.Beep(659, 200)  # E5
        winsound.Beep(784, 200)  # G5

    @staticmethod
    def recalibrate_minimap():
        config.capture.calibrated = False
        while not config.capture.calibrated:
            time.sleep(0.01)
        config.gui.edit.minimap.redraw()

    @staticmethod
    def record_position():
        pos = tuple("{:.3f}".format(round(i, 3)) for i in config.player_pos)
        now = datetime.now().strftime("%I:%M:%S %p")
        config.gui.edit.record.add_entry(now, pos)
        log.info("Recorded position (%s, %s) at %s", pos[0], pos[1], now)
        time.sleep(0.6)

    @staticmethod
    def toggle_mirror_input():
        """Toggle mirror input on/off via hotkey - calls GUI button handler."""
        log.info("Toggle mirror input hotkey pressed (Del)")
        try:
            if hasattr(config, "gui") and config.gui:
                if hasattr(config.gui, "view") and config.gui.view:
                    if hasattr(config.gui.view, "status"):
                        # Call the same function as the GUI button
                        config.gui.view.status._on_toggle_mirror()
                        log.info("Mirror input toggled via hotkey - GUI updated")
                        time.sleep(
                            0.267
                        )  # Same delay as toggle_enabled to prevent multiple toggles
                        return
            log.warning("GUI not available, using fallback method")
        except Exception as exc:
            log.error(f"Failed to toggle mirror input via hotkey: {exc}", exc_info=True)

        # Fallback: direct module call if GUI not available
        mirror = getattr(config, "mirror_input", None)
        if mirror is None:
            log.warning("Mirror input module unavailable")
            return

        if mirror.is_running():
            mirror.stop()
            config.update_mirror_input_settings(enabled=False)
            log.info("Mirror input disabled via hotkey")
        else:
            block = getattr(config, "mirror_input_block_original", False)
            mirror.configure(
                getattr(config, "mirror_input_host", "127.0.0.1"),
                getattr(config, "mirror_input_port", 12345),
                block,
            )
            try:
                mirror.start()
                config.update_mirror_input_settings(enabled=True)
                log.info("Mirror input enabled via hotkey")
            except Exception as exc:
                log.error(f"Mirror start failed: {exc}")

        time.sleep(0.267)  # Same delay as toggle_enabled to prevent multiple toggles
