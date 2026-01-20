"""
Authentication utilities
"""
import bcrypt
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user
from app.models import UserRole


def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(password: str, password_hash: str) -> bool:
    """Verify a password against its hash"""
    password_bytes = password.encode('utf-8')
    hash_bytes = password_hash.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hash_bytes)


def role_required(roles):
    """
    Decorator to restrict access to specific roles
    Usage: @role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])
    """
    # Handle both list and single role
    if not isinstance(roles, (list, tuple)):
        roles = [roles]
    
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                flash('Please log in to access this page.', 'warning')
                return redirect(url_for('auth.login'))
            
            if current_user.role not in roles:
                flash('You do not have permission to access this page.', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator for admin-only routes"""
    return role_required([UserRole.ADMIN])(f)


def sales_required(f):
    """Decorator for sales/admin routes"""
    return role_required([UserRole.ADMIN, UserRole.SALES])(f)


def instructor_required(f):
    """Decorator for instructor/admin routes"""
    return role_required([UserRole.ADMIN, UserRole.INSTRUCTOR])(f)


def mentor_required(f):
    """Decorator for mentor/instructor/admin routes"""
    return role_required([UserRole.ADMIN, UserRole.INSTRUCTOR, UserRole.MENTOR])(f)


def student_required(f):
    """Decorator for student routes"""
    return role_required(UserRole.STUDENT)(f)
