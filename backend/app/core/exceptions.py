"""Domain and API exceptions."""

from fastapi import HTTPException, status


class SmartParkException(Exception):
    """Base exception for application."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ImageValidationError(SmartParkException):
    """Raised when an uploaded image fails validation."""
    pass


class ModelInferenceError(SmartParkException):
    """Raised when ML model fails to load or infer."""
    pass


class StorageError(SmartParkException):
    """Raised when persistence operations fail."""
    pass


class RateLimitExceededError(SmartParkException):
    """Raised when rate limit is exceeded."""
    pass
