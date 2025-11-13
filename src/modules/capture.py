"""A module for tracking useful in-game information."""

import time
import cv2
import threading
import ctypes
import mss
import mss.windows
import numpy as np
from src.common import config, utils
from ctypes import wintypes
import os
import sys
from src.common.logger import get_logger
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()


# Toggle verbose debug logging
DEBUG = False  # Disabled for cleaner output


log = get_logger(__name__)

# The distance between the top of the minimap and the top of the screen
MINIMAP_TOP_BORDER = 5

# The thickness of the other three borders of the minimap
MINIMAP_BOTTOM_BORDER = 9

# Minimap size scaling factors (adjust detection area)
# Balanced scale to show full minimap without too much extra space
MINIMAP_WIDTH_SCALE = 1.2   # 20% extra for full coverage
MINIMAP_HEIGHT_SCALE = 1.2  # 20% extra for full coverage

# Offset in pixels to adjust for windowed mode
WINDOWED_OFFSET_TOP = 36
WINDOWED_OFFSET_LEFT = 10

def get_asset_path(rel_path):
    base = getattr(sys, '_MEIPASS', os.path.abspath('.'))
    return os.path.join(base, rel_path)

# The top-left and bottom-right corners of the minimap
MM_TL_TEMPLATE = cv2.imread(get_asset_path('assets/minimap_tl_template.png'), 0)
MM_BR_TEMPLATE = cv2.imread(get_asset_path('assets/minimap_br_template.png'), 0)

MMT_HEIGHT = max(MM_TL_TEMPLATE.shape[0], MM_BR_TEMPLATE.shape[0])
MMT_WIDTH = max(MM_TL_TEMPLATE.shape[1], MM_BR_TEMPLATE.shape[1])

# The player's symbol on the minimap (support multiple templates and pick the first that matches)
_player_template_paths = [
    get_asset_path('assets/player_template.png'),        # default 10x10
    get_asset_path('assets/player_template_new.png')     # optional 20x20
]
PLAYER_TEMPLATES = []
for path in _player_template_paths:
    try:
        tpl = cv2.imread(path, 0)
        if tpl is not None:
            PLAYER_TEMPLATES.append((path, tpl))
    except Exception:
        pass

# Use first template for dimension reference
PLAYER_TEMPLATE = PLAYER_TEMPLATES[0][1] if PLAYER_TEMPLATES else None
PT_HEIGHT, PT_WIDTH = PLAYER_TEMPLATE.shape if PLAYER_TEMPLATE is not None else (10, 10)


