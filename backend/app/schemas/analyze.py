"""Pydantic schemas for analysis requests and responses."""

from typing import List, Optional
from pydantic import BaseModel, Field


class DetectionItem(BaseModel):
    id: str = Field(..., description="Unique space identifier, e.g. P1")
    label: str = Field(..., description="Model detection class label")
    status: str = Field(..., description="Classified status: vacant, occupied, or unknown")
    occupied: bool = Field(..., description="Whether the spot is occupied")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence score")
    box: List[int] = Field(..., min_length=4, max_length=4, description="Bounding box [x1, y1, x2, y2]")


class AnalyzeResponse(BaseModel):
    message: str = "Parking image analyzed successfully."
    total_spaces: int = Field(..., ge=0)
    occupied: int = Field(..., ge=0)
    vacant: int = Field(..., ge=0)
    unknown: int = Field(..., ge=0)
    occupancy_percent: float = Field(..., ge=0.0, le=100.0)
    vehicle_count: Optional[int] = None
    results: List[DetectionItem]
    detections: List[DetectionItem]
    annotated_image: str = Field(..., description="Data URL base64 encoded JPEG")
    spaces_available: bool
    note: str
    image_width: int = Field(..., gt=0)
    image_height: int = Field(..., gt=0)


class HealthResponse(BaseModel):
    status: str = "ok"
    model_loaded: bool
