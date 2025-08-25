from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import logging
import asyncio
import uuid
from datetime import datetime

from ...models.schemas import (
    GenerateRequest, 
    GenerateResponse, 
    ExampleResponse, 
    ExampleItem,
    HealthResponse,
    ErrorResponse,
    ProgressResponse,
    JobStatusResponse
)
from ...services.ai_service import ai_service
from ...services.manim_service import manim_service
from ...services.file_service import file_service

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

# In-memory job storage (in production, use Redis or database)
job_storage: Dict[str, Dict[str, Any]] = {}

async def update_job_progress(job_id: str, status: str, progress: int, current_step: str, **kwargs):
    """Update job progress in storage"""
    if job_id in job_storage:
        job_storage[job_id].update({
            "status": status,
            "progress": progress,
            "current_step": current_step,
            "last_updated": datetime.now(),
            **kwargs
        })
        # Log video URL when it gets set
        video_url = kwargs.get("video_url")
        if video_url:
            logger.info(f"📊 Job {job_id}: {status} ({progress}%) - {current_step} | Video URL: {video_url}")
        else:
            logger.info(f"📊 Job {job_id}: {status} ({progress}%) - {current_step}")

async def process_generation_job(job_id: str, prompt: str, quality: str = "medium"):
    """Background task to process video generation"""
    try:
        # Step 1: Analyzing prompt (5%)
        await update_job_progress(job_id, "analyzing", 5, "Starting AI analysis of your prompt...")
        await asyncio.sleep(0.5)  # Brief pause
        
        await update_job_progress(job_id, "analyzing", 10, "Understanding mathematical concepts...")
        await asyncio.sleep(0.5)
        
        # Step 2: Generate Manim code (20-40%)
        await update_job_progress(job_id, "generating", 20, "Calling OpenAI to generate animation code...")
        ai_result = await ai_service.generate_manim_code(prompt)
        
        # Step 3: Save script and validate (45%)
        await update_job_progress(job_id, "generating", 45, "Saving and validating generated code...")
        script_path = await file_service.save_generated_script(
            ai_result["code"], 
            ai_result["class_name"]
        )
        
        # Step 4: Validate script (55%)
        await update_job_progress(job_id, "generating", 55, "Running code validation checks...")
        validation = await manim_service.validate_script(script_path)
        if not validation["valid"]:
            await update_job_progress(job_id, "failed", 55, "Code validation failed", 
                                    error=validation["error"])
            return
        
        # Step 5: Check for existing video first (65%)
        await update_job_progress(job_id, "rendering", 65, "Preparing video rendering environment...")
        existing_video = file_service.check_existing_video(ai_result["class_name"])
        
        if existing_video:
            # Use existing video (90%)
            await update_job_progress(job_id, "rendering", 90, "Found existing render, finalizing...")
            video_url = file_service.get_video_url(existing_video)
            await asyncio.sleep(1)  # Brief pause for UI
            
            # Complete (100%)
            await update_job_progress(job_id, "completed", 100, "Animation ready!", 
                                    video_url=video_url,
                                    code=ai_result["code"],
                                    scene_name=ai_result["class_name"],
                                    description=ai_result["description"],
                                    method=ai_result.get("method", "unknown"),
                                    model=ai_result.get("model"),
                                    sample_used=ai_result.get("sample_used"))
        else:
            # Step 6: Render new video (75-95%)
            await update_job_progress(job_id, "rendering", 75, "Starting Manim video rendering...")
            
            # Start actual Manim rendering with job_id for filename tracking
            render_result = await manim_service.render_video(
                script_path, 
                ai_result["class_name"],
                quality,
                job_id  # Pass job_id for unique filename generation
            )
            
            await update_job_progress(job_id, "rendering", 95, "Finalizing video output...")
            
            if render_result["success"]:
                # Complete (100%)
                await update_job_progress(job_id, "completed", 100, "Animation ready!",
                                        video_url=render_result["video_url"],
                                        code=ai_result["code"],
                                        scene_name=ai_result["class_name"],
                                        description=ai_result["description"],
                                        method=ai_result.get("method", "unknown"),
                                        model=ai_result.get("model"),
                                        sample_used=ai_result.get("sample_used"))
            else:
                # Rendering failed
                await update_job_progress(job_id, "failed", 90, "Video rendering failed",
                                        error=render_result["error"])
                
    except Exception as e:
        logger.error(f"Job {job_id} failed: {str(e)}")
        await update_job_progress(job_id, "failed", 0, "Generation failed", error=str(e))

