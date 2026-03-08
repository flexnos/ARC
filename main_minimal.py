"""
Minimal FastAPI backend - No model preloading
Use this for testing if server starts
"""
from fastapi import FastAPI
import uvicorn

app = FastAPI(title="Test API")

@app.get("/")
def root():
    return {"message": "Hello World", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy", "port": 8000}

@app.get("/test")
def test():
    return {"test": "success", "backend": "working"}

if __name__ == "__main__":
    print("=" * 50)
    print("Starting Minimal Backend Server...")
    print("=" * 50)
    print()
    print("Server will run at: http://localhost:8000")
    print("API docs at: http://localhost:8000/docs")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 50)
    print()
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
