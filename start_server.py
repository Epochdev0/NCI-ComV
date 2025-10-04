#!/usr/bin/env python3
"""Startup script for the Exoplanet Classification FastAPI server."""

import os
import sys
import subprocess
import time

def check_dependencies():
    """Check if required dependencies are installed."""
    print("Checking dependencies...")
    try:
        import fastapi
        import uvicorn
        import pandas
        import sklearn
        import joblib
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def train_model():
    """Train the model if it doesn't exist."""
    model_path = "models/baseline.pkl"
    if os.path.exists(model_path):
        print("✅ Model already exists")
        return True
    
    print("Training model...")
    try:
        result = subprocess.run([
            sys.executable, "src/prepare_model.py"
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Model trained successfully")
            return True
        else:
            print(f"❌ Model training failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error training model: {e}")
        return False

def start_server():
    """Start the FastAPI server."""
    print("Starting FastAPI server...")
    print("Server will be available at: http://localhost:8000")
    print("API documentation: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "src/api.py"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

def main():
    """Main startup function."""
    print("🚀 Exoplanet Classification FastAPI Server")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Train model if needed
    if not train_model():
        sys.exit(1)
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
