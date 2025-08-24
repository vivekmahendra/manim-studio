import random
import re
from pathlib import Path
from typing import Dict, Any
from ..core.config import settings

class AIService:
    def __init__(self):
        # Map of keywords to existing sample scripts
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
        
        # Sample prompts for each animation
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
    
    async def generate_manim_code(self, prompt: str) -> Dict[str, Any]:
        """Generate Manim code based on user prompt (stubbed with sample scripts)"""
        
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
        
        sample = self.samples[selected_sample]
        
        # Read the actual code from output-scripts
        code_path = settings.SAMPLE_SCRIPTS_PATH / sample["file"]
        
        try:
            with open(code_path, 'r') as f:
                code = f.read()
        except FileNotFoundError:
            # Fallback if sample file doesn't exist
            code = self._generate_fallback_code(prompt, sample["class_name"])
        
        return {
            "code": code,
            "class_name": sample["class_name"],
            "description": sample["description"],
            "sample_used": selected_sample
        }
    
    def _generate_fallback_code(self, prompt: str, class_name: str) -> str:
        """Generate a simple fallback Manim scene if sample files are missing"""
        return f'''from manim import *

class {class_name}(Scene):
    def construct(self):
        # Simple placeholder animation for: {prompt}
        title = Text("Mathematical Animation", font_size=48)
        subtitle = Text("Generated from: {prompt[:50]}...", font_size=24)
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
'''
    
    def get_sample_prompts(self) -> Dict[str, list]:
        """Return sample prompts for each category"""
        return self.sample_prompts
    
    def extract_class_name(self, code: str) -> str:
        """Extract the Scene class name from generated code"""
        # Use regex to find class definition
        class_match = re.search(r'class\s+(\w+)\s*\(\s*Scene\s*\)', code)
        if class_match:
            return class_match.group(1)
        return "GeneratedScene"

# Global AI service instance  
ai_service = AIService()