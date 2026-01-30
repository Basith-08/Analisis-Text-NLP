#!/bin/bash

echo "=================================="
echo "NLP Text Preprocessing Tool"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 not found. Please install Python 3.13.6"
    exit 1
fi

# Check if Bun is installed
if ! command -v bun &> /dev/null; then
    echo "Error: Bun not found. Please install Bun from https://bun.sh"
    exit 1
fi

echo "Starting Backend (Python Flask)..."
cd backend

# Install Python dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt > /dev/null 2>&1

# Start backend in background
python3 app.py &
BACKEND_PID=$!
echo "Backend started with PID: $BACKEND_PID"

echo "Waiting for backend to initialize..."
sleep 5

cd ..

echo ""
echo "Starting Frontend (Vue + Vite + Bun)..."
cd frontend

# Install dependencies if needed
if [ ! -d "node_modules" ]; then
    echo "Installing frontend dependencies..."
    bun install
fi

# Start frontend
echo ""
echo "=================================="
echo "Application is starting..."
echo "Backend: http://localhost:5000"
echo "Frontend: http://localhost:3000"
echo "=================================="
echo ""
echo "Press Ctrl+C to stop both servers"
echo ""

bun run dev

# Cleanup when script exits
trap "kill $BACKEND_PID" EXIT
