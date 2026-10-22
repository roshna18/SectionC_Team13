"""Unit tests for spaces service, storage, and validation."""

import json
from pathlib import Path
import pytest
from app.core.exceptions import StorageError
from app.schemas.spaces import ParkingSpace, SaveSpacesRequest
from app.services.spaces_service import SpacesService


def test_get_spaces_empty_initially(test_spaces_service: SpacesService):
    assert test_spaces_service.get_spaces() == []


def test_save_and_retrieve_spaces(test_spaces_service: SpacesService):
    sample_data = [
        {"id": "slot-1", "label": "Bay A1", "box": [10, 10, 50, 80], "status": "vacant"},
        {"id": "slot-2", "label": "Bay A2", "box": [60, 10, 100, 80], "status": "occupied"},
    ]
    count = test_spaces_service.save_spaces(sample_data)
    assert count == 2

    loaded = test_spaces_service.get_spaces()
    assert len(loaded) == 2
    assert loaded[0]["id"] == "slot-1"
    assert loaded[1]["status"] == "occupied"


def test_save_spaces_rejects_non_list(test_spaces_service: SpacesService):
    with pytest.raises(StorageError):
        test_spaces_service.save_spaces({"not": "a list"})  # type: ignore


def test_pydantic_spaces_validation():
    # Valid model
    valid_space = ParkingSpace(
        id="space_1",
        label="Space 1",
        box=[10.0, 20.0, 30.0, 40.0],
        custom_legacy_field="preserved_value",
    )
    assert valid_space.id == "space_1"
    assert valid_space.model_dump()["custom_legacy_field"] == "preserved_value"

    # Valid SaveSpacesRequest
    req = SaveSpacesRequest(spaces=[{"id": "1", "box": [0, 0, 10, 10]}])
    assert len(req.spaces) == 1
