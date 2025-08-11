@echo off
echo Running Aqualix Test Suite
echo ========================

REM Change to project directory
cd /d "%~dp0"

REM Activate virtual environment
call .venv\Scripts\activate.bat

REM Run tests by category
echo.
echo [1/4] Running Unit Tests...
python -m pytest tests\unit\ -v

echo.
echo [2/4] Running Integration Tests...
python -m pytest tests\integration\ -v

echo.
echo [3/4] Running UI Tests...
python -m pytest tests\ui\ -v

echo.
echo [4/4] Running Performance Tests...
python -m pytest tests\performance\ -v

echo.
echo Test suite completed!
pause
