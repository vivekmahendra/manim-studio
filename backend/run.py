#!/usr/bin/env python3
"""
ManimStudio API Server Runner

This script starts the FastAPI server for ManimStudio.
"""

import uvicorn
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.main import app
from app.core.config import settings

if __name__ == "__main__":
    print("🎬 Starting ManimStudio API Server...")
    print(f"📍 Host: {settings.HOST}:{settings.PORT}")
    print(f"🔧 Debug mode: {settings.DEBUG}")
    print(f"📁 Media path: {settings.MEDIA_PATH}")
    print(f"🎥 Quality: {settings.MANIM_QUALITY}")
    print("📚 API docs will be available at: http://localhost:8000/docs")
    print("-" * 50)
    
    try:
        uvicorn.run(
            "app.main:app",
            host=settings.HOST,
            port=settings.PORT,
            reload=settings.DEBUG,
            log_level="info" if settings.DEBUG else "warning"
        )
    except KeyboardInterrupt:
        print("\n👋 Shutting down ManimStudio API Server...")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)