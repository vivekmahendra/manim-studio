# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Manim-based educational animation project that generates mathematical animations from LLM prompts. The project creates animated math lessons with a consistent two-pane layout format.

## Key Commands

### Running Manim Animations

```bash
# Preview animation (low quality, quick)
manim -pql backend/output-scripts/<script_name>.py <SceneName>

# High quality render
manim -pqh backend/output-scripts/<script_name>.py <SceneName>

# Example for existing scenes
manim -pql backend/output-scripts/hyperbola_foci.py HyperbolaFoci
manim -pql backend/output-scripts/hyperbola_teacher.py HyperbolaTeacher
manim -pql backend/output-scripts/vector_add_sub.py VectorAddSub
```

### Python Environment

```bash
# Activate virtual environment
source backend/.venv/bin/activate

# Install dependencies
pip install -r backend/requirements.txt
```

## Architecture & Structure

### Core Components

1. **Prompt System** (`backend/prompts/prompt.txt`): Contains the master prompt template used for generating Manim scenes. Defines strict layout requirements and animation guidelines.

2. **Output Scripts** (`backend/output-scripts/`): Generated Manim Scene classes that follow the two-pane educational format specified in the prompt.

3. **Media Output** (`backend/media/`): Manim's output directory containing:
   - `videos/`: Rendered animation files
   - `Tex/`: LaTeX formula renderings
   - `texts/`: Text element SVGs
   - `images/`: Supporting images

### Scene Design Pattern

All generated scenes follow this structure:
- **Layout**: Two-pane design (60-65% left for visuals, 35-40% right for text board)
- **Pacing**: Short beats (5-15s) with one concept per beat
- **Board API**: Each scene implements a `show_board()` helper for clean text management
- **Persistent Elements**: Title and axes remain throughout, other elements fade in/out per beat
- **Color Scheme**: Consistent use (BLUE/GREEN for main curves, GRAY for asymptotes, YELLOW/RED for special points)

### Key Design Constraints

From the prompt template:
- No text overlapping graphs (text only on right board)
- One equation + one visual + one label group maximum per screen
- FadeOut old content before showing new
- Small title with top margin
- Background rectangles for contrast when needed
- Clean transitions (FadeIn, Create, TransformFromCopy, FadeOut only)

## Development Workflow

When creating new Manim scenes:
1. Follow the template structure in existing scenes (e.g., `vector_add_sub.py`)
2. Implement the `show_board()` helper method
3. Structure content into clear beats with proper pacing
4. Test with low-quality preview before final high-quality render
5. Output files go in `backend/output-scripts/`