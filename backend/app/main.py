"""FastAPI application factory and middleware configuration."""

from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.router import api_router
from app.core.config import settings
from app.core.exceptions import (
    ImageValidationError,
    ModelInferenceError,
    RateLimitExceededError,
    StorageError,
)
from app.core.logging import logger
from app.ml.model_loader import get_model


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan manager.
    Optionally preloads the model on startup if configured.
    """
    logger.info(f"Starting {settings.PROJECT_NAME} in '{settings.ENV}' environment.")

    if settings.PRELOAD_MODEL_ON_STARTUP:
        logger.info("Preload flag enabled: initializing YOLO parking model on startup...")
        try:
            get_model()
            logger.info("Startup model preloading completed.")
        except Exception as exc:
            logger.error(f"Startup model preloading failed: {exc}", exc_info=True)

    yield

    logger.info(f"Shutting down {settings.PROJECT_NAME}.")


def create_app() -> FastAPI:
    """Create and configure FastAPI application instance."""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description="Smart parking occupancy analysis API powered by computer vision.",
        version="1.0.0",
        lifespan=lifespan,
    )

    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Central exception handlers
    @app.exception_handler(ImageValidationError)
    async def image_validation_exception_handler(request: Request, exc: ImageValidationError):
        logger.warning(f"Image validation error on {request.url.path}: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": exc.message},
        )

    @app.exception_handler(ModelInferenceError)
    async def model_inference_exception_handler(request: Request, exc: ModelInferenceError):
        logger.error(f"Model inference error on {request.url.path}: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": (
                    "The parking model could not run. "
                    "Check server logs for details or verify model configuration."
                )
            },
        )

    @app.exception_handler(StorageError)
    async def storage_exception_handler(request: Request, exc: StorageError):
        logger.error(f"Storage error on {request.url.path}: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": exc.message},
        )

    @app.exception_handler(RateLimitExceededError)
    async def rate_limit_exception_handler(request: Request, exc: RateLimitExceededError):
        logger.warning(f"Rate limit exceeded on {request.url.path}: {exc.message}")
        return JSONResponse(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            content={"detail": exc.message},
        )

    # Root informational route
    @app.get("/", tags=["Info"])
    def home():
        return {
            "name": settings.PROJECT_NAME,
            "message": "Parking detection API is running.",
            "docs": "/docs",
        }

    # Mount API routers
    app.include_router(api_router, prefix=settings.API_V1_STR)

    return app


app = create_app()
