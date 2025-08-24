from pydantic import BaseModel, Field
from typing import List, Optional

class GenerateRequest(BaseModel):
    prompt: str = Field(..., min_length=1, max_length=500, description="User prompt describing the math concept to animate")
    quality: str = Field("medium", description="Video quality: low, medium, high")

class GenerateResponse(BaseModel):
    video_url: str
    code: str
    scene_name: str
    status: str
    description: Optional[str] = None
    job_id: Optional[str] = None
    progress: Optional[int] = None
    current_step: Optional[str] = None

class ExampleItem(BaseModel):
    title: str
    prompt: str
    video_url: str
    thumbnail_url: Optional[str] = None
    description: str
    category: str
    duration: str

class ExampleResponse(BaseModel):
    examples: List[ExampleItem]

class HealthResponse(BaseModel):
    status: str
    message: str

class ErrorResponse(BaseModel):
    error: str
    message: str
    details: Optional[str] = None

class ProgressResponse(BaseModel):
    job_id: str
    status: str  # 'analyzing', 'generating', 'rendering', 'completed', 'failed'
    progress: int  # 0-100
    current_step: str
    message: Optional[str] = None
    error: Optional[str] = None

class JobStatusResponse(BaseModel):
    job_id: str
    status: str
    progress: int
    current_step: str
    estimated_time_remaining: Optional[int] = None  # seconds
    video_url: Optional[str] = None
    code: Optional[str] = None
    scene_name: Optional[str] = None
    error: Optional[str] = None
    method: Optional[str] = None  # 'openai_generated' | 'sample_fallback' | 'emergency_fallback'
    model: Optional[str] = None
    sample_used: Optional[str] = None