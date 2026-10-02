@echo off
echo ========================================
echo HEALIX HOSPITAL - Debug Mode
echo ========================================
echo.

echo Step 1: Running diagnostic check...
python test_setup.py
if errorlevel 1 (
    echo.
    echo Diagnostic check failed. Please fix the issues above.
    pause
    exit /b 1
)

echo.
echo Step 2: Installing/Updating dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo Failed to install dependencies. Trying alternative...
    python -m pip install -r requirements.txt
)

echo.
echo Step 3: Starting the server...
echo.
echo ========================================
echo Server will be available at:
echo http://localhost:5000
echo.
echo Default login: admin / admin123
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

python app.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo ERROR: Server failed to start!
    echo ========================================
    echo.
    echo Common issues:
    echo 1. Python not installed or not in PATH
    echo 2. Flask not installed - run: pip install Flask
    echo 3. Port 5000 already in use
    echo 4. Missing files or incorrect folder structure
    echo.
    echo Check the error message above for details.
    echo.
)

pause
