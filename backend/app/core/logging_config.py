"""
Logging configuration for cZr Catering System
Provides structured logging with JSON format for production
"""
import logging
import sys
from datetime import datetime
from typing import Any, Dict
from app.core.config import settings


class StructuredFormatter(logging.Formatter):
    """
    Custom formatter that outputs logs in a structured format
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record with structured data"""
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno
        }
        
        # Add extra fields if present
        if hasattr(record, "extra"):
            log_data.update(record.extra)
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        # Format as JSON-like string for easy parsing
        if settings.ENVIRONMENT == "production":
            import json
            return json.dumps(log_data)
        else:
            # Human-readable format for development
            base = f"{log_data['timestamp']} | {log_data['level']:8} | {log_data['logger']:20} | {log_data['message']}"
            if record.exc_info:
                base += f"\n{log_data['exception']}"
            return base


def setup_logging() -> logging.Logger:
    """
    Configure application logging
    Returns the root logger
    """
    # Get root logger
    logger = logging.getLogger()
    
    # Set level based on environment
    if settings.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    
    # Remove existing handlers
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(StructuredFormatter())
    logger.addHandler(console_handler)
    
    # File handler for errors (optional)
    if settings.ENVIRONMENT == "production":
        error_handler = logging.FileHandler("errors.log")
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(StructuredFormatter())
        logger.addHandler(error_handler)
    
    # Suppress noisy loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    
    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance with the given name
    """
    return logging.getLogger(name)


# Convenience functions for structured logging
def log_info(logger: logging.Logger, message: str, **kwargs: Any) -> None:
    """Log info message with extra data"""
    logger.info(message, extra=kwargs)


def log_warning(logger: logging.Logger, message: str, **kwargs: Any) -> None:
    """Log warning message with extra data"""
    logger.warning(message, extra=kwargs)


def log_error(logger: logging.Logger, message: str, **kwargs: Any) -> None:
    """Log error message with extra data"""
    logger.error(message, extra=kwargs, exc_info=True)


def log_debug(logger: logging.Logger, message: str, **kwargs: Any) -> None:
    """Log debug message with extra data"""
    logger.debug(message, extra=kwargs)