@router.post("/generate", response_model=GenerateResponse)
async def generate_animation(request: GenerateRequest, background_tasks: BackgroundTasks):
    """Start a mathematical animation generation job"""
    try:
        # Create unique job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job in storage
        job_storage[job_id] = {
            "job_id": job_id,
            "prompt": request.prompt,
            "quality": request.quality,
            "status": "initialized",
            "progress": 0,
            "current_step": "Starting generation...",
            "created_at": datetime.now(),
            "last_updated": datetime.now()
        }
        
        # Start background processing
        background_tasks.add_task(process_generation_job, job_id, request.prompt, request.quality)
        
        # Return immediate response with job ID
        return GenerateResponse(
            video_url="",  # Will be populated when complete
            code="",       # Will be populated when complete
            scene_name="",  # Will be populated when complete
            status="processing",
            description="Generation started",
            job_id=job_id,
            progress=0,
            current_step="Starting generation..."
        )
        
    except Exception as e:
        logger.error(f"Error starting generation: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to start generation: {str(e)}"
        )

@router.get("/job/{job_id}/status", response_model=JobStatusResponse)
async def get_job_status(job_id: str):
    """Get the status of a generation job"""
    if job_id not in job_storage:
        raise HTTPException(status_code=404, detail="Job not found")
    
    job = job_storage[job_id]
    
    return JobStatusResponse(
        job_id=job_id,
        status=job["status"],
        progress=job["progress"],
        current_step=job["current_step"],
        video_url=job.get("video_url"),
        code=job.get("code"),
        scene_name=job.get("scene_name"),
        error=job.get("error"),
        method=job.get("method"),
        model=job.get("model"),
        sample_used=job.get("sample_used")
    )

@router.delete("/job/{job_id}")
async def cleanup_job(job_id: str):
    """Clean up a completed job"""
    if job_id in job_storage:
        del job_storage[job_id]
        return {"message": "Job cleaned up successfully"}
    else:
        raise HTTPException(status_code=404, detail="Job not found")

@router.get("/examples", response_model=ExampleResponse)
async def get_examples():
    """Get list of example animations"""
    try:
        # Get sample videos from file service
        sample_videos = file_service.list_sample_videos()
        
        # Create example items with rich metadata
        examples = []
        sample_prompts = ai_service.get_sample_prompts()
        
        for video in sample_videos:
            # Determine category based on video name
            video_name_lower = video["name"].lower()
            if "vector" in video_name_lower:
                category = "algebra"
                title = "Vector Addition & Subtraction"
                prompt = sample_prompts.get("vector", ["Show vector addition"])[0]
                description = "Learn how to add and subtract vectors with animated arrows and step-by-step visualization."
            elif "hyperbola_foci" in video_name_lower:
                category = "geometry" 
                title = "Hyperbola & Foci"
                prompt = sample_prompts.get("hyperbola", ["Show hyperbola with foci"])[0]
                description = "Explore hyperbolas and their foci with interactive geometric visualization."
            elif "hyperbola_teacher" in video_name_lower:
                category = "geometry"
                title = "Hyperbola Teaching Animation"
                prompt = sample_prompts.get("teacher", ["Teach hyperbolas"])[0]
                description = "Educational animation explaining hyperbola properties and mathematical concepts."
            else:
                category = "general"
                title = video["name"].replace("_", " ").title()
                prompt = f"Create an animation about {title.lower()}"
                description = f"Mathematical visualization of {title.lower()}."
            
            examples.append(ExampleItem(
                title=title,
                prompt=prompt,
                video_url=video["url"],
                description=description,
                category=category,
                duration="45-90s"
            ))
        
        return ExampleResponse(examples=examples)
        
    except Exception as e:
        logger.error(f"Error getting examples: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get examples: {str(e)}"
        )

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        message="ManimStudio API is running"
    )

@router.post("/render")
async def render_video(request: GenerateRequest):
    """Direct render endpoint for testing (bypasses job queue)"""
    try:
        # Generate code
        ai_result = await ai_service.generate_manim_code(request.prompt)
        
        # Save script
        script_path = await file_service.save_generated_script(
            ai_result["code"], 
            ai_result["class_name"]
        )
        
        # Validate script
        validation = await manim_service.validate_script(script_path)
        if not validation["valid"]:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid script: {validation['error']}"
            )
        
        # Render video
        render_result = await manim_service.render_video(
            script_path, 
            ai_result["class_name"],
            request.quality
        )
        
        if render_result["success"]:
            return {
                "video_url": render_result["video_url"],
                "code": ai_result["code"],
                "scene_name": ai_result["class_name"],
                "status": "rendered",
                "description": ai_result["description"]
            }
        else:
            raise HTTPException(
                status_code=500,
                detail=f"Rendering failed: {render_result['error']}"
            )
            
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error rendering video: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to render video: {str(e)}"
        )