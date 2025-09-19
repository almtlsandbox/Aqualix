@echo off
REM Build script for Aqualix Standalone Windows Executable (Single File)
REM This script creates a SINGLE STANDALONE executable with ALL dependencies

echo ========================================
echo  AQUALIX - BUILD STANDALONE EXECUTABLE
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
if exist "dist\Aqualix-Standalone.exe" del "dist\Aqualix-Standalone.exe"
if exist "build" rmdir /s /q "build"

echo 2. Installing/updating PyInstaller...
.venv\Scripts\python.exe -m pip install --upgrade pyinstaller setuptools

echo 3. Building STANDALONE executable (this may take 5-10 minutes)...
echo    • Bundling ALL dependencies into ONE file
echo    • Applying UPX compression for smaller size
echo    • No external dependencies required
echo.

.venv\Scripts\python.exe -m PyInstaller aqualix_standalone.spec --clean --noconfirm

REM Check if build was successful
if exist "dist\Aqualix-Standalone.exe" (
    echo.
    echo ========================================
    echo  BUILD SUCCESSFUL!
    echo ========================================
    echo.
    echo Standalone executable created: dist\Aqualix-Standalone.exe
    echo.
    
    REM Get file size
    for %%A in ("dist\Aqualix-Standalone.exe") do (
        echo File size: %%~zA bytes
        set /a sizeMB=%%~zA/1024/1024
        echo File size: !sizeMB! MB approximately
    )
    
    echo.
    echo ✅ STANDALONE FEATURES:
    echo • Single file executable - NO dependencies
    echo • NO Python installation required
    echo • NO additional DLLs or folders needed
    echo • Can be copied/moved anywhere
    echo • Runs directly on any Windows 10/11 PC
    echo.
    echo 🚀 USAGE:
    echo • Copy Aqualix-Standalone.exe to any Windows computer
    echo • Double-click to run - that's it!
    echo • No installation, no setup, no configuration needed
    echo.
    echo 📝 NOTE: First launch may take 10-15 seconds as the exe
    echo    extracts dependencies to a temporary folder.
    echo    Subsequent launches will be much faster.
    echo.
    echo Build completed successfully!
) else (
    echo.
    echo ========================================
    echo  BUILD FAILED!
    echo ========================================
    echo.
    echo The standalone executable was not created.
    echo Check the output above for error messages.
    echo.
    echo Common solutions:
    echo 1. Ensure all dependencies are installed
    echo 2. Check for import errors in the source code
    echo 3. Verify the virtual environment is working
    echo 4. Try running with --debug flag for more info
    echo.
)

echo.
pause