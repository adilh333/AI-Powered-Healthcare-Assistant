#!/usr/bin/env python3
"""
Azure App Service startup script for Healthcare Assistant
This script starts both the Flask API and Streamlit dashboard
"""

import os
import sys
import subprocess
import threading
import time
import signal
from pathlib import Path

class HealthcareAppStarter:
    def __init__(self):
        self.api_process = None
        self.streamlit_process = None
        self.running = True
        
    def start_flask_api(self):
        """Start Flask API server"""
        print("🚀 Starting Flask API server...")
        try:
            self.api_process = subprocess.Popen([
                sys.executable, 'app.py'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✅ Flask API server started on port 5000")
        except Exception as e:
            print(f"❌ Failed to start Flask API: {e}")
    
    def start_streamlit(self):
        """Start Streamlit dashboard"""
        print("🚀 Starting Streamlit dashboard...")
        try:
            # Configure Streamlit for Azure
            os.environ['STREAMLIT_SERVER_PORT'] = '8501'
            os.environ['STREAMLIT_SERVER_ADDRESS'] = '0.0.0.0'
            os.environ['STREAMLIT_SERVER_HEADLESS'] = 'true'
            os.environ['STREAMLIT_BROWSER_GATHER_USAGE_STATS'] = 'false'
            
            self.streamlit_process = subprocess.Popen([
                sys.executable, '-m', 'streamlit', 'run', 'streamlit_app.py',
                '--server.port=8501',
                '--server.address=0.0.0.0',
                '--server.headless=true',
                '--browser.gatherUsageStats=false'
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("✅ Streamlit dashboard started on port 8501")
        except Exception as e:
            print(f"❌ Failed to start Streamlit: {e}")
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals"""
        print("\n🛑 Shutting down Healthcare Assistant...")
        self.running = False
        
        if self.api_process:
            self.api_process.terminate()
            print("✅ Flask API stopped")
        
        if self.streamlit_process:
            self.streamlit_process.terminate()
            print("✅ Streamlit dashboard stopped")
        
        sys.exit(0)
    
    def start(self):
        """Start both services"""
        print("🏥 Starting Healthcare Assistant on Azure...")
        print("=" * 50)
        
        # Set up signal handlers
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Start Flask API in a separate thread
        api_thread = threading.Thread(target=self.start_flask_api)
        api_thread.daemon = True
        api_thread.start()
        
        # Wait a moment for API to start
        time.sleep(3)
        
        # Start Streamlit
        self.start_streamlit()
        
        print("=" * 50)
        print("🎉 Healthcare Assistant is running!")
        print("📊 Streamlit Dashboard: http://localhost:8501")
        print("🔌 Flask API: http://localhost:5000")
        print("=" * 50)
        
        # Keep the main thread alive
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.signal_handler(signal.SIGINT, None)

if __name__ == "__main__":
    app = HealthcareAppStarter()
    app.start()
