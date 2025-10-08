#!/usr/bin/env python3
"""
Healthcare Assistant Application Launcher
Starts both Flask API and Streamlit dashboard
"""

import subprocess
import sys
import time
import threading
import os
from pathlib import Path

def run_flask_api():
    """Run Flask API in background"""
    try:
        print("🚀 Starting Flask API server...")
        subprocess.run([sys.executable, "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Flask API failed to start: {e}")
    except KeyboardInterrupt:
        print("🛑 Flask API stopped")

def run_streamlit():
    """Run Streamlit dashboard"""
    try:
        print("🚀 Starting Streamlit dashboard...")
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "streamlit_app.py",
            "--server.port", "8501",
            "--server.address", "0.0.0.0",
            "--browser.gatherUsageStats", "false"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Streamlit failed to start: {e}")
    except KeyboardInterrupt:
        print("🛑 Streamlit stopped")

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'streamlit', 'flask', 'pandas', 'numpy', 'scikit-learn', 
        'xgboost', 'plotly', 'requests'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True

def main():
    """Main launcher function"""
    print("=" * 60)
    print("🏥 Healthcare Assistant - Application Launcher")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check if models exist
    models_dir = Path("models")
    if not models_dir.exists() or not any(models_dir.glob("*.pkl")):
        print("⚠️  No trained models found. Training models first...")
        try:
            subprocess.run([sys.executable, "train_models.py"], check=True)
            print("✅ Models trained successfully!")
        except subprocess.CalledProcessError as e:
            print(f"❌ Model training failed: {e}")
            sys.exit(1)
    
    print("\n🎯 Starting Healthcare Assistant...")
    print("📊 Streamlit Dashboard: http://localhost:8501")
    print("🔌 Flask API: http://localhost:5000")
    print("\nPress Ctrl+C to stop both services")
    print("=" * 60)
    
    try:
        # Start Flask API in a separate thread
        flask_thread = threading.Thread(target=run_flask_api, daemon=True)
        flask_thread.start()
        
        # Wait a moment for Flask to start
        time.sleep(3)
        
        # Start Streamlit (this will block)
        run_streamlit()
        
    except KeyboardInterrupt:
        print("\n🛑 Shutting down Healthcare Assistant...")
        print("✅ Application stopped successfully!")

if __name__ == "__main__":
    main()
