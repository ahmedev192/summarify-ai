@echo off
echo 🚀 Starting Summarify AI...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ❌ Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies if requirements.txt exists
if exist "requirements.txt" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

REM Create .env file if it doesn't exist
if not exist ".env" (
    echo 📝 Creating .env file...
    echo # Model Configuration > .env
    echo MODEL_NAME=facebook/opt-125m >> .env
    echo MAX_LENGTH=512 >> .env
    echo MIN_LENGTH=50 >> .env
    echo. >> .env
    echo # Server Configuration >> .env
    echo HOST=0.0.0.0 >> .env
    echo PORT=8000 >> .env
    echo. >> .env
    echo # Logging Configuration >> .env
    echo LOG_FILE=request_logs.xlsx >> .env
)

REM Start the application
echo 🚀 Starting Summarify AI server...
echo 📡 Server will be available at: http://localhost:8000
echo 📊 Dashboard: http://localhost:8000
echo 🔧 API docs: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop the server
echo.

python run.py

pause
