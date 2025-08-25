from pydantic_settings import BaseSettings
from pathlib import Path
import os

class Settings(BaseSettings):
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = True
    
    # Manim settings
    MANIM_QUALITY: str = "low_quality"  # For faster testing: low_quality, medium_quality, high_quality
    MANIM_FORMAT: str = "mp4"
    MANIM_FPS: int = 30
    MANIM_PYTHON_PATH: str = "/usr/bin/python3"  # Python interpreter for running Manim
    
    # Paths - relative to backend directory
    BASE_DIR: Path = Path(__file__).parent.parent.parent
    GENERATED_SCRIPTS_PATH: Path = BASE_DIR / "generated"
    OUTPUT_VIDEOS_PATH: Path = BASE_DIR / "output"
    SAMPLE_SCRIPTS_PATH: Path = BASE_DIR / "output-scripts"
    MEDIA_PATH: Path = BASE_DIR / "media"
    
    # Limits
    MAX_PROMPT_LENGTH: int = 500
    VIDEO_TIMEOUT: int = 120  # seconds
    MAX_CONCURRENT_RENDERS: int = 3
    
    # CORS settings
    CORS_ORIGINS: str = "*"
    
    # OpenAI settings
    OPENAI_API_KEY: str = ""  # Must be set in .env file
    OPENAI_MODEL: str = "gpt-4o"
    OPENAI_MAX_TOKENS: int = 4000
    OPENAI_TEMPERATURE: float = 0.3
    OPENAI_TIMEOUT: int = 30
    
    @property
    def cors_origins(self) -> list:
        """Parse CORS_ORIGINS string into list"""
        if self.CORS_ORIGINS == "*":
            return ["*"]
        return [origin.strip() for origin in self.CORS_ORIGINS.split(",")]
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()