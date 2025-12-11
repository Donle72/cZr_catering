"""
cZr Catering System - Backend API
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.database import engine
from app.db.base import Base
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events for the application
    """
    # Startup
    print("🚀 Starting cZr Catering System...")
    print(f"📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    print(f"🔧 Environment: {settings.ENVIRONMENT}")
    
    # Create tables (in production, use Alembic migrations)
    if settings.ENVIRONMENT == "development":
        print("🔨 Creating database tables...")
        Base.metadata.create_all(bind=engine)
    
    yield
    
    # Shutdown
    print("👋 Shutting down cZr Catering System...")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema integral de gestión de catering con ingeniería gastronómica computacional",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GZip Middleware for response compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """
    Root endpoint - Health check
    """
    return {
        "message": "🍽️ cZr Catering System API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "environment": settings.ENVIRONMENT
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "environment": settings.ENVIRONMENT,
        "database": "connected"
    }
