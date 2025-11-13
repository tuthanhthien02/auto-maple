"""A module that handles screen capture and minimap detection."""

import time
import ctypes
import threading
from ctypes import wintypes
import cv2
import numpy as np
import mss
from src.common import config, utils
from src.common.logger import get_logger

log = get_logger(__name__)
DEBUG = False

user32 = ctypes.windll.user32

MM_TL_TEMPLATE = cv2.imread('assets/minimap_tl_template.png', 0)
MM_BR_TEMPLATE = cv2.imread('assets/minimap_br_template.png', 0)
PLAYER_TEMPLATES = [
    ('player_template_new.png', cv2.imread('assets/player_template_new.png', 0)),
    ('player_template.png', cv2.imread('assets/player_template.png', 0))
]

MINIMAP_TOP_BORDER = 3
MINIMAP_BOTTOM_BORDER = 3
PT_WIDTH = 421
PT_HEIGHT = 133
MMT_WIDTH = 800
MMT_HEIGHT = 600

# Scaling factors to expand minimap detection area (for better edge detection)
MINIMAP_WIDTH_SCALE = 1.0
MINIMAP_HEIGHT_SCALE = 1.0

# Position update intervals (in seconds)
POSITION_CHECK_INTERVAL = 0.1  # Check position every 0.1s
POS_UPDATE_INTERVAL = 2.0  # Force position update every 2s to detect stuck


