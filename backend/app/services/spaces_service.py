"""Parking spaces persistence and storage service."""

import json
import os
import tempfile
from pathlib import Path
from typing import Any, Dict, List

from app.core.config import settings
from app.core.exceptions import StorageError
from app.core.logging import logger


class SpacesService:
    def __init__(self, storage_dir: Path = None, filename: str = None):
        self.storage_dir = storage_dir or settings.STORAGE_DIR
        self.filename = filename or settings.SPACES_FILENAME
        self._ensure_storage_dir()

    def _ensure_storage_dir(self) -> None:
        try:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        except Exception as exc:
            logger.error(f"Failed to create storage directory {self.storage_dir}: {exc}")
            raise StorageError(f"Cannot initialize storage directory: {exc}") from exc

    @property
    def file_path(self) -> Path:
        return self.storage_dir / self.filename

    def get_spaces(self) -> List[Dict[str, Any]]:
        """
        Retrieve saved parking spaces list.
        Returns empty list if file doesn't exist or is invalid.
        """
        if not self.file_path.exists():
            return []

        try:
            content = self.file_path.read_text(encoding="utf-8")
            data = json.loads(content)
            return data if isinstance(data, list) else []
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning(f"Error reading spaces file {self.file_path}: {exc}")
            return []

    def save_spaces(self, spaces: List[Dict[str, Any]]) -> int:
        """
        Atomic save of parking spaces list to disk to prevent corrupt partial writes.
        """
        if not isinstance(spaces, list):
            raise StorageError("Spaces data must be a list.")

        self._ensure_storage_dir()

        # Write to temporary file in the same directory, then rename atomically
        try:
            with tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                dir=str(self.storage_dir),
                delete=False,
            ) as tmp:
                json.dump(spaces, tmp, indent=2)
                tmp_path = Path(tmp.name)

            tmp_path.replace(self.file_path)
            logger.info(f"Successfully saved {len(spaces)} spaces to {self.file_path}")
            return len(spaces)
        except Exception as exc:
            logger.error(f"Failed to save spaces: {exc}", exc_info=True)
            raise StorageError(f"Could not persist spaces: {str(exc)}") from exc


spaces_service = SpacesService()
