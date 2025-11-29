"""A collection of functions and classes used across multiple modules."""

import math
import os
import sys
import queue
import cv2
import threading
import numpy as np
from src.common import config, settings
from random import random


def run_if_enabled(function):
    """
    Decorator for functions that should only run if the bot is enabled.
    :param function:    The function to decorate.
    :return:            The decorated function.
    """

    def helper(*args, **kwargs):
        if config.enabled:
            return function(*args, **kwargs)

    return helper


def run_if_disabled(message=""):
    """
    Decorator for functions that should only run while the bot is disabled. If MESSAGE
    is not empty, it will also print that message if its function attempts to run when
    it is not supposed to.
    """

    def decorator(function):
        def helper(*args, **kwargs):
            if not config.enabled:
                return function(*args, **kwargs)
            elif message:
                print(message)

        return helper

    return decorator


def distance(a, b):
    """
    Applies the distance formula to two points.
    :param a:   The first point.
    :param b:   The second point.
    :return:    The distance between the two points.
    """

    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


def separate_args(arguments):
    """
    Separates a given array ARGUMENTS into an array of normal arguments and a
    dictionary of keyword arguments.
    :param arguments:    The array of arguments to separate.
    :return:             An array of normal arguments and a dictionary of keyword arguments.
    """

    args = []
    kwargs = {}
    for a in arguments:
        a = a.strip()
        index = a.find("=")
        if index > -1:
            key = a[:index].strip()
            value = a[index + 1 :].strip()
            kwargs[key] = value
        else:
            args.append(a)
    return args, kwargs


def single_match(frame, template, is_gray=False):
    """
    Finds the best match within FRAME.
    :param frame:       The image in which to search for TEMPLATE.
    :param template:    The template to match with.
    :param is_gray:     If True, FRAME is already grayscale (CPU optimization).
    :return:            The top-left and bottom-right positions of the best match.
    """

    # CPU Optimization: Skip color conversion if frame is already grayscale
    if is_gray:
        gray = frame
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF)
    _, _, _, top_left = cv2.minMaxLoc(result)
    w, h = template.shape[::-1]
    bottom_right = (top_left[0] + w, top_left[1] + h)
    return top_left, bottom_right


def multi_match(frame, template, threshold=0.95, is_gray=False, max_results=None):
    """
    Finds all matches in FRAME that are similar to TEMPLATE by at least THRESHOLD.
    :param frame:       The image in which to search.
    :param template:    The template to match with.
    :param threshold:   The minimum percentage of TEMPLATE that each result must match.
    :param is_gray:     If True, FRAME is already grayscale (CPU optimization).
    :return:            An array of matches that exceed THRESHOLD.
    """

    if template.shape[0] > frame.shape[0] or template.shape[1] > frame.shape[1]:
        return []
    # CPU Optimization: Skip color conversion if frame is already grayscale
    if is_gray:
        gray = frame
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    result = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
    matches = []
    while True:
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val < threshold:
            break
        x = int(round(max_loc[0] + template.shape[1] / 2))
        y = int(round(max_loc[1] + template.shape[0] / 2))
        matches.append((x, y, float(max_val)))
        if max_results and len(matches) >= max_results:
            break
        top_left = max_loc
        bottom_right = (
            top_left[0] + template.shape[1],
            top_left[1] + template.shape[0],
        )
        cv2.rectangle(result, top_left, bottom_right, 0, thickness=-1)
    return matches


def multi_match_multi_scale(
    frame,
    template,
    threshold=0.95,
    is_gray=False,
    scales=None,
    max_results=None,
    overlap_threshold=20,
):
    """
    Finds all matches in FRAME that are similar to TEMPLATE at multiple scales.
    This function is useful when the template size may vary in the frame.
    :param frame:           The image in which to search.
    :param template:        The template to match with.
    :param threshold:       The minimum percentage of TEMPLATE that each result must match.
    :param is_gray:         If True, FRAME is already grayscale (CPU optimization).
    :param scales:          List of scales to try (e.g., [0.75, 0.9, 1.0, 1.1, 1.2]).
                            Default: [0.75, 0.85, 0.95, 1.0, 1.1, 1.2, 1.3]
    :param max_results:     Maximum number of results to return.
    :param overlap_threshold: Maximum pixel distance to consider matches as duplicates.
    :return:                An array of matches that exceed THRESHOLD, format: [(x, y, score), ...]
    """
    if scales is None:
        scales = [0.75, 0.85, 0.95, 1.0, 1.1, 1.2, 1.3]

    # CPU Optimization: Skip color conversion if frame is already grayscale
    if is_gray:
        gray = frame
    else:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    all_matches = []
    template_h, template_w = template.shape[:2]

    for scale in scales:
        # Resize template
        new_w = max(5, int(round(template_w * scale)))
        new_h = max(5, int(round(template_h * scale)))

        # Skip if scaled template is larger than frame
        if new_h > gray.shape[0] or new_w > gray.shape[1]:
            continue

        # Skip if scaled template is too small
        if new_h < 5 or new_w < 5:
            continue

        scaled_template = cv2.resize(
            template, (new_w, new_h), interpolation=cv2.INTER_LINEAR
        )

        # Match template
        result = cv2.matchTemplate(gray, scaled_template, cv2.TM_CCOEFF_NORMED)

        # Find all matches above threshold
        result_copy = result.copy()
        while True:
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result_copy)
            if max_val < threshold:
                break

            x = int(round(max_loc[0] + scaled_template.shape[1] / 2))
            y = int(round(max_loc[1] + scaled_template.shape[0] / 2))
            all_matches.append((x, y, float(max_val), scale))

            if max_results and len(all_matches) >= max_results * len(scales):
                break

            # Mask out this match
            top_left = max_loc
            bottom_right = (
                top_left[0] + scaled_template.shape[1],
                top_left[1] + scaled_template.shape[0],
            )
            cv2.rectangle(result_copy, top_left, bottom_right, 0, thickness=-1)

    if not all_matches:
        return []

    # Sort by score (descending) to prioritize best matches
    all_matches.sort(key=lambda x: x[2], reverse=True)

    # Remove overlapping matches (keep highest score)
    filtered_matches = []
    for match in all_matches:
        x, y, score, scale = match
        is_duplicate = False
        for existing in filtered_matches:
            ex, ey, _, _ = existing
            # If within overlap_threshold pixels, consider duplicate
            if abs(x - ex) < overlap_threshold and abs(y - ey) < overlap_threshold:
                is_duplicate = True
                break
        if not is_duplicate:
            filtered_matches.append(match)
            if max_results and len(filtered_matches) >= max_results:
                break

    # Return in format (x, y, score) for compatibility with multi_match
    return [(x, y, score) for x, y, score, _ in filtered_matches]


