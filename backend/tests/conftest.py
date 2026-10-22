"""Pytest configuration and shared fixtures."""

import os
import tempfile
from pathlib import Path
from typing import Generator
import cv2
import numpy as np
import pytest
from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app
from app.ml.model_loader import set_model_for_testing
from app.services.spaces_service import SpacesService


@pytest.fixture
def temp_storage_dir() -> Generator[Path, None, None]:
    """Provide an isolated temporary directory for file storage tests."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield Path(tmp_dir)


@pytest.fixture
def test_spaces_service(temp_storage_dir: Path) -> SpacesService:
    """Create a spaces service instance using temporary storage."""
    return SpacesService(storage_dir=temp_storage_dir, filename="test_spaces.json")


@pytest.fixture
def sample_test_image() -> np.ndarray:
    """Create a valid synthetic 400x300 BGR test image."""
    img = np.zeros((300, 400, 3), dtype=np.uint8)
    # Draw some boxes to simulate parking bays
    cv2.rectangle(img, (20, 20), (120, 180), (255, 255, 255), -1)
    cv2.rectangle(img, (140, 20), (240, 180), (100, 100, 100), -1)
    return img


@pytest.fixture
def sample_image_bytes(sample_test_image: np.ndarray) -> bytes:
    """Encoded sample test image bytes."""
    success, encoded = cv2.imencode(".jpg", sample_test_image)
    assert success
    return encoded.tobytes()


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """Test client for FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def cleanup_ml_mock():
    """Ensure mock model is cleaned up after each test."""
    yield
    set_model_for_testing(None)
