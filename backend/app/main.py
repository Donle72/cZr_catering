"""
cZr Catering System - Backend API
Main application entry point with enhanced error handling and logging
"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy import text
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager
from datetime import datetime

from app.core.config import settings
from app.core.database import engine, get_db
from app.core.logging_config import setup_logging, get_logger
from app.core.exceptions import CateringException
from app.core.error_handlers import (
    catering_exception_handler,
    validation_exception_handler,
    integrity_error_handler,
    sqlalchemy_error_handler,
    global_exception_handler
)
from app.core.rate_limit import limiter
from app.db.base import Base
from app.api.v1.api import api_router
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

# Setup logging
logger = setup_logging()
app_logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle events for the application
    """
    # Startup
    app_logger.info("🚀 Starting cZr Catering System...")
    app_logger.info(f"📊 Environment: {settings.ENVIRONMENT}")
    app_logger.info(f"🔧 Debug Mode: {settings.DEBUG}")
    app_logger.info(f"🌐 CORS Origins: {', '.join(settings.CORS_ORIGINS)}")
    
    # Create tables (in production, use Alembic migrations)
    if settings.ENVIRONMENT == "development":
        app_logger.info("🔨 Creating database tables...")
        try:
            Base.metadata.create_all(bind=engine)
            app_logger.info("✅ Database tables created successfully")
        except Exception as e:
            app_logger.error(f"❌ Failed to create database tables: {str(e)}")
            raise
    
    yield
    
    # Shutdown
    app_logger.info("👋 Shutting down cZr Catering System...")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Sistema integral de gestión de catering con ingeniería gastronómica computacional",
    version="1.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan
)

# Add rate limiter to app state
app.state.limiter = limiter

# Register exception handlers
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_exception_handler(CateringException, catering_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_error_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_error_handler)
app.add_exception_handler(Exception, global_exception_handler)

# CORS Middleware with secure configuration
allowed_origins = settings.CORS_ORIGINS
if settings.ENVIRONMENT == "development":
    # In development, allow localhost variations
    allowed_origins = list(set(settings.CORS_ORIGINS + [
        "http://localhost:3020",
        "http://localhost:5173",
        "http://127.0.0.1:3020",
        "http://127.0.0.1:5173"
    ]))
    app_logger.info(f"🔓 CORS: Development mode - allowing {len(allowed_origins)} origins")
else:
    app_logger.info(f"🔒 CORS: Production mode - strict origin validation")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["*"],
    max_age=3600,  # Cache preflight requests for 1 hour
)

# GZip Middleware for response compression
app.add_middleware(GZipMiddleware, minimum_size=1000)

# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    """Log all requests"""
    start_time = datetime.utcnow()
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = (datetime.utcnow() - start_time).total_seconds()
    
    # Log request
    app_logger.info(
        f"{request.method} {request.url.path}",
        extra={
            "method": request.method,
            "path": str(request.url.path),
            "status_code": response.status_code,
            "duration_seconds": duration,
            "client_host": request.client.host if request.client else None
        }
    )
    
    return response

# Include API router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """
    Root endpoint - API information
    """
    return {
        "message": "🍽️ cZr Catering System API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs",
        "health": "/health",
        "environment": settings.ENVIRONMENT,
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    """
    Comprehensive health check endpoint for monitoring
    Checks database and returns system status
    """
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "environment": settings.ENVIRONMENT,
        "version": "1.0.0",
        "checks": {}
    }
    
    # Database check
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "message": "Database connection successful"
        }
        app_logger.debug("Health check: Database OK")
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }
        app_logger.error(f"Health check: Database FAILED - {str(e)}")
    
    # Determine HTTP status code
    status_code = 200 if health_status["status"] == "healthy" else 503
    
    return JSONResponse(content=health_status, status_code=status_code)

