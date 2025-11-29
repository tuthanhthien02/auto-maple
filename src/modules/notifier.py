"""A module for detecting and notifying the user of dangerous in-game events."""

import os
import sys
import threading
import time

import cv2
import numpy as np
import pygame

from src.common import config, utils
from src.common.logger import get_logger
from src.routine.components import Point

try:
    import keyboard as kb  # noqa: WPS433
except ImportError:  # pragma: no cover
    kb = None  # type: ignore

log = get_logger(__name__)

# Debug flag for lie detector tuning (keep code but disable logs by default)
LIE_DEBUG = False


def get_asset_path(rel_path):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)


# A rune's symbol on the minimap
RUNE_RANGES = (((141, 148, 245), (146, 158, 255)),)
rune_filtered = utils.filter_color(
    cv2.imread(get_asset_path("assets/rune_template.png")), RUNE_RANGES
)
RUNE_TEMPLATE = cv2.cvtColor(rune_filtered, cv2.COLOR_BGR2GRAY)

# Other players' symbols on the minimap
OTHER_RANGES = (((0, 245, 215), (10, 255, 255)),)
other_filtered = utils.filter_color(
    cv2.imread(get_asset_path("assets/other_template.png")), OTHER_RANGES
)
OTHER_TEMPLATE = cv2.cvtColor(other_filtered, cv2.COLOR_BGR2GRAY)

# The Elite Boss's warning sign
ELITE_TEMPLATE = cv2.imread(get_asset_path("assets/elite_template.jpg"), 0)

# Lie Detector templates - using pre-cropped templates
PUZZLE_TEMPLATE = cv2.imread(
    get_asset_path("assets/lie-detector/puzzle_crop.png"), cv2.IMREAD_GRAYSCALE
)
VIOLET_TEMPLATE = cv2.imread(
    get_asset_path("assets/lie-detector/violet_crop.png"), cv2.IMREAD_GRAYSCALE
)
CAPTCHA_TEMPLATE = cv2.imread(
    get_asset_path("assets/lie-detector/captcha_crop.png"), cv2.IMREAD_GRAYSCALE
)

# Log template info for debugging
if PUZZLE_TEMPLATE is not None:
    log.debug(f"Puzzle template loaded: {PUZZLE_TEMPLATE.shape}")
else:
    log.warning("Puzzle template failed to load!")

if VIOLET_TEMPLATE is not None:
    log.debug(f"Violet template loaded: {VIOLET_TEMPLATE.shape}")
else:
    log.warning("Violet template failed to load!")

if CAPTCHA_TEMPLATE is not None:
    log.debug(f"Captcha template loaded: {CAPTCHA_TEMPLATE.shape}")
else:
    log.warning("Captcha template failed to load!")


def get_alert_path(name):
    return os.path.join(Notifier.ALERTS_DIR, f"{name}.mp3")


