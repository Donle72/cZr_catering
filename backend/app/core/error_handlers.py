"""
Global error handlers for FastAPI application
Provides consistent error responses across the API
"""
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from datetime import datetime
import logging
import traceback

from app.core.exceptions import CateringException
from app.core.config import settings

logger = logging.getLogger(__name__)


async def catering_exception_handler(request: Request, exc: CateringException) -> JSONResponse:
    """Handle custom catering exceptions"""
    logger.warning(
        f"Catering exception: {exc.message}",
        extra={
            "path": str(request.url),
            "method": request.method,
            "status_code": exc.status_code,
            "details": exc.details
        }
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.message,
            "details": exc.details,
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors"""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        f"Validation error: {len(errors)} field(s)",
        extra={
            "path": str(request.url),
            "errors": errors
        }
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "ValidationError",
            "message": "Request validation failed",
            "errors": errors,
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def integrity_error_handler(request: Request, exc: IntegrityError) -> JSONResponse:
    """Handle database integrity errors"""
    logger.error(
        f"Database integrity error: {str(exc.orig)}",
        extra={
            "path": str(request.url),
            "method": request.method
        }
    )
    
    # Extract useful information from the error
    error_message = str(exc.orig)
    
    # Try to make the error message more user-friendly
    if "duplicate key" in error_message.lower():
        message = "A record with this value already exists"
    elif "foreign key" in error_message.lower():
        message = "Referenced record does not exist"
    elif "not null" in error_message.lower():
        message = "Required field is missing"
    else:
        message = "Database constraint violation"
    
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "error": "IntegrityError",
            "message": message,
            "details": {"database_error": error_message} if settings.DEBUG else {},
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def sqlalchemy_error_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """Handle general SQLAlchemy errors"""
    logger.error(
        f"Database error: {str(exc)}",
        extra={
            "path": str(request.url),
            "method": request.method
        },
        exc_info=True
    )
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "DatabaseError",
            "message": "A database error occurred",
            "details": {"error": str(exc)} if settings.DEBUG else {},
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle all unhandled exceptions"""
    logger.error(
        f"Unhandled exception: {str(exc)}",
        extra={
            "path": str(request.url),
            "method": request.method,
            "exception_type": type(exc).__name__
        },
        exc_info=True
    )
    
    # In production, don't expose internal error details
    if settings.ENVIRONMENT == "production":
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": "InternalServerError",
                "message": "An unexpected error occurred. Please try again later.",
                "path": str(request.url.path),
                "timestamp": datetime.utcnow().isoformat()
            }
        )
    
    # In development, provide more details
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": type(exc).__name__,
            "message": str(exc),
            "traceback": traceback.format_exc().split("\n") if settings.DEBUG else None,
            "path": str(request.url.path),
            "timestamp": datetime.utcnow().isoformat()
        }
    )
