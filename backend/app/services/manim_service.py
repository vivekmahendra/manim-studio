import asyncio
import subprocess
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any
from ..core.config import settings
from .file_service import file_service

# Set up logging
logger = logging.getLogger(__name__)

class ManimService:
    def __init__(self):
        self.output_path = settings.OUTPUT_VIDEOS_PATH
        self.quality = settings.MANIM_QUALITY
        self.timeout = settings.VIDEO_TIMEOUT
        
    async def render_video(self, script_path: Path, scene_name: str, quality: str = None, job_id: str = None) -> Dict[str, Any]:
        """Render a Manim script to video"""
        if quality is None:
            quality = self.quality
            
        # Generate output filename with job_id for better tracking
        output_filename = file_service.generate_unique_filename(scene_name, "mp4", job_id)
        output_path = self.output_path / output_filename
        
        # Build manim command without preview flag (removes desktop video opening)
        quality_flag = "-ql" if "low" in quality else "-qh"
        
        cmd = [
            settings.MANIM_PYTHON_PATH,  # Use configured Python interpreter
            "-m", "manim",              # Run manim as Python module
            quality_flag,
            str(script_path),
            scene_name
        ]
        
        logger.info(f"🎬 Starting video render for scene: {scene_name}")
        logger.info(f"📝 Script: {script_path}")
        logger.info(f"🔧 Command: {' '.join(cmd)}")
        
        try:
            # Run manim command asynchronously
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=str(script_path.parent)
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), 
                timeout=self.timeout
            )
            
            if process.returncode == 0:
                # Find the video file in Manim's default output structure
                # Manim creates: media/videos/script_name/quality/scene_name.mp4
                script_name = script_path.stem
                quality_dir = "480p15" if "l" in quality_flag else "720p30"
                
                # Look for the generated video in expected path
                manim_output_path = script_path.parent / "media" / "videos" / script_name / quality_dir / f"{scene_name}.mp4"
                
                logger.info(f"🔍 Looking for video at expected path: {manim_output_path}")
                
                if manim_output_path.exists() and manim_output_path.stat().st_size > 1000:  # Ensure it's not just a tiny partial file
                    # Move the video to our output directory
                    import shutil
                    shutil.move(str(manim_output_path), str(output_path))
                    
                    video_url = f"/output/{output_filename}"
                    logger.info(f"✅ Video rendered and moved successfully: {output_filename}")
                    logger.info(f"🔗 Video URL: {video_url}")
                    return {
                        "success": True,
                        "video_path": output_filename,
                        "video_url": video_url,
                        "message": "Video rendered successfully"
                    }
                else:
                    # Search for any .mp4 files in the media directory
                    media_dir = script_path.parent / "media"
                    if media_dir.exists():
                        all_video_files = list(media_dir.rglob("*.mp4"))
                        # Filter out tiny files (likely partial renders)
                        video_files = [f for f in all_video_files if f.stat().st_size > 1000]
                        logger.info(f"🔍 Found video files: {[(str(f), f.stat().st_size) for f in all_video_files]}")
                        logger.info(f"🔍 Filtered video files (>1KB): {[(str(f), f.stat().st_size) for f in video_files]}")
                        
                        if video_files:
                            # Find the largest video file (likely the complete render)
                            largest_video = max(video_files, key=lambda f: f.stat().st_size)
                            logger.info(f"📊 Video file sizes: {[(f.name, f.stat().st_size) for f in video_files]}")
                            logger.info(f"✅ Selected largest video: {largest_video.name} ({largest_video.stat().st_size} bytes)")
                            
                            import shutil
                            shutil.move(str(largest_video), str(output_path))
                            video_url = f"/output/{output_filename}"
                            logger.info(f"✅ Video found and moved: {output_filename}")
                            logger.info(f"🔗 Video URL: {video_url}")
                            return {
                                "success": True,
                                "video_path": output_filename,
                                "video_url": video_url,
                                "message": "Video rendered successfully"
                            }
                    
                    logger.error(f"❌ Video file not found after rendering")
                    return {
                        "success": False,
                        "error": "Video file not found after rendering",
                        "stdout": stdout.decode(),
                        "stderr": stderr.decode()
                    }
            else:
                stderr_text = stderr.decode()
                stdout_text = stdout.decode()
                
                logger.error(f"❌ Manim process failed with return code {process.returncode}")
                logger.error(f"STDOUT: {stdout_text}")
                logger.error(f"STDERR: {stderr_text}")
                
                # Analyze the error to provide helpful messages
                if "ModuleNotFoundError: No module named 'manim'" in stderr_text:
                    error_msg = "Manim Python module not found. Please ensure Manim is installed in the Python environment."
                elif "command not found" in stderr_text or "No such file or directory" in stderr_text:
                    error_msg = f"Python interpreter '{settings.MANIM_PYTHON_PATH}' not found. Please check MANIM_PYTHON_PATH setting."
                else:
                    error_msg = f"Manim rendering failed with code {process.returncode}"
                
                return {
                    "success": False,
                    "error": error_msg,
                    "stdout": stdout_text,
                    "stderr": stderr_text
                }
                
        except asyncio.TimeoutError:
            logger.error(f"⏰ Rendering timed out after {self.timeout} seconds")
            return {
                "success": False,
                "error": f"Rendering timed out after {self.timeout} seconds"
            }
        except FileNotFoundError as e:
            logger.error(f"❌ File not found during rendering: {str(e)}")
            logger.error(f"❌ Attempted to use Python path: {settings.MANIM_PYTHON_PATH}")
            logger.error(f"❌ Command: {' '.join(cmd)}")
            error_msg = f"Python interpreter '{settings.MANIM_PYTHON_PATH}' not found. Please check MANIM_PYTHON_PATH setting in .env file."
            return {
                "success": False,
                "error": error_msg
            }
        except Exception as e:
            logger.error(f"❌ Unexpected error during rendering: {str(e)}")
            return {
                "success": False,
                "error": f"Unexpected error during rendering: {str(e)}"
            }
    
    async def validate_script(self, script_path: Path) -> Dict[str, Any]:
        """Validate a Manim script without rendering"""
        try:
            # Simple syntax check
            with open(script_path, 'r') as f:
                code = f.read()
            
            # Try to compile the code
            compile(code, str(script_path), 'exec')
            
            # Check if it has a Scene class
            if 'class ' not in code or 'Scene' not in code:
                return {
                    "valid": False,
                    "error": "No Scene class found in script"
                }
            
            return {
                "valid": True,
                "message": "Script validation passed"
            }
            
        except SyntaxError as e:
            return {
                "valid": False,
                "error": f"Syntax error: {e.msg} at line {e.lineno}"
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}"
            }
    
    def get_available_qualities(self) -> list:
        """Return available video quality options"""
        return ["low_quality", "medium_quality", "high_quality"]
    
    async def get_render_progress(self, job_id: str) -> Dict[str, Any]:
        """Get rendering progress (placeholder for future implementation)"""
        # This would be used for tracking long-running renders
        return {
            "job_id": job_id,
            "status": "completed",
            "progress": 100
        }

# Global manim service instance
manim_service = ManimService()