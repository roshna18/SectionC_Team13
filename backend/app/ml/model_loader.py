"""ML model loader and lifecycle management."""

import threading
from typing import Optional
from huggingface_hub import hf_hub_download
from ultralytics import YOLO

from app.core.config import settings
from app.core.exceptions import ModelInferenceError
from app.core.logging import logger

_model: Optional[YOLO] = None
_model_lock = threading.Lock()


def get_model() -> YOLO:
    """
    Get or lazily load the singleton YOLO parking model weights.
    Thread-safe initialization.
    """
    global _model

    if _model is not None:
        return _model

    with _model_lock:
        if _model is None:
            logger.info(
                f"Loading model weights from repo '{settings.MODEL_REPO}', file '{settings.MODEL_FILENAME}'"
            )
            try:
                weights_path = hf_hub_download(
                    repo_id=settings.MODEL_REPO,
                    filename=settings.MODEL_FILENAME,
                )
                logger.info(f"Model weights downloaded/cached at: {weights_path}")
                _model = YOLO(weights_path)
                logger.info("YOLO parking model successfully loaded into memory.")
            except Exception as exc:
                logger.error(f"Failed to download or load model: {exc}", exc_info=True)
                raise ModelInferenceError(
                    f"Parking model could not be initialized: {str(exc)}"
                ) from exc

    return _model


def is_model_loaded() -> bool:
    """Check if the model is currently loaded in memory."""
    return _model is not None


def set_model_for_testing(mock_model: Optional[YOLO]) -> None:
    """Utility for unit testing to inject a mock YOLO detector."""
    global _model
    with _model_lock:
        _model = mock_model
