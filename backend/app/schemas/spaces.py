"""Pydantic schemas for parking spaces persistence."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field


class ParkingSpace(BaseModel):
    """
    Representation of a parking space.
    Accepts polygon coordinates, bounding box coordinates, or id/label mappings
    to support various frontend manual marking tools without data loss.
    """
    id: Optional[str] = Field(None, description="Space identifier")
    label: Optional[str] = Field(None, description="Custom label or bay number")
    points: Optional[List[List[float]]] = Field(None, description="Polygon vertices [[x, y], ...]")
    box: Optional[List[float]] = Field(None, min_length=4, max_length=4, description="Bounding box [x1, y1, x2, y2]")
    status: Optional[str] = Field(None, description="Initial or assigned status")

    model_config = ConfigDict(extra="allow")


class SaveSpacesRequest(BaseModel):
    spaces: List[Dict[str, Any]] = Field(..., max_length=1000, description="List of space definitions")


class SpacesResponse(BaseModel):
    spaces: List[Dict[str, Any]]


class SaveSpacesResponse(BaseModel):
    message: str = "Saved."
    count: int
