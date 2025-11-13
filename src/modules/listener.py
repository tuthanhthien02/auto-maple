"""A keyboard listener to track user inputs."""

import time
import threading
import winsound
from datetime import datetime
from src.common.interfaces import Configurable
from src.common import config, utils
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
    }
    BLOCK_DELAY = 1  # Delay after blocking restricted button press

    def __init__(self):
        """Initializes this Listener object's main thread."""

        super().__init__("controls")
        config.listener = self

        self.enabled = False
        self.ready = False
        self.block_time = 0
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True
        self.keyboard_available = kb is not None

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

                if self.enabled:
                    if kb is None:
                        time.sleep(0.05)
                        continue
                    if kb.is_pressed(self.config["Start/stop"]):
                        Listener.toggle_enabled()
                    elif kb.is_pressed(self.config["Reload routine"]):
                        Listener.reload_routine()
                    elif self.restricted_pressed("Record position"):
                        Listener.record_position()
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

        if not config.enabled:
            Listener.recalibrate_minimap()  # Recalibrate only when being enabled.

        config.enabled = not config.enabled
        utils.print_state()

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