class Capture:
    """
    A class that tracks player position and various in-game events. It constantly updates
    the config module with information regarding these events. It also annotates and
    displays the minimap in a pop-up window.
    """

    def __init__(self):
        """Initializes this Capture object's main thread."""

        config.capture = self

        self.frame = None
        self.minimap = {}
        self.minimap_ratio = 1
        self.minimap_sample = None
        self.sct = None
        self.window = {
            'left': 0,
            'top': 0,
            'width': 1366,
            'height': 768
        }

        self.ready = False
        self.calibrated = False
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True
        
        # CPU optimization: Track position for skipping template matching
        self.last_player_pos = None
        self.last_pos_update_time = time.time()
        self.pos_update_interval = 0.5  # Force update every 0.5s even if position unchanged
        self.position_check_interval = 0.2  # Check position change every 0.2s

        # Minimap calibration coordinates (stored for recalibration)
        self.mm_tl = None
        self.mm_br = None
        self._recalibrate_requested = False

    def start(self):
        """Starts this Capture's thread."""

        log.info("Started video capture")
        self.thread.start()

    def _main(self):
        """Constantly monitors the player's position and in-game events."""

        mss.windows.CAPTUREBLT = 0
        consecutive_calibration_errors = 0
        max_calibration_errors = 20
        
        while True:
            try:
            # Calibrate screen capture (try MapleStory N first, then MapleStory)
            handle = None
            for title in ['MapleStory N', 'MapleStory']:
                handle = user32.FindWindowW(None, title)
                if handle:
                    if DEBUG:
                        log.debug("Found window: %s", title)
                    break
            
            if not handle:
                if DEBUG:
                    log.debug("MapleStory window not found, retrying...")
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

            # Calibrate by finding the top-left and bottom-right corners of the minimap
            with mss.mss() as self.sct:
                self.frame = self.screenshot()
            if self.frame is None:
                if DEBUG:
                    log.debug("Screenshot is None, retrying...")
                continue
            
            # Restrict search areas to avoid false positives and ensure ROI validity
            fh, fw = self.frame.shape[:2]
            if DEBUG:
                log.debug("Frame shape: %sx%s", fh, fw)
            tl_roi_x0, tl_roi_y0 = 0, 0
            tl_roi_x1, tl_roi_y1 = int(fw * 0.5), int(fh * 0.35)
            
            # Ensure TL ROI is valid
            if tl_roi_x1 <= tl_roi_x0 or tl_roi_y1 <= tl_roi_y0:
                if DEBUG:
                    log.debug("Invalid TL ROI bounds: %s,%s to %s,%s", tl_roi_x0, tl_roi_y0, tl_roi_x1, tl_roi_y1)
                continue
            
            tl_roi = self.frame[tl_roi_y0:tl_roi_y1, tl_roi_x0:tl_roi_x1]
            if tl_roi.size == 0:
                if DEBUG:
                    log.debug("TL ROI is empty")
                continue
            
            if DEBUG:
                log.debug("Searching for TL corner in ROI...")
            tl_local, _ = utils.single_match(tl_roi, MM_TL_TEMPLATE)
            tl = (tl_local[0] + tl_roi_x0, tl_local[1] + tl_roi_y0)
            if DEBUG:
                log.debug("TL corner found at: %s", tl)
            
            # Restrict search area for BR corner
            br_roi_x0 = min(max(tl[0] + 50, 0), fw - 1)
            br_roi_y0 = min(max(tl[1] + 20, 0), fh - 1)
            br_roi_x1 = fw
            br_roi_y1 = min(int(fh * 0.6), fh)
            
            # Ensure BR ROI is valid
            if br_roi_x0 >= br_roi_x1 or br_roi_y0 >= br_roi_y1:
                if DEBUG:
                    log.debug("Invalid BR ROI bounds: %s,%s to %s,%s", br_roi_x0, br_roi_y0, br_roi_x1, br_roi_y1)
                continue
            
            br_roi = self.frame[br_roi_y0:br_roi_y1, br_roi_x0:br_roi_x1]
            if br_roi.size == 0:
                if DEBUG:
                    log.debug("BR ROI is empty")
                continue
            
            if DEBUG:
                log.debug("Searching for BR corner in ROI...")
            _, br_local = utils.single_match(br_roi, MM_BR_TEMPLATE)
            br = (br_local[0] + br_roi_x0, br_local[1] + br_roi_y0)
            if DEBUG:
                log.debug("BR corner found at: %s", br)
            
            mm_tl = (
                tl[0] + MINIMAP_BOTTOM_BORDER,
                tl[1] + MINIMAP_TOP_BORDER
            )
            mm_br_base = (
                max(mm_tl[0] + PT_WIDTH, br[0] - MINIMAP_BOTTOM_BORDER),
                max(mm_tl[1] + PT_HEIGHT, br[1] - MINIMAP_BOTTOM_BORDER)
            )
            
            # Apply scaling factors to expand minimap detection area
            base_w = mm_br_base[0] - mm_tl[0]
            base_h = mm_br_base[1] - mm_tl[1]
            scaled_w = int(base_w * MINIMAP_WIDTH_SCALE)
            scaled_h = int(base_h * MINIMAP_HEIGHT_SCALE)
            
            # Ensure scaled minimap doesn't exceed frame bounds
            mm_br = (
                min(mm_tl[0] + scaled_w, fw - 1),
                min(mm_tl[1] + scaled_h, fh - 1)
            )
            
            self.minimap_ratio = (mm_br[0] - mm_tl[0]) / (mm_br[1] - mm_tl[1])
            
            # Guard against bad corner matches producing a thin strip
            expected_w, expected_h = int(421 * MINIMAP_WIDTH_SCALE), int(133 * MINIMAP_HEIGHT_SCALE)
            crop_w = max(0, mm_br[0] - mm_tl[0])
            crop_h = max(0, mm_br[1] - mm_tl[1])
            if crop_w < 200 or crop_h < 80:
                # Fallback to expected size anchored at TL
                mm_br = (
                    min(mm_tl[0] + expected_w, fw - 1),
                    min(mm_tl[1] + expected_h, fh - 1)
                )
            
            # Final validation: ensure crop is valid
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
                log.debug("Calibration successful! Minimap size: %sx%s", mm_br[0]-mm_tl[0], mm_br[1]-mm_tl[1])
                
                # Store calibration coordinates as instance variables
                self.mm_tl = mm_tl
                self.mm_br = mm_br
            self.calibrated = True
                self._recalibrate_requested = False
                consecutive_calibration_errors = 0  # Reset on success

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

                    # CPU Optimization: Adaptive frame rate based on bot state
                    # - Bot enabled + moving: 30 FPS (0.033s)
                    # - Bot enabled + idle: 10 FPS (0.1s)
                    # - Bot disabled: 5 FPS (0.2s)
                    current_time = time.time()
                    bot_active = config.enabled and len(config.path) > 0
                    
                    if bot_active:
                        frame_delay = 0.033  # 30 FPS when active
                    elif config.enabled:
                        frame_delay = 0.1     # 10 FPS when idle
                    else:
                        frame_delay = 0.2    # 5 FPS when disabled

                    # Take screenshot
                    self.frame = self.screenshot()
                    if self.frame is None:
                        time.sleep(frame_delay)
                        continue

                            # Crop the frame to only show the minimap (use stored coordinates)
                            minimap = self.frame[self.mm_tl[1]:self.mm_br[1], self.mm_tl[0]:self.mm_br[0]]
                    
                    # CPU Optimization: Skip template matching if position hasn't changed
                    # Only skip if:
                    # - Position is known and hasn't changed
                    # - But force update every pos_update_interval to detect stuck
                    should_match = True
                    time_since_last_update = current_time - self.last_pos_update_time
                    
                    if self.last_player_pos is not None and time_since_last_update < self.position_check_interval:
                        # Skip matching if position likely unchanged and not timeout
                        should_match = False
                    elif time_since_last_update >= self.pos_update_interval:
                        # Force update to detect if stuck
                        should_match = True
                    
                    # CPU Optimization: Convert BGRA to BGR once, reuse for both matching and GUI
                    # Only convert when needed (for matching or GUI display)
                    minimap_bgr = None
                    
                    if should_match:
                        # Convert BGRA to BGR for template matching
                        minimap_bgr = cv2.cvtColor(minimap, cv2.COLOR_BGRA2BGR)
                        
                        # CPU Optimization: Pre-convert to grayscale once, reuse for all template matches
                        minimap_gray = cv2.cvtColor(minimap_bgr, cv2.COLOR_BGR2GRAY)
                        
                        # Determine the player's position using the first matching template
                        player = []
                        for name, tpl in PLAYER_TEMPLATES:
                            thr = 0.6
                            # Slightly lower threshold for larger/new template
                            if name.endswith('player_template_new.png'):
                                thr = 0.55
                            # Pass is_gray=True since minimap_gray is already grayscale
                            player = utils.multi_match(minimap_gray, tpl, threshold=thr, is_gray=True)
                            if player:
                                break
                        
                        if player:
                            new_pos = utils.convert_to_relative(player[0], minimap)
                            # Only update if position changed or timeout
                            if new_pos != self.last_player_pos or time_since_last_update >= self.pos_update_interval:
                                config.player_pos = new_pos
                                self.last_player_pos = new_pos
                                self.last_pos_update_time = current_time
                    
                    # Package display information to be polled by GUI
                    # Convert minimap to BGR for GUI display (reuse if already converted)
                    if minimap_bgr is None:
                        minimap_bgr = cv2.cvtColor(minimap, cv2.COLOR_BGRA2BGR)
                    self.minimap = {
                        'minimap': minimap_bgr,
                        'rune_active': config.bot.rune_active,
                        'rune_pos': config.bot.rune_pos,
                        'path': config.path,
                        'player_pos': config.player_pos
                    }

                    if not self.ready:
                        self.ready = True
                            
                            # Reset error counter on successful iteration
                            consecutive_tracking_errors = 0
                    
                    # CPU Optimization: Use adaptive delay instead of fixed 0.001s
                    time.sleep(frame_delay)
                                
                        except KeyboardInterrupt:
                            log.info("Capture tracking loop interrupted by user")
                            raise
                        except Exception as e:
                            consecutive_tracking_errors += 1
                            log.error("Capture tracking error (consecutive: %d/%d): %s", 
                                     consecutive_tracking_errors, max_tracking_errors, e, exc_info=True)
                            
                            # If too many errors, force recalibration
                            if consecutive_tracking_errors >= max_tracking_errors:
                                log.warning("Too many tracking errors, forcing recalibration")
                                self.calibrated = False
                                self._recalibrate_requested = False
                                break
                            
                            # Brief pause before retry
                            time.sleep(0.1)
                            
            except KeyboardInterrupt:
                log.info("Capture calibration loop interrupted by user")
                raise
            except Exception as e:
                consecutive_calibration_errors += 1
                log.error("Capture calibration error (consecutive: %d/%d): %s", 
                         consecutive_calibration_errors, max_calibration_errors, e, exc_info=True)
                
                # If too many consecutive calibration errors, wait longer before retry
                if consecutive_calibration_errors >= max_calibration_errors:
                    log.warning("Too many calibration errors, waiting 5 seconds before retry")
                    time.sleep(5)
                    consecutive_calibration_errors = 0  # Reset counter
                else:
                    time.sleep(0.5)  # Brief pause before retry

    def screenshot(self, delay=1):
        try:
            return np.array(self.sct.grab(self.window))
        except mss.exception.ScreenShotError:
            suffix = 's' if delay != 1 else ''
            log.warning("Error while taking screenshot, retrying in %s second%s", delay, suffix)
            time.sleep(delay)
    
    def recalibrate_minimap(self):
        """
        Request recalibration of minimap location.
        This is useful when the player moves to a different map.
        """
        if not self.ready:
            log.warning("Cannot recalibrate: Capture module not ready yet")
            return False
        
        log.info("📍 Recalibration requested by user")
        self._recalibrate_requested = True
        return True
