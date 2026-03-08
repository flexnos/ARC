@echo off
title Quick Start - Copy Paste Commands
color 0A
cls

echo ========================================
echo   MANUAL APPROACH - COPY THESE COMMANDS
echo ========================================
echo.
echo Choose ONE method below and copy-paste into PowerShell:
echo.
echo ========================================
echo METHOD 1: Automatic (Recommended!)
echo ========================================
echo.
echo Copy this SINGLE command into PowerShell:
echo.
echo powershell -ExecutionPolicy Bypass -File "d:\D down\bit\SETUP_MANUAL.ps1"
echo.
echo This does everything automatically!
echo.
pause
goto :methods

:methods
cls
echo ========================================
echo METHOD 2: Step by Step Commands
echo ========================================
echo.
echo Open PowerShell and run these ONE BY ONE:
echo.
echo --- STEP 1: Install Frontend ---
cd /d "d:\D down\bit\ui-react"
npm install
echo.
echo Wait for installation to complete...
echo Then continue with Step 2.
echo.
pause
cls

echo ========================================
echo --- STEP 2: Start Backend ---
echo ========================================
echo.
echo Open a NEW PowerShell window and run:
echo.
cd /d "d:\D down\bit"
python -m uvicorn main:app --host 127.0.0.1 --port 8000
echo.
pause
cls

echo ========================================
echo --- STEP 3: Start Frontend ---
echo ========================================
echo.
echo Go back to FIRST PowerShell window and run:
echo.
cd /d "d:\D down\bit\ui-react"
npm run dev
echo.
pause
cls

echo ========================================
echo   DONE! Both servers should be running!
echo ========================================
echo.
echo Backend:  http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Open your browser to: http://localhost:3000
echo.
echo Press any key to open browser now...
pause > nul
start http://localhost:3000

echo.
echo Browser opened! Check if you see the UI.
echo.
pause
