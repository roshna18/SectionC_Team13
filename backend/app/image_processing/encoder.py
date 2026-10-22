"""Image decoding, validation, and encoding utilities."""

import base64
from pathlib import Path
from typing import Set
import cv2
import numpy as np
from fastapi import UploadFile

from app.core.config import settings
from app.core.exceptions import ImageValidationError

ALLOWED_EXTENSIONS: Set[str] = {".jpg", ".jpeg", ".png", ".webp"}


async def read_uploaded_image(file: UploadFile) -> np.ndarray:
    """
    Validate and decode an uploaded image file.
    
    Raises:
        ImageValidationError: If format, size, or decoding is invalid.
    """
    filename = file.filename or ""
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ImageValidationError(
            f"Unsupported image format '{extension}'. Upload a JPG, JPEG, PNG, or WEBP image."
        )

    content = await file.read(settings.MAX_FILE_SIZE_BYTES + 1)

    if not content:
        raise ImageValidationError("The uploaded image is empty.")

    if len(content) > settings.MAX_FILE_SIZE_BYTES:
        raise ImageValidationError(
            f"The image must be smaller than {settings.MAX_FILE_SIZE_BYTES // (1024 * 1024)} MB."
        )

    # Decode using OpenCV
    image_array = np.frombuffer(content, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    if image is None:
        raise ImageValidationError("Could not read this image. The file may be corrupted.")

    return image


def encode_image_to_base64(image: np.ndarray, quality: int = 90) -> str:
    """
    Encode an OpenCV BGR image to base64 Data URL JPEG string.
    """
    success, encoded = cv2.imencode(
        ".jpg",
        image,
        [cv2.IMWRITE_JPEG_QUALITY, quality],
    )

    if not success or encoded is None:
        raise ImageValidationError("Could not encode the image.")

    encoded_text = base64.b64encode(encoded.tobytes()).decode("ascii")
    return f"data:image/jpeg;base64,{encoded_text}"
