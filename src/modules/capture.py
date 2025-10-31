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
user32 = ctypes.windll.user32
user32.SetProcessDPIAware()


# Toggle verbose debug logging
DEBUG = False  # Disabled for cleaner output

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
    'assets/player_template.png',               # default 10x10
    'assets/player_template_new.png'            # optional 20x20
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

    def start(self):
        """Starts this Capture's thread."""

        print('\n[~] Started video capture')
        self.thread.start()

    def _main(self):
        """Constantly monitors the player's position and in-game events."""

        mss.windows.CAPTUREBLT = 0
        while True:
            # Calibrate screen capture (try MapleStory N first, then MapleStory)
            handle = None
            for title in ['MapleStory N', 'MapleStory']:
                handle = user32.FindWindowW(None, title)
                if handle:
                    if DEBUG:
                        print(f'[DEBUG] Found window: {title}')
                    break
            
            if not handle:
                if DEBUG:
                    print('[DEBUG] MapleStory window not found, retrying...')
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
                print(f'[DEBUG] Window rect: {rect}')

            # Calibrate by finding the top-left and bottom-right corners of the minimap
            with mss.mss() as self.sct:
                self.frame = self.screenshot()
            if self.frame is None:
                if DEBUG:
                    print('[DEBUG] Screenshot is None, retrying...')
                continue
            
            # Restrict search areas to avoid false positives and ensure ROI validity
            fh, fw = self.frame.shape[:2]
            if DEBUG:
                print(f'[DEBUG] Frame shape: {fh}x{fw}')
            tl_roi_x0, tl_roi_y0 = 0, 0
            tl_roi_x1, tl_roi_y1 = int(fw * 0.5), int(fh * 0.35)
            
            # Ensure TL ROI is valid
            if tl_roi_x1 <= tl_roi_x0 or tl_roi_y1 <= tl_roi_y0:
                if DEBUG:
                    print(f'[DEBUG] Invalid TL ROI bounds: {tl_roi_x0},{tl_roi_y0} to {tl_roi_x1},{tl_roi_y1}')
                continue
            
            tl_roi = self.frame[tl_roi_y0:tl_roi_y1, tl_roi_x0:tl_roi_x1]
            if tl_roi.size == 0:
                if DEBUG:
                    print('[DEBUG] TL ROI is empty')
                continue
            
            if DEBUG:
                print(f'[DEBUG] Searching for TL corner in ROI...')
            tl_local, _ = utils.single_match(tl_roi, MM_TL_TEMPLATE)
            tl = (tl_local[0] + tl_roi_x0, tl_local[1] + tl_roi_y0)
            if DEBUG:
                print(f'[DEBUG] TL corner found at: {tl}')
            
            # Restrict search area for BR corner
            br_roi_x0 = min(max(tl[0] + 50, 0), fw - 1)
            br_roi_y0 = min(max(tl[1] + 20, 0), fh - 1)
            br_roi_x1 = fw
            br_roi_y1 = min(int(fh * 0.6), fh)
            
            # Ensure BR ROI is valid
            if br_roi_x0 >= br_roi_x1 or br_roi_y0 >= br_roi_y1:
                if DEBUG:
                    print(f'[DEBUG] Invalid BR ROI bounds: {br_roi_x0},{br_roi_y0} to {br_roi_x1},{br_roi_y1}')
                continue
            
            br_roi = self.frame[br_roi_y0:br_roi_y1, br_roi_x0:br_roi_x1]
            if br_roi.size == 0:
                if DEBUG:
                    print('[DEBUG] BR ROI is empty')
                continue
            
            if DEBUG:
                print(f'[DEBUG] Searching for BR corner in ROI...')
            _, br_local = utils.single_match(br_roi, MM_BR_TEMPLATE)
            br = (br_local[0] + br_roi_x0, br_local[1] + br_roi_y0)
            if DEBUG:
                print(f'[DEBUG] BR corner found at: {br}')
            
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
                    print(f'[DEBUG] Invalid minimap crop bounds: mm_tl={mm_tl}, mm_br={mm_br}')
                continue
            
            self.minimap_sample = self.frame[mm_tl[1]:mm_br[1], mm_tl[0]:mm_br[0]]
            if self.minimap_sample.size == 0:
                if DEBUG:
                    print('[DEBUG] Minimap sample is empty')
                continue
            
            if DEBUG:
                print(f'[DEBUG] Calibration successful! Minimap size: {mm_br[0]-mm_tl[0]}x{mm_br[1]-mm_tl[1]}')
            self.calibrated = True

            with mss.mss() as self.sct:
                while True:
                    if not self.calibrated:
                        break

                    # Take screenshot
                    self.frame = self.screenshot()
                    if self.frame is None:
                        continue

                    # Crop the frame to only show the minimap
                    minimap = self.frame[mm_tl[1]:mm_br[1], mm_tl[0]:mm_br[0]]
                    
                    # Convert BGRA to BGR for multi_match (which expects BGR format)
                    minimap_bgr = cv2.cvtColor(minimap, cv2.COLOR_BGRA2BGR)

                    # Determine the player's position using the first matching template
                    player = []
                    for name, tpl in PLAYER_TEMPLATES:
                        thr = 0.6
                        # Slightly lower threshold for larger/new template
                        if name.endswith('player_template_new.png'):
                            thr = 0.55
                        player = utils.multi_match(minimap_bgr, tpl, threshold=thr)
                        if player:
                            break
                    
                    if player:
                        config.player_pos = utils.convert_to_relative(player[0], minimap)

                    # Package display information to be polled by GUI
                    self.minimap = {
                        'minimap': minimap,
                        'rune_active': config.bot.rune_active,
                        'rune_pos': config.bot.rune_pos,
                        'path': config.path,
                        'player_pos': config.player_pos
                    }

                    if not self.ready:
                        self.ready = True
                    time.sleep(0.001)

    def screenshot(self, delay=1):
        try:
            return np.array(self.sct.grab(self.window))
        except mss.exception.ScreenShotError:
            print(f'\n[!] Error while taking screenshot, retrying in {delay} second'
                  + ('s' if delay != 1 else ''))
            time.sleep(delay)
