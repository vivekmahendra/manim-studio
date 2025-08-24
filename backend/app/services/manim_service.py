import asyncio
import subprocess
import os
from pathlib import Path
from typing import Optional, Dict, Any
from ..core.config import settings
from .file_service import file_service

class ManimService:
    def __init__(self):
        self.output_path = settings.OUTPUT_VIDEOS_PATH
        self.quality = settings.MANIM_QUALITY
        self.timeout = settings.VIDEO_TIMEOUT
        
    async def render_video(self, script_path: Path, scene_name: str, quality: str = None) -> Dict[str, Any]:
        """Render a Manim script to video"""
        if quality is None:
            quality = self.quality
            
        # Generate output filename
        output_filename = file_service.generate_unique_filename(scene_name, "mp4")
        output_path = self.output_path / output_filename
        
        # Build manim command
        quality_flag = f"-p{quality[0]}l" if "low" in quality else f"-p{quality[0]}h"
        
        cmd = [
            "manim",
            quality_flag,
            str(script_path),
            scene_name,
            "-o", output_filename,
            "--media_dir", str(self.output_path.parent)
        ]
        
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
                # Check if the video file was created
                if output_path.exists():
                    return {
                        "success": True,
                        "video_path": output_filename,
                        "video_url": f"/static/output/{output_filename}",
                        "message": "Video rendered successfully"
                    }
                else:
                    return {
                        "success": False,
                        "error": "Video file not found after rendering",
                        "stdout": stdout.decode(),
                        "stderr": stderr.decode()
                    }
            else:
                return {
                    "success": False,
                    "error": f"Manim rendering failed with code {process.returncode}",
                    "stdout": stdout.decode(),
                    "stderr": stderr.decode()
                }
                
        except asyncio.TimeoutError:
            return {
                "success": False,
                "error": f"Rendering timed out after {self.timeout} seconds"
            }
        except FileNotFoundError:
            return {
                "success": False,
                "error": "Manim not found. Please ensure Manim is installed and in PATH."
            }
        except Exception as e:
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