class Capture:
    """
    A class that handles screen capture and minimap detection.
    """

    def __init__(self):
        self.window = {
            'left': 0,
            'top': 0,
            'width': MMT_WIDTH,
            'height': MMT_HEIGHT
        }
        config.capture = self
        self.frame = None
        self.sct = None
        self.minimap_sample = None
        self.minimap_ratio = 0
        self.calibrated = False
        self.minimap = None
        self.ready = False
        self.mm_tl = None
        self.mm_br = None
        self._recalibrate_requested = False
        
        # Position tracking for CPU optimization
        self.last_player_pos = None
        self.last_pos_update_time = 0
        self.position_check_interval = POSITION_CHECK_INTERVAL
        self.pos_update_interval = POS_UPDATE_INTERVAL

    def start(self):
        """
        Starts the capture thread.
        """
        try:
            self.thread = threading.Thread(
                target=self._main,
                name="CaptureThread",
                daemon=True
            )
            self.thread.start()
        except Exception:
            log.error("Failed to start capture thread", exc_info=True)

    @staticmethod
    def _templates_available():
        """Check that minimap templates are loaded successfully."""
        if MM_TL_TEMPLATE is None or MM_BR_TEMPLATE is None:
            missing = []
            if MM_TL_TEMPLATE is None:
                missing.append("MM_TL_TEMPLATE")
            if MM_BR_TEMPLATE is None:
                missing.append("MM_BR_TEMPLATE")
            log.error("Missing minimap template(s): %s. Please ensure assets are present.",
                      ", ".join(missing))
            return False
        return True

    def recalibrate_minimap(self):
        """Request minimap recalibration without restarting the module."""
        self._recalibrate_requested = True
        log.info("📍 Minimap recalibration requested")

    def _main(self):
        """
        The main capture loop that calibrates and tracks the minimap.
        """
        if not self._templates_available():
            self.ready = False
            log.error("Capture module disabled because required templates are missing.")
            return

        consecutive_calibration_errors = 0
        max_calibration_errors = 20
        calibration_attempts = 0
        max_calibration_attempts = 60  # 60 attempts * 0.5s = 30 seconds before giving up

        while True:
            try:
                calibration_attempts += 1

                handle = None
                for title in ['MapleStory N', 'MapleStory']:
                    handle = user32.FindWindowW(None, title)
                    if handle:
                        if DEBUG:
                            log.debug("Found window: %s", title)
                        break

                if not handle:
                    if calibration_attempts % 10 == 0:
                        log.warning(
                            "⚠️  MapleStory window not found (attempt %d/%d). Please open MapleStory game.",
                            calibration_attempts,
                            max_calibration_attempts,
                        )
                    elif calibration_attempts == 1:
                        log.info("🔍 Searching for MapleStory window...")
                    if calibration_attempts >= max_calibration_attempts:
                        log.error("❌ Failed to find MapleStory window after %d attempts", max_calibration_attempts)
                        log.error("   Please ensure MapleStory is running and try again")
                        self.ready = True
                        break
                    time.sleep(0.5)
                    continue

                rect = wintypes.RECT()
                user32.GetWindowRect(handle, ctypes.pointer(rect))
                rect = (rect.left, rect.top, rect.right, rect.bottom)
                rect = tuple(max(0, x) for x in rect)

                self.window['left'] = rect[0]
                self.window['top'] = rect[1]
                self.window['width'] = max(rect[2] - rect[0], MMT_WIDTH)
                self.window['height'] = max(rect[3] - rect[1], MMT_HEIGHT)

                if DEBUG:
                    log.debug("Window rect: %s", rect)

                with mss.mss() as self.sct:
                    self.frame = self.screenshot()
                if self.frame is None:
                    if DEBUG:
                        log.debug("Screenshot is None, retrying...")
                    continue

                fh, fw = self.frame.shape[:2]
                if DEBUG:
                    log.debug("Frame shape: %sx%s", fh, fw)

                tl_roi_x0, tl_roi_y0 = 0, 0
                tl_roi_x1, tl_roi_y1 = int(fw * 0.5), int(fh * 0.35)
                if tl_roi_x1 <= tl_roi_x0 or tl_roi_y1 <= tl_roi_y0:
                    if DEBUG:
                        log.debug(
                            "Invalid TL ROI bounds: %s,%s to %s,%s",
                            tl_roi_x0,
                            tl_roi_y0,
                            tl_roi_x1,
                            tl_roi_y1,
                        )
                    continue

                tl_roi = self.frame[tl_roi_y0:tl_roi_y1, tl_roi_x0:tl_roi_x1]
                if tl_roi.size == 0:
                    if DEBUG:
                        log.debug("TL ROI is empty")
                    continue

                if DEBUG:
                    log.debug("Searching for TL corner in ROI...")
                if tl_roi.shape[0] < MM_TL_TEMPLATE.shape[0] or tl_roi.shape[1] < MM_TL_TEMPLATE.shape[1]:
                    if DEBUG:
                        log.debug(
                            "TL ROI smaller than template: roi=%s, template=%s",
                            tl_roi.shape,
                            MM_TL_TEMPLATE.shape,
                        )
                    continue

                tl_local, _ = utils.single_match(tl_roi, MM_TL_TEMPLATE)
                tl = (tl_local[0] + tl_roi_x0, tl_local[1] + tl_roi_y0)
                if DEBUG:
                    log.debug("TL corner found at: %s", tl)

                br_roi_x0 = min(max(tl[0] + 50, 0), fw - 1)
                br_roi_y0 = min(max(tl[1] + 20, 0), fh - 1)
                br_roi_x1 = fw
                br_roi_y1 = min(int(fh * 0.6), fh)

                if br_roi_x0 >= br_roi_x1 or br_roi_y0 >= br_roi_y1:
                    if DEBUG:
                        log.debug(
                            "Invalid BR ROI bounds: %s,%s to %s,%s",
                            br_roi_x0,
                            br_roi_y0,
                            br_roi_x1,
                            br_roi_y1,
                        )
                    continue

                br_roi = self.frame[br_roi_y0:br_roi_y1, br_roi_x0:br_roi_x1]
                if br_roi.size == 0:
                    if DEBUG:
                        log.debug("BR ROI is empty")
                    continue

                if DEBUG:
                    log.debug("Searching for BR corner in ROI...")
                if br_roi.shape[0] < MM_BR_TEMPLATE.shape[0] or br_roi.shape[1] < MM_BR_TEMPLATE.shape[1]:
                    if DEBUG:
                        log.debug(
                            "BR ROI smaller than template: roi=%s, template=%s",
                            br_roi.shape,
                            MM_BR_TEMPLATE.shape,
                        )
                    continue

                _, br_local = utils.single_match(br_roi, MM_BR_TEMPLATE)
                br = (br_local[0] + br_roi_x0, br_local[1] + br_roi_y0)
                if DEBUG:
                    log.debug("BR corner found at: %s", br)

                mm_tl = (tl[0] + MINIMAP_BOTTOM_BORDER, tl[1] + MINIMAP_TOP_BORDER)
                mm_br_base = (
                    max(mm_tl[0] + PT_WIDTH, br[0] - MINIMAP_BOTTOM_BORDER),
                    max(mm_tl[1] + PT_HEIGHT, br[1] - MINIMAP_BOTTOM_BORDER),
                )

                base_w = mm_br_base[0] - mm_tl[0]
                base_h = mm_br_base[1] - mm_tl[1]
                scaled_w = int(base_w * MINIMAP_WIDTH_SCALE)
                scaled_h = int(base_h * MINIMAP_HEIGHT_SCALE)

                mm_br = (
                    min(mm_tl[0] + scaled_w, fw - 1),
                    min(mm_tl[1] + scaled_h, fh - 1),
                )

                self.minimap_ratio = (mm_br[0] - mm_tl[0]) / (mm_br[1] - mm_tl[1])

                expected_w, expected_h = int(421 * MINIMAP_WIDTH_SCALE), int(133 * MINIMAP_HEIGHT_SCALE)
                crop_w = max(0, mm_br[0] - mm_tl[0])
                crop_h = max(0, mm_br[1] - mm_tl[1])
                if crop_w < 200 or crop_h < 80:
                    mm_br = (
                        min(mm_tl[0] + expected_w, fw - 1),
                        min(mm_tl[1] + expected_h, fh - 1),
                    )

                if mm_tl[0] >= mm_br[0] or mm_tl[1] >= mm_br[1]:
                    if DEBUG:
                        log.debug("Invalid minimap crop bounds: mm_tl=%s, mm_br=%s", mm_tl, mm_br)
                    continue

                self.minimap_sample = self.frame[mm_tl[1]:mm_br[1], mm_tl[0]:mm_br[0]]
                if self.minimap_sample.size == 0:
                    if DEBUG:
                        log.debug("Minimap sample is empty")
                    continue

                if DEBUG:
                    log.debug("Calibration successful! Minimap size: %sx%s", mm_br[0] - mm_tl[0], mm_br[1] - mm_tl[1])

                self.mm_tl = mm_tl
                self.mm_br = mm_br
                self.calibrated = True
                self._recalibrate_requested = False
                consecutive_calibration_errors = 0

                with mss.mss() as self.sct:
                    consecutive_tracking_errors = 0
                    max_tracking_errors = 10

                    while True:
                        try:
                            if not self.calibrated or self._recalibrate_requested:
                                if self._recalibrate_requested:
                                    log.info("🔄 Recalibration requested, restarting calibration...")
                                    self.calibrated = False
                                    self._recalibrate_requested = False
                                break

                            current_time = time.time()
                            bot_active = config.enabled and len(config.path) > 0

                            if bot_active:
                                frame_delay = 0.033
                            elif config.enabled:
                                frame_delay = 0.1
                            else:
                                frame_delay = 0.2

                            self.frame = self.screenshot()
                            if self.frame is None:
                                time.sleep(frame_delay)
                                continue

                            minimap = self.frame[self.mm_tl[1]:self.mm_br[1], self.mm_tl[0]:self.mm_br[0]]

                            should_match = True
                            time_since_last_update = current_time - self.last_pos_update_time
                            if self.last_player_pos is not None and time_since_last_update < self.position_check_interval:
                                should_match = False
                            elif time_since_last_update >= self.pos_update_interval:
                                should_match = True

                            minimap_bgr = None

                            if should_match:
                                minimap_bgr = cv2.cvtColor(minimap, cv2.COLOR_BGRA2BGR)
                                minimap_gray = cv2.cvtColor(minimap_bgr, cv2.COLOR_BGR2GRAY)

                                player = []
                                for name, tpl in PLAYER_TEMPLATES:
                                    thr = 0.6
                                    if name.endswith('player_template_new.png'):
                                        thr = 0.55
                                    player = utils.multi_match(minimap_gray, tpl, threshold=thr, is_gray=True)
                                    if player:
                                        break

                                if player:
                                    new_pos = utils.convert_to_relative(player[0], minimap)
                                    if (
                                        new_pos != self.last_player_pos
                                        or time_since_last_update >= self.pos_update_interval
                                    ):
                                        config.player_pos = new_pos
                                        self.last_player_pos = new_pos
                                        self.last_pos_update_time = current_time

                            if minimap_bgr is None:
                                minimap_bgr = cv2.cvtColor(minimap, cv2.COLOR_BGRA2BGR)
                            self.minimap = {
                                'minimap': minimap_bgr,
                                'rune_active': config.bot.rune_active,
                                'rune_pos': config.bot.rune_pos,
                                'path': config.path,
                                'player_pos': config.player_pos,
                            }

                            if not self.ready:
                                self.ready = True

                            consecutive_tracking_errors = 0
                            time.sleep(frame_delay)

                        except KeyboardInterrupt:
                            log.info("Capture tracking loop interrupted by user")
                            raise
                        except Exception as e:
                            consecutive_tracking_errors += 1
                            log.error(
                                "Capture tracking error (consecutive: %d/%d): %s",
                                consecutive_tracking_errors,
                                max_tracking_errors,
                                e,
                                exc_info=True,
                            )

                            if consecutive_tracking_errors >= max_tracking_errors:
                                log.warning("Too many tracking errors, forcing recalibration")
                                self.calibrated = False
                                self._recalibrate_requested = False
                                break

                            time.sleep(0.1)
            except KeyboardInterrupt:
                log.info("Capture calibration loop interrupted by user")
                raise
            except Exception as e:
                consecutive_calibration_errors += 1
                log.error(
                    "Capture calibration error (consecutive: %d/%d): %s",
                    consecutive_calibration_errors,
                    max_calibration_errors,
                    e,
                    exc_info=True,
                )

                if consecutive_calibration_errors >= max_calibration_errors:
                    log.warning("Too many calibration errors, waiting 5 seconds before retry")
                    time.sleep(5)
                    consecutive_calibration_errors = 0
                else:
                    time.sleep(0.5)

    def screenshot(self, delay=1):
        try:
            return np.array(self.sct.grab(self.window))
        except mss.exception.ScreenShotError:
            return None
