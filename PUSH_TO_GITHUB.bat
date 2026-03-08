@echo off
echo ========================================
echo  GitHub Push - Professional Setup
echo ========================================
echo.

REM Check if git is installed
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git is not installed!
    echo Please install git from https://git-scm.com/
    pause
    exit /b 1
)

echo [1/6] Checking current directory...
cd /d "%~dp0"
echo Current directory: %CD%
echo.

echo [2/6] Cleaning up unnecessary files...
del /Q *.log 2>nul
del /Q *.db 2>nul
del /Q *.sqlite 2>nul
rmdir /S /Q __pycache__ 2>nul
rmdir /S /Q .pytest_cache 2>nul
rmdir /S /Q .vscode 2>nul
echo Cleanup complete!
echo.

echo [3/6] Initializing git repository...
if not exist ".git" (
    git init
    echo Git initialized!
) else (
    echo Git already initialized!
)
echo.

echo [4/6] Adding all files to git...
git add .
echo.

echo [5/6] Showing files to be committed...
echo ----------------------------------------
git status --short
echo ----------------------------------------
echo.

echo [6/6] Ready to commit?
echo.
set /p confirm="Press Y to commit and push, or any other key to cancel: "
if /i not "%confirm%"=="Y" (
    echo Cancelled by user
    pause
    exit /b 1
)

echo.
echo Creating commit...
git commit -m "feat: Initial commit - AI Answer Evaluation System

- FastAPI backend with multiple evaluation modes
- React/Next.js frontend with modern UI  
- Text, PDF, OCR, and batch processing support
- Auto-reference generation using AI
- Comprehensive HTML report generation
- Multi-metric scoring system
- Database integration with SQLAlchemy"

echo.
echo ========================================
echo  Next Steps:
echo ========================================
echo.
echo 1. Create a new repository on GitHub:
echo    https://github.com/new
echo.
echo 2. Repository name suggestion:
echo    answer-evaluation-system
echo.
echo 3. Then run these commands:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/answer-evaluation-system.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo ========================================
echo  Setup Complete!
echo ========================================
echo.

pause
