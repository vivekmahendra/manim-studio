from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import Dict, Any
import logging

from ...models.schemas import (
    GenerateRequest, 
    GenerateResponse, 
    ExampleResponse, 
    ExampleItem,
    HealthResponse,
    ErrorResponse
)
from ...services.ai_service import ai_service
from ...services.manim_service import manim_service
from ...services.file_service import file_service

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
async def generate_animation(request: GenerateRequest, background_tasks: BackgroundTasks):
    """Generate a mathematical animation from a text prompt"""
    try:
        logger.info(f"Generating animation for prompt: {request.prompt[:50]}...")
        
        # Step 1: Generate Manim code using AI service (stubbed)
        ai_result = await ai_service.generate_manim_code(request.prompt)
        
        # Step 2: Check if pre-rendered video exists
        video_path = file_service.check_existing_video(ai_result["class_name"])
        
        if video_path:
            # Use existing video
            video_url = file_service.get_video_url(video_path)
            logger.info(f"Using existing video: {video_url}")
            
            return GenerateResponse(
                video_url=video_url,
                code=ai_result["code"],
                scene_name=ai_result["class_name"],
                status="success",
                description=ai_result["description"]
            )
        else:
            # Need to render new video
            logger.info("No existing video found, would need to render new one")
            
            # Save the generated script
            script_path = await file_service.save_generated_script(
                ai_result["code"], 
                ai_result["class_name"]
            )
            
            # For now, return success without actually rendering
            # In production, this would trigger actual Manim rendering
            return GenerateResponse(
                video_url="/static/placeholder/rendering.mp4",  # Placeholder
                code=ai_result["code"],
                scene_name=ai_result["class_name"],
                status="success",
                description=f"{ai_result['description']} (New render would be triggered)"
            )
            
    except Exception as e:
        logger.error(f"Error generating animation: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to generate animation: {str(e)}"
        )

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
    """Actually render a video (for testing Manim integration)"""
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
            request.quality if hasattr(request, 'quality') else "low_quality"
        )
        
        if render_result["success"]:
            return {
                "video_url": render_result["video_url"],
                "code": ai_result["code"],
                "scene_name": ai_result["class_name"],
                "status": "rendered"
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