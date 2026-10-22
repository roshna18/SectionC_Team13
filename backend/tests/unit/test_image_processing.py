"""Unit tests for image encoding, decoding, validation, and annotations."""

import numpy as np
import pytest
from app.core.exceptions import ImageValidationError
from app.image_processing.annotations import (
    classify_label,
    draw_detection_annotations,
)
from app.image_processing.encoder import encode_image_to_base64
from app.schemas.analyze import DetectionItem


def test_classify_label():
    assert classify_label("space_empty") == "vacant"
    assert classify_label("vacant_spot") == "vacant"
    assert classify_label("free_parking") == "vacant"
    assert classify_label("occupied_car") == "occupied"
    assert classify_label("car_filled") == "occupied"
    assert classify_label("unknown_object") == "unknown"


def test_encode_image_to_base64(sample_test_image: np.ndarray):
    data_url = encode_image_to_base64(sample_test_image)
    assert data_url.startswith("data:image/jpeg;base64,")
    assert len(data_url) > 100


def test_draw_detection_annotations(sample_test_image: np.ndarray):
    detections = [
        DetectionItem(
            id="P1",
            label="empty",
            status="vacant",
            occupied=False,
            confidence=0.95,
            box=[10, 10, 100, 100],
        ),
        DetectionItem(
            id="P2",
            label="car",
            status="occupied",
            occupied=True,
            confidence=0.88,
            box=[110, 10, 200, 100],
        ),
    ]

    annotated = draw_detection_annotations(sample_test_image, detections)
    assert annotated.shape == sample_test_image.shape
    # Ensure drawing made modifications on the pixel canvas
    assert not np.array_equal(annotated, sample_test_image)
