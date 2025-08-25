#!/bin/bash

# Cleanup script for ManimStudio
echo "🧹 Cleaning up ManimStudio files..."

# Clear output videos
echo "Clearing output videos..."
rm -f /Users/vivekmahendra/Documents/manim-llm/backend/output/*.mp4
rm -f /Users/vivekmahendra/Documents/manim-llm/backend/output/*.mov

# Clear generated scripts (optional - uncomment if needed)
# echo "Clearing generated scripts..."
# rm -f /Users/vivekmahendra/Documents/manim-llm/backend/generated/*.py

# Clear Manim media cache in generated folder
echo "Clearing Manim media cache..."
rm -rf /Users/vivekmahendra/Documents/manim-llm/backend/generated/media/

echo "✅ Cleanup completed!"
echo ""
echo "Remaining files:"
echo "Output folder:"
ls -la /Users/vivekmahendra/Documents/manim-llm/backend/output/ | head -5
echo ""
echo "Generated folder (recent files):"
ls -lt /Users/vivekmahendra/Documents/manim-llm/backend/generated/*.py 2>/dev/null | head -3 || echo "No .py files found"