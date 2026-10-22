"""
Backend entry point.
Exports FastAPI `app` from `app.main` for uvicorn compatibility:
    uvicorn main:app --reload
"""

from app.main import app

if __name__ == "__main__":
    import uvicorn
    from app.core.config import settings

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
