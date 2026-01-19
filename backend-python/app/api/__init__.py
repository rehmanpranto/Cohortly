"""
API routes exports
"""

from .auth import router as auth_router
from .bootcamps import router as bootcamps_router
from .enrollments import router as enrollments_router
from .assignments import router as assignments_router
from .leads import router as leads_router

__all__ = [
    "auth_router",
    "bootcamps_router",
    "enrollments_router",
    "assignments_router",
    "leads_router",
]
