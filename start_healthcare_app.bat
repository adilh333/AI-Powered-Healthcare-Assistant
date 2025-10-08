@echo off
echo 🏥 Starting Healthcare Assistant...

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is required but not installed.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
echo 📚 Installing dependencies...
pip install -r requirements.txt

REM Check if models exist
if not exist "models" (
    echo 🤖 Training ML models...
    python train_models.py
) else (
    dir models\*.pkl >nul 2>&1
    if errorlevel 1 (
        echo 🤖 Training ML models...
        python train_models.py
    )
)

REM Start the application
echo 🚀 Starting Healthcare Assistant...
echo 📊 Dashboard: http://localhost:8501
echo 🔌 API: http://localhost:5000
echo.
echo Press Ctrl+C to stop the application
echo ==================================================

python run_app.py

pause
