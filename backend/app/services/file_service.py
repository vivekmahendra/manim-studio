import os
import uuid
import aiofiles
from pathlib import Path
from typing import Optional, List
from ..core.config import settings

class FileService:
    def __init__(self):
        self.generated_scripts_path = settings.GENERATED_SCRIPTS_PATH
        self.output_videos_path = settings.OUTPUT_VIDEOS_PATH
        self.media_path = settings.MEDIA_PATH
        
    async def save_generated_script(self, code: str, class_name: str) -> Path:
        """Save generated Manim script to file"""
        filename = f"{class_name}_{uuid.uuid4().hex[:8]}.py"
        file_path = self.generated_scripts_path / filename
        
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(code)
            
        return file_path
    
    def check_existing_video(self, scene_name: str) -> Optional[str]:
        """Check if a pre-rendered video exists for the scene"""
        # Check in the media/videos directory for existing videos
        media_videos_path = self.media_path / "videos"
        
        if not media_videos_path.exists():
            return None
        
        # Convert CamelCase scene name to snake_case for matching
        def camel_to_snake(name):
            import re
            # Insert underscore before uppercase letters (except the first one)
            s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
            # Insert underscore before uppercase letters preceded by lowercase
            return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()
        
        snake_case_scene = camel_to_snake(scene_name)
        
        # Look for directories matching the scene name
        for video_dir in media_videos_path.iterdir():
            if video_dir.is_dir():
                dir_name = video_dir.name.lower()
                scene_lower = scene_name.lower()
                
                # Try multiple matching strategies
                if (dir_name == snake_case_scene or  # Exact snake_case match
                    dir_name == scene_lower or       # Exact lowercase match
                    scene_lower in dir_name or       # Scene name contained in dir
                    dir_name in scene_lower):        # Dir name contained in scene
                    
                    # Look for the actual video file
                    quality_dirs = ["480p15", "720p30", "1080p60"]
                    
                    for quality_dir in quality_dirs:
                        quality_path = video_dir / quality_dir
                        if quality_path.exists():
                            # Look for mp4 files
                            for video_file in quality_path.glob("*.mp4"):
                                # Return relative path from media directory
                                return f"videos/{video_dir.name}/{quality_dir}/{video_file.name}"
        
        return None
    
    def get_video_url(self, video_path: str) -> str:
        """Convert video path to URL"""
        # If this is a newly generated video (in output directory), use /output/
        if video_path.endswith('.mp4') and not video_path.startswith('videos/'):
            return f"/output/{video_path}"
        # Otherwise, use /static/ for sample videos from media directory
        return f"/static/{video_path}"
    
    async def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up old generated files"""
        import time
        current_time = time.time()
        max_age_seconds = max_age_hours * 3600
        
        # Clean generated scripts
        for file_path in self.generated_scripts_path.glob("*.py"):
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                file_path.unlink()
                
        # Clean output videos (but not the sample ones in media/)
        for file_path in self.output_videos_path.glob("*.mp4"):
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                file_path.unlink()
    
    def generate_unique_filename(self, base_name: str, extension: str, job_id: str = None) -> str:
        """Generate a unique filename with optional job_id"""
        unique_id = uuid.uuid4().hex[:8]
        if job_id:
            # Include job_id in filename for better tracking
            return f"{base_name}_{job_id}_{unique_id}.{extension}"
        return f"{base_name}_{unique_id}.{extension}"
    
    def list_sample_videos(self) -> List[dict]:
        """List all available sample videos"""
        samples = []
        media_videos_path = self.media_path / "videos"
        
        if not media_videos_path.exists():
            return samples
            
        for video_dir in media_videos_path.iterdir():
            if video_dir.is_dir():
                # Look for the actual video file
                quality_dirs = ["480p15", "720p30", "1080p60"]
                
                for quality_dir in quality_dirs:
                    quality_path = video_dir / quality_dir
                    if quality_path.exists():
                        for video_file in quality_path.glob("*.mp4"):
                            video_path = f"videos/{video_dir.name}/{quality_dir}/{video_file.name}"
                            samples.append({
                                "name": video_dir.name,
                                "path": video_path,
                                "url": self.get_video_url(video_path)
                            })
                            break  # Take first video found
                        break  # Take first quality found
        
        return samples

# Global file service instance
file_service = FileService()