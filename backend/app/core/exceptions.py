"""
Custom exceptions for the cZr Catering System
Provides structured error handling with clear messages
"""
from typing import Any, Dict, Optional


class CateringException(Exception):
    """Base exception for catering system"""
    
    def __init__(
        self, 
        message: str, 
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ResourceNotFoundError(CateringException):
    """Raised when a resource is not found"""
    
    def __init__(self, resource: str, id: Any):
        super().__init__(
            message=f"{resource} with id {id} not found",
            status_code=404,
            details={"resource": resource, "id": id}
        )


class DuplicateResourceError(CateringException):
    """Raised when trying to create a duplicate resource"""
    
    def __init__(self, resource: str, field: str, value: Any):
        super().__init__(
            message=f"{resource} with {field}='{value}' already exists",
            status_code=409,
            details={"resource": resource, "field": field, "value": value}
        )


class ValidationError(CateringException):
    """Raised when validation fails"""
    
    def __init__(self, message: str, field: Optional[str] = None):
        details = {"field": field} if field else {}
        super().__init__(
            message=message,
            status_code=422,
            details=details
        )


class BusinessRuleError(CateringException):
    """Raised when a business rule is violated"""
    
    def __init__(self, message: str, rule: Optional[str] = None):
        details = {"rule": rule} if rule else {}
        super().__init__(
            message=message,
            status_code=400,
            details=details
        )


class AuthenticationError(CateringException):
    """Raised when authentication fails"""
    
    def __init__(self, message: str = "Authentication failed"):
        super().__init__(
            message=message,
            status_code=401
        )


class AuthorizationError(CateringException):
    """Raised when authorization fails"""
    
    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(
            message=message,
            status_code=403
        )


class DatabaseError(CateringException):
    """Raised when a database operation fails"""
    
    def __init__(self, message: str, operation: Optional[str] = None):
        details = {"operation": operation} if operation else {}
        super().__init__(
            message=message,
            status_code=500,
            details=details
        )
