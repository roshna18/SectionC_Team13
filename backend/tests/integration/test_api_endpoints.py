"""Integration tests for all REST API endpoints."""

import io
from unittest.mock import MagicMock
import numpy as np
import pytest
from fastapi.testclient import TestClient
from app.ml.model_loader import set_model_for_testing


def test_root_endpoint(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "SmartPark AI" in data["name"]
    assert "docs" in data


def test_health_endpoint(client: TestClient):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "model_loaded" in data


def test_spaces_crud_endpoints(client: TestClient):
    # 1. Get spaces initially
    res = client.get("/api/spaces")
    assert res.status_code == 200
    assert "spaces" in res.json()

    # 2. Save invalid payload
    bad_res = client.post("/api/spaces", json={"spaces": "not-a-list"})
    assert bad_res.status_code == 422  # Pydantic validation error

    # 3. Save valid spaces
    payload = {"spaces": [{"id": "P1", "box": [10, 10, 50, 50]}]}
    save_res = client.post("/api/spaces", json=payload)
    assert save_res.status_code == 200
    assert save_res.json()["count"] == 1


def test_analyze_rejects_empty_or_non_image(client: TestClient):
    # Text file upload should be rejected
    files = {"file": ("test.txt", b"plain text content", "text/plain")}
    res = client.post("/api/analyze", files=files)
    assert res.status_code == 400
    assert "Unsupported image format" in res.json()["detail"]


def test_analyze_with_mock_model(client: TestClient, sample_image_bytes: bytes):
    # Mock YOLO prediction result
    mock_box = MagicMock()
    mock_box.cls.item.return_value = 0
    mock_box.conf.item.return_value = 0.92
    mock_box.xyxy = [MagicMock()]
    mock_box.xyxy[0].tolist.return_value = [20.0, 20.0, 100.0, 150.0]

    mock_prediction = MagicMock()
    mock_prediction.boxes = [mock_box]
    mock_prediction.names = {0: "space_vacant"}

    mock_yolo = MagicMock()
    mock_yolo.predict.return_value = [mock_prediction]

    # Inject mock detector
    set_model_for_testing(mock_yolo)

    files = {"file": ("parking.jpg", sample_image_bytes, "image/jpeg")}
    response = client.post("/api/analyze", files=files)

    assert response.status_code == 200
    data = response.json()
    assert data["total_spaces"] == 1
    assert data["vacant"] == 1
    assert data["occupied"] == 0
    assert data["occupancy_percent"] == 0.0
    assert data["spaces_available"] is True
    assert data["annotated_image"].startswith("data:image/jpeg;base64,")
    assert len(data["results"]) == 1
    assert data["results"][0]["id"] == "P1"
    assert data["results"][0]["status"] == "vacant"
