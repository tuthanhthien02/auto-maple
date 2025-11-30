"""AI solvers for lie detector puzzles: Puzzle and Violetta."""

import os
import sys
import time
import threading
import cv2
import numpy as np
from pathlib import Path
from typing import List, Tuple, Optional, Dict

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from src.common.vkeys import click  # noqa: E402
from src.common.logger import get_logger  # noqa: E402

log = get_logger(__name__)


class PuzzleTargetDetector:
    """Detect puzzle target using YOLOv8 ONNX model."""

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize detector.

        Args:
            model_path: Path to ONNX model (default: auto-detect)
        """
        if model_path is None:
            model_path = os.path.join(
                project_root,
                "ai",
                "lie_detector",
                "puzzle",
                "models",
                "puzzle_target_yolov8n.onnx",
            )

        self.model_path = model_path

        if not os.path.exists(model_path):
            log.warning(f"Model not found: {model_path}")
            self.session = None
            return

        try:
            import onnxruntime as ort

            self.session = ort.InferenceSession(model_path)
            self.input_name = self.session.get_inputs()[0].name
            log.info(f"Loaded puzzle detector model: {model_path}")
        except ImportError:
            log.error(
                "onnxruntime not installed. Install with: pip install onnxruntime"
            )
            self.session = None
        except Exception as e:
            log.error(f"Error loading model: {e}")
            self.session = None

    def detect(
        self, frame: np.ndarray, confidence_threshold: float = 0.5
    ) -> List[Tuple]:
        """
        Detect puzzle target in frame.

        Args:
            frame: Input frame (BGR format, already cropped to ROI)
            confidence_threshold: Minimum confidence score

        Returns:
            List of (bbox, confidence) tuples
            bbox format: (x_min, y_min, x_max, y_max) in pixel coordinates
        """
        if self.session is None:
            return []

        # Preprocess
        input_size = 640
        h, w = frame.shape[:2]
        frame_resized = cv2.resize(frame, (input_size, input_size))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        frame_norm = frame_rgb.astype(np.float32) / 255.0
        frame_input = np.transpose(frame_norm, (2, 0, 1))
        frame_input = np.expand_dims(frame_input, axis=0)

        # Inference
        try:
            outputs = self.session.run(None, {self.input_name: frame_input})

            # Parse YOLO output (simplified - adjust based on actual model output)
            # YOLOv8 output format: [batch, num_detections, 6] where 6 = [x, y, w, h, conf, class]
            if len(outputs) == 0:
                return []

            detections = outputs[0][0]  # [num_detections, 6]

            results = []
            for det in detections:
                x_center, y_center, width, height, conf, class_id = det

                if conf < confidence_threshold:
                    continue

                # Convert to pixel coordinates
                x_min = int((x_center - width / 2) * w)
                y_min = int((y_center - height / 2) * h)
                x_max = int((x_center + width / 2) * w)
                y_max = int((y_center + height / 2) * h)

                results.append(((x_min, y_min, x_max, y_max), float(conf)))

            # Sort by confidence
            results.sort(key=lambda x: x[1], reverse=True)

            return results
        except Exception as e:
            log.error(f"Error during inference: {e}")
            return []


class PuzzleTracker:
    """Track puzzle target across frames using Kalman Filter."""

    def __init__(self):
        """Initialize tracker."""
        try:
            from filterpy.kalman import KalmanFilter

            self.kf = KalmanFilter(dim_x=4, dim_z=2)

            # State: [x, y, vx, vy]
            self.kf.x = np.array([0, 0, 0, 0])
            self.kf.F = np.array(
                [
                    [1, 0, 1, 0],
                    [0, 1, 0, 1],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1],
                ]
            )
            self.kf.H = np.array(
                [
                    [1, 0, 0, 0],
                    [0, 1, 0, 0],
                ]
            )
            self.kf.P *= 1000
            self.kf.R = 5
            self.kf.Q = np.eye(4) * 0.1

            self.initialized = False
            log.info("Puzzle tracker initialized")
        except ImportError:
            log.warning("filterpy not installed. Tracking disabled.")
            self.kf = None
            self.initialized = False

    def update(self, bbox: Tuple[int, int, int, int]):
        """
        Update tracker with new detection.

        Args:
            bbox: (x_min, y_min, x_max, y_max)
        """
        if self.kf is None:
            return

        x_min, y_min, x_max, y_max = bbox
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2

        if not self.initialized:
            self.kf.x = np.array([center_x, center_y, 0, 0])
            self.initialized = True
        else:
            self.kf.update(np.array([center_x, center_y]))

        self.kf.predict()

    def predict(self) -> Optional[Tuple[int, int, int, int]]:
        """
        Predict target position.

        Returns:
            Predicted bbox (x_min, y_min, x_max, y_max) or None
        """
        if self.kf is None or not self.initialized:
            return None

        self.kf.predict()
        x, y = self.kf.x[0], self.kf.x[1]

        # Assume fixed size (adjust based on actual target size)
        size = 30
        return (int(x - size), int(y - size), int(x + size), int(y + size))


class PuzzleSolver:
    """Solver for puzzle lie detector using object detection and tracking."""

    def __init__(self, detector: PuzzleTargetDetector, tracker: PuzzleTracker):
        """
        Initialize solver.

        Args:
            detector: Puzzle target detector
            tracker: Puzzle target tracker
        """
        self.detector = detector
        self.tracker = tracker
        self.confidence_threshold = 0.5
        self.running = False
        self.solved = False

    def solve(
        self, frame: np.ndarray, puzzle_window_bbox: Tuple[int, int, int, int]
    ) -> Dict:
        """
        Solve puzzle by following target.

        Args:
            frame: Full frame
            puzzle_window_bbox: (x, y, w, h) of puzzle window in frame

        Returns:
            Status dict: {'status': 'solved'|'in_progress'|'failed', ...}
        """
        if self.solved:
            return {"status": "solved"}

        # Crop to puzzle window
        x, y, w, h = puzzle_window_bbox
        roi = frame[y : y + h, x : x + w]

        if roi.size == 0:
            return {"status": "failed", "reason": "invalid_roi"}

        # Detect target
        detections = self.detector.detect(roi, self.confidence_threshold)

        if detections:
            bbox, confidence = detections[0]
            self.tracker.update(bbox)
            target_pos = bbox
        else:
            # Use predicted position from tracker
            predicted = self.tracker.predict()
            if predicted is None:
                return {"status": "failed", "reason": "no_detection"}
            target_pos = predicted

        # Calculate center position relative to puzzle window
        x_min, y_min, x_max, y_max = target_pos
        center_x = (x_min + x_max) / 2
        center_y = (y_min + y_max) / 2

        # Convert to absolute screen coordinates
        abs_x = x + int(center_x)
        abs_y = y + int(center_y)

        # Move mouse to target (smooth movement would be better, but simple click for now)
        click((abs_x, abs_y), button="left")

        # Check if solved (simplified - should check for success message)
        # For now, assume solved after some time or when target disappears
        time.sleep(0.1)  # Small delay

        return {"status": "in_progress", "target_pos": (abs_x, abs_y)}

    def stop(self):
        """Stop solver."""
        self.running = False

    def reset(self):
        """Reset solver state."""
        self.solved = False
        self.tracker.initialized = False


class ViolettaTargetDetector:
    """Detect Violetta with make-up using YOLOv8 ONNX model."""

    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize detector.

        Args:
            model_path: Path to ONNX model (default: auto-detect)
        """
        if model_path is None:
            model_path = os.path.join(
                project_root,
                "ai",
                "lie_detector",
                "violetta",
                "models",
                "violetta_target_yolov8n.onnx",
            )

        self.model_path = model_path

        if not os.path.exists(model_path):
            log.warning(f"Model not found: {model_path}")
            self.session = None
            return

        try:
            import onnxruntime as ort

            self.session = ort.InferenceSession(model_path)
            self.input_name = self.session.get_inputs()[0].name
            log.info(f"Loaded violetta detector model: {model_path}")
        except ImportError:
            log.error(
                "onnxruntime not installed. Install with: pip install onnxruntime"
            )
            self.session = None
        except Exception as e:
            log.error(f"Error loading model: {e}")
            self.session = None

    def detect(
        self, frame: np.ndarray, confidence_threshold: float = 0.5
    ) -> List[Tuple]:
        """
        Detect Violetta with make-up in frame.

        Args:
            frame: Input frame (BGR format, already cropped to ROI)
            confidence_threshold: Minimum confidence score

        Returns:
            List of (bbox, confidence) tuples
            bbox format: (x_min, y_min, x_max, y_max) in pixel coordinates
        """
        if self.session is None:
            return []

        # Preprocess
        input_size = 640
        h, w = frame.shape[:2]
        frame_resized = cv2.resize(frame, (input_size, input_size))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        frame_norm = frame_rgb.astype(np.float32) / 255.0
        frame_input = np.transpose(frame_norm, (2, 0, 1))
        frame_input = np.expand_dims(frame_input, axis=0)

        # Inference
        try:
            outputs = self.session.run(None, {self.input_name: frame_input})

            # Parse YOLO output
            # YOLOv8 output format depends on export, typically: [batch, num_detections, 6]
            # where 6 = [x_center, y_center, width, height, conf, class_id] (normalized)
            if len(outputs) == 0:
                return []

            # Handle different YOLO output formats
            output = outputs[0]

            # If output is 2D: [num_detections, 6]
            if len(output.shape) == 2:
                detections = output
            # If output is 3D: [batch, num_detections, 6]
            elif len(output.shape) == 3:
                detections = output[0]
            else:
                log.warning(f"Unexpected YOLO output shape: {output.shape}")
                return []

            results = []
            for det in detections:
                if len(det) < 6:
                    continue

                (
                    x_center_norm,
                    y_center_norm,
                    width_norm,
                    height_norm,
                    conf,
                    class_id,
                ) = det[:6]

                if conf < confidence_threshold:
                    continue

                # Convert normalized coordinates to pixel coordinates
                x_center = x_center_norm * w
                y_center = y_center_norm * h
                bbox_width = width_norm * w
                bbox_height = height_norm * h

                x_min = int(x_center - bbox_width / 2)
                y_min = int(y_center - bbox_height / 2)
                x_max = int(x_center + bbox_width / 2)
                y_max = int(y_center + bbox_height / 2)

                # Clamp to frame bounds
                x_min = max(0, min(x_min, w))
                y_min = max(0, min(y_min, h))
                x_max = max(0, min(x_max, w))
                y_max = max(0, min(y_max, h))

                results.append(((x_min, y_min, x_max, y_max), float(conf)))

            # Sort by confidence
            results.sort(key=lambda x: x[1], reverse=True)

            return results
        except Exception as e:
            log.error(f"Error during inference: {e}")
            return []


