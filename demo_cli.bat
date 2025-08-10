@echo off
REM Demo script for Aqualix CLI interface

echo ==================================================
echo             Aqualix CLI Demo
echo ==================================================
echo.

echo 1. Showing CLI help:
echo.
.venv\Scripts\python.exe cli.py --help
echo.

echo ==================================================
echo 2. CLI processing demo (if you have test images):
echo.
echo To process a single image:
echo .venv\Scripts\python.exe cli.py input_image.jpg -o processed_image.jpg
echo.
echo To process a folder with custom parameters:
echo .venv\Scripts\python.exe cli.py input_folder -o output_folder --batch --gray-world-percentile 15 --hist-eq-clip 3.0
echo.

echo ==================================================
echo 3. Launching GUI application:
echo.
.venv\Scripts\python.exe main.py

pause
