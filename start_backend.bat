@echo off
echo Starting Backend Server...
echo.
echo Python version:
python --version
echo.
echo Installing/Checking dependencies...
pip install -q fastapi uvicorn python-multipart pydantic
echo.
echo Starting FastAPI server...
echo Backend will run at: http://localhost:8000
echo API docs at: http://localhost:8000/docs
echo.
echo Press Ctrl+C to stop
echo.
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --log-level info
pause
