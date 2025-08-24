from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import logging
from pathlib import Path

from .core.config import settings
from .api.routes.generation import router as generation_router

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="ManimStudio API",
    description="API for generating mathematical animations from natural language prompts",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173", "http://localhost:5174"],
    allow_credentials=False,  # Disable credentials to allow broader origins in dev
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Static file serving
try:
    # Mount media directory for existing videos
    if settings.MEDIA_PATH.exists():
        app.mount("/static", StaticFiles(directory=str(settings.MEDIA_PATH)), name="static")
        logger.info(f"Mounted static files from {settings.MEDIA_PATH}")
    else:
        logger.warning(f"Media path does not exist: {settings.MEDIA_PATH}")
    
    # Mount output directory for generated videos
    if settings.OUTPUT_VIDEOS_PATH.exists():
        app.mount("/output", StaticFiles(directory=str(settings.OUTPUT_VIDEOS_PATH)), name="output")
        logger.info(f"Mounted output files from {settings.OUTPUT_VIDEOS_PATH}")
    
    # Mount generated scripts directory
    if settings.GENERATED_SCRIPTS_PATH.exists():
        app.mount("/static/generated", StaticFiles(directory=str(settings.GENERATED_SCRIPTS_PATH)), name="generated")
        logger.info(f"Mounted generated scripts from {settings.GENERATED_SCRIPTS_PATH}")

except Exception as e:
    logger.error(f"Error mounting static files: {e}")

# Include routers
app.include_router(generation_router, prefix="/api", tags=["generation"])

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    logger.error(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc) if settings.DEBUG else "An error occurred"
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    logger.info("Starting ManimStudio API...")
    logger.info(f"Debug mode: {settings.DEBUG}")
    logger.info(f"Media path: {settings.MEDIA_PATH}")
    logger.info(f"Output path: {settings.OUTPUT_VIDEOS_PATH}")
    logger.info(f"Generated scripts path: {settings.GENERATED_SCRIPTS_PATH}")
    
    # Ensure directories exist
    settings.GENERATED_SCRIPTS_PATH.mkdir(parents=True, exist_ok=True)
    settings.OUTPUT_VIDEOS_PATH.mkdir(parents=True, exist_ok=True)

# Shutdown event  
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down ManimStudio API...")

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to ManimStudio API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

# Additional health check at root level
@app.get("/health")
async def health():
    return {"status": "healthy", "message": "ManimStudio API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level="info"
    )