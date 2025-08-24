import asyncio
import random
import re
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from pydantic import BaseModel, Field
from ..core.config import settings

# Set up logging
logger = logging.getLogger(__name__)

# Pydantic model for structured output
class ManimCodeGeneration(BaseModel):
    code: str = Field(
        description="Complete, executable Python code for the Manim scene. Should contain ONLY valid Python code with imports, class definition, and methods. No markdown formatting, no explanations, no comments outside the code."
    )
    class_name: str = Field(
        description="The name of the Scene class defined in the code (e.g., 'ComplexPlaneScene')"
    )
    description: str = Field(
        description="A brief description of what this animation teaches or demonstrates"
    )
    explanation: Optional[str] = Field(
        default=None,
        description="Optional detailed explanation of the mathematical concept being visualized"
    )

class AIService:
    def __init__(self):
        # Initialize OpenAI client
        self.client = AsyncOpenAI(
            api_key=settings.OPENAI_API_KEY,
            timeout=settings.OPENAI_TIMEOUT
        )
        
        # Load system prompt template
        self.system_prompt = self._load_system_prompt()
        
        # Keep sample fallback scripts for emergencies
        self.samples = {
            "vector": {
                "file": "vector_add_sub.py",
                "class_name": "VectorAddSub",
                "description": "Vector addition and subtraction visualization",
                "keywords": ["vector", "add", "subtract", "addition", "subtraction", "arrow"]
            },
            "hyperbola": {
                "file": "hyperbola_foci.py", 
                "class_name": "HyperbolaFoci",
                "description": "Hyperbola and foci visualization",
                "keywords": ["hyperbola", "foci", "focus", "conic", "asymptote"]
            },
            "teacher": {
                "file": "hyperbola_teacher.py",
                "class_name": "HyperbolaTeacher",
                "description": "Educational hyperbola animation",
                "keywords": ["teach", "explain", "hyperbola", "lesson", "education"]
            }
        }
        
        # Sample prompts for examples
        self.sample_prompts = {
            "vector": [
                "Show how vectors add and subtract",
                "Visualize vector addition with arrows",
                "Animate vector operations in 2D",
                "Demonstrate vector arithmetic"
            ],
            "hyperbola": [
                "Show a hyperbola with its foci",
                "Animate hyperbola properties",
                "Visualize conic sections - hyperbola",
                "Explain hyperbola asymptotes"
            ],
            "teacher": [
                "Teach hyperbolas step by step",
                "Educational animation about conics",
                "Explain mathematical concepts visually",
                "Create a math lesson animation"
            ]
        }
    
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
            
            # Prepare the system prompt with the user's topic
            system_prompt = self.system_prompt.replace("{TOPIC}", prompt)
            system_prompt = system_prompt.replace("{SceneName}", "GeneratedScene")
            system_prompt = system_prompt.replace("{file_name}", "generated_scene")
            system_prompt = system_prompt.replace("{output_name}", "generated_animation")
            
            # Use structured outputs compatible model
            model_to_use = "gpt-4o-2024-08-06"  # Required for structured outputs
            logger.info(f"Calling OpenAI API with structured outputs model: {model_to_use}")
            
            # Call OpenAI API with structured outputs
            response = await self.client.beta.chat.completions.parse(
                model=model_to_use,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Create a Manim animation that teaches: {prompt}"}
                ],
                max_tokens=settings.OPENAI_MAX_TOKENS,
                temperature=settings.OPENAI_TEMPERATURE,
                response_format=ManimCodeGeneration
            )
            
            # Handle structured output response
            if response.choices[0].message.refusal:
                logger.error(f"OpenAI refused the request: {response.choices[0].message.refusal}")
                raise ValueError(f"OpenAI refused the request: {response.choices[0].message.refusal}")
            
            # Extract the parsed structured data
            structured_response = response.choices[0].message.parsed
            if not structured_response:
                raise ValueError("No structured response received from OpenAI")
            
            logger.info(f"✅ Successfully generated structured OpenAI response")
            logger.info(f"Code length: {len(structured_response.code)} characters")
            logger.info(f"Class name: {structured_response.class_name}")
            
            return {
                "code": structured_response.code,
                "class_name": structured_response.class_name,
                "description": structured_response.description,
                "explanation": structured_response.explanation,
                "method": "openai_generated", 
                "model": model_to_use
            }
            
        except Exception as e:
            logger.error(f"❌ OpenAI structured generation failed: {type(e).__name__}: {str(e)}")
            
            # Handle different types of errors
            error_str = str(e).lower()
            
            # Don't fallback for authentication/authorization errors
            if any(keyword in error_str for keyword in ["api_key", "invalid", "unauthorized", "forbidden"]):
                logger.error("❌ Authentication/authorization issue - not falling back to samples")
                raise e
            
            # Don't fallback for structured output parsing errors (indicates prompt/schema issues)
            if any(keyword in error_str for keyword in ["parsing", "schema", "validation", "pydantic"]):
                logger.error("❌ Structured output parsing failed - not falling back to samples")
                raise e
            
            # Fallback for network/server errors, quota issues, and other temporary problems
            if any(keyword in error_str for keyword in ["quota", "rate_limit", "timeout", "connection", "server"]):
                logger.warning("⚠️ Falling back to sample-based generation due to temporary issue")
                return await self._fallback_generation(prompt)
            
            # For unknown errors, also fallback but log as unexpected
            logger.warning("⚠️ Unknown error - falling back to sample-based generation")
            return await self._fallback_generation(prompt)
    
    async def _fallback_generation(self, prompt: str) -> Dict[str, Any]:
        """Fallback to sample-based generation if OpenAI fails"""
        logger.warning(f"🔄 Using sample fallback for prompt: '{prompt[:50]}{'...' if len(prompt) > 50 else ''}'")
        
        # Simple keyword matching to select appropriate sample
        prompt_lower = prompt.lower()
        selected_sample = None
        max_matches = 0
        
        # Find the sample with the most keyword matches
        for sample_key, sample_data in self.samples.items():
            matches = sum(1 for keyword in sample_data["keywords"] if keyword in prompt_lower)
            if matches > max_matches:
                max_matches = matches
                selected_sample = sample_key
        
        # If no matches found, randomly select one
        if not selected_sample:
            selected_sample = random.choice(list(self.samples.keys()))
            logger.warning(f"🎲 No keyword matches found, randomly selected: {selected_sample}")
        else:
            logger.info(f"📝 Selected sample '{selected_sample}' with {max_matches} keyword matches")
        
        sample = self.samples[selected_sample]
        
        # Read the actual code from output-scripts
        code_path = settings.SAMPLE_SCRIPTS_PATH / sample["file"]
        
        try:
            with open(code_path, 'r') as f:
                code = f.read()
            
            logger.info(f"📄 Successfully loaded sample code from: {sample['file']}")
            
            return {
                "code": code,
                "class_name": sample["class_name"],
                "description": f"⚠️ SAMPLE CONTENT: {sample['description']} (OpenAI temporarily unavailable)",
                "method": "sample_fallback",
                "sample_used": selected_sample
            }
        except FileNotFoundError:
            logger.error(f"❌ Sample file not found: {code_path}")
            # Ultimate fallback if sample files are missing
            code = self._generate_emergency_fallback(prompt, sample["class_name"])
            return {
                "code": code,
                "class_name": sample["class_name"],
                "description": f"⚠️ EMERGENCY FALLBACK for: {prompt}",
                "method": "emergency_fallback"
            }
    
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
    
    def _generate_emergency_fallback(self, prompt: str, class_name: str) -> str:
        """Generate a simple emergency fallback Manim scene"""
        return f'''from manim import *

class {class_name}(Scene):
    def construct(self):
        # Emergency fallback animation for: {prompt}
        title = Text("Mathematical Animation", font_size=48)
        subtitle = Text("Generated from: {prompt[:50]}{'...' if len(prompt) > 50 else ''}", font_size=24)
        subtitle.next_to(title, DOWN, buff=0.5)
        
        self.play(Write(title))
        self.wait(1)
        self.play(FadeIn(subtitle))
        self.wait(2)
        
        # Simple visual element
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        self.play(circle.animate.set_color(RED))
        self.wait(1)
        
        self.play(FadeOut(title), FadeOut(subtitle), FadeOut(circle))

# Render Commands:
# manim -pql {class_name.lower()}.py {class_name}
# manim -pqh {class_name.lower()}.py {class_name} -o high_quality_output
'''
    
    def extract_class_name(self, code: str) -> str:
        """Extract the Scene class name from generated code"""
        # Use regex to find class definition
        class_match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
        if class_match:
            return class_match.group(1)
        
        # Fallback to a default name
        return "GeneratedScene"
    
    def get_sample_prompts(self) -> Dict[str, list]:
        """Return sample prompts for each category"""
        return self.sample_prompts
    
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