class ViolettaClassifier:
    """Classify Violetta puzzle state using ONNX model."""

    def __init__(
        self, model_path: Optional[str] = None, classes_path: Optional[str] = None
    ):
        """
        Initialize classifier.

        Args:
            model_path: Path to ONNX model
            classes_path: Path to class mapping JSON
        """
        if model_path is None:
            model_path = os.path.join(
                project_root,
                "ai",
                "lie_detector",
                "violetta",
                "models",
                "violetta_classifier.onnx",
            )

        if classes_path is None:
            classes_path = os.path.join(
                project_root,
                "ai",
                "lie_detector",
                "violetta",
                "models",
                "violetta_classes.json",
            )

        self.model_path = model_path
        self.classes_path = classes_path

        # Load class mapping
        import json

        if os.path.exists(classes_path):
            with open(classes_path, "r") as f:
                class_mapping = json.load(f)
                self.id_to_class = {int(k): v for k, v in class_mapping.items()}
        else:
            self.id_to_class = {}
            log.warning(f"Class mapping not found: {classes_path}")

        if not os.path.exists(model_path):
            log.warning(f"Model not found: {model_path}")
            self.session = None
            return

        try:
            import onnxruntime as ort

            self.session = ort.InferenceSession(model_path)
            self.input_name = self.session.get_inputs()[0].name
            log.info(f"Loaded violetta classifier model: {model_path}")
        except ImportError:
            log.error(
                "onnxruntime not installed. Install with: pip install onnxruntime"
            )
            self.session = None
        except Exception as e:
            log.error(f"Error loading model: {e}")
            self.session = None

    def classify(self, frame: np.ndarray) -> Tuple[Optional[str], float]:
        """
        Classify frame.

        Args:
            frame: Input frame (BGR format, already cropped to ROI)

        Returns:
            (class_name, confidence) or (None, 0.0) if error
        """
        if self.session is None:
            return (None, 0.0)

        # Preprocess
        input_size = 224
        frame_resized = cv2.resize(frame, (input_size, input_size))
        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
        frame_norm = frame_rgb.astype(np.float32) / 255.0

        # ImageNet normalization
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        frame_norm = (frame_norm - mean) / std

        frame_input = np.transpose(frame_norm, (2, 0, 1))
        frame_input = np.expand_dims(frame_input, axis=0)

        # Inference
        try:
            outputs = self.session.run(None, {self.input_name: frame_input})
            logits = outputs[0][0]

            # Get predicted class
            class_id = int(np.argmax(logits))
            confidence = float(np.max(logits))

            class_name = self.id_to_class.get(class_id, f"class_{class_id}")

            return (class_name, confidence)
        except Exception as e:
            log.error(f"Error during inference: {e}")
            return (None, 0.0)


