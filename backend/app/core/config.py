"""Core application configuration using pydantic-settings or environment variables."""

import os
from pathlib import Path
from typing import List
from pydantic import BaseModel, Field

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseModel):
    # App
    PROJECT_NAME: str = "SmartPark AI"
    API_V1_STR: str = "/api"
    ENV: str = Field(default_factory=lambda: os.getenv("ENV", "development"))
    DEBUG: bool = Field(default_factory=lambda: os.getenv("DEBUG", "false").lower() == "true")

    # Host & Port
    HOST: str = Field(default_factory=lambda: os.getenv("HOST", "127.0.0.1"))
    PORT: int = Field(default_factory=lambda: int(os.getenv("PORT", "8000")))

    # CORS
    CORS_ORIGINS: List[str] = Field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS",
                "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000",
            ).split(",")
            if origin.strip()
        ]
    )

    # Storage paths
    STORAGE_DIR: Path = Field(
        default_factory=lambda: Path(os.getenv("STORAGE_DIR", str(BASE_DIR / "storage")))
    )
    SPACES_FILENAME: str = "parking_spaces.json"
    MAX_FILE_SIZE_BYTES: int = Field(
        default_factory=lambda: int(os.getenv("MAX_FILE_SIZE_BYTES", str(15 * 1024 * 1024)))  # 15 MB
    )

    # ML Model Config
    MODEL_REPO: str = Field(
        default_factory=lambda: os.getenv("MODEL_REPO", "simahanyan/parking-lot-yolo26m")
    )
    MODEL_FILENAME: str = Field(
        default_factory=lambda: os.getenv("MODEL_FILENAME", "weights/parking_lot.pt")
    )
    MODEL_CONFIDENCE_THRESHOLD: float = Field(
        default_factory=lambda: float(os.getenv("MODEL_CONFIDENCE_THRESHOLD", "0.25"))
    )
    MODEL_IMAGE_SIZE: int = Field(
        default_factory=lambda: int(os.getenv("MODEL_IMAGE_SIZE", "1280"))
    )
    PRELOAD_MODEL_ON_STARTUP: bool = Field(
        default_factory=lambda: os.getenv("PRELOAD_MODEL_ON_STARTUP", "false").lower() == "true"
    )

    # Rate Limiting (In-memory token bucket per client IP)
    RATE_LIMIT_ENABLED: bool = Field(
        default_factory=lambda: os.getenv("RATE_LIMIT_ENABLED", "true").lower() == "true"
    )
    RATE_LIMIT_REQUESTS: int = Field(
        default_factory=lambda: int(os.getenv("RATE_LIMIT_REQUESTS", "30"))  # per minute
    )
    RATE_LIMIT_WINDOW_SECONDS: int = Field(
        default_factory=lambda: int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))
    )

    @property
    def SPACES_FILE(self) -> Path:
        return self.STORAGE_DIR / self.SPACES_FILENAME


settings = Settings()
