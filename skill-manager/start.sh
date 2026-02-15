#!/bin/bash

# Skills Manager Launcher
# This script starts the backend server and opens the frontend in the browser

echo "🚀 Starting Skills Manager..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
BACKEND_DIR="$SCRIPT_DIR/backend"
FRONTEND_DIR="$SCRIPT_DIR/frontend"

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed"
    echo "Please install Python 3 and try again"
    exit 1
fi

# Check if dependencies are installed
echo "📦 Checking dependencies..."
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing backend dependencies..."
    pip3 install -r "$BACKEND_DIR/requirements.txt"
fi

# Start backend server in background
echo "🔧 Starting backend server..."
cd "$BACKEND_DIR"
python3 app.py &
BACKEND_PID=$!

# Wait for server to start
echo "⏳ Waiting for server to start..."
sleep 3

# Check if server is running
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ Error: Backend server failed to start"
    exit 1
fi

echo "✅ Backend server started (PID: $BACKEND_PID)"
echo "🌐 Server running at http://localhost:5000"
echo ""

# Open frontend in browser
echo "🌐 Opening frontend in browser..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    open "$FRONTEND_DIR/index.html"
elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    xdg-open "$FRONTEND_DIR/index.html"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    # Windows
    start "$FRONTEND_DIR/index.html"
fi

echo ""
echo "✨ Skills Manager is ready!"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""

# Wait for Ctrl+C
trap "echo ''; echo '🛑 Stopping server...'; kill $BACKEND_PID; echo '✅ Server stopped'; exit 0" INT

# Keep script running
wait $BACKEND_PID
