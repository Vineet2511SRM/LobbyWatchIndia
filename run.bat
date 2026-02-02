@echo off
REM NewsGraph - Simple Setup and Run Script for Windows

echo.
echo NewsGraph - Automated Setup and Launch
echo ==================================================
echo.

REM Check if Python is installed
echo [INFO] Checking Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python not found! Please install Python 3.8+ first.
    echo Visit: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [SUCCESS] Python found

REM Check if virtual environment exists
if not exist "newsgraph_env" (
    echo [INFO] Creating virtual environment...
    python -m venv newsgraph_env
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [SUCCESS] Virtual environment created
) else (
    echo [INFO] Virtual environment already exists
)

REM Activate virtual environment
echo [INFO] Activating virtual environment...
call newsgraph_env\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo [ERROR] Failed to activate virtual environment
    pause
    exit /b 1
)

echo [SUCCESS] Virtual environment activated

REM Install/upgrade pip
echo [INFO] Upgrading pip...
python -m pip install --upgrade pip --quiet

REM Install requirements
echo [INFO] Installing dependencies...
if exist "requirements.txt" (
    pip install -r requirements.txt --quiet
    if %errorlevel% neq 0 (
        echo [ERROR] Failed to install dependencies
        pause
        exit /b 1
    )
    echo [SUCCESS] Dependencies installed
) else (
    echo [ERROR] requirements.txt not found!
    pause
    exit /b 1
)

REM Check if main app exists
if not exist "app\live_demo.py" (
    echo [ERROR] Application file not found: app\live_demo.py
    pause
    exit /b 1
)

echo [SUCCESS] Setup completed successfully!
echo.
echo [INFO] Starting NewsGraph application...
echo.
echo The application will open in your default web browser
echo If it doesn't open automatically, go to: http://localhost:8501
echo Press Ctrl+C to stop the application
echo.

REM Run the application
streamlit run app\live_demo.py