def _get_minimap_ratio(default=1.0):
    """
    Safely retrieve minimap ratio from config.capture.
    Returns DEFAULT if capture module or ratio is unavailable.
    """
    capture = getattr(config, "capture", None)
    ratio = getattr(capture, "minimap_ratio", None) if capture else None
    try:
        if ratio and float(ratio) > 0:
            return float(ratio)
    except (TypeError, ValueError):
        pass
    return default


def convert_to_relative(point, frame):
    """
    Converts POINT into relative coordinates in the range [0, 1] based on FRAME.
    Normalizes the units of the vertical axis to equal those of the horizontal
    axis by using config.mm_ratio.
    :param point:   The point in absolute coordinates.
    :param frame:   The image to use as a reference.
    :return:        The given point in relative coordinates.
    """

    x = point[0] / frame.shape[1]
    minimap_ratio = _get_minimap_ratio()
    y = point[1] / minimap_ratio / frame.shape[0]
    return x, y


def convert_to_absolute(point, frame):
    """
    Converts POINT into absolute coordinates (in pixels) based on FRAME.
    Normalizes the units of the vertical axis to equal those of the horizontal
    axis by using config.mm_ratio.
    :param point:   The point in relative coordinates.
    :param frame:   The image to use as a reference.
    :return:        The given point in absolute coordinates.
    """

    x = int(round(point[0] * frame.shape[1]))
    minimap_ratio = _get_minimap_ratio()
    y = int(round(point[1] * minimap_ratio * frame.shape[0]))
    return x, y


def filter_color(img, ranges):
    """
    Returns a filtered copy of IMG that only contains pixels within the given RANGES.
    on the HSV scale.
    :param img:     The image to filter.
    :param ranges:  A list of tuples, each of which is a pair upper and lower HSV bounds.
    :return:        A filtered copy of IMG.
    """

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, ranges[0][0], ranges[0][1])
    for i in range(1, len(ranges)):
        mask = cv2.bitwise_or(mask, cv2.inRange(hsv, ranges[i][0], ranges[i][1]))

    # Mask the image
    color_mask = mask > 0
    result = np.zeros_like(img, np.uint8)
    result[color_mask] = img[color_mask]
    return result


LOCATION_DISPLAY_RADIUS_SCALE = 0.65


def draw_location(minimap, pos, color):
    """
    Draws a visual representation of POINT onto MINIMAP. The radius of the circle represents
    the allowed error when moving towards POINT.
    :param minimap:     The image on which to draw.
    :param pos:         The location (as a tuple) to depict.
    :param color:       The color of the circle.
    :return:            None
    """

    center = convert_to_absolute(pos, minimap)
    radius = max(
        2,
        round(
            minimap.shape[1] * settings.move_tolerance * LOCATION_DISPLAY_RADIUS_SCALE
        ),
    )
    cv2.circle(minimap, center, radius, color, 1)


def print_separator():
    """Prints a 3 blank lines for visual clarity."""

    print("\n\n")


def print_state():
    """Prints whether Auto Maple is currently enabled or disabled."""

    print_separator()
    print("#" * 18)
    print(f"#    {'ENABLED ' if config.enabled else 'DISABLED'}    #")
    print("#" * 18)


def closest_point(points, target):
    """
    Returns the point in POINTS that is closest to TARGET.
    :param points:      A list of points to check.
    :param target:      The point to check against.
    :return:            The point closest to TARGET, otherwise None if POINTS is empty.
    """

    if points:
        points.sort(key=lambda p: distance(p, target))
        return points[0]


def bernoulli(p):
    """
    Returns the value of a Bernoulli random variable with probability P.
    :param p:   The random variable's probability of being True.
    :return:    True or False.
    """

    return random() < p


def rand_float(start, end):
    """Returns a random float value in the interval [START, END)."""

    assert start < end, "START must be less than END"
    return (end - start) * random() + start


def get_asset_path(rel_path: str) -> str:
    """
    Resolve asset path both in dev (cwd) and in PyInstaller bundle.
    """
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, rel_path)


##########################
#       Threading        #
##########################
class Async(threading.Thread):
    def __init__(self, function, *args, **kwargs):
        super().__init__()
        self.queue = queue.Queue()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    def run(self):
        self.function(*self.args, **self.kwargs)
        self.queue.put("x")

    def process_queue(self, root):
        def f():
            try:
                self.queue.get_nowait()
            except queue.Empty:
                root.after(100, self.process_queue(root))

        return f


def async_callback(context, function, *args, **kwargs):
    """Returns a callback function that can be run asynchronously by the GUI."""

    def f():
        task = Async(function, *args, **kwargs)
        task.start()
        context.after(100, task.process_queue(context))

    return f
