#!/bin/bash

# ExoVision Explorer - Development Startup Script
# This script starts both the FastAPI backend and React frontend

echo "🌌 Starting ExoVision Explorer Development Environment"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "start_server.py" ]; then
    echo "❌ Error: Please run this script from the project root directory"
    echo "   Expected to find start_server.py in current directory"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Error: Virtual environment not found. Please run:"
    echo "   python -m venv venv"
    echo "   source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
    echo "   pip install -r requirements.txt"
    exit 1
fi

# Function to cleanup background processes
cleanup() {
    echo ""
    echo "🛑 Shutting down servers..."
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

echo "🚀 Starting FastAPI backend server..."
# Activate virtual environment and start backend
source venv/bin/activate
python start_server.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

echo "🎨 Starting React frontend..."
# Start frontend
cd frontend/exo-vision-explorer
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ Both servers are starting up!"
echo ""
echo "📡 Backend API: http://localhost:8000"
echo "🌐 Frontend UI: http://localhost:5173"
echo "📚 API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

# Wait for user interrupt
wait
