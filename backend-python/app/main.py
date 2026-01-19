from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.database import engine, Base

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

# Import routers
from app.api import auth, bootcamps, enrollments, assignments, leads

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(bootcamps.router, prefix="/api/v1/bootcamps", tags=["Bootcamps"])
app.include_router(enrollments.router, prefix="/api/v1/enrollments", tags=["Enrollments"])
app.include_router(assignments.router, prefix="/api/v1/assignments", tags=["Assignments"])
app.include_router(leads.router, prefix="/api/v1/leads", tags=["Leads"])

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
