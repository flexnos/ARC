@echo off
title Testing Backend - Minimal
color 0B
cls

echo ========================================
echo   TESTING BACKEND STARTUP
echo ========================================
echo.
echo Python version:
python --version
echo.
echo Starting minimal FastAPI server...
echo.
echo This should start in 2-3 seconds...
echo.

python main_minimal.py

echo.
echo ========================================
echo   Server stopped or failed!
echo ========================================
pause
