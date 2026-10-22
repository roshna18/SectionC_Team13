"""Parking spaces configuration and legacy endpoints."""

from pathlib import Path
import cv2
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.image_processing.encoder import read_uploaded_image
from app.schemas.spaces import SaveSpacesRequest, SaveSpacesResponse, SpacesResponse
from app.services.spaces_service import spaces_service

router = APIRouter()


@router.get("/spaces", response_model=SpacesResponse, summary="Get saved parking spaces")
def get_spaces() -> SpacesResponse:
    """Retrieve saved parking spaces list."""
    spaces = spaces_service.get_spaces()
    return SpacesResponse(spaces=spaces)


@router.post("/spaces", response_model=SaveSpacesResponse, summary="Save parking spaces")
def save_spaces(payload: SaveSpacesRequest) -> SaveSpacesResponse:
    """Persist parking spaces with schema validation."""
    count = spaces_service.save_spaces(payload.spaces)
    return SaveSpacesResponse(message="Saved.", count=count)


@router.post("/lot/upload", summary="Upload reference parking lot image")
async def upload_lot_image(file: UploadFile = File(...)):
    """Upload a reference image for parking lot marking (kept for backward compatibility)."""
    image = await read_uploaded_image(file)

    destination = settings.STORAGE_DIR / "reference_image.jpg"
    success = cv2.imwrite(str(destination), image)

    if not success:
        raise HTTPException(status_code=500, detail="Could not save reference image.")

    return {"message": "Image uploaded successfully."}
