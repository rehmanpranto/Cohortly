"""
Authentication middleware and dependencies
"""

from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User, UserRole
from app.utils.auth import verify_token


security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency to get current authenticated user from JWT token
    """
    token = credentials.credentials
    
    # Verify token
    payload = verify_token(token, "access")
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Get user from database
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
        )
    
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user


class RoleChecker:
    """
    Dependency class for role-based access control
    """
    def __init__(self, allowed_roles: list[UserRole]):
        self.allowed_roles = allowed_roles
    
    def __call__(self, current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {[role.value for role in self.allowed_roles]}",
            )
        return current_user


# Convenience functions for common role checks
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Require admin role"""
    return RoleChecker([UserRole.ADMIN])(current_user)


def require_instructor(current_user: User = Depends(get_current_user)) -> User:
    """Require instructor or admin role"""
    return RoleChecker([UserRole.ADMIN, UserRole.INSTRUCTOR])(current_user)


def require_sales(current_user: User = Depends(get_current_user)) -> User:
    """Require sales or admin role"""
    return RoleChecker([UserRole.ADMIN, UserRole.SALES])(current_user)


def require_mentor(current_user: User = Depends(get_current_user)) -> User:
    """Require mentor, instructor, or admin role"""
    return RoleChecker([UserRole.ADMIN, UserRole.INSTRUCTOR, UserRole.MENTOR])(current_user)
