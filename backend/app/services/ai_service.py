import asyncio
import re
import logging
from pathlib import Path
from typing import Dict, Any
from openai import AsyncOpenAI
from ..core.config import settings

# Set up logging
logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        # Initialize OpenAI client
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.OPENAI_TIMEOUT
        )
        
        # Load system prompt template
        self.system_prompt = self._load_system_prompt()
    
    def _load_system_prompt(self) -> str:
        """Load the system prompt template from file"""
        try:
            prompt_path = settings.BASE_DIR / "prompts" / "prompt.txt"
            with open(prompt_path, 'r') as f:
                return f.read().strip()
        except FileNotFoundError:
            logger.error(f"System prompt file not found: {prompt_path}")
            return self._get_fallback_prompt()
    
    def _get_fallback_prompt(self) -> str:
        """Fallback system prompt if file is missing"""
        return """You are a veteran math teacher and motion designer. Create one Manim Scene that teaches {TOPIC} clearly, with clean pacing and zero clutter.

Create a single Python file containing one Scene class that:
1. Uses a two-pane layout (left for visuals, right for text board)
2. Teaches the concept step-by-step with clear beats
3. Uses proper Manim syntax and imports
4. Has clean, readable code with appropriate comments
5. Implements proper animations with FadeIn, FadeOut, Create, etc.

Output only the complete Python code for the Manim scene."""
    
    async def generate_manim_code(self, prompt: str) -> Dict[str, Any]:
        """Generate Manim code using OpenAI API"""
        try:
            # Validate prompt
            if not prompt or len(prompt.strip()) == 0:
                raise ValueError("Prompt cannot be empty")
            
            if len(prompt) > settings.MAX_PROMPT_LENGTH:
                raise ValueError(f"Prompt too long. Maximum {settings.MAX_PROMPT_LENGTH} characters.")
            
            logger.info(f"Starting OpenAI generation for prompt: '{prompt[:100]}{'...' if len(prompt) > 100 else ''}'")
            
            # Check if API key is configured
            if not settings.OPENAI_API_KEY or settings.OPENAI_API_KEY == "your_openai_api_key_here":
                logger.error("OpenAI API key not configured properly")
                raise ValueError("OpenAI API key not configured")
            
            # Prepare the prompt with the user's topic
            system_prompt = self.system_prompt.replace("{TOPIC}", prompt)
            
            # Use GPT-5 model
            model_to_use = settings.OPENAI_MODEL
            logger.info(f"Calling OpenAI API with model: {model_to_use}")
            
            # Create simple input combining system prompt and user request
            input_text = f"{system_prompt}\n\nCreate a Manim animation that teaches: {prompt}"
            logger.info(f"📤 Input length: {len(input_text)} chars")
            
            # Call OpenAI API with GPT-5 - simple call without token limits
            response = await self.client.chat.completions.create(
                model=model_to_use,
                messages=[{"role": "user", "content": input_text}]
            )
            
            # Extract raw content from response
            raw_content = response.choices[0].message.content
            finish_reason = response.choices[0].finish_reason
            
            logger.info(f"📝 Raw OpenAI response: {raw_content[:200] if raw_content else 'EMPTY/NULL'}...")
            logger.info(f"📊 Finish reason: {finish_reason}")
            
            if not raw_content:
                logger.error("❌ OpenAI returned empty content!")
                logger.error(f"Full response: {response.choices[0].message.model_dump()}")
                logger.error(f"Finish reason: {finish_reason}")
                raise ValueError(f"No content received from OpenAI (finish_reason: {finish_reason})")
            
            # Clean and extract Python code
            cleaned_code = self._clean_generated_code(raw_content)
            
            # Extract class name from the code
            class_name = self.extract_class_name(cleaned_code)
            
            logger.info(f"✅ Successfully generated OpenAI response")
            logger.info(f"Code length: {len(cleaned_code)} characters")
            logger.info(f"Class name: {class_name}")
            
            return {
                "code": cleaned_code,
                "class_name": class_name,
                "description": f"Mathematical animation for: {prompt}",
                "method": "openai_generated", 
                "model": model_to_use
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI generation failed: {type(e).__name__}: {str(e)}")
            
            # Handle different types of errors
            error_str = str(e).lower()
            
            # Don't fallback for authentication/authorization errors
            if any(keyword in error_str for keyword in ["api_key", "invalid", "unauthorized", "forbidden"]):
                logger.error("❌ Authentication/authorization issue - not falling back to samples")
                raise e
            
            # Re-raise all errors instead of falling back to samples
            raise e
    
    
    def _clean_generated_code(self, code: str) -> str:
        """Clean up generated code by removing markdown formatting"""
        # Remove markdown code blocks
        if "```python" in code:
            code = re.sub(r'^```python\s*\n', '', code, flags=re.MULTILINE)
            code = re.sub(r'\n```\s*$', '', code, flags=re.MULTILINE)
        elif "```" in code:
            code = re.sub(r'^```\s*\n', '', code, flags=re.MULTILINE)
            code = re.sub(r'\n```\s*$', '', code, flags=re.MULTILINE)
        
        return code.strip()
    
    
    def extract_class_name(self, code: str) -> str:
        """Extract the Scene class name from generated code"""
        # Use regex to find class definition
        class_match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
        if class_match:
            return class_match.group(1)
        
        # Fallback to a default name
        return "GeneratedScene"
    
    
    async def validate_generated_code(self, code: str) -> Dict[str, Any]:
        """Validate the generated code for basic requirements"""
        try:
            # Check if code contains required imports
            if "from manim import" not in code:
                return {"valid": False, "error": "Missing 'from manim import' statement"}
            
            # Check if code has a Scene class
            if not re.search(r'class\s+\w+\s*\(\s*Scene\s*\)', code):
                return {"valid": False, "error": "No Scene class found"}
            
            # Check if construct method exists
            if "def construct(" not in code:
                return {"valid": False, "error": "No construct method found"}
            
            # Try to compile the code
            compile(code, '<generated>', 'exec')
            
            return {"valid": True, "message": "Code validation passed"}
            
        except SyntaxError as e:
            return {"valid": False, "error": f"Syntax error: {e.msg} at line {e.lineno}"}
        except Exception as e:
            return {"valid": False, "error": f"Validation error: {str(e)}"}

# Global AI service instance  
ai_service = AIService()