class Notifier:
    ALERTS_DIR = os.path.join("assets", "alerts")

    def __init__(self):
        """Initializes this Notifier object's main thread."""

        pygame.mixer.init()
        self.mixer = pygame.mixer.music

        self.ready = False
        self.thread = threading.Thread(target=self._main)
        self.thread.daemon = True

        self.room_change_threshold = 0.9
        self.rune_alert_delay = 270  # 4.5 minutes
        self.last_lie_detector_check = time.time()
        self.last_lie_detector_sound_time = 0.0
        self.lie_detector_sound_cooldown = 23.0  # seconds (length of siren)
        self.lie_detector_channel = None
        self.lie_detector_threshold = 0.5
        self.lie_detector_edge_threshold = 0.35
        self.lie_detector_edge_confirm_margin = 0.05
        self.lie_detector_min_scale = 0.6
        self.lie_detector_max_scale = 1.6
        self._lie_detector_last_debug = 0.0
        self._lie_detector_color_lower = (100, 80, 70)
        self._lie_detector_color_upper = (130, 255, 255)
        self._lie_detector_color_area_threshold = 15000
        self.lie_templates = [
            tmpl
            for tmpl in (PUZZLE_TEMPLATE, VIOLET_TEMPLATE, CAPTCHA_TEMPLATE)
            if tmpl is not None
        ]

        config.notifier = self

    def start(self):
        """Starts this Notifier's thread."""

        log.info("Started notifier")
        self.thread.start()

    def _main(self):
        self.ready = True
        prev_others = 0
        rune_start_time = time.time()
        consecutive_errors = 0
        max_consecutive_errors = 10

        # CPU Optimization: Throttle checks with different intervals
        last_black_check = time.time()
        last_elite_check = time.time()
        last_others_check = time.time()
        last_rune_check = time.time()
        last_lie_detector_check = time.time()

        while True:
            try:
                if config.enabled:
                    current_time = time.time()
                    frame = config.capture.frame
                    height, width, _ = frame.shape
                    # Bug fix: Thread-safe minimap access
                    with config.capture._minimap_lock:
                        minimap = (
                            config.capture.minimap["minimap"]
                            if config.capture.minimap
                            else None
                        )

                    # CPU Optimization: Check black screen every 0.2s (5 Hz)
                    if current_time - last_black_check > 0.2:
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        if (
                            np.count_nonzero(gray < 15) / height / width
                            > self.room_change_threshold
                        ):
                            self._alert("siren")
                        last_black_check = current_time

                    # CPU Optimization: Check elite warning every 0.5s (2 Hz)
                    if current_time - last_elite_check > 0.5:
                        elite_frame = frame[
                            height // 4 : 3 * height // 4, width // 4 : 3 * width // 4
                        ]
                        # CPU Optimization: Pre-convert to grayscale once
                        elite_frame_gray = cv2.cvtColor(elite_frame, cv2.COLOR_BGR2GRAY)
                        elite = utils.multi_match(
                            elite_frame_gray,
                            ELITE_TEMPLATE,
                            threshold=0.9,
                            is_gray=True,
                        )
                        if len(elite) > 0:
                            self._alert("siren")
                        last_elite_check = current_time

                    # CPU Optimization: Check other players every 0.3s (~3.3 Hz)
                    if current_time - last_others_check > 0.3:
                        filtered = utils.filter_color(minimap, OTHER_RANGES)
                        # CPU Optimization: Pre-convert to grayscale once
                        filtered_gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
                        others = len(
                            utils.multi_match(
                                filtered_gray,
                                OTHER_TEMPLATE,
                                threshold=0.5,
                                is_gray=True,
                            )
                        )
                        config.stage_fright = others > 0
                        if others != prev_others:
                            if others > prev_others:
                                self._ping("ding")
                            prev_others = others
                        last_others_check = current_time

                    # CPU Optimization: Check rune every 0.5s (2 Hz)
                    now = time.time()
                    if current_time - last_rune_check > 0.5:
                        if not config.bot.rune_active:
                            filtered = utils.filter_color(minimap, RUNE_RANGES)
                            # CPU Optimization: Pre-convert to grayscale once
                            filtered_gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)
                            matches = utils.multi_match(
                                filtered_gray,
                                RUNE_TEMPLATE,
                                threshold=0.9,
                                is_gray=True,
                            )
                            rune_start_time = now
                            if matches and config.routine.sequence:
                                abs_rune_pos = (matches[0][0], matches[0][1])
                                config.bot.rune_pos = utils.convert_to_relative(
                                    abs_rune_pos, minimap
                                )
                                distances = list(
                                    map(distance_to_rune, config.routine.sequence)
                                )
                                index = np.argmin(distances)
                                config.bot.rune_closest_pos = config.routine[
                                    index
                                ].location
                                config.bot.rune_active = True
                                self._ping("rune_appeared", volume=0.75)
                        elif (
                            now - rune_start_time > self.rune_alert_delay
                        ):  # Alert if rune hasn't been solved
                            config.bot.rune_active = False
                            self._alert("siren")
                        last_rune_check = current_time

                    # CPU Optimization: Check lie detector every 0.5s (2 Hz)
                    if current_time - last_lie_detector_check > 0.5:
                        puzzle_matches = []
                        violet_matches = []
                        captcha_matches = []

                        # Puzzle và Violet chỉ xuất hiện ở bottom-right, nên chỉ scan vùng đó
                        if PUZZLE_TEMPLATE is not None or VIOLET_TEMPLATE is not None:
                            # Crop vùng bottom right của game window (nơi popup xuất hiện)
                            # Dò ở vùng bottom-right ~60% (giảm nhiễu, tăng tốc)
                            br_y0 = int(height * 0.4)
                            br_x0 = int(width * 0.4)
                            br_frame = frame[br_y0:height, br_x0:width]

                            # Convert sang grayscale để tối ưu CPU
                            frame_gray = cv2.cvtColor(br_frame, cv2.COLOR_BGR2GRAY)

                            # Multi-scale matching cho puzzle template
                            # Scales từ 0.75 đến 1.3 để cover các kích thước khác nhau
                            if PUZZLE_TEMPLATE is not None:
                                puzzle_matches = utils.multi_match_multi_scale(
                                    frame_gray,
                                    PUZZLE_TEMPLATE,
                                    threshold=0.75,
                                    is_gray=True,
                                    scales=[0.75, 0.85, 0.95, 1.0, 1.1, 1.2, 1.3],
                                )

                            # Multi-scale matching cho violet template
                            if VIOLET_TEMPLATE is not None:
                                violet_matches_raw = utils.multi_match_multi_scale(
                                    frame_gray,
                                    VIOLET_TEMPLATE,
                                    threshold=0.72,  # Tăng từ 0.7 lên 0.72 để giảm false positive
                                    is_gray=True,
                                    scales=[0.75, 0.85, 0.95, 1.0, 1.1, 1.2, 1.3],
                                )

                                # Thêm edge confirmation cho các matches có score gần threshold để giảm false positive
                                violet_matches = []
                                frame_edges = cv2.Canny(frame_gray, 50, 150)
                                for match in violet_matches_raw:
                                    x, y, score = match[0], match[1], match[2]
                                    # Nếu score >= 0.75 thì chấp nhận luôn (high confidence)
                                    if score >= 0.75:
                                        violet_matches.append(match)
                                    # Nếu score trong khoảng 0.72-0.75 thì cần edge confirmation
                                    elif score >= 0.72:
                                        # Extract ROI xung quanh match position
                                        template_h, template_w = VIOLET_TEMPLATE.shape
                                        roi_size = max(template_h, template_w) * 2
                                        roi_x0 = max(0, x - roi_size // 4)
                                        roi_y0 = max(0, y - roi_size // 4)
                                        roi_x1 = min(
                                            frame_gray.shape[1],
                                            x + template_w + roi_size // 4,
                                        )
                                        roi_y1 = min(
                                            frame_gray.shape[0],
                                            y + template_h + roi_size // 4,
                                        )

                                        roi_edges = frame_edges[
                                            roi_y0:roi_y1, roi_x0:roi_x1
                                        ]
                                        if roi_edges.size > 0:
                                            # Tìm scale tốt nhất cho template
                                            best_edge_score = 0.0
                                            for scale in [
                                                0.75,
                                                0.85,
                                                0.95,
                                                1.0,
                                                1.1,
                                                1.2,
                                                1.3,
                                            ]:
                                                new_h = max(
                                                    5, int(round(template_h * scale))
                                                )
                                                new_w = max(
                                                    5, int(round(template_w * scale))
                                                )
                                                if (
                                                    new_h > roi_edges.shape[0]
                                                    or new_w > roi_edges.shape[1]
                                                ):
                                                    continue
                                                scaled_template = cv2.resize(
                                                    VIOLET_TEMPLATE,
                                                    (new_w, new_h),
                                                    interpolation=cv2.INTER_LINEAR,
                                                )
                                                scaled_edge = cv2.Canny(
                                                    scaled_template, 60, 160
                                                )
                                                if (
                                                    scaled_edge.shape[0]
                                                    <= roi_edges.shape[0]
                                                    and scaled_edge.shape[1]
                                                    <= roi_edges.shape[1]
                                                ):
                                                    edge_score = self._match_template(
                                                        roi_edges, scaled_edge
                                                    )
                                                    if edge_score > best_edge_score:
                                                        best_edge_score = edge_score

                                            # Chỉ chấp nhận nếu edge score >= 0.3 (edge confirmation)
                                            if best_edge_score >= 0.3:
                                                violet_matches.append(match)

                            # Debug: In ra max score của violet để tune threshold
                            if LIE_DEBUG and VIOLET_TEMPLATE is not None:
                                max_violet_score = 0.0
                                best_violet_scale = 1.0
                                violet_scales = [0.75, 0.85, 0.95, 1.0, 1.1, 1.2, 1.3]
                                for scale in violet_scales:
                                    new_w = max(
                                        5, int(round(VIOLET_TEMPLATE.shape[1] * scale))
                                    )
                                    new_h = max(
                                        5, int(round(VIOLET_TEMPLATE.shape[0] * scale))
                                    )
                                    if (
                                        new_h > frame_gray.shape[0]
                                        or new_w > frame_gray.shape[1]
                                    ):
                                        continue
                                    if new_h < 5 or new_w < 5:
                                        continue
                                    scaled_template = cv2.resize(
                                        VIOLET_TEMPLATE,
                                        (new_w, new_h),
                                        interpolation=cv2.INTER_LINEAR,
                                    )
                                    violet_result = cv2.matchTemplate(
                                        frame_gray,
                                        scaled_template,
                                        cv2.TM_CCOEFF_NORMED,
                                    )
                                    _, max_val, _, _ = cv2.minMaxLoc(violet_result)
                                    if max_val > max_violet_score:
                                        max_violet_score = max_val
                                        best_violet_scale = scale
                                log.debug(
                                    "Violet max score (multi-scale): %.3f at scale %.2f (threshold: 0.72)",
                                    max_violet_score,
                                    best_violet_scale,
                                )

                        # Captcha có thể xuất hiện random toàn màn hình, nên scan full frame
                        if CAPTCHA_TEMPLATE is not None:
                            # Convert toàn màn hình sang grayscale
                            full_frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                            # Multi-scale matching cho captcha template trên toàn màn hình
                            # Captcha mờ và có background trong suốt, nhưng cần threshold cao hơn để tránh false positive
                            captcha_matches_raw = utils.multi_match_multi_scale(
                                full_frame_gray,
                                CAPTCHA_TEMPLATE,
                                threshold=0.65,  # Tăng từ 0.6 lên 0.65 để giảm false positive
                                is_gray=True,
                                scales=[0.75, 0.85, 0.95, 1.0, 1.1, 1.2, 1.3],
                            )

                            # Thêm edge confirmation cho các matches có score gần threshold để giảm false positive
                            captcha_matches = []
                            full_frame_edges = cv2.Canny(full_frame_gray, 50, 150)
                            for match in captcha_matches_raw:
                                x, y, score = match[0], match[1], match[2]
                                # Nếu score >= 0.7 thì chấp nhận luôn (high confidence)
                                if score >= 0.7:
                                    captcha_matches.append(match)
                                # Nếu score trong khoảng 0.65-0.7 thì cần edge confirmation
                                elif score >= 0.65:
                                    # Extract ROI xung quanh match position
                                    template_h, template_w = CAPTCHA_TEMPLATE.shape
                                    roi_size = max(template_h, template_w) * 2
                                    roi_x0 = max(0, x - roi_size // 4)
                                    roi_y0 = max(0, y - roi_size // 4)
                                    roi_x1 = min(
                                        full_frame_gray.shape[1],
                                        x + template_w + roi_size // 4,
                                    )
                                    roi_y1 = min(
                                        full_frame_gray.shape[0],
                                        y + template_h + roi_size // 4,
                                    )

                                    roi_edges = full_frame_edges[
                                        roi_y0:roi_y1, roi_x0:roi_x1
                                    ]
                                    if roi_edges.size > 0:
                                        # Tìm scale tốt nhất cho template
                                        best_edge_score = 0.0
                                        for scale in [
                                            0.75,
                                            0.85,
                                            0.95,
                                            1.0,
                                            1.1,
                                            1.2,
                                            1.3,
                                        ]:
                                            new_h = max(
                                                5, int(round(template_h * scale))
                                            )
                                            new_w = max(
                                                5, int(round(template_w * scale))
                                            )
                                            if (
                                                new_h > roi_edges.shape[0]
                                                or new_w > roi_edges.shape[1]
                                            ):
                                                continue
                                            scaled_template = cv2.resize(
                                                CAPTCHA_TEMPLATE,
                                                (new_w, new_h),
                                                interpolation=cv2.INTER_LINEAR,
                                            )
                                            scaled_edge = cv2.Canny(
                                                scaled_template, 60, 160
                                            )
                                            if (
                                                scaled_edge.shape[0]
                                                <= roi_edges.shape[0]
                                                and scaled_edge.shape[1]
                                                <= roi_edges.shape[1]
                                            ):
                                                edge_score = self._match_template(
                                                    roi_edges, scaled_edge
                                                )
                                                if edge_score > best_edge_score:
                                                    best_edge_score = edge_score

                                        # Chỉ chấp nhận nếu edge score >= 0.3 (edge confirmation)
                                        if best_edge_score >= 0.3:
                                            captcha_matches.append(match)

                        # Nếu tìm thấy match (puzzle, violet hoặc captcha)
                        puzzle_detected = len(puzzle_matches) > 0
                        violet_detected = len(violet_matches) > 0
                        captcha_detected = len(captcha_matches) > 0

                        if puzzle_detected or violet_detected or captcha_detected:
                            # Xác định loại lie detector và thông tin chi tiết
                            detected_types = []
                            if puzzle_detected:
                                puzzle_max_score = (
                                    max([match[2] for match in puzzle_matches])
                                    if puzzle_matches
                                    else 0.0
                                )
                                detected_types.append(
                                    f"PUZZLE (matches={len(puzzle_matches)}, max_score={puzzle_max_score:.3f})"
                                )
                            if violet_detected:
                                violet_max_score = (
                                    max([match[2] for match in violet_matches])
                                    if violet_matches
                                    else 0.0
                                )
                                detected_types.append(
                                    f"VIOLET (matches={len(violet_matches)}, max_score={violet_max_score:.3f})"
                                )
                            if captcha_detected:
                                captcha_max_score = (
                                    max([match[2] for match in captcha_matches])
                                    if captcha_matches
                                    else 0.0
                                )
                                detected_types.append(
                                    f"CAPTCHA (matches={len(captcha_matches)}, max_score={captcha_max_score:.3f})"
                                )

                            lie_type_str = " + ".join(detected_types)

                            if (
                                current_time - self.last_lie_detector_sound_time
                                > self.lie_detector_sound_cooldown
                            ):
                                log.info(
                                    "Lie detector detected: %s. Playing notification sound.",
                                    lie_type_str,
                                )
                                self._notify_sound("siren")
                                self.last_lie_detector_sound_time = current_time
                            else:
                                log.debug(
                                    "Lie detector detected: %s (sound cooldown active).",
                                    lie_type_str,
                                )
                        last_lie_detector_check = current_time

                # Reset error counter on successful iteration
                consecutive_errors = 0

                # CPU Optimization: 10 Hz instead of 20 Hz (sufficient for notifier)
                time.sleep(0.1)

            except KeyboardInterrupt:
                log.info("Notifier loop interrupted by user")
                raise
            except Exception as e:
                consecutive_errors += 1
                log.error(
                    "Notifier error (consecutive: %d/%d): %s",
                    consecutive_errors,
                    max_consecutive_errors,
                    e,
                    exc_info=True,
                )

                # If too many errors, wait longer before retry
                if consecutive_errors >= max_consecutive_errors:
                    log.warning(
                        "Too many notifier errors, waiting 2 seconds before retry"
                    )
                    consecutive_errors = 0
                    time.sleep(2)
                else:
                    time.sleep(0.2)  # Brief pause before retry

    def _alert(self, name, volume=0.75):
        """
        Plays an alert to notify user of a dangerous event. Stops the alert
        once the key bound to 'Start/stop' is pressed.
        """

        config.enabled = False
        listener = getattr(config, "listener", None)
        if listener is not None:
            listener.enabled = False
        self.mixer.load(get_asset_path(os.path.join(self.ALERTS_DIR, f"{name}.mp3")))
        self.mixer.set_volume(volume)
        self.mixer.play(-1)
        if config.enable_keyboard_listener and kb is not None and listener is not None:
            while not kb.is_pressed(listener.config["Start/stop"]):
                time.sleep(0.1)
        else:
            log.warning(
                "Keyboard listener disabled; stopping alert automatically (no hotkey)."
            )
            time.sleep(2)
        self.mixer.stop()
        time.sleep(2)
        if listener is not None:
            listener.enabled = True

    def _ping(self, name, volume=0.5):
        """A quick notification for non-dangerous events."""
        # Disabled per user request: silent ping (logged at debug level for diagnostics)
        log.debug("Ping '%s' suppressed (volume=%.2f)", name, volume)

    def _notify_sound(self, name, volume=0.5):
        """Play a notification sound once without stopping the bot."""
        try:
            sound_path = get_asset_path(os.path.join(self.ALERTS_DIR, f"{name}.mp3"))
            if os.path.exists(sound_path):
                # Use pygame.mixer.Sound for one-time playback
                sound = pygame.mixer.Sound(sound_path)
                sound.set_volume(volume)
                channel = sound.play()
                if name == "siren":
                    # Stop any previous siren channel before assigning new one
                    self.stop_lie_detector_sound()
                    self.lie_detector_channel = channel
                log.info(f"Played notification sound: {name}")
            else:
                log.warning(f"Sound file not found: {sound_path}")
        except Exception as e:
            log.error(f"Error playing notification sound: {e}")

    def stop_lie_detector_sound(self):
        """Stop the currently playing lie detector siren, if any."""
        if self.lie_detector_channel is not None:
            try:
                if self.lie_detector_channel.get_busy():
                    self.lie_detector_channel.stop()
            except Exception as e:
                log.debug(f"Error stopping lie detector sound: {e}")
            finally:
                self.lie_detector_channel = None
                self.last_lie_detector_sound_time = 0.0

    def _detect_lie_detector(self, frame_bgr):
        """Return True if any lie detector template matches the given frame."""
        rois = self._extract_lie_detector_rois(frame_bgr)
        if not rois:
            if LIE_DEBUG:
                self._save_debug_image(
                    frame_bgr, prefix="lie_roi_fallback", debug_id=int(time.time())
                )
            rois = [self._build_roi_from_frame(frame_bgr)]
        for roi in rois:
            if self._match_lie_detector_roi(roi["gray"], roi["edges"], roi["height"]):
                return True
        return False

    def _extract_lie_detector_rois(self, frame_bgr):
        resized = cv2.resize(frame_bgr, (0, 0), fx=0.5, fy=0.5)
        frame_hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(
            frame_hsv, self._lie_detector_color_lower, self._lie_detector_color_upper
        )
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        rois = []
        h_scale = frame_bgr.shape[0] / resized.shape[0]
        w_scale = frame_bgr.shape[1] / resized.shape[1]
        ts = int(time.time())
        roi_index = 0
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area < self._lie_detector_color_area_threshold:
                continue
            x, y, w, h = cv2.boundingRect(cnt)
            x = int(x * w_scale)
            y = int(y * h_scale)
            w = int(w * w_scale)
            h = int(h * h_scale)
            pad_w = max(10, int(w * 0.15))
            pad_h = max(10, int(h * 0.25))
            x0 = max(x - pad_w, 0)
            y0 = max(y - pad_h, 0)
            x1 = min(x + w + pad_w, frame_bgr.shape[1])
            y1 = min(y + h + pad_h, frame_bgr.shape[0])
            roi_bgr = frame_bgr[y0:y1, x0:x1]
            if roi_bgr.size == 0:
                continue
            if LIE_DEBUG:
                self._save_debug_image(
                    roi_bgr, prefix="lie_roi", debug_id=f"{ts}_{roi_index}"
                )
                roi_index += 1
            roi_gray = cv2.cvtColor(roi_bgr, cv2.COLOR_BGR2GRAY)
            roi_gray = cv2.GaussianBlur(roi_gray, (3, 3), 0)
            roi_edges = cv2.Canny(roi_gray, 50, 150)
            rois.append(
                {
                    "gray": roi_gray,
                    "edges": roi_edges,
                    "height": roi_gray.shape[0],
                }
            )
        return rois

    @staticmethod
    def _build_roi_from_frame(frame_bgr):
        roi_gray = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2GRAY)
        roi_gray = cv2.GaussianBlur(roi_gray, (3, 3), 0)
        roi_edges = cv2.Canny(roi_gray, 50, 150)
        return {
            "gray": roi_gray,
            "edges": roi_edges,
            "height": roi_gray.shape[0],
        }

    def _match_lie_detector_roi(self, roi_gray, roi_edges, roi_height):
        if not self.lie_templates:
            return False
        for template in self.lie_templates:
            base_height = template.shape[0]
            if base_height == 0:
                continue
            scales = self._candidate_scales(roi_height / base_height)
            for scale in scales:
                new_h = max(5, int(round(base_height * scale)))
                new_w = max(5, int(round(template.shape[1] * scale)))
                if new_h > roi_gray.shape[0] or new_w > roi_gray.shape[1]:
                    continue
                scaled_template = cv2.resize(
                    template, (new_w, new_h), interpolation=cv2.INTER_LINEAR
                )
                score = self._match_template(roi_gray, scaled_template)
                if score >= self.lie_detector_threshold:
                    return True
                if score >= (
                    self.lie_detector_threshold - self.lie_detector_edge_confirm_margin
                ):
                    scaled_edge = cv2.Canny(scaled_template, 60, 160)
                    if (
                        scaled_edge.shape[0] <= roi_edges.shape[0]
                        and scaled_edge.shape[1] <= roi_edges.shape[1]
                    ):
                        edge_score = self._match_template(roi_edges, scaled_edge)
                        if edge_score >= self.lie_detector_edge_threshold:
                            return True
        return False

    def _candidate_scales(self, scale_hint):
        candidates = [
            scale_hint,
            scale_hint * 0.92,
            scale_hint * 1.08,
        ]
        normalized = []
        seen = set()
        for scale in candidates:
            scale = float(
                np.clip(scale, self.lie_detector_min_scale, self.lie_detector_max_scale)
            )
            key = round(scale, 2)
            if key in seen:
                continue
            seen.add(key)
            normalized.append(scale)
        return normalized

    @staticmethod
    def _match_template(frame, template):
        if template.shape[0] > frame.shape[0] or template.shape[1] > frame.shape[1]:
            return 0.0
        result = cv2.matchTemplate(frame, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val

    @staticmethod
    def _save_debug_image(image, prefix, debug_id):
        try:
            debug_path = os.path.join(
                "logs",
                f"{prefix}_{debug_id}.png",
            )
            cv2.imwrite(debug_path, image)
        except Exception:
            pass


#################################
#       Helper Functions        #
#################################
def distance_to_rune(point):
    """
    Calculates the distance from POINT to the rune.
    :param point:   The position to check.
    :return:        The distance from POINT to the rune, infinity if it is not a Point object.
    """

    if isinstance(point, Point):
        return utils.distance(config.bot.rune_pos, point.location)
    return float("inf")
