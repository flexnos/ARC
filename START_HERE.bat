@echo off
title Answer Evaluation System - Launcher
color 0A
cls

echo ========================================
echo   ANSWER EVALUATION SYSTEM
echo ========================================
echo.
echo Starting servers...
echo.
echo This will open TWO separate windows:
echo   [1] Backend API Server  - http://localhost:8000
echo   [2] Frontend React App  - http://localhost:3000
echo.
echo Keep BOTH windows open to use the application!
echo.
echo Press any key to start...
pause > nul
echo.

:: Start backend
start "Backend Server" cmd /k "start_backend.bat"

:: Wait 2 seconds
timeout /t 2 /nobreak > nul

:: Start frontend
start "Frontend UI" cmd /k "start_frontend.bat"

echo.
echo ========================================
echo  Servers are starting!
echo ========================================
echo.
echo Check the two new windows for status.
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo You can close this window now.
echo ========================================
timeout /t 5
exit
