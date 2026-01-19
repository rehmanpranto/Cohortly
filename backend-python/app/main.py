from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.config import settings
from app.database import engine, Base
import traceback
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="Cohortly API",
    description="Bootcamp Management System - Python/FastAPI Version",
    version="2.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.CORS_ORIGIN, "*"],  # Allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handling middleware
@app.middleware("http")
async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as e:
        logger.error(f"❌ Error processing request {request.url}: {str(e)}")
        logger.error(traceback.format_exc())
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": f"Internal server error: {str(e)}"}
        )

# Import routers
from app.api import (
    auth_router,
    bootcamps_router,
    enrollments_router,
    assignments_router,
    leads_router,
)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(bootcamps_router, prefix="/api/v1")
app.include_router(enrollments_router, prefix="/api/v1")
app.include_router(assignments_router, prefix="/api/v1")
app.include_router(leads_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {
        "message": "Welcome to Cohortly API",
        "version": "2.0.0",
        "framework": "FastAPI",
        "docs": "/api/docs"
    }

@app.get("/api/v1/health")
async def health():
    return {
        "status": "healthy",
        "framework": "FastAPI",
        "version": "2.0.0",
        "database": "PostgreSQL"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=settings.PORT)