class ViolettaSolver:
    """Solver for Violetta lie detector using YOLO detection."""

    def __init__(
        self,
        detector: Optional[ViolettaTargetDetector] = None,
        classifier: Optional[ViolettaClassifier] = None,
    ):
        """
        Initialize solver.

        Args:
            detector: Violetta target detector (YOLO) - preferred
            classifier: Violetta classifier (fallback, deprecated)
        """
        self.detector = detector
        self.classifier = classifier  # Fallback for backward compatibility
        self.confidence_threshold = 0.5
        self.running = False
        self.solved = False

        # Load action mapping
        from ai.lie_detector.violetta.violetta_actions import ACTION_MAP

        self.action_map = ACTION_MAP

    def _determine_click_position(
        self, bbox: Tuple[int, int, int, int], frame_width: int, frame_height: int
    ) -> str:
        """
        Determine click position based on bounding box location.

        Args:
            bbox: (x_min, y_min, x_max, y_max) in pixel coordinates
            frame_width: Width of ROI frame
            frame_height: Height of ROI frame

        Returns:
            Action name: "click_top_left", "click_top_right", "click_bottom_left", "click_bottom_right"
        """
        x_min, y_min, x_max, y_max = bbox

        # Calculate center of bounding box
        bbox_center_x = (x_min + x_max) / 2
        bbox_center_y = (y_min + y_max) / 2

        # Divide frame into 4 quadrants
        mid_x = frame_width / 2
        mid_y = frame_height / 2

        # Determine quadrant
        if bbox_center_x < mid_x and bbox_center_y < mid_y:
            return "click_top_left"
        elif bbox_center_x >= mid_x and bbox_center_y < mid_y:
            return "click_top_right"
        elif bbox_center_x < mid_x and bbox_center_y >= mid_y:
            return "click_bottom_left"
        else:
            return "click_bottom_right"

    def solve(
        self, frame: np.ndarray, violet_window_bbox: Tuple[int, int, int, int]
    ) -> Dict:
        """
        Solve Violetta puzzle by detecting Violetta with make-up and clicking.

        Args:
            frame: Full frame
            violet_window_bbox: (x, y, w, h) of violet window in frame

        Returns:
            Status dict: {'status': 'solved'|'in_progress'|'waiting'|'failed', ...}
        """
        if self.solved:
            return {"status": "solved"}

        # Crop to violet window
        x, y, w, h = violet_window_bbox
        roi = frame[y : y + h, x : x + w]

        if roi.size == 0:
            return {"status": "failed", "reason": "invalid_roi"}

        # Try YOLO detection first (preferred)
        if self.detector:
            detections = self.detector.detect(
                roi, confidence_threshold=self.confidence_threshold
            )

            if detections:
                # Get best detection (highest confidence)
                bbox, confidence = detections[0]

                # Determine click position based on bbox location
                action_name = self._determine_click_position(bbox, w, h)
                action = self.action_map.get(action_name)

                if action and action["type"] == "click":
                    # Click at center of bounding box (more accurate than quadrant center)
                    x_min, y_min, x_max, y_max = bbox
                    bbox_center_x = (x_min + x_max) / 2
                    bbox_center_y = (y_min + y_max) / 2

                    # Convert to absolute screen coordinates
                    abs_x = x + int(bbox_center_x)
                    abs_y = y + int(bbox_center_y)

                    click((abs_x, abs_y), button="left")
                    time.sleep(0.2)  # Wait for action to complete

                    return {
                        "status": "in_progress",
                        "action": action_name,
                        "confidence": confidence,
                        "bbox": bbox,
                    }
                else:
                    return {
                        "status": "failed",
                        "reason": f"invalid_action: {action_name}",
                    }
            else:
                # No detection - might be wait state or success
                return {"status": "waiting", "reason": "no_detection"}

        # Fallback to classification (backward compatibility)
        elif self.classifier:
            class_name, confidence = self.classifier.classify(roi)

            if class_name is None:
                return {"status": "failed", "reason": "classification_error"}

            if confidence < 0.7:  # Higher threshold for classification
                return {
                    "status": "waiting",
                    "reason": "low_confidence",
                    "confidence": confidence,
                }

            # Get action
            action = self.action_map.get(class_name)
            if action is None:
                return {"status": "failed", "reason": f"unknown_class: {class_name}"}

            # Execute action
            if action["type"] == "click":
                rel_x = action["x"]
                rel_y = action["y"]
                abs_x = x + int(w * rel_x)
                abs_y = y + int(h * rel_y)

                click((abs_x, abs_y), button="left")
                time.sleep(0.2)

            elif action["type"] == "wait":
                time.sleep(action.get("duration", 0.5))

            elif action["type"] == "success":
                self.solved = True
                return {"status": "solved"}

            return {
                "status": "in_progress",
                "class": class_name,
                "confidence": confidence,
                "action": action,
            }
        else:
            return {"status": "failed", "reason": "no_detector_or_classifier"}

    def stop(self):
        """Stop solver."""
        self.running = False

    def reset(self):
        """Reset solver state."""
        self.solved = False


