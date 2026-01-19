"""
Pydantic schemas for request/response validation
"""

from .user import (
    UserRegister,
    UserLogin,
    UserResponse,
    UserUpdate,
    TokenResponse,
    RefreshTokenRequest,
)
from .bootcamp import (
    BootcampCreate,
    BootcampUpdate,
    BootcampResponse,
    BootcampListResponse,
)
from .enrollment import (
    EnrollmentCreate,
    EnrollmentUpdate,
    EnrollmentResponse,
    EnrollmentListResponse,
)
from .assignment import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentResponse,
    AssignmentListResponse,
)
from .lead import (
    LeadCreate,
    LeadUpdate,
    LeadResponse,
    LeadListResponse,
)

__all__ = [
    # User schemas
    "UserRegister",
    "UserLogin",
    "UserResponse",
    "UserUpdate",
    "TokenResponse",
    "RefreshTokenRequest",
    # Bootcamp schemas
    "BootcampCreate",
    "BootcampUpdate",
    "BootcampResponse",
    "BootcampListResponse",
    # Enrollment schemas
    "EnrollmentCreate",
    "EnrollmentUpdate",
    "EnrollmentResponse",
    "EnrollmentListResponse",
    # Assignment schemas
    "AssignmentCreate",
    "AssignmentUpdate",
    "AssignmentResponse",
    "AssignmentListResponse",
    # Lead schemas
    "LeadCreate",
    "LeadUpdate",
    "LeadResponse",
    "LeadListResponse",
]
