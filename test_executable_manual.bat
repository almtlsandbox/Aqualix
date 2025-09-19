@echo off
REM Test script for Aqualix Windows Executable
REM This script tests the built executable

echo ========================================
echo  AQUALIX - EXECUTABLE TEST
echo ========================================

REM Check if executable exists
if not exist "dist\Aqualix\Aqualix.exe" (
    echo Error: Executable not found!
    echo Please build the executable first using: build_executable.bat
    pause
    exit /b 1
)

echo Executable found: dist\Aqualix\Aqualix.exe

REM Get file information
echo.
echo ========================================
echo  EXECUTABLE INFORMATION
echo ========================================

for %%A in ("dist\Aqualix\Aqualix.exe") do (
    echo File size: %%~zA bytes
    echo Modified: %%~tA
)

REM Count total files in distribution
for /f %%A in ('dir "dist\Aqualix" /b /s ^| find /c /v ""') do echo Total files in distribution: %%A

REM Get distribution folder size
for /f "tokens=3" %%A in ('dir "dist\Aqualix" /-c ^| findstr "bytes"') do echo Distribution size: %%A bytes

echo.
echo ========================================
echo  TESTING EXECUTABLE LAUNCH
echo ========================================

echo Starting Aqualix.exe...
echo (The application should launch in a separate window)
echo.

REM Launch the executable
start "" "dist\Aqualix\Aqualix.exe"

REM Wait a moment for the application to start
timeout /t 3 /nobreak >nul

echo.
echo ========================================
echo  TEST COMPLETE
echo ========================================
echo.
echo If the application window opened successfully, the executable is working!
echo.
echo What to do next:
echo 1. Test all application features
echo 2. Try opening image/video files
echo 3. Test processing operations
echo 4. Verify save functionality
echo.
echo Distribution is ready at: dist\Aqualix\
echo Copy the entire folder to share the application.
echo.

pause