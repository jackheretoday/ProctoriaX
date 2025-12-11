"""
Authentication middleware
Validates user session before each request
"""
from flask import session, redirect, url_for, request
from flask_login import current_user
from functools import wraps


def check_session_validity():
    """
    Check if session is valid before each request
    Called as before_request handler
    """
    # Skip for static files and auth endpoints
    if request.endpoint and (request.endpoint.startswith('static') or 
                             request.endpoint.startswith('auth')):
        return None
    
    # Check if user is authenticated
    if not current_user.is_authenticated:
        # Allow access to public endpoints
        if request.endpoint in ['index', 'health']:
            return None
        return redirect(url_for('auth.login'))
    
    # Check if account is active
    if not current_user.is_active:
        from flask import flash
        from flask_login import logout_user
        logout_user()
        flash('Your account has been deactivated.', 'danger')
        return redirect(url_for('auth.login'))
    
    # Check if account is locked
    if current_user.is_locked():
        from flask import flash
        from flask_login import logout_user
        logout_user()
        flash('Your account is locked due to too many failed login attempts.', 'danger')
        return redirect(url_for('auth.login'))
    
    return None


def require_authentication(f):
    """
    Decorator to require authentication for a view
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            from flask import flash
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function
