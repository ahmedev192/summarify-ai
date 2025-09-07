@echo off
echo 🚀 Setting up Summarify AI...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo ✅ Python is installed
python --version

REM Create virtual environment
echo 📦 Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists, removing old one...
    rmdir /s /q venv
)

python -m venv venv
if errorlevel 1 (
    echo ❌ Failed to create virtual environment
    pause
    exit /b 1
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Upgrade pip
echo 📥 Upgrading pip...
python -m pip install --upgrade pip

REM Install dependencies
echo 📥 Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
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
    echo ✅ .env file created
) else (
    echo ✅ .env file already exists
)

echo.
echo 🎉 Setup completed successfully!
echo.
echo 📋 Next steps:
echo 1. Run the application: run.bat
echo 2. Or manually: python run.py
echo 3. Open your browser: http://localhost:8000
echo 4. Test the API: python test_app.py
echo.
echo 📚 For more information, see README.md
echo.
pause
