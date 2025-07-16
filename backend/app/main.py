from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.settings import settings

# Create FastAPI application
app = FastAPI(
    title="ETA Agent System",
    description="AI-driven system for logistics anomaly handling",
    version="0.1.0",
    debug=settings.DEBUG
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://frontend:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "ETA Agent System API",
        "version": "0.1.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "debug": settings.DEBUG
    }

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "api": "ETA Agent System",
        "version": "0.1.0",
        "database": "SQLite",
        "ai_model": settings.OPENAI_MODEL,
        "environment": settings.ENVIRONMENT
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    ) 