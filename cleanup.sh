#!/bin/bash

# Cleanup script for ManimStudio
# This script should be run from the project root directory

# Get the directory where the script is located (project root)
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🧹 Cleaning up ManimStudio files..."
echo "📁 Working directory: $SCRIPT_DIR"

# Clear ALL files from output directory
echo ""
echo "🗑️  Clearing output directory..."
if [ -d "$SCRIPT_DIR/backend/output" ]; then
    rm -rf "$SCRIPT_DIR/backend/output"/*
    echo "   ✓ Cleared all files from backend/output/"
else
    echo "   ⚠️  Output directory not found"
fi

# Clear ALL files from generated directory
echo ""
echo "🗑️  Clearing generated scripts and cache..."
if [ -d "$SCRIPT_DIR/backend/generated" ]; then
    rm -rf "$SCRIPT_DIR/backend/generated"/*
    echo "   ✓ Cleared all files from backend/generated/"
else
    echo "   ⚠️  Generated directory not found"
fi

# Clear Manim media cache from backend root
echo ""
echo "🗑️  Clearing Manim media cache..."
if [ -d "$SCRIPT_DIR/backend/media" ]; then
    rm -rf "$SCRIPT_DIR/backend/media"
    echo "   ✓ Cleared backend/media/ directory"
fi

# Clear any __pycache__ directories
echo ""
echo "🗑️  Clearing Python cache..."
find "$SCRIPT_DIR/backend" -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null
echo "   ✓ Cleared all __pycache__ directories"

# Create .gitkeep files to preserve empty directories
echo ""
echo "📝 Preserving directory structure..."
touch "$SCRIPT_DIR/backend/output/.gitkeep" 2>/dev/null
touch "$SCRIPT_DIR/backend/generated/.gitkeep" 2>/dev/null

echo ""
echo "✅ Cleanup completed!"
echo ""
echo "📊 Directory status:"
echo "-------------------"
echo "backend/output/:"
file_count=$(find "$SCRIPT_DIR/backend/output" -type f ! -name ".gitkeep" 2>/dev/null | wc -l | tr -d ' ')
echo "   Files: $file_count (excluding .gitkeep)"

echo ""
echo "backend/generated/:"
file_count=$(find "$SCRIPT_DIR/backend/generated" -type f ! -name ".gitkeep" 2>/dev/null | wc -l | tr -d ' ')
echo "   Files: $file_count (excluding .gitkeep)"

echo ""
echo "💡 Tip: The backend server will recreate these directories as needed."