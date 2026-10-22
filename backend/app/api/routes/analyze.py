"""Analysis API routes."""

from fastapi import APIRouter, File, Request, UploadFile

from app.core.rate_limit import limiter
from app.schemas.analyze import AnalyzeResponse
from app.services.analysis_service import analysis_service

router = APIRouter()


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    summary="Analyze parking lot image",
    description="Detect parking spaces and compute occupancy status (vacant/occupied).",
)
async def analyze_image_endpoint(
    request: Request,
    file: UploadFile = File(...),
) -> AnalyzeResponse:
    # Check rate limit before performing heavy ML analysis
    limiter.check(request)

    return await analysis_service.analyze_image_file(file=file)
