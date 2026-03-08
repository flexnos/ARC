@echo off
title Installing Frontend Dependencies
color 0E
cls

echo ========================================
echo   INSTALLING FRONTEND DEPENDENCIES
echo ========================================
echo.
echo This will take 2-5 minutes on first run.
echo Please wait...
echo.
echo [Installing packages from npm...]
echo.

cd ui-react

call npm install --loglevel=progress

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo   SUCCESS! Installation complete!
    echo ========================================
    echo.
    echo You can now run the frontend!
    echo.
    echo Next steps:
    echo   1. Close this window
    echo   2. Run START_HERE.bat
    echo.
) else (
    echo.
    echo ========================================
    echo   ERROR! Installation failed!
    echo ========================================
    echo.
    echo Please check:
    echo   1. Internet connection
    echo   2. Node.js is installed
    echo   3. Run as Administrator if needed
    echo.
)

pause
