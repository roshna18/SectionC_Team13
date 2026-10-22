"""Central API router aggregating all endpoints."""

from fastapi import APIRouter

from app.api.routes import analyze, spaces
from app.ml.model_loader import is_model_loaded
from app.schemas.analyze import HealthResponse

api_router = APIRouter()


@api_router.get("/health", response_model=HealthResponse, summary="Service health check")
def health() -> HealthResponse:
    """Service and model loading status."""
    return HealthResponse(
        status="ok",
        model_loaded=is_model_loaded(),
    )


# Mount feature routes
api_router.include_router(analyze.router, tags=["Analysis"])
api_router.include_router(spaces.router, tags=["Spaces"])
