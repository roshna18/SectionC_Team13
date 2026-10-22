"""Parking spaces prediction logic using YOLO detector."""

import threading
from typing import List, Tuple
import numpy as np

from app.core.config import settings
from app.core.exceptions import ModelInferenceError
from app.core.logging import logger
from app.image_processing.annotations import classify_label
from app.ml.model_loader import get_model
from app.schemas.analyze import DetectionItem

_inference_lock = threading.Lock()


def predict_parking_spaces(
    image: np.ndarray,
    confidence_threshold: float = None,
    image_size: int = None,
) -> Tuple[List[DetectionItem], int, int]:
    """
    Run YOLO detection on an image to detect parking bays.
    
    Returns:
        Tuple of (detections_list, image_height, image_width)
    """
    conf = confidence_threshold if confidence_threshold is not None else settings.MODEL_CONFIDENCE_THRESHOLD
    imgsz = image_size if image_size is not None else settings.MODEL_IMAGE_SIZE

    height, width = image.shape[:2]

    try:
        model = get_model()
        # Protect inference across concurrent requests if underlying backend requires thread isolation
        with _inference_lock:
            predictions = model.predict(
                source=image,
                conf=conf,
                imgsz=imgsz,
                verbose=False,
            )
    except Exception as exc:
        logger.error(f"Inference execution failed: {exc}", exc_info=True)
        raise ModelInferenceError(f"Model prediction failed: {str(exc)}") from exc

    detections: List[DetectionItem] = []

    for prediction in predictions:
        if prediction.boxes is None:
            continue

        names = prediction.names

        for box in prediction.boxes:
            class_id = int(box.cls.item())
            label = str(names[class_id])
            status = classify_label(label)
            confidence = float(box.conf.item())

            coordinates = box.xyxy[0].tolist()
            x1, y1, x2, y2 = [int(v) for v in coordinates]

            # Constrain to image bounds
            x1 = max(0, min(x1, width - 1))
            x2 = max(0, min(x2, width - 1))
            y1 = max(0, min(y1, height - 1))
            y2 = max(0, min(y2, height - 1))

            detections.append(
                DetectionItem(
                    id=f"P{len(detections) + 1}",
                    label=label,
                    status=status,
                    occupied=(status == "occupied"),
                    confidence=round(confidence, 4),
                    box=[x1, y1, x2, y2],
                )
            )

    return detections, height, width
