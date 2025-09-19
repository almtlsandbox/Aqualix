@echo off
REM Quick launcher for Aqualix executable
REM Double-click this file to run Aqualix

if exist "dist\Aqualix\Aqualix.exe" (
    echo Launching Aqualix...
    start "" "dist\Aqualix\Aqualix.exe"
) else (
    echo Error: Aqualix executable not found!
    echo Please build the executable first using: build_executable.bat
    pause
)