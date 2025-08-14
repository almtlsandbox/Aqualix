@echo off
REM Test script for Aqualix executable
REM Verifies that the executable works correctly

echo ========================================
echo  AQUALIX - TEST EXECUTABLE
echo ========================================

REM Check if executable exists
if not exist "dist\Aqualix\Aqualix.exe" (
    echo Error: Executable not found!
    echo Please run build_executable.bat first.
    pause
    exit /b 1
)

echo Testing Aqualix executable...
echo.

REM Get executable information
echo File Information:
for %%A in ("dist\Aqualix\Aqualix.exe") do (
    echo   Path: %%~fA
    echo   Size: %%~zA bytes
    echo   Date: %%~tA
)

echo.
echo Distribution Contents:
dir "dist\Aqualix" /b

echo.
echo ========================================
echo  LAUNCHING APPLICATION...
echo ========================================
echo.
echo The application window should open.
echo If it opens successfully, the build is working correctly.
echo Close the application when done testing.
echo.

REM Launch the executable
start "" "dist\Aqualix\Aqualix.exe"

REM Wait a moment for startup
timeout /t 3 /nobreak >nul

echo.
echo Test completed.
echo If the application opened without errors, the executable is ready!
echo.
pause
