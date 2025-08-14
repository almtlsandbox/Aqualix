@echo off
REM Build script for Aqualix Windows Executable
REM This script creates a standalone Windows executable for Aqualix

echo ========================================
echo  AQUALIX - BUILD WINDOWS EXECUTABLE
echo ========================================

REM Check if virtual environment is activated
if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment not found!
    echo Please run: python -m venv .venv
    echo Then activate: .venv\Scripts\activate
    echo And install dependencies: pip install -r requirements.txt
    pause
    exit /b 1
)

echo 1. Cleaning previous builds...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"

echo 2. Installing/updating PyInstaller...
.venv\Scripts\python.exe -m pip install --upgrade pyinstaller setuptools

echo 3. Running PyInstaller...
.venv\Scripts\python.exe -m PyInstaller aqualix.spec --clean --noconfirm

REM Check if build was successful
if exist "dist\Aqualix\Aqualix.exe" (
    echo.
    echo ========================================
    echo  BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Executable created: dist\Aqualix\Aqualix.exe
    echo Distribution folder: dist\Aqualix\
    echo.
    echo The application is now ready for distribution.
    echo All dependencies are bundled in the dist folder.
    echo.
    echo You can:
    echo 1. Copy the entire "dist\Aqualix" folder to any Windows computer
    echo 2. Run Aqualix.exe directly (no Python installation needed)
    echo 3. Create a desktop shortcut to Aqualix.exe
    echo.
    
    REM Get file size
    for %%A in ("dist\Aqualix\Aqualix.exe") do echo File size: %%~zA bytes
    
    REM Count files in distribution
    for /f %%A in ('dir "dist\Aqualix" /b /s ^| find /c /v ""') do echo Total files: %%A
    
    echo.
    echo Build completed successfully!
) else (
    echo.
    echo ========================================
    echo  BUILD FAILED!
    echo ========================================
    echo.
    echo The executable was not created.
    echo Check the output above for error messages.
    echo.
    echo Common solutions:
    echo 1. Ensure all dependencies are installed
    echo 2. Check for import errors in the source code
    echo 3. Verify the virtual environment is working
    echo.
)

echo.
pause
