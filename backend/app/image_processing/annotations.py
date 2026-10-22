"""Annotation rendering on OpenCV images."""

from typing import List, Tuple
import cv2
import numpy as np

from app.schemas.analyze import DetectionItem

COLOR_VACANT: Tuple[int, int, int] = (0, 200, 0)      # BGR Green
COLOR_OCCUPIED: Tuple[int, int, int] = (0, 0, 255)    # BGR Red
COLOR_UNKNOWN: Tuple[int, int, int] = (160, 160, 160) # BGR Grey


def classify_label(label: str) -> str:
    """
    Map raw model detection class label to application status ('vacant', 'occupied', 'unknown').
    """
    name = label.lower().replace("_", "-").replace(" ", "-")

    if any(keyword in name for keyword in ("empty", "vacant", "free")):
        return "vacant"

    if any(keyword in name for keyword in ("occupied", "filled", "taken")):
        return "occupied"

    return "unknown"


def draw_detection_annotations(image: np.ndarray, detections: List[DetectionItem]) -> np.ndarray:
    """
    Draw bounding boxes and status labels on a copy of the input image.
    """
    annotated = image.copy()

    for item in detections:
        status = item.status
        if status == "vacant":
            color = COLOR_VACANT
        elif status == "occupied":
            color = COLOR_OCCUPIED
        else:
            color = COLOR_UNKNOWN

        x1, y1, x2, y2 = item.box
        display_label = (
            f"{status.upper()} {item.confidence:.0%}"
            if status != "unknown"
            else f"{item.label} {item.confidence:.0%}"
        )

        # Draw bounding box
        cv2.rectangle(
            annotated,
            (x1, y1),
            (x2, y2),
            color,
            2,
        )

        # Draw text label above box
        text_y = max(22, y1 - 8)
        cv2.putText(
            annotated,
            display_label,
            (x1, text_y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            color,
            2,
            cv2.LINE_AA,
        )

    return annotated
