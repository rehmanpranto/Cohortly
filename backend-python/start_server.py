"""
Server Start Script
Properly starts the FastAPI server with correct Python path
"""
import sys
from pathlib import Path
import uvicorn

# Add backend-python to path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

if __name__ == "__main__":
    print("🚀 Starting Cohortly FastAPI Server...")
    print(f"📁 Working Directory: {backend_dir}")
    print(f"🐍 Python Path: {sys.path[0]}")
    print("-" * 50)
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=5000,
        reload=False,
        log_level="info"
    )