class LieDetectorSolverManager:
    """Manager for lie detector solvers."""

    def __init__(self):
        """Initialize manager."""
        self.puzzle_solver = None
        self.violetta_solver = None
        self.puzzle_thread = None
        self.violetta_thread = None
        self.running = False

    def initialize_solvers(self):
        """Initialize solvers (lazy loading)."""
        if self.puzzle_solver is None:
            detector = PuzzleTargetDetector()
            tracker = PuzzleTracker()
            self.puzzle_solver = PuzzleSolver(detector, tracker)
            log.info("Puzzle solver initialized")

        if self.violetta_solver is None:
            # Try YOLO detector first (preferred)
            detector = ViolettaTargetDetector()
            classifier = None

            # Fallback to classifier if detector not available
            if detector.session is None:
                log.warning(
                    "Violetta YOLO detector not available, falling back to classifier"
                )
                classifier = ViolettaClassifier()

            self.violetta_solver = ViolettaSolver(
                detector=detector, classifier=classifier
            )
            log.info("Violetta solver initialized")

    def start_puzzle_solver(
        self, frame: np.ndarray, puzzle_window_bbox: Tuple[int, int, int, int]
    ):
        """Start puzzle solver in separate thread."""
        if self.puzzle_thread and self.puzzle_thread.is_alive():
            return  # Already running

        self.initialize_solvers()
        self.puzzle_solver.reset()
        self.puzzle_solver.running = True

        def solve_loop():
            while self.puzzle_solver.running:
                result = self.puzzle_solver.solve(frame, puzzle_window_bbox)
                if result["status"] in ["solved", "failed"]:
                    break
                time.sleep(0.1)  # 10 FPS

        self.puzzle_thread = threading.Thread(target=solve_loop, daemon=True)
        self.puzzle_thread.start()
        log.info("Puzzle solver started")

    def start_violetta_solver(
        self, frame: np.ndarray, violet_window_bbox: Tuple[int, int, int, int]
    ):
        """Start violetta solver in separate thread."""
        if self.violetta_thread and self.violetta_thread.is_alive():
            return  # Already running

        self.initialize_solvers()
        self.violetta_solver.reset()
        self.violetta_solver.running = True

        def solve_loop():
            while self.violetta_solver.running:
                result = self.violetta_solver.solve(frame, violet_window_bbox)
                if result["status"] in ["solved", "failed"]:
                    break
                time.sleep(0.2)  # 5 FPS

        self.violetta_thread = threading.Thread(target=solve_loop, daemon=True)
        self.violetta_thread.start()
        log.info("Violetta solver started")

    def stop_all(self):
        """Stop all solvers."""
        if self.puzzle_solver:
            self.puzzle_solver.stop()
        if self.violetta_solver:
            self.violetta_solver.stop()
        log.info("All solvers stopped")
