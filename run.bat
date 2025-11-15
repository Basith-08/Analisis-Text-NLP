@echo off
echo ==================================
echo NLP Text Preprocessing Tool
echo ==================================
echo.

:: Check if Python is installed
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Python not found. Please install Python 3.13.6
    pause
    exit /b 1
)

:: Check if Bun is installed
where bun >nul 2>nul
if %errorlevel% neq 0 (
    echo Error: Bun not found. Please install Bun from https://bun.sh
    pause
    exit /b 1
)

echo Starting Backend (Python Flask)...
cd backend

:: Install Python dependencies
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt >nul 2>&1

:: Start backend in background
start /B python app.py
echo Backend started

cd ..

echo.
echo Starting Frontend (Vue + Vite + Bun)...
cd frontend

:: Install dependencies if needed
if not exist "node_modules" (
    echo Installing frontend dependencies...
    bun install
)

echo.
echo ==================================
echo Application is starting...
echo Backend: http://localhost:5000
echo Frontend: http://localhost:3000
echo ==================================
echo.
echo Press Ctrl+C to stop both servers
echo.

bun run dev

pause
