#!/bin/bash

# Healthcare Assistant Startup Script
echo "🏥 Starting Healthcare Assistant..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📚 Installing dependencies..."
pip install -r requirements.txt

# Check if models exist
if [ ! -d "models" ] || [ ! "$(ls -A models)" ]; then
    echo "🤖 Training ML models..."
    python train_models.py
fi

# Start the application
echo "🚀 Starting Healthcare Assistant..."
echo "📊 Dashboard: http://localhost:8501"
echo "🔌 API: http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the application"
echo "=" * 50

python run_app.py
