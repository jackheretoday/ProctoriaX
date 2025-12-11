"""
Authorization middleware
Checks user permissions for role-based access control
"""
from flask import abort
from flask_login import current_user
from functools import wraps


def check_user_permissions(required_role):
    """
    Check if current user has required role
    
    Args:
        required_role: Role required (admin, teacher, student)
        
    Raises:
        403: If user doesn't have required role
    """
    if not current_user.is_authenticated:
        abort(401)  # Unauthorized
    
    if not current_user.has_role(required_role):
        abort(403)  # Forbidden


def require_role(role):
    """
    Decorator to require specific role for a view
    
    Args:
        role: Required role (admin, teacher, student)
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            
            if not current_user.has_role(role):
                from flask import flash
                flash(f'Access denied. {role.title()} role required.', 'danger')
                abort(403)
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def require_admin(f):
    """Decorator to require admin role"""
    return require_role('admin')(f)


def require_teacher(f):
    """Decorator to require teacher role"""
    return require_role('teacher')(f)


def require_student(f):
    """Decorator to require student role"""
    return require_role('student')(f)
