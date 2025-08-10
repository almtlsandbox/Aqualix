# Image and Video Processing Application

This is a Python Tkinter-based application for processing images and videos with the following features:

## Key Features
- File browser for selecting images, videos, or folders
- Navigation controls (next/previous) for browsing files
- Video frame slider for navigating video frames
- Image processing pipeline with operations:
  - Gray-world white balancing
  - Histogram equalization
- Parameter tuning interface with real-time preview
- Pipeline description section
- **Interactive Split View** with:
  - Adjustable split divider (drag or slider)
  - Zoom in/out functionality (mouse wheel or buttons)
  - Pan support (click and drag)
  - 90-degree rotation controls
  - Reset view functionality
- Save processed results
- Batch processing for videos (apply to all frames)

## Project Structure
- Main application: `main.py`
- Image processing modules: `image_processing.py`
- UI components: `ui_components.py`
- Requirements: `requirements.txt`
- Documentation: `README.md`

## Development Guidelines
- Use OpenCV for image and video processing
- Use Tkinter for the GUI interface
- Use PIL/Pillow for interactive image transformations (zoom, pan, rotate)
- Follow modular design patterns
- Include proper error handling
- Provide clear parameter descriptions
- Implement smooth interactive controls for user experience
