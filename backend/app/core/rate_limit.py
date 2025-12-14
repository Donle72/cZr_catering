"""
Rate limiting configuration for cZr Catering System
Protects endpoints from abuse and ensures fair usage
"""
from slowapi import Limiter
from slowapi.util import get_remote_address


# Create limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["100/minute"],  # Global default
    storage_uri="memory://",  # Use memory storage (can be Redis in production)
)


# Rate limit configurations for different endpoint types
RATE_LIMITS = {
    # Critical operations - very restrictive
    "bulk_operations": "5/minute",
    "delete_operations": "10/minute",
    
    # Write operations - moderate
    "create_operations": "20/minute",
    "update_operations": "30/minute",
    
    # Read operations - generous
    "read_operations": "100/minute",
}
