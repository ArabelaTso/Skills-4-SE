@echo off
REM Skills Manager Launcher for Windows

echo Starting Skills Manager...
echo.

REM Get the directory where this script is located
set SCRIPT_DIR=%~dp0
set BACKEND_DIR=%SCRIPT_DIR%backend
set FRONTEND_DIR=%SCRIPT_DIR%frontend

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed
    echo Please install Python 3 and try again
    pause
    exit /b 1
)

REM Check if dependencies are installed
echo Checking dependencies...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing backend dependencies...
    pip install -r "%BACKEND_DIR%\requirements.txt"
)

REM Start backend server
echo Starting backend server...
cd /d "%BACKEND_DIR%"
start "Skills Manager Backend" python app.py

REM Wait for server to start
echo Waiting for server to start...
timeout /t 3 /nobreak >nul

echo Backend server started
echo Server running at http://localhost:5000
echo.

REM Open frontend in browser
echo Opening frontend in browser...
start "" "%FRONTEND_DIR%\index.html"

echo.
echo Skills Manager is ready!
echo.
echo Close this window to stop the server
echo.

pause
