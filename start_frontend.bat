@echo off
echo Starting Frontend UI...
echo.
echo Node version:
node --version
echo NPM version:
npm --version
echo.
cd ui-react

if not exist node_modules (
    echo Installing dependencies for the first time...
    echo This may take 2-3 minutes...
    call npm install
    if errorlevel 1 (
        echo.
        echo ERROR: Failed to install dependencies!
        echo Please check your internet connection and try again.
        pause
        exit /b 1
    )
)

echo.
echo Starting Next.js development server...
echo Frontend will run at: http://localhost:3000
echo.
echo Press Ctrl+C to stop
echo.
call npm run dev
pause
